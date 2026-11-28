# Tóm tắt mô phỏng simulate-1@20261128-105759

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 21 | 1 | 3126 | 529 | 1.0 | 2.4 |
| hoi_khi_doi_phong | 18 | 1 | 3342 | 612 | 1.0 | 2.3 |
| hoi_truoc_moi_lab | 5 | 2 | 6111 | 912 | 2.0 | 4.4 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-2@20261127-190717

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from). ⚠️ Lượt này chạy bằng gemini-3.1-flash-lite, mô phỏng đo trên nvidia/nemotron-3-ultra-550b-a55b:free — khác model.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0018 | $0.0019 | $0.0017 | $5.55 | $12.96 | $18.51 | $0.0185 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0099 | $0.0106 | $0.0095 | $30.54 | $71.26 | $101.81 | $0.1018 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.1) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: nvidia/nemotron-3-ultra-550b-a55b:free. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 6/50.
