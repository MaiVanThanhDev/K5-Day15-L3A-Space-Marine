"""Giao diện chat web cho bản chạy thử (chỉ thư viện chuẩn).

Chạy:  python3 codebase/web.py [--port 8000]   rồi mở http://127.0.0.1:8000
Mỗi tin nhắn → answer() trong agent.py, bọc tracing.begin("web") / end() như app.py
để đếm số lần gọi model, công cụ, token.
"""
import argparse
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tracing  # noqa: E402
from agent import answer  # noqa: E402

LOCK = threading.Lock()  # tracing dùng trạng thái chung → xử lý từng câu một

PAGE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trợ lý lịch L3</title>
<style>
:root{
  --bg:#313338; --side:#2b2d31; --input:#383a40; --text:#dbdee1; --muted:#949ba4;
  --accent:#5865f2; --bot:#23a559; --err:#f23f43; --hover:#2e3035; --border:#1f2023;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--text);font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;display:flex}
aside{width:240px;background:var(--side);padding:16px 8px;display:flex;flex-direction:column;gap:4px}
aside h1{font-size:15px;margin:0 8px 12px;color:#fff}
.chan{padding:6px 8px;border-radius:4px;color:var(--muted)}
.chan.on{background:#404249;color:#fff}
.hint{margin-top:auto;font-size:12px;color:var(--muted);padding:8px}
main{flex:1;display:flex;flex-direction:column;min-width:0}
header{height:48px;border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 16px;font-weight:600;color:#fff;gap:8px}
header span{color:var(--muted);font-weight:400;font-size:13px}
#log{flex:1;overflow-y:auto;padding:16px 0}
.msg{display:flex;gap:12px;padding:6px 16px}
.msg:hover{background:var(--hover)}
.av{width:40px;height:40px;border-radius:50%;flex:none;display:grid;place-items:center;font-weight:700;color:#fff}
.u .av{background:var(--accent)} .b .av{background:var(--bot)}
.name{font-weight:600;color:#fff} .b .name{color:#57f287}
.tag{background:var(--accent);color:#fff;font-size:10px;padding:1px 4px;border-radius:3px;margin-left:4px;vertical-align:middle}
.time{color:var(--muted);font-size:12px;margin-left:6px}
.body{white-space:pre-wrap;word-wrap:break-word}
.meta{color:var(--muted);font-size:12px;margin-top:2px}
.err .body{color:var(--err)}
.typing{color:var(--muted);font-size:13px;padding:0 16px 4px;height:20px}
form{padding:0 16px 20px}
.box{background:var(--input);border-radius:8px;display:flex;align-items:flex-end}
textarea{flex:1;background:none;border:0;color:var(--text);font:inherit;padding:11px 14px;resize:none;outline:none;max-height:200px}
button{background:none;border:0;color:var(--muted);padding:10px 14px;cursor:pointer;font-size:18px}
button:disabled{opacity:.4;cursor:default}
.chips{display:flex;flex-wrap:wrap;gap:8px;padding:0 16px 10px}
.chip{background:var(--side);border:1px solid var(--border);color:var(--text);border-radius:14px;padding:4px 10px;font-size:13px;cursor:pointer}
.chip:hover{background:#404249}
@media (max-width:700px){aside{display:none}}
</style>
</head>
<body>
<aside>
  <h1>AI20K · L3</h1>
  <div class="chan on"># hỏi-lịch-học</div>
  <div class="chan"># thông-báo</div>
  <div class="hint">Trợ lý chỉ trả lời khi có nguồn chính thức. Không chắc → chuyển TA (bản nháp chờ duyệt).</div>
</aside>
<main>
  <header># hỏi-lịch-học <span>Hỏi lịch học, giờ học, phòng học lớp L3A / L3B</span></header>
  <div id="log"></div>
  <div class="chips" id="chips"></div>
  <div class="typing" id="typing"></div>
  <form id="f">
    <div class="box">
      <textarea id="t" rows="1" placeholder="Nhắn #hỏi-lịch-học" autofocus></textarea>
      <button id="send" title="Gửi">➤</button>
    </div>
  </form>
</main>
<script>
const log=document.getElementById('log'),t=document.getElementById('t'),f=document.getElementById('f'),
      send=document.getElementById('send'),typing=document.getElementById('typing'),chips=document.getElementById('chips');
const SAMPLES=["Buổi học tối mai lớp L3A ở phòng nào?","Thứ Bảy này L3B học mấy giờ?","Hạn nộp bài tuần này là khi nào?"];
SAMPLES.forEach(s=>{const c=document.createElement('button');c.type='button';c.className='chip';c.textContent=s;
  c.onclick=()=>{t.value=s;f.requestSubmit()};chips.appendChild(c)});
function hhmm(){return new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit'})}
function add(kind,text,meta){
  const d=document.createElement('div');d.className='msg '+kind;
  const bot=kind!=='u';
  d.innerHTML=`<div class="av">${bot?'TL':'Bạn'.slice(0,1)}</div><div style="min-width:0">
    <div><span class="name">${bot?'Trợ lý L3':'Bạn'}</span>${bot?'<span class="tag">BOT</span>':''}<span class="time">${hhmm()}</span></div>
    <div class="body"></div>${meta?'<div class="meta"></div>':''}</div>`;
  d.querySelector('.body').textContent=text;
  if(meta)d.querySelector('.meta').textContent=meta;
  log.appendChild(d);log.scrollTop=log.scrollHeight;
}
add('b','Chào bạn! Mình tra lịch học / phòng học lớp L3 theo bảng phân công chính thức. Bạn cần hỏi gì?');
t.addEventListener('input',()=>{t.style.height='auto';t.style.height=t.scrollHeight+'px'});
t.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();f.requestSubmit()}});
f.addEventListener('submit',async e=>{
  e.preventDefault();const q=t.value.trim();if(!q||send.disabled)return;
  chips.style.display='none';
  add('u',q);t.value='';t.style.height='auto';send.disabled=true;typing.textContent='Trợ lý L3 đang trả lời…';
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:q})});
    const j=await r.json();
    if(j.error)add('b err',j.error);
    else{const s=j.stats||{};
      add('b',j.output||'(không có trả lời)',`model: ${(s.models||[]).join(', ')||'—'} · gọi model ${s.model_calls||0} · công cụ ${s.tool_calls||0} · token ${s.tokens_in||0}/${s.tokens_out||0}`)}
  }catch(err){add('b err','Không kết nối được server: '+err)}
  send.disabled=false;typing.textContent='';t.focus();
});
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        else:
            self._send(404, "Không có trang này", "text/plain")

    def do_POST(self):
        if self.path != "/api/chat":
            return self._json(404, {"error": "Không có API này"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            text = (json.loads(self.rfile.read(n) or b"{}").get("text") or "").strip()
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Dữ liệu gửi lên không hợp lệ"})
        if not text:
            return self._json(400, {"error": "Câu hỏi trống"})
        with LOCK:
            tracing.begin("web")
            try:
                result = answer(text)
            except NotImplementedError as e:
                tracing.end()
                return self._json(200, {"error": "Chưa nối model: %s" % e})
            except Exception as e:  # lỗi gọi model: báo, server chạy tiếp
                tracing.end()
                return self._json(200, {"error": "[lỗi] %s: %s" % (type(e).__name__, e)})
            stats, _ = tracing.end()
        output = result.get("output", "") if isinstance(result, dict) else str(result)
        self._json(200, {"output": output, "stats": stats})

    def log_message(self, fmt, *args):
        sys.stderr.write("[web] %s\n" % (fmt % args))


def main():
    p = argparse.ArgumentParser(description="Giao diện chat web cho trợ lý lịch L3")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    a = p.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print("Mở http://%s:%d  (dừng: Ctrl+C)" % (a.host, a.port))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
