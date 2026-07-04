import os
import uuid
from dotenv import load_dotenv
from supabase.client import create_client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document
import torch

load_dotenv()

print("1. Đang khởi tạo siêu mẫu BAAI/bge-m3 (Dense 1024 chiều)...")

# Tự động chọn phần cứng tốt nhất
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"-> Đang chạy mô hình trên thiết bị: {device.upper()}")

# Khởi tạo mô hình Embedding BGE-M3 qua LangChain (Load từ Offline)
bge_embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/bge-m3",
    model_kwargs={"device": device},
    encode_kwargs={
        "normalize_embeddings": True
    },  # Cosine similarity luôn cần normalize = True
)

print("2. Kết nối tới Supabase Database...")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# 3. Chuẩn bị tài liệu
docs = [
    Document(
        page_content="Công ty AIVN được thành lập năm 2024, chuyên đào tạo và triển khai AI Enterprise.",
        metadata={"source": "wikipedia", "tenant_id": "tenant_001"},
    ),
    Document(
        page_content="Morgan Stanley dùng RAG để tiết kiệm hàng triệu đô la mỗi năm nhờ việc tối ưu tìm kiếm tài liệu tài chính.",
        metadata={"source": "news", "tenant_id": "tenant_001"},
    ),
]

# Tạo ID cố định (Stable UUID) chống trùng lặp theo bài học 3.4
NAMESPACE_RAG = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
ids = [str(uuid.uuid5(NAMESPACE_RAG, doc.page_content)) for doc in docs]

print(
    f"3. Đang đưa {len(docs)} tài liệu lên bảng rag_bge_chunks (Vector 1024 chiều)..."
)
# Liên kết LangChain với bảng mới tạo
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=bge_embeddings,
    table_name="rag_bge_chunks",
    query_name="match_bge_chunks",
)

vector_store.add_documents(documents=docs, ids=ids)
print("✅ Upsert dữ liệu thành công!")

print("\n4. Chạy thử Tìm kiếm Ngữ Nghĩa (Dense Search) trên Vector 1024 chiều:")
query = "Công ty nào dạy về Trí tuệ nhân tạo?"
print(f"💬 Câu hỏi: '{query}'")

# Tìm kiếm trên Database với quyền của Công ty 1 (tenant_001)
print("\n--- Đóng vai nhân viên Công ty 1 (tenant_001) ---")
results_1 = vector_store.similarity_search(query, k=1, filter={"tenant_id": "tenant_001"})
if results_1:
    print(f"🤖 Tìm thấy: {results_1[0].page_content}")
else:
    print("❌ Không tìm thấy dữ liệu.")

# Tìm kiếm trên Database với quyền của Công ty 2 (tenant_002) - Cố tình nhìn trộm
print("\n--- Đóng vai nhân viên Công ty 2 (tenant_002) - Tính nhìn trộm ---")
results_2 = vector_store.similarity_search(query, k=1, filter={"tenant_id": "tenant_002"})
if results_2:
    print(f"🤖 Tìm thấy: {results_2[0].page_content}")
else:
    print("❌ Bị chặn! Không tìm thấy dữ liệu (Dù dữ liệu vẫn nằm trong Database).")
