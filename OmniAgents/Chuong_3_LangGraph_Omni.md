# CHẶNG 3: KIẾN TRÚC OMNI-AGENT VỚI LANGGRAPH 🧠🕸️

Làm sao để kết hợp Hình ảnh, Âm thanh, Thao tác Web và Lý luận logic vào chung một hệ thống không bị crash? Chúng ta cần LangGraph. LangGraph giúp duy trì trạng thái (State) và phân luồng phức tạp.

## Bài 3.1: StateGraph Đa phương thức
Khác với Agentic RAG chỉ có Text, State của Omni-Agent sẽ chứa thêm:
```python
class OmniState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_screenshot: str # Base64 ảnh màn hình hiện tại
    active_url: str # URL đang đứng
    user_audio: bytes # Luồng âm thanh từ Mic
```
Mỗi khi LangGraph chạy qua một vòng lặp, `current_screenshot` sẽ được cập nhật lại để AI luôn "nhìn" thấy thực tại mới nhất.

## Bài 3.2: Xử lý Luồng (Streaming) Thời gian thực
Omni-Agent đòi hỏi tốc độ. Nếu bạn đợi Agent phân tích ảnh -> sinh văn bản -> chuyển sang giọng nói -> rồi mới phát ra loa, User sẽ phải đợi 5-10 giây cho một câu trả lời.
**Giải pháp:** Streaming Token. 
Khi LangGraph nhả ra từng Token chữ, bạn hứng các Token đó và quăng ngay vào TTS Engine. AI vừa suy nghĩ xong từ "Xin chào", loa đã bắt đầu phát "Xin chào", trong lúc đó AI nghĩ tiếp đoạn sau. Sự kết hợp giữa `astream_events` của LangChain và WebSockets là cốt lõi của tính năng này.

## Bài 3.3: Visual Self-Correction (Sửa sai bằng mắt)
Trong môi trường Web, AI thường xuyên click nhầm hoặc Web tải chậm.
**Kiến trúc Sửa sai:**
- AI gọi Tool `click(Nút Đăng Nhập)`.
- LangGraph chuyển tới Node `Verify_Action` (Kiểm chứng).
- `Verify_Action` sẽ chụp ảnh màn hình mới, gọi một con VLM (Giám khảo) hỏi: *"Màn hình đã chuyển sang trang Dashboard chưa?"*
- Nếu Giám khảo bảo *"Chưa, vẫn ở trang cũ, có báo lỗi sai mật khẩu"*.
- LangGraph tự động kích hoạt **Conditional Edge**, bẻ lái luồng chạy quay ngược về Node phân tích lỗi, AI sẽ thử nhập mật khẩu khác.
Đây là điểm ưu việt tuyệt đối của LangGraph so với các Automation Tool cứng nhắc rẽ nhánh tĩnh.
