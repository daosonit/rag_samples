# 📖 TẬP 1: NHẬP MÔN AGENTIC RAG (KHỞI ĐỘNG)

## 1. Sự thất bại của RAG truyền thống (Naive RAG)
RAG truyền thống hoạt động theo đường thẳng (Tuyến tính): 
`User hỏi -> Băm câu hỏi thành Vector -> Lấy 5 đoạn văn -> Ném cho LLM -> Trả lời`.

**Vấn đề:** 
- Nếu 5 đoạn văn lôi lên toàn rác (không liên quan), LLM vẫn ngoan ngoãn dựa vào rác đó để chém gió.
- Không thể trả lời các câu hỏi so sánh hoặc tổng hợp phức tạp (Vd: "So sánh doanh thu công ty A và B" -> Nếu dữ liệu công ty A ở file PDF, công ty B ở trên Website, RAG truyền thống "bó tay").

## 2. Agentic RAG là gì?
Agentic RAG biến hệ thống từ một **"Cái máy đọc vẹt"** thành một **"Thực thể có tư duy"**. 
Thay vì chỉ Retrieve (Truy xuất) 1 lần, Agent có thể Retrieve nhiều lần, thay đổi từ khóa tìm kiếm nếu tìm không ra, lên Google tra cứu, hoặc dùng Python để vẽ biểu đồ.

**Tư duy ReAct (Reason + Act):**
- **Thought (Suy nghĩ):** "User muốn so sánh doanh thu A và B. Mình cần tìm doanh thu A trước."
- **Action (Hành động):** Gọi công cụ `DocSearch(query="Doanh thu A")`.
- **Observation (Quan sát):** "Đã có doanh thu A. Giờ mình phải lên Web tìm doanh thu B."
- **Action (Hành động 2):** Gọi công cụ `WebSearch(query="Doanh thu B năm nay")`.
- **Answer (Trả lời):** Đưa ra đáp án cuối cùng.

## 3. Các thành phần cốt lõi của Agent
- **Brain (Não bộ):** Chính là LLM (Nên dùng model cực thông minh như GPT-4o, Claude 3.5 hoặc Qwen-2.5-14b/32b).
- **Tools (Tay chân):** Các hàm Python mà Agent được phép gọi (vd: Hàm search DB, hàm gọi API thời tiết).
- **Memory (Bộ nhớ):** Nơi lưu trữ ngữ cảnh hội thoại để Agent không bị "não cá vàng".
