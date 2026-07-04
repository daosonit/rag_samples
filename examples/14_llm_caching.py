import os
import time
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

load_dotenv()
ollama_url = os.environ.get("OLLAMA_URL", "http://192.168.1.99:11434")

print("1. Đang bật bộ nhớ đệm (Caching) bằng SQLite...")
# Dòng lệnh ma thuật giúp bạn tiết kiệm hàng ngàn đô la tiền API (Hoặc tiết kiệm 99% CPU máy chủ của bạn)
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

print("2. Khởi tạo LLM (Qwen2.5:14b)...")
llm = ChatOllama(model="qwen2.5:14b", base_url=ollama_url, temperature=0)

cau_hoi = "Tóm tắt lịch sử hình thành Trí tuệ nhân tạo (AI) trong 1 đoạn văn ngắn."

# ---------------------------------------------------------
# LẦN HỎI ĐẦU TIÊN (LLM PHẢI SUY NGHĨ THẬT)
# ---------------------------------------------------------
print(f"\n💬 Người dùng hỏi: '{cau_hoi}'")
print("\n⏳ [Lần 1]: LLM đang suy nghĩ... (Sẽ tốn thời gian)")

start_time = time.time()
response_1 = llm.invoke(cau_hoi)
end_time = time.time()

print(f"🤖 Trả lời: {response_1.content}")
print(f"⏱️ Thời gian phản hồi Lần 1: {end_time - start_time:.2f} giây")

# ---------------------------------------------------------
# LẦN HỎI THỨ HAI (LLM LẤY TỪ CACHE RA, KHÔNG CẦN NGHĨ)
# ---------------------------------------------------------
print("\n" + "="*50)
print(f"💬 Người dùng hỏi lại y hệt: '{cau_hoi}'")
print("\n⚡ [Lần 2]: LLM đang kiểm tra Cache...")

start_time = time.time()
response_2 = llm.invoke(cau_hoi)
end_time = time.time()

print(f"🤖 Trả lời: {response_2.content}")
print(f"⏱️ Thời gian phản hồi Lần 2: {end_time - start_time:.4f} giây")

print("\n✅ Bài học: Cùng một câu hỏi, lần 2 không hề chạm vào LLM mà đọc thẳng từ file database '.langchain_cache.db'!")
