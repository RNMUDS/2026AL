"""公開されたGitHub Pagesを実際に開いて、表示を確かめる。"""
from playwright.sync_api import sync_playwright

BASE = "https://rnmuds.github.io/2026AL/al2/"
pages = ["index.html"] + [f"session{i:02d}.html" for i in range(1, 16)]

with sync_playwright() as p:
    b = p.chromium.launch()
    for name in pages:
        pg = b.new_page(viewport={"width": 1000, "height": 1200})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(BASE + name, wait_until="load")
        pg.evaluate("() => document.querySelectorAll('img').forEach(i => i.loading='eager')")
        pg.wait_for_timeout(2000)
        bad = pg.evaluate("() => [...document.querySelectorAll('img')].filter(i => !i.complete || i.naturalWidth === 0).length")
        title = pg.title()
        svg = pg.evaluate("() => document.querySelectorAll('.diagram-container svg').length")
        print(f"{name:<18} {title:<44} 図{svg:>2}  画像NG:{bad}  失敗:{len(failed)}  エラー:{len(errors)}")
        pg.close()
    b.close()
