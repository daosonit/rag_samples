-- FINAL PROJECT: ENTERPRISE KNOWLEDGE BASE
-- File: src/database/schema.sql

-- 1. Bật extension pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Tạo bảng cho Final Project
CREATE TABLE IF NOT EXISTS enterprise_kb_chunks (
    id uuid PRIMARY KEY,
    content text NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    
    -- Dùng cho BGE-M3 (1024 chiều)
    embedding vector(1024) NOT NULL,
    
    -- Multi-tenancy (Phân quyền người dùng/công ty)
    tenant_id text NOT NULL,
    
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Tạo HNSW Index tối ưu hóa tìm kiếm tốc độ cao
CREATE INDEX IF NOT EXISTS enterprise_kb_hnsw_index 
ON enterprise_kb_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 4. Kích hoạt Row Level Security (RLS)
ALTER TABLE enterprise_kb_chunks ENABLE ROW LEVEL SECURITY;

-- 5. Tạo Policy phân quyền
CREATE POLICY "Enterprise Tenant Isolation" 
ON enterprise_kb_chunks 
FOR ALL 
USING (
    tenant_id = current_setting('app.current_tenant', true)
);

-- 6. Tạo Hàm tìm kiếm RPC cho SupabaseVectorStore
CREATE OR REPLACE FUNCTION match_enterprise_kb_chunks (
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
        enterprise_kb_chunks.id,
        enterprise_kb_chunks.content,
        enterprise_kb_chunks.metadata,
        1 - (enterprise_kb_chunks.embedding <=> query_embedding) AS similarity
    FROM enterprise_kb_chunks
    WHERE enterprise_kb_chunks.metadata @> filter
    ORDER BY enterprise_kb_chunks.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
