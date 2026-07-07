import os
import base64
from openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from io import BytesIO
from PIL import Image

# ==========================================
# CẤU HÌNH CÁC GIÁC QUAN (SENSORS) CỦA AI
# ==========================================

# 1. ĐÔI TAI: Kết nối tới máy chủ PC (Whisper đang chạy ở cổng 8800)
# Giả lập OpenAI API Client để trỏ về mạng nội bộ
whisper_client = OpenAI(
    base_url="http://192.168.1.99:8800/v1", api_key="khong-can-mat-khau"
)

# 2. ĐÔI MẮT: Kết nối tới máy chủ PC (LLaVA đang chạy trên Ollama cổng 11434)
vision_agent = ChatOllama(
    base_url="http://192.168.1.99:11434",
    model="llama3.2-vision:latest",  # Đổi sang model xịn hơn mà PC của sếp đang có llava:latest
    temperature=0,
)

# ==========================================
# CÁC HÀM HOẠT ĐỘNG
# ==========================================


def nghe_am_thanh(audio_path: str) -> str:
    """Hàm giúp AI nghe một file âm thanh và dịch ra Text (STT)"""
    print(f"\n[🎧 TAI] Đang ném file {audio_path} sang PC để nghe lén...")

    if not os.path.exists(audio_path):
        print(
            f"Lỗi: Không tìm thấy file {audio_path}. Hãy tạo một file audio giả lập nhé!"
        )
        return "Bức ảnh này có màu gì và chụp cái gì?"  # Giả lập kết quả trả về

    with open(audio_path, "rb") as audio_file:
        transcription = whisper_client.audio.transcriptions.create(
            model="whisper-1", file=audio_file  # Tên mặc định của chuẩn API OpenAI
        )
    return transcription.text


def nhin_hinh_anh(image_path: str, question: str) -> str:
    """Hàm giúp AI nhìn ảnh và trả lời câu hỏi dựa trên ảnh"""
    print(f"\n[👁️ MẮT] Đang ném bức ảnh {image_path} và câu hỏi sang PC để phân tích...")

    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file {image_path}. Cần có ảnh để AI nhìn!")
        return ""

    # Chuyển ảnh thành chuỗi mã hóa Base64, khử nền trong suốt (RGBA -> RGB)
    try:
        img = Image.open(image_path).convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Lỗi khi xử lý ảnh: {e}")
        return ""

    # Ép kiểu cấu trúc Đa phương thức (Multimodal Message)
    message = HumanMessage(
        content=[
            {"type": "text", "text": question},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
            },
        ]
    )

    # Kích hoạt LLaVA
    response = vision_agent.invoke([message])
    return response.content


# ==========================================
# TỔNG DUYỆT (OMNI-AGENT CƠ BẢN)
# ==========================================
def chay_omni_agent():
    print("=" * 50)
    print("🚀 BẮT ĐẦU CHẠY OMNI-AGENT VỚI 192.168.1.99")
    print("=" * 50)

    # File mô phỏng (Bạn cần ném 2 file này vào cùng thư mục để chạy thật)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_am_thanh = os.path.join(base_dir, "lenh_cua_boss.wav")
    file_hinh_anh = os.path.join(base_dir, "man_hinh_shopee.png")

    # Bước 1: AI Nghe lệnh từ sếp
    cau_hoi = nghe_am_thanh(file_am_thanh)
    print(f"-> 🗣️ Sếp vừa nói: '{cau_hoi}'")

    # Bước 2: AI Nhìn ảnh và tìm câu trả lời
    if cau_hoi:
        cau_tra_loi = nhin_hinh_anh(file_hinh_anh, cau_hoi)
        print(f"-> 🤖 LLaVA trả lời: {cau_tra_loi}")


if __name__ == "__main__":
    chay_omni_agent()
