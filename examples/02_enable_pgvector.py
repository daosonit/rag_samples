import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")


def enable_pgvector():
    print(
        f"Đang kết nối tới CSDL: {db_url.split('@')[1] if '@' in db_url else 'Unknown'}"
    )
    try:
        # Kết nối tới PostgreSQL
        conn = psycopg2.connect(db_url)
        # Bắt buộc phải bật autocommit để chạy lệnh CREATE EXTENSION
        conn.autocommit = True
        cursor = conn.cursor()

        # 1. Bật extension pgvector
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("✅ Đã bật thành công sức mạnh AI (pgvector) cho PostgreSQL!")

        # 2. Tạo bảng lưu trữ tài liệu với cột vector
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                id bigserial primary key,
                content text not null,
                embedding vector(1536) -- Chuẩn bị sẵn 1536 chiều cho OpenAI
            );
        """
        )
        print(
            "✅ Đã tạo thành công bảng 'document_chunks' chứa cột 'embedding' kiểu vector(1536)."
        )

        # 3. Tạo hàm RPC (Stored Procedure) để tìm kiếm Vector
        cursor.execute(
            """
            CREATE OR REPLACE FUNCTION match_documents (
              query_embedding vector(1536),
              match_threshold float,
              match_count int
            )
            RETURNS TABLE (
              id bigint,
              content text,
              similarity float
            )
            LANGUAGE sql STABLE
            AS $$
              SELECT
                id,
                content,
                1 - (embedding <=> query_embedding) AS similarity
              FROM document_chunks
              WHERE 1 - (embedding <=> query_embedding) > match_threshold
              ORDER BY similarity DESC
              LIMIT match_count;
            $$;
            """
        )
        print("✅ Đã tạo thành công hàm RPC 'match_documents' giấu trong lòng Database.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
    enable_pgvector()
