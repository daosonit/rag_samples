# GIÁO TRÌNH ĐÀO TẠO GRAPHRAG: TỪ "ZERO" ĐẾN "PROFESSOR"

Chào mừng bạn đến với khóa đào tạo toàn diện về **GraphRAG** (Graph Retrieval-Augmented Generation). Giáo trình này được thiết kế theo lộ trình chuẩn từ việc xây dựng nền tảng lý thuyết cho đến triển khai thực tế các hệ thống AI phức tạp cỡ doanh nghiệp, giúp bạn làm chủ hoàn toàn công nghệ này.

---

## 🎯 TẠI SAO LẠI LÀ GRAPHRAG?

RAG truyền thống (dựa trên Vector Search) rất tốt trong việc tìm kiếm văn bản tương đồng, nhưng lại **thất bại** khi phải:

1. Kết nối các điểm dữ liệu rời rạc (Connecting the dots).
2. Trả lời các câu hỏi tổng hợp mang tính vĩ mô (Global synthesis).
3. Hiểu các mối quan hệ phức tạp, gián tiếp.

GraphRAG giải quyết điều này bằng cách kết hợp sức mạnh của **Sơ đồ tri thức (Knowledge Graph)** và **LLM**.

---

## 📚 [/] CHẶNG 1: XÂY DỰNG NỀN TẢNG (TỪ ZERO ĐẾN BEGINNER)

_Mục tiêu: Hiểu rõ khái niệm, không viết code phức tạp, định hình tư duy Đồ thị._

### [x] Bài 1.1: Ôn tập RAG Truyền thống & Nỗi đau của Vector Search

- Nhắc lại Chunking, Embeddings, Vector Database.
- Hạn chế: Khó nhận diện ngữ cảnh xuyên suốt, dễ bị nhiễu thông tin (noise).
- Demo lý thuyết: Đặt một câu hỏi yêu cầu tổng hợp toàn bộ cuốn sách, Vector RAG sẽ thất bại thế nào?

### [x] Bài 1.2: Nhập môn Sơ đồ Tri thức (Knowledge Graph - KG)

- Cấu trúc cốt lõi: **Nodes** (Thực thể: Người, Địa điểm, Khái niệm), **Edges** (Mối quan hệ) và **Properties** (Thuộc tính).
- Khái niệm **Triple** (Subject - Predicate - Object). Ví dụ: `(Steve Jobs) -[FOUNDED]-> (Apple)`.
- Giới thiệu Graph Database cơ bản: Neo4j (Cypher), NetworkX (Python RAM-based).

### [x] Bài 1.3: GraphRAG là gì?

- Định nghĩa kiến trúc GraphRAG cơ bản.
- So sánh: **Vector-based RAG** vs **Graph-based RAG**.

---

## 🛠 [/] CHẶNG 2: THỰC HÀNH GRAPHRAG CƠ BẢN (INTERMEDIATE)

_Mục tiêu: Tự code một hệ thống GraphRAG từ đầu để hiểu cơ chế hoạt động, có thể chạy trên tập dữ liệu nhỏ._

### [x] Bài 2.1: Trích xuất Tri thức (Knowledge Extraction)

- Sử dụng LLM để trích xuất (Entity & Relation Extraction) từ Text.
- Kỹ thuật Prompt Engineering để xuất ra định dạng JSON chứa các Node và Edge.
- **Thực hành:** Viết script Python nhận một đoạn văn báo chí và nhả ra list các Triples.

### [x] Bài 2.2: Xây dựng Knowledge Graph đầu tiên

- Lưu trữ Triples vừa tạo vào một Graph DB.
- **Thực hành:** Dùng Python `NetworkX` để dựng đồ thị trên RAM và vẽ đồ thị (Visualisation). Hoặc kết nối tạo Node/Edge bằng `neo4j-driver`.

### [x] Bài 2.3: Kỹ thuật Retrieval trên Graph

- **Phương pháp 1: Text-to-Cypher.** Yêu cầu LLM chuyển câu hỏi tự nhiên của user thành câu lệnh Cypher, query DB, rồi dùng LLM tóm tắt lại.
- **Phương pháp 2: Entity Retrieval (Sub-graph Extraction).** Trích xuất thực thể từ câu hỏi (vd: "Apple"), tìm Node "Apple" trong Graph, lấy tất cả các node lân cận (depth 1 hoặc 2), biến chúng thành Text Context và đưa cho LLM.

### [x] Bài 2.4: Khai thác các Framework có sẵn

- Sử dụng `KnowledgeGraphIndex` của **LlamaIndex**.
- Sử dụng `GraphCypherQAChain` của **LangChain**.

---

## 🚀 [/] CHẶNG 3: GRAPHRAG NÂNG CAO & KIẾN TRÚC MICROSOFT (ADVANCED)

_Mục tiêu: Nắm vững hệ thống Microsoft GraphRAG - chuẩn mực hiện tại của ngành._

### [x] Bài 3.1: Triết lý của Microsoft GraphRAG

- Tại sao trích xuất Entity đơn thuần là chưa đủ? Sự cần thiết của **Tóm tắt (Summarization)** ở cấp độ đồ thị.
- Đọc hiểu quy trình: Source Docs -> Text Chunks -> Entity/Relationships -> **Element Summaries**.

### [x] Bài 3.2: Graph Communities (Phân cụm đồ thị)

- Hiểu thuật toán **Leiden Algorithm** trong việc gom nhóm các node thành các Cộng đồng (Communities).
- Ý tưởng phân cấp: Từ vi mô (cụm nhỏ) đến vĩ mô (cụm lớn).
- **Community Summaries:** Dùng LLM tóm tắt toàn bộ thông tin của từng cụm.

### [x] Bài 3.3: Global Search vs Local Search

- **Local Search:** Kỹ thuật tìm kiếm đi từ các Node cụ thể, kết hợp với các Community liền kề (dành cho câu hỏi đặc tả).
- **Global Search:** Kỹ thuật Map-Reduce trên toàn bộ Community Summaries để trả lời câu hỏi mang tính khái quát (vd: "Chủ đề chính của tập dữ liệu này là gì?").

### [x] Bài 3.4: Triển khai Microsoft GraphRAG Open Source

- Cài đặt thư viện `microsoft/graphrag`.
- Cấu hình Prompt tuning cho phù hợp với Domain (Y tế, Pháp luật,...).
- Chạy Indexing pipeline (cảnh báo: sẽ rất tốn token API).
- Thực thi truy vấn.

---

## 🧠 [/] CHẶNG 4: KIẾN TRÚC HYBRID & TỐI ƯU HÓA (EXPERT)

_Mục tiêu: Đưa GraphRAG vào Production, giảm chi phí, tăng tính linh hoạt._

### [x] Bài 4.1: Kiến trúc Hybrid (Vector + Graph)

- Graph không hoàn hảo để search semantic, Vector thì không hiểu quan hệ. -> Cần gộp cả hai.
- Thiết kế hệ thống: Khớp Entity bằng Vector Search, sau đó mở rộng bằng Graph Traversal.
- Thuật toán Reranking kết hợp điểm số Vector và Graph.

### [x] Bài 4.2: Bài toán Entity Resolution (Giải quyết thực thể)

- Làm sao xử lý khi Graph có cả "Steve Jobs", "S. Jobs", "CEO Apple" nhưng đều chỉ 1 người?
- Entity Deduplication (Gộp thực thể) bằng các mô hình nhúng văn bản hoặc LLM.

### [x] Bài 4.3: Tối ưu chi phí trích xuất đồ thị (Cost Optimization)

- Không dùng GPT-4 cho mọi bước. Sử dụng SLM (Small Language Models) như Llama 3 8B, hoặc mô hình chuyên dụng cho Information Extraction (như GLiNER, REBEL) để giảm chi phí 90%.

### [x] Bài 4.4: Dynamic Graph Updates (Cập nhật đồ thị động)

- Cách thiết kế hệ thống khi có document mới thêm vào: Chỉ upsert các Node/Edge mới và cập nhật lại cụm (Community) bị ảnh hưởng, thay vì build lại từ đầu.

---

## 🎓 [/] CHẶNG 5: CẤP ĐỘ GIÁO SƯ (PROFESSOR / RESEARCHER)

_Mục tiêu: Đủ khả năng đọc hiểu các Paper mới nhất, đánh giá hệ thống và tự thiết kế Framework của riêng bạn._

### [x] Bài 5.1: Đánh giá hệ thống (Evaluation metrics)

- Làm sao biết GraphRAG tốt hơn Vector RAG trong Use-case của bạn?
- Các Metrics: Độ bao phủ của Graph (Graph Completeness), Độ chính xác quan hệ (Relation Accuracy), Comprehensiveness & Diversity (theo paper của Microsoft).

### [x] Bài 5.2: Tương lai của Knowledge Graph và LLM và các báo cáo khoa học (Papers)

- Nghiên cứu các phương pháp kết hợp LLM Reasoning với Graph:
  - **RoG (Reasoning on Graphs):** LLM tạo ra các đường đi (paths) trên graph trước khi sinh câu trả lời.
  - **G-Retriever:** Graph Neural Networks (GNNs) kết hợp với LLM.
- Multi-Agent GraphRAG: Các Agents cùng nhau đi trên đồ thị để thu thập manh mối (Clues).

### [x] Bài 5.3: Đồ án tốt nghiệp (The Masterpiece)

- Xây dựng file tổng hợp toàn bộ kiến thức. Input: Tập tin PDF.
  2. Dùng LLM trích xuất Triples, lưu vào Neo4j.
  3. Áp dụng thuật toán nhúng (Node2Vec) hoặc nhúng nội dung Node vào Milvus/Qdrant.
  4. Viết Router Agent: Tự quyết định câu hỏi nào dùng Vector Search, câu hỏi nào dùng Graph Traversal.
  5. Xuất báo cáo chứng minh nó vượt trội hơn RAG truyền thống.

---

## 🛠 DANH MỤC CÔNG CỤ & TÀI LIỆU CHUẨN BỊ

1. **Môi trường:** Python 3.10+, Jupyter Notebook, Poetry/UV.
2. **Database:** Tải Neo4j Desktop (hoặc dùng Neo4j AuraDB miễn phí).
3. **Thư viện chính:**
   - `networkx` (cho Đồ thị bộ nhớ)
   - `neo4j` (Python driver)
   - `langchain-community`, `llama-index-graph-stores-neo4j`
   - `graphrag` (Của Microsoft)
4. **LLM Provider:** Khuyên dùng OpenAI (GPT-4o) cho việc extraction chính xác ở giai đoạn đầu, sau đó dùng Gemini hoặc Anthropic để so sánh.

---

**BẠN ĐÃ SẴN SÀNG CHƯA?**
Để bắt đầu, hãy chuẩn bị môi trường Python tại thư mục này, tạo một Virtual Environment, cài đặt `networkx` và `openai`, sau đó chúng ta sẽ bắt tay vào **Chặng 1**!
