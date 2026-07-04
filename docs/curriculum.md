# LỘ TRÌNH ĐÀO TẠO MASTER RAG VỚI SUPABASE

## 🗂️ Module 1: Nền tảng (Fundamentals)

- [x] **Bài 1.1: Giải phẫu hệ thống RAG.** Chi tiết về Ingestion, Retrieval, và Generation.
- [x] **Bài 1.2: Embedding Models.** Biến văn bản thành số (Vector). Cách các mô hình như OpenAI `text-embedding-3`, BGE, Cohere hoạt động.
- [x] **Bài 1.3: Kỹ thuật Chunking cơ bản.** Cắt nhỏ tài liệu (Fixed-size, Recursive Character) - Tại sao cắt sai sẽ làm hỏng RAG?
- [x] **Case Study Doanh Nghiệp:** Cách **Morgan Stanley** áp dụng RAG nội bộ để 16,000 chuyên viên tài chính truy vấn thư viện nghiên cứu.

## 🗂️ Module 2: Xây dựng Bộ nhớ với Supabase (Vector Store)

- [x] **Bài 2.1: Kiến trúc Supabase & pgvector.** Hiểu về cơ sở dữ liệu PostgreSQL mở rộng.
- [x] **Bài 2.2: Kết nối Python với Supabase tự host (Self-hosted).** Cấu hình biến môi trường kết nối tới `192.168.1.99`, tạo bảng vector bằng SQL.
- [x] **Bài 2.3: Indexing trong pgvector (HNSW vs IVFFlat).** Tối ưu hóa tốc độ tìm kiếm khi dữ liệu lên tới hàng triệu records.

## 🗂️ Module 3: Xây dựng Pipeline RAG (Core Implementation)

- [x] **Bài 3.1: Vector Search & Similarity.** Thực hiện truy vấn (Cosine similarity, Inner product) bằng Supabase.
- [x] **Bài 3.2: Tích hợp LangChain / LlamaIndex.** Kết nối Prompt -> Retriever (Supabase) -> LLM.
- [x] **Bài 3.3: Semantic Chunking.** Kỹ thuật cắt tài liệu dựa trên ý nghĩa ngữ nghĩa thay vì độ dài vật lý.
- [x] **Bài 3.4: Thuật toán Upsert.** Chống trùng lặp dữ liệu Vector (Data Duplication) bằng cách tạo ID ổn định (Stable ID).

## 🗂️ Module 4: Nâng cấp độ chính xác (Advanced RAG)

- [x] **Bài 4.1: Query Expansion & HyDE.** Làm gì khi câu hỏi của người dùng quá ngắn hoặc mơ hồ?
- [x] **Bài 4.2: Hybrid Search (Keyword + Vector).** Kết hợp sức mạnh của từ khóa truyền thống (BM25) và ngữ nghĩa (Vector) bằng EnsembleRetriever.
- [x] **Bài 4.3: Re-ranking.** Dùng mô hình Cross-Encoder để chấm điểm lại kết quả tìm kiếm với độ chính xác tuyệt đối.
- [x] **Case Study Doanh Nghiệp:** Cách **Klarna** giảm 25% khối lượng công việc của tổng đài viên nhờ hệ thống RAG kết hợp Hybrid Search.

## 🗂️ Module 5: Thực tiễn, Bảo mật & Đánh giá (Production-Ready)

- [x] **Bài 5.1: Đánh giá RAG.** Sử dụng LLM-as-a-judge để đo lường Faithfulness (Độ trung thành) và Answer Relevance (Độ bám sát câu hỏi).
- [x] **Bài 5.2: Quản lý quyền truy cập (Access Control) trong Supabase RAG.** Sử dụng Row Level Security (RLS) để cô lập dữ liệu (Multi-tenancy).
- [x] **Bài 5.3: Caching & Tối ưu tài nguyên.** Sử dụng SQLiteCache để lưu trữ câu trả lời, giảm tải CPU/GPU và tiết kiệm API.

## 🗂️ Module 6: Chuyên sâu về BAAI/bge-m3 (Enterprise-grade Embedding)

- [x] **Bài 6.1: Giải phẫu BGE-M3.** Cấu trúc Multi-lingual (Đa ngôn ngữ) và sức mạnh thực sự của 1024 chiều Vector.
- [x] **Bài 6.2: Triển khai Server Local.** Cài đặt môi trường, sử dụng thư viện `FlagEmbedding`, sinh ra 3 loại Vector cùng lúc.
- [x] **Bài 6.3: Cỗ máy 3 trong 1.** Khai thác Dense Retrieval (Tìm theo ý nghĩa), Sparse Retrieval (Tìm từ khóa BM25) và ColBERT (Đối sánh đa Vector) của BGE-M3.
- [x] **Bài 6.4: Thực chiến với Supabase.** Thiết lập bảng mới cho `vector(1024)` và nhúng BGE-M3 vào Pipeline LangChain.

## 🚀 Project Cuối Khóa: "Enterprise Knowledge Base AI"

- [ ] Xây dựng API bằng FastAPI cho phép upload file PDF (tài liệu công ty).
- [ ] Hệ thống tự động Chunking, Embedding bằng siêu mẫu BGE-M3 và lưu vào Supabase (`192.168.1.99`).
- [ ] Giao diện/API cho phép chat với tài liệu, áp dụng Hybrid Search (Sparse + Dense) và Re-ranking.
