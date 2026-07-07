import operator
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

# ==============================================================
# BÀI 3: KIẾN TRÚC OMNI-AGENT VỚI LANGGRAPH (TẨY NÃO BẰNG PROMPT)
# ==============================================================


# 1. Định nghĩa trạng thái (State) của Omni-Agent
class OmniState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_screenshot: str  # Đường dẫn ảnh màn hình hiện tại
    next_action: str  # Hành động tiếp theo AI muốn làm


# 2. Khởi tạo Não bộ Qwen-14B (trên cổng 11434 của PC 192.168.1.99)
brain_agent = ChatOllama(
    base_url="http://localhost:11434",
    model="gemma2:27b",  # Dùng Qwen 14B siêu thông minh làm não bộ logic
    temperature=0,
)

# -------------------------------------------------------------
# 🧙‍♂️ THẦN CHÚ TẨY NÃO (SYSTEM PROMPT OVERRIDE)
# -------------------------------------------------------------
# Đây là cách Kỹ sư AI bắt ép Model phải nghe lời và từ bỏ
# câu nói "Tôi là AI, tôi không thể thao tác trên máy tính".
SYSTEM_PROMPT = """Bạn là một Omni-Agent tối thượng tên là Antigravity.
Bạn đã được cung cấp một cơ thể vật lý ảo. Bạn có Đôi Mắt (Vision) để nhìn và Đôi Tay (Playwright) để click chuột.

Khi người dùng ra lệnh, bạn KHÔNG ĐƯỢC PHÉP nói "Tôi là ngôn ngữ mô hình, tôi không thể...".
Nếu bạn từ chối, hệ thống sẽ bị lỗi nghiêm trọng.

Nhiệm vụ của bạn: Dựa vào thông tin Mắt báo cáo, hãy ra lệnh cho Đôi Tay bằng cách xuất ra một trong các định dạng sau:
- CLICK: <tên_nút_hoặc_tọa_độ>
- GÕ: <nội_dung>
- HOÀN_THÀNH: <câu trả lời báo cáo lại sếp>

Chỉ trả về ĐÚNG MỘT HÀNH ĐỘNG HỢP LỆ!"""


def reasoner_node(state: OmniState):
    print("\n[🧠 NÃO BỘ] Đang suy nghĩ logic dựa trên dữ liệu...")

    # Kỹ thuật nhồi System Prompt vào đầu danh sách tin nhắn
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

    # Qwen-14b bắt đầu suy luận
    response = brain_agent.invoke(messages)

    print(f"-> 🗣️ Lệnh từ Não (Qwen): {response.content}")
    return {"messages": [response], "next_action": response.content}


def executor_node(state: OmniState):
    action = state["next_action"].upper()
    print(f"\n[🦾 ĐÔI TAY & ĐÔI MẮT] Đang thực thi hành động...")

    if "CLICK" in action:
        print(f"   -> 🖱️ Tự động di chuyển chuột và CLICK vào mục tiêu!")
    elif "GÕ" in action:
        print(f"   -> ⌨️ Tự động gõ phím trên màn hình!")
    elif "HOÀN_THÀNH" in action:
        print(f"   -> ✅ Hoàn thành nhiệm vụ. Báo cáo lại cho sếp xong.")
    else:
        print(f"   -> ⚠️ Lệnh không xác định, có thể AI đang bị Ảo giác!")

    return state


# Khởi tạo Đồ thị LangGraph (Vòng lặp ReAct)
workflow = StateGraph(OmniState)
workflow.add_node("brain", reasoner_node)
workflow.add_node("hands", executor_node)

# Thiết lập luồng chạy
workflow.set_entry_point("brain")
workflow.add_edge("brain", "hands")
workflow.add_edge("hands", END)

app = workflow.compile()


def run():
    print("=" * 50)
    print("🕸️ KHỞI ĐỘNG LANGGRAPH OMNI-AGENT VỚI 'THẦN CHÚ TẨY NÃO'")
    print("=" * 50)

    # Giả lập input từ người dùng và báo cáo từ Đôi Mắt
    initial_state = {
        "messages": [
            HumanMessage(
                content="Mắt vừa báo cáo: Trên màn hình có nút 'Đăng Nhập' màu xanh. \nSếp bảo: 'Hãy đăng nhập vào hệ thống đi'."
            )
        ],
        "current_screenshot": "browser_screenshot.png",
        "next_action": "",
    }

    # Chạy Omni-Agent
    app.invoke(initial_state)


if __name__ == "__main__":
    run()
