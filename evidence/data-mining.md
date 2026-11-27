# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Không đào data thì xoá file này. Script / công thức đếm để trong repo (vd `evidence/count.py` hoặc ghi công thức Sheets ngay dưới), người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: tin nhắn kênh hỏi đáp __ *(tên kênh)* trên Discord công khai của khoá AI20K K5, xuất bằng DiscordChatExporter ra `evidence/raw-discord.json` (không commit), từ __ đến __.
- Đếm gì: tin là **câu hỏi** về **hạn nộp / phòng học / lịch học** · trên tập nào: tin của học viên · lọc gì: bỏ bot, bỏ tài khoản TA / BTC / lab coach (danh sách ở `evidence/raw-staff.txt`, không commit), bỏ tin rỗng / chỉ ảnh, chỉ giữ tin trong khoảng ngày trên.
- **Mẫu số là gì:** N = mọi tin của học viên trong kênh, trong khoảng ngày đã chọn (không phải tổng tin của kênh, không phải số câu hỏi).
  - x / N = tin hỏi hạn / phòng / lịch trên tổng tin học viên. x lấy theo từ khoá rồi **kiểm tay từng dòng** (cột `dung_chu_de`).
  - y / x = số câu hỏi trong x mà **thông báo chính thức đăng trước giờ hỏi đã có câu trả lời** (kiểm tay, cột `da_co_trong_thong_bao`). Mẫu số của y là x đã kiểm tay, không phải N.
- Script / công thức: `evidence/count.py`. Từ khoá ở đầu file. Chạy lại:
  ```
  python evidence/count.py evidence/raw-discord.json --staff evidence/raw-staff.txt --from YYYY-MM-DD --to YYYY-MM-DD
  # gán nhãn tay evidence/raw-labels.csv rồi chạy lại, thêm:
  #   --labels evidence/raw-labels.csv
  ```

## 2. Đọc trước, đếm sau

Đã đọc __ dòng đầu và từ điển cột. Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):
- __
- __

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| | | | |
| | | | |

Ghi dạng "x/N (y%)". "Nhiều bạn…" không phải số.

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1.
2.
3.
4.
5.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào: __
→ Kiểm lại bằng phỏng vấn / khảo sát nào: __
