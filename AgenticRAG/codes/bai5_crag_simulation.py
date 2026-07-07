import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List


# ==========================================
# 1. ĐỊNH NGHĨA CUỐN SỔ TAY (STATE)
# ==========================================
# Khác với bài trước chỉ lưu messages, lần này State của ta phức tạp hơn
class AgentState(TypedDict):
    question: str
    documents: List[str]
    generation: str


# ==========================================
# 2. KHỞI TẠO BỘ NÃO (LLM)
# ==========================================
# (Trò có thể thay ChatOllama bằng ChatMLX nếu đã tải model HuggingFace về)
llm = ChatOllama(
    base_url="http://192.168.1.99:11434", model="qwen2.5:14b", temperature=0
)

# ==========================================
# 3. CÁC HÀM HÀNH ĐỘNG (NODES)
# ==========================================


def retrieve_node(state: AgentState):
    """Tìm kiếm trong Database nội bộ của công ty"""
    print("\n[🔍 NODE: RETRIEVE] Đang tìm kiếm trong Database nội bộ...")
    question = state["question"]

    # Mock data: Giả sử DB nội bộ chỉ có dữ liệu về Apple, không có Samsung
    if "apple" in question.lower():
        docs = ["Apple đạt doanh thu 383 tỷ USD năm 2023 nhờ bán iPhone."]
    else:
        docs = ["Quy định nghỉ phép năm 2023 của nhân viên là 12 ngày."]

    return {"documents": docs}


def grade_documents_node(state: AgentState):
    """LLM tự làm Giám khảo chấm điểm tài liệu (Self-Grading)"""
    print("\n[⚖️ NODE: GRADER] LLM đang tự chấm điểm tài liệu xem có liên quan không...")
    question = state["question"]
    docs = state["documents"]

    # Bắt LLM trả lời "yes" hoặc "no"
    prompt = f"""Bạn là một giám khảo.
    Câu hỏi của user: {question}
    Tài liệu tìm được: {docs[0]}
    Tài liệu này có chứa thông tin trả lời được câu hỏi không? Chỉ trả lời "yes" hoặc "no"."""

    response = llm.invoke([HumanMessage(content=prompt)]).content.lower()

    if "yes" in response:
        print("   => ĐÁNH GIÁ: Tài liệu CHUẨN (Relevant) ✅")
        return {"documents": docs}  # Giữ nguyên tài liệu
    else:
        print("   => ĐÁNH GIÁ: Tài liệu RÁC (Irrelevant) ❌ -> Xóa bỏ!")
        return {"documents": []}  # Vứt bỏ tài liệu vào sọt rác


def web_search_node(state: AgentState):
    """Cứu cánh (Fallback): Lên mạng tìm nếu DB nội bộ bị rác"""
    print("\n[🌐 NODE: WEB SEARCH] Kích hoạt chế độ Cứu cánh: Lên Google tìm kiếm...")
    question = state["question"]
    # Mock data tìm kiếm web
    web_result = f"Kết quả từ Google: Samsung đạt doanh thu 200 tỷ USD."
    return {"documents": [web_result]}


def generate_node(state: AgentState):
    """Sinh câu trả lời cuối cùng"""
    print("\n[✍️ NODE: GENERATE] Bắt đầu viết câu trả lời cuối cùng gửi cho User...")
    question = state["question"]
    docs = state["documents"]

    prompt = f"Dựa vào thông tin sau: {docs[0]}\nHãy trả lời câu hỏi: {question}"
    response = llm.invoke([HumanMessage(content=prompt)]).content

    return {"generation": response}


# ==========================================
# 4. HÀM QUYẾT ĐỊNH RẼ NHÁNH (CONDITIONAL EDGE)
# ==========================================
def check_relevance(state: AgentState):
    """Quyết định xem sẽ đi Sinh văn (Generate) hay đi Tra mạng (Web Search)"""
    # Nếu danh sách tài liệu trống (bị Giám khảo vứt vào sọt rác ở bước trước)
    if not state["documents"]:
        print("  => LỘ TRÌNH: Dữ liệu hỏng, rẽ sang hướng [WEB SEARCH]")
        return "web_search"
    else:
        print("  => LỘ TRÌNH: Dữ liệu tốt, rẽ sang hướng [GENERATE]")
        return "generate"


# ==========================================
# 5. XÂY DỰNG ĐỒ THỊ CRAG
# ==========================================
workflow = StateGraph(AgentState)

# Thêm các Node
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_documents_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_node)

# Bắt đầu tại Retrieve
workflow.set_entry_point("retrieve")

# Retrieve xong thì chuyển sang Grade để chấm điểm
workflow.add_edge("retrieve", "grade")

# Grade xong thì tới ngã tư rẽ nhánh
workflow.add_conditional_edges(
    "grade", check_relevance, {"web_search": "web_search", "generate": "generate"}
)

# Web Search xong thì quay lại Generate
workflow.add_edge("web_search", "generate")

# Generate xong thì Kết thúc
workflow.add_edge("generate", END)

# Compile thành App
app = workflow.compile()

# ==========================================
# 6. CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 THỬ NGHIỆM 1: CÂU HỎI CÓ SẴN TRONG DATABASE")
    print("=" * 50)
    user_query_1 = "Doanh thu của Apple là bao nhiêu?"
    print(f"👤 User: {user_query_1}")
    result_1 = app.invoke({"question": user_query_1})
    print(f"\n🎯 TRẢ LỜI: {result_1['generation']}")

    print("\n" + "=" * 50)
    print("🚀 THỬ NGHIỆM 2: CÂU HỎI KHÔNG CÓ TRONG DATABASE (KÍCH HOẠT CRAG)")
    print("=" * 50)
    user_query_2 = "Doanh thu của Samsung là bao nhiêu?"
    print(f"👤 User: {user_query_2}")
    result_2 = app.invoke({"question": user_query_2})
    print(f"\n🎯 TRẢ LỜI: {result_2['generation']}")
