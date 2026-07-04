from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()


def demo_semantic_chunking():
    print("1. Đang tải mô hình Embedding nội bộ...")
    embeddings = HuggingFaceEmbeddings(
        model_name="./local_models/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Một đoạn văn bản phức tạp gộp nhiều chủ đề
    text = """Trí tuệ nhân tạo (AI) đang thay đổi thế giới. Các công ty công nghệ lớn trên toàn cầu đang đầu tư hàng tỷ USD vào lĩnh vực này để chạy đua vũ trang. 
Trái ngược với quy mô toàn cầu, doanh thu của công ty TNHH AI Việt Nam trong quý 3 năm 2023 chỉ đạt 50 tỷ đồng. Dù vậy, ông Nguyễn Văn Sơn, giám đốc công ty, cho biết con số này đã tăng trưởng 20% so với cùng kỳ năm ngoái, một tín hiệu rất đáng mừng.
Sản phẩm chủ đạo giúp công ty sinh lời là hệ thống RAG Enterprise tích hợp Supabase. Hệ thống này giúp các doanh nghiệp tự động hóa việc tra cứu tài liệu nội bộ một cách an toàn, bảo mật và hoàn toàn tự động."""

    print("\n2. Đang phân tích và cắt tài liệu theo ý nghĩa (Semantic Chunking)...")

    # Khởi tạo công cụ cắt theo ngữ nghĩa
    # breakpoint_threshold_type="percentile" nghĩa là nó sẽ tính toán độ tương đồng giữa các câu liên tiếp.
    # Nếu sự khác biệt giữa 2 câu vượt qua một ngưỡng (ví dụ đỉnh của biểu đồ), nó sẽ "chặt" làm đôi.
    text_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
    # Tiến hành cắt tài liệu
    docs = text_splitter.create_documents([text])

    print(f"\n✅ Đã cắt đoạn văn trên thành {len(docs)} mẩu (chunks) khác nhau:\n")
    for i, doc in enumerate(docs):
        print(f"--- Chunk {i+1} ---")
        print(doc.page_content)
        print("-" * 30 + "\n")


if __name__ == "__main__":
    demo_semantic_chunking()
