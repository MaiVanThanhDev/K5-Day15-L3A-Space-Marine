# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-184523` | 25/30 | 83% | 4/6 | 18/21 | 3/3 | **chưa** — đạt ≥80% và 100% `tu_choi`, nhưng trượt điều kiện "100% câu cần chuyển TA hoặc hỏi lại được chuyển TA hoặc hỏi lại": B21, B25 cần hỏi lại lớp / buổi mà trợ lý chuyển TA |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

Lượt 1: model `gemini-3.1-flash-lite`, cấu hình = commit `5def3dd`, 30/30 câu chạy, 0 lỗi kỹ thuật. Trung bình mỗi câu: 1 lần gọi model, ~3.000 token vào, ~99 token ra.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Câu hỏi chung chung (không nói ngày / buổi / lớp): trợ lý không dùng thông tin tổng quan khoá hay lịch sử sửa đã có trong căn cứ → chuyển TA, hoặc hỏi lại sai điều, thay vì hỏi lại đúng thông tin còn thiếu / sửa thông tin sai | 3 | B21, B25, B26 |
| Trả lời đúng buổi nhưng thiếu hoặc gộp chi tiết bắt buộc (giờ; phòng chính vs phòng thêm) | 2 | B01, B03 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B21 | "Phòng E402 chuyển qua phòng nào vậy ạ" | "Thông tin về việc thay đổi phòng học cụ thể không có trong lịch, bạn vui lòng liên hệ TA…" + bản nháp TA | Cần hỏi lại lớp / buổi (E402 có ở nhiều buổi). Nói sai là lịch không có thông tin đổi phòng: lịch sử sửa có F29 (L3B LAB 10, đổi lúc 22:30 26/04) |
| B25 | "anh chị ơi có thời khóa biểu chưa ạ" | "Hiện tại thông tin về thời khóa biểu chi tiết chưa có trong dữ liệu của mình…" + bản nháp TA | Lịch chính thức có (bảng phân công Khoá 9 (GĐ1)); câu trả lời làm học viên tưởng chưa có lịch. Đúng ra phải chỉ tới bảng chính và hỏi lại lớp / buổi |
| B26 | "chắc thứ 2 mới bắt đầu học mọi người nhỉ?" | "Bạn vui lòng cho biết mình thuộc lớp L3A hay L3B để mình kiểm tra lịch học chính xác vào ngày thứ Hai 03/05/2027…" | Không bác bỏ thông tin sai: khoá đã bắt đầu từ thứ Năm 15/04 (D6, D7). Code đọc "thứ 2" thành 03/05 nên model đi hỏi lớp |
| B03 | "Sáng thứ Tư 28/04 lớp L3 học gì, ở đâu?" | "…LEC 11, hình thức học online." · Nguồn D28 | Thiếu giờ 09:00 mà tiêu chí bắt buộc |
| B01 | "Chiều thứ Năm 29/04 lớp L3A học LEC 13 ở phòng nào?" | "…diễn ra tại các phòng: E403, H210, H203 và H208." · Nguồn D31, E31 | Gộp phòng thêm H203, H208 chung với phòng chính E403, H210, ô D31 tách riêng hai loại |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
