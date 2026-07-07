# 📖 TẬP 3: MỔ XẺ MICROSOFT GRAPHRAG VÀ THUẬT TOÁN LEIDEN

*Nằm trong Bộ Bách khoa toàn thư GraphRAG 5 Tập*
*Tác giả: Giáo sư AI & Đào Sơn*

---

## MỤC LỤC
1. [Sự bế tắc của Vector RAG với câu hỏi vĩ mô](#phan-1)
2. [Element Summaries: Biến Node thành Kho tàng](#phan-2)
3. [Thuật toán Leiden: Phép màu của Toán học](#phan-3)
4. [Community Summaries: Tuyệt chiêu của Microsoft](#phan-4)
5. [Global Search (Map-Reduce)](#phan-5)

---

## 1. SỰ BẾ TẮC CỦA VECTOR RAG VỚI CÂU HỎI VĨ MÔ <a name="phan-1"></a>

Trước khi Microsoft tung ra thư viện `graphrag`, giới AI toàn cầu đều đau đầu với một loại câu hỏi gọi là **Global Query (Câu hỏi Vĩ mô / Tổng quát)**.
Ví dụ: Bạn có 1.000 bài báo về một vụ scandal tài chính.
- *Câu hỏi Vi mô (Local):* "Ông A có chuyển tiền cho bà B không?" -> Vector RAG trả lời cực kỳ xuất sắc.
- *Câu hỏi Vĩ mô (Global):* "Chủ đề chính xuyên suốt 1.000 bài báo này là gì? Sự sụp đổ của công ty bắt nguồn từ đâu?" -> Vector RAG **sụp đổ**. 

Tại sao? Vì Vector Search hoạt động theo cơ chế Top-K (Chỉ lấy 5-10 đoạn văn có độ tương đồng cao nhất). Để trả lời câu hỏi tổng quát, LLM phải đọc TẤT CẢ 1.000 bài báo, điều này vượt quá giới hạn Token của bất kỳ LLM nào.

=> **Microsoft GraphRAG** ra đời để giải quyết bài toán Vĩ mô này!

---

## 2. ELEMENT SUMMARIES: BIẾN NODE THÀNH KHO TÀNG <a name="phan-2"></a>

Trong GraphRAG thông thường (LangChain), một Node chỉ là một cái tên vô tri vô giác: `{id: "Apple"}`.
Microsoft không chấp nhận điều đó. Họ tạo ra một khái niệm gọi là **Element Summaries**.

Mỗi khi hệ thống trích xuất ra một Thực thể (Entity) hoặc một Mối quan hệ (Edge), nó sẽ yêu cầu LLM viết một đoạn mô tả (Description) cực kỳ chi tiết nhét vào bên trong nó.

```json
// Thay vì chỉ lưu thế này:
{"head": "Steve Jobs", "relation": "FOUNDED", "tail": "Apple"}

// Microsoft lưu thế này:
{
  "entity": "Steve Jobs",
  "description": "Là một doanh nhân người Mỹ, người đồng sáng lập Apple Inc. Ông nổi tiếng với phong cách lãnh đạo độc đoán nhưng đầy tính nghệ thuật. Trong tài liệu này, ông được nhắc đến chủ yếu ở giai đoạn 2007 khi ra mắt iPhone."
}
```
Nhờ có Description này, khi Vector Search quét qua, nó có thể nắm bắt được toàn bộ **Ngữ cảnh (Context)** của Node đó mà không cần phải đi tìm lại văn bản gốc.

---

## 3. THUẬT TOÁN LEIDEN: PHÉP MÀU CỦA TOÁN HỌC <a name="phan-3"></a>

Khi Đồ thị của bạn có 1 triệu Node, nhìn vào sẽ thấy đen kịt như một đống tơ vò (Hairball). Làm sao để LLM đọc được nó?
Microsoft áp dụng một thuật toán Phân cụm Đồ thị (Graph Clustering) mang tên **Leiden Algorithm** (Thuật toán xịn nhất thế giới hiện nay, vượt trội hơn cả thuật toán Louvain huyền thoại).

**Bản chất của thuật toán Leiden:**
- Nó lướt qua đồ thị và gom các Node hay "chơi" với nhau thành một Cụm (Community).
- Phân chia theo **Thứ bậc (Hierarchical)**:
  - *Level 0 (Vi mô):* Nhóm 3-4 nhân viên trong cùng một phòng ban.
  - *Level 1 (Tầm trung):* Gộp các phòng ban lại thành 1 Công ty.
  - *Level 2 (Vĩ mô):* Gộp các công ty lại thành 1 Ngành công nghiệp.

Về mặt Toán học, Leiden tối ưu hóa một hàm số gọi là **Modularity (Độ mô-đun)**:
$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$
*(Thuật toán này liên tục xé nhỏ và gộp lại các cụm cho đến khi đạt được độ kết dính cao nhất, đồng thời tránh việc một cụm bị dính quá nhiều cụm nhỏ không liên quan).*

---

## 4. COMMUNITY SUMMARIES: TUYỆT CHIÊU CỦA MICROSOFT <a name="phan-4"></a>

Đây là thứ làm nên tên tuổi của Microsoft GraphRAG.
Sau khi thuật toán Leiden chia đồ thị thành hàng nghìn Cụm nhỏ, hệ thống sẽ thực hiện một bước cực kỳ "đốt tiền":

Nó ném **TẤT CẢ** các Node và Edge trong một Cụm (Community) vào mồm LLM và ra lệnh:
> *"Đây là dữ liệu của Cụm số 15. Hãy đóng vai một chuyên gia phân tích, viết cho tôi một bản Báo cáo dài 2 trang tóm tắt lại toàn bộ những gì đang diễn ra trong Cụm này. Ai là nhân vật chính? Mối đe dọa là gì?"*

Hệ thống sẽ làm điều này với hàng nghìn Cụm. Kết quả là, từ 1 triệu Node rải rác, giờ đây ta có 100 bản **Báo cáo (Reports)** cực kỳ súc tích, văn phong mượt mà do con người (hoặc LLM) viết ra.

---

## 5. GLOBAL SEARCH (TÌM KIẾM VĨ MÔ - MAP-REDUCE) <a name="phan-5"></a>

Cuối cùng, khi User hỏi: *"Chủ đề chính của 1000 bài báo này là gì?"*

Hệ thống sẽ KHÔNG quét qua 1 triệu Node nữa. Nó sẽ chạy thuật toán **Map-Reduce** trên 100 bản Báo cáo (Community Summaries) đã được viết ở trên:

### Bước 1: MAP (Chấm điểm song song)
Hệ thống ném 100 bản báo cáo đó cho 100 luồng (threads) LLM khác nhau cùng đọc và hỏi:
*"Bản báo cáo này có chứa câu trả lời cho câu hỏi của User không? Nếu có, hãy chấm điểm từ 0-100 và tóm tắt lại đoạn liên quan."*

### Bước 2: REDUCE (Chốt sổ)
Hệ thống lấy những bản báo cáo được chấm điểm cao nhất (Ví dụ lấy Top 10), gộp chúng lại làm Ngữ cảnh (Context) cuối cùng và ném cho LLM (GPT-4) phán quyết:
*"Dựa trên 10 báo cáo này, hãy viết câu trả lời hoàn chỉnh cuối cùng cho User."*

> [!WARNING]
> **Cảnh báo độ "Ngốn tiền":** 
> Nếu bạn dùng ChatGPT API (GPT-4o) cho quá trình tạo Community Summaries và Global Search, tài khoản của bạn sẽ "bốc hơi" vài chục đô la chỉ trong 10 phút. Đó là lý do vì sao ở **Tập 4**, Giáo sư sẽ hướng dẫn bạn cách tối ưu chi phí bằng SLM (Small Language Models)!

---
*(Hết Tập 3. Mời bạn đón đọc Tập 4: Kiến trúc Hybrid & Tối ưu chi phí (Dành cho Chuyên gia)).*
