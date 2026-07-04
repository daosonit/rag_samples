import os
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

print("1. Đang nạp mô hình Vector...")
embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
)

print("2. Đang cắt văn bản (Chunking)...")
text = """
Công ty TNHH AI Việt Nam (AIVN) được thành lập năm 2021.
Sản phẩm chủ đạo của công ty là các hệ thống Trí tuệ nhân tạo (AI) giúp tự động hóa quy trình cho doanh nghiệp.
Gần đây, công ty vừa ra mắt hệ thống RAG Enterprise có khả năng đọc hiểu hàng triệu tài liệu.
Giám đốc hiện tại là ông Nguyễn Văn Sơn.
"""

text_splitter = CharacterTextSplitter(separator="\n", chunk_size=50, chunk_overlap=0)
docs = text_splitter.create_documents([text])

print("\n3. Đang tạo mã UUID ổn định (Stable UUID5) cho từng đoạn văn...")
stable_ids = []
for i, doc in enumerate(docs):
    # DÙNG NỘI DUNG ĐỂ BĂM RA UUID:
    # Nếu nội dung văn bản không đổi, UUID này vĩnh viễn không đổi.
    chunk_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content))
    stable_ids.append(chunk_uuid)

    # Gắn thêm một ít metadata cho chuẩn thực chiến
    doc.metadata = {"source": "bao_cao_thuong_nien.txt", "author": "Giám đốc Sơn"}

    print(f" - Chunk {i+1}: {chunk_uuid} | '{doc.page_content[:20]}...'")

print("\n4. Đang nạp vào bảng 'rag_document_chunks' (Quá trình Upsert)...")
# Khởi tạo SupabaseVectorStore trỏ vào Bảng mới và Hàm mới
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="rag_document_chunks",
    query_name="match_rag_chunks",
)

# Chèn tài liệu kèm theo bộ ID chuẩn mực (upsert)
vector_store.add_documents(documents=docs, ids=stable_ids)

print(
    "✅ Đã hoàn tất Upsert chuẩn mực! Bạn có thể chạy lại file này bao nhiêu lần tùy thích, dữ liệu sẽ không bao giờ bị nhân đôi."
)
