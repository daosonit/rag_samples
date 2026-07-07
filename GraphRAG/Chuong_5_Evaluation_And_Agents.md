# 📖 TẬP 5: ĐÁNH GIÁ HỆ THỐNG VÀ KIẾN TRÚC AGENTS (CẤP ĐỘ GIÁO SƯ)

*Nằm trong Bộ Bách khoa toàn thư GraphRAG 5 Tập*
*Tác giả: Giáo sư AI & Đào Sơn*

---

## MỤC LỤC
1. [Khoa học Đánh giá: LLM-as-a-Judge](#phan-1)
2. [Bộ tiêu chuẩn đánh giá của Microsoft GraphRAG](#phan-2)
3. [Reasoning on Graphs (RoG): Lướt trên Đồ thị](#phan-3)
4. [Đỉnh cao cuối cùng: Autonomous Graph Agents](#phan-4)

---

## 1. KHOA HỌC ĐÁNH GIÁ: LLM-AS-A-JUDGE <a name="phan-1"></a>

"Không có thước đo, mọi mô hình AI đều là đồ chơi."
Khi bạn đưa GraphRAG vào doanh nghiệp, câu hỏi đầu tiên của Sếp sẽ là: *"Làm sao tôi biết nó không bịa chuyện?"*
Giải pháp hiện đại nhất là dùng **LLM-as-a-Judge** (Dùng một con LLM siêu thông minh như GPT-4 đóng vai giám khảo để chấm điểm cho con LLM trả lời).

### 1.1 RAG Triad (Bộ 3 tiêu chuẩn RAGAS)
Các Framework như RAGAS hoặc TruLens dựa trên 3 trụ cột:
- **Context Relevance (Độ chuẩn xác của Ngữ cảnh):** Những Node/Edges mà hệ thống moi lên từ Neo4j có thực sự liên quan đến câu hỏi không, hay lôi lên toàn rác?
- **Faithfulness (Độ trung thực - Sống còn):** Câu trả lời của LLM có hoàn toàn dựa vào dữ liệu của Neo4j không? Nếu LLM lén dùng kiến thức có sẵn trên mạng để chém gió -> Bị chấm 0 điểm (Hallucination).
- **Answer Relevance (Độ liên quan của câu trả lời):** Hỏi một đằng có trả lời một nẻo không?

---

## 2. BỘ TIÊU CHUẨN ĐÁNH GIÁ CỦA MICROSOFT GRAPHRAG <a name="phan-2"></a>

Trong các bài báo khoa học của Microsoft, họ không dùng bộ RAGAS tiêu chuẩn. Họ thiết kế ra các bộ chỉ số đo lường đặc thù để chứng minh GraphRAG ăn đứt Vector RAG trong các truy vấn Vĩ mô (Global Search):

1. **Comprehensiveness (Tính toàn diện):** 
   - *Định nghĩa:* Câu trả lời có bao hàm được tất cả các yếu tố, khía cạnh ẩn giấu trong toàn bộ kho tài liệu hay không?
   - *Thực tế:* Vector RAG thường đạt 30% (vì nó chỉ lấy Top 5 chunks). GraphRAG có thể đạt 95% vì nó dùng Map-Reduce đọc toàn bộ Community Summaries.
2. **Diversity (Tính đa dạng):** 
   - Câu trả lời có đưa ra được nhiều góc nhìn đa chiều không?
3. **Empowerment (Tính trao quyền):** 
   - Sau khi đọc câu trả lời, người dùng có đủ thông tin để tự tin đưa ra quyết định (Decision Making) hay không?

---

## 3. REASONING ON GRAPHS (RoG): LƯỚT TRÊN ĐỒ THỊ <a name="phan-3"></a>

GraphRAG hiện tại (như của Microsoft) vẫn mang tính "Thụ động" (Passive Retrieval): Nó gom hết Node xung quanh và nhét vào mồm LLM.
Tương lai của công nghệ này là **RoG (Suy luận trên Đồ thị)**.

### Cách RoG hoạt động:
- Thay vì gom Node, LLM sẽ tự lập ra một Lộ trình đi dạo (Path Planning).
- Ví dụ câu hỏi: *"Sản phẩm chủ lực của công ty do chồng của Laurene sáng lập là gì?"*
- LLM sẽ tự vạch đường đi:
  - Lệnh 1: Tìm chồng của Laurene -> Gặp Node `Steve Jobs`.
  - Lệnh 2: Tìm công ty của Steve Jobs -> Gặp Node `Apple`.
  - Lệnh 3: Tìm sản phẩm chủ lực của Apple -> Gặp Node `iPhone`.
=> Hệ thống tự động nhảy từ Node này sang Node khác y hệt như tư duy của một Thám tử lần mò dấu vết. Trí tuệ lúc này nằm ở **Cách điều hướng (Navigation)** chứ không chỉ là Cách đọc chữ.

---

## 4. ĐỈNH CAO CUỐI CÙNG: AUTONOMOUS GRAPH AGENTS <a name="phan-4"></a>

Hãy tưởng tượng bạn không phải viết code LangChain hay Cypher nữa. Bạn thiết kế ra một Đặc vụ (Agent) tự trị, ném nó vào bên trong Database Neo4j và cung cấp cho nó một loạt Công cụ (Tools).

**Một vòng đời của Graph Agent:**
1. **User hỏi:** "Phân tích rủi ro tài chính của công ty X."
2. **Agent suy nghĩ (ReAct):** "Mình cần tìm công ty X trên đồ thị." -> Tự động sinh lệnh Cypher để lấy Node X.
3. **Agent quan sát:** "Công ty X có vay nợ công ty Y. Mình cần kiểm tra tiếp công ty Y." -> Tiếp tục sinh lệnh Cypher đi tới Node Y.
4. **Agent phát hiện thiếu dữ liệu:** "Trên đồ thị chưa có dữ liệu báo cáo thuế của công ty Y." -> Nó tự kích hoạt tool Web Search, lên Google tải báo cáo về.
5. **Agent tự mở rộng Đồ thị:** Sau khi đọc báo cáo tải về, nó tự trích xuất Triples và chèn (MERGE) thêm Node báo cáo thuế vào Đồ thị.
6. **Agent đưa ra kết luận:** Khi đã thu thập đủ bằng chứng, nó tổng hợp lại và báo cáo cho User.

Đây là sự kết hợp giữa **Multi-Agent (LangGraph/AutoGen)** và **GraphRAG**. Nó biến Đồ thị Tri thức thành một bộ não thực sự, biết tự học, tự suy luận, tự tìm kiếm và tự mở rộng mỗi ngày!

---

## 🎓 LỄ TỐT NGHIỆP

**Gửi Kỹ sư Hệ thống Tương lai,**

Cuốn bách khoa toàn thư GraphRAG này là hành trang quý giá nhất mà Giáo sư trao lại cho bạn.
Bạn đã đi từ việc lơ ngơ không biết Cypher là gì, đến việc hiểu thấu đáo kiến trúc Hybrid, các thuật toán phân cụm Leiden đắt đỏ của Microsoft, và cách dùng các LLM mã nguồn mở (Local LLM) để tối ưu hóa chi phí đến mức tối đa.

Sự bùng nổ của AI không nằm ở việc Model nào to hơn, mà nằm ở việc ai biết cách tổ chức dữ liệu thông minh hơn. Với Knowledge Graph, bạn đang nắm giữ chìa khóa để xây dựng các thế hệ Trí tuệ Nhân tạo đáng tin cậy, logic và không thể bị đánh lừa.

Chúc bạn mang những kiến thức này ra chiến trường và xây dựng nên những hệ thống AI vĩ đại! 🚀
