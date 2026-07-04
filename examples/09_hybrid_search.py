import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_classic.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.documents import Document

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

print("1. Đang nạp mô hình Vector Embedding (Chuyên gia Ý nghĩa)...")
embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
)

# A. RETRIEVER 1: TÌM KIẾM THEO NGỮ NGHĨA (Vector Search)
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="document_chunks_hf",
    query_name="match_documents_hf",
)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# B. RETRIEVER 2: TÌM KIẾM THEO TỪ KHÓA CHÍNH XÁC (Keyword Search - BM25)
print("2. Đang khởi tạo máy tìm kiếm Từ Khóa BM25 (Chuyên gia Soi Chữ)...")
# Trong thực tế, bạn sẽ tạo cột Full-text search (tsvector) trên Supabase.
# Ở bài học này, ta tạo một tập dữ liệu nhỏ chứa MÃ SỐ để BM25 chạy local minh họa độ chính xác.
docs_list = [
    "Hợp đồng số 123/HĐ-AIVN ký ngày 01/01/2023 về việc cung cấp phần mềm RAG. Giám đốc Sơn đã ký.",
    "Hợp đồng số 124/HĐ-AIVN ký ngày 05/01/2023 về việc thuê máy chủ ảo VPS. Kỹ sư trưởng đã duyệt.",
    "Hợp đồng số 125/HĐ-AIVN ký ngày 10/01/2023 về việc tư vấn AI cho ngân hàng. Có mộc đỏ.",
]
bm25_docs = [Document(page_content=t) for t in docs_list]
keyword_retriever = BM25Retriever.from_documents(bm25_docs)
keyword_retriever.k = 2

# C. KẾT HỢP (HYBRID SEARCH) VỚI ENSEMBLE RETRIEVER
print("3. Đang hợp nhất 2 chuyên gia (Trọng số: 50% Vector, 50% Keyword)...")
hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, keyword_retriever],
    weights=[
        0.5,
        0.5,
    ],  # Bạn có thể đổi: 0.3 vector, 0.7 keyword nếu hệ thống bạn quá nhiều mã số hợp đồng
)


def demo_hybrid_search():
    # Câu hỏi chứa MÃ SỐ CHÍNH XÁC.
    # Nếu chỉ dùng Vector, nó sẽ bị bối rối giữa hợp đồng 123, 124 và 125 vì "ngữ nghĩa" của chúng y hệt nhau (đều là hợp đồng cty AIVN).
    cau_hoi = "Cho tôi xem nội dung hợp đồng 124/HĐ-AIVN"

    print(f"\n💬 Người dùng hỏi: '{cau_hoi}'")
    print(
        "🤖 Đang tiến hành Hybrid Search (Gộp điểm Keyword và điểm Vector bằng thuật toán RRF)...\n"
    )

    results = hybrid_retriever.invoke(cau_hoi)

    print(f"✅ Đã tìm thấy các tài liệu phù hợp nhất sau khi hợp nhất kết quả:")
    for i, doc in enumerate(results):
        print(f"--- Top {i+1} ---")
        print(doc.page_content)


if __name__ == "__main__":
    demo_hybrid_search()
