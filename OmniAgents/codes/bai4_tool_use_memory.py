from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

# ==============================================================
# BÀI 4: OMNI-AGENT DÙNG CÔNG CỤ (TOOL-USE) VÀ CÓ TRÍ NHỚ (MEMORY)
# ==============================================================


# 1. Chế tạo Công cụ (Tool) cho AI
@tool
def tra_cuu_khach_hang(ten_khach_hang: str) -> str:
    """Sử dụng công cụ này để tra cứu điểm tích luỹ của khách hàng."""
    print(f"\n[🛠️ CÔNG CỤ] Đang móc nối Database để tra cứu cho: '{ten_khach_hang}'...")
    db_gia_lap = {
        "sơn": "Sếp Sơn hiện có 9000 điểm tích luỹ VIP.",
        "nam": "Khách hàng Nam có 200 điểm tích luỹ.",
    }
    ten = ten_khach_hang.lower()
    for key in db_gia_lap:
        if key in ten:
            return db_gia_lap[key]
    return "Không tìm thấy khách hàng này trong hệ thống."


tools = [tra_cuu_khach_hang]


# 2. Định nghĩa State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# 3. Khởi tạo Não bộ (LLM) hỗ trợ Tool Calling
# Qwen 2.5 và Llama 3.2 đều hỗ trợ Tool Calling cực tốt
llm = ChatOllama(
    base_url="http://192.168.1.99:11434",
    model="llama3.2:latest",  # Dùng Qwen 14B siêu thông minh làm não bộ logic
    temperature=0,
)
# Gắn công cụ vào não bộ (Giống như đưa máy tính bỏ túi cho học sinh)
llm_with_tools = llm.bind_tools(tools)


def reasoner_node(state: AgentState):
    print("\n[🧠 NÃO BỘ] Đang đọc tin nhắn và suy nghĩ xem có cần dùng Tool không...")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# Điều hướng: Nếu AI đòi dùng Tool, rẽ sang Node Tool. Nếu không, kết thúc.
def router_edge(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print(f"-> 🗣️ AI quyết định GỌI CÔNG CỤ: {last_message.tool_calls[0]['name']}")
        return "tools"
    print("-> 🗣️ AI đã trả lời trực tiếp, không cần dùng công cụ.")
    return END


# 4. Ráp đồ thị LangGraph
workflow = StateGraph(AgentState)
workflow.add_node("agent", reasoner_node)
workflow.add_node(
    "tools", ToolNode(tools)
)  # Node chuyên chạy Tool do LangGraph cấp sẵn

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", router_edge, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")  # Chạy tool xong quay lại não bộ báo cáo

# Thêm "BỘ NHỚ NGẮN HẠN" (MemorySaver)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def run():
    print("=" * 60)
    print("🕸️ BÀI 4: LANGGRAPH SỬ DỤNG TOOLS VÀ MEMORY")
    print("=" * 60)

    # Session ID để phân biệt các cuộc hội thoại khác nhau
    config = {"configurable": {"thread_id": "phien_lam_viec_boss_son"}}

    # ---------------------------------------------------------
    # TÌNH HUỐNG 1: Ép AI dùng Tool
    # ---------------------------------------------------------
    print("\n👤 User: Kiểm tra giúp tôi xem Sếp Sơn có bao nhiêu điểm tích luỹ?")
    initial_state = {
        "messages": [
            HumanMessage(
                content="Kiểm tra giúp tôi xem Sếp Sơn có bao nhiêu điểm tích luỹ?"
            )
        ]
    }

    # Chạy luồng
    for event in app.stream(initial_state, config=config, stream_mode="values"):
        pass  # In log từ bên trong node
    print("\n🤖 AI trả lời:", app.get_state(config).values["messages"][-1].content)

    # ---------------------------------------------------------
    # TÌNH HUỐNG 2: AI tự nhớ ngữ cảnh cũ (Memory)
    # ---------------------------------------------------------
    print("\n" + "-" * 40)
    print("👤 User: Anh ấy còn thiếu bao nhiêu điểm nữa để đạt 10.000 điểm?")
    follow_up_state = {
        "messages": [
            HumanMessage(
                content="Anh ấy còn thiếu bao nhiêu điểm nữa để đạt 10.000 điểm?"
            )
        ]
    }

    for event in app.stream(follow_up_state, config=config, stream_mode="values"):
        pass
    print("\n🤖 AI trả lời:", app.get_state(config).values["messages"][-1].content)


if __name__ == "__main__":
    run()
