import math
from langchain_ollama import OllamaEmbeddings


# ==========================================
# HÀM TOÁN HỌC: TÍNH COSINE SIMILARITY (ĐỘ TƯƠNG ĐỒNG)
# ==========================================
# Không dùng thư viện ngoài để trò hiểu bản chất Toán học
def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


# ==========================================
# BƯỚC 1: KHỞI TẠO EMBEDDING MODEL
# ==========================================
print("🧠 Khởi tạo Nomic-Embed-Text (Ollama)...")
# Sử dụng mô hình nhúng siêu nhẹ và chuẩn xác mà chúng ta đã cài đặt từ hồi GraphRAG
embeddings = OllamaEmbeddings(
    base_url="http://localhost:11434", model="nomic-embed-text"
)

# ==========================================
# BƯỚC 2: ĐỊNH NGHĨA CÁC "TUYẾN ĐƯỜNG" (ROUTES)
# ==========================================
# Đây là "định hướng" của từng tuyến. Semantic Router hoạt động bằng cách xem
# câu hỏi của User giống với định hướng nào nhất.

routes = {
    "math_route": "tính toán, toán học, cộng trừ nhân chia, con số, phép tính, giải tích",
    "history_route": "lịch sử, quá khứ, triều đại, chiến tranh, vị vua, năm thành lập, công ty ra đời",
    "weather_route": "thời tiết, dự báo, nắng mưa, nhiệt độ, bão, độ ẩm, hôm nay trời thế nào",
}

print("🔄 Đang nhúng (Embed) các tuyến đường thành Vector...")
# Nhúng các chuỗi này thành Vector để lưu lại
route_vectors = {name: embeddings.embed_query(text) for name, text in routes.items()}


# ==========================================
# BƯỚC 3: ĐỊNH TUYẾN CÂU HỎI USER (ROUTING)
# ==========================================
def semantic_router(user_query: str):
    print(f"\n👤 User hỏi: '{user_query}'")

    # 1. Nhúng câu hỏi của User thành Vector
    query_vector = embeddings.embed_query(user_query)

    # 2. So sánh khoảng cách Cosine với các tuyến đường
    scores = {}
    for route_name, route_vec in route_vectors.items():
        score = cosine_similarity(query_vector, route_vec)
        scores[route_name] = score

    # 3. Tìm tuyến đường có điểm cao nhất
    best_route = max(scores, key=scores.get)
    best_score = scores[best_route]

    # 4. Ngưỡng (Threshold) - Nếu điểm quá thấp tức là câu hỏi chitchat linh tinh
    THRESHOLD = 0.5
    if best_score < THRESHOLD:
        print("⚠️  Quyết định: CHITCHAT (Câu hỏi không thuộc chuyên môn nào)")
        return "chitchat_route"

    print(
        f"✅ Quyết định: Điều hướng vào luồng [{best_route.upper()}] (Độ tự tin: {best_score:.2f})"
    )

    # Chi tiết điểm số để debug
    print("   [Log điểm số]:")
    for r, s in scores.items():
        print(f"     - {r}: {s:.2f}")

    return best_route


# ==========================================
# CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    # Test 1: Hỏi Toán
    semantic_router("Làm sao để giải phương trình bậc hai?")

    # Test 2: Hỏi Lịch sử
    semantic_router("Trận chiến Điện Biên Phủ diễn ra năm nào?")

    # Test 3: Hỏi Thời tiết
    semantic_router("Sài Gòn ngày mai có mưa rào không?")

    # Test 4: Lừa hệ thống (Chitchat)
    semantic_router("Hôm nay tôi thất tình, buồn quá!")
