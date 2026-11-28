# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code | Viết `codebase/tools.py`, `agent.py`, phần gọi API trong `ai.py`; bản sau viết lại `tools.py`, `agent.py` theo data `data/lich-l3-k9.csv` | Chạy `python run.py eval` 2 lượt bằng model thật (run-1 24/30, run-2 28/30); sau lượt 1 đọc nhóm lỗi rồi sửa `agent.py`, `tools.py` (commit `a9dd63e`). Phần tự đọc / sửa tay: __ (Tuấn ghi) | Lục Anh Tuấn |
| Prompt / thiết kế lời gọi mô hình | Claude Code | Viết bản đầu `SYSTEM` trong `agent.py` (4 quyết định, JSON) | Kiểm qua 30 câu thử ở 2 lượt; sau lượt 1 sửa luật hỏi lại / chuyển TA trong `SYSTEM` (commit `a9dd63e`). Phần tự sửa tay: __ (Tuấn ghi) | Lục Anh Tuấn |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Phân loại kiểu câu hỏi của 18 bài kênh hỏi-đáp từ ảnh chụp danh sách bài (`evidence/data-mining.md` mục 2); tính bảng impact `spec.md` §2 và nhóm tần suất từ `evidence/survey/results.csv` qua `stats.py` | Đếm tay cả 18 bài trên Discord trước (2/18 hỏi hạn / phòng / lịch); bảng phân loại của AI ra cùng 2/18 bài hạn nộp → khớp. Kiểm lại phép tính impact: __ | Mai Văn Thanh |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | Không dùng | Nhóm không sinh data; lịch là data giả lập do BTC cấp (`data/training-ops/`, xem `data/DATA_CARD.md`) | — | — |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code | Chấm `eval/run-1.csv`, `eval/run-2.csv` (30 câu mỗi lượt) theo `pass_criterion` + `eval/metric_spec.yaml`, ghi lý do từng câu ở cột `ghi_chu` | Người thứ hai (Nguyễn Lê Hải Nam) chấm độc lập 5 câu lượt 2 (B01, B08, B18, B26, B30), khớp 5/5 với cột `pass` (`eval/README.md` mục 3) | Lục Anh Tuấn nhờ chấm; Lê Quang Trường kiểm |
| Slide, văn bản | Claude Code | Soạn nháp `spec.md` (§0, §3–§6, §9) từ `canvas.md`; điền `cost/personas.yaml` (giá theo bảng chung BTC `further-reading/model-prices.md`; đếm số buổi LAB / buổi bị sửa phòng từ `data/` làm tần suất persona) và mục 1 `cost/cost-estimate.md`; nháp nội dung `slides/outline.md`; trước CP3 (27/11): điền `spec.md` §2 (bảng impact), §4 "Không làm", ví dụ §6 lấy từ output thật B07, sửa các câu về hạn nộp cho khớp code; mục "Dùng AI vào việc gì" trong README; `eval/README.md` mục 1; bản dự phòng CP4 (nhánh `cp4-backup`): đổi persona `cost/personas.yaml` theo khảo sát, chạy `python run.py simulate` (50 phiên, model thật), điền `cost/cost-estimate.md` và `spec.md` §8, dựng `slides/demo-slides.html` → `demo-slides.pdf` (mọi số trỏ về file trong repo) | Nhóm đọc lại spec; Nam kiểm giá với bảng BTC, kiểm lại phép đếm trong data, thay share persona bằng số khảo sát khi có; Thanh đọc lại phần sửa trước CP3 trước khi commit | Nguyễn Lê Hải Nam |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
