# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu — `hoi_it` 50% · 4 phiên / tháng · 1 lượt; `hoi_khi_doi_phong` 35% · 13 phiên · 1 lượt; `hoi_truoc_moi_lab` 15% · 17 phiên · 2 lượt. Nguồn: số phiên của 2 kiểu sau đếm từ data lịch BTC (giả lập Khoá 9, 24 ngày quy ra 30 ngày): 10–11 buổi / lớp bị sửa phòng (`data/lich-su-sua-l3-k9.csv`), 14 buổi LAB / lớp (`data/lich-l3-k9.csv`); share, số lượt / phiên và kiểu `hoi_it` *(tự ước tính)* — chờ thay bằng khảo sát (`evidence/survey/`)
- **Số người dùng thật** 3 kịch bản: thấp 300 · cơ sở 700 · cao 1000. Nguồn: cơ sở = lớp L3 hơn 700 học viên, cao = cả khoá hơn 1.000 (repo đề `02-guide.md` mục 4.2); thấp = ~40% học viên L3 dùng *(tự ước tính)*
- **Giá** ≥2 mức model (USD / 1 triệu token, bảng chung BTC `further-reading/model-prices.md`, BTC xem trang giá Google 25/11/2026): `gemini-3.1-flash-lite` vào 0.25 / ra 1.50 (tầng Nhỏ) · `gemini-4-hydrogen` vào 1.50 / ra 7.50 (tầng Lớn)
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` (lượt 2)
- Đo token trên model __, tính giá model __ và __

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
