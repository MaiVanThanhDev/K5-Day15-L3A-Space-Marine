# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, tần suất và tỉ lệ lấy từ khảo sát 27/11/2026 (n = 18 học viên, câu 3 "1 tuần qua tra mấy lần", chia nhóm như `spec.md` §2):

  | Persona | Tỉ lệ | Phiên / tháng | Lượt / phiên | Nguồn |
  |---|---:|---:|---:|---|
  | `hoi_it` (0–2 lần / tuần) | 11% | 2 | 1 | share: 2/18; số phiên *(tự ước tính)* vì cả 2 trả lời 0 lần tuần qua |
  | `hoi_vua` (3–6 lần / tuần) | 44,5% | 19 | 1 | 8/18, trung vị 4,5 lần / tuần × 30/7 |
  | `hoi_nhieu` (≥7 lần / tuần) | 44,5% | 34 | 1 | 8/18, trung vị 8 lần / tuần × 30/7 |

  Trung bình ≈ 23,8 phiên / người / tháng, khớp với 21,4 lần ở bảng impact (`spec.md` §2). Lượt / phiên = 1 *(tự ước tính)*. Câu 3 đếm cả lần tra hạn nộp; trợ lý vẫn tốn 1 lần gọi model để chuyển TA nên vẫn tính.
- **Số người dùng thật** 3 kịch bản: thấp 300 · cơ sở 700 · cao 1000. Nguồn: cơ sở = lớp L3 hơn 700 học viên, cao = cả khoá hơn 1.000 (repo đề `02-guide.md` mục 4.2); thấp = ~40% học viên L3 dùng *(tự ước tính)*
- **Giá** ≥2 mức model (USD / 1 triệu token, bảng chung BTC `further-reading/model-prices.md`, BTC xem trang giá Google 25/11/2026): `gemini-3.1-flash-lite` vào 0.25 / ra 1.50 (tầng Nhỏ) · `gemini-4-hydrogen` vào 1.50 / ra 7.50 (tầng Lớn)
- **Tỉ lệ đạt** dùng để tính: 28/30 (93%) — lượt `run-2@20261127-190717` (lượt 2), truyền bằng `--rate-from eval/run-2.csv`
- Đo token trên model `gemini-3.1-flash-lite`, tính giá model `gemini-3.1-flash-lite` và `gemini-4-hydrogen` (cùng số token; model lớn khác bộ tách token thì số thật có thể lệch)

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261127-233703` · 50 phiên (0 phiên lỗi) · seed 42 · tóm tắt `cost/simulate-1-summary.md` · trace `traces/simulate-1.jsonl`

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 9 | 1 | 3278 | 110 | 1.0 | 2.3 |
| hoi_vua | 17 | 1 | 3330 | 112 | 1.0 | 2.5 |
| hoi_nhieu | 24 | 1 | 3167 | 110 | 1.0 | 2.5 |

Thời gian trả lời / phiên: trung bình 6,5 giây · trung vị 2,0 giây · chậm nhất 57,9 giây (đo trong `cost/simulate-1.csv`, cột `latency_s`).

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (300) | / tháng — cơ sở (700) | / tháng — cao (1.000) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| `gemini-3.1-flash-lite` | $0.00098 | **$0.0010** | $6.94 | **$16.20** | $23.15 | $0.0231 |
| `gemini-4-hydrogen` | $0.0057 | $0.0061 | $40.48 | $94.46 | $134.94 | $0.1349 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈ 131 phút tra cứu / học viên / tháng (**trần**; 622 người × 21,4 lần × 6,1 phút ÷ 622). Giá trị chính là giảm nhầm: 7/18 học viên từng nhầm hạn / phòng / giờ.
- Chi phí / người / tháng (cơ sở, model `gemini-3.1-flash-lite`): **$0.0231** (≈ $16,20 / tháng cho 700 học viên); model lớn `gemini-4-hydrogen`: $0.1349.
- **Kết luận một dòng — đáng làm không:** **Đáng thử** — tiền model gần như không đáng kể (dưới 3 cent / học viên / tháng ở model nhỏ, kể cả model lớn vẫn dưới 15 cent), nên chi phí thật nằm ở giờ TA duyệt bản nháp chuyển TA (mục 4), không phải ở model; dùng model nhỏ vì lượt 2 đã đạt chuẩn với nó.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- **Chi phí ngoài model — giờ TA duyệt bản nháp:** mỗi tháng ở kịch bản cơ sở ≈ 700 × 23,8 ≈ 16.700 phiên. Trong bộ câu thử lượt 2, 11/30 câu kết thúc bằng bản nháp chuyển TA (B08, B09, B10, B13, B14, B20, B22, B23, B24, B28, B30). Bộ câu thử lệch về ca khó (21/30 câu `kho`), nên 37% là **trần** *(tự ước tính, chưa đo tỉ lệ thật)*: nếu đúng 37% thì ≈ 6.100 bản nháp / tháng — quá nhiều để TA duyệt từng cái. Cần đo tỉ lệ chuyển TA trên câu hỏi thật trước khi pilot; đây là cần gạt chi phí lớn nhất.
- **Đổi model:** `gemini-3.1-flash-lite` → `gemini-4-hydrogen` nhân chi phí ≈ 5,8 lần (cơ sở $16,20 → $94,46 / tháng), chưa có số cho thấy model lớn tăng tỉ lệ đạt (chưa chạy eval với model lớn).
- **Cắt ngữ cảnh:** ≈ 97% token là token vào (≈ 3.240 vào / 111 ra mỗi phiên) — chủ yếu là căn cứ lịch và prompt. Cache prompt hoặc chỉ đưa các buổi khớp bộ lọc sẽ là cần gạt rẻ nhất nếu quy mô tăng.
- **Hosting:** chưa tính (chạy trên máy; bot Discord thật cần một máy chạy liên tục).
