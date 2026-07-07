# CHẶNG 1: NỀN TẢNG ĐA PHƯƠNG THỨC (CƠ BẢN) 👁️👂

Chào mừng bạn đến với Chặng đầu tiên của Omni-Agents. Ở chặng này, chúng ta sẽ lắp ráp các giác quan cơ bản cho AI: Mắt và Tai. Một AI không thể tương tác với thế giới nếu nó chỉ biết đọc văn bản.

## Bài 1.1: Vision-Language Models (VLM)

**Khái niệm:** VLM là mô hình AI có khả năng nhận đầu vào là CẢ văn bản lẫn hình ảnh. Trọng tâm của VLM là khả năng "hiểu" không gian 2D, đọc chữ trên ảnh (OCR), nhận diện vật thể và màu sắc.
**Mô hình tiêu biểu năm 2026:**

- `Qwen-VL` (Local / API)
- `LLaVA` (Local)
- `GPT-4o` (API)

**Cách hoạt động:**
VLM chia bức ảnh thành các ô vuông nhỏ (Patches), biến mỗi ô vuông thành các Vector (Vision Embeddings) và nối chúng với Vector văn bản để đưa vào bộ giải mã (Decoder). Nhờ đó, AI "nhìn" bức ảnh giống như đọc một đoạn văn bản dài.

## Bài 1.2: Audio & Speech Processing (Whisper & TTS)

Để AI nghe và nói, chúng ta sử dụng hệ thống chuyển đổi:

- **STT (Speech-to-Text):** Sử dụng `Whisper` của OpenAI. Nó bắt âm thanh, khử ồn, và biến luồng âm thanh thành Text siêu tốc độ.
- **TTS (Text-to-Speech):** Sử dụng các engine như ElevenLabs, XTTS, hoặc Edge TTS. Khi AI (Qwen) sinh ra văn bản, đoạn văn bản đó lập tức được đẩy qua TTS để phát ra âm thanh.
- **Real-time Voice:** Công nghệ Streaming. AI nói chữ nào ra, loa phát chữ đó ngay lập tức (độ trễ < 200ms).

## Bài 1.3: Tích hợp vào Prompt qua LangChain

Khi gọi API hoặc dùng LangChain, bức ảnh không được ném trực tiếp vào như một file thông thường, mà thường được mã hóa sang chuỗi **Base64**.

**Ví dụ cấu trúc Prompt Đa phương thức:**

```python
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Món ăn trong bức ảnh này là gì và có bao nhiêu calo?"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
    ]
}
```

LLM sẽ đọc cấu trúc này, nhận diện phần `image_url` và xử lý hình ảnh qua bộ phận Vision trước khi trả lời.
