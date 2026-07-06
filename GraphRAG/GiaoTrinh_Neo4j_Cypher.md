# GIÁO TRÌNH NEO4J & CYPHER: NỀN TẢNG ĐỒ THỊ CHO GRAPHRAG

Chào mừng bạn đến với khóa đào tạo chuyên sâu về **Neo4j và ngôn ngữ truy vấn Cypher**. Đây là khóa học nền tảng bắt buộc để bạn có thể xây dựng, lưu trữ và truy vấn Sơ đồ tri thức (Knowledge Graph), từ đó làm chủ công nghệ **GraphRAG**.

_Chú thích tiến độ:_

- `[ ]`: Chưa học
- `[/]`: Đang học
- `[x]`: Đã hoàn thành

---

## 🎯 MỤC TIÊU KHÓA HỌC

- Hiểu tư duy mô hình hóa dữ liệu theo dạng đồ thị (Graph Modeling).
- Thành thạo ngôn ngữ truy vấn Cypher từ cơ bản đến nâng cao.
- Biết cách import dữ liệu, tối ưu hóa hiệu năng cơ sở dữ liệu.
- Tích hợp Neo4j với Python và các ứng dụng AI/LLM.

---

## 📚 [/] CHẶNG 1: NHẬP MÔN GRAPH DATABASE VÀ NEO4J

_Mục tiêu: Hiểu lý thuyết về Đồ thị, thiết lập môi trường và làm quen với Neo4j Browser._

### [x] Bài 1.1: Graph Database là gì?

- Sự khác biệt giữa Relational DB (SQL), Document DB (NoSQL) và Graph Database.
- Khi nào nên dùng Graph DB? (Mạng xã hội, Hệ thống gợi ý, Fraud Detection, GraphRAG).
- Khái niệm **LPG (Labeled Property Graph)**:
  - **Node (Nút):** Đại diện cho thực thể (ví dụ: `Person`, `Movie`).
  - **Relationship (Mối quan hệ):** Kết nối các node, luôn có hướng và tên (ví dụ: `ACTED_IN`, `DIRECTED`).
  - **Property (Thuộc tính):** Dữ liệu key-value lưu trên Node hoặc Relationship.

### [x] Bài 1.2: Hệ sinh thái Neo4j & Cài đặt

- Tổng quan các phiên bản: Neo4j Desktop, Neo4j AuraDB (Cloud), Docker.
- Sử dụng Docker Compose để khởi chạy Neo4j cục bộ với cấu hình APOC và giới hạn tài nguyên.
- Giới thiệu **Neo4j Browser** (giao diện query) và **Neo4j Workspace** (công cụ khám phá dữ liệu).
- Thư viện mở rộng **APOC (Awesome Procedures on Cypher)**: Tại sao nó là "con dao Thụy Sĩ" của Neo4j.

---

## ✏️ [/] CHẶNG 2: NGÔN NGỮ CYPHER CƠ BẢN

_Mục tiêu: Đọc hiểu và viết được các câu truy vấn Cypher tạo, đọc, sửa, xóa (CRUD)._

### [x] Bài 2.1: Triết lý ASCII Art trong Cypher

- Cypher dùng hình vẽ để mô tả dữ liệu:
  - `(n:Person)` đại diện cho một vòng tròn (Node).
  - `-[r:KNOWS]->` đại diện cho mũi tên (Relationship).
- Viết câu hoàn chỉnh: `(a:Person)-[:KNOWS]->(b:Person)`

### [x] Bài 2.2: Tạo dữ liệu (CREATE & MERGE)

- `CREATE`: Tạo mới Node và Relationship.
  - Ví dụ: `CREATE (p:Person {name: 'Keanu Reeves', born: 1964})`
- `MERGE`: Tạo nếu chưa có, bỏ qua hoặc cập nhật nếu đã tồn tại (rất quan trọng trong GraphRAG để tránh trùng lặp thực thể).

### [x] Bài 2.3: Đọc dữ liệu (MATCH & RETURN)

- `MATCH`: Khớp mẫu đồ thị.
  - Ví dụ: `MATCH (p:Person)-[:ACTED_IN]->(m:Movie) RETURN p.name, m.title`
- Lọc kết quả với `WHERE`.

### [x] Bài 2.4: Cập nhật và Xóa (SET, REMOVE, DELETE)

- `SET` để thêm/sửa thuộc tính, `REMOVE` để xóa thuộc tính hoặc Label.
- `DELETE` để xóa Node/Relationship. Lưu ý: Không thể xóa Node nếu nó vẫn còn Relationship -> Sử dụng `DETACH DELETE`.

---

## 🔍 [/] CHẶNG 3: TRUY VẤN CYPHER NÂNG CAO

_Mục tiêu: Xử lý các logic phức tạp, tìm kiếm đường đi và gom nhóm dữ liệu._

### [x] Bài 3.1: Variable-Length Paths (Đường đi không xác định độ dài)

- Bài toán: Tìm bạn của bạn (bạn cấp 2, cấp 3).
- Cú pháp: `MATCH (p1:Person)-[:KNOWS*1..3]->(p2:Person)` (Tìm từ 1 đến 3 cấp độ).
- Tìm đường đi ngắn nhất: `shortestPath()`.

### [x] Bài 3.2: Aggregation (Gom nhóm)

- Tính toán: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.
- Lệnh `WITH`: Chuyền kết quả từ một phần của truy vấn sang phần tiếp theo.
- Lệnh `COLLECT()`: Gom nhiều kết quả thành một mảng (List/Array) - Rất hữu ích khi trả context về cho LLM.

### [x] Bài 3.3: Sắp xếp và Phân trang

- `ORDER BY DESC/ASC`.
- `SKIP` và `LIMIT` để phân trang kết quả tìm kiếm.

---

## ⚡ [/] CHẶNG 4: IMPORT DỮ LIỆU & TỐI ƯU HÓA

_Mục tiêu: Nhập hàng triệu records vào Neo4j và làm cho truy vấn chạy nhanh như chớp._

### [x] Bài 4.1: Nhập dữ liệu (Importing Data)

- Import dữ liệu từ file CSV bằng lệnh `LOAD CSV`.
  - Cấu trúc: `LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row`.
- Sử dụng APOC để import từ JSON: `CALL apoc.load.json("url")`.

### [x] Bài 4.2: Indexes và Constraints

- **Unique Constraint:** Đảm bảo một thuộc tính (vd: ID hoặc Tên thực thể) là duy nhất.
  - `CREATE CONSTRAINT FOR (p:Person) REQUIRE p.name IS UNIQUE`
- **Index:** Tăng tốc độ tìm kiếm `MATCH`. (Rất quan trọng khi tìm kiếm Thực thể trong GraphRAG).

### [x] Bài 4.3: Phân tích Hiệu năng (EXPLAIN & PROFILE)

- Đọc kế hoạch thực thi (Execution Plan) của Neo4j.
- Phân biệt `EXPLAIN` (chỉ xem kế hoạch) và `PROFILE` (thực thi và xem số lượng row DB chạm vào).

---

## 🤖 [/] CHẶNG 5: TÍCH HỢP PYTHON & ỨNG DỤNG AI (GRAPHRAG)

_Mục tiêu: Đưa Neo4j vào hệ thống phần mềm, kết nối với LLM._

### [x] Bài 5.1: Làm việc với Neo4j Python Driver

- Cài đặt thư viện: `pip install neo4j`.
- Thiết lập Driver và quản lý Session/Transaction.
- Chạy câu lệnh Cypher từ Python và đọc kết quả trả về dưới dạng Pandas DataFrame hoặc Dict.

### [x] Bài 5.2: Text-to-Cypher với LangChain / LlamaIndex

- Cung cấp Schema của Graph cho LLM (OpenAI/Gemini).
- Prompt engineering để LLM tự viết câu lệnh Cypher từ câu hỏi của user: "Cho tôi biết các bộ phim Keanu Reeves đã đóng".
- Execute Cypher trên Neo4j và tổng hợp câu trả lời cuối cùng.

### [x] Bài 5.3: Graph Extraction Pipeline (Xây dựng Knowledge Graph từ Văn bản)

- Nhận diện Entity & Relationship từ Text bằng LLM (như đã học ở khóa GraphRAG).
- Dùng Cypher (`UNWIND` và `MERGE`) để insert hàng loạt Triples vào Neo4j một cách hiệu quả nhất.

---

## 🛠 BƯỚC TIẾP THEO DÀNH CHO BẠN

1. **Khởi động Neo4j:** Hãy chạy lệnh `docker compose up -d` trong thư mục này để bật server Neo4j.
2. **Truy cập Giao diện:** Mở trình duyệt vào địa chỉ `http://localhost:7474` (Tên đăng nhập mặc định có thể là `neo4j` / mật khẩu nằm trong file `.env` của bạn).
3. **Bắt đầu gõ Cypher:** Thử câu lệnh đầu tiên: `RETURN "Hello Neo4j" AS message`.

Bạn đã sẵn sàng để thực hành **Chặng 1** chưa? Mở trình duyệt và bắt đầu thôi!
