"""授業ページを実際にブラウザで開いて、確認用のスクリーンショットを撮る。

使い方: python3 shot.py session01.html [出力先ディレクトリ]
"""
import pathlib, sys, http.server, socketserver, threading, functools
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
page_name = sys.argv[1]
outdir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "_shots"
outdir.mkdir(exist_ok=True, parents=True)

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 1400}, device_scale_factor=2)
    pg.goto(f"http://127.0.0.1:{port}/{page_name}")
    pg.wait_for_timeout(2500)
    total = pg.evaluate("document.body.scrollHeight")
    print("page height:", total)
    n = 0
    y = 0
    while y < total and n < 30:
        pg.evaluate(f"window.scrollTo(0,{y})")
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(outdir / f"{page_name.replace('.html','')}_{n:02d}.png"))
        y += 1300
        n += 1
    b.close()
httpd.shutdown()
print("shots:", n)
