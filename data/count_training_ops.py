"""Đếm số mô tả quy trình lịch / phòng hiện tại từ data/training-ops của repo đề (GIẢ LẬP).

Data này KHÔNG phải bằng chứng pain (README của BTC ghi rõ). Chỉ dùng để mô tả
"hiện tại việc này diễn ra thế nào" (spec.md §0) và làm nguồn cho bản chạy thử.

Chạy:  python data/count_training_ops.py _de-bai/data/training-ops
Cần:   openpyxl (đã ghi vào requirements.txt)
"""
from __future__ import annotations

import re
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import openpyxl

SLOT_START = {"Sáng": 9, "Chiều": 14}


def pct(x: int, n: int) -> str:
    return f"{x}/{n} ({x / n:.0%})" if n else f"{x}/0"


def session_cells(ws):
    """Các ô buổi học L3 (cột D, E, F) và L2 (G, H) trong sheet Khoá 9 (GĐ1). Ô gộp D+E tính 1 buổi."""
    seen, out = set(), []
    for row in ws.iter_rows(min_row=6):
        for cell in row[3:8]:
            v = cell.value
            if not isinstance(v, str) or "—" not in v or v.strip() == "không có lớp":
                continue
            head = v.splitlines()[0].strip()          # "L3A — LEC 1"
            key = (cell.row, head)
            if key in seen:                             # D và E cùng một buổi LEC
                continue
            seen.add(key)
            out.append({"col": cell.column_letter, "head": head, "text": v})
    return out


def parse_edit_buoi(s: str, year: int = 2027):
    """'19/04 Sáng · L2B — LEC 2' → (giờ bắt đầu buổi, tên buổi)"""
    m = re.match(r"(\d{2})/(\d{2}) (Sáng|Chiều) · (.+)", s or "")
    if not m:
        return None, s
    d, mo, slot, name = m.groups()
    return datetime(year, int(mo), int(d), SLOT_START[slot]), name


def main(root: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(root)
    wb = openpyxl.load_workbook(root / "teaching-schedule.xlsx")

    # 1. Bảng lịch tại lúc xuất (21:00 27/04/2027)
    cells = session_cells(wb["Khoá 9 (GĐ1)"])
    l3 = [c for c in cells if c["head"].startswith("L3")]
    pending = [c for c in l3 if "chờ xác nhận" in c["text"]]
    online = [c for c in l3 if "\nOnline" in c["text"]]
    extra = [c for c in l3 if "Phòng thêm" in c["text"]]
    multi_lab = [c for c in l3 if "LAB" in c["head"] and re.search(r"Phòng: [^\n]*,", c["text"])]
    labs = [c for c in l3 if "LAB" in c["head"]]
    print("## 1. Bảng lịch Khoá 9 lúc xuất (27/04/2027 21:00) — chỉ lớp L3")
    print(f"- Buổi L3 có trong bảng: {len(l3)} (LEC {len(l3) - len(labs)}, LAB {len(labs)})")
    print(f"- Buổi còn 'chờ xác nhận' phòng: {pct(len(pending), len(l3))}")
    print(f"- Buổi online: {pct(len(online), len(l3))} · buổi LEC có 'Phòng thêm': {pct(len(extra), len(l3) - len(labs))}")
    print(f"- Buổi LAB rải ≥2 phòng: {pct(len(multi_lab), len(labs))}")

    # 2. Lịch sử chỉnh sửa
    ws = wb["Lịch sử chỉnh sửa"]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    kinds = Counter()
    lead_confirm, changed_after = [], []
    l3_rows = 0
    for t, who, _sheet, _cell, buoi, before, after in rows:
        start, name = parse_edit_buoi(buoi)
        edited = datetime.strptime(t, "%d/%m/%Y %H:%M")
        before, after = str(before or ""), str(after or "")
        is_l3 = name.startswith("L3")
        l3_rows += is_l3
        if "chờ xác nhận" in before and after.startswith("Phòng"):
            kind = "chot_phong"
            if start:
                lead_confirm.append(((start - edited).total_seconds() / 3600, is_l3, buoi))
        elif before.startswith("Phòng:") and after.startswith("Phòng:"):
            kind = "doi_phong_da_chot"
            changed_after.append(((start - edited).total_seconds() / 3600 if start else None, buoi, before, after))
        elif before.startswith("Phòng thêm"):
            kind = "them_phong"
        elif before.startswith("Giảng Viên"):
            kind = "doi_giang_vien"
        elif re.match(r"\d{2}:\d{2}", before):
            kind = "doi_gio"
        else:
            kind = "khac"
        kinds[kind] += 1
    n = len(rows)
    print(f"\n## 2. Lịch sử chỉnh sửa bảng lịch: {n} lần sửa (L3: {l3_rows})")
    for k, v in kinds.most_common():
        print(f"- {k}: {pct(v, n)}")
    hrs = sorted(h for h, _, _ in lead_confirm)
    if hrs:
        print(f"\nChốt phòng (từ 'chờ xác nhận' → phòng cụ thể): {len(hrs)} lần")
        print(f"- Trước giờ học: trung vị {statistics.median(hrs):.1f} giờ · ngắn nhất {hrs[0]:.1f} giờ · dài nhất {hrs[-1]:.1f} giờ")
        print(f"- Chốt < 24 giờ trước buổi: {pct(sum(h < 24 for h in hrs), len(hrs))}")
        print(f"- Chốt < 12 giờ trước buổi: {pct(sum(h < 12 for h in hrs), len(hrs))}")
        print(f"- Chốt SAU khi buổi đã bắt đầu: {pct(sum(h < 0 for h in hrs), len(hrs))}")
    if changed_after:
        print(f"\nPhòng đã chốt rồi vẫn đổi: {len(changed_after)} lần")
        for h, buoi, b, a in changed_after:
            print(f"- {buoi}: '{b}' → '{a}' ({h:.1f} giờ trước buổi)")

    # 3. Bảng lab coach
    wb2 = openpyxl.load_workbook(root / "lab-coach-schedule.xlsx")
    ws = wb2["Lịch lab 2604-0805"]
    header_col = None
    room_vals = []
    for row in ws.iter_rows(values_only=True):
        if "Phòng" in row and "Lab Coach" in row:
            header_col = row.index("Phòng")
            continue
        if header_col is not None and row[header_col]:
            room_vals.append(str(row[header_col]))
    if room_vals:
        pend = [v for v in room_vals if "chờ" in v or v.startswith("dk")]
        print(f"\n## 3. Lịch lab đợt 2 (sheet 'Lịch lab 2604-0805')")
        print(f"- Ô phòng có ghi: {len(room_vals)} · còn 'chờ xác nhận' hoặc 'dk:' (dự kiến): {pct(len(pend), len(room_vals))}")
    ws = wb2["Đổi buổi (form)"]
    req = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    print(f"- Yêu cầu đổi buổi của lab coach qua form: {len(req)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_de-bai/data/training-ops")
