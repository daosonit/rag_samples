# 📖 TẬP 5: CẤP ĐỘ GIÁO SƯ - ADVANCED AGENTIC PATTERNS

## 1. Self-RAG (Tự đánh giá và Sửa sai)
Đây là bài báo khoa học làm rúng động giới AI. Thay vì trả lời ngay, Agent sẽ tự đóng vai giám khảo của chính mình.
- **Luồng hoạt động:**
  1. Retrieve tài liệu.
  2. Đọc tài liệu, nếu thấy tài liệu không liên quan (Irrelevant) -> Vứt bỏ, viết lại câu query khác để tìm lại.
  3. Nếu tài liệu liên quan -> Sinh câu trả lời.
  4. Đọc câu trả lời vừa sinh ra -> Kiểm tra xem có bịa chuyện (Hallucination) không?
  5. Nếu bịa -> Xóa đi làm lại. Nếu chuẩn xác -> Trả về cho User.
- Self-RAG đảm bảo độ chính xác của hệ thống gần như tuyệt đối, hy sinh một chút tốc độ phản hồi.

## 2. CRAG (Corrective RAG)
Tương tự như Self-RAG nhưng mạnh mẽ hơn ở khâu đối phó với dữ liệu hỏng.
- Nếu Agent tìm trong Database nội bộ mà không thấy câu trả lời (hoặc câu trả lời chất lượng thấp), nó sẽ không báo lỗi.
- Nó kích hoạt **Web Search Tool** để bay ra ngoài Internet tìm kiếm bù đắp vào phần thiếu hụt.

## 3. Plan-and-Solve (Lập kế hoạch trước khi hành động)
Với các câu hỏi phức tạp (vd: *"Viết báo cáo nghiên cứu thị trường xe điện ở Việt Nam"*), Agent không nên hành động ngay.
- Nó sẽ gọi một Node `Planner` trước. `Planner` sẽ vạch ra 5 bước cần làm.
- Sau đó, một Node `Executor` sẽ tuần tự thực thi từng bước một, ghi chú lại kết quả.
- Cách này giúp Agent không bị "lạc lối" giữa chừng khi làm tác vụ dài.

---
**TỔNG KẾT:** Agentic RAG chính là tương lai. LLM không còn là cái máy gõ chữ, mà đã trở thành "Bán cầu não trái" của một con Robot ảo, biết cầm nắm công cụ và làm việc theo nhóm. Chúc bạn thành công trong chặng đường mới này!
