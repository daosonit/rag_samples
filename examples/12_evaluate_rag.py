import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

load_dotenv()
ollama_url = os.environ.get("OLLAMA_URL", "http://192.168.1.99:11434")

print("1. Khởi tạo Giám khảo AI (LLM-as-a-judge)...")
# Giám khảo cần thông minh và khắt khe, temperature = 0 để chấm điểm khách quan nhất
judge_llm = ChatOllama(model="qwen2.5:14b", base_url=ollama_url, temperature=0)

# Dữ liệu giả lập của một hệ thống RAG vừa trả lời xong
question = "Chính sách thai sản của công ty là gì?"
retrieved_context = (
    "Nhân viên nữ được nghỉ thai sản 6 tháng có lương. Phụ cấp thêm 5 triệu đồng/tháng."
)

# Tình huống 1: AI ngoan ngoãn
answer_good = "Công ty cho phép nhân viên nữ nghỉ thai sản 6 tháng và nhận phụ cấp 5 triệu mỗi tháng."

# Tình huống 2: AI bị ảo giác (Bịa thêm thông tin không có trong context)
answer_hallucinated = "Công ty cho phép nghỉ thai sản 6 tháng. Ngoài ra nhân viên nam cũng được nghỉ 1 tháng."


print("\n2. Kiểm tra ĐỘ TRUNG THÀNH (Faithfulness)...")
# Faithfulness: Trả lời có bịa chuyện ngoài Context không?
faithfulness_prompt = PromptTemplate(
    input_variables=["context", "answer"],
    template="""Bạn là một giám khảo chấm điểm khắt khe. 
Hãy đọc Ngữ cảnh (Context) và Câu trả lời (Answer) dưới đây.
Nhiệm vụ: Câu trả lời có chứa thông tin nào BỊA ĐẶT, KHÔNG HỀ XUẤT HIỆN trong Ngữ cảnh hay không?
Nếu KHÔNG bịa đặt, hãy trả lời: ĐIỂM 10/10.
Nếu CÓ thông tin bịa đặt, hãy trả lời: ĐIỂM 0/10 và giải thích.

[Ngữ cảnh]: {context}
[Câu trả lời]: {answer}
""",
)

chain = faithfulness_prompt | judge_llm

print("\n--- Chấm điểm Câu trả lời TỐT ---")
score_good = chain.invoke({"context": retrieved_context, "answer": answer_good})
print(score_good.content)

print("\n--- Chấm điểm Câu trả lời ẢO GIÁC (Bịa chuyện) ---")
score_bad = chain.invoke({"context": retrieved_context, "answer": answer_hallucinated})
print(score_bad.content)
