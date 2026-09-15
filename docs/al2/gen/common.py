"""授業ページ本文（parts/sNN.html）を組み立てるための共通部品。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from pyhl import highlight   # noqa: E402
from build import SESSIONS   # noqa: E402


def apply_blanks(src, items):
    """src の中の、items で指定された部分を ____ にして返す（行末に穴番号を付ける）。"""
    for i, b in enumerate(items, 1):
        pos = -1
        for _ in range(b["nth"] + 1):
            pos = src.index(b["find"], pos + 1)
        line_start = src.rfind("\n", 0, pos) + 1
        line_end = src.find("\n", pos)
        if line_end < 0:
            line_end = len(src)
        line = src[line_start:line_end]
        blanked = line.replace(b["answer"], "____", 1)
        if "#" in blanked:
            blanked = blanked.split("#")[0].rstrip()
        blanked = blanked + f"      # ← 穴{i}"
        src = src[:line_start] + blanked + src[line_end:]
    return src


def code(filename, label=None):
    """src/ に置いた Python ファイルを、色つきの <pre> ブロックに変換する。
    blanks.BLANKS に載っているファイルは、要になる行を ____ にして載せ、
    下にヒントと候補の表を付ける（答えは解答セクションに入る）。"""
    from blanks import BLANKS
    src = (HERE / "src" / filename).read_text(encoding="utf-8").rstrip("\n")
    label = label or ("Python ── " + filename)
    items = BLANKS.get(filename, [])
    src = apply_blanks(src, items)
    body = highlight(src).replace("____", '<span class="blank">____</span>')
    pre = f'<pre data-blanks="{len(items)}"><span class="code-label">{label}</span>\n{body}</pre>'
    if not items:
        return pre
    return pre + "\n" + blank_hints(filename, items)


def _choices(filename, i, b):
    """答えとまちがい2つを、ファイル名と穴番号で決まる順に並べる（毎回同じ順になる）。"""
    import random
    options = [b["answer"]] + list(b["wrong"])
    random.Random(f"{filename}-{i}").shuffle(options)
    return options


def blank_hints(filename, items):
    import html as H
    rows = []
    for i, b in enumerate(items, 1):
        choices = "<br>".join(f"{'ABC'[k]}. <code>{H.escape(c)}</code>" for k, c in enumerate(_choices(filename, i, b)))
        rows.append(f'        <tr><td style="white-space:nowrap"><strong>穴{i}</strong></td><td>{b["hint"]}</td>'
                    f'<td style="white-space:nowrap">{choices}</td></tr>')
    return f"""      <div class="concept-box" style="margin-top:0.8rem">
      <h4>穴埋め（____ を埋めてから実行する）</h4>
      <table>
        <tr><th>穴</th><th>ヒント</th><th>候補（1つが正解）</th></tr>
{chr(10).join(rows)}
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        埋めたら保存して実行し、下の実行結果と同じになるか見比べる。ちがえば、どの穴がちがうかを考えて直す。
        答えは次回の授業の時刻に、ページのいちばん下の「解答例」に出ます。</p>
    </div>"""


def blank_answers(week):
    """その回の穴埋めの答え一覧（解答セクション用）。"""
    import html as H
    from blanks import BLANKS
    rows = []
    for fname in sorted(BLANKS):
        if not fname.startswith(f"AL2-{week}-"):
            continue
        for i, b in enumerate(BLANKS[fname], 1):
            rows.append(f"          <tr><td><code>{fname}</code></td><td>穴{i}</td>"
                        f"<td><code>{H.escape(b['answer'])}</code></td></tr>")
    if not rows:
        return ("穴埋めの答え", "        <p>この回に穴埋めはありません。</p>")
    body = f"""        <table>
          <tr><th>ファイル</th><th>穴</th><th>答え</th></tr>
{chr(10).join(rows)}
        </table>"""
    return ("穴埋めの答え", body)


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
    return f'      <div class="slide-hint"><span><strong>図のヒント:</strong> {text}</span></div>'


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

      <div class="note-warn">
        <strong>例題2は穴埋めです。</strong>
        コードの中の <code>____</code>（穴）は、アルゴリズムの要になる部分です。
        コードの下の「ヒント」と「候補」を見て、<strong>自分で埋めてから</strong>実行してください。
        実行結果がページの画像と同じになれば正解です。ちがえば、どの穴がちがうかを考えて直します。
        例題1は完成したコードです。コメントを読みながら1行ずつ意味を追ってから実行してください。
      </div>
    </div>"""


def keywords(rows):
    body = "\n".join(
        f'        <tr><td><strong style="color:#76B900">{term}</strong></td>'
        f'<td>{desc}</td></tr>'
        for term, _reading, desc in rows)
    return f"""    <div class="concept-box" style="margin-bottom:1.5rem">
      <h4>今回のキーワード</h4>
      <table>
        <tr><th>用語</th><th>説明</th></tr>
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


# ── Googleスライド課題のための共通部品 ──────────────────
def jp_date(text):
    """'2026-10-21' → '10月21日'"""
    _y, m, d = text.split("-")
    return f"{int(m)}月{int(d)}日"


RULES = [
    "例題を自分で決めた数値で動かし、アルゴリズムの仕組みをコード上の変数や数値を用いて図形で説明する",
    "画像の貼り付けは不可（図形・矢印・テキストボックスで描く。クリックすると1つずつ選べる状態）",
    "図の中に自分の数値を入れる",
    "文章は1枚につき1〜2行まで",
]


def rules_box():
    items = "\n".join(f"          <li>{t}</li>" for t in RULES)
    return f"""      <div class="note-warn">
        <strong>毎回同じ4つの約束</strong>
        <ol style="margin:0.4rem 0 0 1.2rem;padding:0;line-height:1.9">
{items}
        </ol>
      </div>"""


def slide_submission(week):
    """ページ上部の提出ガイド。標準課題（70点）と発展課題（30点）。"""
    from slides_data import ADVANCED, advanced_of
    n = int(week)
    d = ADVANCED[advanced_of(week)]
    goal = d["milestones"][week]["goal"]
    label = d["title"] if d["algo"] == "─" else f'作品{advanced_of(week)} {d["title"]}'
    return f"""
<!-- ============ SUBMISSION GUIDE ============ -->
<section id="sec-submission" style="padding-top:2rem;padding-bottom:0">
  <div class="container">
    <div class="submission-box">
      <h3>提出ガイド（今回の提出物）</h3>
      <div class="submission-items">
        <a class="sub-item" href="#sec-slides"><span class="sub-count">70点</span><span class="tag tag-standard">標準課題</span>アルゴリズムの仕組みを、コード上の変数や数値を用いて図で説明する</a>
        <a class="sub-item" href="#sec-advanced"><span class="sub-count">30点</span><span class="tag tag-advanced">発展課題</span>{label} ─ 今回の到達点: {goal}</a>
      </div>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:8px;padding:0.8rem 1rem;margin-top:1rem;font-size:0.9rem;color:#93D500">
        <strong>提出方法:</strong> 第{n}回のGoogleスライドを新しく作る（発展課題をやった人は同じファイルに発展のスライドも入れる） →
        PDFに書き出してManabaに提出 → コメント欄にスライドの共有URLを貼る（発展課題は <code>app.py</code> も添付）。
        締切は<strong>次回の授業が始まる時刻</strong>です。
      </div>
    </div>
  </div>
</section>"""


def slides_section(week, d):
    """標準課題「アルゴリズムの仕組みを図で説明する」のセクション。"""
    n = int(week)
    el_items = "\n".join(f"          <li>{t}</li>" for t in d["elements"])
    body = f"""    <p style="margin-bottom:1.5rem">
      第{n}回のGoogleスライドを新しく作り、見出しを「第{n}回: {d["topic"]}」にしてください。
      その回のアルゴリズムの仕組みを、<strong>コード上の変数や自分で決めた数値を用いて図で説明</strong>します。
      枚数は自由です（1枚に収まらなければ分けてかまいません）。
    </p>

{rules_box()}

    <div class="card standard">
      <div class="card-header">
        <span class="tag tag-standard">標準課題</span>
        <h3>{d["topic"]}を図形で描く</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">1. 自分の数値を決めて、例題を動かす</p>
        <p style="font-size:0.95rem"><code>{d["run_file"]}</code> を開き、{d["own"]}
        保存して実行し、実行結果をそのまま残しておく（あとで図と見比べる）。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 実行結果を見ながら、図形で描く</p>
        <p style="font-size:0.95rem">{d["draw"]}</p>
        <p class="step-title" style="margin-top:0.8rem">図に必ず入れる3つ</p>
        <ol>
{el_items}
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">3. 文章を1〜2行だけ書く</p>
        <p style="font-size:0.95rem">図から分かることを、自分の数値を使って1〜2行で書く。
        「自分の数値では○○が△△になった」の形。</p>
      </div>
      <div class="concept-box" style="margin-top:1rem">
        <h4>課題要件（満点の条件）</h4>
        <p style="font-size:0.95rem;margin:0">{d["check"]}</p>
      </div>
    </div>

    <div class="concept-box">
      <h4>Googleスライドでの図の描き方</h4>
      <table>
        <tr><th>描きたいもの</th><th>やり方</th></tr>
        <tr><td>マス目・箱・丸</td><td><strong>挿入 → 図形 → 図形</strong> から四角や丸を置く。Ctrl+D（Mac は Command+D）で複製すると速い</td></tr>
        <tr><td>矢印・線</td><td><strong>挿入 → 線 → 矢印</strong>。図形の端にくっつけると、動かしてもついてくる</td></tr>
        <tr><td>数値・文字</td><td><strong>挿入 → テキストボックス</strong>。図形をダブルクリックして中に直接書いてもよい</td></tr>
        <tr><td>色分け</td><td>図形を選んで、ツールバーの<strong>塗りつぶしの色</strong>・<strong>枠線の色</strong></td></tr>
        <tr><td>木（枝分かれ）</td><td>上に1つ箱を置き、下の段に箱を並べて矢印でつなぐ。段ごとに横にそろえる</td></tr>
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        授業ページの図のスクリーンショット、AIが作った画像、手描きの写真は<strong>すべて不可</strong>です。
        図形で描いたものだけを受けつけます。
      </p>
    </div>"""
    return section("sec-slides", "3", "標準課題: アルゴリズムの仕組みを図で説明する", body)


def slides_for(week, data):
    """slides_data.SLIDES から、その回の標準課題セクションを組み立てる。"""
    return slides_section(week, data[week])


def gradio_card():
    """Gradio の準備。第1回の発展課題に入れる。"""
    return f"""    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">準備</span>
        <h3>Gradio で画面のあるアプリを動かす</h3>
      </div>
      <p style="font-size:0.95rem">Gradio（グラディオ）は、Python の関数に「入力欄・ボタン・図」の画面を付ける道具です。
      授業で作った関数を残したまま、外側に画面を付けられます。</p>
      <div class="setup-step">
        <p class="step-title">1. 1回だけ入れる</p>
        <p style="font-size:0.95rem">VS Code のターミナル（メニューの「ターミナル → 新しいターミナル」）で次を実行する。数分かかる。</p>
{plain("Windows:  py -m pip install gradio" + chr(10) + "Mac:      python3 -m pip install gradio", "ターミナル")}
      </div>
      <div class="setup-step">
        <p class="step-title">2. いちばん小さいアプリを動かしてみる</p>
        <p style="font-size:0.95rem"><code>AL2/work</code> フォルダを作り、<code>app.py</code> という名前で保存する。</p>
{code("AL2-app-min.py", "Python ── app.py（Gradio）")}
        <p style="font-size:0.95rem">例題と同じように、VS Code の右上の <strong>▷</strong> を押す。
        ターミナルに <code>Running on local URL: http://127.0.0.1:7860</code> と出て、ブラウザが自動で開く。
        名前を書き換え、スライダーを動かして「Submit」を押すと、結果の文が変わる。</p>
        <p style="font-size:0.9rem;color:#888">止めるときはターミナルで Ctrl+C。コードを直したら、止めてからもう一度 ▷ を押す。
        ブラウザが開かないときは、ターミナルに出た URL をブラウザに貼る。</p>
      </div>
    </div>"""


def milestone_card(week, num, d):
    """今回の到達点（30点）のカード。"""
    m = d["milestones"][week]
    must = "\n".join(f"          <li>{t}</li>" for t in m["must"])
    return f"""    <div class="card advanced">
      <div class="card-header">
        <span class="tag tag-advanced">今回の到達点（30点）</span>
        <h3>{m["goal"]}</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">満たすこと（3つとも必要）</p>
        <ol>
{must}
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">発展課題のスライドに貼るもの</p>
        <p style="font-size:0.95rem">{m["evidence"]}。文章は1〜2行まで。
        見出しは「第{int(week)}回 発展: {d["title"]}」にする。</p>
      </div>
      <div class="concept-box" style="margin-top:1rem">
        <h4>30点になる条件</h4>
        <p style="font-size:0.95rem;margin:0">3つをすべて満たし、<code>app.py</code> とスライドが締切までに提出されている。
        1つでも欠けていれば0点（部分点はありません）。</p>
      </div>
    </div>"""


def advanced_section(week):
    """発展課題（30点）のセクション。第1回は Gradio の準備、それ以外はその単元の作品の今回の到達点。"""
    from slides_data import ADVANCED, advanced_of
    num = advanced_of(week)
    d = ADVANCED[num]
    intro = """    <p style="margin-bottom:1.5rem">
      発展課題は<strong>やらなくてもよい</strong>課題です（標準課題だけで各回70点）。
      作り方の細かい説明はしません。
      到達点を満たすものを、自分で調べて作ってください。
    </p>"""

    if d["algo"] == "─":
        rows = "\n".join(
            f'        <tr><td>作品{k}</td><td>{v["title"]}</td><td>{v["algo"]}</td>'
            f'<td>第{int(v["weeks"][0])}〜{int(v["weeks"][-1])}回</td></tr>'
            for k, v in ADVANCED.items() if v["algo"] != "─")
        body = intro + f"""

    <div class="concept-box">
      <h4>4つの作品を、毎回の到達点に分けて育てる</h4>
      <table>
        <tr><th>作品</th><th>作るもの</th><th>使うアルゴリズム</th><th>取り組む回</th></tr>
{rows}
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        各回のページに「今回の到達点」が書いてあります。その回の到達点を満たせば30点です。
      </p>
    </div>

{milestone_card(week, num, d)}

{gradio_card()}"""
        return section("sec-advanced", "4", "発展課題（30点・任意）: Gradio の準備", body, color="#FFB800")

    screen = "\n".join(f"          <li>{t}</li>" for t in d["screen"])
    body = intro + f"""

    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">作品{num}</span>
        <h3>{d["title"]}（第{int(d["weeks"][0])}〜{int(d["weeks"][-1])}回で育てる）</h3>
      </div>
      <table>
        <tr><th>使うアルゴリズム</th><td>{d["algo"]}</td></tr>
        <tr><th>自分のデータ</th><td>{d["data"]}</td></tr>
        <tr><th>答え合わせ</th><td>{d["match"]}</td></tr>
      </table>
      <div class="setup-step" style="margin-top:1rem">
        <p class="step-title">完成したときに画面でできること</p>
        <ol>
{screen}
        </ol>
      </div>
    </div>

{milestone_card(week, num, d)}

    <p style="font-size:0.9rem;color:#888">
      Gradio の入れ方と最小のアプリは<a href="session01.html#sec-advanced" style="color:#FFB800">第1回のページ</a>にあります。</p>"""
    return section("sec-advanced", "4", f"発展課題（30点・任意）: 作品{num}「{d['title']}」", body, color="#FFB800")


def rubric_section(week):
    """提出のしかたと配点。学生に最初から見せる。"""
    n = int(week)
    body = f"""    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>提出のしかた</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">標準課題（毎回）</p>
        <ol>
          <li>第{n}回のGoogleスライドを新しく作る（ファイル名は「AL2 第{n}回 学籍番号 名前」）</li>
          <li><strong>ファイル → ダウンロード → PDFドキュメント</strong> でPDFに書き出す</li>
          <li>ManabaにPDFを提出する</li>
          <li>Manabaのコメント欄に、<strong>スライドの共有URL</strong>を貼る</li>
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">発展課題（やった回）</p>
        <ol>
          <li>発展課題のスライドを、その回の同じファイルの標準課題の次に入れる（PDFは1つにまとまる）</li>
          <li>PDFといっしょに <code>app.py</code> をManabaに添付する</li>
        </ol>
      </div>
      <div class="note-warn">
        <strong>共有URLも毎回必ず提出してください。</strong>
        図が図形で描かれているか（画像の貼り付けでないか）を確認するために使います。
      </div>
    </div>

    <div class="concept-box" style="margin-top:1.5rem">
      <h4>配点（毎回100点。成績は15回の平均）</h4>
      <table>
        <tr><th>課題</th><th>点</th><th>条件</th></tr>
        <tr><td>標準課題</td><td>70点</td><td>〆切までに提出し、課題要件を満たしている場合。遅れた場合や、要件を満たしていない場合は減点</td></tr>
        <tr><td rowspan="2">発展課題</td><td>30点</td><td>「今回の到達点」の3つをすべて満たし、<code>app.py</code> とスライドが締切までに提出されている</td></tr>
        <tr><td>0点</td><td>1つでも欠けている。部分点はありません</td></tr>
      </table>
      <table style="margin-top:0.8rem">
        <tr><th>ねらう評価</th><th>必要なこと</th></tr>
        <tr><td>70点以上</td><td>標準課題を毎回満点にする。これだけで届く</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>減点になる例</h4>
      <table>
        <tr><th>減点になる例</th><th>どう直すか</th></tr>
        <tr><td>授業ページの図やAIの画像を貼る</td><td>同じ内容でよいので、図形を自分で並べて描く</td></tr>
        <tr><td>例題の数値のまま描いている</td><td>自分の数値に書き換えて実行し直し、図の数値も差し替える</td></tr>
        <tr><td>図の数値と実行結果が合っていない</td><td>実行結果を横に置いて、1つずつ見比べる</td></tr>
        <tr><td>文章が3行以上ある</td><td>図で伝え、文章は「自分の数値では○○が△△になった」の1〜2行にする</td></tr>
      </table>
    </div>"""
    return section("sec-submit", "5", "提出と評価", body, color="#FFB800")
