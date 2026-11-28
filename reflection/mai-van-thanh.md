# Reflection — Mai Văn Thanh

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
   - Đội trưởng: tạo repo từ starter, điền `TEAMS.md`, `canvas.md` (commit `7ed24d3`, `2a67c48`), nộp các checkpoint.
   - Bằng chứng pain: viết giả thuyết trước khi tìm bằng chứng (`evidence/hypothesis.md`, `43a8ced`); soạn bộ câu khảo sát và script đếm (`evidence/survey/questions.md`, `evidence/count.py`, `10f1738`).
   - Thu 20 phiếu khảo sát (18 học viên), tổng hợp ở `evidence/summary.md`, `stats.py` tính lại được (`43c437b`). Đếm kênh hỏi-đáp Discord: 2/18 bài hỏi hạn / phòng / lịch (`evidence/data-mining.md`).
   - Chép 13 tin học viên hỏi trên Discord, chọn 10 làm câu thử `data_that` B21–B30, viết dataset 2 trong `data/DATA_CARD.md` (`43c437b`).
   - Trước CP3: thu hẹp lát cắt sang "phòng / giờ học; hạn nộp → chuyển TA" cho khớp data, ghi changelog `spec.md` §10 (`29f922e`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   - Dùng Claude Code phân loại kiểu câu hỏi của 18 bài kênh hỏi-đáp từ ảnh chụp danh sách bài. Mình đếm tay cả 18 bài trước, AI ra cùng 2/18 bài, khớp với số đếm tay.
   - Dùng Claude Code tính bảng impact `spec.md` §2 và nhóm tần suất từ `evidence/survey/results.csv` qua `stats.py`. Mình đọc lại phần AI sửa spec trước CP3 rồi mới commit.
   - Chỗ phải giữ quyết định của người: cách quy ô chữ tự do ở câu 3 ra số lần / tuần ("Rất nhiều lần." xếp vào nhóm ≥2), và việc giữ lại 2 phiếu mâu thuẫn (S17, S19) trong n thay vì bỏ cho số đẹp.
   - Không dùng AI để tạo phiếu khảo sát, trích dẫn hay tin Discord: tất cả là câu trả lời thật, chỉ bỏ tên.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   - B25 "anh chị ơi có thời khóa biểu chưa ạ" là một trong 10 câu mình chép nguyên văn từ Discord. Ở lượt 1, trợ lý trả lời "thông tin về thời khóa biểu chi tiết chưa có", trong khi lịch chính thức có sẵn. Học viên đọc câu đó sẽ tưởng chưa có lịch.
   - Nguyên nhân là một dòng mô tả dữ liệu ghi "không có link tài liệu / thời khoá biểu", nên model hiểu là không có thời khoá biểu. Lỗi không nằm ở model mà ở cách nhóm mô tả nguồn.
   - Cả 3 câu trượt nhóm "câu hỏi chung chung" (B21, B25, B26) đều là câu `data_that`. Câu nhóm tự viết thường đủ ngày / lớp / buổi nên dễ qua; câu học viên gõ thật thì cụt và thiếu thông tin.
   - Bài học: câu thử từ người dùng thật mới lộ lỗi thật. Lần sau mình sẽ lấy câu thật sớm hơn và nhiều hơn (hiện mới 10/30), thêm câu của học viên L3B và câu nhiều lượt.
