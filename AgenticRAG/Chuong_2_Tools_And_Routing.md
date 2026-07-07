# 📖 TẬP 2: VŨ KHÍ CỦA AGENT (TOOLS & ROUTING)

## 1. Tool Calling (Function Calling)
LLM không có tay chân để chạm vào Database của bạn. Tool Calling là cơ chế giúp LLM "ra lệnh" cho Python chạy một hàm cụ thể.

```python
# Ví dụ định nghĩa một Tool bằng LangChain:
from langchain_core.tools import tool

@tool
def get_company_revenue(company_name: str) -> str:
    """Sử dụng công cụ này để tìm doanh thu của một công ty."""
    # Bên trong này có thể là Code SQL hoặc API Call
    if company_name == "Apple":
        return "383 tỷ USD"
    return "Không tìm thấy"

tools = [get_company_revenue]
llm_with_tools = llm.bind_tools(tools)
```

## 2. Semantic Router (Người gác cổng)
Đừng bắt một Agent làm mọi việc. Hãy dùng Semantic Router để phân loại câu hỏi ngay từ đầu.
- Nếu câu hỏi về Lịch sử -> Chuyển vào luồng `HistoryAgent`.
- Nếu câu hỏi về Toán học -> Chuyển vào luồng `MathAgent`.
Việc Router này hoạt động dựa trên Vector Search (nhúng câu hỏi của User thành Vector và đo khoảng cách với các "Tuyến đường" định sẵn).

## 3. Cơ chế Fallback (Dự phòng rủi ro)
Agent rất hay bị lỗi khi gọi Tool (vd: truyền sai tham số vào hàm Python).
Chúng ta phải thiết lập cơ chế Fallback:
- Nếu gọi Tool lỗi -> Bắt lỗi (Try/Catch) -> Trả lại lỗi đó cho LLM kèm câu chửi: *"Mày truyền tham số sai rồi, hãy nhìn lại hàm và truyền cho đúng!"*. LLM sẽ tự động sửa lỗi và gọi lại.
