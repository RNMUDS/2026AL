# -*- coding: utf-8 -*-
"""第14回: 実践的課題（2）仕上げとレポート作成 の本文を組み立てる。"""
from common import (AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)


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
            ("3. 動かし方", "実行手順と入力の例", "python AL2-14-work.py を実行し、道を入力…"),
            ("4. 実行結果", "画面のコピーと、読み取れること", "図1のとおり、プレイヤー42秒・最短18秒…"),
            ("5. 調べたこと", "表と図で数値を示す", "表1のとおり、ステージを大きくすると…"),
            ("6. 苦労した点", "つまずきと、どう解決したか", "IndexError が出た。行の長さがそろって…"),
            ("7. これからやりたいこと", "足せなかった機能", "ステージを3つに増やしたい…")]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'レポートの7つの見出し</text>']
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
    "課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "実行確認", "例題1のテスト結果"),
    ("#sec-standard", "tag-standard", "課題1", "作品を仕上げる"),
    ("#sec-standard", "tag-standard", "課題1", "テスト結果を記録"),
    ("#sec-standard", "tag-standard", "課題2", "レポートを書く"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第14回では、第13回で作りはじめた作品を<strong>仕上げて</strong>、レポートにまとめます。
      仕上げるとは「機能を足す」ことだけではありません。
      <strong>変な入力を与えても止まらないようにする</strong>ことが、いちばん大切な仕上げです。
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
        第14回のレポートには、<strong>この表の4行それぞれについて、実際に試した結果</strong>を書いてもらいます。
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

{code('AL2-14-ex1.py')}

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

{code('AL2-14-ex2.py')}

{run('a14_ex2_result.png', 'バグのある関数は <code>[0, 0, 0, 0]</code> という結果を返し、同じ場所を4回訪れています。'
     '<code>print</code> を入れた結果を見ると、原因がはっきり分かります。'
     '<code>nearest</code> の初期値が <code>0</code> になっており、'
     '<code>distance[0][0]</code> は<strong>0.0</strong>なので、'
     'どの都市と比べても「0.0より小さい」ことがなく、<code>nearest</code> が一度も更新されません。'
     '修正版では初期値を <code>None</code> にして、最初の1件で必ず更新されるようにしています。')}"""

ex3_body = f"""      <p>レポートに実行時間を書くときの、正しい測り方を学びます。
      1回だけ測ると、たまたま遅かった値をつかむことがあります。</p>

{code('AL2-14-ex3.py')}

{run('a14_ex3_result.png', '同じ処理を5回測ったところ、いちばん速い回といちばん遅い回で差が出ました。'
     '差はわずかですが、<strong>毎回同じ値にはならない</strong>ことが確かめられます。'
     'パソコンは同時にほかの仕事もしているため、実行時間は必ずばらつきます。'
     'レポートには「5回測った平均」のように<strong>測り方も書く</strong>ことが大切です。'
     '「0.07秒でした」とだけ書かれていると、読んだ人は本当かどうか確かめられません。')}"""

ex4_body = f"""      <p>レポートに載せる「表」と「グラフ」を、文字だけで作ります。
      グラフを描くための特別な道具は必要ありません。</p>

{code('AL2-14-ex4.py')}

{run('a14_ex4_result.png', '表1では、都市の数ごとに最適解と貪欲法の答えが並んでいます。'
     '5都市のときだけ貪欲法が<strong>13.2%も長く</strong>、6都市と7都市では差が0%でした。'
     '図1のように棒の長さで表すと、5都市だけが飛び抜けていることが一目で分かります。'
     '図2では最適解と貪欲法を並べていますが、棒の長さがほとんど同じで差が読み取りにくくなっています。'
     '<strong>同じデータでも、何を棒の長さにするかで伝わり方が変わる</strong>ということです。'
     'レポートでは「差」を図にするほうが、言いたいことが伝わります。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    自分の作品を仕上げるときに、そのまま使えるやり方です。</p>

{setup_guide('14', ['AL2-14-ex1.py', 'AL2-14-ex2.py', 'AL2-14-ex3.py', 'AL2-14-ex4.py'])}

{keywords([
    ('テスト', 'test', 'わざと特別な入力を与えて、プログラムが正しく動くか確かめる作業。'),
    ('境界値', 'きょうかいち / boundary value', '0、1、いちばん大きい値など「ぎりぎりの値」。バグの多くは境界値で見つかる。'),
    ('デバッグ', 'debug', 'バグ（誤り）をさがして直すこと。<code>print</code> を入れて変数の中身を見る方法がいちばん手軽。'),
    ('例外', 'れいがい / exception', 'プログラムが続けられなくなったときに出るエラー。<code>IndexError</code> や <code>KeyError</code> など種類がある。'),
    ('再現性', 'さいげんせい / reproducibility', '同じ手順で誰がやっても同じ結果になること。レポートには測り方や環境も書く。'),
])}

{example(1, '境界値テストでバグを見つける', ex1_body)}

{example(2, 'print デバッグでバグの原因をつきとめる', ex2_body)}

{example(3, '実行時間の正しい測り方', ex3_body)}

{example(4, 'レポート用の表とグラフを作る', ex4_body)}"""

std1_body = """      <p>第13回で作りはじめた <code>AL2-13-work.py</code> を仕上げます。
      作業用のファイルは <code>AL2-14-work.py</code> という名前でコピーしてから始めてください。</p>

      <div class="setup-step">
        <p class="step-title">Step 1: テストする</p>
        <p style="font-size:0.95rem;color:#ccc;margin-bottom:0.5rem">次の4種類の入力を、実際に自分の作品に与えてください。</p>
        <ol>
          <li><strong>空っぽ</strong>: 何も入力しない／空のリストを渡す</li>
          <li><strong>はしっこ</strong>: いちばん小さい値・いちばん大きい値を入れる</li>
          <li><strong>範囲の外</strong>: マイナス、迷路の外、大きすぎる数を入れる</li>
          <li><strong>形がちがう</strong>: 数字のかわりに文字、使えない記号を入れる</li>
        </ol>
      </div>

      <div class="setup-step">
        <p class="step-title">Step 2: 直す</p>
        <ol>
          <li>エラーで止まったものを、<strong>止まらないように</strong>直す</li>
          <li>受けつけない入力には、<strong>理由を文章で表示する</strong></li>
          <li>直したら、もう一度4種類すべてを試す</li>
        </ol>
      </div>

      <div class="setup-step">
        <p class="step-title">Step 3: 記録する</p>
        <p style="font-size:0.95rem;color:#ccc">次の表をNotionに作り、4種類すべてについて記入してください。</p>
      </div>

      <table>
        <tr><th>試した入力</th><th>直す前の動き</th><th>直したあとの動き</th><th>直した内容</th></tr>
        <tr><td>空っぽ</td><td></td><td></td><td></td></tr>
        <tr><td>はしっこ</td><td></td><td></td><td></td></tr>
        <tr><td>範囲の外</td><td></td><td></td><td></td></tr>
        <tr><td>形がちがう</td><td></td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>もともと正しく動いていた場合:</strong>
      「直す前から正しく動いた」と書き、<strong>なぜ正しく動いたのか</strong>（どの行が守っているのか）を説明してください。</p>
"""

std2_body = """      <p>作品についてのレポートをNotionに書きます。次の7つの見出しをすべて作ってください。</p>

      <table>
        <tr><th>見出し</th><th>書くこと</th><th>目安</th></tr>
        <tr><td>1. 作品の名前と概要</td><td>何を作ったか</td><td>3行以上</td></tr>
        <tr><td>2. 使ったアルゴリズム</td><td>名前と、なぜ選んだか（第11回の3つの問いに沿って）</td><td>5行以上</td></tr>
        <tr><td>3. 動かし方</td><td>実行手順、入力の例、出力の見方</td><td>3行以上</td></tr>
        <tr><td>4. 実行結果</td><td>画面のコピーと、そこから読み取れること</td><td>結果＋3行以上</td></tr>
        <tr><td>5. 調べたこと</td><td><strong>表を1つ以上</strong>と<strong>図を1つ以上</strong></td><td>表1・図1として番号を付ける</td></tr>
        <tr><td>6. 苦労した点</td><td>つまずいた内容と、どう解決したか</td><td>2つ以上</td></tr>
        <tr><td>7. これからやりたいこと</td><td>足せなかった機能と、その理由</td><td>2つ以上</td></tr>
      </table>

      <div class="note-warn">
        <strong>見出し5「調べたこと」のヒント:</strong>
        自分の作品で、条件を変えると結果がどう変わるかを調べて表にします。次のような例があります。
        <ul style="padding-left:1.2rem;margin-top:0.5rem;font-size:0.92rem;line-height:1.9">
          <li>ステージの大きさを 5×5、8×8、12×12 と変えて、実行時間を測る</li>
          <li>配達先を 4件、6件、8件と増やして、貪欲法と全探索の差を測る</li>
          <li>沼のマスの割合を 0%、20%、40% と変えて、最短時間がどう変わるかを測る</li>
        </ul>
        例題3のように<strong>5回測った平均</strong>を書き、例題4のように<strong>表と図</strong>にしてください。
      </div>

      <p style="margin-top:1rem"><strong>書き方の注意:</strong></p>
      <ul class="point-list">
        <li>「動きました」「うまくいきました」だけでは足りません。<strong>数値</strong>を書いてください</li>
        <li>本文からは「表1のとおり」「図1を見ると」のように<strong>番号で指して</strong>ください</li>
        <li>うまくいかなかったことも、正直に書いてください。減点にはなりません</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">課題1と課題2に取り組み、解答をNotionに記録してください。
    第14回が作品づくりの<strong>最終回</strong>です。</p>

{standard(1, '作品をテストして仕上げる', std1_body)}
{notion('4種類のテストの表（直す前・直したあと・直した内容）、および仕上げたコード全体。')}

{standard(2, 'レポートを書く', std2_body)}
{notion('7つの見出しをすべて埋めたレポート。見出し5には表と図を必ず1つ以上ずつ入れる。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第14回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題1</strong>: 6種類の入力についての表、「行ったり戻ったりする道」を受けつける理由</li>
        <li><strong>課題1</strong>: 4種類のテストの表</li>
        <li><strong>課題1</strong>: 仕上げたコード全体と、最終的な実行結果</li>
        <li><strong>課題2</strong>: 7つの見出しを埋めたレポート</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
      <div class="note-warn" style="margin-top:1rem">
        <strong>第15回について:</strong> 第15回は後期のまとめです。
        提出物の最終チェックを行い、後期に学ばなかった発展的な手法（焼きなまし法・遺伝的アルゴリズム）を体験します。
        作品とレポートは第15回の授業中まで修正できます。
      </div>
    </div>"""

ans = answers([
    ("例題1: 6種類の入力についての表", """        <table>
          <tr><th>入力</th><th>バグのある関数</th><th>修正版</th></tr>
          <tr><td>ふつうの道 "DDRR"</td><td>(2,2) 迷路の中</td><td>OK: 4歩 ／ 12秒</td></tr>
          <tr><td>空の道 ""</td><td>(0,0) 迷路の中</td><td>受けつけない: ゴールに着いていません</td></tr>
          <tr><td>迷路の外に出る道 "DDDDDD"</td><td><strong style="color:#FF5252">(6,0) 迷路の外</strong></td><td>受けつけない: 迷路の外に出てしまいました</td></tr>
          <tr><td>ゴールに着かない道 "DR"</td><td>(1,1) 迷路の中</td><td>受けつけない: ゴールに着いていません</td></tr>
          <tr><td>使えない文字 "DDXR"</td><td>(2,1) 迷路の中（Xが無視された）</td><td>受けつけない: 「X」は使えない文字です</td></tr>
          <tr><td>行ったり戻ったりする道 "DRLDRR"</td><td><strong style="color:#FF5252">(2,3) 迷路の外</strong></td><td>OK: 6歩 ／ 22秒</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>バグのある関数の問題点:</strong></p>
        <ul class="point-list">
          <li>迷路の外に出ても気づかず、そのまま返している。あとで <code>cost_map[6][0]</code> を計算しようとして <code>IndexError</code> で止まる</li>
          <li><code>U</code> と <code>L</code> をあつかっていないため、"DRLDRR" の <code>L</code>（左）が無視され、右へ進みすぎて外に出た</li>
          <li>使えない文字 <code>X</code> も無視されるので、プレイヤーは打ちまちがいに気づけない</li>
          <li>空の道やゴールに着かない道も「OK」として返してしまう</li>
        </ul>
        <p style="margin-top:0.8rem"><strong>「行ったり戻ったりする道」を受けつけている理由:</strong>
        "DRLDRR" は 下→右→左→下→右→右 と動き、途中で1歩戻っていますが、
        <strong>迷路の外に出ておらず、最後にゴールへ着いている</strong>ので、ルールの上では正しい道です。
        遠回りをしたぶん歩数が増え、合計時間も長くなるだけで、反則ではありません。</p>
        <p style="margin-top:0.6rem">テストで大切なのは「変な入力をすべて拒む」ことではなく、
        <strong>「正しい入力は受けつけ、正しくない入力は理由をつけて断る」</strong>ことです。
        正しい入力まで断ってしまうと、遊べる道が減ってゲームがつまらなくなります。</p>"""),
    ("課題1・課題2: 仕上げとレポートのヒント", """        <p>作品は人によって違うので、ここでは評価される書き方の例を示します。</p>
        <p style="margin-top:0.6rem"><strong>課題1のテスト表の記入例:</strong></p>
        <table>
          <tr><th>試した入力</th><th>直す前</th><th>直したあと</th><th>直した内容</th></tr>
          <tr><td>空っぽ（道を入力しない）</td><td>0秒・スコア100点と表示された</td><td>「ゴールに着いていません」と表示</td><td>最後のマスがゴールかを確かめる <code>if</code> を追加</td></tr>
          <tr><td>はしっこ（1歩だけの道 "D"）</td><td>エラーにはならないが100点と出た</td><td>「ゴールに着いていません」と表示</td><td>同上</td></tr>
          <tr><td>範囲の外（"DDDDDDDDDD"）</td><td><code>IndexError</code> で止まった</td><td>「迷路の外に出てしまいました」と表示</td><td>1歩進むたびに範囲内かを確かめる <code>if</code> を追加</td></tr>
          <tr><td>形がちがう（"DD1R"）</td><td>1 が無視されて別の場所に着いた</td><td>「1 は使えない文字です」と表示</td><td><code>else</code> で使えない文字をはじく</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>課題2の見出し2（使ったアルゴリズム）の記入例:</strong></p>
        <p style="margin-top:0.4rem">「ダイクストラ法を使った。第11回の3つの問いに当てはめると、
        まず問題の種類は『2地点をつなぐ道をさがす』であり、巡回セールスマン問題ではない。
        次に、マスごとに通り抜ける時間が1秒・5秒・9秒と違うので、重みに差がある。
        最後に、ゲームの採点に使うため、最短時間は必ず正確でなければならない。
        以上から、重み付きグラフで必ず最適解を出せるダイクストラ法を選んだ。
        幅優先探索では歩数しか見ないため、沼を通る道を最短と判断してしまい、採点が正しくならない。」</p>
        <p style="margin-top:0.8rem"><strong>課題2の見出し5（調べたこと）の記入例:</strong></p>
        <p style="margin-top:0.4rem">「ステージの大きさを変えたときの実行時間を、5回ずつ測って平均した（表1）。
        マスの数が4倍になると、実行時間もおよそ4倍になった。
        図1のとおり、増え方はまっすぐで、急に遅くなる大きさは見られなかった。
        第7回の例題3で確かめたダイクストラ法の性質と一致している。」</p>
        <p style="margin-top:0.8rem"><strong>評価が低くなる書き方:</strong></p>
        <ul class="point-list">
          <li><span style="color:#FF5252">「ダイクストラ法を使いました。動いてよかったです。」</span> — なぜ選んだかがない</li>
          <li><span style="color:#FF5252">「速く動きました。」</span> — 数値がない</li>
          <li><span style="color:#FF5252">「特に苦労はありませんでした。」</span> — 何も試していない可能性が高い</li>
          <li><span style="color:#FF5252">表や図に番号と題がない</span> — 本文から指せない</li>
        </ul>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "テストと仕上げ", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("14", NAV, body)
