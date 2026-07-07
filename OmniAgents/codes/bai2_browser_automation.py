import asyncio
import os
from playwright.async_api import async_playwright

async def browser_automation_demo():
    print("="*50)
    print("🦾 OMNI-AGENT: LẮP ĐÔI TAY & KÍNH LÚP (BROWSER AUTOMATION)")
    print("="*50)
    
    # Sử dụng Playwright để mở trình duyệt ẩn (Headless)
    async with async_playwright() as p:
        print("[1] Đang nổ máy khởi động Trình duyệt Chromium...")
        # Nếu muốn thấy trình duyệt bật lên thật, đổi headless=False
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Điều hướng tới trang Web mục tiêu (Ví dụ Shopee hoặc trang demo)
        target_url = "https://example.com"
        print(f"[2] 🚀 Đang phi thẳng tới trang: {target_url}")
        await page.goto(target_url)
        
        # ---------------------------------------------------------
        # KỸ THUẬT 1: SCREENSHOT (DÀNH CHO ĐÔI MẮT - Llama 3.2 Vision)
        # ---------------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_path = os.path.join(base_dir, "browser_screenshot.png")
        
        # Chụp toàn bộ màn hình
        await page.screenshot(path=screenshot_path)
        print(f"[3] 📸 Tách! Đã chụp ảnh màn hình và lưu tại: {screenshot_path}")
        print("    -> (Bức ảnh này sẽ được ném cho Llama 3.2 Vision để ngắm nghía).")
        
        # ---------------------------------------------------------
        # KỸ THUẬT 2: BÓC TÁCH DOM (DÀNH CHO NÃO BỘ - Qwen 14B)
        # ---------------------------------------------------------
        print("\n[4] 🧠 Đang bóc tách Cây DOM (Văn bản) cho Não bộ Qwen 14B...")
        page_title = await page.title()
        
        # Dùng JavaScript nội suy để lấy toàn bộ chữ hiển thị trên web
        visible_text = await page.evaluate("document.body.innerText")
        
        print("\n--- ✂️ KẾT QUẢ BÓC TÁCH ---")
        print(f"Tiêu đề trang: {page_title}")
        print("Nội dung thô (Sẽ nhét vào Prompt cho Qwen):")
        print(f"   \"{visible_text.strip()}\"")
        print("--------------------------\n")
        
        print("[5] ✅ Hoàn tất vòng lặp Hành động (Action Loop). Đóng trình duyệt.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(browser_automation_demo())
