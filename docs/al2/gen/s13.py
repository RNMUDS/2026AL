# -*- coding: utf-8 -*-
"""第13回: 実践的課題（1）設計と実装 の本文を組み立てる。"""
from slides_data import SLIDES
from slide_examples import slide_example
from common import (slide_submission, slides_for, rubric_section, advanced_section, blank_answers, code_pair,
                    AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)


# ────────────────────────────────────────────────────────────
# 図1: 作品づくりの4ステップ
# ────────────────────────────────────────────────────────────
def fig_cycle():
    steps = [("① 設計", "何を作るかを紙に書く", "テーマ・入力・出力・使うアルゴリズム", GREEN),
             ("② 実装", "動く最小版をまず作る", "完成をめざさず、まず動かす", GREEN),
             ("③ テスト", "わざと変な入力を試す", "空・0・大きすぎる値・想定外の順番", AMBER),
             ("④ 修正", "見つけた問題を直す", "直したら②へ戻る", AMBER)]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '作品づくりの4ステップ（②〜④はくり返す）</text>']
    for i, (title, line1, line2, color) in enumerate(steps):
        x = 20 + i * 168
        s.append(f'        <rect x="{x}" y="52" width="150" height="118" rx="12" fill="#141414" stroke="#444" stroke-width="1.5"/>')
        s.append(f'        <text x="{x+75}" y="80" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{title}</text>')
        s.append(f'        <text x="{x+75}" y="106" text-anchor="middle" fill="#E0E0E0" font-size="11">{line1}</text>')
        for j, part in enumerate([line2[:16], line2[16:]]):
            if part:
                s.append(f'        <text x="{x+75}" y="{130+j*16}" text-anchor="middle" fill="{GRAY}" font-size="10">{part}</text>')
        a, b = i / 4, (i + 1) / 4
        s.append(f'        <rect x="{x-3}" y="49" width="156" height="124" rx="14" fill="none" stroke="{color}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
        if i < 3:
            s.append(f'        <text x="{x+159}" y="116" text-anchor="middle" fill="#666" font-size="16">▶</text>')
    s.append(f'        <path d="M 654 178 L 654 198 L 264 198 L 264 178" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    s.append(f'        <polygon points="264,178 259,188 269,188" fill="{AMBER}"/>')
    s.append(f'        <text x="459" y="216" text-anchor="middle" fill="{AMBER}" font-size="11" font-weight="700">直したら、もう一度テストする</text>')
    s.append(f'        <text x="350" y="244" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '第13回で①と②、第14回で③と④に取り組む</text>')
    return fig(700, 260, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 2つのテンプレート
# ────────────────────────────────────────────────────────────
def fig_templates():
    items = [
        ("テンプレートA", "コスト付き迷路ゲーム", ["プレイヤーが道を選ぶ", "最短の道と比べて採点", "ダイクストラ法を使う"], GREEN),
        ("テンプレートB", "配達ルート最適化", ["配達先を並べる", "貪欲法と全探索で比べる", "巡回セールスマン問題"], AMBER),
    ]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '作品の出発点にできる2つのテンプレート</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'どれか1つを選んで書き換えれば、自分の作品になる</text>']
    for i, (label, title, lines, color) in enumerate(items):
        x = 130 + i * 230
        s.append(f'        <rect x="{x}" y="62" width="212" height="152" rx="12" fill="#141414" stroke="{color}" stroke-width="1.8"/>')
        s.append(f'        <text x="{x+106}" y="86" text-anchor="middle" fill="{color}" font-size="11">{label}</text>')
        s.append(f'        <text x="{x+106}" y="110" text-anchor="middle" fill="#E0E0E0" font-size="13" font-weight="700">{title}</text>')
        for j, line in enumerate(lines):
            s.append(f'        <text x="{x+106}" y="{140+j*22}" text-anchor="middle" fill="#bbb" font-size="11">{line}</text>')
    s.append(f'        <text x="350" y="238" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'テンプレートを使わず、まったく新しい作品を作ってもよい</text>')
    return fig(700, 254, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 設計シート
# ────────────────────────────────────────────────────────────
def fig_sheet():
    rows = [("作品の名前", "沼をよけろ！コスト迷路", GREEN),
            ("どんな作品か", "プレイヤーが道を選び、最短の道と比べて採点する", "#ccc"),
            ("入力", "プレイヤーが選んだ道（D/R/U/L の文字列）", "#ccc"),
            ("出力", "プレイヤーの秒数・最短の秒数・スコア（100点満点）", "#ccc"),
            ("使うアルゴリズム", "ダイクストラ法（最短コスト経路を求める）", AMBER),
            ("なぜそれを使うか", "マスごとに通る時間が違うので、幅優先探索では求まらない", "#ccc"),
            ("作れたら足したいこと", "ステージを3つにする／制限時間を付ける", GRAY)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '設計シートの書き方（記入例）</text>']
    for i, (label, value, color) in enumerate(rows):
        y = 52 + i * 40
        s.append(f'        <rect x="24" y="{y}" width="652" height="34" rx="7" fill="{"#141414" if i%2==0 else "#101010"}" stroke="#282828"/>')
        s.append(f'        <text x="40" y="{y+22}" fill="{GREEN}" font-size="11" font-weight="700">{label}</text>')
        s.append(f'        <text x="220" y="{y+22}" fill="{color}" font-size="12">{value}</text>')
    s.append(f'        <text x="350" y="{52+7*40+22}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '「なぜそのアルゴリズムを使うか」がいちばん大切。作る前に言葉にしておく</text>')
    return fig(700, 52 + 7 * 40 + 40, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: フローチャートの書き方（テンプレートAの流れ）
# ────────────────────────────────────────────────────────────
def fig_flowchart():
    """処理は四角、判断はひし形、開始と終了は角丸。テンプレートAの流れを順に出す。"""
    dur = 12
    n = 8
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'フローチャートの書き方（テンプレートA「コスト付き迷路ゲーム」の流れ）</text>']
    # 左: 記号の説明
    legend = [("角丸", "開始・終了", "rect_r"), ("四角", "処理（計算・表示）", "rect"),
              ("ひし形", "判断（はい／いいえ）", "diamond"), ("矢印", "次に進む向き", "arrow")]
    for i, (name, mean, kind) in enumerate(legend):
        y = 60 + i * 52
        if kind == "rect_r":
            s.append(f'        <rect x="30" y="{y}" width="70" height="30" rx="15" fill="#141414" stroke="{GREEN}" stroke-width="1.5"/>')
        elif kind == "rect":
            s.append(f'        <rect x="30" y="{y}" width="70" height="30" fill="#141414" stroke="#888" stroke-width="1.5"/>')
        elif kind == "diamond":
            s.append(f'        <polygon points="65,{y-4} 100,{y+15} 65,{y+34} 30,{y+15}" fill="#141414" stroke="{AMBER}" stroke-width="1.5"/>')
        else:
            s.append(f'        <line x1="30" y1="{y+15}" x2="92" y2="{y+15}" stroke="#888" stroke-width="2"/>'
                     f'<polygon points="100,{y+15} 90,{y+10} 90,{y+20}" fill="#888"/>')
        s.append(f'        <text x="112" y="{y+13}" fill="#E0E0E0" font-size="11" font-weight="700">{name}</text>')
        s.append(f'        <text x="112" y="{y+27}" fill="{GRAY}" font-size="10">{mean}</text>')
    s.append(f'        <line x1="250" y1="48" x2="250" y2="{60+4*52+80}" stroke="#333" stroke-width="1"/>')

    # 右: テンプレートAの流れ
    cx = 470
    boxes = [
        ("start", 52, "開始"),
        ("proc", 96, "迷路とプレイヤーの道を読む"),
        ("proc", 140, "道を座標の列に直す"),
        ("judge", 196, "道はゴールに着く？"),
        ("proc", 258, "ダイクストラ法で最短の秒数を求める"),
        ("proc", 302, "プレイヤーの秒数と比べてスコアを出す"),
        ("proc", 346, "2つの道とスコアを表示する"),
        ("end", 390, "終了"),
    ]
    for i, (kind, y, label) in enumerate(boxes):
        g = [f'        <g opacity="0">{reveal(i, n, dur)}']
        if kind in ("start", "end"):
            g.append(f'          <rect x="{cx-50}" y="{y}" width="100" height="30" rx="15" fill="#141414" stroke="{GREEN}" stroke-width="1.5"/>')
        elif kind == "proc":
            stroke = AMBER if "ダイクストラ" in label else "#888"
            g.append(f'          <rect x="{cx-120}" y="{y}" width="240" height="30" fill="#141414" stroke="{stroke}" stroke-width="{2 if stroke==AMBER else 1.5}"/>')
        else:
            g.append(f'          <polygon points="{cx},{y-10} {cx+120},{y+15} {cx},{y+40} {cx-120},{y+15}" fill="#141414" stroke="{AMBER}" stroke-width="1.5"/>')
        fill = AMBER if ("ダイクストラ" in label or kind == "judge") else "#E0E0E0"
        g.append(f'          <text x="{cx}" y="{y+19}" text-anchor="middle" fill="{fill}" font-size="11" font-weight="700">{label}</text>')
        if i < n - 1 and kind != "judge":
            ny = boxes[i+1][1]
            top = ny - 10 if boxes[i+1][0] == "judge" else ny
            g.append(f'          <line x1="{cx}" y1="{y+30}" x2="{cx}" y2="{top-2}" stroke="#888" stroke-width="2"/>'
                     f'<polygon points="{cx},{top} {cx-5},{top-8} {cx+5},{top-8}" fill="#888"/>')
        if kind == "judge":
            # はい: 下へ
            g.append(f'          <line x1="{cx}" y1="{y+40}" x2="{cx}" y2="{boxes[i+1][1]-2}" stroke="#888" stroke-width="2"/>'
                     f'<polygon points="{cx},{boxes[i+1][1]} {cx-5},{boxes[i+1][1]-8} {cx+5},{boxes[i+1][1]-8}" fill="#888"/>')
            g.append(f'          <text x="{cx+8}" y="{y+52}" fill="{GREEN}" font-size="10">はい</text>')
            # いいえ: 右へ出て「着かない」表示 → 終了へ
            g.append(f'          <line x1="{cx+120}" y1="{y+15}" x2="{cx+170}" y2="{y+15}" stroke="#888" stroke-width="2"/>')
            g.append(f'          <text x="{cx+128}" y="{y+8}" fill="{RED}" font-size="10">いいえ</text>')
            g.append(f'          <rect x="{cx+170}" y="{y}" width="60" height="30" fill="#141414" stroke="#888" stroke-width="1.5"/>')
            g.append(f'          <text x="{cx+200}" y="{y+13}" text-anchor="middle" fill="#E0E0E0" font-size="9">「着かない」</text>')
            g.append(f'          <text x="{cx+200}" y="{y+25}" text-anchor="middle" fill="#E0E0E0" font-size="9">と表示する</text>')
            ey = boxes[-1][1] + 15
            g.append(f'          <path d="M {cx+200} {y+30} L {cx+200} {ey} L {cx+52} {ey}" fill="none" stroke="#888" stroke-width="2"/>'
                     f'<polygon points="{cx+50},{ey} {cx+58},{ey-5} {cx+58},{ey+5}" fill="#888"/>')
        g.append('        </g>')
        s.extend(g)
    s.append(f'        <text x="350" y="446" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'アルゴリズムが働く箱（オレンジ）に印を付ける。ひし形は「はい」「いいえ」で行き先が分かれる</text>')
    return fig(700, 462, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "フローチャート #sec-explanation",
    "テンプレート #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("13")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第13回と第14回は、後期に作ってきたプログラムを<strong>「設計図」で読み、「テスト」で確かめる</strong>回です。
      第13回はフローチャート、第14回はテストを扱います。
      発展課題に取り組んでいる人は、作品4（自由テーマ）の設計と実装を進める回でもあります。
    </p>

    <div class="analogy">
      料理のレシピは「材料を切る → 炒める → 味を見る → 足りなければ塩を足す」のように、
      順番と分かれ道で書かれています。
      プログラムも同じで、<strong>処理の順番と、条件によって分かれる場所</strong>を絵にしたものがフローチャートです。
      コードを1行ずつ読むより、全体の流れがひと目で分かります。
    </div>

{fig_flowchart()}

    <div class="concept-box">
      <h4>フローチャートを描く手順</h4>
      <table>
        <tr><th>順番</th><th>やること</th><th>コードのどこを見るか</th></tr>
        <tr><td>1</td><td>「開始」と「終了」の角丸を、上と下に置く</td><td>─</td></tr>
        <tr><td>2</td><td>上から順に、処理の四角を置いて矢印でつなぐ</td><td>関数の呼び出しと <code>print</code>。1つの四角に1つの仕事</td></tr>
        <tr><td>3</td><td><code>if</code> のところにひし形を置き、「はい」「いいえ」の矢印を分ける</td><td><code>if</code> / <code>else</code></td></tr>
        <tr><td>4</td><td><code>for</code> や <code>while</code> は、下から上へ戻る矢印にする</td><td>くり返しの終わりから始めへ</td></tr>
        <tr><td>5</td><td>アルゴリズム（探索・最短経路・全探索）が働く四角に色を付ける</td><td>第2〜12回で学んだ関数</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        細かい行（変数を1つ用意する、など）は四角にしません。
        <strong>「何をしているか」を人に説明するときに言う単位</strong>で四角を作ります。
        テンプレートAなら、上の図のように8個ほどで足ります。
      </p>
    </div>

{fig_templates()}

    <div class="concept-box">
      <h4>標準課題では、2つのテンプレートのどちらか1つを使う</h4>
      <p style="font-size:0.95rem">
        2つとも、後期に学んだアルゴリズムを1つのプログラムにまとめたものです。
        自分の迷路や配達先に書き換えて動かし、その流れをフローチャートにします。
        どちらも「参考」（完成したコード）と「実践」（穴埋め）の2つで載せてあります。
      </p>
    </div>

    <div class="concept-box" style="border-color:#FFB800">
      <h4>発展課題（作品4・自由テーマ）に取り組む人へ</h4>
      <p style="font-size:0.95rem">
        自由テーマの作品は、いきなり完成品を作ろうとするとうまくいきません。
        次の4ステップでまわします。第13回で①と②、第14回で③と④です。
      </p>
    </div>

{fig_cycle()}

    <div class="concept-box">
      <h4>動く最小版とは</h4>
      <p style="font-size:0.95rem">
        「動く最小版」とは、<strong>やりたいことの中心だけができている状態</strong>のことです。
        たとえば迷路ゲームなら、次のものが最小版になります。
      </p>
      <table>
        <tr><th>最小版に入れるもの</th><th>あとで足すもの</th></tr>
        <tr><td>迷路が1つある</td><td>ステージが3つある</td></tr>
        <tr><td>プレイヤーの道を1つ受け取る</td><td>何度でも遊び直せる</td></tr>
        <tr><td>最短の道と比べて点数を出す</td><td>ランキングを保存する</td></tr>
        <tr><td>結果を文字で表示する</td><td>色を付けてきれいに表示する</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        最小版が動いてから足していけば、途中で止まっても「動くもの」が手元に残ります。
        AI に頼むときも、<strong>最初は最小版だけを頼み、動いてから1つずつ足す</strong>のがいちばん確実です。
      </p>
    </div>

    <div class="concept-box">
      <h4>テーマの決め方</h4>
      <p style="font-size:0.95rem">
        テーマが思いつかないときは、次の3つの問いから考えてみてください。
      </p>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li><strong>自分が毎日している「順番を決めること」は何か</strong>（買い物、部活の練習メニュー、朝の支度）</li>
        <li><strong>自分がよく遊ぶゲームの中に、最短や最適が出てくる場面はないか</strong>（敵の追いかけ方、アイテム集め）</li>
        <li><strong>身のまわりの地図で、時間や料金が違う道はないか</strong>（自宅から大学、キャンパス内の移動）</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        大きな作品である必要はありません。<strong>小さくても、動いて、アルゴリズムが役に立っていること</strong>が大切です。
        2つのテンプレートのどちらかを Gradio の画面に載せ替えるだけでも、作品4になります。
      </p>
    </div>

{fig_sheet()}"""

ex1_body = f"""      <p>プレイヤーが選んだ道と、ダイクストラ法が見つけた最短の道を比べて点数を付けるゲームです。
      <code>cost_map</code> と <code>player_moves</code> を書き換えれば、自分のステージが作れます。</p>

{code_pair('AL2-13-ex1.py')}

{run('a13_ex1_result.png', 'プレイヤーの道は14歩で<strong>42秒</strong>、最短の道は18歩で<strong>18秒</strong>でした。'
     'プレイヤーは歩数こそ少ないものの、9（沼）のマスを何度も通っているため時間がかかっています。'
     '最短の道は4歩よけいに歩くかわりに、沼を1つも通っていません。'
     'スコアは <code>最短 ÷ プレイヤー × 100</code> で計算しており、42点となりました。'
     '<code>player_moves</code> を書き換えて、100点を取れる道をさがしてみてください。')}"""

ex2_body = f"""      <p>配達先を並べると、貪欲法と全探索の両方でルートを作って比べるアプリです。
      <code>places</code> を書き換えれば、自分の配達先が作れます（8件までなら全探索が使えます）。</p>

{code_pair('AL2-13-ex2.py')}

{run('a13_ex2_result.png', '貪欲法は<strong>59.4</strong>、全探索は<strong>54.3</strong>で、貪欲法は9.3%長いという結果でした。'
     '作った時間を比べると、貪欲法は0.000005秒、全探索は0.000134秒です。'
     '6件の配達先なら全探索でも一瞬ですが、件数を増やすと全探索だけが急に遅くなります。'
     '<code>places</code> に配達先を足して、9件・10件と増やしたときの時間の変化を確かめてみてください。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">2つのテンプレートを実行してください。
    標準課題では、どちらか1つを自分の数値に書き換えて動かし、その流れをフローチャートにします。
    発展課題の自由テーマの出発点にも使えます。</p>

{setup_guide('13', ['AL2-13-ex1.py', 'AL2-13-ex2.py'])}

{keywords([
    ('動く最小版', 'うごくさいしょうばん / MVP', 'やりたいことの中心だけができている状態。まず最小版を動かしてから、少しずつ足していく。'),
    ('設計シート', 'せっけいシート', '作る前に「何を・どう作るか」を紙に書き出したもの。テーマ・入力・出力・使うアルゴリズムを書く。'),
    ('テンプレート', 'template', '書き換えて使うための下書き。ゼロから書くより速く、まちがいも少ない。'),
    ('入力の検査', 'にゅうりょくのけんさ / validation', '受け取った入力が正しい形かを調べること。まちがった入力をそのまま使うと、あとで止まる原因になる。'),
])}

{example(1, 'テンプレートA: コスト付き迷路ゲーム', ex1_body)}

{example(2, 'テンプレートB: 配達ルート最適化アプリ', ex2_body)}"""

ans = answers([slide_example("13"), blank_answers("13"),
    ("つまずいたときの調べ方", """        <p>テンプレートを自分の数値に書き換えたときに、よくあるつまずきと、その調べ方を挙げます。</p>
        <table>
          <tr><th>症状</th><th>まず見るところ</th></tr>
          <tr><td><code>IndexError: list index out of range</code></td><td>迷路の行の長さがそろっているか。すべての行を同じマス数にする</td></tr>
          <tr><td><code>KeyError</code></td><td>辞書にない名前を使っていないか。両方向とも書いたか（「新宿」側だけ書いていないか）</td></tr>
          <tr><td><code>TypeError</code></td><td>文字列と数を足していないか。<code>input()</code> の結果は文字列なので <code>int()</code> が要る</td></tr>
          <tr><td>答えがおかしい</td><td>途中に <code>print()</code> を入れて変数の中身を見る（第14回の例題2のやり方）</td></tr>
          <tr><td>ゴールに着かない</td><td>幅優先探索で全マスに届くか先に確かめる。壁で分断されていないか</td></tr>
        </table>
        <p style="margin-top:0.8rem">エラーが出たら、<strong>いちばん下の行</strong>から読んでください。
        その1つ上に、何行目で起きたかが書いてあります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "プログラムをフローチャートで読む", explanation),
    section("sec-examples", "2", "テンプレート", examples),
    slides_for("13", SLIDES),
    advanced_section("13"),
    rubric_section("13"),
    ans,
])

write("13", NAV, body)
