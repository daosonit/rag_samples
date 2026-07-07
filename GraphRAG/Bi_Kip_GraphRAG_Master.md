# 📖 CUỐN BÍ KÍP TỐI THƯỢNG: TỪ ZERO ĐẾN MASTER GRAPHRAG (PHIÊN BẢN MỞ RỘNG)

_Tác giả: Giáo sư AI & Học viên Đào Sơn_
_Thời gian biên soạn: Chuyến hành trình chinh phục GraphRAG 2026_

> **Lời tựa:** Phiên bản này được viết lại dưới dạng một cuốn E-Book chi tiết, bao gồm toàn bộ lý thuyết sâu sắc, các đoạn code thực chiến bằng Python, các câu lệnh Cypher và những kinh nghiệm xương máu khi triển khai Production.

---

## MỤC LỤC

1. [Chặng 1: Khởi động - Nhập môn Đồ thị và Neo4j](#chặng-1)
2. [Chặng 2: Nền tảng - Build Graph từ Văn bản bằng LLM](#chặng-2)
3. [Chặng 3: Nâng cao - Mổ xẻ Microsoft GraphRAG](#chặng-3)
4. [Chặng 4: Cấp độ Chuyên gia - Kiến trúc Hybrid & Tối ưu hóa](#chặng-4)
5. [Chặng 5: Cấp độ Giáo sư - Đánh giá và Tương lai](#chặng-5)

---

## 🏔️ CHẶNG 1: KHỞI ĐỘNG - NHẬP MÔN ĐỒ THỊ VÀ NEO4J <a name="chặng-1"></a>

### 1.1 Điểm mù của Vector RAG truyền thống

Vector RAG đã thống trị năm 2023 nhờ khả năng biến văn bản thành các con số (Vector) và tính toán khoảng cách (Cosine Similarity). Tuy nhiên, kiến trúc này có một "điểm mù" chết người: **Mù ngữ cảnh chéo (Cross-context Blindness)**.

Giả sử trong một cuốn tiểu thuyết trinh thám:

- Trang 10 viết: _"Jonh ghét Mary."_
- Trang 50 viết: _"Mary là em gái của Peter."_
- Khi người dùng hỏi: _"Vì sao Peter không ưa John?"_, Vector RAG sẽ bị "tê liệt" vì không có một đoạn văn nào chứa cùng lúc 3 người này để tính toán Vector.

=> **GraphRAG ra đời:** GraphRAG đóng vai trò như một bảng ghim của thám tử. Nó kết nối `John` -> `Ghét` -> `Mary` -> `Em gái` -> `Peter`. Nhờ đường đi vật lý (Edges) này, hệ thống có thể suy luận ra nguyên nhân mà không cần chung một đoạn văn.

### 1.2 Ngôn ngữ Cypher - Nghệ thuật vẽ tranh bằng phím

Cypher là ngôn ngữ truy vấn độc quyền của Neo4j. Nó được thiết kế dựa trên nghệ thuật ASCII Art, giúp người đọc nhìn vào code là hình dung ra đồ thị.

- **Node (Thực thể):** Biểu diễn bằng dấu ngoặc đơn `()`. Ví dụ: `(p:Person {name: "John"})`
- **Relationship (Mối quan hệ):** Biểu diễn bằng mũi tên `-->`. Ví dụ: `-[r:KNOWS]->`

**Các lệnh Cypher thực chiến hàng ngày:**

```cypher
// 1. Dọn dẹp Database (Cẩn thận khi dùng)
MATCH (n) DETACH DELETE n;

// 2. Tạo Node và Edge cơ bản
CREATE (steve:Person {id: "Steve Jobs"}),
       (apple:Company {id: "Apple"}),
       (steve)-[:FOUNDED {year: 1976}]->(apple);

// 3. Truy vấn (Tìm những công ty mà Steve Jobs đã sáng lập)
MATCH (p:Person {id: "Steve Jobs"})-[:FOUNDED]->(c:Company)
RETURN c.id;

// 4. Lệnh MERGE (Linh hồn của Upsert - Cập nhật tự động)
// Nếu Node có rồi thì không tạo mới, chưa có thì tạo mới
MERGE (elon:Person {id: "Elon Musk"})
MERGE (tesla:Company {id: "Tesla"})
MERGE (elon)-[:CEO_OF]->(tesla);
```

---

## 🏗️ CHẶNG 2: NỀN TẢNG - BUILD GRAPH TỪ VĂN BẢN <a name="chặng-2"></a>

### 2.1 Ma thuật trích xuất Triples bằng LLM

Máy tính không tự biết "Steve Jobs" là ai. Chúng ta phải dùng LLM (như GPT-4, Llama 3) để đọc văn bản và trích xuất các **Triples (Node - Edge - Node)**.

**Cấu trúc Prompt chuẩn mực để ép JSON:**

```python
extraction_prompt = """
Bạn là một chuyên gia dữ liệu. Hãy đọc đoạn văn bản sau và trích xuất thông tin thành Đồ thị Tri thức.
Quy tắc:
1. Xác định các thực thể (Nodes) và phân loại chúng (Person, Organization, Location, Concept).
2. Xác định mối quan hệ (Edges) giữa chúng.
3. ĐẦU RA BẮT BUỘC PHẢI LÀ JSON THEO ĐÚNG FORMAT SAU, KHÔNG GIẢI THÍCH:
[
  {
    "head": "Tên thực thể 1",
    "head_type": "Loại thực thể 1",
    "relation": "TÊN_MỐI_QUAN_HỆ_VIẾT_HOA",
    "tail": "Tên thực thể 2",
    "tail_type": "Loại thực thể 2"
  }
]
Văn bản: {text}
"""
```

### 2.2 Đưa dữ liệu vào Neo4j bằng Python

Sau khi có mảng JSON, chúng ta dùng thư viện `neo4j` của Python để ghi vào Database.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def insert_triples(triples):
    with driver.session() as session:
        for t in triples:
            query = f"""
            MERGE (h:{t['head_type']} {{id: $head}})
            MERGE (t:{t['tail_type']} {{id: $tail}})
            MERGE (h)-[:{t['relation']}]->(t)
            """
            session.run(query, head=t['head'], tail=t['tail'])
```

### 2.3 LangChain GraphCypherQAChain - Dịch tiếng người sang Cypher

Người dùng không biết gõ Cypher, họ chỉ hỏi: _"Ai lập ra Apple?"_. Ta dùng LangChain để dịch câu này.

```python
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate

# Prompt bẻ lái LangChain dùng id thay vì label
cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""Dựa vào Schema sau: {schema}
Hãy viết lệnh Cypher để trả lời: {question}
LƯU Ý: Tuyệt đối chỉ tìm kiếm bằng thuộc tính `id`. KHÔNG tìm kiếm bằng `label`.
Đúng: MATCH (e:Entity {{id: 'Apple'}})
Sai: MATCH (e:Entity {{label: 'Apple'}})
"""
)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=cypher_prompt,
    verbose=True
)
```

---

## 🏛️ CHẶNG 3: NÂNG CAO - MỔ XẺ MICROSOFT GRAPHRAG <a name="chặng-3"></a>

Microsoft đã nâng tầm GraphRAG lên một đẳng cấp mới bằng cách kết hợp Đồ thị (Graph) với Tóm tắt Cụm (Clustering Summaries). Kiến trúc này tốn kém, nhưng giải quyết triệt để bài toán "Global Search".

### 3.1 Thuật toán Leiden & Community Summaries

Đồ thị lớn nhìn vào sẽ như một đống bùi nhùi (Hairball). Microsoft áp dụng thuật toán **Leiden** để chia đồ thị thành các cộng đồng (Communities).

- **Element Summaries:** Mỗi Node và Edge không chỉ có tên, mà còn có 1 đoạn văn miêu tả do LLM tự viết.
- **Community Summaries:** Sau khi chia cụm, hệ thống nhét tất cả thông tin của một cụm vào LLM và ra lệnh: _"Hãy viết một báo cáo dài 3 trang tóm tắt mọi diễn biến trong cộng đồng này."_
  => Nhờ vậy, kiến thức không còn rải rác mà đã được cô đặc thành các báo cáo (Reports).

### 3.2 Tác chiến: Local Search vs Global Search

- **Local Search (Tìm vi mô):** Phù hợp với câu hỏi tọc mạch (Ví dụ: _"Steve Jobs thích ăn gì?"_). Hệ thống nhảy thẳng vào Node `Steve Jobs` và lôi ra các báo cáo cộng đồng liền kề.
- **Global Search (Tìm vĩ mô):** Phù hợp với câu hỏi học thuật (Ví dụ: _"Chủ đề chính của 1000 bài báo này là gì?"_). Hệ thống sẽ dùng chiến thuật **Map-Reduce**:
  - Dùng LLM đọc _hàng ngàn_ báo cáo cộng đồng cùng một lúc (Map).
  - Chọn ra những báo cáo có chứa câu trả lời.
  - Viết lại thành một bài luận tổng hợp cực kỳ hoàn hảo (Reduce).

---

## 🧠 CHẶNG 4: CẤP ĐỘ CHUYÊN GIA - KIẾN TRÚC HYBRID & TỐI ƯU <a name="chặng-4"></a>

### 4.1 Kiến trúc Hybrid (Vũ khí tối thượng của Big Tech)

Không có công nghệ nào là hoàn hảo. Đồ thị yếu ở việc khớp từ khóa mập mờ (Semantic), Vector yếu ở việc suy luận (Reasoning).
**Giải pháp:** Neo4j hỗ trợ **Vector Index**. Ta nhúng (Embed) nội dung của Node thành Vector và lưu trực tiếp vào Node.

Quy trình truy vấn Hybrid:

1. User hỏi -> Dịch câu hỏi thành Vector.
2. Dùng hàm `db.index.vector.queryNodes` để tìm Top 5 Node có Vector giống nhất.
3. Từ 5 Node đó, dùng lệnh `MATCH` lan truyền ra xung quanh độ sâu 2 cấp.
4. Lấy kết quả đem cho LLM tổng hợp.

### 4.2 Entity Resolution (Bài toán gộp thực thể)

Nếu để nguyên văn bản gốc, LLM sẽ tạo ra 3 Node: `"Steve Jobs"`, `"S. Jobs"`, `"Cựu CEO Apple"`. Điều này làm gãy đồ thị.
**Giải pháp Thực tiễn (Best Practice):**

- Bước 1 (Lọc thô): Dùng thuật toán so sánh chuỗi (Fuzzy Wuzzy) hoặc Vector Embedding để tìm các cặp Node giống nhau trên 90%.
- Bước 2 (Chốt hạ): Gom các cặp đáng ngờ này gửi cho LLM (`Llama-3-8b` hoặc `Qwen-2.5-14b`) kiểm tra xem chúng có thực sự là một người không. Nếu đúng -> Chạy lệnh `MERGE` để gộp.

### 4.3 Tối ưu chi phí bằng SLM (Small Language Models)

- Chạy Microsoft GraphRAG nguyên bản bằng GPT-4o có thể tốn $50/sách.
- Để giảm chi phí xuống 90%:
  1. Trích xuất Node/Edge: Dùng **Qwen-2.5-14B** (Chạy Local qua Ollama) hoặc mô hình NLP **GLiNER**. Chi phí = $0.
  2. Viết Community Summaries: Dùng **GPT-4o-mini** (Siêu rẻ).
  3. Trả lời User (Query): Dùng **GPT-4o** (Tốn ít Token nhưng cực thông minh).

### 4.4 Incremental Updates (Đồ thị Động)

- Đừng bao giờ xóa Database đi làm lại khi có file mới.
- Khi file mới vào: Trích xuất Node/Edge mới -> `MERGE` vào Database.
- Thuật toán sẽ tính toán các Cụm (Communities) bị phình to ra và **CHỈ BẮT LLM VIẾT LẠI TÓM TẮT CHO CỤM ĐÓ**.

---

## 🔭 CHẶNG 5: CẤP ĐỘ GIÁO SƯ - ĐÁNH GIÁ VÀ TƯƠNG LAI <a name="chặng-5"></a>

### 5.1 LLM-as-a-Judge (Chấm điểm Toán học)

Trong môi trường học thuật, ta dùng Framework **RAGAS** hoặc **TruLens** để chấm điểm hệ thống (Thang điểm 0 - 1).

- **Faithfulness (Độ trung thực):** Kiểm tra xem LLM có bịa số liệu không. Nếu câu trả lời có chứa thông tin KHÔNG có trong Graph -> Cho 0 điểm.
- **Answer Relevance:** Kiểm tra xem LLM trả lời có đúng trọng tâm câu hỏi không.
- **Comprehensiveness (Độ toàn diện):** Dùng GPT-4 để chấm điểm xem câu trả lời của GraphRAG bao quát được bao nhiêu khía cạnh so với Vector RAG.

### 5.2 Tương lai: Graph Reasoning (RoG) và Autonomous Agents

- Khái niệm **Reasoning on Graphs (RoG):** LLM không nhận một đống dữ liệu lộn xộn nữa. Nó tự phân tích câu hỏi, vạch ra các con đường (Paths) trên đồ thị trước. Ví dụ: `Person -> WorksAt -> Company -> Produces -> Product`.
- **Đặc vụ Đồ thị (Graph Agents):** Kết hợp GraphRAG với hệ thống Multi-Agent (LangGraph hoặc AutoGen). Các Agent sẽ đóng vai thám tử, đi dọc theo các mũi tên của Neo4j để tự động thu thập chứng cứ cho đến khi có đủ dữ liệu để phá án.

---

**🎓 LỜI KẾT**

> Kiến thức là vô tận, nhưng tư duy hệ thống (System Thinking) mới là thứ làm nên một Kỹ sư giỏi. Từ những dòng lệnh Cypher sơ khai, đến kiến trúc lai tạo Hybrid, bạn đã nắm trong tay chìa khóa để xây dựng các "Bộ não AI" mạnh mẽ nhất thế giới hiện tại.
> Hãy mang những kiến thức này ra ngoài kia và xây dựng những sản phẩm thay đổi thế giới!

Chuong_1_Neo4j_DeepDive.md
Chuong_2_Graph_Extraction_Code.md
Chuong_3_Microsoft_GraphRAG_Core.md
Chuong_4_Hybrid_Architecture_Scale.md
Chuong_5_Evaluation_And_Agents.md
