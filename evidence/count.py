"""Đếm tin hỏi hạn nộp / phòng học / lịch học trong kênh hỏi đáp Discord.

Cách đếm (ghi trước khi chạy, chi tiết ở evidence/data-mining.md §1):
  Mẫu số N   = tin của HỌC VIÊN trong kênh, trong khoảng ngày đã chọn
               (bỏ bot, bỏ tài khoản TA / BTC / lab coach trong --staff, bỏ tin rỗng / chỉ có ảnh).
  Tử số x    = tin trong N là CÂU HỎI và thuộc ít nhất 1 chủ đề: han_nop · phong · lich.
  Tử số y    = tin trong x mà người gán nhãn ghi `co` ở cột da_co_trong_thong_bao
               (= thông báo chính thức đăng TRƯỚC giờ hỏi đã có câu trả lời).

Bước 1 — phân loại tự động, sinh file gán nhãn (không commit vì có nội dung tin):
  python evidence/count.py evidence/raw-discord.json --staff evidence/raw-staff.txt \
      --from 2026-10-01 --to 2026-11-27
  → in số N, x ra màn hình, ghi evidence/raw-labels.csv

Bước 2 — mở raw-labels.csv, với từng dòng điền 2 cột:
  dung_chu_de           : co / khong   (máy phân loại có đúng là câu hỏi hạn/phòng/lịch không)
  da_co_trong_thong_bao : co / khong / chua_ro
Rồi chạy lại cùng lệnh, thêm --labels evidence/raw-labels.csv → ra x đã kiểm tay và y.

Input: file xuất bằng DiscordChatExporter (JSON hoặc CSV). Chỉ dùng thư viện chuẩn.
Output in ra màn hình chỉ có số tổng hợp + ví dụ đã ẩn danh (tên → U1, U2…; bỏ @mention, email, SĐT, link).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

# ---------- Từ khoá: so khớp trên chữ đã bỏ dấu, viết thường ----------
TOPICS = {
    "han_nop": [
        r"\bhan\b", r"han nop", r"deadline", r"\bdl\b", r"\bdue\b", r"\bnop\b", r"submit",
        r"het han", r"tre han", r"nop muon", r"nop tre", r"checkpoint", r"\bcp\d\b",
    ],
    "phong": [
        r"\bphong\b", r"\broom\b", r"\btang\b", r"toa nha", r"dia diem", r"o dau hoc", r"hoc o dau",
        r"co so", r"\bzoom\b", r"link (hoc|zoom|meet)",
    ],
    "lich": [
        r"\blich\b", r"schedule", r"may gio", r"\bgio hoc\b", r"buoi (mai|toi|sau|nay)", r"hom nay (co )?hoc",
        r"mai (co )?hoc", r"nghi hoc", r"doi lich", r"\bonline\b", r"\boffline\b", r"hoc bu",
    ],
}
QUESTION_WORDS = [
    r"\?", r"\bkhong\b\s*(a|ạ|nhi|nhe|vay)?\s*$", r"\bchua\b\s*(a|nhi)?\s*$", r"khi nao", r"bao gio",
    r"\bnao\b", r"o dau", r"\bmay\b", r"bao nhieu", r"co ai biet", r"cho (em|minh|to) hoi", r"\bhoi\b",
    r"\bphai khong\b", r"\bdung khong\b", r"\bko\b\s*$", r"\bk\b\s*$",
]

TOPIC_RE = {k: re.compile("|".join(v)) for k, v in TOPICS.items()}
QUESTION_RE = re.compile("|".join(QUESTION_WORDS))

MENTION_RE = re.compile(r"<@[!&]?\d+>|@\S+")
URL_RE = re.compile(r"https?://\S+")
EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
PHONE_RE = re.compile(r"(\+?84|0)\d[\d .-]{7,}\d")
ID_RE = re.compile(r"\b2A\d{9}\b", re.I)  # mã học viên


def fold(text: str) -> str:
    """Bỏ dấu tiếng Việt + viết thường, để so từ khoá."""
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text.lower()).strip()


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[email]", text)
    text = URL_RE.sub("[link]", text)
    text = MENTION_RE.sub("[@]", text)
    text = PHONE_RE.sub("[sđt]", text)
    text = ID_RE.sub("[mã HV]", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------- Đọc file xuất ----------
def load_messages(path: Path) -> list[dict]:
    """Trả về list {id, time, author, is_bot, text} từ JSON hoặc CSV của DiscordChatExporter."""
    out = []
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        for m in data.get("messages", data if isinstance(data, list) else []):
            a = m.get("author") or {}
            out.append({
                "id": str(m.get("id", "")),
                "time": m.get("timestamp", ""),
                "author": a.get("name") or a.get("nickname") or str(a.get("id", "")),
                "author_id": str(a.get("id", "")),
                "is_bot": bool(a.get("isBot")),
                "text": m.get("content") or "",
            })
    elif path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            for i, r in enumerate(csv.DictReader(f)):
                out.append({
                    "id": r.get("MessageID") or r.get("ID") or str(i),
                    "time": r.get("Date") or r.get("Timestamp") or "",
                    "author": r.get("Author") or "",
                    "author_id": r.get("AuthorID") or "",
                    "is_bot": (r.get("Author") or "").lower().endswith("[bot]"),
                    "text": r.get("Content") or "",
                })
    else:
        sys.exit(f"Không đọc được {path}: chỉ nhận .json hoặc .csv (DiscordChatExporter)")
    return out


def parse_day(s: str) -> date | None:
    s = (s or "").strip()
    for fmt in (None, "%d-%b-%y %I:%M %p", "%m/%d/%Y %I:%M %p", "%d/%m/%Y %H:%M"):
        try:
            if fmt is None:
                return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def load_staff(path: str | None) -> set[str]:
    if not path:
        return set()
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return {fold(x) for x in lines if x.strip() and not x.startswith("#")}


def load_labels(path: str | None) -> dict[str, dict]:
    if not path:
        return {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {r["msg_id"]: r for r in csv.DictReader(f)}


def pct(x: int, n: int) -> str:
    return f"{x}/{n} ({x / n:.1%})" if n else f"{x}/0"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="file xuất Discord (.json / .csv), đặt tên evidence/raw-*.json để không bị commit")
    ap.add_argument("--staff", help="file .txt, mỗi dòng một tên hoặc ID tài khoản TA / BTC / lab coach (bỏ khỏi mẫu số)")
    ap.add_argument("--from", dest="d_from", help="từ ngày YYYY-MM-DD (tính cả ngày đó)")
    ap.add_argument("--to", dest="d_to", help="đến ngày YYYY-MM-DD (tính cả ngày đó)")
    ap.add_argument("--labels", help="raw-labels.csv đã gán nhãn tay → tính x đã kiểm và y")
    ap.add_argument("--out", default="evidence/raw-labels.csv", help="nơi ghi file gán nhãn (mặc định evidence/raw-labels.csv)")
    ap.add_argument("--examples", type=int, default=8, help="số ví dụ ẩn danh in ra")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định không in được tiếng Việt

    msgs = load_messages(Path(args.export))
    staff = load_staff(args.staff)
    d_from = date.fromisoformat(args.d_from) if args.d_from else None
    d_to = date.fromisoformat(args.d_to) if args.d_to else None

    dropped = {"bot": 0, "staff": 0, "ngoai_khoang_ngay": 0, "rong": 0}
    pool = []
    for m in msgs:
        day = parse_day(m["time"])
        if m["is_bot"]:
            dropped["bot"] += 1
        elif fold(m["author"]) in staff or m["author_id"] in staff:
            dropped["staff"] += 1
        elif (d_from and (not day or day < d_from)) or (d_to and (not day or day > d_to)):
            dropped["ngoai_khoang_ngay"] += 1
        elif not m["text"].strip():
            dropped["rong"] += 1
        else:
            m["day"] = day
            pool.append(m)

    alias: dict[str, str] = {}
    hits = []
    for m in pool:
        f = fold(m["text"])
        topics = [k for k, r in TOPIC_RE.items() if r.search(f)]
        m["is_q"] = bool(QUESTION_RE.search(f))
        m["topics"] = topics
        key = m["author_id"] or m["author"]
        alias.setdefault(key, f"U{len(alias) + 1}")
        m["alias"] = alias[key]
        if m["is_q"] and topics:
            hits.append(m)

    N = len(pool)
    days = sorted(d for d in (m["day"] for m in pool) if d)
    print(f"File: {args.export} · tổng {len(msgs)} tin · bỏ {dropped}")
    if days:
        print(f"Khoảng ngày thực tế: {days[0]} → {days[-1]} · {len(alias)} học viên khác nhau")
    print(f"\nN (tin học viên)                    = {N}")
    print(f"Tin là câu hỏi (mọi chủ đề)         = {pct(sum(m['is_q'] for m in pool), N)}")
    print(f"x · câu hỏi hạn/phòng/lịch (máy)    = {pct(len(hits), N)}")
    for k in TOPICS:
        print(f"    - {k:<8} = {pct(sum(k in m['topics'] for m in hits), N)}")

    labels = load_labels(args.labels)
    if labels:
        checked = [m for m in hits if m["id"] in labels]
        ok = [m for m in checked if labels[m["id"]].get("dung_chu_de", "").strip().lower() == "co"]
        ans = [m for m in ok if labels[m["id"]].get("da_co_trong_thong_bao", "").strip().lower() == "co"]
        unk = [m for m in ok if labels[m["id"]].get("da_co_trong_thong_bao", "").strip().lower() == "chua_ro"]
        print(f"\n--- Sau khi gán nhãn tay ({len(checked)}/{len(hits)} dòng đã có nhãn) ---")
        print(f"Máy phân loại đúng (precision)      = {pct(len(ok), len(checked))}")
        print(f"x đã kiểm · câu hỏi hạn/phòng/lịch  = {pct(len(ok), N)}")
        print(f"y · đã có đáp án trong thông báo    = {pct(len(ans), len(ok))}  (chưa rõ: {len(unk)})")
        sample = ok
    else:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["msg_id", "ngay", "nguoi", "chu_de", "noi_dung", "dung_chu_de", "da_co_trong_thong_bao", "ghi_chu"])
            for m in hits:
                w.writerow([m["id"], m["day"], m["alias"], "+".join(m["topics"]), m["text"], "", "", ""])
        print(f"\nĐã ghi {len(hits)} dòng cần gán nhãn tay → {out}  (KHÔNG commit file này)")
        sample = hits

    print(f"\nVí dụ đã ẩn danh (chép vào data-mining.md §4):")
    step = max(1, len(sample) // max(1, args.examples))
    for m in sample[::step][: args.examples]:
        print(f"  - [{m['day']} · {m['alias']} · {'+'.join(m['topics'])}] \"{redact(m['text'])[:160]}\"")


if __name__ == "__main__":
    main()
