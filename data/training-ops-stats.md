# Quy trình lịch / phòng hiện tại — số đếm từ `data/training-ops` *(GIẢ LẬP)*

> **Không phải bằng chứng pain.** BTC ghi rõ đây là data dựng lại cách khoá vận hành lịch: người, email, ngày đều giả, chỉ mã phòng và chủ đề giữ theo khoá thật.
> Dùng để mô tả "hiện tại việc này diễn ra thế nào" (spec.md §0), chọn tình huống khó cho bộ câu thử, và làm nguồn cho bản chạy thử.
> Chạy lại: `python data/count_training_ops.py _de-bai/data/training-ops` (cần `openpyxl`). Repo chỉ giữ số tổng hợp, không chép file gốc.

## 1. Bảng lịch Khoá 9 lúc xuất (21:00 27/04/2027), chỉ lớp L3

| Đếm gì | x / N |
|---|---|
| Buổi L3 trong bảng | 56 (LEC 28, LAB 28) |
| Buổi còn **"chờ xác nhận"** phòng lúc xuất | 8/56 (14%) |
| Buổi LEC có "Phòng thêm" ngoài H209/H210 | 16/28 (57%) |
| Buổi LAB rải ≥2 phòng | 25/28 (89%) |
| Buổi online | 4/56 (7%) |

## 2. Lịch sử chỉnh sửa bảng lịch (44 lần sửa, 27 lần của lớp L3)

| Loại sửa | x / 44 |
|---|---|
| Chốt phòng ("chờ xác nhận" → phòng cụ thể) | 38 (86%) |
| Đổi phòng **đã chốt** | 2 (5%) |
| Đổi giảng viên | 2 (5%) |
| Thêm phòng | 1 (2%) |
| Đổi giờ | 1 (2%) |

Thời điểm chốt phòng so với giờ bắt đầu buổi (sáng 09:00, chiều 14:00), tính trên 38 lần chốt:
- Trung vị **40 giờ** trước buổi.
- Chốt dưới 24 giờ trước buổi: **15/38 (39%)**. Dưới 12 giờ: 6/38 (16%).
- Chốt **sau khi buổi đã bắt đầu**: 3/38 (8%).

Phòng đã chốt rồi vẫn đổi (thông báo cũ bị thay):
- 22/04 sáng · L3A LAB 5: C204, C301, C305, H104 → C104, C203, E402, E403 (khoảng 40 giờ trước buổi)
- 28/04 chiều · L3B LAB 10: đổi cả 6 phòng (khoảng 40 giờ trước buổi)

## 3. Bảng lab coach

- Lịch lab đợt 2: **20/35 (57%)** ô phòng còn "chờ xác nhận" hoặc "dk:" (dự kiến) lúc cập nhật lần cuối.
- 22 yêu cầu đổi buổi của lab coach qua form.

## Dùng vào đâu

- **spec.md §0** (luồng hiện tại): phòng đi từ "Phòng dự kiến … (chờ xác nhận)" sang "Phòng: …" trong một bảng tính chung, chủ yếu do Support và Ban đào tạo sửa tay. Phòng chốt sát ngày và đôi khi đổi sau khi đã chốt.
- **Bộ câu thử (eval/)**: các tình huống phòng chưa xác nhận, phòng đổi sau khi chốt, buổi đổi giờ (L3B LAB 8: 14:00 → 16:30), buổi online.
- **Không** đưa vào `evidence/summary.md` như số pain. Muốn có số thật về việc học viên bị ảnh hưởng thì phải đếm Discord hoặc làm khảo sát.
