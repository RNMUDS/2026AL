# -*- coding: utf-8 -*-
"""第13回: 実践的課題（1）設計と実装 の本文を組み立てる。"""
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
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
# 図2: 3つのテンプレート
# ────────────────────────────────────────────────────────────
def fig_templates():
    items = [
        ("テンプレートA", "コスト付き迷路ゲーム", ["プレイヤーが道を選ぶ", "最短の道と比べて採点", "ダイクストラ法を使う"], GREEN),
        ("テンプレートB", "配達ルート最適化", ["配達先を並べる", "貪欲法と全探索で比べる", "巡回セールスマン問題"], AMBER),
        ("テンプレートC", "アイテム収集パズル", ["迷路のアイテムを集める", "拾う順番を決める", "幅優先探索＋全探索"], BLUE),
    ]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '作品の出発点にできる3つのテンプレート</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'どれか1つを選んで書き換えれば、自分の作品になる</text>']
    for i, (label, title, lines, color) in enumerate(items):
        x = 20 + i * 224
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
NAV = [
    "提出 #sec-submission",
    "進め方 #sec-explanation",
    "テンプレート #sec-examples",
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("13")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第13回と第14回は、<strong>自分でテーマを決めた作品づくり</strong>に取り組みます。
      第13回で設計と実装、第14回でテストと仕上げ、そしてレポート作成を行います。
      後期に学んだアルゴリズムを、少なくとも<strong>1つ</strong>は使ってください。
    </p>

    <div class="analogy">
      料理と同じで、いきなり完成品を作ろうとするとうまくいきません。
      まず「何を作るか」を決め、次に「とりあえず食べられる状態」まで作り、
      味見をして足りないものを足していきます。
      プログラムも同じで、<strong>まず動く最小版を作る</strong>ことがいちばん大切です。
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
        逆に全部いっぺんに作ろうとすると、最後まで1度も動かないまま時間切れになりがちです。
      </p>
    </div>

{fig_templates()}

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
      </p>
    </div>

{fig_sheet()}"""

ex1_body = f"""      <p>プレイヤーが選んだ道と、ダイクストラ法が見つけた最短の道を比べて点数を付けるゲームです。
      <code>cost_map</code> と <code>player_moves</code> を書き換えれば、自分のステージが作れます。</p>

{code('AL2-13-ex1.py')}

{run('a13_ex1_result.png', 'プレイヤーの道は14歩で<strong>42秒</strong>、最短の道は18歩で<strong>18秒</strong>でした。'
     'プレイヤーは歩数こそ少ないものの、9（沼）のマスを何度も通っているため時間がかかっています。'
     '最短の道は4歩よけいに歩くかわりに、沼を1つも通っていません。'
     'スコアは <code>最短 ÷ プレイヤー × 100</code> で計算しており、42点となりました。'
     '<code>player_moves</code> を書き換えて、100点を取れる道をさがしてみてください。')}"""

ex2_body = f"""      <p>配達先を並べると、貪欲法と全探索の両方でルートを作って比べるアプリです。
      <code>places</code> を書き換えれば、自分の配達先が作れます（8件までなら全探索が使えます）。</p>

{code('AL2-13-ex2.py')}

{run('a13_ex2_result.png', '貪欲法は<strong>59.4</strong>、全探索は<strong>54.3</strong>で、貪欲法は9.3%長いという結果でした。'
     '作った時間を比べると、貪欲法は0.000005秒、全探索は0.000134秒です。'
     '6件の配達先なら全探索でも一瞬ですが、件数を増やすと全探索だけが急に遅くなります。'
     '<code>places</code> に配達先を足して、9件・10件と増やしたときの時間の変化を確かめてみてください。')}"""

ex3_body = f"""      <p>迷路の中のアイテムを全部拾ってゴールへ向かうパズルです。
      幅優先探索で歩数の表を作ってから、貪欲法と全探索で拾う順番を決めます。
      <code>maze</code> と <code>items</code> を書き換えれば、自分のステージが作れます。</p>

{code('AL2-13-ex3.py')}

{run('a13_ex3_result.png', '貪欲法は<strong>60歩</strong>、全探索は<strong>30歩</strong>で、貪欲法はちょうど2倍かかっています。'
     '歩数の表を見ると、SからAが3歩、SからCも3歩と、どちらも近い場所にあります。'
     '貪欲法はAを先に選びましたが、最短ルートはCを先に拾っています。'
     'アイテムの位置を1つ動かすだけで差が大きく変わるので、'
     '<strong>「貪欲法でも十分なステージ」と「全探索が必要なステージ」を作り分けられます</strong>。'
     'なお、迷路を書き換えたときにゴールへ行けなくなると、エラーメッセージが出るようにしてあります。')}"""

ex4_body = f"""      <p>作品に組み込むための小さな道具を4つ集めました。
      必要な部分だけをコピーして使ってください。</p>

      <div class="note-warn">
        <strong>入力について:</strong> 授業ページに実行結果を載せるため、<code>USE_INPUT</code> を <code>False</code> にしてあります。
        自分の作品では <code>USE_INPUT = True</code> に書き換えると、キーボードから入力できるようになります。
      </div>

{code('AL2-13-ex4.py')}

{run('a13_ex4_result.png', '4つの部品が順に動きました。'
     '部品2では、用意した答え「DDRR」が数字でないため<strong>「数字を入力してください」と表示され、はじかれて</strong>います。'
     'まちがった入力をそのまま受け取ると、あとでプログラムが止まる原因になります。'
     '部品3では100万回の足し算が0.05秒ほどで終わりました。'
     '部品4では、スコアに応じて <code>#</code> の棒グラフと星の評価が表示されています。'
     '文字だけでも、見せ方をくふうすれば作品らしくなります。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">3つのテンプレートと部品集を実行してください。
    どれか1つを選んで書き換えると、自分の作品の出発点になります。</p>

{setup_guide('13', ['AL2-13-ex1.py', 'AL2-13-ex2.py', 'AL2-13-ex3.py', 'AL2-13-ex4.py'])}

{keywords([
    ('動く最小版', 'うごくさいしょうばん / MVP', 'やりたいことの中心だけができている状態。まず最小版を動かしてから、少しずつ足していく。'),
    ('設計シート', 'せっけいシート', '作る前に「何を・どう作るか」を紙に書き出したもの。テーマ・入力・出力・使うアルゴリズムを書く。'),
    ('テンプレート', 'template', '書き換えて使うための下書き。ゼロから書くより速く、まちがいも少ない。'),
    ('入力の検査', 'にゅうりょくのけんさ / validation', '受け取った入力が正しい形かを調べること。まちがった入力をそのまま使うと、あとで止まる原因になる。'),
])}

{example(1, 'テンプレートA: コスト付き迷路ゲーム', ex1_body)}

{example(2, 'テンプレートB: 配達ルート最適化アプリ', ex2_body)}

{example(3, 'テンプレートC: アイテム収集パズル', ex3_body)}

{example(4, '作品に使える部品集', ex4_body)}"""

ans = answers([
    ("つまずいたときの調べ方", """        <p>作品は人によって違うので、数値の正解はありません。
        よくあるつまずきと、その調べ方を挙げます。</p>
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
    section("sec-explanation", "1", "作品づくりの進め方", explanation),
    section("sec-examples", "2", "テンプレートと部品", examples),
    slides_for("13", SLIDES),
    rubric_section("13"),
    ans,
])

write("13", NAV, body)
