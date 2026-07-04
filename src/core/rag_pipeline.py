import os
import torch
from dotenv import load_dotenv
from supabase.client import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# Load biến môi trường từ .env
load_dotenv()

# Bật bộ nhớ đệm cho LLM để phản hồi tức thì với câu hỏi trùng lặp
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

class RAGPipeline:
    """
    Namespace class quản lý toàn bộ các core components của hệ thống RAG.
    Sử dụng Singleton pattern để tái sử dụng các models, tránh việc load lại model (memory leak / chậm).
    """
    _supabase_client: Client = None
    _embeddings: HuggingFaceEmbeddings = None
    _vector_store: SupabaseVectorStore = None
    _llm: ChatOllama = None

    @classmethod
    def get_device(cls) -> str:
        """Tự động chọn phần cứng tốt nhất (CUDA/MPS/CPU)"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    @classmethod
    def get_supabase(cls) -> Client:
        """Khởi tạo hoặc lấy kết nối Supabase hiện tại"""
        if cls._supabase_client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("Thiếu cấu hình SUPABASE_URL hoặc SUPABASE_KEY trong .env")
            cls._supabase_client = create_client(url, key)
        return cls._supabase_client

    @classmethod
    def get_bge_embeddings(cls) -> HuggingFaceEmbeddings:
        """Khởi tạo siêu mẫu BGE-M3 (Offline) một lần duy nhất và lưu vào RAM"""
        if cls._embeddings is None:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "local_models",
                "bge-m3",
            )
            
            if not os.path.exists(model_path):
                print(f"Cảnh báo: Không tìm thấy thư mục {model_path}. Fallback sang mạng BAAI/bge-m3.")
                model_path = "BAAI/bge-m3"

            cls._embeddings = HuggingFaceEmbeddings(
                model_name=model_path,
                model_kwargs={"device": cls.get_device()},
                encode_kwargs={"normalize_embeddings": True},
            )
        return cls._embeddings

    @classmethod
    def get_vector_store(cls) -> SupabaseVectorStore:
        """Lấy Vector Store trỏ vào bảng enterprise_kb_chunks"""
        if cls._vector_store is None:
            cls._vector_store = SupabaseVectorStore(
                client=cls.get_supabase(),
                embedding=cls.get_bge_embeddings(),
                table_name="enterprise_kb_chunks",
                query_name="match_enterprise_kb_chunks",
            )
        return cls._vector_store

    @classmethod
    def get_llm(cls) -> ChatOllama:
        """Khởi tạo LLM Qwen2.5 qua Ollama"""
        if cls._llm is None:
            ollama_url = os.environ.get("OLLAMA_URL", "http://192.168.1.99:11434")
            cls._llm = ChatOllama(base_url=ollama_url, model="qwen2.5:7b", temperature=0.1)
        return cls._llm
