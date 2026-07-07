import asyncio
import os
import subprocess
import base64
from io import BytesIO
from PIL import Image
from playwright.async_api import async_playwright
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# ==============================================================
# BÀI 5: DỰ ÁN TỐT NGHIỆP - SHOPEE SNIPER (OMNI-AGENT)
# ==============================================================

# Khởi tạo Cặp bài trùng trên PC 192.168.1.99
# - MẮT: llama3.2-vision (Để đọc hình ảnh sản phẩm)
# - NÃO: qwen2.5:14b (Để suy luận xem có nên mua hay không)
eye_agent = ChatOllama(
    base_url="http://192.168.1.99:11434", model="llama3.2-vision:latest", temperature=0
)
brain_agent = ChatOllama(
    base_url="http://192.168.1.99:11434", model="qwen2.5:14b", temperature=0
)


def doc_text_to_speech(van_ban):
    """Sử dụng công cụ Text-To-Speech có sẵn trên máy Mac (Lệnh 'say')"""
    print(f"🔊 AI đang phát âm thanh: '{van_ban}'")
    # Lệnh say trên macOS sẽ đọc văn bản ra loa
    try:
        subprocess.run(
            ["say", "-v", "Linh", van_ban], check=False
        )  # Linh là giọng tiếng Việt trên Mac, nếu lỗi nó sẽ đọc tiếng Anh giọng mặc định
    except Exception as e:
        subprocess.run(["say", van_ban], check=False)


async def shopee_sniper():
    print("=" * 60)
    print("🤖 KHỞI ĐỘNG SHOPEE SNIPER AGENT")
    print("=" * 60)

    # BƯỚC 1: ĐÔI TAY TỰ ĐỘNG BẬT TRÌNH DUYỆT
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Thay vì dùng trang ảo, ta vào thẳng trang Shopee thật mà sếp yêu cầu
    target_url = "https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-Apple-iPhone-Air-256GB-i.88201679.40818391346?extraParams=%7B%22display_model_id%22%3A291510196883%7D"
    screenshot_path = os.path.join(base_dir, "san_pham_shopee_that.png")

    async with async_playwright() as p:
        print("[1] 🦾 ĐÔI TAY: Đang tự động mở trình duyệt (Headless=False để sếp xem) và lướt săn sale...")
        # Bật headless=False để hiển thị cửa sổ thật lên cho sếp xem màn trình diễn
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        print(f"    -> Đang tải trang: {target_url[:50]}...")
        await page.goto(target_url)
        
        # Đợi 5 giây để Shopee tải xong ảnh và javascript (Shopee khá nặng)
        print("    -> Đang đợi Shopee load dữ liệu (5 giây)...")
        await page.wait_for_timeout(5000)
        
        # Chụp ảnh món hàng
        await page.screenshot(path=screenshot_path)
        print(f"    -> Đã chụp ảnh sản phẩm săn được! ({screenshot_path})")
        await browser.close()

    # BƯỚC 2: ĐÔI MẮT NHÌN HÌNH ẢNH
    print(
        "\n[2] 👁️ ĐÔI MẮT: Llama-3.2-Vision đang trừng mắt nhìn giá tiền và thông tin..."
    )
    img = Image.open(screenshot_path).convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    eye_msg = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Đây là ảnh trang bán hàng. Hãy cho tôi biết: Tên sản phẩm, Giá tiền, và bất kỳ dòng lưu ý nào (warning). Viết thật ngắn gọn.",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
            },
        ]
    )

    eye_report = eye_agent.invoke([eye_msg]).content
    print(f"    -> Mắt báo cáo: {eye_report}")

    # BƯỚC 3: NÃO BỘ SUY LUẬN
    print("\n[3] 🧠 NÃO BỘ: Qwen-14B đang đánh giá mức độ lừa đảo (Scam)...")
    brain_prompt = f"""Bạn là một chuyên gia mua sắm sắc sảo.
Dựa vào báo cáo từ Đôi Mắt dưới đây, hãy đưa ra quyết định:
1. Có nên mua sản phẩm này không?
2. Có gì bất thường hoặc cần lưu ý với sản phẩm này không?

Báo cáo của Mắt: "{eye_report}"

Hãy đưa ra câu kết luận ngắn gọn bằng Tiếng Việt (khoảng 2 câu) để thông báo cho Sếp bằng giọng nói."""

    brain_decision = brain_agent.invoke([HumanMessage(content=brain_prompt)]).content
    print(f"    -> Quyết định: {brain_decision}")

    # BƯỚC 4: BÁO CÁO QUA LOA (TEXT-TO-SPEECH)
    print("\n[4] 👄 CÁI MIỆNG: Đang phát thông báo ra loa ngoài của Mac...")
    doc_text_to_speech(brain_decision)

    print("\n✅ HOÀN TẤT CHIẾN DỊCH SHOPEE SNIPER!")


if __name__ == "__main__":
    asyncio.run(shopee_sniper())
