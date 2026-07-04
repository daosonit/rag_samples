-- FILE NÀY CHỈ ĐỂ THAM KHẢO VÀ CHẠY TRONG GIAO DIỆN SQL CỦA SUPABASE --

-- 1. Bật tính năng Row Level Security (RLS) trên bảng RAG
ALTER TABLE rag_document_chunks ENABLE ROW LEVEL SECURITY;

-- 2. Đảm bảo bảng có 1 cột để phân biệt người dùng (Ví dụ: tenant_id hoặc user_id)
-- Nếu dùng bảng cũ, ta có thể lấy từ cột metadata, nhưng tạo cột riêng sẽ nhanh hơn.
ALTER TABLE rag_document_chunks ADD COLUMN IF NOT EXISTS tenant_id text;

-- 3. Cài đặt Chính sách Bảo mật (Policy)
-- Nguyên tắc: Người dùng (tenant) nào thì chỉ được đọc/ghi dữ liệu của chính người đó
CREATE POLICY "Tenant Isolation Policy" 
ON rag_document_chunks 
FOR ALL 
USING (
    -- Trong thực tế với Supabase Auth, bạn dùng: auth.uid() = user_id
    -- Ở đây ta dùng hàm current_setting để lập trình viên Python truyền vào
    tenant_id = current_setting('app.current_tenant', true)
);

-- HẬU QUẢ KHI ĐÃ BẬT RLS:
-- Nếu một Hacker chạy lệnh: SELECT * FROM rag_document_chunks;
-- Kết quả sẽ trả về 0 dòng! (Database tự động chặn lại vì Hacker không có thẻ tenant_id hợp lệ)
