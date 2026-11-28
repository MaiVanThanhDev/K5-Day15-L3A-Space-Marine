# Tóm tắt mô phỏng simulate-1@20261127-233703

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 9 | 1 | 3278 | 110 | 1.0 | 2.3 |
| hoi_vua | 17 | 1 | 3330 | 112 | 1.0 | 2.5 |
| hoi_nhieu | 24 | 1 | 3167 | 110 | 1.0 | 2.5 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-2@20261127-190717

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00098 | $0.0010 | $0.0010 | $6.94 | $16.20 | $23.15 | $0.0231 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0057 | $0.0061 | $0.0061 | $40.48 | $94.46 | $134.94 | $0.1349 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
