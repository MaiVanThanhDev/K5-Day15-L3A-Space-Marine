# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu — `hoi_it` 50% · 4 phiên / tháng · 1 lượt; `hoi_khi_doi_phong` 35% · 13 phiên · 1 lượt; `hoi_truoc_moi_lab` 15% · 17 phiên · 2 lượt. Nguồn: số phiên của 2 kiểu sau đếm từ data lịch BTC (giả lập Khoá 9, 24 ngày quy ra 30 ngày): 10–11 buổi / lớp bị sửa phòng (`data/lich-su-sua-l3-k9.csv`), 14 buổi LAB / lớp (`data/lich-l3-k9.csv`); share, số lượt / phiên và kiểu `hoi_it` *(tự ước tính)* — chờ thay bằng khảo sát (`evidence/survey/`)
- **Số người dùng thật** 3 kịch bản: thấp 300 · cơ sở 700 · cao 1000. Nguồn: cơ sở = lớp L3 hơn 700 học viên, cao = cả khoá hơn 1.000 (repo đề `02-guide.md` mục 4.2); thấp = ~40% học viên L3 dùng *(tự ước tính)*
- **Giá** ≥2 mức model (USD / 1 triệu token, bảng chung BTC `further-reading/model-prices.md`, BTC xem trang giá Google 25/11/2026): `gemini-3.1-flash-lite` vào 0.25 / ra 1.50 (tầng Nhỏ) · `gemini-4-hydrogen` vào 1.50 / ra 7.50 (tầng Lớn)
- **Tỉ lệ đạt** dùng để tính: 28/30 (93%) — lượt `run-2@20261127-190717` (lượt 2, `--rate-from eval/run-2.csv`)
- Đo token trên model `nvidia/nemotron-3-ultra-550b-a55b:free` (qua OpenRouter, gói miễn phí), tính giá model `gemini-3.1-flash-lite` và `gemini-4-hydrogen`. **Khác model:** lượt eval chạy bằng `gemini-3.1-flash-lite`; tài khoản OpenRouter chưa có credit nên không gọi được model đó, phải đo token bằng model miễn phí

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-105759` · 50 phiên (44 chạy xong, 6 lỗi bị loại khỏi trung bình) · seed 42 · lệnh `python run.py simulate --wait 4 --rate-from eval/run-2.csv`

Bảng chép từ `cost/simulate-1-summary.md`:

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 21 | 1 | 3126 | 529 | 1.0 | 2.4 |
| hoi_khi_doi_phong | 18 | 1 | 3342 | 612 | 1.0 | 2.3 |
| hoi_truoc_moi_lab | 5 | 2 | 6111 | 912 | 2.0 | 4.4 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0018 | $0.0019 | $0.0017 | $5.55 | $12.96 | $18.51 | $0.0185 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0099 | $0.0106 | $0.0095 | $30.54 | $71.26 | $101.81 | $0.1018 |

- **6 phiên lỗi** (S045–S050): `HTTP 429 Rate limit exceeded: free-models-per-day` — hết hạn mức lượt gọi / ngày của gói miễn phí OpenRouter, không phải lỗi của trợ lý.
- **Token ra bị đẩy cao:** model đo là model suy luận, token suy luận được cộng vào token ra (đúng hợp đồng `ai.py`): ~530–910 token ra / phiên, trong khi lượt 2 trên `gemini-3.1-flash-lite` chỉ ~114 token ra / câu (`eval/report.md` mục 1). Token vào gần như khớp (~3.100–3.300 / câu so với ~3.250). Vì vậy số ở dòng `gemini-3.1-flash-lite` nhiều khả năng là **cận trên**.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈131 phút học viên / tháng (trần, không phải số tiết kiệm được), cộng giảm rủi ro nhầm (7/18 từng nhầm)
- Chi phí / người / tháng (cơ sở 700 người): **$0.0185** (`gemini-3.1-flash-lite`) · $0.1018 (`gemini-4-hydrogen`); cả khoá ở quy mô cơ sở ≈ $13 / tháng với model nhỏ
- **Kết luận một dòng — đáng làm không:** đáng làm về chi phí — chi phí model không đáng kể so với impact (dưới 2 cent / học viên / tháng với model nhỏ, kể cả khi token ra bị đẩy cao); chi phí thật nằm ở giờ công TA duyệt bản nháp chuyển TA (chưa đo)

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
