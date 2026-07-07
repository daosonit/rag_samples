# 📖 TẬP 4: KIẾN TRÚC HYBRID & TỐI ƯU HÓA (CẤP ĐỘ CHUYÊN GIA)

*Nằm trong Bộ Bách khoa toàn thư GraphRAG 5 Tập*
*Tác giả: Giáo sư AI & Đào Sơn*

---

## MỤC LỤC
1. [Kiến trúc Hybrid: Kết hợp Vector và Graph](#phan-1)
2. [Bài toán Giải quyết Thực thể (Entity Resolution)](#phan-2)
3. [Tối ưu chi phí bằng SLM (Multi-model Architecture)](#phan-3)
4. [Cập nhật Đồ thị động (Incremental Indexing)](#phan-4)

---

## 1. KIẾN TRÚC HYBRID: KẾT HỢP VECTOR VÀ GRAPH <a name="phan-1"></a>

GraphRAG không phải là "viên đạn bạc" (Silver Bullet) có thể thay thế hoàn toàn Vector RAG.
- Nếu người dùng hỏi bóng gió: *"Trong cuốn tiểu thuyết, có nhân vật nào tính cách u ám không?"* -> GraphRAG sẽ "ngáo" vì không tìm thấy Node nào tên là `Nhân vật tính cách u ám`. Nhưng Vector RAG lại giải quyết câu này cực tốt nhờ tìm kiếm theo Semantic (Ngữ nghĩa/Cảm xúc).
- Nếu người dùng gõ sai chính tả: *"S. Jobs"* thay vì `"Steve Jobs"` -> GraphRAG gãy.

### Trái tim của Hybrid RAG: Vector Index trong Neo4j
Kể từ phiên bản 5.11, Neo4j đã tích hợp sẵn tính năng Vector. Bạn không cần dùng thêm PostgreSQL (pgvector) hay Supabase nữa. Mọi thứ được giải quyết trong 1 câu lệnh Cypher:

**Quy trình Hybrid:**
1. Khi có câu hỏi của người dùng, biến câu hỏi đó thành Vector bằng Embedding Model (vd: `nomic-embed-text`).
2. Dùng Cypher để tìm Node có tên mang ý nghĩa giống với câu hỏi nhất (Vector Search).
3. Từ Node đó, bung ra các Node xung quanh (Graph Traversal).

```cypher
// Đoạn Cypher thần thánh kết hợp cả Vector và Graph
CALL db.index.vector.queryNodes('node_embeddings', 5, $question_vector)
YIELD node AS startNode, score
MATCH (startNode)-[r*1..2]-(neighbor) // Đi sâu 2 cấp độ từ Node tìm được
RETURN startNode.id, score, neighbor.id
ORDER BY score DESC
```

---

## 2. BÀI TOÁN GIẢI QUYẾT THỰC THỂ (ENTITY RESOLUTION) <a name="phan-2"></a>

"Cơn ác mộng của Data Engineer" - Graph Fracturing (Mảnh vỡ đồ thị).
Khi trích xuất từ nhiều nguồn, LLM có thể tạo ra:
- `Node A:` `{id: "Công ty Apple"}`
- `Node B:` `{id: "Apple Inc"}`
- `Node C:` `{id: "Tập đoàn Táo khuyết"}`
Thực chất 3 Node này là MỘT. Nếu không gộp lại, các mối quan hệ sẽ bị đứt gãy.

### Giải pháp Hybrid Deduplication (Chuẩn Industry)
Không thể ném 1 triệu Node cho LLM gộp vì quá đắt. Ta làm theo 2 bước:
- **Bước 1 (Lọc thô - Phễu lọc):** Dùng Vector Embedding hoặc thuật toán Jaro-Winkler (So khớp chuỗi). Những Node nào giống nhau > 0.90 thì xếp vào một cụm "Nghi ngờ". (Giảm từ 1 triệu Node xuống còn 1.000 cụm).
- **Bước 2 (Chốt hạ - Sát thủ):** Đưa 1.000 cụm nghi ngờ đó cho LLM (vd: Qwen-2.5-14b). LLM sẽ phân tích ngữ cảnh (Description) của Node xem chúng có thực sự là một không. Nếu LLM gật đầu, chạy lệnh Cypher để gộp:

```cypher
// Dùng plugin APOC để gộp Node B vào Node A, tự động gom luôn các mũi tên của B sang A
CALL apoc.refactor.mergeNodes([nodeA, nodeB])
YIELD node
RETURN node
```

---

## 3. TỐI ƯU CHI PHÍ BẰNG SLM (MULTI-MODEL ARCHITECTURE) <a name="phan-3"></a>

Chạy Microsoft GraphRAG nguyên bản bằng GPT-4o cho 1 cuốn sách có thể ngốn của bạn $50. Để đưa dự án ra kiếm tiền (Production), bạn phải áp dụng chiến thuật "Trộn Model".

### Chiến thuật "Dao mổ trâu đúng lúc"
1. **Khâu Trích xuất (Entity Extraction) -> Chiếm 80% khối lượng công việc.**
   - *Không dùng:* GPT-4o.
   - *Khuyên dùng:* Các SLM (Small Language Models) chạy Local qua Ollama như `Qwen-2.5-14b`, `Llama-3.1-8b`. Hoặc các mô hình NLP chuyên biệt như **GLiNER**, **REBEL**. Mất 0 đồng.
2. **Khâu Viết Tóm tắt Cụm (Community Summaries) -> Cần văn phong tốt.**
   - *Khuyên dùng:* `GPT-4o-mini` hoặc `Claude 3 Haiku`. (Tốc độ tên lửa, giá bằng 1/10 bản xịn).
3. **Khâu Trả lời User (Global Query) -> Cần IQ cao nhất.**
   - *Khuyên dùng:* `GPT-4o` hoặc `Claude 3.5 Sonnet`. Vì lúc này đầu vào chỉ còn là các bản báo cáo đã được rút gọn, tốn rất ít Token, nên hãy dùng Model thông minh nhất để cho ra câu trả lời xuất sắc.

---

## 4. CẬP NHẬT ĐỒ THỊ ĐỘNG (INCREMENTAL INDEXING) <a name="phan-4"></a>

Nếu hôm nay bạn nhận được 1 văn bản luật mới ban hành, bạn KHÔNG THỂ đập đi xây lại toàn bộ Đồ thị (Re-indexing). Bạn phải cập nhật nó "Sống" (Dynamically).

### Quy trình Incremental Updates
1. Trích xuất Thực thể và Quan hệ CHỈ từ tờ văn bản luật mới.
2. Dùng lệnh `MERGE` chèn vào Neo4j.
3. Thuật toán Leiden sẽ kiểm tra xem Node mới này làm xô lệch cấu trúc của những Cụm (Community) nào.
4. **Blast Radius (Bán kính chấn thương):** Tính toán xem Cụm nào bị thay đổi nội dung -> **CHỈ GỌI LLM ĐỂ VIẾT LẠI SUMMARY CHO ĐÚNG CỤM ĐÓ**.

Nhờ kỹ thuật này, hệ thống của bạn có thể nuốt hàng chục nghìn tin tức chứng khoán mỗi ngày, nở to ra liên tục theo thời gian thực (Real-time) mà chi phí API mỗi ngày chỉ tốn vài xu (cents).

---
*(Hết Tập 4. Mời bạn đón đọc Tập cuối: Đánh giá hệ thống và Kiến trúc Agent (Cấp độ Giáo sư)).*
