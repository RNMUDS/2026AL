"""全ページをブラウザで開き、コンソールエラーとリンク切れがないか確かめる。"""
import functools, http.server, pathlib, socketserver, threading
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()

pages = ["index.html", "grading.html"] + [f"session{i:02d}.html" for i in range(1, 16)]
problems = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for name in pages:
        pg = b.new_page(viewport={"width": 1000, "height": 1200})
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(f"http://127.0.0.1:{port}/{name}")
        # loading="lazy" の画像を読み込ませるため、いったん最後までスクロールする
        pg.wait_for_timeout(400)
        height = pg.evaluate("document.body.scrollHeight")
        y = 0
        while y < height:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(150)
            y += 900
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(1200)
        # ページ内リンクの飛び先が存在するか
        bad_anchors = pg.evaluate("""() => {
            const bad = [];
            document.querySelectorAll('a[href^="#"]').forEach(a => {
                const id = a.getAttribute('href').slice(1);
                if (id && !document.getElementById(id)) bad.push(a.getAttribute('href'));
            });
            return [...new Set(bad)];
        }""")
        # 解答セクションが表示されているか（暗号化＋公開日前ならロック表示）
        state = pg.evaluate("""() => {
            const s = document.getElementById('answers-section');
            if (!s) return 'no-answers';
            if (document.getElementById('answers-content')) return 'open';
            if (document.getElementById('answers-locked')) return 'locked';
            return 'unknown';
        }""")
        svg_count = pg.evaluate("() => document.querySelectorAll('.diagram-container svg').length")
        img_count = pg.evaluate("() => [...document.querySelectorAll('img')].filter(i => !i.complete || i.naturalWidth === 0).length")
        print(f"{name:<18} 図{svg_count:>2}  解答:{state:<7} 壊れ画像:{img_count}  "
              f"リンク切れ:{bad_anchors or '-'}  読み込み失敗:{len(failed)}  エラー:{len(errors)}")
        if errors or bad_anchors or img_count or failed:
            problems.append((name, errors, bad_anchors, img_count, failed))
        pg.close()
    b.close()
httpd.shutdown()
print()
print("問題のあるページ:", [p[0] for p in problems] or "なし")
for name, errors, anchors, imgs, failed in problems:
    print(" ", name, errors[:3], anchors, imgs, failed[:3])
