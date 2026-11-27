# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu — `hoi_it` 50% · 2 phiên / tháng · 1 lượt; `hoi_moi_tuan` 35% · 4 phiên · 2 lượt; `hoi_truoc_moi_buoi` 15% · 8 phiên · 3 lượt. Nguồn: *(tự ước tính)* — chờ thay bằng số khảo sát (`evidence/survey/`) và đếm tin Discord (`evidence/data-mining.md`)
- **Số người dùng thật** 3 kịch bản: thấp 300 · cơ sở 700 · cao 1000. Nguồn: cơ sở = lớp L3 hơn 700 học viên theo README hackathon (repo đề, cần đối chiếu lại); thấp, cao *(tự ước tính)*
- **Giá** ≥2 mức model (USD / 1 triệu token, gói Standard, [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), xem 27/11/2026): `gemini-3.1-flash-lite` vào 0.25 / ra 1.50 (rẻ) · `gemini-3.6-flash` vào 1.50 / ra 7.50 (mạnh — giá gốc từ 01/01/2027; đến 31/12/2026 đang khuyến mãi 0.75 / 3.75)
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
