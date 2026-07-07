# 📖 TẬP 1: NEO4J & CYPHER - TRÁI TIM CỦA GRAPHRAG (DEEP DIVE)

*Nằm trong Bộ Bách khoa toàn thư GraphRAG 5 Tập*
*Tác giả: Giáo sư AI & Đào Sơn*

---

## MỤC LỤC
1. [Bản chất của Đồ thị (Property Graph Model)](#phan-1)
2. [Neo4j Architecture & APOC Plugin](#phan-2)
3. [Cypher - Nghệ thuật truy vấn đỉnh cao](#phan-3)
4. [Tối ưu hóa Hiệu suất (Indexes & Constraints)](#phan-4)
5. [Tích hợp Python Driver Thực chiến](#phan-5)

---

## 1. BẢN CHẤT CỦA ĐỒ THỊ (PROPERTY GRAPH MODEL) <a name="phan-1"></a>

Trước khi áp dụng AI, bạn phải hiểu cách dữ liệu tồn tại. Neo4j sử dụng mô hình **Property Graph Model** (Đồ thị thuộc tính). Khác với mô hình RDF (Triples cổ điển), Property Graph mạnh mẽ hơn rất nhiều vì nó cho phép chèn dữ liệu trực tiếp vào các mũi tên (Edges).

### 1.1 Cấu trúc hạt nhân
- **Node (Nút):** Đại diện cho thực thể (Entity). 
  - *Ví dụ:* Một con người, một cuốn sách, một công ty.
  - Node có **Label** (Nhãn) để phân loại. Một Node có thể có nhiều Label (vd: `Person` và `CEO`).
- **Relationship (Mối quan hệ):** Nối 2 Node lại với nhau.
  - *Quy tắc thép:* Mối quan hệ **bắt buộc** phải có hướng (Direction) và **bắt buộc** phải có tên (Type). Neo4j không cho phép mối quan hệ vô danh.
- **Properties (Thuộc tính):** Cả Node và Relationship đều có thể chứa dữ liệu dạng Key-Value (giống JSON).

### 1.2 Tại sao Vector Database lại thua Graph Database ở điểm này?
Trong Vector Database, văn bản được nhúng thành một chuỗi số thực: `[0.12, -0.45, 0.89...]`. Nó giống như một "hộp đen" - bạn không thể biết chính xác tại sao Vector A lại gần Vector B, bạn chỉ biết chúng "có vẻ giống nhau".
Trong Neo4j, sự thật (Fact) được lưu dưới dạng Explicit (Rõ ràng). 
Nếu bạn truy vấn: `(Apple)-[:PRODUCES]->(iPhone)`, máy tính hiểu tính nhân quả 100%.

---

## 2. NEO4J ARCHITECTURE & APOC PLUGIN <a name="phan-2"></a>

### 2.1 Kiến trúc Index-Free Adjacency
Tại sao Neo4j lại lướt qua hàng triệu Node trong tích tắc? Nhờ kiến trúc **Index-Free Adjacency** (Kề nhau không cần Index).
Trong SQL (PostgreSQL/MySQL), để tìm bạn của bạn của bạn (JOIN 3 bảng), Database phải dùng Index (B-Tree) để tìm kiếm từ đầu ở mỗi lần JOIN. Khi dữ liệu lên tới hàng triệu dòng, JOIN 3 bảng sẽ làm treo máy.
Trong Neo4j, mỗi Node chứa một con trỏ vật lý (Physical Pointer) chỉ thẳng tới các Node kề với nó trên ổ cứng (RAM/SSD). Việc "đi dạo" (Traverse) từ Node này sang Node kia tốn thời gian cố định O(1) bất chấp Đồ thị có lớn đến cỡ nào.

### 2.2 APOC (Awesome Procedures On Cypher)
Nếu dùng Neo4j mà không cài APOC, bạn mới chỉ xài được 10% sức mạnh. APOC là thư viện mở rộng chứa hàng ngàn hàm tiện ích.
**Ứng dụng của APOC trong GraphRAG:**
- Chạy các thuật toán Đồ thị (như PageRank, Community Detection).
- Export/Import dữ liệu dạng JSON.
- Tự động hóa các tác vụ thao tác chuỗi (String manipulation).

---

## 3. CYPHER - NGHỆ THUẬT TRUY VẤN ĐỈNH CAO <a name="phan-3"></a>

### 3.1 Cú pháp cơ bản
```cypher
// Tạo dữ liệu
CREATE (p1:Person {name: "Steve Jobs", age: 56})
CREATE (p2:Person {name: "Steve Wozniak"})
CREATE (c:Company {name: "Apple", founded: 1976})

// Nối mũi tên (Quan hệ)
CREATE (p1)-[:CO_FOUNDED {role: "CEO"}]->(c)
CREATE (p2)-[:CO_FOUNDED {role: "Engineer"}]->(c)
```

### 3.2 Lệnh MERGE - Chén thánh của GraphRAG
Khi dùng LLM để trích xuất dữ liệu, LLM có thể trả về "Steve Jobs" nhiều lần từ các văn bản khác nhau. Nếu dùng `CREATE`, bạn sẽ tạo ra hàng chục Node "Steve Jobs" (Gãy đồ thị).
**Luôn luôn dùng MERGE:**
```cypher
// Nếu có rồi thì bỏ qua, nếu chưa có thì tạo mới
MERGE (p:Person {id: "Steve Jobs"})
ON CREATE SET p.created_at = timestamp() // Chỉ chạy nếu tạo mới
ON MATCH SET p.last_updated = timestamp() // Chỉ chạy nếu đã tồn tại

MERGE (c:Company {id: "Apple"})

MERGE (p)-[r:CO_FOUNDED]->(c)
SET r.year = 1976
```

### 3.3 Graph Traversal (Lan truyền đồ thị)
Đỉnh cao của RAG là truy vấn nhiều lớp (Multi-hop Query):
```cypher
// Tìm những người làm chung công ty với người đã sáng lập ra iPhone
MATCH (product:Product {name: "iPhone"})<-[:PRODUCES]-(company:Company)
MATCH (company)<-[:WORKS_AT]-(colleague:Person)
RETURN colleague.name
```

---

## 4. TỐI ƯU HÓA HIỆU SUẤT (INDEXES & CONSTRAINTS) <a name="phan-4"></a>

Nếu đồ thị của bạn có 1 triệu Node, một câu lệnh `MATCH (p:Person {id: "Steve"})` sẽ phải quét toàn bộ 1 triệu Node đó (Full Scan) làm chậm hệ thống.
Bạn **BẮT BUỘC** phải tạo Constraint (Ràng buộc duy nhất) hoặc Index (Chỉ mục).

```cypher
// Đảm bảo không bao giờ có 2 Person có cùng 1 ID
CREATE CONSTRAINT person_id_unique IF NOT EXISTS 
FOR (p:Person) REQUIRE p.id IS UNIQUE;

// Tạo Index cho Vector Search (Neo4j 5.0+)
// Đây là trái tim của kiến trúc Hybrid RAG
CREATE VECTOR INDEX node_embeddings IF NOT EXISTS
FOR (e:Entity) ON (e.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
```

---

## 5. TÍCH HỢP PYTHON DRIVER THỰC CHIẾN <a name="phan-5"></a>

Trong các dự án Production, chúng ta không dùng giao diện web Neo4j, mà dùng Python.
Dưới đây là đoạn code Chuẩn Doanh Nghiệp (Enterprise-grade) để Bulk Insert (Chèn hàng loạt) hàng ngàn Triples từ LLM vào Neo4j với tốc độ cực cao, sử dụng **UNWIND**.

```python
from neo4j import GraphDatabase

# 1. Kết nối
uri = "bolt://192.168.1.99:7687"
user = "neo4j"
password = "your_password"
driver = GraphDatabase.driver(uri, auth=(user, password))

# 2. Dữ liệu trích xuất từ LLM (Ví dụ)
llm_triples = [
    {"head": "AI", "head_type": "Technology", "relation": "REVOLUTIONIZES", "tail": "Healthcare", "tail_type": "Industry"},
    {"head": "AI", "head_type": "Technology", "relation": "REQUIRES", "tail": "GPU", "tail_type": "Hardware"}
]

# 3. Hàm Bulk Insert tốc độ cao
def bulk_insert_triples(tx, triples):
    # UNWIND giúp giải nén mảng JSON, chỉ thực thi 1 Transaction duy nhất thay vì hàng ngàn Transaction rời rạc
    query = """
    UNWIND $batch AS row
    MERGE (h:Entity {id: row.head})
    ON CREATE SET h.label = row.head_type
    
    MERGE (t:Entity {id: row.tail})
    ON CREATE SET t.label = row.tail_type
    
    WITH h, t, row
    CALL apoc.merge.relationship(h, row.relation, {}, {}, t, {}) YIELD rel
    RETURN count(rel)
    """
    result = tx.run(query, batch=triples)
    return result.single()[0]

# 4. Thực thi an toàn
with driver.session() as session:
    inserted_count = session.execute_write(bulk_insert_triples, llm_triples)
    print(f"✅ Đã chèn/cập nhật thành công {inserted_count} mối quan hệ.")

driver.close()
```

### 💡 LỜI KHUYÊN TỪ GIÁO SƯ
Neo4j rất dễ bị "thắt cổ chai" (Bottleneck) ở khâu Write (Ghi dữ liệu) nếu bạn dùng vòng lặp `for` trong Python để gọi lệnh `session.run()` hàng ngàn lần. 
**Luôn luôn dùng `UNWIND`** như trong đoạn code trên để truyền toàn bộ mảng JSON vào Neo4j trong 1 lần duy nhất. Tốc độ sẽ tăng lên gấp 100 lần!

---
*(Hết Tập 1. Mời bạn đón đọc Tập 2: Xây dựng Pipeline trích xuất Đồ thị bằng LLM và LangChain).*
