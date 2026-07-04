import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_ollama import ChatOllama
from langchain_classic.retrievers.multi_query import MultiQueryRetriever

# Bật log của LangChain để chúng ta có thể nhìn thấy AI "suy nghĩ" ra các câu hỏi phụ
logging.basicConfig()
logging.getLogger("langchain_classic.retrievers.multi_query").setLevel(logging.INFO)

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
ollama_url = os.environ.get("OLLAMA_URL", "http://192.168.1.99:11434")

supabase: Client = create_client(supabase_url, supabase_key)
embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="document_chunks_hf",
    query_name="match_documents_hf",
)

# LLM dùng để "Nghĩ ra" các câu hỏi đồng nghĩa (Nhiệt độ 0.5 để nó sáng tạo một chút)
llm = ChatOllama(model="qwen2.5:14b", base_url=ollama_url, temperature=0.5)

from langchain_core.prompts import PromptTemplate

# Ghi đè câu lệnh Prompt mặc định của LangChain bằng Tiếng Việt
# Để ép con Qwen (vốn gốc là tiếng Trung) phải xuất ra câu hỏi phụ bằng Tiếng Việt
vi_prompt = PromptTemplate(
    input_variables=["question"],
    template="""Bạn là một trợ lý AI chuyên nghiệp. Nhiệm vụ của bạn là tạo ra 3 phiên bản câu hỏi khác nhau dựa trên câu hỏi gốc để giúp tìm kiếm tài liệu tốt hơn. 
YÊU CẦU TỐI THƯỢNG: Bắt buộc phải sinh ra câu hỏi bằng TIẾNG VIỆT. Tuyệt đối không dùng tiếng Trung Quốc, không dùng tiếng Anh.

Câu hỏi gốc: {question}

3 phiên bản câu hỏi (mỗi câu nằm trên 1 dòng):""",
)

# Bọc Vector Store bình thường vào bên trong MultiQueryRetriever kèm theo Prompt tùy chỉnh
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
    llm=llm,
    prompt=vi_prompt,
)


def demo_query_expansion():
    print(
        "⚠️ Mô phỏng tình huống: Người dùng lười biếng nhập một câu hỏi rất MƠ HỒ và NGẮN CỤT LỦN."
    )
    cau_hoi = "AI VN bán gì?"

    print(f"\n💬 Truy vấn gốc của user: '{cau_hoi}'")
    print(
        "🤖 LLM đang tự động phân tích và 'dịch' câu hỏi này thành nhiều phiên bản chuyên nghiệp hơn...\n"
    )

    # Thực hiện truy vấn.
    # Lúc này LLM sẽ tự động sinh ra 3 câu hỏi phụ khác nhau để quét mọi góc độ của vấn đề.
    # Sau đó nó tự đi tìm kiếm Database cho cả 3 câu, rồi gộp tất cả kết quả lại (loại bỏ trùng lặp).
    unique_docs = retriever_from_llm.invoke(cau_hoi)

    print(
        f"\n✅ Đã tìm thấy {len(unique_docs)} tài liệu không trùng lặp sau khi lưới bủa vây (Query Expansion):"
    )
    for i, doc in enumerate(unique_docs):
        print(f"--- Tài liệu {i+1} ---")
        print(doc.page_content)


if __name__ == "__main__":
    demo_query_expansion()
