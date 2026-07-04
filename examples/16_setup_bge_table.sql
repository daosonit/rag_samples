-- BÀI 6.4: THIẾT LẬP BẢNG DÀNH RIÊNG CHO BGE-M3 (VECTOR 1024 CHIỀU)

-- 1. Bật extension pgvector (Nếu chưa bật)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Tạo bảng mới tinh để chứa siêu Vector 1024 chiều
CREATE TABLE IF NOT EXISTS rag_bge_chunks (
    id uuid PRIMARY KEY,
    content text NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    
    -- QUAN TRỌNG NHẤT: BGE-M3 đòi hỏi 1024 chiều (MiniLM cũ chỉ có 384)
    embedding vector(1024) NOT NULL,
    
    -- (Tùy chọn tương lai): Lưu trữ Sparse Vector của BGE-M3
    -- sparse_vector jsonb,
    
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Thêm trường tenant_id để phân quyền dữ liệu (Multi-tenancy) theo chuẩn Bài 5.2
ALTER TABLE rag_bge_chunks ADD COLUMN IF NOT EXISTS tenant_id text;

-- Kích hoạt và cấu hình Row Level Security (RLS)
ALTER TABLE rag_bge_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "BGE Tenant Isolation" 
ON rag_bge_chunks 
FOR ALL 
USING (
    tenant_id = current_setting('app.current_tenant', true)
);

-- 3. Tạo chỉ mục HNSW tốc độ cao cho 1024 chiều
-- Lưu ý: Vector lớn hơn nên hàm khoảng cách vẫn là vector_cosine_ops
CREATE INDEX IF NOT EXISTS bge_hnsw_index 
ON rag_bge_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 4. Tạo Hàm tìm kiếm (RPC Function) dành riêng cho BGE-M3
CREATE OR REPLACE FUNCTION match_bge_chunks (
    query_embedding vector(1024),
    match_count int DEFAULT 5,
    filter jsonb DEFAULT '{}'::jsonb
)
RETURNS TABLE (
    id uuid,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        rag_bge_chunks.id,
        rag_bge_chunks.content,
        rag_bge_chunks.metadata,
        1 - (rag_bge_chunks.embedding <=> query_embedding) AS similarity
    FROM rag_bge_chunks
    WHERE rag_bge_chunks.metadata @> filter
    ORDER BY rag_bge_chunks.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
