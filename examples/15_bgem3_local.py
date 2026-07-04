import time
from FlagEmbedding import BGEM3FlagModel

print("1. Đang khởi tạo 'Quái vật' BGE-M3 từ bộ nhớ Offline...")
# Khởi tạo mô hình. Tham số use_fp16=True giúp giảm một nửa dung lượng RAM (chỉ dùng khoảng 1.5GB RAM)
model = BGEM3FlagModel('./local_models/bge-m3', use_fp16=True)

# 2 câu văn để test
sentences = [
    "Công ty AIVN được thành lập vào năm 2024.",
    "AIVN is a company founded in 2024."
]

print("\n2. Đang nén dữ liệu... (Chỉ 1 lần chạy, sinh ra cả 3 phép thuật)")
start = time.time()
# return_dense: Bật Vector Ý nghĩa
# return_sparse: Bật Vector Từ khóa (như BM25)
# return_colbert_vecs: Bật Vector Re-ranking (Ma trận từ-đối-từ)
output = model.encode(
    sentences, 
    return_dense=True, 
    return_sparse=True, 
    return_colbert_vecs=True
)
end = time.time()

print(f"✅ Xong trong {end - start:.2f} giây!\n")

print("--- PHÉP THUẬT 1: DENSE VECTOR (1024 chiều) ---")
# Đây là thứ thay thế cho MiniLM 384 chiều
dense_vecs = output['dense_vecs']
print(f"Kích thước vector câu 1: {dense_vecs[0].shape}") 
print(f"Vài con số đầu tiên: {dense_vecs[0][:5]}\n")

print("--- PHÉP THUẬT 2: SPARSE VECTOR (Ma trận từ khóa chính xác) ---")
# Trọng số từ khóa chính xác (Giống hệt BM25 nhưng thông minh hơn)
sparse_vecs = output['lexical_weights']
print(f"Trọng số từ khóa câu 1: {sparse_vecs[0]}\n")

print("--- PHÉP THUẬT 3: COLBERT (Ma trận chấm điểm chéo) ---")
# Mỗi một TỪ trong câu văn sẽ được biến thành 1 vector 1024 chiều riêng biệt!
colbert_vecs = output['colbert_vecs']
print(f"Kích thước ma trận ColBERT câu 1: {colbert_vecs[0].shape}") 
print("(Cực kỳ nặng và chi tiết, dùng để Re-rank thay thế Cross-Encoder)")
