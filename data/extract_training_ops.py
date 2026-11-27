"""Trích lịch lớp L3 từ data BTC (training-ops, GIẢ LẬP) ra CSV nhỏ cho bản chạy thử và bộ câu thử.

Chạy (ở thư mục gốc repo):
    python data/extract_training_ops.py [thư mục training-ops]
Mặc định đọc _de-bai/data/training-ops/ (repo đề, đã gitignore, KHÔNG commit file xlsx).
Cần: python -m pip install -r requirements.txt  (openpyxl)

Ghi ra:
    data/lich-l3-k9.csv        mỗi dòng = một ô lịch của lớp L3, từ 3 nguồn:
                               bang_chinh (teaching-schedule.xlsx · Khoá 9 (GĐ1), bản xuất 21:00 27/04/2027)
                               ban_chep   (lab-coach-schedule.xlsx · Lịch lớp K9 (bản chép), chép 12/04 — chỉ giữ ô KHÁC bảng chính)
                               lich_lab   (lab-coach-schedule.xlsx · Lịch lab 2604-0805, cột K–P, các buổi L3)
    data/lich-su-sua-l3-k9.csv các lần sửa ô lịch L3 (sheet Lịch sử chỉnh sửa), bỏ cột Người sửa
Bỏ: lớp L2, tên giảng viên / lab coach, email, các sheet không dùng.
"""
import csv
import os
import re
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_de-bai", "data", "training-ops")
OUT = os.path.join(ROOT, "data")
TEACH = "teaching-schedule.xlsx"
COACH = "lab-coach-schedule.xlsx"
MAIN_SHEET = "Khoá 9 (GĐ1)"
COPY_SHEET = "Lịch lớp K9 (bản chép)"
LAB_SHEET = "Lịch lab 2604-0805"
HIST_SHEET = "Lịch sử chỉnh sửa"
L3_COLS = {"D": "H209", "E": "H210", "F": None}   # cột LEC ghi phòng ở tiêu đề cột; cột F là LAB
COLS = ["nguon", "file", "sheet", "o", "ngay", "thu", "buoi", "gio", "lop", "session", "online",
        "chu_de", "phong", "trang_thai_phong", "phong_them", "ghi_chu", "cap_nhat"]
TIME = re.compile(r"^\d{1,2}:\d{2}\s*[–-]\s*\d{1,2}:\d{2}$")


def parse_cell(text, col):
    """Tách một ô lịch nhiều dòng → dict các trường."""
    lines = [x.strip() for x in str(text).split("\n") if x.strip()]
    r = {"lop": "", "session": "", "online": "khong", "chu_de": "", "phong": "", "trang_thai_phong": "",
         "phong_them": "", "ghi_chu": "", "gio_rieng": ""}
    if " — " not in lines[0]:                       # KHAI GIẢNG / NGHỈ LỄ / không có lớp
        r["ghi_chu"] = lines[0]
        r["trang_thai_phong"] = "khong_ap_dung"
        return r
    r["lop"], r["session"] = [x.strip() for x in lines[0].split(" — ", 1)]
    for line in lines[1:]:
        if line == "Online":
            r["online"] = "co"
        elif TIME.match(line):
            r["gio_rieng"] = line
        elif line.startswith("Phòng dự kiến:"):
            r["phong"] = line.split(":", 1)[1].replace("(chờ xác nhận)", "").strip()
            r["trang_thai_phong"] = "du_kien"
        elif line.startswith("Phòng thêm:"):
            r["phong_them"] = line.split(":", 1)[1].strip()
        elif line.startswith("Phòng:"):
            v = line.split(":", 1)[1].strip()
            if v == "chờ xác nhận":
                r["trang_thai_phong"] = "cho_xac_nhan"
            else:
                r["phong"], r["trang_thai_phong"] = v, "da_chot"
        elif line.startswith("Giảng Viên"):
            continue                                 # không trích tên giảng viên
        elif not r["chu_de"]:
            r["chu_de"] = line
    if r["online"] == "co":
        r["trang_thai_phong"] = "online"
    elif not r["trang_thai_phong"] and L3_COLS.get(col):
        r["phong"], r["trang_thai_phong"] = L3_COLS[col], "theo_tieu_de_cot"
    return r


def schedule_rows(ws, nguon, fname, cap_nhat, only_cells=None):
    rows, ngay = [], ""
    for r in range(6, ws.max_row + 1):
        ngay = ws["A%d" % r].value or ngay
        thu, khung = ws["B%d" % r].value or "", ws["C%d" % r].value or ""
        m = re.match(r"(Sáng|Chiều)\s*\((.*)\)", str(khung))
        for col in L3_COLS:
            ref = "%s%d" % (col, r)
            v = ws[ref].value
            if v is None or (only_cells is not None and ref not in only_cells):
                continue
            p = parse_cell(v, col)
            rows.append({"nguon": nguon, "file": fname, "sheet": ws.title, "o": ref, "ngay": ngay, "thu": thu,
                         "buoi": m.group(1) if m else khung, "gio": p["gio_rieng"] or (m.group(2).replace(" - ", "–") if m else ""),
                         "lop": p["lop"], "session": p["session"], "online": p["online"], "chu_de": p["chu_de"],
                         "phong": p["phong"], "trang_thai_phong": p["trang_thai_phong"], "phong_them": p["phong_them"],
                         "ghi_chu": p["ghi_chu"], "cap_nhat": cap_nhat})
    return rows


def lab_rows(ws):
    rows, seen = [], set()
    for r in range(6, ws.max_row + 1):
        ngay, lop, session, phong, buoi = [ws.cell(r, c).value for c in range(11, 16)]
        if not lop or not str(lop).startswith("L3") or (ngay, lop, session) in seen:
            continue
        seen.add((ngay, lop, session))
        phong = str(phong or "").strip()
        them = ""
        if " + " in phong:
            phong, them = [x.strip() for x in phong.split(" + ", 1)]
        if phong.startswith("dk:"):
            phong, tt = phong[3:].strip(), "du_kien"
        elif phong == "chờ xác nhận":
            phong, tt = "", "cho_xac_nhan"
        else:
            tt = "da_chot"
        rows.append({"nguon": "lich_lab", "file": COACH, "sheet": ws.title, "o": "N%d" % r, "ngay": ngay, "thu": "",
                     "buoi": buoi, "gio": "", "lop": lop, "session": session, "online": "khong", "chu_de": "",
                     "phong": phong, "trang_thai_phong": tt, "phong_them": them, "ghi_chu": "",
                     "cap_nhat": "không ghi giờ cập nhật"})
    return rows


def main():
    teach = openpyxl.load_workbook(os.path.join(SRC, TEACH))
    coach = openpyxl.load_workbook(os.path.join(SRC, COACH))
    main_ws, copy_ws = teach[MAIN_SHEET], coach[COPY_SHEET]
    diff = {"%s%d" % (c, r) for r in range(6, main_ws.max_row + 1) for c in L3_COLS
            if main_ws["%s%d" % (c, r)].value != copy_ws["%s%d" % (c, r)].value}
    rows = (schedule_rows(main_ws, "bang_chinh", TEACH, str(main_ws["D1"].value))
            + schedule_rows(copy_ws, "ban_chep", COACH, str(copy_ws["D1"].value), only_cells=diff)
            + lab_rows(coach[LAB_SHEET]))
    with open(os.path.join(OUT, "lich-l3-k9.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    hist = []
    for r in teach[HIST_SHEET].iter_rows(min_row=2, values_only=True):
        thoi_diem, _nguoi, sheet, o, buoi, truoc, sau = r
        if buoi and "· L3" in buoi:
            hist.append({"thoi_diem": thoi_diem, "file": TEACH, "sheet": sheet, "o": o, "buoi": buoi,
                         "truoc": truoc, "sau": sau})
    with open(os.path.join(OUT, "lich-su-sua-l3-k9.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["thoi_diem", "file", "sheet", "o", "buoi", "truoc", "sau"])
        w.writeheader()
        w.writerows(hist)
    by = {}
    for x in rows:
        by[x["nguon"]] = by.get(x["nguon"], 0) + 1
    print("data/lich-l3-k9.csv: %d dòng %s · data/lich-su-sua-l3-k9.csv: %d dòng" % (len(rows), by, len(hist)))


if __name__ == "__main__":
    main()
