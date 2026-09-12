"""授業ページ本文（parts/sNN.html）を組み立てるための共通部品。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from pyhl import highlight   # noqa: E402
from build import SESSIONS   # noqa: E402


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


# ── Googleスライド課題のための共通部品 ──────────────────
def jp_date(text):
    """'2026-10-21' → '10月21日'"""
    _y, m, d = text.split("-")
    return f"{int(m)}月{int(d)}日"


RULES = [
    "自分で決めた数値で例題を動かし、その動きを図形で描く",
    "画像の貼り付けは不可（図形・矢印・テキストボックスで描く。クリックすると1つずつ選べる状態）",
    "図の中に自分の数値を入れる",
    "文章は1〜2行まで",
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
    """ページ上部の提出ガイド。標準課題（スライド1枚）と、その単元の発展課題。"""
    from slides_data import ADVANCED, advanced_of
    n = int(week)
    adv = advanced_of(week)
    items = ['        <a class="sub-item" href="#sec-slides"><span class="sub-count">標準</span>'
             '<span class="tag tag-standard">スライド1枚</span>自分の数値で動かして、図形で描く</a>']
    if adv:
        d = ADVANCED[adv]
        items.append(f'        <a class="sub-item" href="#sec-advanced"><span class="sub-count">発展</span>'
                     f'<span class="tag tag-advanced">作品{adv}</span>{d["title"]}'
                     f'（任意・第{int(d["due"])}回まで）</a>')
    else:
        items.append('        <a class="sub-item" href="#sec-advanced"><span class="sub-count">発展</span>'
                     '<span class="tag tag-advanced">作品づくり</span>全体の説明（第2回から始まります）</a>')
    return f"""
<!-- ============ SUBMISSION GUIDE ============ -->
<section id="sec-submission" style="padding-top:2rem;padding-bottom:0">
  <div class="container">
    <div class="submission-box">
      <h3>提出ガイド（今回の提出物: スライド1枚）</h3>
      <div class="submission-items">
{chr(10).join(items)}
      </div>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:8px;padding:0.8rem 1rem;margin-top:1rem;font-size:0.9rem;color:#93D500">
        <strong>提出方法:</strong> 自分のGoogleスライドに第{n}回の1枚を追加 →
        PDFに書き出してManabaに提出 → コメント欄にスライドの共有URLを貼る。
        締切は<strong>次回の授業が始まる時刻</strong>です。
      </div>
    </div>
  </div>
</section>"""


def slides_section(week, d):
    """標準課題「スライド1枚（図）をつくる」のセクション。"""
    n = int(week)
    el_items = "\n".join(f"          <li>{t}</li>" for t in d["elements"])
    body = f"""    <p style="margin-bottom:1.5rem">
      自分のGoogleスライドに、第{n}回ぶんの<strong>1枚</strong>を追加してください。
      見出しは「第{n}回: {d["topic"]}」にします。
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
        <h4>○（満点）になる条件</h4>
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
    return section("sec-slides", "3", "標準課題: スライド1枚（図）をつくる", body)


def slides_for(week, data):
    """slides_data.SLIDES から、その回の標準課題セクションを組み立てる。"""
    return slides_section(week, data[week])


def streamlit_card():
    """Streamlit の準備。発展課題のセクションに毎回入れる。"""
    return f"""    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">準備</span>
        <h3>Streamlit で画面のあるアプリを動かす</h3>
      </div>
      <p style="font-size:0.95rem">Streamlit（ストリームリット）は、Python のプログラムをそのままブラウザの画面にする道具です。
      HTML や JavaScript を書かずに、ボタン・入力欄・図が作れます。</p>
      <div class="setup-step">
        <p class="step-title">1. 1回だけ入れる</p>
        <p style="font-size:0.95rem">VS Code のターミナルで次を実行する（数分かかる）。</p>
{plain("Windows:  py -m pip install streamlit" + chr(10) + "Mac:      python3 -m pip install streamlit", "ターミナル")}
      </div>
      <div class="setup-step">
        <p class="step-title">2. いちばん小さいアプリを動かしてみる</p>
        <p style="font-size:0.95rem"><code>AL2/work</code> フォルダを作り、<code>app.py</code> という名前で保存する。</p>
{code("AL2-app-min.py", "Python ── app.py（Streamlit）")}
        <p style="font-size:0.95rem">ターミナルで <code>AL2/work</code> に移動してから、次を実行する。ブラウザが自動で開く。</p>
{plain("streamlit run app.py", "ターミナル")}
        <p style="font-size:0.9rem;color:#888">止めるときはターミナルで Ctrl+C。コードを直して保存すると、ブラウザの右上に「Rerun」が出るので押す。</p>
      </div>
    </div>"""


def advanced_section(week):
    """発展課題（任意・加点）のセクション。第1回は全体の説明、それ以外はその単元の作品。"""
    from slides_data import ADVANCED, advanced_of
    adv = advanced_of(week)
    overview_rows = "\n".join(
        f'        <tr><td>作品{k}</td><td>{d["title"]}</td><td>{d["algo"]}</td>'
        f'<td>第{int(d["weeks"][0])}〜{int(d["weeks"][-1])}回</td>'
        f'<td>第{int(d["due"])}回（{jp_date(SESSIONS[d["due"]][2])}）</td></tr>'
        for k, d in ADVANCED.items())
    overview = f"""    <p style="margin-bottom:1.5rem">
      発展課題は<strong>やらなくてもよい</strong>課題です。標準課題だけで70点に届きます。
      90点以上（S評価）をねらう人は、発展課題に取り組んでください。
      単元ごとに1作品、全部で4作品あります。
    </p>
    <div class="concept-box">
      <h4>4つの作品</h4>
      <table>
        <tr><th>作品</th><th>作るもの</th><th>使うアルゴリズム</th><th>取り組む回</th><th>締切</th></tr>
{overview_rows}
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">締切は、その回の授業が始まる時刻です。</p>
    </div>

    <div class="concept-box">
      <h4>ChatGPT などの AI を使ってかまいません</h4>
      <p style="font-size:0.95rem">
        発展課題では AI を使ってよいことにします。ただし、次の5つの要件を<strong>全部</strong>満たしたものだけを作品として受けつけます。
        AI に1回頼んだだけでは5つはそろいません。動かして・直して・聞き直す、をくり返してください。
      </p>
      <table>
        <tr><th>#</th><th>要件</th><th>確かめ方</th></tr>
        <tr><td>1</td><td><strong>自分のデータ</strong>が入っている</td><td>画面に、自分で決めた駅名・迷路・座標が出ている</td></tr>
        <tr><td>2</td><td><strong>画面で入力を変えられる</strong></td><td>ボタン・入力欄・スライダーのどれかがあり、変えると結果が変わる</td></tr>
        <tr><td>3</td><td><strong>結果が図で表示される</strong></td><td>経路が線で描かれる、訪問順に色が付く、など。文字だけは不可</td></tr>
        <tr><td>4</td><td><strong>変な入力で落ちない</strong></td><td>空・範囲の外・行き止まりを入れても、エラー画面ではなく説明の文が出る</td></tr>
        <tr><td>5</td><td><strong>授業の例題と同じ答えになる</strong></td><td>標準課題で使った自分の数値を入れると、例題の出力と一致する</td></tr>
      </table>
    </div>"""

    if adv is None:
        body = overview + f"""

    <div class="concept-box">
      <h4>提出するもの（作品ごと）</h4>
      <table>
        <tr><th>もの</th><th>中身</th></tr>
        <tr><td><code>app.py</code></td><td>Streamlit で動くプログラム。ManabaにPDFといっしょに添付する</td></tr>
        <tr><td>スライド1枚</td><td>①アプリの画面のスクリーンショット ②<strong>アルゴリズムがアプリのどこで働くか</strong>を図形で描いた図 ③例題と同じ答えになった証拠（2つの数値を並べる）</td></tr>
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        スライドの約束は標準課題と同じです（図形で描く・自分の数値を入れる・文章は1〜2行）。</p>
    </div>"""
        return section("sec-advanced", "4", "発展課題（任意・加点）: 学んだアルゴリズムでアプリをつくる",
                       body, color="#FFB800")

    d = ADVANCED[adv]
    screen = "\n".join(f"          <li>{t}</li>" for t in d["screen"])
    due = f'第{int(d["due"])}回（{jp_date(SESSIONS[d["due"]][2])}）の授業が始まる時刻'
    first = week == d["weeks"][0]
    body = f"""    <p style="margin-bottom:1.5rem">
      発展課題は<strong>やらなくてもよい</strong>課題です。標準課題だけで70点に届きます。
      90点以上（S評価）をねらう人は取り組んでください。
      いまの単元の作品は<strong>作品{adv}「{d["title"]}」</strong>、締切は{due}です。
    </p>

    <div class="card advanced">
      <div class="card-header">
        <span class="tag tag-advanced">作品{adv}</span>
        <h3>{d["title"]}</h3>
      </div>
      <table>
        <tr><th>使うアルゴリズム</th><td>{d["algo"]}</td></tr>
        <tr><th>自分のデータ</th><td>{d["data"]}</td></tr>
        <tr><th>締切</th><td>{due}</td></tr>
      </table>
      <div class="setup-step" style="margin-top:1rem">
        <p class="step-title">画面でできること（この3つを入れる）</p>
        <ol>
{screen}
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">例題との答え合わせ</p>
        <p style="font-size:0.95rem">{d["match"]}。一致した2つの数値をスライドに並べて書く。</p>
      </div>
    </div>

    <div class="concept-box">
      <h4>ChatGPT などの AI を使ってかまいません</h4>
      <p style="font-size:0.95rem">
        ただし、次の5つの要件を<strong>全部</strong>満たしたものだけを作品として受けつけます。
        AI に1回頼んだだけでは5つはそろいません。動かして・直して・聞き直す、をくり返してください。
      </p>
      <table>
        <tr><th>#</th><th>要件</th><th>確かめ方</th></tr>
        <tr><td>1</td><td><strong>自分のデータ</strong>が入っている</td><td>画面に、自分で決めた駅名・迷路・座標が出ている</td></tr>
        <tr><td>2</td><td><strong>画面で入力を変えられる</strong></td><td>ボタン・入力欄・スライダーのどれかがあり、変えると結果が変わる</td></tr>
        <tr><td>3</td><td><strong>結果が図で表示される</strong></td><td>経路が線で描かれる、訪問順に色が付く、など。文字だけは不可</td></tr>
        <tr><td>4</td><td><strong>変な入力で落ちない</strong></td><td>空・範囲の外・行き止まりを入れても、エラー画面ではなく説明の文が出る</td></tr>
        <tr><td>5</td><td><strong>授業の例題と同じ答えになる</strong></td><td>標準課題で使った自分の数値を入れると、例題の出力と一致する</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>AI への頼み方（往復のしかた）</h4>
      <table>
        <tr><th>順番</th><th>頼むこと</th><th>自分で確かめること</th></tr>
        <tr><td>1</td><td>「Streamlit で{d["title"].replace("アプリ", "")}を表示するだけの最小のアプリ」を頼む</td><td><code>streamlit run app.py</code> で画面が出るか</td></tr>
        <tr><td>2</td><td>自分のデータに差し替えてもらう（データはこちらから貼る）</td><td>画面に自分の駅名・迷路・座標が出ているか</td></tr>
        <tr><td>3</td><td>{d["algo"].split("（")[0]}を入れて、結果を図で描いてもらう</td><td>例題に同じデータを入れた答えと一致するか（要件5）</td></tr>
        <tr><td>4</td><td>エラーが出たら、<strong>赤い文字を全部</strong>貼って聞く</td><td>直ったあと、前にできていたことが壊れていないか</td></tr>
        <tr><td>5</td><td>空・範囲の外・行き止まりを入れたときの動きを直してもらう</td><td>3つとも、エラー画面でなく説明の文が出るか（要件4）</td></tr>
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        最後に、コードの中で<strong>アルゴリズムが働いている部分</strong>を自分で探し、それがアプリのどこで使われているかを図形で描きます（スライドに必要）。</p>
    </div>

{streamlit_card() if first else ""}

    <div class="concept-box">
      <h4>提出するもの</h4>
      <table>
        <tr><th>もの</th><th>中身</th></tr>
        <tr><td><code>app.py</code></td><td>Streamlit で動くプログラム。ManabaにPDFといっしょに添付する</td></tr>
        <tr><td>スライド1枚</td><td>①アプリの画面のスクリーンショット ②<strong>アルゴリズムがアプリのどこで働くか</strong>を図形で描いた図 ③例題と同じ答えになった証拠（2つの数値を並べる）</td></tr>
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        スライドの約束は標準課題と同じです（図形で描く・自分の数値を入れる・文章は1〜2行）。
        {"" if first else "Streamlit の入れ方と最小のアプリは、作品" + adv + "の最初の回（第" + str(int(d["weeks"][0])) + "回）のページにあります。"}</p>
    </div>"""
    return section("sec-advanced", "4", f"発展課題（任意・加点）: 作品{adv}「{d['title']}」",
                   body, color="#FFB800")


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
          <li>自分のGoogleスライドを開き、第{n}回の1枚を追加する</li>
          <li><strong>ファイル → ダウンロード → PDFドキュメント</strong> でPDFに書き出す</li>
          <li>ManabaにPDFを提出する</li>
          <li>Manabaのコメント欄に、<strong>スライドの共有URL</strong>を貼る</li>
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">発展課題（作品ができた回）</p>
        <ol>
          <li>作品のスライド1枚を、その回の標準課題の次に追加する</li>
          <li>PDFといっしょに <code>app.py</code> をManabaに添付する</li>
        </ol>
      </div>
      <div class="note-warn">
        <strong>共有URLも毎回必ず提出してください。</strong>
        Googleスライドには変更履歴が残ります。いつ・どのスライドを作ったかを確認するために使います。
      </div>
    </div>

    <div class="concept-box" style="margin-top:1.5rem">
      <h4>配点（15回共通）</h4>
      <table>
        <tr><th>課題</th><th>点</th><th>条件</th></tr>
        <tr><td rowspan="3">標準課題（毎回）</td><td>○ 5点</td><td>締切までに提出し、「○になる条件」を満たしている</td></tr>
        <tr><td>△ 2点</td><td>締切までに提出したが、条件を満たしていない（数値が合わない・画像の貼り付け・自分の数値がない）。締切後の提出も△まで</td></tr>
        <tr><td>0点</td><td>未提出、または次回の授業日以降の提出</td></tr>
        <tr><td>発展課題（作品ごと）</td><td>10点</td><td>5つの要件をすべて満たす（1つ2点）。締切後は受けつけない</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        標準課題は15回で最大 <strong>70点</strong>（5点×15回＝75点を70点で打ち切り。1回ぶんの余裕があります）。
        発展課題は4作品で最大40点。合計は<strong>100点で打ち切り</strong>です。
      </p>
      <table style="margin-top:0.8rem">
        <tr><th>ねらう評価</th><th>必要なこと</th></tr>
        <tr><td>70点以上</td><td>標準課題を毎回○にする。これだけで届く</td></tr>
        <tr><td>90点以上（S評価）</td><td>標準課題を毎回○にしたうえで、発展課題を<strong>2作品以上</strong>仕上げる</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>△になる例</h4>
      <table>
        <tr><th>△になる例</th><th>どう直すか</th></tr>
        <tr><td>授業ページの図やAIの画像を貼る</td><td>同じ内容でよいので、図形を自分で並べて描く</td></tr>
        <tr><td>例題の数値のまま描いている</td><td>自分の数値に書き換えて実行し直し、図の数値も差し替える</td></tr>
        <tr><td>図の数値と実行結果が合っていない</td><td>実行結果を横に置いて、1つずつ見比べる</td></tr>
        <tr><td>文章が3行以上ある</td><td>図で伝え、文章は「自分の数値では○○が△△になった」の1〜2行にする</td></tr>
        <tr><td>何回ぶんかを最後にまとめて作る</td><td>変更履歴で分かります。締切後の提出は△までです</td></tr>
      </table>
    </div>"""
    return section("sec-submit", "5", "提出と評価", body, color="#FFB800")
