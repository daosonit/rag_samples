import json
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# ==========================================
# BƯỚC 1: ĐỊNH NGHĨA CÁC CÔNG CỤ (TOOLS)
# ==========================================


# Sử dụng decorator @tool để biến một hàm Python bình thường thành Tool cho LLM.
# LƯU Ý: Phần Docstring (chuỗi ngoặc kép) là CỰC KỲ QUAN TRỌNG. LLM sẽ đọc nó để biết khi nào cần dùng.
@tool
def multiply(a: int, b: int) -> int:
    """Sử dụng công cụ này để nhân hai số nguyên với nhau.
    Chỉ dùng khi người dùng yêu cầu thực hiện phép nhân."""
    return a * b


@tool
def get_weather(location: str) -> str:
    """Sử dụng công cụ này để tra cứu thời tiết của một tỉnh/thành phố cụ thể."""
    # Đây là dữ liệu giả lập (Mock data). Thực tế bạn sẽ gọi API thời tiết ở đây.
    mock_db = {
        "hà nội": "Trời đang mưa to, 24 độ C",
        "hồ chí minh": "Trời nắng gắt, 35 độ C",
        "đà nẵng": "Mát mẻ, 28 độ C",
    }
    loc = location.lower()
    return mock_db.get(loc, f"Không tìm thấy dữ liệu thời tiết cho {location}")


# Gom các tool lại thành một mảng
tools = [multiply, get_weather]

# ==========================================
# BƯỚC 2: KHỞI TẠO LLM VÀ "TRANG BỊ" TOOL
# ==========================================

print("🤖 Đang khởi động não bộ (Qwen 2.5 14B)...")
# Khởi tạo mô hình qua Ollama (Cần đảm bảo Ollama đang chạy ở nền)
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:14b",
    temperature=0,  # Nhiệt độ = 0 để nó không sáng tạo linh tinh khi dùng hàm
)

# Bước quan trọng: "Gắn" tool vào não bộ của LLM
llm_with_tools = llm.bind_tools(tools)


# ==========================================
# BƯỚC 3: THỬ NGHIỆM (TESTING)
# ==========================================


def test_agent(query: str):
    print(f"\n👤 Bạn hỏi: '{query}'")

    # Đưa câu hỏi vào LLM
    messages = [HumanMessage(content=query)]

    # Lấy câu trả lời từ LLM (Chú ý: Lúc này LLM chưa thực sự CHẠY hàm, nó chỉ "RA LỆNH" chạy hàm)
    response = llm_with_tools.invoke(messages)

    # Kiểm tra xem LLM có quyết định dùng Tool không
    if response.tool_calls:
        print("🛠️  Agent quyết định dùng công cụ:")
        for tool_call in response.tool_calls:
            print(f"   - Tên công cụ: {tool_call['name']}")
            print(f"   - Tham số LLM truyền vào: {tool_call['args']}")

            # --- Thực thi hàm Python thật ---
            if tool_call["name"] == "multiply":
                ket_qua = multiply.invoke(tool_call["args"])
                print(f"   => KẾT QUẢ TỪ PYTHON: {ket_qua}")

            elif tool_call["name"] == "get_weather":
                ket_qua = get_weather.invoke(tool_call["args"])
                print(f"   => KẾT QUẢ TỪ PYTHON: {ket_qua}")
    else:
        # Nếu LLM thấy câu hỏi bình thường, không cần tool, nó sẽ tự chém gió
        print("💬 Agent trả lời trực tiếp (Không dùng công cụ):")
        print(f"   => {response.content}")


# Chạy thử 3 tình huống
if __name__ == "__main__":
    # Tình huống 1: Hỏi phép tính (Sẽ kích hoạt hàm multiply)
    test_agent("Hãy tính 150 nhân với 6 giúp tôi.")

    # Tình huống 2: Hỏi thời tiết (Sẽ kích hoạt hàm get_weather)
    test_agent("Thời tiết ở Đà Nẵng hôm nay thế nào?")

    # Tình huống 3: Hỏi chào hỏi bình thường (Sẽ KHÔNG kích hoạt Tool)
    test_agent("Xin chào, bạn là ai?")
