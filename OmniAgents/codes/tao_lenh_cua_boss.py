import os
import subprocess

# Kịch bản hội thoại dài khoảng 30 giây
# Có sử dụng thẻ [[slnc 1500]] để tạo khoảng nghỉ (silence) 1.5 giây giữa các câu nói
text = """Good morning, David. Could you come into my office for a moment?
[[slnc 1500]]
Good morning, Mr. Smith. Sure, I am on my way.
[[slnc 2000]]
Did you want to see me, sir?
[[slnc 1000]]
Yes, David. I need you to prioritize the Q 3 marketing report today. The board of directors wants to review it tomorrow morning.
[[slnc 1500]]
Understood. I will put everything else on hold and get it to you by 4 PM for your final review.
[[slnc 1000]]
Excellent. Let me know if you need any additional data from the sales team.
[[slnc 1000]]
Will do, Mr. Smith. I will get right on it."""

def tao_audio():
    # Thư mục hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    temp_aiff = os.path.join(current_dir, "temp_lenh.aiff")
    output_wav = os.path.join(current_dir, "lenh_cua_boss.wav")

    print(f"🎙️ Đang tạo file âm thanh bằng công cụ 'say' của macOS (Giọng: Alex)...")
    # Tạo file AIFF
    subprocess.run(["say", "-v", "Alex", "-o", temp_aiff, text])

    print(f"🔄 Đang chuyển đổi sang định dạng .wav chuẩn...")
    # Chuyển đổi AIFF sang WAV
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", temp_aiff, output_wav])

    # Xóa file tạm
    if os.path.exists(temp_aiff):
        os.remove(temp_aiff)

    print(f"✅ Hoàn tất! Đã tạo thành công file: {output_wav}")

if __name__ == "__main__":
    tao_audio()
