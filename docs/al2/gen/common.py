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
    return f'      <div class="slide-hint"><span><strong>スライドに使えること:</strong> {text}</span></div>'


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
def slide_submission(week):
    """毎回の提出ガイド。提出物はスライド3枚とその提出だけ。"""
    n = int(week)
    return f"""
<!-- ============ SUBMISSION GUIDE ============ -->
<section id="sec-submission" style="padding-top:2rem;padding-bottom:0">
  <div class="container">
    <div class="submission-box">
      <h3>提出ガイド（今回の提出物: 解説スライド3枚）</h3>
      <div class="submission-items">
        <a class="sub-item" href="#sec-slides"><span class="sub-count">A</span><span class="tag tag-standard">しくみ</span>自分で作った図で説明する</a>
        <a class="sub-item" href="#sec-slides"><span class="sub-count">B</span><span class="tag tag-standard">動かした</span>自分の実行画面と読み取り</a>
        <a class="sub-item" href="#sec-slides"><span class="sub-count">C</span><span class="tag tag-standard">考えた</span>問いに自分の数値で答える</a>
      </div>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:8px;padding:0.8rem 1rem;margin-top:1rem;font-size:0.9rem;color:#93D500">
        <strong>提出方法:</strong> 自分のGoogleスライドに第{n}回の3枚を追加 →
        PDFに書き出してManabaに提出 → コメント欄にスライドの共有URLを貼る
      </div>
    </div>
  </div>
</section>"""


def slides_section(week, topic, figure_points, run_file, run_points, questions):
    """「解説スライドを3枚つくる」課題のセクションを組み立てる。

    week          : "05" のような回番号
    topic         : スライドの見出しにするテーマ名
    figure_points : スライドAの図に必ず入れる要素（3つ）
    run_file      : スライドBで動かすファイル名
    run_points    : スライドBで読み取ること（2つ）
    questions     : スライドCの問い（2つ）
    """
    n = int(week)
    fig_items = "\n".join(f"          <li>{t}</li>" for t in figure_points)
    run_items = "\n".join(f"          <li>{t}</li>" for t in run_points)
    q_items = "\n".join(f"        <li><strong>問い{i+1}:</strong> {t}</li>"
                        for i, t in enumerate(questions))
    body = f"""    <p style="margin-bottom:1.5rem">
      自分のGoogleスライドに、第{n}回ぶんの<strong>3枚</strong>を追加してください。
      見出しは「第{n}回: {topic}」にします。
      説明する相手は<strong>前期のアルゴリズム論及び演習Iを受けていない友達</strong>です。
      専門用語をそのまま書いても伝わりません。
    </p>

    <div class="card standard">
      <div class="card-header">
        <span class="tag tag-standard">スライドA</span>
        <h3>しくみを、自分で作った図で説明する</h3>
      </div>
      <p>次の3つが伝わる図を、<strong>自分で作って</strong>1枚に入れてください。</p>
      <div class="setup-step">
        <p class="step-title">図に必ず入れる3つ</p>
        <ol>
{fig_items}
        </ol>
      </div>
      <div class="note-warn">
        <strong>図の作り方:</strong> Googleスライドの「挿入 → 図形」で四角・丸・矢印を並べて作ります。
        紙に手描きして写真を撮り、貼りつけてもかまいません。
        <strong>授業ページの図をそのまま貼るのは不可</strong>です。自分で線を引いたものだけを認めます。
      </div>
      <p style="margin-top:1rem">図のほかに、<strong>1文だけ</strong>説明を書いてください。
      「{topic}とは、○○を○○する方法です」の形で、20〜40字におさめます。</p>
    </div>

    <div class="card standard">
      <div class="card-header">
        <span class="tag tag-standard">スライドB</span>
        <h3>自分で動かした結果をのせる</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li><code>{run_file}</code> を自分のパソコンで実行する</li>
          <li><strong>VS Codeのウィンドウごと</strong>スクリーンショットを撮る
              （左のエクスプローラーに <code>AL2/No{week}</code> のフォルダ名とファイル名が写っている状態）</li>
          <li>スクリーンショットをスライドに貼る</li>
          <li>実行結果から読み取れることを、<strong>数値を挙げて</strong>2つ書く</li>
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">読み取ること（この2つに答える）</p>
        <ul>
{run_items}
        </ul>
      </div>
      <div class="note-warn">
        <strong>スクリーンショットの撮り方:</strong>
        Windows は <strong>Windows キー ＋ Shift ＋ S</strong>、Mac は <strong>Shift ＋ Command ＋ 4</strong> のあと
        <strong>スペースキー</strong>を押してウィンドウをクリックします。
        画面の一部だけを切り取ったものは受けつけません。フォルダ名とファイル名が読める状態にしてください。
      </div>
    </div>

    <div class="card standard">
      <div class="card-header">
        <span class="tag tag-standard">スライドC</span>
        <h3>問いに、自分の数値を根拠にして答える</h3>
      </div>
      <p>次の2つの問いに答えてください。答えの中で、
      <strong>スライドBに貼った自分の実行結果の数値を必ず引用</strong>してください。</p>
      <ul class="point-list">
{q_items}
      </ul>
      <div class="note-warn">
        <strong>「〜が分かった」「うまくいった」だけでは点になりません。</strong>
        「自分の実行結果では○○が△△だった。だから□□と言える」の形で書いてください。
      </div>
    </div>"""
    return section("sec-slides", "3", f"課題: 解説スライドを3枚つくる", body)


def rubric_section(week):
    """評価の観点と、よくある不十分な例。学生に最初から見せる。"""
    n = int(week)
    body = f"""    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>提出のしかた</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">手順</p>
        <ol>
          <li>自分のGoogleスライドを開き、第{n}回の3枚（A・B・C）を追加する</li>
          <li><strong>ファイル → ダウンロード → PDFドキュメント</strong> でPDFに書き出す</li>
          <li>ManabaにPDFを提出する</li>
          <li>Manabaのコメント欄に、<strong>スライドの共有URL</strong>を貼る</li>
        </ol>
      </div>
      <div class="note-warn">
        <strong>共有URLも毎回必ず提出してください。</strong>
        Googleスライドには変更履歴が残ります。
        いつ・どのスライドを作ったかを確認するために使います。
        まとめて作ると履歴に残るので、毎回の授業の中で少しずつ進めてください。
      </div>
    </div>

    <div class="concept-box" style="margin-top:1.5rem">
      <h4>評価の観点（毎回同じ・10点満点）</h4>
      <table>
        <tr><th>観点</th><th>点</th><th>見るところ</th></tr>
        <tr><td>図を自分で作ったか</td><td>3</td><td>授業ページの図の貼りつけは0点。指定の3要素が図に入っているか</td></tr>
        <tr><td>自分で動かした証拠があるか</td><td>2</td><td>VS Codeのウィンドウごとのスクリーンショット。フォルダ名が読めるか</td></tr>
        <tr><td>数値を根拠にしているか</td><td>3</td><td>自分の実行結果の数値を引用しているか。数値と説明が合っているか</td></tr>
        <tr><td>言葉が自分のものか</td><td>2</td><td>専門用語をそのまま並べていないか。前期未履修の友達に伝わるか</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>よくある不十分な例</h4>
      <table>
        <tr><th>不十分な例</th><th>どう直すか</th></tr>
        <tr><td>授業ページの図をスクリーンショットして貼る</td><td>同じ内容でよいので、図形を自分で並べ直す。手描きの写真でもよい</td></tr>
        <tr><td>ターミナルの文字だけを切り取って貼る</td><td>VS Codeのウィンドウ全体を撮る。フォルダ名とファイル名が写るようにする</td></tr>
        <tr><td>「速いことが分かりました」で終わる</td><td>「自分の結果では6秒と0.01秒で、600倍ほど違った」と数値を書く</td></tr>
        <tr><td>教材の文をそのまま写す</td><td>専門用語を1つ選び、それを使わずに言いかえてみる</td></tr>
        <tr><td>3枚を最後の週にまとめて作る</td><td>変更履歴で分かります。毎回の授業中に作ってください</td></tr>
      </table>
    </div>"""
    return section("sec-submit", "4", "提出と評価", body, color="#FFB800")


def slides_for(week, data):
    """slides_data.SLIDES から、その回の課題セクションを組み立てる。"""
    d = data[week]
    return slides_section(week, d["topic"], d["figure"],
                          d["run_file"], d["run"], d["questions"])
