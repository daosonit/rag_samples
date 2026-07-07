# HÀNH TRÌNH CHINH PHỤC BẦY ĐÀN TIẾN HÓA (SELF-EVOLVING AGENTS) 🧬🧠
*Đích đến: Xây dựng một Hệ sinh thái AI biết tự sinh sản, tự viết code, tự vẽ luồng hoạt động (Graph) và tự tiêu diệt khi xong việc.*

## 🌱 CHẶNG 1: KHỞI NGUYÊN TIẾN HÓA (CƠ BẢN)
*Mục tiêu: Thoát khỏi việc gõ cứng (Hard-code) Prompt và Tools. Để AI tự quyết định nó cần công cụ gì.*

- [ ] **Bài 1.1:** Meta-Prompting. Kỹ thuật dùng "Đấng sáng tạo" (Meta-Agent) để tự động viết System Prompt cho các Agent con dựa trên yêu cầu của User.
- [ ] **Bài 1.2:** Dynamic Tool Creation. AI tự viết ra một hàm Python (Tool) mới toanh trong quá trình chạy, load vào bộ nhớ và sử dụng nó.
- [ ] **Bài 1.3:** Đánh giá độ tin cậy của Tool tự chế bằng Sandbox môi trường ảo.

---

## 🦠 CHẶNG 2: SINH SẢN VÀ TIÊU DIỆT (NÂNG CAO)
*Mục tiêu: Đưa LangGraph lên một tầm cao mới - Đồ thị động (Dynamic Graph) thay vì Đồ thị tĩnh.*

- [ ] **Bài 2.1:** Khái niệm "Swarm" (Bầy đàn) trong LangGraph. Động lực học của các Agent song song.
- [ ] **Bài 2.2:** Sinh sản (Spawning): Meta-Agent phân rã 1 Task khó thành 5 Task nhỏ, sau đó tự động `.add_node()` 5 con Lính on-the-fly (ngay trong lúc chạy).
- [ ] **Bài 2.3:** Tiêu diệt (Garbage Collection): Cách "giết" Agent con, gom dữ liệu về Node chính và giải phóng RAM cho Mac M4.

---

## 🧬 CHẶNG 3: ĐỘT BIẾN GEN VÀ TỰ SỬA SAI LÕI (CHUYÊN GIA)
*Mục tiêu: Bầy đàn không bao giờ sụp đổ (Fault-tolerance). Nếu 1 lối đi sai, nó tự vẽ lối đi khác.*

- [ ] **Bài 3.1:** Dynamic Routing (Re-wiring). Nếu Luồng A thất bại 3 lần, AI tự động thay đổi cấu trúc Edge của LangGraph để chuyển hướng sang Luồng B.
- [ ] **Bài 3.2:** Tự gỡ lỗi Code (Self-Debugging Agents). Agent tự sinh mã Python, nếu gặp Exception, nó tự đọc Traceback và sửa lại code cho đến khi chạy được.
- [ ] **Bài 3.3:** Ký ức Tiến hóa (Evolutionary Memory). Agent lưu lại bài học "Tại sao lần trước mình thất bại" vào Database để lần sau đẻ ra lính xịn hơn.

---

## 👑 CHẶNG 4: CHÚA TỂ BẦY ĐÀN (DỰ ÁN TỐT NGHIỆP)
*Mục tiêu: Triển khai một Swarm thực thụ xử lý dữ liệu Big Data khổng lồ.*

- [ ] **Bài 4.1:** Dự án "Market Devourer" (Kẻ nuốt chửng thị trường). 
  - User: *"Phân tích thị trường Bất Động Sản Hà Nội tuần qua và dự phóng."*
  - Chúa tể tự đẻ ra 10 con Lính. 1 con chui vào Database nội bộ, 9 con tự tỏa đi cào 9 trang báo khác nhau. 
  - Nếu gặp trang web chặn IP, con Lính tự đẻ ra 1 cái Tool Fake IP. 
  - Cuối cùng, bầy đàn gom dữ liệu về, Chúa tể hấp thụ toàn bộ, đúc kết thành Báo cáo PDF chuyên sâu và tự tắt hệ thống đi ngủ.
