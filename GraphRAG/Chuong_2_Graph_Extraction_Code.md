# 📖 TẬP 2: TRÍCH XUẤT ĐỒ THỊ TỪ VĂN BẢN (GRAPH EXTRACTION)

*Nằm trong Bộ Bách khoa toàn thư GraphRAG 5 Tập*
*Tác giả: Giáo sư AI & Đào Sơn*

---

## MỤC LỤC
1. [Nghệ thuật Băm dữ liệu (Chunking Strategy)](#phan-1)
2. [Lựa chọn Model (LLM) phù hợp](#phan-2)
3. [Prompt Engineering Đỉnh cao cho Trích xuất Triples](#phan-3)
4. [Tự động hóa với LangChain (LLMGraphTransformer)](#phan-4)

---

## 1. NGHỆ THUẬT BĂM DỮ LIỆU (CHUNKING STRATEGY) <a name="phan-1"></a>

Trong Vector RAG, người ta thường dùng **RecursiveCharacterTextSplitter** để cắt nhỏ văn bản thành các đoạn 500-1000 ký tự (Chunks).
Nhưng trong GraphRAG, nếu bạn cắt 1 câu ra làm 2 đoạn (ví dụ: Chunk 1: *"Steve Jobs sinh ra tại"*, Chunk 2: *"Mỹ"*), LLM sẽ không bao giờ nhìn thấy bức tranh toàn cảnh để tạo ra mũi tên `(Steve Jobs)-[:BORN_IN]->(Mỹ)`.

**Quy tắc cắt Chunk cho GraphRAG:**
- **Chunk Size lớn hơn:** Thường để kích thước Chunk lớn (1000 - 2000 tokens) để LLM có đủ bối cảnh (Context).
- **Chunk Overlap cực lớn:** Độ chồng chéo (Overlap) phải ở mức 20-30% để đảm bảo các mối quan hệ nằm vắt ngang giữa 2 đoạn văn không bị mất dấu.
- **Tốt nhất là cắt theo Semantic (Ngữ nghĩa):** Cắt theo từng đoạn văn (Paragraph) hoặc từng phần (Section) của tài liệu.

---

## 2. LỰA CHỌN MODEL (LLM) PHÙ HỢP <a name="phan-2"></a>

Trích xuất đồ thị (Graph Extraction) là tác vụ đòi hỏi khả năng bám sát định dạng JSON (JSON Following) cực kỳ khắt khe. Nếu LLM trả về dư một dấu phẩy (`,`) hoặc lỡ tay viết thêm *"Dưới đây là kết quả của bạn:"*, toàn bộ code Python parsing sẽ bị Crash (Sập).

- **Hạng S (Dành cho Doanh nghiệp - Đắt tiền nhưng an toàn):** `gpt-4o`, `claude-3-5-sonnet`. Bọn này trả JSON hoàn hảo 100%.
- **Hạng A (Dành cho Local, Chuyên gia Code & JSON):** `qwen2.5:14b`, `qwen2.5:32b`. Dòng Qwen 2.5 cực mạnh trong việc tuân thủ cấu trúc dữ liệu.
- **Hạng B (Tốt nhưng thỉnh thoảng lỗi):** `llama3.1:8b`.
- **Hạng C (Không nên dùng cho tác vụ này):** `gemma2:27b` (Vì cửa sổ ngữ cảnh quá ngắn, dễ bị tràn khi xử lý Chunk lớn).

---

## 3. PROMPT ENGINEERING ĐỈNH CAO CHO TRÍCH XUẤT TRIPLES <a name="phan-3"></a>

Một kỹ sư AI nghiệp dư sẽ viết Prompt: *"Hãy tìm các thực thể và mối quan hệ."*
Một kỹ sư AI chuyên nghiệp (Expert) sẽ viết Prompt khóa chặt mọi rủi ro như sau:

```text
Bạn là một chuyên gia Khai phá Dữ liệu (Data Mining).
Nhiệm vụ của bạn là đọc đoạn văn bản sau và trích xuất một Đồ thị Tri thức.

[CÁC BƯỚC THỰC HIỆN]
1. Xác định các Thực thể chính (Nodes) bao gồm: PERSON, ORGANIZATION, LOCATION, CONCEPT.
2. Trích xuất các Mối quan hệ (Edges) nối giữa chúng. Tên mối quan hệ phải viết HOA toàn bộ bằng Tiếng Anh (VD: FOUNDED, LOCATED_IN).
3. Gộp các thực thể trùng lặp (Ví dụ "Apple Inc." và "Apple" phải dùng chung ID là "Apple").

[RÀNG BUỘC ĐẦU RA - BẮT BUỘC]
- Tuyệt đối KHÔNG trả lời thêm bất cứ lời chào, lời giải thích nào.
- Chỉ xuất duy nhất một mảng JSON có định dạng như sau:
[
  {
    "head": "Steve Jobs",
    "head_type": "PERSON",
    "relation": "FOUNDED",
    "tail": "Apple",
    "tail_type": "ORGANIZATION"
  }
]

Văn bản cần xử lý:
{text}
```

*Mẹo: Khi gọi API qua Ollama hoặc OpenAI, nhớ luôn bật tham số `response_format={"type": "json_object"}` để ép LLM không được lảm nhảm.*

---

## 4. TỰ ĐỘNG HÓA VỚI LANGCHAIN (LLMGraphTransformer) <a name="phan-4"></a>

Nếu tự code tay bằng Prompt ở trên, bạn sẽ phải tự viết code gỡ lỗi (Parse) JSON, tự bắt lỗi (Try/Catch) nếu LLM sinh sai.
May mắn thay, LangChain đã đóng gói tất cả vào một Class siêu cấp tên là `LLMGraphTransformer`. Thư viện này tự động chia Chunk, gọi LLM, ép JSON, và thậm chí tự động đẩy luôn vào Neo4j!

**Đoạn Code Thực chiến End-to-End:**

```python
import os
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_models import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document

# 1. Kết nối Neo4j
graph = Neo4jGraph(
    url="bolt://192.168.1.99:7687", 
    username="neo4j", 
    password="your_password"
)

# 2. Khởi tạo LLM qua Ollama
# Lưu ý: Bắt buộc dùng model mạnh về JSON format (vd: qwen2.5:14b)
llm = ChatOllama(
    base_url="http://192.168.1.99:11434",
    model="qwen2.5:14b",
    temperature=0  # Quan trọng: Đặt bằng 0 để LLM không sáng tạo lung tung
)

# 3. Khởi tạo Kẻ biến hình (Transformer)
# Allowed_nodes và Allowed_relationships giúp khóa chặt không cho LLM tự bịa ra nhãn linh tinh
llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Person", "Company", "Product", "Location"],
    allowed_relationships=["FOUNDED", "PRODUCES", "LOCATED_IN", "CEO_OF"],
    strict_mode=True # Ép LLM bám sát danh sách trên
)

# 4. Giả lập một Document (Trong thực tế, bạn sẽ dùng PyPDFLoader để đọc file)
text = """
Năm 1976, Steve Jobs và Steve Wozniak thành lập Apple tại California. 
Apple sản xuất chiếc iPhone đầu tiên vào năm 2007.
"""
documents = [Document(page_content=text)]

# 5. Chuyển đổi Văn bản -> Đồ thị (Khâu này tốn thời gian nhất vì LLM phải đọc và suy nghĩ)
print("🧠 Đang vắt óc suy nghĩ và trích xuất Triples...")
graph_documents = llm_transformer.convert_to_graph_documents(documents)

# Xem thử kết quả LLM trích xuất được gì
for doc in graph_documents:
    print(f"Nodes: {doc.nodes}")
    print(f"Relationships: {doc.relationships}")

# 6. Chèn tất cả vào Database chỉ bằng 1 dòng lệnh
# Thư viện sẽ tự động chạy lệnh MERGE để tránh trùng lặp
graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
print("✅ Đã ghi đồ thị vào Neo4j thành công!")
```

### 💡 LỜI KHUYÊN TỪ GIÁO SƯ
1. Đừng bao giờ ném một cuốn sách 1000 trang vào `LLMGraphTransformer` rồi đi ngủ! Vì LLM sẽ xử lý Tuần tự (Sequential), mất cả ngày và có thể sập giữa chừng. 
2. Trong Production, hãy đưa mảng `documents` vào một Message Queue (như RabbitMQ / Celery), chạy đa luồng (Multi-threading), và cho 3-4 con LLM (Ollama) cùng xâu xé dữ liệu.
3. Nếu hệ thống báo lỗi Parse JSON, hãy kiểm tra lại con LLM của bạn (có thể `temperature` chưa đặt bằng 0, hoặc Model quá yếu như 8B).

---
*(Hết Tập 2. Mời bạn đón đọc Tập 3: Mổ xẻ chi tiết Kiến trúc khổng lồ của Microsoft GraphRAG).*
