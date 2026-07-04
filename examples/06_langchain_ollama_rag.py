import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Khai báo thư viện kết nối Ollama
from langchain_ollama import ChatOllama

# 1. Tải biến môi trường
load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
ollama_url = os.environ.get("OLLAMA_URL")  # Đã cấu hình OLLAMA_URL trong file .env

if not ollama_url:
    raise ValueError("Thiếu OLLAMA_URL trong file .env")

supabase: Client = create_client(supabase_url, supabase_key)

# 2. Cài đặt Mô hình Embedding (Local hoàn toàn)
print("Đang nạp mô hình Embedding nội bộ...")
embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
)

# 3. Kết nối Supabase Vector Store
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="document_chunks_hf",
    query_name="match_documents_hf",
)

# 4. Cài đặt LLM 100% Local (Ollama)
print(f"Đang kết nối tới Ollama ({ollama_url})...")
# Sử dụng qwen2.5:14b vì đây là mô hình có tiếng Việt cực tốt trong danh sách của bạn
llm = ChatOllama(
    model="qwen2.5:14b",
    base_url=ollama_url,
    temperature=0.1,  # Trả lời nghiêm túc, bám sát tài liệu
)

# 5. Thiết lập Prompt
prompt = ChatPromptTemplate.from_template(
    """
Bạn là trợ lý AI nội bộ của công ty. Hãy trả lời câu hỏi dựa trên các thông tin được cung cấp dưới đây.
Tuyệt đối KHÔNG sử dụng kiến thức bên ngoài. Nếu thông tin không có, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu".

THÔNG TIN ĐƯỢC CUNG CẤP:
{context}

CÂU HỎI CỦA NGƯỜI DÙNG: {question}

CÂU TRẢ LỜI CỦA BẠN:
"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chú ý: Ở đây tôi tăng k=4 để lấy đủ tài liệu (tránh cú lừa thiếu Doanh thu như bài 3.2)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 6. RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    cau_hoi = "Giám đốc công ty là ai và doanh thu quý 3 năm 2023 đạt bao nhiêu?"
    print(f"\n💬 Người dùng hỏi: {cau_hoi}")
    print("🤖 Ollama (Qwen2.5 14B) đang suy nghĩ...\n")

    ket_qua = rag_chain.invoke(cau_hoi)
    print(f"👉 AI Trả lời: {ket_qua}")
