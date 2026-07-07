# HÀNH TRÌNH CHINH PHỤC GRAPHRAG 3D VÀ VECTOR ĐỘNG 🌐⏳

_Đích đến: Vượt qua đồ thị tĩnh 2D. Đưa Đồ thị tri thức vào chiều Không gian (Spatial) và chiều Thời gian (Temporal) để AI dự đoán tương lai thay vì chỉ tra cứu quá khứ._

## ⏳ CHẶNG 1: ĐỒ THỊ THỜI GIAN - TEMPORAL GRAPHS (CƠ BẢN)

_Mục tiêu: Đưa chiều thứ 3 (Trục thời gian) vào Neo4j. Mọi mối quan hệ đều có hạn sử dụng._

- [ ] **Bài 1.1:** Khái niệm Temporal Knowledge Graphs. Biến Nodes tĩnh thành Event Nodes (Sự kiện).
- [ ] **Bài 1.2:** Cài cắm thuộc tính `valid_from` và `valid_until` trên các mối quan hệ (Edges). (VD: Sam Altman [LÀ_CEO] của OpenAI từ 2015 đến 11/2023, rồi từ 12/2023 đến nay).
- [ ] **Bài 1.3:** Truy vấn Cypher xuyên không: Kỹ thuật bắt AI trả lời câu hỏi _"Ai là người lãnh đạo công ty X vào thời điểm xảy ra sự kiện Y?"_

---

## 🌊 CHẶNG 2: VECTOR ĐỘNG - DYNAMIC EMBEDDINGS (NÂNG CAO)

_Mục tiêu: Chống lại sự "lão hóa" của Vector. Khi sự kiện mới xảy ra, Vector tự động biến đổi._

- [ ] **Bài 2.1:** Streaming RAG & Upsert Pipeline. Bơm dữ liệu thời gian thực (Real-time RSS, WebSocket) trực tiếp vào Neo4j mà không phải chạy lại toàn bộ hệ thống.
- [ ] **Bài 2.2:** Gắn Vector (Embeddings) lên Cạnh (Edges) thay vì chỉ gắn lên Nút (Nodes). Dùng Vector để đo đạc "Cường độ" của mối quan hệ thay đổi theo thời gian.
- [ ] **Bài 2.3:** Decay Functions (Hàm suy giảm). Tự động hạ điểm Vector Similarity của những thông tin lỗi thời. Tin tức hôm nay giá trị hơn tin tức 10 năm trước.

---

## 🌍 CHẶNG 3: SUY LUẬN KHÔNG GIAN VÀ THỜI GIAN (CHUYÊN GIA)

_Mục tiêu: Đưa chiều thứ 4 (Không gian địa lý) vào GraphRAG._

- [ ] **Bài 3.1:** Neo4j Spatial. Lưu trữ Tọa độ (Lat/Lon) và Đa giác (Polygons) trực tiếp lên Graph.
- [ ] **Bài 3.2:** Spatio-Temporal Queries (Truy vấn Không-Thời gian): _"Tìm tất cả các nhà cung cấp linh kiện AI nằm trong bán kính 100km từ nhà máy của tôi, đã từng hợp tác với tôi trong khoảng thời gian từ 2022-2024"_.
- [ ] **Bài 3.3:** Khả năng "Tiên tri" (Predictive RAG). Bắt LLM nhìn vào chuỗi sự kiện nối tiếp nhau trên Graph để dự đoán sự kiện tiếp theo (Predicting Next Edge).

---

## 👁️‍🗨️ CHẶNG 4: DỰ ÁN TỐT NGHIỆP - MẮT THẦN 4D (THẦN THÁNH)

_Mục tiêu: Triển khai một hệ thống GraphRAG động, tự lớn lên và tự thay đổi._

- [ ] **Bài 4.1:** Dự án "News Radar 4D".
  - Một Agent ẩn mình, liên tục bắt dữ liệu từ 50 tờ báo tài chính mỗi phút.
  - Khi có tin mới, hệ thống tự mọc ra Node sự kiện mới, tự nối Edge vào các Node cũ (Ví dụ: "Công ty A vừa mua lại Công ty B").
  - Trò có thể mở phần mềm lên, kéo thanh trượt Timeline để xem mạng lưới Đồ thị (Graph) phình to và thay đổi hình dáng như một sinh vật sống từ năm 2020 đến nay.
  - User hỏi: _"Nếu công ty A sụp đổ, dựa trên lịch sử quan hệ, công ty C có bị ảnh hưởng theo hiệu ứng domino không?"_. Hệ thống sẽ dò theo Graph thời gian thực và trả lời.
