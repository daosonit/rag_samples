import json
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode


# ==========================================
# 1. TẠO TOOLS (TAY CHÂN)
# ==========================================
@tool
def multiply(a: int, b: int) -> int:
    """Sử dụng công cụ này để nhân hai số nguyên với nhau."""
    print(f"\n[🔧 TOOL ĐANG CHẠY]: Đang tính {a} * {b}...")
    return a * b


tools = [multiply]

# ==========================================
# 2. KHỞI TẠO BỘ NÃO (LLM)
# ==========================================
# Gắn tay chân (tools) vào não bộ (LLM)
llm = ChatOllama(
    base_url="http://localhost:11434", model="qwen2.5:14b", temperature=0
).bind_tools(tools)

# ==========================================
# 3. ĐỊNH NGHĨA CÁC NODES (CÁC BƯỚC HÀNH ĐỘNG)
# ==========================================


# Node 1: Agent (LLM suy nghĩ và ra quyết định)
def chatbot_node(state: MessagesState):
    print("\n[🧠 LLM ĐANG SUY NGHĨ]...")
    # LLM đọc toàn bộ "Cuốn sổ" (state["messages"]) và đưa ra câu trả lời
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# Node 2: Thực thi Tool
# LangGraph cung cấp sẵn ToolNode để tự động chạy các tool mà LLM yêu cầu
tool_node = ToolNode(tools=tools)


# Node Rẽ nhánh (Conditional Edge): Giám khảo quyết định đi tiếp hay dừng ollama pull qwen2.5:14b && ollama pull qwen2.5:14b ollama pull nomic-embed-text ollama pull gemma2:27b
def should_continue(state: MessagesState):
    # Lấy tin nhắn cuối cùng trong sổ
    last_message = state["messages"][-1]

    # Nếu LLM bảo "Tôi muốn dùng Tool", chuyển hướng sang Node Tool
    if last_message.tool_calls:
        print("  => Quyết định: Rẽ sang ngã rẽ [SỬ DỤNG TOOL] ➡️")
        return "tools"

    # Nếu LLM bảo "Tôi đã có đủ thông tin, tôi trả lời bằng Text", chuyển hướng kết thúc
    print("  => Quyết định: Đã xong, rẽ sang ngã rẽ [KẾT THÚC] 🛑")
    return END


# ==========================================
# 4. VẼ SƠ ĐỒ ĐỒ THỊ (THE MAGIC)
# ==========================================
# MessagesState là một Class sổ tay có sẵn, chỉ chứa một mảng "messages"
workflow = StateGraph(MessagesState)

# Thêm 2 Node vào bản đồ
workflow.add_node("agent", chatbot_node)
workflow.add_node("tools", tool_node)

# Bắt đầu tại Node Agent
workflow.set_entry_point("agent")

# Từ Agent, đi qua Ngã tư rẽ nhánh
workflow.add_conditional_edges(
    "agent",
    should_continue,
)

# Từ Tool, BẮT BUỘC phải đi ngược lại Agent để Agent đọc kết quả Tool và chém gió tiếp
workflow.add_edge("tools", "agent")

# Compile thành App
app = workflow.compile()

# ==========================================
# 5. CHẠY THỬ VÒNG LẶP (THE LOOP)
# ==========================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 BẮT ĐẦU VÒNG LẶP LANGGRAPH")
    print("=" * 50)

    # User hỏi một câu cần phải suy nghĩ và dùng Tool
    user_input = "Hãy tính giúp tôi 55 nhân với 14 bằng bao nhiêu?"
    print(f"👤 User: {user_input}")

    # Khởi tạo cuốn sổ tay với câu hỏi đầu tiên
    initial_state = {"messages": [HumanMessage(content=user_input)]}

    # Chạy luồng Đồ thị
    final_state = app.invoke(initial_state)

    print("\n" + "=" * 50)
    print("🎯 KẾT QUẢ CUỐI CÙNG TỪ AGENT:")
    print(final_state["messages"][-1].content)
    print("=" * 50)
