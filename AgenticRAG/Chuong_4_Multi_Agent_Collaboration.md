# 📖 TẬP 4: TÁC CHIẾN MỞ RỘNG - MULTI-AGENT COLLABORATION

## 1. Tại sao cần nhiều Agent?
Một Agent đóng vai trò "Trợ lý toàn năng" sẽ rất dễ bị rối trí khi đối mặt với tác vụ lớn.
Chiến thuật là "Chia để trị":
- **Web Searcher Agent:** Chỉ giỏi việc lên mạng tìm kiếm tin tức nóng hổi.
- **RAG Researcher Agent:** Chỉ giỏi việc Query vào Neo4j/Vector DB nội bộ.
- **Coder Agent:** Chỉ giỏi việc viết và chạy code Python.
- **Writer Agent:** Giỏi văn chương, biết tóm tắt.

## 2. Các kiến trúc Multi-Agent
### A. Network Architecture (Kiến trúc mạng lưới ngang hàng)
Các Agent tự giao tiếp với nhau. 
Ví dụ: `Writer` cần dữ liệu, nó sẽ pass (chuyền bóng) cho `Researcher`. `Researcher` tìm xong chuyền lại cho `Writer`.

### B. Supervisor Architecture (Kiến trúc phân cấp Sếp - Lính)
Đây là kiến trúc an toàn và hiệu quả nhất cho Doanh nghiệp.
- Tạo một `Supervisor Agent` đóng vai trò là Trưởng phòng.
- Trưởng phòng đọc yêu cầu của User: *"So sánh báo cáo tài chính nội bộ và chứng khoán trên web"*.
- Trưởng phòng ra lệnh:
  - "Này `RAG Agent`, hãy vào Database nội bộ lấy báo cáo tài chính ra đây."
  - "Này `Web Agent`, hãy lên mạng cào dữ liệu chứng khoán hôm nay về."
  - "Này `Writer Agent`, lấy 2 báo cáo kia tổng hợp lại thành bài nộp cho User."
- Tất cả tiến trình đều được Trưởng phòng giám sát, nếu Lính làm sai, Trưởng phòng bắt làm lại.

## 3. LangGraph Multi-Agent
Với LangGraph, việc xây dựng kiến trúc Sếp - Lính cực kỳ dễ dàng bằng cách coi mỗi Agent là một **Node**. Cuốn sổ `State` sẽ chứa danh sách các tin nhắn trao đổi qua lại giữa các Node để tất cả đều biết chuyện gì đang xảy ra.
