# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Lịch lớp L3 Khoá 9 (`data/lich-l3-k9.csv`, `data/lich-su-sua-l3-k9.csv`)

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ tra lịch / phòng trong `codebase/tools.py` (tên công cụ: `tra_lich`, Lục Anh Tuấn viết) · căn cứ duy nhất cho cột `expected` của `eval/benchmark.csv` |
| Từ đâu | Data BTC cấp: `data/training-ops/` trong repo đề [VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon). Hai file, bốn sheet: `teaching-schedule.xlsx` → sheet `Khoá 9 (GĐ1)` (bảng chính, ô D1: bản xuất 27/04/2027 21:00) và `Lịch sử chỉnh sửa`; `lab-coach-schedule.xlsx` → sheet `Lịch lớp K9 (bản chép)` (ô D1: chép ngày 12/04) và `Lịch lab 2604-0805` (cột K–P) |
| Xử lý những bước gì | Script `data/extract_training_ops.py` (chạy lại ra cùng kết quả). **Lọc:** chỉ cột lớp L3 (D, E = LEC phòng H209 / H210; F = LAB), bỏ L2; trong bản chép chỉ giữ 27 ô khác bảng chính; trong Lịch lab chỉ giữ dòng L3, mỗi buổi một dòng; trong Lịch sử chỉnh sửa chỉ giữ dòng của buổi L3. **Tách ô nhiều dòng** thành cột: lớp, session, online, giờ riêng, chủ đề, phòng, trạng thái phòng (`da_chot` / `theo_tieu_de_cot` / `du_kien` / `cho_xac_nhan` / `online` / `khong_ap_dung`), phòng thêm, ghi chú (`không có lớp`, `NGHỈ LỄ`, `KHAI GIẢNG KHOÁ 9`). Cột LEC không có dòng `Phòng:` thì phòng = tiêu đề cột. Ô gộp ngày được điền tiếp xuống dòng dưới. **Bỏ:** tên giảng viên, lab coach, người sửa, email, các sheet không dùng (đăng ký, nhân sự, workload, đổi buổi…). Giữ địa chỉ ô gốc (cột `o`) để trích nguồn |
| Số dòng / số đoạn | `lich-l3-k9.csv`: 158 dòng (bang_chinh 112 · ban_chep 27 · lich_lab 19) · `lich-su-sua-l3-k9.csv`: 27 dòng |
| Phiên bản / ngày lấy | Repo đề tải ngày 27/11/2026 (bản `--depth 1` của nhánh mặc định). Mốc thời gian trong data: 21:00 27/04/2027 |
| Nhãn | `synthetic` (BTC giả lập: người, email, mã, ngày đều giả; mã phòng và chủ đề giữ theo khoá thật) |
| Giới hạn | Không có **hạn nộp bài** nào → câu hỏi hạn nộp không có nguồn. Không có link riêng cho từng buổi → trích nguồn bằng `file · sheet · ô`. Bảng Lịch lab và bản chép không ghi giờ cập nhật cụ thể → quy ước bảng chính là nguồn đúng khi đã chốt. Chỉ phủ 15/04–08/05/2027. Data giả lập **không phải bằng chứng pain** |

Quy ước khi các nguồn lệch nhau (dùng trong metric và bộ câu thử):
- Bảng chính **đã chốt** phòng → dùng bảng chính, bỏ qua nguồn phụ.
- Bảng chính **chưa chốt** (chờ xác nhận / dự kiến), dù nguồn phụ ghi gì → không khẳng định, chuyển TA.

Tái tạo: tải repo đề vào `_de-bai/` (đã có trong `.gitignore`), `python -m pip install -r requirements.txt`, rồi `python data/extract_training_ops.py`. File xlsx gốc **không** commit.

## Dataset 2 · Tin hỏi đáp trên Discord của khoá (bằng chứng + nguồn câu thử `data_that`)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/data-mining.md`, Mai Văn Thanh) · nguồn câu thử `data_that` |
| Từ đâu | Kênh Discord công khai của khoá |
| Xử lý những bước gì | lọc __ · ẩn danh __ (bỏ tên, mã học viên) |
| Số dòng / số đoạn | __ |
| Phiên bản / ngày lấy | __ |
| Nhãn | thật |
| Giới hạn | __ |
