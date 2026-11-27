# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Thông báo + lịch học mẫu (`data/announcements.json`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `search_announcements`, `get_schedule` (`codebase/tools.py`) · căn cứ để viết câu thử |
| Từ đâu | nhóm tự viết (Lục Anh Tuấn), dựng theo dạng thông báo thường gặp trên Discord / LMS của khoá. Mốc hackathon (TB-08) chép từ README / guide của repo đề. Không chép thông báo thật nào |
| Xử lý những bước gì | không lọc / ẩn danh (không có dữ liệu cá nhân). Trạng thái từng thông báo (`hien_hanh`, `da_bi_thay`, `mau_thuan`, `chua_chot`, `khong_chinh_thuc`) do `codebase/tools.py` tính lúc chạy, không ghi tay |
| Số dòng / số đoạn | 17 thông báo (15 chính thức, trong đó 2 đã bị thay: TB-02, TB-10 · 2 tin học viên: TB-04, TB-14) · 6 buổi học (26–28/11/2026) |
| Phiên bản / ngày lấy | bản 1 · 27/11/2026 · "hôm nay" của dữ liệu = `as_of` 2026-11-27 (đổi bằng `APP_TODAY`) |
| Nhãn | `synthetic` |
| Giới hạn | Nhỏ, sạch hơn thật. Mỗi kiểu khó chỉ có 1–2 ví dụ: gia hạn (lab 12), tin đồn (lab 13, phòng L3A 28/11), mâu thuẫn Discord vs LMS (lab 14), phòng chưa chốt (L3A 28/11), đổi phòng (L3B 27/11), chưa có thông báo phòng (chiều 28/11). Thông báo thật dài, lẫn nhiều việc trong một tin, có ảnh → khó tra hơn. Link là `.example` giả |

**Data `synthetic` (nhóm tự sinh):** viết tay, không dùng seed. Kịch bản khó chọn để khớp các lớp ở `spec.md` §5. Người kiểm: __ (cần một người ngoài người viết đối chiếu 17 dòng). Data tự dựng **không phải bằng chứng pain**.

## Dataset 2 · [tên]

…
