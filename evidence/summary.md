# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data: đếm tay kênh hỏi-đáp Discord của khoá | ☐ (n = 18 bài, quá nhỏ; dùng để đối chiếu) | `evidence/data-mining.md` |
| Phỏng vấn | ☐ (không làm, xem mục 5) | — |
| Khảo sát (≥20 người, đúng người dùng) | ☑ 20 phiếu, 18 học viên | `evidence/survey/questions.md` · `results.csv` · `stats.py` |

**Nguồn chính đổi từ đếm Discord sang khảo sát** (giả thuyết ghi nguồn chính là Discord): kênh hỏi-đáp chỉ có 18 bài, không đủ làm mẫu số. Khảo sát cũng cho thấy chỉ 3/18 học viên hỏi trên kênh hỏi-đáp (câu 5), nên kênh này không phản ánh hết việc tra cứu.

## 2. Số chính

- **Đào data (Discord, kênh hỏi-đáp):** 2/18 bài hỏi về hạn nộp / phòng / lịch *(n nhỏ, chỉ ghi x/n)*.
- **Khảo sát:** 20 phiếu ngày 27/11/2026 (17:02–18:10). n = **18 học viên**; 1 lab coach và 1 "người lạ" tách riêng, không cộng chung. Chạy lại: `python evidence/survey/stats.py`.

| Đếm gì (n = 18 học viên) | x / n | Câu |
|---|---|---|
| Đã tra hạn / phòng / lịch **≥2 lần trong 1 tuần qua** | **16/18 (89%)** · trung vị 5 lần / tuần | 3 |
| Lần gần nhất là **hôm nay** | 12/18 (67%) | 2 |
| Tìm gì: giờ học / lịch buổi · hạn nộp · phòng học · online hay offline | 13/18 (72%) · 12/18 (67%) · 11/18 (61%) · 4/18 (22%) | 4 |
| Tìm bằng email / LMS · lục kênh thông báo Discord | 13/18 (72%) · 9/18 (50%) | 5 |
| **Phải hỏi người khác** (nhắn bạn / kênh hỏi đáp / TA) | 8/18 (44%) · riêng kênh hỏi đáp: 3/18 (17%) | 5 |
| Tự đoán | 2/18 (11%) | 5 |
| Mất **≥5 phút** đến khi chắc chắn | 5/18 (28%) · dưới 2 phút: 9/18 (50%) | 6 |
| Tìm được nhưng **không chắc là bản mới nhất** | **7/18 (39%)** | 7 |
| **Từng nhầm** hạn / phòng / giờ trong khoá | **7/18 (39%)**: nhầm hạn nộp 6/18 (33%), nhầm phòng 1/18 (6%) | 8 |

Cách quy câu 3 (ô chữ tự do) ra số lần / tuần ghi ở `stats.py` (vd "1-2 lần/ngày" → 7, "Rất nhiều lần." → xếp nhóm ≥2).

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Thông tin giữ các LabCoach chưa được đồng nhất, nên dù có thông tin về thời gian nộp bài lab nhưng k biêt là đúng hay sai" — phiếu khảo sát S19
2. "Mình tới trường vào buổi sáng nhưng lại quên lớp học, mình mở lại link html chứa TKB trên điện thoại thì bị báo expired. Mình phải mở lại trong Outlook rồi mở file .html rồi chọn "Tiếp tục trên trình duyệt" mới xem được kết quả" — phiếu khảo sát S04
3. "Tìm hạn nộp lab code khó, làm mình khó lẻn kế hoạch làm việc phù hợp" — phiếu khảo sát S10
4. "Học tòa D những không biết tòa D ở đâu" — phiếu khảo sát S12
5. "mỗi lần tìm mất công mở lms để xem tkb" — phiếu khảo sát S14
6. "Dạ anh/chị cho em hỏi, trong yêu cầu của bài LAB03 có thông tin ở mục Checkpoint 4h là 17:30 - Improve v3 + hoàn thiện report Phần B thì bài LAB03 deadline đến 17:30 là chốt luôn hay được kéo dài đến 23:59 như mấy bài trước ạ" — Discord của khoá, 14:51 10/11/2026
7. "Phòng E402 chuyển qua phòng nào vậy ạ" — Discord của khoá, 14:15 21/11/2026

Phản ví dụ (giữ lại): "Không có gì khó chịu lắm" — S11. 9/18 học viên tìm được trong dưới 2 phút.

## 4. Các nguồn có khớp nhau không

Discord: kênh hỏi-đáp chỉ có 18 bài, 2 bài về hạn / phòng / lịch. Người dùng (khảo sát): 16/18 tra ≥2 lần / tuần, nhưng chỉ 3/18 hỏi trên kênh hỏi-đáp; phần lớn tự tra email / LMS (13/18) hoặc nhắn riêng bạn (8/18).
→ **Khớp:** cả hai cho thấy kênh hỏi-đáp không phải nơi chính học viên tìm thông tin này. **Lệch:** giả thuyết cho rằng câu hỏi lặp lại dồn về kênh hỏi đáp để TA trả lời; thực tế việc tra cứu diễn ra riêng lẻ (email, LMS, nhắn bạn) nên TA ít thấy, và đếm kênh hỏi-đáp đánh giá thấp pain.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng một phần, phải đổi**.
- Ngưỡng khảo sát **đạt**: tra ≥2 lần / tuần 16/18 (89%, ngưỡng ≥50%); từng nhầm 7/18 (39%, ngưỡng ≥20%).
- Ngưỡng Discord **không kiểm được**: n = 18 bài quá nhỏ.
- **Phải đổi:** pain chính không phải *thời gian tra* (50% tìm được trong dưới 2 phút) mà là **không chắc thông tin là bản mới nhất** (7/18) và **nhầm hạn nộp** (6/18). Nhầm phòng chỉ 1/18. Lát cắt hiện tại (phòng / lịch) khớp với việc tra thường xuyên nhất (lịch 13/18, phòng 11/18), nhưng **hạn nộp là chỗ người dùng nhầm nhiều nhất**, mà data lịch không có hạn nộp. Nhóm cần ghi giới hạn này ở spec §2 / §4.

Điều vẫn chưa biết:
- Người trả lời có đúng là ngoài nhóm và lớp nào (L3A / L3B): form không hỏi.
- Phía TA: TA mất bao nhiêu phút / tuần trả lời câu lặp lại (không phỏng vấn TA).
- 2 phiếu có câu trả lời mâu thuẫn (S17: câu 2 "Hôm nay" nhưng câu 3 "không"; S19: câu 2 "Chưa bao giờ" nhưng câu 3 "4"), vẫn giữ trong n.
- Tất cả phiếu thu trong khoảng 1 giờ chiều 27/11, có thể lệch về những người online lúc đó.

**Không phỏng vấn TA:** nhóm quyết định không làm nguồn này; khảo sát đủ ngưỡng làm nguồn chính.
