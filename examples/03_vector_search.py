import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def demo_vector_search():
    # 1. Tạo 1 Vector giả (mock) dài 1536 chiều
    # Trong thực tế, vector này được lấy từ OpenAI hoặc SentenceTransformers
    mock_vector = [0.01] * 1536

    # 2. Thêm thử 1 bản ghi vào database
    print("Đang thêm tài liệu mẫu vào Supabase...")
    supabase.table("document_chunks").insert(
        {
            "content": "Đây là tài liệu bí mật về doanh thu quý 3 của công ty.",
            "embedding": mock_vector,
        }
    ).execute()

    # 3. Gọi hàm RPC để tìm kiếm tài liệu có vector tương đồng
    print("Đang tìm kiếm tài liệu...")
    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": mock_vector,  # Truyền vector câu hỏi vào
            "match_threshold": 0.8,  # Chỉ lấy kết quả giống > 80%
            "match_count": 3,  # Lấy Top 3 kết quả
        },
    ).execute()

    print("\n✅ Kết quả tìm kiếm:")
    for row in response.data:
        print(f"- ID: {row['id']}")
        print(f"- Độ giống (Similarity): {row['similarity']:.4f}")
        print(f"- Nội dung: {row['content']}\n")


if __name__ == "__main__":
    demo_vector_search()
