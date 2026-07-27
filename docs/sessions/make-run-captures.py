"""授業ページの <pre> から実コードを抜き出して実行し、その出力を
ターミナル風の PNG (images/sXX_*_result.png) に描画するビルドスクリプト。

使い方:
    python3 make-run-captures.py session15.html

処理:
  1. <pre> 内の <span class="code-label">Python ── AL15-ex1.py</span> を手がかりにコードを抽出
  2. 実際に python3 で実行し、標準出力を取得（失敗したら画像を作らず報告）
  3. ターミナル風 PNG を images/ に保存
  4. HTML 側の <img ... alt="..."> を実際の出力で自動更新（記述ズレ防止）

ファイル名に "std" を含むもの（予測型の課題）は、答えの流出を防ぐためスキップする。
必要ライブラリ: Pillow
"""
import re, html, subprocess, tempfile, os, sys, pathlib
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) < 2:
    sys.exit("usage: python3 make-run-captures.py <session??.html>")
SRC   = pathlib.Path(sys.argv[1]).resolve()
OUT   = SRC.parent / "images"
SCALE = 2                      # Retina（HTML には width=物理幅/SCALE を書き込む）
FS_PT = 12.5                   # 論理 px でのフォントサイズ
FS    = int(FS_PT * SCALE)
MONO  = "/System/Library/Fonts/Menlo.ttc"
JP    = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

MINW  = int(380 * SCALE)       # 全パネル共通の最小幅（論理 380px）

# ページの <pre> と同じ配色。プロンプトは控えめにして出力を主役にする
BG, TXT, PROMPT = "#0A0A0A", "#cdd6f4", "#5f6672"

f_mono = ImageFont.truetype(MONO, FS)
f_jp   = ImageFont.truetype(JP,   FS)
CW     = f_mono.getlength("M")          # 半角1文字の幅

def draw_line(d, x, y, text, color):
    """半角=Menlo(等幅), 全角=ヒラギノ(自然な字送り) の混植描画"""
    for ch in text:
        wide = ord(ch) > 0x2000
        f = f_jp if wide else f_mono
        d.text((x, y), ch, font=f, fill=color)
        x += f.getlength(ch) if wide else CW

def cells(text):
    """描画幅を半角セル数に換算"""
    return sum((f_jp.getlength(c) / CW) if ord(c) > 0x2000 else 1 for c in text)

def render(path, filename, out_lines):
    """装飾を持たない素の出力パネルを描く。角丸・枠線は CSS 側 (.run-capture img) が付ける。"""
    lines = [("$ python3 " + filename, PROMPT)] + [(l, TXT) for l in out_lines]
    pad = int(14 * SCALE)
    lh  = int(FS * 1.62)
    w   = int(max(cells(t) for t, _ in lines) * CW) + pad * 2
    w   = max(w, MINW)          # 4枚の幅を揃えて、並んだときにばらつかないようにする
    h   = pad * 2 + lh * len(lines)

    img = Image.new("RGB", (int(w), int(h)), BG)
    d   = ImageDraw.Draw(img)
    y   = pad
    for t, c in lines:
        draw_line(d, pad, y, t, c)
        y += lh
    img.save(path)
    return img.size

# ── HTML から実コードを取り出して実行 ──
src    = SRC.read_text(encoding="utf-8")
blocks = re.findall(r"<pre>(.*?)</pre>", src, re.S)
tmp    = tempfile.mkdtemp()
OUT.mkdir(exist_ok=True)

for b in blocks:
    m = re.search(r'<span class="code-label">(.*?)</span>', b)
    label = html.unescape(re.sub("<.*?>", "", m.group(1)))
    fname = label.split("── ")[-1].strip()
    if "std" in fname:            # 予測課題なので答えの画像は作らない
        print(f"skip {fname} (prediction task)"); continue
    code  = html.unescape(re.sub("<.*?>", "",
            re.sub(r'<span class="code-label">.*?</span>', "", b, flags=re.S))).strip("\n")
    p = os.path.join(tmp, fname)
    open(p, "w", encoding="utf-8").write(code)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print(f"!! {fname} FAILED\n{r.stderr}"); continue
    out = r.stdout.rstrip("\n").split("\n")
    prefix = "s" + re.sub(r"\D", "", SRC.stem).zfill(2)      # session15.html -> s15
    png = OUT / (prefix + "_" + re.sub(r"^AL\d+-", "", fname).replace(".py", "") + "_result.png")
    size = render(png, fname, out)

    # alt と表示サイズを「実際の出力／実際の画素数」から自動生成して HTML に書き戻す。
    # PNG は Retina 用に SCALE 倍で描いているので、width/height には論理サイズを入れる。
    # これを省くと 2 倍の大きさで表示されてしまう。
    alt = html.escape(f"{fname} の実行結果。" + " / ".join(l.strip() for l in out), quote=True)
    lw, lh_ = size[0] // SCALE, size[1] // SCALE
    src_html = SRC.read_text(encoding="utf-8")
    pat = re.compile(r'<img src="images/' + re.escape(png.name) + r'"[^>]*>')
    new = (f'<img src="images/{png.name}" alt="{alt}" '
           f'width="{lw}" height="{lh_}" loading="lazy">')
    src_html, n = pat.subn(lambda m: new, src_html)
    SRC.write_text(src_html, encoding="utf-8")
    print(f"{png.name}  {size[0]}x{size[1]}px → 表示 {lw}x{lh_}  ({len(out)}行)  HTML更新={n}")
