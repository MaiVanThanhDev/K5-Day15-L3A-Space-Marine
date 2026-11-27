"""Công cụ của bài toán — trợ lý lịch học / phòng học cho học viên lớp L3 (spec.md §4).

Ba công cụ, khớp bảng "AI dựa vào đâu" ở spec.md §4:
    tong_quan_khoa()                           khai giảng, khung giờ, nghỉ lễ, buổi giờ riêng… kèm ô nguồn — chỉ đọc
    tra_lich(ngay, buoi, lop, session, phong)  tra các buổi trong bảng chính + nguồn phụ + lịch sử sửa    — chỉ đọc
    soan_chuyen_ta(cau_hoi, ly_do)             soạn BẢN NHÁP tin nhắn cho TA, chờ người duyệt              — KHÔNG tự gửi

Dữ liệu: data/lich-l3-k9.csv, data/lich-su-sua-l3-k9.csv (trích từ data BTC training-ops, xem data/DATA_CARD.md).
Trạng thái mỗi buổi do CODE tính theo quy ước ở data/DATA_CARD.md (không để model tự suy):
    da_chot        bảng chính đã chốt phòng (da_chot / theo_tieu_de_cot) → dùng bảng chính, bỏ qua nguồn phụ
    chua_chot      bảng chính chờ xác nhận / dự kiến → không khẳng định phòng, dù nguồn phụ ghi gì
    online         buổi học online
    khong_ap_dung  không có lớp / nghỉ lễ / khai giảng
"""
import csv
import datetime
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LICH = os.path.join(ROOT, "data", "lich-l3-k9.csv")
LICH_SU = os.path.join(ROOT, "data", "lich-su-sua-l3-k9.csv")
MAX_BUOI = 12  # số buổi tối đa trả về một lần tra


def norm(text):
    """chữ thường, bỏ dấu tiếng Việt (đ → d), gộp khoảng trắng — để so khớp."""
    text = unicodedata.normalize("NFD", (text or "").lower().replace("đ", "d"))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def _read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _date(s):
    return datetime.datetime.strptime(s, "%d/%m/%Y").date()


ROWS = _read(LICH)
HISTORY = _read(LICH_SU)
MAIN = [r for r in ROWS if r["nguon"] == "bang_chinh"]
SECONDARY = [r for r in ROWS if r["nguon"] != "bang_chinh"]
CELLS = {(r["file"], r["sheet"], r["o"]): r for r in ROWS}
MAIN_CELLS = {r["o"]: r for r in MAIN}


def _as_of():
    """Mốc hiện tại của dữ liệu: "Bản xuất 27/04/2027 21:00" ở cột cap_nhat của bảng chính."""
    for r in MAIN:
        m = re.search(r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2})", r.get("cap_nhat", ""))
        if m:
            return datetime.datetime.strptime(" ".join(m.groups()), "%d/%m/%Y %H:%M")
    return datetime.datetime.now()


AS_OF = _as_of()


def cite(o, row=None):
    """Chuỗi trích nguồn dạng  file · sheet · ô  (dạng metric trich_nguon yêu cầu)."""
    r = row or MAIN_CELLS[o]
    return "%s · %s · %s" % (r["file"], r["sheet"], r["o"])


def rooms_of(text):
    return re.findall(r"\b[A-H]\d{3}\b", text or "")


def _status(rows):
    tt = {r["trang_thai_phong"] for r in rows}
    if tt & {"cho_xac_nhan", "du_kien"}:
        return "chua_chot"
    if "online" in tt:
        return "online"
    if tt <= {"khong_ap_dung"}:
        return "khong_ap_dung"
    return "da_chot"


def _session_obj(rows):
    """Gộp các ô bảng chính của cùng một buổi (LEC chiếm 2 cột D, E) thành một buổi."""
    r0 = rows[0]
    status = _status(rows)
    cells = [r["o"] for r in rows]
    rooms = []
    for r in rows:
        for p in rooms_of(r["phong"]):
            if p not in rooms:
                rooms.append(p)
    extra = []
    for r in rows:
        for p in rooms_of(r["phong_them"]):
            if p not in extra:
                extra.append(p)
    obj = {
        "o": cells, "ngay": r0["ngay"], "thu": r0["thu"], "buoi": r0["buoi"], "gio": r0["gio"],
        "lop": r0["lop"] or None, "session": r0["session"] or None, "chu_de": r0["chu_de"] or None,
        "hinh_thuc": ("online" if r0["online"] == "co" else (r0["ghi_chu"] or "truc_tiep")),
        "trang_thai": status,
        "phong": rooms if status == "da_chot" else [],
        "phong_them": extra if status == "da_chot" else [],
    }
    if status == "chua_chot":
        obj["phong_du_kien_chua_xac_nhan"] = rooms or "chờ xác nhận, chưa có phòng"
    # nguồn phụ cùng ngày / buổi / lớp — chỉ để model biết các nguồn đang lệch, KHÔNG dùng làm đáp án
    sec = [s for s in SECONDARY if s["ngay"] == r0["ngay"] and s["buoi"] == r0["buoi"] and s["lop"] == r0["lop"] and r0["lop"]]
    if sec:
        obj["nguon_phu"] = [{"nguon": cite(s["o"], s), "phong": s["phong"] or None,
                             "trang_thai_phong": s["trang_thai_phong"]} for s in sec]
        obj["nguon_phu_ghi_chu"] = ("Bảng chính đã chốt → bỏ qua nguồn phụ." if status == "da_chot"
                                    else "Bảng chính chưa chốt → không khẳng định phòng, dù nguồn phụ ghi gì.")
    hist = [h for h in HISTORY if set(x.strip() for x in h["o"].split(",")) & set(cells)]
    if hist:
        obj["lich_su_sua"] = [{"thoi_diem": h["thoi_diem"], "truoc": h["truoc"], "sau": h["sau"]} for h in hist]
    return obj


def cell_obj(o):
    """Một ô bảng chính → dạng buổi như tra_lich trả (dùng khi model trích ô lấy từ tong_quan_khoa)."""
    return _session_obj([MAIN_CELLS[o]]) if o in MAIN_CELLS else None


def _khung_gio(buoi):
    gios = [r["gio"] for r in MAIN if r["buoi"] == buoi and r["gio"]]
    return max(set(gios), key=gios.count) if gios else ""


@tool
def tong_quan_khoa() -> dict:
    """Thông tin chung của lịch Khoá 9 trong bảng chính: ngày khai giảng, buổi đầu tiên của mỗi lớp, ngày cuối,
    khung giờ buổi sáng / chiều, các buổi có giờ riêng, ngày nghỉ lễ, ví dụ buổi học thứ 7. Mỗi mục kèm ô nguồn.
    Input: không có. Output: dict. Không tác động ra ngoài."""
    khai = [r for r in MAIN if "KHAI GIẢNG" in r["ghi_chu"]]
    khung = {b: _khung_gio(b) for b in ("Sáng", "Chiều")}
    first = {}
    for lop in ("L3A", "L3B"):
        rows = sorted((r for r in MAIN if r["lop"] == lop), key=lambda r: (_date(r["ngay"]), r["buoi"] != "Sáng"))
        if rows:
            first[lop] = {"o": rows[0]["o"], "ngay": rows[0]["ngay"], "thu": rows[0]["thu"], "buoi": rows[0]["buoi"],
                          "gio": rows[0]["gio"], "session": rows[0]["session"]}
    rieng = [{"o": r["o"], "ngay": r["ngay"], "buoi": r["buoi"], "gio": r["gio"], "lop": r["lop"], "session": r["session"]}
             for r in MAIN if r["lop"] and r["gio"] and r["gio"] != khung.get(r["buoi"])]
    le = [{"o": r["o"], "ngay": r["ngay"], "buoi": r["buoi"]} for r in MAIN if "NGHỈ LỄ" in r["ghi_chu"]]
    t7 = [{"o": r["o"], "ngay": r["ngay"], "buoi": r["buoi"], "lop": r["lop"], "session": r["session"]}
          for r in MAIN if r["thu"] == "T7" and r["lop"]][:3]
    days = sorted({_date(r["ngay"]) for r in MAIN})
    return {
        "nguon": "teaching-schedule.xlsx · Khoá 9 (GĐ1), bản xuất %s" % AS_OF.strftime("%H:%M %d/%m/%Y"),
        "khai_giang": [{"o": r["o"], "ngay": r["ngay"], "thu": r["thu"], "buoi": r["buoi"], "gio": r["gio"]} for r in khai],
        "buoi_hoc_dau_tien": first,
        "ngay_dau_den_ngay_cuoi": "%s – %s" % (days[0].strftime("%d/%m/%Y"), days[-1].strftime("%d/%m/%Y")),
        "khung_gio_buoi": khung,
        "buoi_gio_rieng": rieng,
        "nghi_le": le,
        "vi_du_hoc_thu_7": t7,
        "khong_co_trong_du_lieu": "hạn nộp, link nộp bài, link tài liệu / thời khoá biểu, danh sách chia học viên vào từng phòng, "
                                  "lịch họp nhóm, điểm, điểm danh",
    }


@tool
def tra_lich(ngay: str = "", buoi: str = "", lop: str = "", session: str = "", phong: str = "") -> list:
    """Tra các buổi học của lớp L3 trong bảng chính (teaching-schedule.xlsx · Khoá 9 (GĐ1)).
    Input (bỏ trống = không lọc): ngay "dd/mm/yyyy" · buoi "Sáng" / "Chiều" · lop "L3A" / "L3B" · session vd "LAB 13", "LEC 15", "HACKATHON"
    · phong mã phòng, vd "E402" (nhiều mã cách nhau dấu phẩy) — khớp phòng / phòng thêm hiện tại, hoặc phòng cũ trong lịch sử sửa.
    Output: tối đa 12 buổi {o, ngay, thu, buoi, gio, lop, session, chu_de, hinh_thuc, trang_thai, phong, phong_them,
    phong_du_kien_chua_xac_nhan?, nguon_phu?, lich_su_sua?}; khi lọc theo ngày có cả ô "không có lớp" / "NGHỈ LỄ".
    Không tác động ra ngoài."""
    if not (ngay or lop or session or phong):
        return []
    want_lop = lop.upper().replace(" ", "")
    want_ses = norm(session)
    want_rooms = set(rooms_of(phong.upper()))
    old_room_cells = {o.strip() for h in HISTORY if want_rooms & set(rooms_of(h["truoc"])) for o in h["o"].split(",")}
    picked = []
    for r in MAIN:
        if want_rooms and not (want_rooms & set(rooms_of(r["phong"] + " " + r["phong_them"])) or r["o"] in old_room_cells):
            continue
        if ngay and r["ngay"] != ngay:
            continue
        if buoi and norm(r["buoi"]) != norm(buoi):
            continue
        if not r["lop"]:  # ô không có lớp / nghỉ lễ / khai giảng: chỉ có nghĩa khi hỏi theo ngày
            if ngay and not session:
                picked.append(r)
            continue
        if want_lop and r["lop"] not in (want_lop, "L3AB"):
            continue
        if want_ses and not norm(r["session"]).startswith(want_ses):
            continue
        picked.append(r)
    groups = {}
    for r in picked:
        groups.setdefault((r["ngay"], r["buoi"], r["lop"], r["session"], r["ghi_chu"]), []).append(r)
    out = [_session_obj(g) for g in groups.values()]
    out.sort(key=lambda s: (_date(s["ngay"]), 0 if s["buoi"] == "Sáng" else 1, s["o"][0]))
    return out[:MAX_BUOI]


@tool
def soan_chuyen_ta(cau_hoi: str, ly_do: str) -> dict:
    """Soạn bản nháp tin nhắn chuyển câu hỏi cho TA trực Discord.
    Input: câu hỏi gốc (str), lý do chuyển (str). Output: {trang_thai: "ban_nhap_cho_duyet", gui_cho, noi_dung}.
    CÓ tác động ra ngoài nếu gửi → công cụ KHÔNG gửi, chỉ trả bản nháp; người trực duyệt rồi mới gửi."""
    noi_dung = "@TA-truc Học viên hỏi: \"%s\"\nLý do trợ lý chuyển: %s" % (cau_hoi.strip()[:500], ly_do.strip()[:300])
    return {"trang_thai": "ban_nhap_cho_duyet", "gui_cho": "TA trực Discord", "noi_dung": noi_dung}
