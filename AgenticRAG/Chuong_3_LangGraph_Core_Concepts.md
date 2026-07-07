# 📖 TẬP 3: TRÁI TIM HỆ THỐNG - LANGGRAPH & WORKFLOWS

## 1. Tại sao lại là LangGraph?
LangChain truyền thống là những đường ống (Chains) đi thẳng từ A đến B. 
Nhưng tư duy của con người là một đường vòng (Cyclic): Làm -> Kiểm tra -> Sai -> Làm lại.
**LangGraph** sinh ra để biến Agent thành một cỗ máy trạng thái (State Machine). Nó cho phép luồng chạy quay ngược lại bước trước đó vô hạn lần cho đến khi thành công.

## 2. Các thành phần của LangGraph
- **State (Trạng thái):** Một cuốn sổ ghi chép (Thường là một Class trong Python). Cuốn sổ này được chuyền tay qua các bước.
- **Node (Nút):** Các hàm Python thực hiện công việc (vd: `retrieve_node`, `generate_node`). Nó đọc sổ (State) và ghi thêm thông tin vào sổ.
- **Edge (Cạnh):** Đường thẳng nối Node A sang Node B.
- **Conditional Edge (Cạnh có điều kiện - Rẽ nhánh):** Nơi "Trí tuệ" bùng nổ.
  - Từ Node A, gọi một LLM đóng vai trò Giám khảo. Giám khảo nói "Tốt" -> Đi đến Node End.
  - Giám khảo nói "Tệ" -> Quay ngược lại Node A để sửa.

## 3. Xây dựng Agent bằng LangGraph
```python
from langgraph.graph import StateGraph, END

# Khởi tạo đồ thị
workflow = StateGraph(AgentState)

# Thêm các Node (Hành động)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Định nghĩa luồng đi
workflow.set_entry_point("agent")

# Cạnh có điều kiện: Agent suy nghĩ xong, nếu cần gọi Tool thì đi sang "action", nếu không thì kết thúc
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

# Từ Tool phải quay ngược lại Agent để nó đánh giá kết quả
workflow.add_edge("action", "agent")

# Biên dịch thành một App chạy được
app = workflow.compile()
```
