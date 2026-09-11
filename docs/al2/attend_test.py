"""出席コードの表示を、日時を変えて確かめる。"""
import functools, http.server, pathlib, socketserver, threading
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()

cases = [
    ("いま（授業日でない）",       "2026-09-11T17:30:00+09:00", "Asia/Tokyo"),
    ("第1回の朝",                 "2026-09-16T10:00:00+09:00", "Asia/Tokyo"),
    ("第1回の授業中",             "2026-09-16T15:00:00+09:00", "Asia/Tokyo"),
    ("第1回の授業後",             "2026-09-16T17:00:00+09:00", "Asia/Tokyo"),
    ("第14回の授業中",            "2026-12-23T14:45:00+09:00", "Asia/Tokyo"),
    ("第15回の授業中・海外のPC",   "2027-01-13T15:00:00+09:00", "America/New_York"),
    ("全部終わったあと",          "2027-02-01T15:00:00+09:00", "Asia/Tokyo"),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, when, tz in cases:
        ctx = b.new_context(timezone_id=tz)
        pg = ctx.new_page()
        pg.clock.set_fixed_time(when)
        pg.goto(f"http://127.0.0.1:{port}/index.html")
        pg.wait_for_timeout(1500)
        text = pg.evaluate("document.getElementById('attend-box').innerText").replace("\n", " ／ ")
        print(f"{label:<22} → {text[:80]}")
        ctx.close()
    # スタッフ用パスワード
    ctx = b.new_context(timezone_id="Asia/Tokyo"); pg = ctx.new_page()
    pg.clock.set_fixed_time("2026-09-11T17:30:00+09:00")
    pg.goto(f"http://127.0.0.1:{port}/index.html"); pg.wait_for_timeout(1500)
    pg.click("summary"); pg.fill("#attend-pass", "attend-al2-2026"); pg.click("#attend-pass-btn")
    pg.wait_for_timeout(1500)
    rows = pg.evaluate("[...document.querySelectorAll('#attend-box tr')].map(r => r.innerText.replace(/\\t/g,' ')).slice(0,4)")
    print("スタッフ表示:", rows, "…")
    b.close()
httpd.shutdown()
