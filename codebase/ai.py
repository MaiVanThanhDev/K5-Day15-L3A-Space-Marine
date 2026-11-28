"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import socket
import time
import urllib.error
import urllib.request

from tracing import model_call

SHOW_RAW = False   # True: in nguyên phản hồi API (khi cần tìm tên trường)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
MODEL_BASE_URL = (os.environ.get("MODEL_BASE_URL") or "").strip()  # tuỳ chọn: API dạng OpenAI khác, Ollama máy khác


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env (mã gọi API của model).")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env.")
    if MODEL_PROVIDER in ("openai", "openai_compat", "deepseek"):
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "openrouter":
        # OpenRouter dùng API dạng OpenAI; MODEL_NAME có tiền tố nhà cung cấp, vd google/gemini-3.1-flash-lite
        r = call_openai(system, user, MODEL_BASE_URL or "https://openrouter.ai/api/v1")
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "MODEL_PROVIDER=%s chưa hỗ trợ — dùng openai / anthropic / gemini / ollama "
            "(API dạng OpenAI: openai + MODEL_BASE_URL). Xem docs/connect-model.md" % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"] or 0), "tokens_out": int(r["tokens_out"] or 0)}


# ---------------------------------------------------------------- gọi API (chỉ thư viện chuẩn)

RETRIES = 2            # gọi lại tối đa 2 lần khi lỗi tạm thời (hết giờ chờ, 429, 5xx)
RETRY_WAIT = [5, 15]   # giây chờ trước lần gọi lại thứ 1, 2


def post_json(url, headers, body, timeout=120):
    """Gửi POST JSON, trả về JSON phản hồi. Lỗi tạm thời thì gọi lại; lỗi khác (sai key, sai model) báo ngay.
    Chỉ lần gọi thành công trả token, nên token đếm vẫn là token thật của câu trả lời."""
    data = None
    for attempt in range(RETRIES + 1):
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"), method="POST",
            headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = "HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300])
            if (e.code == 429 or e.code >= 500) and attempt < RETRIES:
                time.sleep(RETRY_WAIT[attempt])
                continue
            raise RuntimeError(msg)
        except (TimeoutError, socket.timeout, urllib.error.URLError) as e:
            if attempt < RETRIES:
                time.sleep(RETRY_WAIT[attempt])
                continue
            raise RuntimeError("Gọi model thất bại sau %d lần: %s: %s" % (RETRIES + 1, type(e).__name__, e))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system, user, base_url=None):
    """OpenAI và mọi API dạng OpenAI (đổi MODEL_BASE_URL, vd https://api.deepseek.com/v1; OpenRouter)."""
    url = (base_url or MODEL_BASE_URL or "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {"Authorization": "Bearer " + API_KEY}, {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"] or "",
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


def call_claude(system, user):
    data = post_json("https://api.anthropic.com/v1/messages",
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


def call_gemini(system, user):
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}],
            # agent.py cần JSON: bật chế độ trả JSON của Gemini (không có ``` bao quanh)
            "generationConfig": {"responseMimeType": "application/json"}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {"x-goog-api-key": API_KEY}, body)
    parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
    u = data.get("usageMetadata") or {}
    return {"text": "".join(p.get("text", "") for p in parts if not p.get("thought")),
            "tokens_in": u.get("promptTokenCount", 0),
            # token suy nghĩ tính riêng ở Gemini → cộng vào token ra (hợp đồng ở đầu file)
            "tokens_out": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)}


def call_ollama(system, user):
    url = (MODEL_BASE_URL or "http://localhost:11434").rstrip("/") + "/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}
