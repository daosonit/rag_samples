from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.document_api import router as document_router
from src.routes.chat_api import router as chat_router

app = FastAPI(
    title="Enterprise Knowledge Base API",
    description="Hệ thống RAG nâng cao kết hợp BGE-M3 1024D, Qwen2.5 và Supabase RLS",
    version="1.0.0",
)

# Cấu hình CORS để Frontend (Web/Mobile) có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các API Routes
app.include_router(document_router)
app.include_router(chat_router)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "message": "Welcome to Enterprise RAG API! Truy cập /docs để xem tài liệu API.",
    }


# Để khởi chạy: uv run uvicorn src.main:app --reload --port 8000
