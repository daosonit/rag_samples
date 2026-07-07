# CHẶNG 2: MÔI TRƯỜNG TƯƠNG TÁC & COMPUTER USE 🦾🖱️

Đã có Mắt và Tai, giờ là lúc lắp Đôi tay cho AI. Đây là bước đột phá lớn nhất của năm 2026: Cho phép AI trực tiếp cầm chuột, gõ phím và tương tác với máy tính của bạn như một con người thực thụ (Computer Use).

## Bài 2.1: Kỹ thuật Screenshot & DOM Parsing
AI không thể trực tiếp chạy phần mềm như chúng ta. Để AI thao tác được, ta cần làm 2 việc:
1. **Screenshot:** Chụp màn hình liên tục mỗi giây và gửi bức ảnh đó cho Vision Model (VLM).
2. **DOM/Accessibility Parsing:** Đối với trình duyệt Web, thay vì bắt AI nhìn bức ảnh vô hồn, ta trích xuất Cây DOM (HTML) hoặc Cây Accessibility (Tương tác trợ năng) thành dạng Text. DOM chứa chính xác thông tin: Nút bấm A ở đâu, Form nhập B tên là gì. Sự kết hợp giữa Hình ảnh (Screenshot) và Văn bản cấu trúc (DOM) giúp AI không bao giờ click trượt.

## Bài 2.2: Browser Automation Agent (Playwright)
Để AI click chuột trên Web, chúng ta sử dụng `Playwright` hoặc `Selenium`.
Thay vì bạn tự code kịch bản cố định (ví dụ: chờ nút này hiện ra rồi click), bạn cung cấp `Playwright` cho AI dưới dạng **Tools**.
- AI gọi tool: `click_element(selector="#login-button")`
- AI gọi tool: `type_text(selector="#email", text="admin@example.com")`

Vòng lặp ReAct lúc này là: 
`Chụp ảnh màn hình` -> `AI phân tích xem đang ở trang nào` -> `Gọi Tool Click chuột` -> `Màn hình chuyển trang` -> `Chụp ảnh tiếp` -> `Phân tích...`

## Bài 2.3: Spatial Grounding (Gắn kết không gian tọa độ)
Một trong những thách thức lớn là bắt VLM xuất ra chính xác **Tọa độ (X, Y)** trên bức ảnh.
**Kỹ thuật Set-of-Mark (SoM):** 
Trước khi gửi ảnh màn hình cho AI, một lớp tiền xử lý (Pre-processing) sẽ tự động vẽ các Con số (1, 2, 3...) hoặc các Hộp màu (Bounding Boxes) đè lên tất cả các nút bấm trên giao diện.
Sau đó, Prompt sẽ hỏi: *"Bạn muốn click vào đâu?"*
AI chỉ cần trả lời: *"Click vào hộp số 5"*. Hệ thống sẽ dịch hộp số 5 thành tọa độ `(X=150, Y=300)` và điều khiển chuột click vào đó. Tránh hoàn toàn việc AI đoán sai tọa độ.
