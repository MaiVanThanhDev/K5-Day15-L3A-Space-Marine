"""Tính số chính từ evidence/survey/results.csv theo cách đã ghi trước ở questions.md.

Chạy: python evidence/survey/stats.py
n = phiếu có "Bạn là" = Học Viên. LabCoach / Người lạ tách riêng, không cộng chung.
Câu 3 là ô chữ tự do → quy về số lần / tuần theo bảng Q3_MAP bên dưới (ghi rõ để người khác kiểm lại).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
COL_ROLE, COL_LAST, COL_WEEK, COL_WHAT, COL_HOW, COL_TIME, COL_FOUND, COL_WRONG, COL_STORY = range(2, 11)

# Câu 3 → số lần / tuần. None = không quy được ra số.
#   "1-2 lần/ngày"   → 7   (cận dưới: 1 lần/ngày × 7 ngày)
#   "Mỗi ngày 2 lần" → 14
#   "hơn 7 lần"      → 8   (cận dưới)
#   "Rất nhiều lần." → None, nhưng xếp vào nhóm ≥2 (cách hiểu của nhóm, ghi ở summary.md)
#   "không"          → 0
Q3_MAP = {"1-2 lần/ngày": 7, "Mỗi ngày 2 lần": 14, "hơn 7 lần": 8, "Rất nhiều lần.": None, "không": 0}
AT_LEAST_2_TEXT = {"Rất nhiều lần."}
ASK_OTHERS = ("Hỏi trên kênh hỏi đáp Discord", "Nhắn riêng bạn cùng lớp", "Hỏi TA / lab coach")


def per_week(s: str):
    s = s.strip()
    if s in Q3_MAP:
        return Q3_MAP[s]
    digits = s.split()[0] if s else ""
    return int(digits) if digits.isdigit() else None


def pct(x, n):
    return f"{x}/{n} ({x / n:.0%})" if n else "0/0"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(HERE / "results.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))[1:]
    roles = Counter(r[COL_ROLE] for r in rows)
    hv = [r for r in rows if r[COL_ROLE] == "Học Viên"]
    n = len(hv)
    print(f"Tổng phiếu: {len(rows)} · theo vai: {dict(roles)} · n (học viên) = {n}\n")

    weeks = [(r, per_week(r[COL_WEEK])) for r in hv]
    ge1 = sum(1 for r, w in weeks if (w is not None and w >= 1) or r[COL_WEEK].strip() in AT_LEAST_2_TEXT)
    ge2 = sum(1 for r, w in weeks if (w is not None and w >= 2) or r[COL_WEEK].strip() in AT_LEAST_2_TEXT)
    nums = sorted(w for _, w in weeks if w is not None)
    print(f"Câu 3 · đã tra ≥1 lần trong 1 tuần qua : {pct(ge1, n)}")
    print(f"Câu 3 · tra ≥2 lần / tuần              : {pct(ge2, n)}")
    print(f"Câu 3 · số lần / tuần (quy được ra số, {len(nums)} phiếu): trung vị {nums[len(nums) // 2]} · min {nums[0]} · max {nums[-1]}")
    print(f"Câu 2 · lần gần nhất: {dict(Counter(r[COL_LAST] for r in hv))}")

    print(f"\nCâu 4 · tìm gì (chọn nhiều):")
    what = Counter(x for r in hv for x in r[COL_WHAT].split(";") if x)
    for k, v in what.most_common():
        print(f"  - {k}: {pct(v, n)}")

    print(f"\nCâu 5 · tìm bằng cách nào (chọn nhiều):")
    how = Counter(x.strip() for r in hv for x in r[COL_HOW].split(";") if x.strip())
    for k, v in how.most_common():
        print(f"  - {k}: {pct(v, n)}")
    ask = sum(1 for r in hv if any(a in r[COL_HOW] for a in ASK_OTHERS))
    print(f"  → phải hỏi người khác (kênh hỏi đáp / nhắn bạn / hỏi TA): {pct(ask, n)}")
    guess = sum(1 for r in hv if "Tự đoán" in r[COL_HOW])
    print(f"  → có tự đoán: {pct(guess, n)}")

    print(f"\nCâu 6 · mất bao lâu đến khi chắc chắn:")
    order = ["Dưới 2 phút", "2–5 phút", "5–15 phút", "15–30 phút", "Trên 30 phút", "Không tìm được"]
    t = Counter(r[COL_TIME] for r in hv)
    for k in order:
        if t[k]:
            print(f"  - {k}: {pct(t[k], n)}")
    ge5 = sum(t[k] for k in order[2:])
    print(f"  → ≥5 phút: {pct(ge5, n)}")

    f_ = Counter(r[COL_FOUND] for r in hv)
    unsure = sum(v for k, v in f_.items() if k != "Có, chắc chắn")
    print(f"\nCâu 7 · {dict(f_)}")
    print(f"  → không chắc là mới nhất / không tìm được: {pct(unsure, n)}")

    wrong = [r for r in hv if r[COL_WRONG].strip() and r[COL_WRONG].strip() != "Chưa"]
    print(f"\nCâu 8 · từng nhầm (hạn / phòng / giờ): {pct(len(wrong), n)}")
    for k, v in Counter(x for r in wrong for x in r[COL_WRONG].split(";")).most_common():
        print(f"  - {k}: {pct(v, n)}")

    print("\nKhác thường cần ghi chú:")
    for r in hv:
        if r[COL_LAST] == "Chưa bao giờ" and (per_week(r[COL_WEEK]) or 0) > 0:
            print(f"  - {r[0]}: câu 2 'Chưa bao giờ' nhưng câu 3 = {r[COL_WEEK]!r} (mâu thuẫn)")
        if r[COL_LAST] == "Hôm nay" and per_week(r[COL_WEEK]) == 0:
            print(f"  - {r[0]}: câu 2 'Hôm nay' nhưng câu 3 = {r[COL_WEEK]!r} (mâu thuẫn)")

    print("\nCâu 9 · trả lời có nội dung (học viên):")
    for r in hv:
        if len(r[COL_STORY].strip()) > 15:
            print(f"  - {r[0]}: \"{r[COL_STORY].strip()}\"")


if __name__ == "__main__":
    main()
