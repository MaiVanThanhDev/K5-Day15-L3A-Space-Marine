# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Không đào data thì xoá file này. Script / công thức đếm để trong repo (vd `evidence/count.py` hoặc ghi công thức Sheets ngay dưới), người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: kênh forum **🙋-hỏi-đáp** trên Discord công khai của khoá AI20K K5, đọc trực tiếp trên Discord (không xuất file), từ __ đến __ *(điền ngày bài cũ nhất / mới nhất)*.
- Đếm gì: **bài đăng** (post) hỏi về hạn nộp / phòng học / lịch học · trên tập nào: mọi bài đăng trong kênh · lọc gì: không lọc.
- **Mẫu số là gì:** N = tổng số bài đăng trong kênh (không phải số tin nhắn: tin trả lời, cảm ơn trong bài không tính).
- Cách đếm: đọc tay tiêu đề + câu đầu của từng bài, đánh dấu bài thuộc chủ đề hạn / phòng / lịch. Kênh là forum nên đếm theo bài sạch hơn đếm tin nhắn.
- Script `evidence/count.py` viết sẵn cho trường hợp xuất được file (DiscordChatExporter); **không dùng** ở lượt đếm này vì kênh chỉ có 18 bài.

## 2. Đọc trước, đếm sau

Đã đọc cả 18 bài. Các *kiểu* câu hỏi thấy được: __ *(vd lỗi code, thủ tục, hạn / phòng / lịch…)*

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Bài hỏi hạn nộp / phòng / lịch | 2/18 | — | n nhỏ, không ghi % |

**Không đạt ngưỡng nguồn** (N quá nhỏ). Dùng để đối chiếu với khảo sát, không làm nguồn chính.

## 4. ≥5 ví dụ cụ thể (nguyên văn, đã bỏ tên)

Tin học viên hỏi trên Discord của khoá (cũng là câu thử `data_that` B21–B30 trong `eval/benchmark.csv`):
1. "Phòng E402 chuyển qua phòng nào vậy ạ" — 14:15 21/11/2026
2. "cho mình xin link nộp bài lab sáng nay" — 22:36 06/11/2026
3. "… bài LAB03 deadline đến 17:30 là chốt luôn hay được kéo dài đến 23:59 như mấy bài trước ạ" — 14:51 10/11/2026
4. "bài lab chiều nay có phải nộp ko ạ, e ko thấy link nộp" — 23:30 20/11/2026
5. "Dạ e thấy phòng học có chung số kiểu h2xx mà nó chia 3a 3b thì sao mình biết mình thuộc bên nào ạ @@" — 21:33 04/11/2026
6. "… hôm qua em xem lịch thấy phòng ở dưới hôm nay em check lại thì thấy em ở phòng. h104 mà sáng nay em ngồi và điểm danh ở phòng c104 thì có sao không ạ" — 14:06 06/11/2026
7. "Mọi người cho e hỏi là lịch học ngày mai vào buổi chiều sẽ như nào vậy ạ? Hay mai mình chỉ học sáng thôi ạ, em thấy lịch chỉ ghi mỗi 9h-13h thôi ạ" — 18:04 05/11/2026

Ghi chú: 4 tin đầu khoá (04/11) hỏi "có thời khoá biểu / có lịch chưa" — thấy ngay từ ngày đầu học viên không biết tìm lịch ở đâu. Các tin này nằm ở kênh nào, có thuộc 18 bài đếm ở mục 3 không: __ *(điền)*.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Kênh hỏi-đáp chỉ có 18 bài: phần lớn học viên không hỏi ở đây (khảo sát: chỉ 3/18 học viên hỏi trên kênh hỏi đáp; 13/18 tự tra email / LMS, 8/18 nhắn riêng bạn). Vì vậy đếm kênh này **đánh giá thấp** việc tra cứu, lệch về phía những người chịu hỏi công khai.
→ Kiểm lại bằng khảo sát 20 phiếu (`evidence/survey/`), kết quả ở `evidence/summary.md`.
