# -*- coding: utf-8 -*-
"""第11回: アルゴリズム比較・復習 の本文を組み立てる。"""
import math
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
                    AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)


# ────────────────────────────────────────────────────────────
# 図1: 後期に学んだアルゴリズムの地図
# ────────────────────────────────────────────────────────────
def fig_map():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '後期に学んだ5つのアルゴリズム</text>']
    # 大分類
    groups = [
        ("2地点間の最短経路をさがす", 24, 330, GREEN,
         [("幅優先探索", "第1〜3回", "重みなし　歩数を最小に"),
          ("深さ優先探索", "第2回", "重みなし　到達できるかを調べる"),
          ("ダイクストラ法", "第5〜7回", "重みあり　合計コストを最小に")]),
        ("全部回って戻る最短ルートをさがす", 366, 310, AMBER,
         [("全探索", "第8回", "必ず最適　12都市まで"),
          ("貪欲法", "第9回", "近似解　何千都市でも"),
          ("bitDP", "第10回", "必ず最適　20都市まで")]),
    ]
    for title, x0, w, color, items in groups:
        s.append(f'        <rect x="{x0}" y="48" width="{w}" height="230" rx="12" fill="#141414" stroke="{color}" stroke-width="1.6"/>')
        s.append(f'        <text x="{x0+w/2}" y="72" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        for i, (name, week, note) in enumerate(items):
            y = 88 + i * 62
            s.append(f'        <rect x="{x0+14}" y="{y}" width="{w-28}" height="52" rx="8" fill="#1A1A1A" stroke="#3a3a3a"/>')
            s.append(f'        <text x="{x0+26}" y="{y+22}" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
            s.append(f'        <text x="{x0+w-26}" y="{y+22}" text-anchor="end" fill="{GRAY}" font-size="10">{week}</text>')
            s.append(f'        <text x="{x0+26}" y="{y+41}" fill="{GRAY}" font-size="10">{note}</text>')
    s.append(f'        <text x="350" y="302" text-anchor="middle" fill="#ccc" font-size="12">'
             '左は「どの道を通るか」を決める問題、右は「どの順番で回るか」を決める問題</text>')
    return fig(700, 320, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: どれを使うかの判断フローチャート
# ────────────────────────────────────────────────────────────
def fig_flow():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'どのアルゴリズムを使うかの決め方</text>']

    def box(x, y, w, h, text, color, sub=None, rx=10):
        out = [f'        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#141414" stroke="{color}" stroke-width="1.8"/>',
               f'        <text x="{x+w/2}" y="{y+(h/2)+(0 if sub is None else -6)}" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">{text}</text>']
        if sub:
            out.append(f'        <text x="{x+w/2}" y="{y+(h/2)+12}" text-anchor="middle" fill="{GRAY}" font-size="10">{sub}</text>')
        return out

    def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None):
        out = [f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" stroke-width="2"/>',
               f'        <polygon points="{x2},{y2} {x2-5},{y2-9} {x2+5},{y2-9}" fill="#555"/>' if y2 > y1 else
               f'        <polygon points="{x2},{y2} {x2-9},{y2-5} {x2-9},{y2+5}" fill="#555"/>']
        if label:
            out.append(f'        <text x="{lx}" y="{ly}" fill="{AMBER}" font-size="11" font-weight="700">{label}</text>')
        return out

    s += box(250, 48, 200, 44, "どんな問題か？", "#888")
    s += arrow(300, 92, 150, 122, "2地点間の経路", 140, 112)
    s += arrow(400, 92, 550, 122, "全部回って戻る", 470, 112)

    s += box(50, 124, 200, 44, "辺に重みがあるか？", "#888")
    s += arrow(100, 168, 100, 200, "ない", 68, 190)
    s += arrow(200, 168, 220, 200, "ある", 214, 190)
    s += box(20, 202, 160, 56, "幅優先探索", GREEN, "最短が必要なとき")
    s += box(190, 202, 160, 56, "ダイクストラ法", GREEN, "コスト最小が必要")
    s += box(20, 270, 160, 44, "深さ優先探索", BLUE, "行けるかだけ調べる")
    s += arrow(100, 258, 100, 268)

    s += box(450, 124, 200, 44, "必ず最適解が必要か？", "#888")
    s += arrow(500, 168, 500, 200, "いいえ", 452, 190)
    s += arrow(600, 168, 620, 200, "はい", 616, 190)
    s += box(420, 202, 150, 56, "貪欲法", AMBER, "何千都市でも一瞬")
    s += box(580, 202, 100, 44, "都市の数", "#888")
    s += arrow(600, 246, 560, 276, "10以下", 470, 286)
    s += arrow(650, 246, 660, 276, "11〜20", 640, 286)
    s += box(470, 278, 110, 40, "全探索", AMBER)
    s += box(600, 278, 90, 40, "bitDP", AMBER)
    s.append(f'        <text x="350" y="336" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '都市が20を超えるなら、最適解をあきらめて貪欲法を使うしかない</text>')
    return fig(700, 352, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 実測の比較
# ────────────────────────────────────────────────────────────
def fig_measured():
    rows = [(6, 57.8, 0.000, 57.8, 57.8, 0.000),
            (8, 58.0, 0.001, 58.7, 58.0, 0.000),
            (10, 59.5, 0.065, 60.2, 59.5, 0.001),
            (12, 73.1, 8.334, 80.5, 73.1, 0.009),
            (14, None, None, 83.3, 75.9, 0.044),
            (16, None, None, 87.1, 79.7, 0.230)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ問題を3つの方法で解いたときの答えと時間</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '緑 = 必ず最適　／　オレンジ = 近似解　／　時間はパソコンによって変わる</text>']
    head = ["都市数", "全探索", "貪欲法", "bitDP"]
    xs = [40, 180, 360, 540]
    for x, h in zip(xs, head):
        s.append(f'        <text x="{x}" y="76" fill="#E0E0E0" font-size="12" font-weight="700">{h}</text>')
    for i, (n, bv, bt, gv, dv, dt) in enumerate(rows):
        y = 96 + i * 40
        s.append(f'        <rect x="30" y="{y}" width="640" height="34" rx="7" fill="{"#141414" if i%2==0 else "#101010"}" stroke="#252525"/>')
        s.append(f'        <text x="{xs[0]}" y="{y+22}" fill="#ccc" font-size="12">{n}都市</text>')
        if bv is None:
            s.append(f'        <text x="{xs[1]}" y="{y+22}" fill="{RED}" font-size="11">終わらないため省略</text>')
        else:
            s.append(f'        <text x="{xs[1]}" y="{y+22}" fill="{GREEN}" font-size="12" font-weight="700">{bv}</text>')
            s.append(f'        <text x="{xs[1]+52}" y="{y+22}" fill="{GRAY}" font-size="10">{bt:.3f}秒</text>')
        s.append(f'        <text x="{xs[2]}" y="{y+22}" fill="{AMBER}" font-size="12" font-weight="700">{gv}</text>')
        s.append(f'        <text x="{xs[2]+52}" y="{y+22}" fill="{GRAY}" font-size="10">ほぼ0秒</text>')
        s.append(f'        <text x="{xs[3]}" y="{y+22}" fill="{GREEN}" font-size="12" font-weight="700">{dv}</text>')
        s.append(f'        <text x="{xs[3]+52}" y="{y+22}" fill="{GRAY}" font-size="10">{dt:.3f}秒</text>')
    s.append(f'        <text x="350" y="{96+6*40+24}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '12都市では、bitDP は全探索より約900倍速く、答えはまったく同じ')
    s.append('</text>')
    return fig(700, 96 + 6 * 40 + 42, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "全体の整理 #sec-explanation",
    "例題 #sec-examples",
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("11")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第1回から第10回までで、5つのアルゴリズムを学びました。
      第11回では、5つを1つの地図の上に並べ、<strong>どんなときにどれを使うか</strong>を整理します。
      第12回以降の作品づくりでは、自分で選んで使うことになります。
    </p>

{fig_map()}

    <div class="concept-box">
      <h4>5つのアルゴリズムの一覧</h4>
      <table>
        <tr><th>名前</th><th>解く問題</th><th>答えの質</th><th>使う入れもの</th><th>あつかえる大きさ</th></tr>
        <tr><td><strong style="color:#76B900">幅優先探索</strong></td><td>2地点間で歩数（辺の数）が最小の経路</td><td>必ず最適</td><td>キュー</td><td>数百万頂点</td></tr>
        <tr><td><strong style="color:#4FC3F7">深さ優先探索</strong></td><td>2地点がつながっているかの判定</td><td>経路は最短でない</td><td>スタック</td><td>数百万頂点</td></tr>
        <tr><td><strong style="color:#76B900">ダイクストラ法</strong></td><td>2地点間でコストの合計が最小の経路</td><td>必ず最適（重みが0以上のとき）</td><td>優先度付きキュー</td><td>数十万頂点</td></tr>
        <tr><td><strong style="color:#FFB800">全探索</strong></td><td>全部回って戻る最短ルート</td><td>必ず最適</td><td>なし</td><td>12都市くらい</td></tr>
        <tr><td><strong style="color:#FFB800">貪欲法</strong></td><td>全部回って戻るそこそこ短いルート</td><td>近似解</td><td>なし</td><td>何千都市でも</td></tr>
        <tr><td><strong style="color:#FFB800">bitDP</strong></td><td>全部回って戻る最短ルート</td><td>必ず最適</td><td>表（2次元リスト）</td><td>20都市くらい</td></tr>
      </table>
    </div>

{fig_flow()}

    <div class="concept-box">
      <h4>選ぶときの3つの問い</h4>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li><strong>どんな問題か</strong>: 「2地点をつなぐ道」をさがすのか、「回る順番」を決めるのか</li>
        <li><strong>重みに差があるか</strong>: すべての辺が同じ重さなら、幅優先探索で足りる</li>
        <li><strong>必ず最適解が必要か</strong>: 近似解でよいなら、ずっと大きい問題があつかえる</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        3つの問いに答えれば、使うべきアルゴリズムはほぼ1つに決まります。
        例題4では、3つの問いをそのままプログラムにしたものを動かします。
      </p>
    </div>

{fig_measured()}"""

ex1_body = f"""      <p>同じ路線図・同じ出発点・同じ目的地に対して、幅優先探索・深さ優先探索・ダイクストラ法の3つを走らせ、
      出てくる経路を比べます。</p>

{code('AL2-11-ex1.py')}

{run('a11_ex1_result.png', '幅優先探索とダイクストラ法は、はっきり違う経路を返しました。'
     '幅優先探索は<strong>2本・41分</strong>の「新宿 → 品川 → 東京」を選び、'
     'ダイクストラ法は<strong>3本・27分</strong>の「新宿 → 渋谷 → 品川 → 東京」を選んでいます。'
     '乗りかえが1回増えるかわりに、14分も早く着くということです。'
     '深さ優先探索は、たまたま幅優先探索と同じ経路になりました。'
     '深さ優先探索は「本数」も「時間」も最小にしないので、'
     '同じになるかどうかは、たまたま調べた順番で決まります。')}

{notion('例題1の実行結果から、3つの方法それぞれの「路線の本数」「合計時間」「経路」を表にまとめる。'
        'あわせて、幅優先探索とダイクストラ法の答えが違う理由を説明する。')}"""

ex2_body = f"""      <p>巡回セールスマン問題を4つの方法で解きます。
      第9回の貪欲法に「すべての都市を出発点にして試す」やり方を足した4つ目も加えます。</p>

{code('AL2-11-ex2.py')}

{run('a11_ex2_result.png', '全探索・bitDP・貪欲法(全出発点) の3つが、いずれも<strong>46.8</strong>という同じ答えを出しました。'
     '出発点を1つに固定した貪欲法だけが53.2で、6.4長くなっています。'
     '注目すべきは<strong>貪欲法(全出発点)</strong>で、8回ぶん計算しても0.000022秒しかかからず、'
     '全探索の約40分の1の時間で同じ答えにたどり着いています。'
     'ただし、たまたま最適に当たっただけで、いつでも当たる保証はありません。'
     '「必ず最適」と書けるのは全探索と bitDP だけです。')}"""

ex3_body = f"""      <p>都市の数を6個から16個まで変えて、3つの方法の答えと時間を一度に測ります。
      全探索は12都市までで打ち切ります。実行に10秒ほどかかります。</p>

{code('AL2-11-ex3.py')}

{run('a11_ex3_result.png', '全探索と bitDP の答えは、どの大きさでも<strong>完全に一致</strong>しています。'
     '12都市では、全探索に<strong>約8秒</strong>かかったのに対し、bitDP は0.01秒ほどで、<strong>数百倍</strong>の差がつきました。'
     '14都市と16都市では、全探索は終わらないため省略しています。'
     '貪欲法の答えは、12都市で80.5（最適は73.1）と約10%長くなっていますが、時間はほとんどゼロです。'
     '「必ず最適・遅い」「必ず最適・速い」「近似・非常に速い」の3種類がそろっていることを確かめてください。')}

{notion('例題3の表から、都市の数ごとの3つの答えと時間を書き写す。'
        'あわせて、12都市のときに全探索と bitDP の時間が何倍違うかを計算し、'
        '答えが同じである理由を説明する。')}"""

ex4_body = f"""      <p>3つの問い（どんな問題か／重みがあるか／最適解が必要か）を、そのままプログラムにします。
      条件を渡すと、使うべきアルゴリズムと理由が返ってきます。</p>

{code('AL2-11-ex4.py')}

{run('a11_ex4_result.png', '8つの場面について、それぞれ使うべきアルゴリズムと理由が表示されました。'
     '同じ「巡回」の問題でも、6都市なら全探索、18都市なら bitDP、100軒なら貪欲法と、答えが変わっています。'
     '注目すべきは最後の<strong>「30軒の最適な順番を1晩かけて求める」</strong>で、'
     '最適解がほしくても、30都市では bitDP の表が大きすぎるため、貪欲法を選ぶしかありません。'
     '<code>choose</code> 関数の中身を読むと、条件がそのまま <code>if</code> 文になっていることが分かります。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題3は実行に10秒ほどかかります。まず作業フォルダを用意します。</p>

{setup_guide('11', ['AL2-11-ex1.py', 'AL2-11-ex2.py', 'AL2-11-ex3.py', 'AL2-11-ex4.py'])}

{keywords([
    ('最適解', 'さいてきかい', '考えられる中で本当にいちばん良い答え。全探索・bitDP・ダイクストラ法が出す。'),
    ('近似解', 'きんじかい', '最適ではないが実用上じゅうぶん良い答え。貪欲法が出す。'),
    ('計算量', 'けいさんりょう', '問題が大きくなったとき、手数がどれくらい増えるかの目安。'),
    ('トレードオフ', 'trade-off', '一方を良くすると他方が悪くなる関係。「答えの質」と「かかる時間」がその代表。'),
    ('多始点', 'たしてん / multi-start', '出発点をいろいろ変えて何度も試し、いちばん良い答えを採用するやり方。貪欲法の精度を上げられる。'),
])}

{example(1, '3つの探索を同じグラフで比べる', ex1_body)}

{example(2, '巡回セールスマン問題を4つの方法で解く', ex2_body)}

{example(3, '大きさを変えて一括で測る', ex3_body)}

{example(4, '条件からアルゴリズムを選ぶ', ex4_body)}"""

ans = answers([
    ("確かめ用の数値", """        <p><strong>問い1</strong>: <strong>すべての辺の重みが同じとき</strong>に一致します。
        重みがすべて1なら、合計コストはそのまま辺の数と同じ値になるためです。
        幅優先探索は、ダイクストラ法の特別な場合だと言えます。</p>
        <p style="margin-top:0.8rem"><strong>例題3の数値（スライドBで使うもの）</strong></p>
        <table>
          <tr><th>都市数</th><th>全探索</th><th>貪欲法</th><th>bitDP</th></tr>
          <tr><td>10都市</td><td>59.5</td><td>60.2</td><td>59.5</td></tr>
          <tr><td>12都市</td><td>73.1（約8秒）</td><td>80.5（ほぼ0秒）</td><td>73.1（0.01秒ほど）</td></tr>
          <tr><td>14都市</td><td>終わらない</td><td>83.3</td><td>75.9</td></tr>
          <tr><td>16都市</td><td>終わらない</td><td>87.1</td><td>79.7</td></tr>
        </table>
        <p style="margin-top:0.6rem">12都市で貪欲法は 80.5 ÷ 73.1 ＝ 約10%長くなっています。</p>
        <p style="margin-top:0.8rem"><strong>問い2</strong>は答えが1つに決まりません。
        3つの問い（問題の種類／重みに差があるか／最適解が必要か）に沿って書けているかを見ます。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "後期の全体像", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("11", SLIDES),
    rubric_section("11"),
    ans,
])

write("11", NAV, body)
