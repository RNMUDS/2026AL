# -*- coding: utf-8 -*-
"""第14回: 実践的課題（2）仕上げとレポート作成 の本文を組み立てる。"""
from slides_data import SLIDES
from slide_examples import slide_example
from common import (slide_submission, slides_for, rubric_section, advanced_section, blank_answers, code_pair,
                    AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)


# ────────────────────────────────────────────────────────────
# 図1: テストの4つの観点
# ────────────────────────────────────────────────────────────
def fig_tests():
    items = [("空っぽ", "何も入力されなかったとき", "空の文字列、空のリスト、都市0個", GREEN),
             ("はしっこ", "ぎりぎりの値を入れたとき", "0、1、いちばん大きい値", GREEN),
             ("範囲の外", "ありえない値を入れたとき", "マイナス、迷路の外、大きすぎる数", AMBER),
             ("形がちがう", "想定と違う形のとき", "数字のかわりに文字、使えない記号", AMBER)]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '提出する前に必ず試す4種類の入力</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'バグの多くは「ふつうでない入力」で見つかる</text>']
    for i, (title, what, example_text, color) in enumerate(items):
        x = 20 + i * 168
        s.append(f'        <rect x="{x}" y="62" width="152" height="124" rx="12" fill="#141414" stroke="{color}" stroke-width="1.6"/>')
        s.append(f'        <text x="{x+76}" y="90" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{title}</text>')
        s.append(f'        <text x="{x+76}" y="116" text-anchor="middle" fill="#E0E0E0" font-size="11">{what[:12]}</text>')
        s.append(f'        <text x="{x+76}" y="132" text-anchor="middle" fill="#E0E0E0" font-size="11">{what[12:]}</text>')
        for j in range(0, len(example_text), 12):
            s.append(f'        <text x="{x+76}" y="{156+(j//12)*15}" text-anchor="middle" fill="{GRAY}" font-size="10">{example_text[j:j+12]}</text>')
        a, b = i / 4, (i + 1) / 4
        s.append(f'        <rect x="{x-3}" y="59" width="158" height="130" rx="14" fill="none" stroke="{AMBER}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="350" y="212" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '「エラーで止まらない」だけでなく「理由を教えてくれる」ところまで直す</text>')
    return fig(700, 228, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: print デバッグの流れ
# ────────────────────────────────────────────────────────────
def fig_debug():
    steps = [("① 変だと気づく", "答えがおかしい／エラーで止まる", GREEN),
             ("② あたりを付ける", "どのあたりの行が怪しいか考える", GREEN),
             ("③ print を入れる", "変数の中身をその場で表示する", AMBER),
             ("④ 見比べる", "自分の思っている値と実際の値を比べる", AMBER),
             ("⑤ 直して print を消す", "原因が分かったら直し、print は消す", GREEN)]
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'print デバッグの5ステップ</text>']
    for i, (title, note, color) in enumerate(steps):
        y = 54 + i * 46
        s.append(f'        <rect x="60" y="{y}" width="580" height="38" rx="9" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="80" y="{y+25}" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        s.append(f'        <text x="300" y="{y+25}" fill="#ccc" font-size="11">{note}</text>')
        a, b = i / 5, (i + 1) / 5
        s.append(f'        <rect x="57" y="{y-3}" width="586" height="44" rx="11" fill="none" stroke="{AMBER}" stroke-width="2.5" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
        if i < 4:
            s.append(f'        <text x="350" y="{y+48}" text-anchor="middle" fill="#555" font-size="12">▼</text>')
    s.append(f'        <text x="350" y="{54+5*46+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'エラーの文は、いちばん下の行から読む。何行目で何が起きたかが書いてある</text>')
    return fig(700, 54 + 5 * 46 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: レポートの構成
# ────────────────────────────────────────────────────────────
def fig_report():
    rows = [("1. 作品の名前と概要", "何を作ったかを3行で", "沼をよけろ！コスト迷路。プレイヤーが道を選び…"),
            ("2. 使ったアルゴリズム", "名前と、なぜ選んだか", "ダイクストラ法。マスごとに時間が違うため…"),
            ("3. 動かし方", "実行手順と入力の例", "app.py を ▷ で実行し、道を入力…"),
            ("4. 実行結果", "画面のコピーと、読み取れること", "図1のとおり、プレイヤー42秒・最短18秒…"),
            ("5. 調べたこと", "表と図で数値を示す", "表1のとおり、ステージを大きくすると…"),
            ("6. 苦労した点", "つまずきと、どう解決したか", "IndexError が出た。行の長さがそろって…"),
            ("7. これからやりたいこと", "足せなかった機能", "ステージを3つに増やしたい…")]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '作品を人に説明するときの7つの見出し（発展課題の作品スライドの材料）</text>']
    for i, (title, what, sample) in enumerate(rows):
        y = 48 + i * 44
        s.append(f'        <rect x="24" y="{y}" width="652" height="38" rx="8" fill="{"#141414" if i%2==0 else "#101010"}" stroke="#282828"/>')
        s.append(f'        <text x="40" y="{y+17}" fill="{GREEN}" font-size="12" font-weight="700">{title}</text>')
        s.append(f'        <text x="40" y="{y+33}" fill="{GRAY}" font-size="10">{what}</text>')
        s.append(f'        <text x="290" y="{y+25}" fill="#bbb" font-size="11">{sample}</text>')
    s.append(f'        <text x="350" y="{48+7*44+22}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '「動きました」だけでは足りない。数値と、そこから読み取れることを書く</text>')
    return fig(700, 48 + 7 * 44 + 40, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "テストと仕上げ #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("14")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第14回は、プログラムを<strong>テストで確かめる</strong>回です。
      プログラムは、正しい入力で動くだけでは完成ではありません。
      <strong>変な入力を与えても止まらないようにする</strong>ことが、いちばん大切な仕上げです。
      発展課題に取り組んでいる人は、作品4を仕上げる回でもあります（発展課題の要件4「変な入力で落ちない」はここで学ぶ内容です）。
    </p>

    <div class="analogy">
      料理を人に出す前に、味見をして、熱すぎないか確かめ、盛り付けを整えます。
      プログラムも同じで、自分だけが正しく使えるものは「まだ完成していない」状態です。
      作った本人は正しい入力しか試しませんが、ほかの人は思いもよらない使い方をします。
    </div>

{fig_tests()}

    <div class="concept-box">
      <h4>テストの書き方</h4>
      <p style="font-size:0.95rem">
        テストとは、<strong>わざと特別な入力を与えて、正しく動くか確かめる作業</strong>のことです。
        頭の中でやるのではなく、実際に動かして結果を記録します。
      </p>
      <table>
        <tr><th>試すこと</th><th>期待する動き</th></tr>
        <tr><td>空の入力（何も入れない）</td><td>エラーで止まらず、「入力してください」と伝える</td></tr>
        <tr><td>いちばん小さい値・大きい値</td><td>正しく計算できる</td></tr>
        <tr><td>ありえない値（マイナス、範囲外）</td><td>受けつけず、理由を伝える</td></tr>
        <tr><td>形が違う入力（数字のはずが文字）</td><td>受けつけず、理由を伝える</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        標準課題では、<strong>この表の4行それぞれについて自分で入力を決め、実際に試した結果</strong>を図にします。
      </p>
    </div>

{fig_debug()}

    <div class="concept-box">
      <h4>エラーの読み方</h4>
      <p style="font-size:0.95rem">
        エラーが出たときは、<strong>いちばん下の行</strong>から読みます。
        エラーの名前と、何が起きたかが書いてあります。
      </p>
      <table>
        <tr><th>エラーの名前</th><th>意味</th><th>よくある原因</th></tr>
        <tr><td><code>IndexError</code></td><td>リストの範囲外を見た</td><td>迷路の外のマスを見ようとした</td></tr>
        <tr><td><code>KeyError</code></td><td>辞書にない鍵を使った</td><td>存在しない駅名や地点名を書いた</td></tr>
        <tr><td><code>TypeError</code></td><td>型が合わない</td><td>文字列と数を足そうとした</td></tr>
        <tr><td><code>ValueError</code></td><td>値の形が合わない</td><td><code>int("abc")</code> のように変換できない</td></tr>
        <tr><td><code>ZeroDivisionError</code></td><td>0で割った</td><td>0件のときに平均を計算した</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        エラーの1つ上の行には、<strong>何行目で起きたか</strong>が書いてあります。その行から読み始めてください。
      </p>
    </div>

{fig_report()}"""

ex1_body = f"""      <p>第13回のテンプレートAで「プレイヤーの道を受け取る部分」に対し、
      6種類の入力を与えてテストします。バグのある関数と修正版を並べて比べます。</p>

{code_pair('AL2-14-ex1.py')}

{run('a14_ex1_result.png', 'バグのある関数では、「迷路の外に出る道」と「行ったり戻ったりする道」が'
     '<strong>迷路の外のマスを指したまま</strong>返ってきています。'
     'このあと <code>cost_map[r][c]</code> を計算するとエラーで止まります。'
     'また「使えない文字が入った道」では、<code>X</code> が無視されて別の場所に着いてしまいました。'
     '修正版は、6種類すべてに対してエラーで止まらず、'
     '受けつけない場合は<strong>理由を文章で返して</strong>います。'
     '「行ったり戻ったりする道」は、ルールの上では正しい道なので受けつけている点にも注目してください。')}

{notion('例題1の実行結果から、6種類の入力それぞれについて「バグのある関数の結果」と「修正版の結果」を表にまとめる。'
        'あわせて、修正版が「行ったり戻ったりする道」を受けつけている理由を説明する。')}"""

ex2_body = f"""      <p>バグをしこんだ貪欲法の関数を、<code>print</code> を入れて追いかけます。
      どの行で判断がおかしくなっているかを、目で見て確かめます。</p>

{code_pair('AL2-14-ex2.py')}

{run('a14_ex2_result.png', 'バグのある関数は <code>[0, 0, 0, 0]</code> という結果を返し、同じ場所を4回訪れています。'
     '<code>print</code> を入れた結果を見ると、原因がはっきり分かります。'
     '<code>nearest</code> の初期値が <code>0</code> になっており、'
     '<code>distance[0][0]</code> は<strong>0.0</strong>なので、'
     'どの都市と比べても「0.0より小さい」ことがなく、<code>nearest</code> が一度も更新されません。'
     '修正版では初期値を <code>None</code> にして、最初の1件で必ず更新されるようにしています。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1と例題2のコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('14', ['AL2-14-ex1.py', 'AL2-14-ex2.py'])}

{keywords([
    ('テスト', 'test', 'わざと特別な入力を与えて、プログラムが正しく動くか確かめる作業。'),
    ('境界値', 'きょうかいち / boundary value', '0、1、いちばん大きい値など「ぎりぎりの値」。バグの多くは境界値で見つかる。'),
    ('デバッグ', 'debug', 'バグ（誤り）をさがして直すこと。<code>print</code> を入れて変数の中身を見る方法がいちばん手軽。'),
    ('例外', 'れいがい / exception', 'プログラムが続けられなくなったときに出るエラー。<code>IndexError</code> や <code>KeyError</code> など種類がある。'),
])}

{example(1, '境界値テストでバグを見つける', ex1_body)}

{example(2, 'print デバッグでバグの原因をつきとめる', ex2_body)}"""

ans = answers([slide_example("14"), blank_answers("14"),
    ("テストの答え合わせ", """        <p>自分で決めた入力なので、数値の正解は1つではありません。
        4種類のテストで「何が起きれば正しいか」を挙げます。</p>
        <table>
          <tr><th>試す入力</th><th>正しい動き</th><th>直っていない例</th></tr>
          <tr><td>空っぽ</td><td>「入力してください」と伝えて止まらない</td><td>0点や100点と表示される／エラーで止まる</td></tr>
          <tr><td>はしっこ（0、1、最大）</td><td>正しく計算できる</td><td>1つずれた答えが出る</td></tr>
          <tr><td>範囲の外</td><td>「範囲の外です」と伝えて受けつけない</td><td><code>IndexError</code> で止まる</td></tr>
          <tr><td>形がちがう（文字・記号）</td><td>「使えない文字です」と伝える</td><td>無視されて別の答えが出る</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>例題1の確認</strong>:
        修正版は「行ったり戻ったりする道」（"DRLDRR"）は<strong>受けつけます</strong>。
        遠回りなだけで反則ではないからです。正しい入力まで断ってしまうと、遊べる道が減ります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "テストと仕上げ", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("14", SLIDES),
    advanced_section("14"),
    rubric_section("14"),
    ans,
])

write("14", NAV, body)
