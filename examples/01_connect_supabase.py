import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Tải biến môi trường từ file .env (hoặc .env.example nếu đang test)
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError(
        "LỖI: Chưa cấu hình SUPABASE_URL hoặc SUPABASE_KEY trong file .env"
    )

# Khởi tạo client kết nối tới Supabase REST API
supabase: Client = create_client(url, key)


def check_connection():
    try:
        # Thử thực thi một truy vấn đơn giản để kiểm tra kết nối API
        # Đoạn code này cố lấy 1 bản ghi từ bảng hệ thống hoặc bảng bạn sẽ tạo sau này
        print(f"Đang kết nối API Gateway của Supabase tại {url}...")

        # Thử lấy danh sách bảng bằng cách call 1 RPC hoặc test query một bảng bất kỳ
        # Lưu ý: Nếu bảng "test_connection" không tồn tại, nó sẽ báo lỗi API hợp lệ (không phải lỗi timeout)
        response = supabase.table("test_connection").select("*").limit(1).execute()

    except Exception as e:
        error_str = str(e)
        if (
            'relation "public.test_connection" does not exist' in error_str
            or "Not Found" in error_str
            or "PGRST205" in error_str
        ):
            print(
                "✅ Kết nối tới Supabase API thành công! (Lỗi không thấy bảng là bình thường do ta chưa tạo bảng)."
            )
        else:
            print(f"❌ Lỗi kết nối API: {e}")


if __name__ == "__main__":
    check_connection()
