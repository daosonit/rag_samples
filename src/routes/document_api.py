import os
import uuid
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.rag_pipeline import RAGPipeline

router = APIRouter(prefix="/api/documents", tags=["Documents"])

NAMESPACE_ENTERPRISE = uuid.UUID("7ba7b810-9dad-11d1-80b4-00c04fd430c9")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(
        ..., description="ID của công ty/người dùng (VD: tenant_001)"
    ),
):
    """
    Nhận file PDF, cắt nhỏ, nhúng Vector 1024 chiều và đẩy lên Supabase với RLS
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF")

    # 1. Lưu file tạm thời để PyPDFLoader có thể đọc
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # 2. Đọc file PDF
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        # 3. Phân mảnh (Chunking) theo chuẩn bài 2.3
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_documents(pages)

        # 4. Gắn siêu dữ liệu (Metadata) và UUID chống trùng lặp
        ids = []
        for i, chunk in enumerate(chunks):
            # Ép buộc tenant_id để bảo mật RLS
            chunk.metadata["tenant_id"] = tenant_id
            chunk.metadata["source"] = file.filename

            # Tạo UUID từ nội dung + tên file + tenant
            unique_str = f"{tenant_id}_{file.filename}_{chunk.page_content}"
            ids.append(str(uuid.uuid5(NAMESPACE_ENTERPRISE, unique_str)))

        # 5. Lưu vào Database
        vector_store = RAGPipeline.get_vector_store()
        vector_store.add_documents(documents=chunks, ids=ids)

        return {
            "status": "success",
            "message": f"Đã xử lý và nhúng thành công {len(chunks)} đoạn văn bản.",
            "tenant_id": tenant_id,
            "filename": file.filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Dọn dẹp file rác
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
