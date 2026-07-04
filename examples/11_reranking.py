import os
from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

print("1. Khởi tạo danh sách tài liệu (Giả lập kết quả rác từ Vector Search trả về)...")
# Câu hỏi: "Làm thế nào để đăng ký nghỉ phép?"
cau_hoi = "Làm thế nào để đăng ký nghỉ phép?"

# Giả sử Vector Search trả về 4 tài liệu có điểm "ngữ nghĩa" na ná nhau.
# Có những tài liệu bị Vector đẩy lên Top nhưng thực ra không trả lời đúng trọng tâm.
docs = [
    Document(
        page_content="Công ty quy định nhân viên được nghỉ phép 12 ngày mỗi năm nhưng không được dồn sang năm sau."
    ),
    Document(
        page_content="Nhân viên nghỉ việc sẽ được thanh toán những ngày phép chưa dùng vào kỳ lương cuối cùng."
    ),
    Document(
        page_content="Để đăng ký nghỉ phép, nhân viên cần điền form và gửi email cho quản lý trực tiếp trước 3 ngày."
    ),
    Document(
        page_content="Khi quản lý đăng ký lịch làm việc và tăng ca, cần ghi rõ lý do để tính lương."
    ),
]

print("2. Đang tải mô hình Cross-Encoder (Chuyên gia soi xét lại)...")
# Mô hình reranker rất nhỏ nhưng cực kỳ thông minh. Đã được tải offline về thư mục local_models
reranker_model = CrossEncoder("./local_models/ms-marco-MiniLM-L-6-v2", max_length=512)

print("\n3. Đang tiến hành Re-ranking (Chấm điểm lại từng cặp)...")
# BẮT BUỘC: Cross-encoder đòi hỏi phải ghép cặp [Câu hỏi, Tài liệu]
pairs = [[cau_hoi, doc.page_content] for doc in docs]

# Yêu cầu mô hình chấm điểm mức độ phù hợp của từng cặp
scores = reranker_model.predict(pairs)

# Ghép điểm số vào tài liệu
for score, doc in zip(scores, docs):
    doc.metadata["rerank_score"] = score

# Sắp xếp lại (Sort) danh sách tài liệu từ điểm cao nhất xuống thấp nhất
docs_reranked = sorted(docs, key=lambda x: x.metadata["rerank_score"], reverse=True)

print(f"\n💬 Người dùng hỏi: '{cau_hoi}'")
print("\n✅ BẢNG XẾP HẠNG SAU KHI RE-RANK:")
for i, doc in enumerate(docs_reranked):
    print(f"--- Top {i+1} | Điểm tàn khốc: {doc.metadata['rerank_score']:.4f} ---")
    print(doc.page_content)
