import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

print("1. Đang nạp mô hình Embedding...")
embeddings = HuggingFaceEmbeddings(
    model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="document_chunks_hf",
    query_name="match_documents_hf",
)

# Giả lập dữ liệu cần đưa vào hệ thống (giống bài trước)
docs = [
    "Công ty TNHH AI Việt Nam được thành lập năm 2021, chuyên về giải pháp trí tuệ nhân tạo.",
    "Doanh thu quý 3 năm 2023 của công ty AI Việt Nam đạt 50 tỷ đồng, tăng trưởng 20% so với cùng kỳ.",
    "Giám đốc điều hành (CEO) hiện tại của công ty AI Việt Nam là ông Nguyễn Văn Sơn.",
    "Sản phẩm chủ đạo của công ty là hệ thống RAG Enterprise tích hợp Supabase.",
]


def generate_stable_id(text: str) -> str:
    """
    Tạo một ID ổn định dựa trên NỘI DUNG của văn bản.
    Bất kể chạy bao nhiêu lần, đoạn text này vẫn sinh ra đúng 1 mã ID duy nhất.
    Vì cột 'id' trong Supabase của chúng ta là BIGINT, nên ta sẽ cắt lấy 15 ký tự hex
    để đảm bảo số sinh ra nằm trong giới hạn của BIGINT (chứa được tối đa 19 chữ số).
    """
    hex_digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    # Chuyển 15 ký tự hex đầu tiên thành số nguyên (int), sau đó ép sang chuỗi (str)
    bigint_id = int(hex_digest[:15], 16)
    return str(bigint_id)


def demo_upsert():
    print("\n2. Đang tạo ID ổn định (Stable ID) cho từng đoạn văn bản...")
    ids = []
    for doc in docs:
        stable_id = generate_stable_id(doc)
        ids.append(stable_id)
        print(f" - {doc[:30]}... -> ID: {stable_id}")

    print("\n3. Tiến hành chèn dữ liệu bằng thuật toán UPSERT (Update or Insert)...")
    print(
        "Nếu ID đã tồn tại trong Database, nó sẽ Ghi Đè (Update). Nếu chưa có, nó sẽ Thêm Mới (Insert)."
    )

    # LangChain SupabaseVectorStore hỗ trợ truyền tham số 'ids'.
    # Khi có 'ids', nó sẽ sử dụng lệnh upsert() của Supabase thay vì insert() thông thường.
    vector_store.add_texts(
        texts=docs, ids=ids, metadatas=[{"source": "demo_upsert"}] * len(docs)
    )

    print(
        "\n✅ Thành công! Dù bạn có chạy file này 100 lần, Database vẫn chỉ có đúng 4 dòng dữ liệu, không bao giờ sinh ra rác (Duplicates)!"
    )


if __name__ == "__main__":
    demo_upsert()
