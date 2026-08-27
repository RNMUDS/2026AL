# -*- coding: utf-8 -*-
"""第13回: 実践的課題（1）設計と実装 の本文を組み立てる。"""
from common import (AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)


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
    "課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "実行確認", "テンプレート3つを動かす"),
    ("#sec-standard", "tag-standard", "課題1", "設計シートを書く"),
    ("#sec-standard", "tag-standard", "課題2", "動く最小版を作る"),
    ("#sec-standard", "tag-standard", "課題2", "実行結果を記録する"),
], 4)

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

std1_body = """      <p>作りたい作品の<strong>設計シート</strong>をNotionに書きます。
      次の7項目をすべて埋めてください。書けない項目があれば、テーマを見直す合図です。</p>

      <table>
        <tr><th>項目</th><th>書くこと</th></tr>
        <tr><td>作品の名前</td><td>短くて分かりやすい名前</td></tr>
        <tr><td>どんな作品か</td><td>2〜3行で説明する</td></tr>
        <tr><td>入力</td><td>プログラムが受け取るもの（何を、どんな形で）</td></tr>
        <tr><td>出力</td><td>プログラムが表示するもの</td></tr>
        <tr><td>使うアルゴリズム</td><td>後期に学んだものから1つ以上</td></tr>
        <tr><td>なぜそれを使うか</td><td>ほかの方法ではだめな理由を書く</td></tr>
        <tr><td>作れたら足したいこと</td><td>2つ以上（最小版には入れない）</td></tr>
      </table>

      <div class="note-warn">
        <strong>いちばん大切な項目:</strong> 「なぜそのアルゴリズムを使うか」です。
        「重みに差があるからダイクストラ法」「順番を決める問題で都市が少ないから全探索」のように、
        <strong>第11回の3つの問い</strong>（どんな問題か／重みに差があるか／最適解が必要か）に沿って書いてください。
      </div>

      <p style="margin-top:1rem"><strong>テーマが決まらない場合:</strong>
      3つのテンプレートのどれかを選び、「ステージを自分で作る」「配達先を自分の町にする」など、
      中身を自分のものに置きかえるだけでもかまいません。
      その場合も、7項目すべてを自分の言葉で書いてください。</p>
"""

std2_body = """      <p>設計シートをもとに、<strong>動く最小版</strong>を作ります。
      第13回の時間内に完成しなくてもかまいません。<strong>動くところまで</strong>を提出してください。</p>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>テンプレートを1つ選んでコピーし、<code>AL2-13-work.py</code> という名前で保存する</li>
          <li>設計シートの「入力」と「出力」にあたる部分を、自分の作品に書き換える</li>
          <li>1か所書き換えるたびに<strong>実行して確かめる</strong>（まとめて書き換えない）</li>
          <li>動いたら、実行結果をコピーしてNotionに貼る</li>
          <li>まだできていないことを「残っていること」として書き出す</li>
        </ol>
      </div>

      <div class="note-warn">
        <strong>行きづまったときのコツ:</strong>
        <ul style="padding-left:1.2rem;margin-top:0.5rem;font-size:0.92rem;line-height:1.9">
          <li>エラーが出たら、<strong>いちばん下の行</strong>を読む。何行目で何が起きたかが書いてある</li>
          <li><code>print()</code> を途中に入れて、変数の中身を見る</li>
          <li>大きく書き換えず、動いていたところまで戻して、少しずつやり直す</li>
          <li>テンプレートのどの部分が何をしているか分からなくなったら、その行を消して実行してみる</li>
        </ul>
      </div>

      <p style="margin-top:1rem"><strong>Notionに書くこと:</strong></p>
      <ul class="point-list">
        <li>書き換えたコード（全部）</li>
        <li>実行結果（コピーして貼る）</li>
        <li>いま動いていること（3つ以上）</li>
        <li>まだ動いていないこと・残っていること（2つ以上）</li>
        <li>つまずいた点と、どう解決したか（解決していなければ、それも書く）</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">課題1と課題2に取り組み、解答をNotionに記録してください。
    第14回で仕上げるので、第13回では<strong>完成させなくてかまいません</strong>。</p>

{standard(1, '設計シートを書く', std1_body)}
{notion('7項目すべてを埋めた設計シート。とくに「なぜそのアルゴリズムを使うか」は3行以上で書く。')}

{standard(2, '動く最小版を作る', std2_body)}
{notion('書き換えたコード、実行結果、動いていること3つ以上、残っていること2つ以上、つまずいた点とその対応。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第13回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>テンプレートの実行確認</strong>: 3つのテンプレートを動かした結果（画面のコピーでよい）</li>
        <li><strong>課題1</strong>: 設計シート（7項目）</li>
        <li><strong>課題2</strong>: 書き換えたコードと実行結果</li>
        <li><strong>課題2</strong>: 動いていること・残っていること・つまずいた点</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
      <div class="note-warn" style="margin-top:1rem">
        <strong>第14回の準備:</strong> 作りかけの <code>AL2-13-work.py</code> は消さずに残してください。
        第14回では、そのファイルをテストして仕上げ、レポートにまとめます。
      </div>
    </div>"""

ans = answers([
    ("課題1: 設計シートの記入例", """        <p>正解が1つに決まる課題ではありません。次は、テンプレートAをもとにした記入例です。</p>
        <table>
          <tr><th>項目</th><th>記入例</th></tr>
          <tr><td>作品の名前</td><td>沼をよけろ！コスト迷路</td></tr>
          <tr><td>どんな作品か</td><td>マスごとに通る時間が違う迷路で、プレイヤーが道を選ぶ。選んだ道の合計時間と、コンピュータが求めた最短時間を比べて100点満点で採点する。ステージは3つ。</td></tr>
          <tr><td>入力</td><td>プレイヤーが選んだ道を、D（下）R（右）U（上）L（左）の文字列で受け取る。例: <code>"DDRRDR"</code></td></tr>
          <tr><td>出力</td><td>プレイヤーの合計秒数、最短の合計秒数、スコア（100点満点）、2つの道を書き込んだ迷路の絵</td></tr>
          <tr><td>使うアルゴリズム</td><td>ダイクストラ法</td></tr>
          <tr><td>なぜそれを使うか</td><td>マスごとに通り抜ける時間が1秒・5秒・9秒と違うので、重み付きグラフの最短経路問題になる。幅優先探索は歩数しか見ないため、沼を通る道を最短だと判断してしまう。重みが0以上なので、ダイクストラ法が使える。都市を回る問題ではないので、全探索や貪欲法は当てはまらない。</td></tr>
          <tr><td>作れたら足したいこと</td><td>①ステージを3つに増やす　②制限時間を付ける　③スコアをファイルに保存してランキングを出す</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>よくないシートの例と直し方:</strong></p>
        <ul class="point-list">
          <li><span style="color:#FF5252">「ダイクストラ法を使うから」</span>だけでは理由になりません。<strong>ほかの方法ではだめな理由</strong>を書いてください。</li>
          <li><span style="color:#FF5252">「入力: いろいろ」</span>のような書き方では、何を作ればよいか決まりません。<strong>形（文字列か、数か、リストか）</strong>まで書いてください。</li>
          <li><span style="color:#FF5252">「作れたら足したいこと」が空</span>の場合、最小版と完成版の区別ができていません。最小版を小さくするために、あとで足すものを先に分けておきます。</li>
        </ul>"""),
    ("課題2: 進め方のヒント", """        <p>コードそのものは人によって違うので、ここでは進め方の例を示します。</p>
        <p style="margin-top:0.6rem"><strong>テンプレートAを自分の作品にする手順の例:</strong></p>
        <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
          <li><code>AL2-13-ex1.py</code> をコピーして <code>AL2-13-work.py</code> という名前で保存し、まず<strong>そのまま実行</strong>する（動くことを確かめる）</li>
          <li><code>cost_map</code> を自分のステージに書き換えて実行する（迷路の絵が変わることを確かめる）</li>
          <li><code>player_moves</code> を書き換えて実行する（スコアが変わることを確かめる）</li>
          <li>「ステージを選べるようにする」など、足したいことを<strong>1つだけ</strong>足して実行する</li>
          <li>動いたら、また1つ足す</li>
        </ol>
        <p style="margin-top:0.8rem"><strong>「ステージを3つにする」を足す例:</strong></p>
<pre><span class="code-label">Python ── 書き足す部分</span>
<span class="cmt"># ステージを3つ用意する（リストのリストのリストになる）</span>
stages = [
    [[<span class="num">1</span>, <span class="num">1</span>, <span class="num">5</span>], [<span class="num">9</span>, <span class="num">1</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>]],
    [[<span class="num">1</span>, <span class="num">9</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">9</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>]],
    [[<span class="num">1</span>, <span class="num">5</span>, <span class="num">5</span>], [<span class="num">5</span>, <span class="num">1</span>, <span class="num">5</span>], [<span class="num">5</span>, <span class="num">5</span>, <span class="num">1</span>]],
]

stage_number = <span class="num">1</span>              <span class="cmt"># 1、2、3 のどれか</span>
cost_map = stages[stage_number - <span class="num">1</span>]</pre>
        <p style="margin-top:0.8rem"><strong>「動いていること」の書き方の例:</strong></p>
        <ul class="point-list">
          <li>自分で作った8×8のステージが表示される</li>
          <li>プレイヤーの道の合計秒数が正しく計算される</li>
          <li>最短の道がダイクストラ法で求まり、スコアが表示される</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>「残っていること」の書き方の例:</strong></p>
        <ul class="point-list">
          <li>ステージがまだ1つしかない（3つにしたい）</li>
          <li>道が迷路の外に出たときのメッセージが不親切</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>つまずいた点の書き方の例:</strong>
        「<code>IndexError: list index out of range</code> が出た。
        <code>cost_map</code> の行の長さがそろっていなかったことが原因だった。
        すべての行を8マスにそろえたら直った。」</p>
        <p style="margin-top:0.6rem">エラーの内容と原因と対応を書いておくと、第14回のレポートにそのまま使えます。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "作品づくりの進め方", explanation),
    section("sec-examples", "2", "テンプレートと部品", examples),
    section("sec-standard", "3", "課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("13", NAV, body)
