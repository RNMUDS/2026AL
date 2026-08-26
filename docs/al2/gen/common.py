"""授業ページ本文（parts/sNN.html）を組み立てるための共通部品。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from pyhl import highlight   # noqa: E402


def code(filename, label=None):
    """src/ に置いた Python ファイルを、色つきの <pre> ブロックに変換する。"""
    src = (HERE / "src" / filename).read_text(encoding="utf-8").rstrip("\n")
    label = label or ("Python ── " + filename)
    return f'<pre><span class="code-label">{label}</span>\n{highlight(src)}</pre>'


def plain(text, label):
    """Python 以外（ターミナル出力・フォルダ構成など）をそのまま <pre> に入れる。"""
    import html as H
    return f'<pre><span class="code-label">{label}</span>\n{H.escape(text.rstrip())}</pre>'


def run(img, note):
    """実行結果のキャプチャと、読み取り方の説明をまとめて出力する。"""
    return f"""      <p class="run-label">▶ 実行結果</p>
      <div class="run-capture">
        <img src="images/{img}">
      </div>
      <p class="run-note">{note}</p>"""


def card(tag_class, tag_label, title, body, border="example"):
    return f"""    <div class="card {border}">
      <div class="card-header">
        <span class="tag {tag_class}">{tag_label}</span>
        <h3>{title}</h3>
      </div>
{body}
    </div>"""


def example(n, title, body):
    return card("tag-example", f"例題 {n}", title, body, "example")


def standard(n, title, body):
    return card("tag-standard", f"標準課題 {n}", title, body, "standard")


def notion(text):
    return f'      <div class="notion-submit"><span><strong>Notionへの記録:</strong> {text}</span></div>'


def section(sid, num, title, body, color="#76B900"):
    return f"""
<section id="{sid}">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:{color}">{num}</div>
      <h2>{title}</h2>
    </div>
{body}
  </div>
</section>"""


def answers(items):
    """解答例セクション。items は (見出し, 本文HTML) の一覧。"""
    inner = "\n".join(
        f'      <div class="ans-item">\n        <h4>{h}</h4>\n{b}\n      </div>'
        for h, b in items)
    return f"""
<!-- ============ ANSWERS ============ -->
<section style="background:#0A0A0A" id="answers-section" data-release="{{{{RELEASE}}}}">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#616161">解</div>
      <h2>解答例</h2>
    </div>

    <div id="answers-content">
{inner}
    </div>

  </div>
</section>"""


def submission(items, count):
    rows = "\n".join(
        f'        <a class="sub-item" href="{href}"><span class="sub-count">1</span>'
        f'<span class="tag {cls}">{tag}</span>{text}</a>'
        for href, cls, tag, text in items)
    return f"""
<!-- ============ SUBMISSION GUIDE ============ -->
<section id="sec-submission" style="padding-top:2rem;padding-bottom:0">
  <div class="container">
    <div class="submission-box">
      <h3>提出ガイド（今回の提出物: 計{count}項目）</h3>
      <div class="submission-items">
{rows}
      </div>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:8px;padding:0.8rem 1rem;margin-top:1rem;font-size:0.9rem;color:#93D500">
        <strong>提出方法:</strong> 自分のNotionノートに回答を記録 → PDFにエクスポート → ManabaにPDFを提出
      </div>
    </div>
  </div>
</section>"""


def setup_guide(no, files):
    """VS Code でフォルダとファイルを用意する手順。no は "01" のような回番号。"""
    prev = f"No{int(no) - 1:02d}" if int(no) > 1 else None
    prev_line = (f'          &nbsp;&nbsp;&nbsp;&nbsp;├── {prev}/&nbsp;&nbsp;&nbsp;'
                 f'<span style="color:#555">← 前回のファイル</span><br>\n') if prev else ""
    filelist = ", ".join(f"<code>{f}</code>" for f in files)
    return f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>VS Code でフォルダとファイルを用意する</h3>
      </div>

      <div class="setup-step">
        <p class="step-title">Step 1: 作業フォルダを作る</p>
        <ol>
          <li>デスクトップに <strong>AL2</strong> という名前のフォルダを作る（後期の授業ではずっと同じフォルダを使う）</li>
          <li>AL2 フォルダの中に <strong>No{no}</strong> という名前のフォルダを作る</li>
        </ol>
        <div class="tree">
          デスクトップ/<br>
          └── AL2/<br>
{prev_line}          &nbsp;&nbsp;&nbsp;&nbsp;└── <span style="color:#76B900;font-weight:600">No{no}/</span>&nbsp;&nbsp;&nbsp;<span style="color:#76B900">← 第{int(no)}回はここに保存</span>
        </div>
      </div>

      <div class="setup-step">
        <p class="step-title">Step 2: VS Code でフォルダを開く</p>
        <ol>
          <li><strong>Visual Studio Code</strong> を起動する</li>
          <li>メニューから <strong>「ファイル」→「フォルダーを開く」</strong>を選ぶ</li>
          <li>Step 1 で作った <strong>AL2/No{no}</strong> フォルダを選んで開く</li>
        </ol>
        <p style="color:#888;font-size:0.85rem;margin-top:0.5rem">左側のエクスプローラーに No{no} フォルダの中身が表示される（最初は空）。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">Step 3: 例題ごとにファイルを作って実行する</p>
        <ol>
          <li>左側エクスプローラーの No{no} の横にある <strong>新しいファイルアイコン</strong>をクリック</li>
          <li>ファイル名を入力して Enter（例題1なら <code>{files[0]}</code>）</li>
          <li>例題のコードブロック右上の <strong>コピー</strong>ボタンをクリック</li>
          <li>VS Code の編集画面に <strong>貼り付ける</strong>（Ctrl+V / Cmd+V）</li>
          <li><strong>保存する</strong>（Ctrl+S / Cmd+S）</li>
          <li>右上の <strong>▷（再生ボタン）</strong>をクリックして実行する</li>
        </ol>
        <p style="color:#888;font-size:0.85rem;margin-top:0.5rem">今回作るファイル: {filelist}</p>
      </div>
    </div>"""


def keywords(rows):
    body = "\n".join(
        f'        <tr><td><strong style="color:#76B900">{term}</strong>'
        f'<br><span style="color:#888;font-size:0.8rem">{reading}</span></td>'
        f'<td>{desc}</td></tr>'
        for term, reading, desc in rows)
    return f"""    <div class="concept-box" style="margin-bottom:1.5rem">
      <h4>今回のキーワード</h4>
      <table>
        <tr><th>用語（読み方）</th><th>説明</th></tr>
{body}
      </table>
    </div>"""


def write(num, nav, body):
    nav_block = "<!--NAV\n" + "\n".join(nav) + "\n-->\n"
    out = HERE / "parts" / f"s{num}.html"
    out.write_text(nav_block + body, encoding="utf-8")
    print(f"wrote parts/s{num}.html ({out.stat().st_size:,} bytes)")


# ── 図を描くための共通部品 ────────────────────────────────
GREEN, AMBER, GRAY, RED, BLUE = "#76B900", "#FFB800", "#888888", "#FF5252", "#4FC3F7"


def fig(w, h, inner, dark=True):
    """SVG図を <div class="diagram-container"> で包んで返す。"""
    bg = ' style="background:#0A0A0A"' if dark else ""
    return (f'      <div class="diagram-container">\n'
            f'        <svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg"'
            f' font-family="Noto Sans JP, sans-serif"{bg}>\n{inner}\n        </svg>\n'
            f'      </div>')


def reveal(i, n, dur, hold=0.12):
    """i 番目の要素を順番に出す opacity アニメーション（出たあとは消えない）。"""
    a = (1 - hold) * i / n
    return (f'<animate attributeName="opacity" values="0;0;1;1" '
            f'keyTimes="0;{a:.3f};{min(a + 0.03, 0.999):.3f};1" dur="{dur}s" '
            f'repeatCount="indefinite" fill="freeze"/>')


def blink(a, b, dur):
    """割合 a〜b のあいだだけ表示するアニメーション。"""
    return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
            f'keyTimes="0;{a:.3f};{min(a+0.01,0.999):.3f};{max(b-0.01,a+0.02):.3f};{b:.3f};1" '
            f'dur="{dur}s" repeatCount="indefinite"/>')


def svg_text(x, y, text, fill="#E0E0E0", size=12, anchor="middle", weight=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'        <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'font-size="{size}"{w}{extra}>{text}</text>')
