from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from src.core.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str
    tenant_id: str


@router.post("/")
async def chat_with_document(request: ChatRequest):
    """
    Tìm kiếm thông tin theo câu hỏi, ép buộc phân quyền RLS theo tenant_id
    và dùng LLM tạo câu trả lời
    """
    try:
        # 1. Khởi tạo Vector Store & LLM
        vector_store = RAGPipeline.get_vector_store()
        llm = RAGPipeline.get_llm()

        # 2. Tìm kiếm ngữ nghĩa (Retrieval) - Bảo mật cấp độ Application (filter)
        docs = vector_store.similarity_search(
            query=request.query, k=3, filter={"tenant_id": request.tenant_id}
        )

        if not docs:
            return {
                "answer": "Hệ thống không tìm thấy tài liệu nào khớp với câu hỏi của bạn hoặc bạn không có quyền truy cập.",
                "sources": [],
            }

        # 3. Gộp nội dung tài liệu tìm được (Context)
        context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

        # 4. Xây dựng Prompt
        prompt_template = """Bạn là trợ lý AI nội bộ của công ty.
Sử dụng các tài liệu được cung cấp dưới đây để trả lời câu hỏi của người dùng.
Nếu trong tài liệu không có thông tin, hãy trả lời "Tôi không biết dựa trên tài liệu cung cấp". KHÔNG tự bịa ra câu trả lời.

TÀI LIỆU:
{context}

CÂU HỎI: {query}
TRẢ LỜI:"""

        prompt = PromptTemplate.from_template(prompt_template)
        chain = prompt | llm

        # 5. Gọi LLM sinh câu trả lời
        response = chain.invoke({"context": context_text, "query": request.query})

        # Trích xuất nguồn tài liệu để user tham khảo
        sources = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "content": doc.page_content,
            }
            for doc in docs
        ]

        return {"answer": response.content, "sources": sources}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
