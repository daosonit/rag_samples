import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
    ChatHuggingFace,
)
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Tải biến môi trường
load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
hf_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

if not hf_token:
    raise ValueError("Thiếu HUGGINGFACEHUB_API_TOKEN trong file .env")

# Khởi tạo Supabase Client
supabase: Client = create_client(supabase_url, supabase_key)

# 2. Cài đặt Mô hình Embedding (Chạy offline trên máy của bạn)
local_model_path = "./local_models/paraphrase-multilingual-MiniLM-L12-v2"

embeddings = HuggingFaceEmbeddings(model_name=local_model_path)

# 3. Kết nối Supabase thành Vector Store của LangChain
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="document_chunks_hf",
    query_name="match_documents_hf",
)

# 4. Thêm tài liệu mẫu vào Database (Ingestion)
print("Đang dùng AI nhúng (Embedding) và lưu tài liệu vào Supabase...")
docs = [
    "Công ty TNHH AI Việt Nam được thành lập năm 2021, chuyên về giải pháp trí tuệ nhân tạo.",
    "Doanh thu quý 3 năm 2023 của công ty AI Việt Nam đạt 50 tỷ đồng, tăng trưởng 20% so với cùng kỳ.",
    "Giám đốc điều hành (CEO) hiện tại của công ty AI Việt Nam là ông Nguyễn Văn Sơn.",
    "Sản phẩm chủ đạo của công ty là hệ thống RAG Enterprise tích hợp Supabase.",
]
vector_store.add_texts(docs)

# 5. Cài đặt Mô hình LLM (Sử dụng API miễn phí của HuggingFace)
print("Đang thiết lập não bộ LLM...")
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",  # Trở lại Qwen cực thông minh
    huggingfacehub_api_token=hf_token,
    temperature=0.1,
    max_new_tokens=512,
)
# Bọc LLM thành Chat Model để tương thích với chuẩn Conversational mới nhất của HuggingFace
chat_model = ChatHuggingFace(llm=llm)

# 6. Thiết lập Prompt Template (Lời nhắc để gông cùm AI)
prompt = PromptTemplate.from_template(
    """
Bạn là trợ lý AI nội bộ của công ty. Hãy trả lời câu hỏi dựa trên các thông tin được cung cấp dưới đây.
Tuyệt đối KHÔNG sử dụng kiến thức bên ngoài. Nếu thông tin không có, hãy nói "Tôi không tìm thấy thông tin này trong tài liệu".

THÔNG TIN ĐƯỢC CUNG CẤP:
{context}

CÂU HỎI CỦA NGƯỜI DÙNG: {question}

CÂU TRẢ LỜI CỦA BẠN:
"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 7. Lắp ráp Chuỗi RAG (RAG Chain LCEL)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | chat_model
    | StrOutputParser()
)

# 8. Chạy thử nghiệm RAG
if __name__ == "__main__":
    cau_hoi = "Giám đốc công ty là ai và doanh thu quý 3 năm 2023 đạt bao nhiêu?"
    print(f"\n💬 Người dùng hỏi: {cau_hoi}")
    print("🤖 AI đang suy nghĩ (Tìm kiếm Supabase + Sinh văn bản)...\n")

    ket_qua = rag_chain.invoke(cau_hoi)
    print(f"👉 AI Trả lời:{ket_qua}")
