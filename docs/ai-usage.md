# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/tools.py`, `agent.py`, phần gọi API trong `ai.py`; bản sau viết lại `tools.py`, `agent.py` theo data `data/lich-l3-k9.csv` | __ (Tuấn ghi phần đã đọc / sửa / chạy thử) | Lục Anh Tuấn |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Viết bản đầu `SYSTEM` trong `agent.py` (4 quyết định, JSON) | __ | Lục Anh Tuấn |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code | Chấm `eval/run-1.csv`, `eval/run-2.csv` (30 câu mỗi lượt) theo `pass_criterion` + `eval/metric_spec.yaml`, ghi lý do từng câu ở cột `ghi_chu` | Kiểm tra thủ công __ câu thử, khớp __/__ (cần người chấm thứ hai, ưu tiên ca ranh giới B01, B18) | Lục Anh Tuấn nhờ chấm; Lê Quang Trường kiểm |
| Slide, văn bản | Claude Code | Soạn nháp `spec.md` (§0, §3–§6, §9) từ `canvas.md`; điền `cost/personas.yaml` (giá theo bảng chung BTC `further-reading/model-prices.md`; đếm số buổi LAB / buổi bị sửa phòng từ `data/` làm tần suất persona) và mục 1 `cost/cost-estimate.md`; nháp nội dung `slides/outline.md` | Nhóm đọc lại spec; Nam kiểm giá với bảng BTC, kiểm lại phép đếm trong data, thay share persona bằng số khảo sát khi có | Nguyễn Lê Hải Nam |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
