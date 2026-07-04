import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")


def setup_standard_rag_table():
    print(
        f"Đang kết nối tới CSDL: {db_url.split('@')[1] if '@' in db_url else 'Unknown'}"
    )
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()

        # 1. Kích hoạt extension uuid
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        print("✅ Đã bật extension hỗ trợ UUID (uuid-ossp).")

        # 2. Tạo bảng RAG chuẩn mực
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rag_document_chunks (
                id uuid primary key default uuid_generate_v4(),
                content text not null,
                metadata jsonb default '{}',
                embedding vector(384),
                created_at timestamp with time zone default timezone('utc'::text, now())
            );
        """
        )
        print("✅ Đã tạo bảng chuẩn 'rag_document_chunks'.")

        # 3. Tạo HNSW Index
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS rag_document_chunks_embedding_idx 
            ON rag_document_chunks 
            USING hnsw (embedding vector_cosine_ops);
        """
        )
        print(
            "✅ Đã tạo HNSW Index để tối ưu tốc độ tìm kiếm Vector gấp hàng nghìn lần."
        )

        # 4. Tạo hàm tìm kiếm RPC có hỗ trợ lọc Metadata
        cursor.execute(
            """
            CREATE OR REPLACE FUNCTION match_rag_chunks (
              query_embedding vector(384),
              match_count int DEFAULT 5,
              filter jsonb DEFAULT '{}'
            )
            RETURNS TABLE (
              id uuid,
              content text,
              metadata jsonb,
              similarity float
            )
            LANGUAGE plpgsql
            AS $$
            #variable_conflict use_column
            BEGIN
              RETURN QUERY
              SELECT
                id,
                content,
                metadata,
                1 - (rag_document_chunks.embedding <=> query_embedding) AS similarity
              FROM rag_document_chunks
              WHERE metadata @> filter
              ORDER BY rag_document_chunks.embedding <=> query_embedding
              LIMIT match_count;
            END;
            $$;
        """
        )
        print("✅ Đã tạo hàm tìm kiếm RPC 'match_rag_chunks' tích hợp bộ lọc (filter).")

        cursor.close()
        conn.close()
        print("\n🎉 THÀNH CÔNG! Database đã được trang bị vũ khí tận răng.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
    setup_standard_rag_table()
