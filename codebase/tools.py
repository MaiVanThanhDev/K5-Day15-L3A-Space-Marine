"""Công cụ của bài toán — trợ lý hạn nộp / phòng học / lịch cho học viên L3 (spec.md §4).

Ba công cụ, khớp bảng "AI dựa vào đâu" ở spec.md §4:
    search_announcements(query)        tra thông báo (hạn nộp, quy định…)      — chỉ đọc
    get_schedule(date, class_name)     lịch một ngày + phòng từ thông báo mới nhất — chỉ đọc
    draft_ta_handoff(question, reason) soạn BẢN NHÁP chuyển TA, chờ người duyệt   — KHÔNG tự gửi

Dữ liệu: data/announcements.json (synthetic, mô tả ở data/DATA_CARD.md).
Trạng thái từng thông báo do CODE tính (không để model tự đoán):
    hien_hanh        thông báo chính thức, chưa bị thay, không mâu thuẫn → được trích làm nguồn
    da_bi_thay       đã có thông báo chính thức mới hơn thay thế (trường supersedes)
    mau_thuan        ≥2 thông báo chính thức còn hiệu lực cho cùng một việc nhưng khác giá trị
    chua_chot        thông báo chính thức nói rõ là chưa chốt (value = null)
    khong_chinh_thuc tin nhắn của học viên / không phải BTC, TA
"""
import json
import os
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "announcements.json")

STOPWORDS = set("""a ah a oi cho minh em toi ban la gi khi nao bao gio o dau vay va voi cua cac nhung the nay do
khong co duoc phai roi nhe nha a hoi khoa hoc lop buoi""".split())

# ---------------------------------------------------------------- dữ liệu + trạng thái


def norm(text):
    """chữ thường, bỏ dấu tiếng Việt (đ → d), gộp khoảng trắng — để so khớp từ khoá."""
    text = unicodedata.normalize("NFD", (text or "").lower().replace("đ", "d"))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def _load():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    items = data["announcements"]
    by_id = {a["id"]: a for a in items}
    superseded_by = {}
    for a in items:
        old = a.get("supersedes")
        if a.get("official") and old in by_id:
            superseded_by[old] = a["id"]
    # mâu thuẫn: các thông báo chính thức còn hiệu lực, cùng subject, khác value
    active = {}
    for a in items:
        if a.get("official") and a["id"] not in superseded_by:
            active.setdefault(a["subject"], []).append(a)
    for a in items:
        if not a.get("official"):
            a["status"] = "khong_chinh_thuc"
        elif a["id"] in superseded_by:
            a["status"] = "da_bi_thay"
            a["thay_boi"] = superseded_by[a["id"]]
        else:
            others = [o for o in active[a["subject"]] if o["id"] != a["id"] and o.get("value") != a.get("value")]
            if others:
                a["status"] = "mau_thuan"
                a["mau_thuan_voi"] = [o["id"] for o in others]
            elif a.get("value") is None:
                a["status"] = "chua_chot"
            else:
                a["status"] = "hien_hanh"
    return data, by_id


DATA, BY_ID = _load()
AS_OF = DATA.get("as_of")


def public(a):
    """Bản rút gọn đưa cho model / người dùng."""
    keep = ("id", "source", "author_role", "posted_at", "topic", "subject", "value", "text", "status",
            "thay_boi", "mau_thuan_voi")
    return {k: a[k] for k in keep if k in a}


def citation(source_id):
    """Dòng nguồn hiển thị cho người dùng — link lấy từ DỮ LIỆU, không để model tự viết link."""
    a = BY_ID[source_id]
    return "[%s] %s — %s (đăng %s)" % (a["id"], a["source"], a["link"], a["posted_at"])


# ---------------------------------------------------------------- công cụ

TOPIC_WORDS = {
    "deadline": ["han", "nop", "deadline", "gia han", "tre", "due", "submit"],
    "room": ["phong", "room", "hoc o dau", "o dau", "toa", "zoom", "online"],
    "policy": ["tre", "quy dinh", "tru diem", "gia han rieng"],
}
HACKATHON_WORDS = ["hackathon", "checkpoint", "cp1", "cp2", "cp3", "cp4", "demo", "reflection", "slide", "day 15", "lab 15"]


def _labs(qn):
    return {"lab%d" % int(n) for n in re.findall(r"\b(?:lab|day|bai|ngay)\s*(\d{1,2})\b", qn)}


@tool
def search_announcements(query: str) -> list:
    """Tra thông báo của khoá theo câu hỏi.
    Input: câu hỏi (str). Output: tối đa 6 thông báo {id, source, posted_at, subject, value, text, status, …},
    xếp theo độ khớp; status do code tính (hien_hanh / da_bi_thay / mau_thuan / chua_chot / khong_chinh_thuc).
    Không tác động ra ngoài."""
    qn = norm(query)
    labs = _labs(qn)
    if any(w in qn for w in HACKATHON_WORDS):
        labs.discard("lab15")
    words = [w for w in re.findall(r"[a-z0-9]+", qn) if len(w) >= 2 and w not in STOPWORDS]
    scored = []
    for a in DATA["announcements"]:
        if a["topic"] == "room":
            continue  # phòng học tra qua get_schedule (theo ngày + lớp)
        subj = a["subject"]
        if labs and subj.startswith("lab") and subj not in labs:
            continue  # hỏi lab khác → loại hẳn, tránh nhầm lab
        hay = norm(a["text"] + " " + subj + " " + (a.get("value") or ""))
        score = sum(1 for w in words if re.search(r"\b%s\b" % re.escape(w), hay))
        if subj in labs:
            score += 5
        if subj == "hackathon" and any(w in qn for w in HACKATHON_WORDS):
            score += 5
        if any(w in qn for w in TOPIC_WORDS.get(a["topic"], [])):
            score += 2
        if score >= 3:
            scored.append((score, a["posted_at"], a))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [public(a) for _, _, a in scored[:6]]


@tool
def get_schedule(date: str, class_name: str = "") -> list:
    """Lịch học một ngày, kèm phòng lấy từ thông báo phòng mới nhất.
    Input: date "YYYY-MM-DD", class_name "L3A" / "L3B" / "" (không rõ lớp → trả cả hai).
    Output: danh sách buổi {date, session, time, class, activity, room, room_status, room_source, other_notices}.
    room_status: hien_hanh / chua_chot / mau_thuan / chua_co_thong_bao. Không tác động ra ngoài."""
    out = []
    for s in DATA["schedule"]:
        if s["date"] != date:
            continue
        if class_name and s["class"] not in (class_name, "ALL"):
            continue
        notices = [a for a in DATA["announcements"] if a["topic"] == "room"
                   and a["subject"] in ("room|%s|%s|%s" % (date, s["session"], s["class"]),
                                        "room|%s|%s|ALL" % (date, s["session"]))]
        main = [a for a in notices if a["status"] in ("hien_hanh", "chua_chot", "mau_thuan")]
        row = dict(s)
        if not main:
            row.update(room=None, room_status="chua_co_thong_bao", room_source=None)
        else:
            a = sorted(main, key=lambda x: x["posted_at"])[-1]
            row.update(room=a.get("value"), room_status=a["status"], room_source=a["id"])
        row["other_notices"] = [public(a) for a in notices if a["id"] != row["room_source"]]
        out.append(row)
    return out


@tool
def draft_ta_handoff(question: str, reason: str) -> dict:
    """Soạn bản nháp tin nhắn chuyển câu hỏi cho TA trực Discord.
    Input: câu hỏi gốc (str), lý do chuyển (str). Output: {status: "ban_nhap_cho_duyet", to, content}.
    CÓ tác động ra ngoài nếu gửi → công cụ KHÔNG gửi, chỉ trả bản nháp; TA / người trực duyệt rồi mới gửi."""
    content = "@TA-truc Học viên hỏi: \"%s\"\nLý do trợ lý chuyển: %s" % (question.strip()[:500], reason.strip()[:300])
    return {"status": "ban_nhap_cho_duyet", "to": "TA trực Discord", "content": content}
