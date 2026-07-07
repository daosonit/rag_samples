# 🤖 GIÁO TRÌNH HỌC TẬP TỪ A-Z: AGENTIC RAG

_Mục tiêu: Xây dựng hệ thống RAG không chỉ biết "Đọc" mà còn biết "Suy nghĩ", "Sử dụng công cụ" và "Sửa sai" (Self-Correction)._

Quy ước học tập:

- `[ ]`: Chưa học
- `[/]`: Đang học
- `[x]`: Đã hoàn thành

---

## 🚀 CHẶNG 1: KHỞI ĐỘNG - NHẬP MÔN AGENTIC RAG

_Mục tiêu: Hiểu rõ tại sao RAG truyền thống đã chết và Kỷ nguyên Agent bắt đầu._

- [x] **Bài 1.1:** Sự thất bại của RAG truyền thống (Naive RAG).
- [x] **Bài 1.2:** Agentic RAG là gì? (Tư duy ReAct: Reason + Act).
- [x] **Bài 1.3:** Các thành phần cốt lõi của một Agent (Brain, Memory, Tools).

---

## 🛠️ CHẶNG 2: NỀN TẢNG - VŨ KHÍ CỦA AGENT (TOOLS & ROUTING)

_Mục tiêu: Trao cho LLM tay chân để tương tác với thế giới thực._

- [x] **Bài 2.1:** Khái niệm Tool Calling (Function Calling) và định nghĩa Tools bằng Python.
- [x] **Bài 2.2:** Semantic Router (Người gác cổng) - Chuyển hướng câu hỏi của User đến đúng Tool.
- [x] **Bài 2.3:** Fallback Mechanism (Cơ chế dự phòng khi Tool thất bại).

---

## 🧠 CHẶNG 3: TRÁI TIM HỆ THỐNG - LANGGRAPH & WORKFLOWS

_Mục tiêu: Thoát khỏi các Prompt tuyến tính, thiết kế luồng suy nghĩ tuần hoàn (Cyclic) bằng LangGraph._

- [x] **Bài 3.1:** Giới thiệu LangGraph (StateGraph, Nodes, Edges).
- [x] **Bài 3.2:** Conditional Edges (Luồng rẽ nhánh có điều kiện).
- [x] **Bài 3.3:** Xây dựng một Agent cơ bản với bộ nhớ (Memory) bằng LangGraph.

---

## 🕵️‍♂️ CHẶNG 4: TÁC CHIẾN MỞ RỘNG - MULTI-AGENT COLLABORATION

_Mục tiêu: Xây dựng một biệt đội AI làm việc nhóm (Teamwork)._

- [x] **Bài 4.1:** Kiến trúc Supervisor (Một Sếp quản lý nhiều Lính).
- [x] **Bài 4.2:** Kiến trúc Network (Các Agent tự do giao tiếp ngang hàng).
- [x] **Bài 4.3:** Xây dựng Biệt đội: Researcher (Tìm kiếm Vector), Web Surfer (Lên mạng tìm tin), và Writer (Viết báo cáo).

---

## 🌟 CHẶNG 5: CẤP ĐỘ GIÁO SƯ - ADVANCED AGENTIC PATTERNS

_Mục tiêu: Đạt tới đỉnh cao của Agentic RAG bằng các bài báo khoa học mới nhất._

- [/] **Bài 5.1:** Self-RAG (Tự đánh giá, Tự chấm điểm và Tự sửa sai).
- [/] **Bài 5.2:** CRAG (Corrective RAG - RAG có khả năng tự sửa lỗi).
- [/] **Bài 5.3:** Plan-and-Solve (Lập kế hoạch trước khi hành động) và Human-in-the-loop (Chờ người duyệt).
