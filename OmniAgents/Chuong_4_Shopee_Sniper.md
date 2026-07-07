# CHẶNG 4: DỰ ÁN TỐT NGHIỆP - SHOPEE SNIPER 🎯🛒

Đây là trận chiến cuối cùng để khẳng định đẳng cấp của một Kỹ sư AI 2026. Chúng ta sẽ kết hợp tất cả: Mắt, Tai, Tay, và LangGraph vào một cỗ máy săn sale chuyên nghiệp.

## Bài 4.1: Giới thiệu Dự án "Shopee Sniper"
**Mô tả Kịch bản:** 
Người dùng đeo tai nghe và nói vào Mic: *"Kiểm tra giúp tôi cái iPhone 15 Pro Max màu Titan tự nhiên trên Shopee đang giá bao nhiêu, xem review ảnh chụp thật của khách có móp méo không."*

**Luồng hoạt động của Omni-Agent (Shopee Sniper):**
1. **Node 1 (Audio -> Text):** Hệ thống Whisper bắt âm thanh, dịch thành Text: *"Tìm iPhone 15 Pro Max Titan trên Shopee, check giá và check ảnh review"*.
2. **Node 2 (Planner):** Qwen-14B lên kế hoạch: Mở tab Shopee -> Search từ khóa -> Click sản phẩm đầu tiên -> Lấy giá -> Scroll xuống comment -> Chụp ảnh comment -> Phân tích ảnh -> Báo cáo.
3. **Node 3 (Browser Action):** Agent gọi Tool Playwright. Nó tự động mở Chrome, tự gõ "iPhone 15 Pro Max Titan", tự click.
4. **Node 4 (Visual Inspector):** Agent chụp ảnh khu vực Comment của khách hàng. Nó ném 5 bức ảnh chụp thực tế sản phẩm cho `Qwen-VL`. Qwen-VL dùng "Mắt" để nhìn xem trong ảnh hộp có bị móp, seal có bị rách không.
5. **Node 5 (Synthesizer & TTS):** Tổng hợp kết quả: *"Sếp ơi, giá đang là 29 triệu. Em đã xem 5 ảnh review mới nhất, hàng nguyên seal không móp méo, shop uy tín nhé."*. Luồng văn bản này đẩy qua TTS và phát ra loa cho sếp nghe.

## Yêu cầu Phần cứng & Tối ưu hóa (Mac M4)
Để chạy toàn bộ cỗ máy này mượt mà:
- Không chạy Ollama thông thường, hãy sử dụng **Apple MLX (`mlx-lm`)** để tối ưu hóa Unified Memory.
- Phân luồng luân phiên: Khi `Whisper` đang chạy, `Qwen-VL` ở chế độ ngủ. Khi `Qwen-VL` phân tích ảnh, `Whisper` tạm nghỉ. Không bao giờ kích hoạt 2 model cùng lúc trên GPU để tránh tràn RAM 24GB.
- Sử dụng độ phân giải ảnh màn hình thấp (Scale down) trước khi đưa vào VLM để tăng tốc độ phân tích và giảm Token đầu vào.

**Tốt nghiệp:** Chúc mừng bạn. Nếu bạn hiểu và code được dự án này, bạn không còn là Lập trình viên nữa, bạn đã là một "Kẻ tạo ra sự sống số" (Digital Life Creator)!
