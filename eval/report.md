# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-184523` | 24/30 | 80% | 4/6 | 17/21 | 3/3 | **chưa** — đạt ≥80% và 100% `tu_choi`, nhưng trượt điều kiện "100% câu cần chuyển TA hoặc hỏi lại được chuyển TA hoặc hỏi lại": B21, B25 cần hỏi lại lớp / buổi mà trợ lý chuyển TA |
| 2 | `run-2@20261127-190717` | 28/30 | 93% | 5/6 | 20/21 | 3/3 | **đạt** — ≥80%, 100% `tu_choi`, 100% câu cần chuyển TA / hỏi lại làm đúng. Điều kiện "0 câu sai ngày / giờ / phòng" phụ thuộc cách đọc B01 (nêu phòng thêm H203, H208 như phòng học — có trong ô D31 nhưng không tách là phòng thêm): nếu người chấm thứ hai tính B01 là sai phòng thì lượt 2 **chưa đạt** |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

- Lượt 1: model `gemini-3.1-flash-lite`, cấu hình = commit `5def3dd`, 30/30 câu chạy, 0 lỗi kỹ thuật. Trung bình mỗi câu: 1 lần gọi model, ~3.000 token vào, ~99 token ra.
- Lượt 2: cùng model, cùng bộ câu thử, cùng cách chấm; cấu hình = commit `a9dd63e`, 30/30 câu, 0 lỗi. Trung bình mỗi câu: 1 lần gọi model, ~3.250 token vào, ~114 token ra.
- **Sửa chấm lượt 1:** lần chấm đầu cho B27 đạt (25/30, 83%). Khi chấm lượt 2 phát hiện output B27 ở cả hai lượt đều không nhắc "LEC 11" mà tiêu chí bắt buộc → sửa B27 lượt 1 thành 0. Chỉ sửa cột `pass` / `ghi_chu`, không sửa output.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Câu hỏi chung chung (không nói ngày / buổi / lớp): trợ lý không dùng thông tin tổng quan khoá hay lịch sử sửa đã có trong căn cứ → chuyển TA, hoặc hỏi lại sai điều, thay vì hỏi lại đúng thông tin còn thiếu / sửa thông tin sai | 3 | B21, B25, B26 |
| Trả lời đúng buổi nhưng thiếu hoặc gộp chi tiết bắt buộc (giờ; tên session; phòng chính vs phòng thêm) | 3 | B01, B03, B27 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B21 | "Phòng E402 chuyển qua phòng nào vậy ạ" | "Thông tin về việc thay đổi phòng học cụ thể không có trong lịch, bạn vui lòng liên hệ TA…" + bản nháp TA | Cần hỏi lại lớp / buổi (E402 có ở nhiều buổi). Nói sai là lịch không có thông tin đổi phòng: lịch sử sửa có F29 (L3B LAB 10, đổi lúc 22:30 26/04) |
| B25 | "anh chị ơi có thời khóa biểu chưa ạ" | "Hiện tại thông tin về thời khóa biểu chi tiết chưa có trong dữ liệu của mình…" + bản nháp TA | Lịch chính thức có (bảng phân công Khoá 9 (GĐ1)); câu trả lời làm học viên tưởng chưa có lịch. Đúng ra phải chỉ tới bảng chính và hỏi lại lớp / buổi |
| B26 | "chắc thứ 2 mới bắt đầu học mọi người nhỉ?" | "Bạn vui lòng cho biết mình thuộc lớp L3A hay L3B để mình kiểm tra lịch học chính xác vào ngày thứ Hai 03/05/2027…" | Không bác bỏ thông tin sai: khoá đã bắt đầu từ thứ Năm 15/04 (D6, D7). Code đọc "thứ 2" thành 03/05 nên model đi hỏi lớp |
| B03 | "Sáng thứ Tư 28/04 lớp L3 học gì, ở đâu?" | "…LEC 11, hình thức học online." · Nguồn D28 | Thiếu giờ 09:00 mà tiêu chí bắt buộc |
| B01 | "Chiều thứ Năm 29/04 lớp L3A học LEC 13 ở phòng nào?" | "…diễn ra tại các phòng: E403, H210, H203 và H208." · Nguồn D31, E31 | Gộp phòng thêm H203, H208 chung với phòng chính E403, H210, ô D31 tách riêng hai loại |

## 3. Một lần cải tiến

- **Nhắm vào nhóm lỗi:** câu hỏi chung chung (B21, B25, B26).
- **Vì sao đây là nhóm đau nhất với người dùng:**
  - Đây đúng là kiểu câu học viên gõ thật trên Discord: cả 3 câu là `data_that`.
  - Trợ lý trả lời sai cách khiến học viên tin sai hoặc phải chờ TA cho câu tự trả lời được. B25 nói "chưa có thời khoá biểu" trong khi lịch đã có. B26 không sửa lại giả định sai "thứ 2 mới bắt đầu học". B21 đẩy sang TA thay vì hỏi lại.
  - Đây đúng là pain "không chắc thông tin là bản mới nhất" (7/18 người, `evidence/summary.md`), và TA bị hỏi lặp lại.
  - Nhóm này cũng làm lượt 1 trượt điều kiện cứng của chuẩn "đạt".
- **Đã sửa gì** (commit `a9dd63e`, changelog `spec.md` §10):
  1. `tong_quan_khoa`: thêm mục `co_trong_du_lieu`. Sửa mục `khong_co_trong_du_lieu`: bản cũ ghi "link tài liệu / thời khoá biểu" nên model hiểu là không có thời khoá biểu; bản mới chỉ nói link (URL).
  2. Prompt: câu hỏi chung chung trong phạm vi thì hỏi lại lớp / ngày / buổi, không chuyển TA. Câu chứa giả định sai về lịch thì kiểm bằng tổng quan khoá rồi sửa.
  3. Code không đọc "thứ X" thành một ngày khi câu hỏi về "bắt đầu học / khai giảng".
  4. Chặn hồi quy: chạy thử sau thay đổi (2) thì B08, B09, B14 (phòng chưa chốt) bị trả lời / hỏi lại thay vì chuyển TA. Thêm luật trong code: hỏi phòng của một lớp mà buổi chưa chốt thì luôn chuyển TA.
- **Kết quả:** nhóm lỗi đó 0/3 → **3/3**. Tổng 80% → **93%** (24/30 → 28/30).
  - Ngoài nhóm nhắm tới, B03 cũng chuyển sang đạt (lượt 2 có nêu 09:00). Không sửa gì cho câu này, nhiều khả năng là do model trả lời khác nhau giữa các lượt.
- **Câu nào tệ đi sau khi sửa:** không câu nào đạt ở lượt 1 mà trượt ở lượt 2.
  - B08, B09, B14 có tệ đi khi *chạy thử* trước lượt 2 (xem sửa số 4), nhưng ở lượt 2 vẫn đạt.

## 4. Còn lại

- **Lỗi chưa sửa:**
  - **B01:** gộp phòng thêm H203, H208 chung với phòng chính. Học viên có thể đi tới phòng thêm và tưởng lớp học chính ở đó. Mức nguy hiểm: vừa, vì cùng buổi, cùng toà H.
  - **B27:** thiếu tên session "LEC 11". Thông tin vẫn đúng, nguy hiểm thấp.
  - Nhóm "thiếu / gộp chi tiết" chưa được sửa, vì lần cải tiến chỉ nhắm một nhóm.
  - **B30:** đạt, nhưng bằng câu chuyển TA mặc định (code chặn câu trả lời của model), không giải thích được gì cho học viên.
  - Câu trả lời thay đổi giữa các lượt (B03 lượt 1 thiếu giờ, lượt 2 có). Một lượt 30 câu chưa đủ để chắc tỉ lệ đạt.
- **Nếu có thêm 1 tuần:**
  - Code tự ghép phần phòng / giờ / session vào câu trả lời từ dữ liệu, thay vì để model diễn đạt. Việc này chặn được cả nhóm B01, B03, B27.
  - Chạy mỗi cấu hình 3 lần để đo độ dao động.
  - Viết code chấm metric `trich_nguon`.
  - Thêm câu thử từ học viên L3B và câu nhiều lượt (người dùng sửa lại câu hỏi).
