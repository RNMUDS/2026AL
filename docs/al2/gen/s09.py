# -*- coding: utf-8 -*-
"""第9回: 巡回セールスマン問題（2）貪欲法による近似 の本文を組み立てる。"""
import math
from itertools import permutations
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

CITIES = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9),
          ("カフェ", 6, 12), ("公園", 3, 8), ("駅", 17, 4),
          ("病院", 12, 13), ("書店", 8, 7)]
HOUSES = [("営業所", 0, 8), ("A宅", 1, 5), ("遠方のD宅", 11, 2),
          ("B宅", 6, 4), ("E宅", 0, 12), ("C宅", 5, 9)]


def table(cs):
    n = len(cs)
    return [[math.hypot(cs[i][1] - cs[j][1], cs[i][2] - cs[j][2]) for j in range(n)] for i in range(n)]


def greedy(cs, start=0):
    t = table(cs)
    n = len(cs)
    visited = [start]
    total = 0.0
    here = start
    while len(visited) < n:
        nearest = min((j for j in range(n) if j not in visited), key=lambda j: t[here][j])
        total += t[here][nearest]
        visited.append(nearest)
        here = nearest
    total += t[here][start]
    return visited, total


def optimal(cs):
    t = table(cs)
    n = len(cs)
    best, bo = None, None
    for o in permutations(range(1, n)):
        s, h = 0.0, 0
        for c in o:
            s += t[h][c]
            h = c
        s += t[h][0]
        if best is None or s < best:
            best, bo = s, o
    return [0] + list(bo), best


def draw_route(cs, route, x0, y0, sx, sy, color, r=11, labels=True, closed=True):
    out = []
    seq = route + [route[0]] if closed else route
    for k in range(len(seq) - 1):
        a, b = seq[k], seq[k + 1]
        x1, y1 = x0 + cs[a][1] * sx, y0 + cs[a][2] * sy
        x2, y2 = x0 + cs[b][1] * sx, y0 + cs[b][2] * sy
        out.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="2.5"/>')
    order = {c: i for i, c in enumerate(route)}
    for i, (name, x, y) in enumerate(cs):
        cx, cy = x0 + x * sx, y0 + y * sy
        col = AMBER if i == route[0] else color
        out.append(f'        <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
        mark = "S" if i == route[0] else str(order[i])
        out.append(f'        <text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" fill="#E0E0E0" font-size="{r-2}" font-weight="700">{mark}</text>')
        if labels:
            out.append(f'        <text x="{cx:.0f}" y="{cy-r-5:.0f}" text-anchor="middle" fill="{GRAY}" font-size="9">{name}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 貪欲法の進み方
# ────────────────────────────────────────────────────────────
def fig_greedy_steps():
    cs = CITIES[:5]
    t = table(cs)
    route, total = greedy(cs)
    sx, sy, ox, oy = 30, 20, 60, 78
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '貪欲法: いまいる都市から、いちばん近い都市へ進むことをくり返す</text>']
    for i in range(5):
        for j in range(i + 1, 5):
            x1, y1 = ox + cs[i][1] * sx, oy + cs[i][2] * sy
            x2, y2 = ox + cs[j][1] * sx, oy + cs[j][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#242424" stroke-width="1"/>')
    seq = route + [route[0]]
    for k in range(len(seq) - 1):
        a, b = seq[k], seq[k + 1]
        x1, y1 = ox + cs[a][1] * sx, oy + cs[a][2] * sy
        x2, y2 = ox + cs[b][1] * sx, oy + cs[b][2] * sy
        p0 = (1 - 0.18) * k / (len(seq) - 1)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                f'dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="3.5"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'          <text x="{mx}" y="{my-8}" text-anchor="middle" fill="{GREEN}" font-size="11" font-weight="700">{round(t[a][b],1)}</text>')
        s.append('        </g>')
        label = ("出発点へ戻る" if k == len(seq) - 2
                 else f"{cs[a][0]} から見ていちばん近いのは {cs[b][0]}")
        s.append(f'        <text x="350" y="52" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{p0:.3f};{p0+0.02:.3f};{p0+0.14:.3f};{p0+0.16:.3f};1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'{k+1}歩目: {label}</text>')
    for i, (name, x, y) in enumerate(cs):
        cx, cy = ox + x * sx, oy + y * sy
        col = AMBER if i == 0 else GREEN
        s.append(f'        <circle cx="{cx}" cy="{cy}" r="15" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
        s.append(f'        <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{i}</text>')
        s.append(f'        <text x="{cx}" y="{cy-20}" text-anchor="middle" fill="{GRAY}" font-size="10">{name}</text>')
    s.append(f'        <text x="350" y="{oy+13*sy+30}" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             f'貪欲法の答え: 合計 {round(total,1)}　（この5都市では、全探索の答えと同じになった）</text>')
    return fig(700, oy + 13 * sy + 46, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 8都市での比較
# ────────────────────────────────────────────────────────────
def fig_compare8():
    cs = CITIES
    g_route, g_len = greedy(cs)
    o_route, o_len = optimal(cs)
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が8個になると、貪欲法は最短ルートを見つけられない</text>']
    for panel, (route, total, title, color) in enumerate([
            (g_route, g_len, "貪欲法", AMBER), (o_route, o_len, "全探索（本当の最短）", GREEN)]):
        x0 = 20 + panel * 350
        s.append(f'        <rect x="{x0}" y="46" width="330" height="258" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="68" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">'
                 f'{title}: 合計 {round(total,1)}</text>')
        s += draw_route(cs, route, x0 + 24, 88, 15.5, 12.5, color, 11)
    s.append(f'        <text x="350" y="326" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             f'差は {round(g_len-o_len,1)}。貪欲法は最短ルートより 13.6% 長い</text>')
    return fig(700, 342, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 出発点を変えたときの結果
# ────────────────────────────────────────────────────────────
def fig_starts():
    cs = CITIES
    o_route, o_len = optimal(cs)
    results = []
    for start in range(len(cs)):
        route, total = greedy(cs, start)
        results.append((cs[start][0], round(total, 1)))
    worst = max(v for _, v in results)
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '出発する都市を変えるだけで、貪欲法の答えは大きく変わる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         f'全探索で求めた本当の最短は {round(o_len,1)}（緑の点線）</text>']
    x0, wmax = 130, 440
    base = round(o_len, 1)
    for i, (name, v) in enumerate(results):
        y = 62 + i * 34
        w = v / worst * wmax
        color = GREEN if v == base else (RED if v == worst else AMBER)
        s.append(f'        <text x="118" y="{y+19}" text-anchor="end" fill="#ccc" font-size="11">{name}</text>')
        s.append(f'        <rect x="{x0}" y="{y+4}" width="{w:.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{x0+w+10:.0f}" y="{y+21}" fill="{color}" font-size="12" font-weight="700">{v}</text>')
    xline = x0 + base / worst * wmax
    s.append(f'        <line x1="{xline:.0f}" y1="56" x2="{xline:.0f}" y2="{62+8*34}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'        <text x="350" y="{62+8*34+22}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '書店から出発したときだけ、たまたま最短ルートに当たっている</text>')
    return fig(700, 62 + 8 * 34 + 40, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 貪欲法が大きく損をする配置
# ────────────────────────────────────────────────────────────
def fig_trap():
    cs = HOUSES
    g_route, g_len = greedy(cs)
    o_route, o_len = optimal(cs)
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{RED}" font-weight="700" font-size="15">'
         '遠くに1軒だけ離れた家があると、貪欲法は大きく損をする</text>']
    for panel, (route, total, title, color) in enumerate([
            (g_route, g_len, "貪欲法", RED), (o_route, o_len, "全探索（本当の最短）", GREEN)]):
        x0 = 20 + panel * 350
        s.append(f'        <rect x="{x0}" y="46" width="330" height="250" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="68" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">'
                 f'{title}: 合計 {round(total,1)}</text>')
        s += draw_route(cs, route, x0 + 46, 92, 22, 15, color, 12)
    s.append(f'        <text x="350" y="318" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             f'貪欲法は最短より 42.5% 長い。遠方のD宅を最後まで残したことが原因</text>')
    return fig(700, 334, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "貪欲法とは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2の差と速さ"),
    ("#sec-examples", "tag-example", "観察記録", "例題4の失敗のしかた"),
    ("#sec-standard", "tag-standard", "標準課題1", "出発点を変えると？"),
    ("#sec-standard", "tag-standard", "標準課題2", "貪欲法の弱点を説明"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第8回で確かめたとおり、巡回セールスマン問題は都市が増えると全探索が使えなくなります。
      そこで発想を変えます。<strong>「必ず最短」をあきらめて、「そこそこ短いルートを一瞬で作る」</strong>方法を考えます。
      いちばん単純な作戦が<strong>貪欲法</strong>（どんよくほう）です。
    </p>

    <div class="analogy">
      買い物リストを持ってスーパーに入ったとき、「いま自分がいる場所からいちばん近い商品を取りに行く」
      をくり返す人は多いはずです。全部の回り方を頭の中で比べる人はいません。
      目の前でいちばん良さそうな選択をくり返す考え方が、貪欲法です。
    </div>

    <div class="concept-box">
      <h4>貪欲法の手順（最近傍法）</h4>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li>出発点に立つ</li>
        <li>まだ行っていない都市のうち、<strong>いまいる場所からいちばん近い都市</strong>を選ぶ</li>
        <li>そこへ移動する</li>
        <li>まだ行っていない都市がある間、2と3をくり返す</li>
        <li>全部回り終えたら出発点へ戻る</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        「いちばん近い都市へ進む」という選び方から、<strong>最近傍法</strong>（さいきんぼうほう）とも呼ばれます。
        都市が n 個なら、比べる回数は n×n 程度です。8都市なら数十回、1000都市でも100万回程度で終わります。
      </p>
    </div>

{fig_greedy_steps()}

    <div class="concept-box">
      <h4>貪欲法が最短にならない理由</h4>
      <p style="font-size:0.95rem">
        貪欲法は、1歩先だけを見て決めます。「いま近い」都市を選んだせいで、
        あとから<strong>遠く離れた都市が取り残される</strong>ことがあります。
        取り残された都市へ行くには長い移動が必要になり、その1回で、それまでに節約した分をすべて失ってしまいます。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        目の前だけを見て決めた結果、全体としては良くならないことを<strong>局所最適</strong>（きょくしょさいてき）と呼びます。
        「部分的にはいちばん良い」けれど「全体でいちばん良いとはかぎらない」という意味です。
      </p>
    </div>

{fig_compare8()}

    <div class="concept-box">
      <h4>近似解という考え方</h4>
      <table>
        <tr><th></th><th>全探索（第8回）</th><th>貪欲法（第9回）</th></tr>
        <tr><td>答えの質</td><td>必ず最短（最適解）</td><td>最短とはかぎらない（近似解）</td></tr>
        <tr><td>8都市での結果</td><td>46.8</td><td>53.2（13.6%長い）</td></tr>
        <tr><td>調べる手数</td><td>(n-1)! 通り</td><td>n×n 程度</td></tr>
        <tr><td>1000都市</td><td>終わらない</td><td>一瞬で終わる</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        最短ではないけれど実用的な答えを<strong>近似解</strong>（きんじかい）と呼びます。
        配送計画では「1%短いルートを1週間かけて計算する」より
        「10%長くても1秒で出す」ほうが役に立つ場面がほとんどです。
      </p>
    </div>"""

ex1_body = f"""      <p>第8回と同じ5つの都市に、貪欲法を使います。
      「いまいる都市から、まだ行っていない都市のうちいちばん近いところへ進む」をくり返すだけです。
      全探索の答えと比べます。</p>

{code('AL2-09-ex1.py')}

{run('a09_ex1_result.png', '貪欲法は「学校 → 公園 → カフェ → 図書館 → 郵便局 → 学校」というルートを作り、合計は<strong>34.9</strong>でした。'
     '全探索で求めた最短も34.9なので、<strong>差は0</strong>です。'
     'ただし2つのルートをよく見ると、回る向きが逆になっているだけで、通る道はまったく同じです。'
     '貪欲法は24通りを試さず、たった4回の比較でルートを作っています。'
     '都市が5個と少ないため、たまたま最短に当たったという点に注意してください。')}"""

ex2_body = f"""      <p>都市を8個に増やして、同じ比較をします。都市が増えると結果はどう変わるでしょうか。</p>

{code('AL2-09-ex2.py')}

{run('a09_ex2_result.png', '貪欲法は<strong>53.2</strong>、全探索は<strong>46.8</strong>で、差は6.4でした。'
     '貪欲法のルートは最短ルートより<strong>13.6%長い</strong>という結果です。'
     '一方で速さは、貪欲法が全探索の約150倍でした。'
     '都市が5個のときは同じ答えでしたが、8個になると差が出ています。'
     '都市が増えるほど、貪欲法が最短に当たる可能性は下がっていきます。')}

{notion('例題2の実行結果から、貪欲法と全探索の「合計距離」「かかった時間」「試した順番の数」を表にまとめる。'
        'あわせて、2つのルートを見比べて、どの都市の順番が入れかわっているかを書く。')}"""

ex3_body = f"""      <p>貪欲法は出発点によって答えが変わります。
      8つの都市それぞれを出発点にして、貪欲法を8回動かし、結果を並べて比べます。</p>

{code('AL2-09-ex3.py')}

{fig_starts()}

{run('a09_ex3_result.png', '出発点によって、貪欲法の答えは<strong>46.8から61.2まで</strong>ばらつきました。'
     'いちばん悪いのは図書館から出発した場合の61.2で、最短より14.4も長くなっています。'
     '注目すべきは<strong>書店から出発した場合</strong>で、答えは46.8となり、全探索で求めた最短と完全に一致しました。'
     '貪欲法は運に左右されるということです。'
     'この性質を利用して、<strong>すべての出発点で試して、いちばん良かった答えを採用する</strong>というやり方もよく使われます。'
     'それでも全探索よりずっと速く終わります。')}"""

ex4_body = f"""      <p>貪欲法が大きく損をする配置を作って、失敗のしかたを観察します。
      配達先のうち1軒だけが、ほかから遠く離れた場所にある場合です。</p>

{code('AL2-09-ex4.py')}

{fig_trap()}

{run('a09_ex4_result.png', '貪欲法は<strong>46.6</strong>、全探索は<strong>32.7</strong>で、貪欲法は最短より<strong>42.5%長い</strong>結果になりました。'
     '貪欲法の進み方を見ると、近い家（A宅・B宅・C宅・E宅）を先に回り、'
     '遠方のD宅を<strong>いちばん最後に残して</strong>います。'
     'E宅から遠方のD宅へ14.9、そこから営業所へ戻るのに12.5かかり、'
     '最後の2回の移動だけで27.4を使っています。'
     '最短ルートでは、B宅の次に遠方のD宅へ行き、帰り道にC宅とE宅を回ることで、長い移動を1回で済ませています。')}

{notion('例題4の実行結果から、貪欲法の進み方（6行）をすべて書き写す。'
        'あわせて、貪欲法が遠方のD宅を最後に残してしまう理由と、最短ルートがどこで違う判断をしているかを説明する。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('09', ['AL2-09-ex1.py', 'AL2-09-ex2.py', 'AL2-09-ex3.py', 'AL2-09-ex4.py'])}

{keywords([
    ('貪欲法', 'どんよくほう / greedy algorithm', '先のことを考えず、その時点でいちばん良さそうな選択をくり返す方法。速いが最適とはかぎらない。'),
    ('最近傍法', 'さいきんぼうほう / nearest neighbor', '巡回セールスマン問題に貪欲法を使ったもの。いまいる都市からいちばん近い都市へ進む。'),
    ('局所最適', 'きょくしょさいてき / local optimum', '部分的にはいちばん良いが、全体で見るといちばん良いとはかぎらない状態。'),
    ('近似解', 'きんじかい / approximate solution', '最適解ではないが、実用上じゅうぶん良い答え。速く求められることが利点。'),
    ('最適解', 'さいてきかい / optimal solution', '考えられる中で本当にいちばん良い答え。全探索や動的計画法で求まる。'),
])}

{example(1, '貪欲法で5都市を解く', ex1_body)}

{example(2, '8都市で全探索と比べる', ex2_body)}

{example(3, '出発点を変えると答えが変わる', ex3_body)}

{example(4, '貪欲法が大きく損をする配置', ex4_body)}"""

std1_body = """      <p>例題4のファイル <code>AL2-09-ex4.py</code> を開き、<strong>出発点を変えて</strong>貪欲法を動かします。
      いちばん下の行を次のように書き換えると、営業所以外からも出発できます。</p>

<pre><span class="code-label">Python ── 書き足す行（ファイルの末尾に追加）</span>
<span class="fn">print</span>()
<span class="fn">print</span>(<span class="str">"出発点を変えたときの貪欲法の答え"</span>)
<span class="kw">for</span> start <span class="kw">in</span> <span class="fn">range</span>(n):
    route, total, steps = <span class="fn">greedy</span>(start)
    <span class="fn">print</span>(<span class="str">" "</span>, houses[start][<span class="num">0</span>], <span class="str">"から出発:"</span>, <span class="fn">round</span>(total, <span class="num">1</span>))</pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、6つの出発点それぞれで貪欲法の答えがどうなるかを予測してNotionに書く（数値でなく「32.7に近い／46.6に近い」でよい）</li>
          <li>上の3行を <code>AL2-09-ex4.py</code> の末尾に書き足して保存し、実行する</li>
          <li>6つの結果を表にまとめる</li>
          <li>いちばん良かった出発点といちばん悪かった出発点を答える</li>
        </ol>
      </div>

      <table>
        <tr><th>出発点</th><th>予測</th><th>実際の合計距離</th><th>最短(32.7)との差</th></tr>
        <tr><td>営業所</td><td></td><td>46.6</td><td>13.9</td></tr>
        <tr><td>A宅</td><td></td><td></td><td></td></tr>
        <tr><td>遠方のD宅</td><td></td><td></td><td></td></tr>
        <tr><td>B宅</td><td></td><td></td><td></td></tr>
        <tr><td>E宅</td><td></td><td></td><td></td></tr>
        <tr><td>C宅</td><td></td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 遠方のD宅から出発したときの結果は、ほかの出発点と比べてどうでしたか。
      なぜそうなるのかを、貪欲法の進み方と結びつけて説明してください。</p>
"""

std2_body = """      <p>例題1から例題4までの結果をもとに、貪欲法についての説明をまとめます。
      Notionに次の4つの見出しを作り、それぞれ3行以上で書いてください。</p>

      <div class="setup-step">
        <p class="step-title">見出し1: 貪欲法の手順</p>
        <p style="font-size:0.95rem;color:#ccc">巡回セールスマン問題に貪欲法を使うとき、何をくり返すのかを、
        プログラムを見ていない人にも分かるように説明してください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">見出し2: 貪欲法の長所</p>
        <p style="font-size:0.95rem;color:#ccc">例題2で測った時間と、第8回で測った全探索の時間を根拠として挙げてください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">見出し3: 貪欲法の短所</p>
        <p style="font-size:0.95rem;color:#ccc">例題4の結果を根拠として、
        「局所最適」という言葉を使って説明してください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">見出し4: 貪欲法を使ってよい場面・使ってはいけない場面</p>
        <p style="font-size:0.95rem;color:#ccc">次の3つの場面それぞれについて、
        貪欲法で足りるか、最適解が必要かを理由つきで答えてください。</p>
        <ul style="padding-left:1.5rem;font-size:0.92rem;line-height:1.9;color:#ccc">
          <li>場面A: 宅配便のドライバーが、その日の30軒の配達順をスマートフォンで決める</li>
          <li>場面B: 工場のドリルが、毎日同じ200か所の穴をあけ続ける（1回決めれば10年使う）</li>
          <li>場面C: 修学旅行の班別行動で、5か所を回る順番を決める</li>
        </ul>
      </div>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。</p>

{standard(1, '出発点を変えると貪欲法の答えはどう変わるか', std1_body)}
{notion('6つの出発点についての予測と実際の表、いちばん良かった出発点と悪かった出発点、および「遠方のD宅から出発したとき」の考察。')}

{standard(2, '貪欲法について説明する', std2_body)}
{notion('見出し1〜見出し4のそれぞれについて、3行以上の説明。見出し4は場面A・B・Cすべてに答える。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第9回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 距離・時間・順番の数の表、入れかわっている都市</li>
        <li><strong>例題4</strong>: 貪欲法の進み方6行、遠方のD宅が最後に残る理由</li>
        <li><strong>標準課題1</strong>: 6つの出発点の予測と実際、遠方のD宅から出発した場合の考察</li>
        <li><strong>標準課題2</strong>: 見出し1〜4の説明</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

_g = {}
for _s in range(len(HOUSES)):
    _r, _t = greedy(HOUSES, _s)
    _g[HOUSES[_s][0]] = round(_t, 1)
_opt_h = round(optimal(HOUSES)[1], 1)
_rows = "\n".join(
    f'          <tr><td>{name}</td><td>{v}</td><td>{round(v-_opt_h,1)}</td></tr>'
    for name, v in _g.items())

ans = answers([
    ("標準課題1: 出発点を変えたときの結果", f"""        <table>
          <tr><th>出発点</th><th>合計距離</th><th>最短({_opt_h})との差</th></tr>
{_rows}
        </table>
        <p style="margin-top:0.8rem"><strong>いちばん良かった出発点:</strong> 遠方のD宅 と B宅（どちらも {min(_g.values())} で、全探索の最短と一致）<br>
        <strong>いちばん悪かった出発点:</strong> {max(_g, key=_g.get)}（{max(_g.values())}）</p>
        <p style="margin-top:0.6rem"><strong>遠方のD宅から出発したときの考察:</strong>
        遠方のD宅から出発すると、答えは {min(_g.values())} となり、全探索で求めた最短と完全に一致しました。
        営業所から出発した46.6と比べて、13.9も短くなっています。</p>
        <p style="margin-top:0.6rem">理由は、貪欲法が損をするパターンが起きないからです。
        貪欲法が損をするのは<strong>遠い場所を最後まで残してしまい、そこへ行って戻る往復で大きく損をする</strong>ときです。
        営業所から出発した場合、D宅は最後まで残され、E宅→D宅（14.9）とD宅→営業所（12.5）の2回で27.4もかかりました。
        D宅そのものを出発点にすると、D宅への長い移動は<strong>帰りの1回だけ</strong>になり、往復にならずに済みます。</p>
        <p style="margin-top:0.6rem">B宅から出発したときも同じ32.7になっています。
        B宅はD宅にいちばん近い家なので、貪欲法が早い段階でD宅へ向かう形になり、やはり取り残しが起きません。</p>
        <p style="margin-top:0.6rem">貪欲法の弱点は「遠い場所を後回しにしてしまうこと」です。
        遠い場所そのものを出発点にすると、その弱点が出にくくなります。
        ただし、どの出発点が良いかは<strong>実際に試してみないと分かりません</strong>。
        だからこそ、例題3のように「すべての出発点で試して、いちばん良い答えを採用する」やり方が有効になります。</p>"""),
    ("標準課題2: 貪欲法についての説明", """        <p><strong>見出し1: 貪欲法の手順</strong></p>
        <p style="margin-top:0.4rem">出発する場所を1つ決めます。そこから、まだ行っていない場所のうち
        <strong>いま自分がいる場所からいちばん近い場所</strong>を選んで移動します。
        移動したら、そこを新しい「いまいる場所」として、同じことをくり返します。
        行っていない場所がなくなったら、最後に出発点へ戻ります。
        先のことは一切考えず、そのときいちばん近い場所を選び続けるだけです。</p>

        <p style="margin-top:0.8rem"><strong>見出し2: 貪欲法の長所</strong></p>
        <p style="margin-top:0.4rem">とにかく速いことです。
        例題2の8都市では、全探索が5,040通りを調べて0.00089秒かかったのに対し、
        貪欲法は0.000006秒で、およそ<strong>150倍</strong>速く終わりました。
        差は都市が増えるほど広がります。第8回で確かめたように、全探索は12都市で8.7秒、
        15都市では24時間以上かかりますが、貪欲法は1000都市でも一瞬で終わります。
        調べる手数が (n-1)! 通りから n×n 程度に減るためです。</p>

        <p style="margin-top:0.8rem"><strong>見出し3: 貪欲法の短所</strong></p>
        <p style="margin-top:0.4rem">最短ルートを見つけるとはかぎらないことです。
        例題4では、貪欲法の答えが46.6で、本当の最短32.7より<strong>42.5%も長く</strong>なりました。
        原因は、貪欲法が1歩先しか見ていないことです。
        近い家から順に回った結果、遠方のD宅だけが最後に取り残され、
        そこへ行って戻るだけで27.4もかかってしまいました。
        「その時点ではいちばん近い家を選んだ」という判断は部分的には正しいのに、
        全体では損をしています。この状態を<strong>局所最適</strong>と呼びます。</p>

        <p style="margin-top:0.8rem"><strong>見出し4: 使ってよい場面・使ってはいけない場面</strong></p>
        <ul class="point-list">
          <li><strong>場面A（30軒の配達順をその場で決める）: 貪欲法で足りる。</strong>
          30軒の全探索は 29! 通りで、まったく終わりません。
          出発前の数秒で答えを出す必要があるので、多少長くても速く出せることが優先されます。
          例題3のように複数の出発点で試して、いちばん良いものを選べばさらに良くなります。</li>
          <li><strong>場面B（200か所を10年使い続ける）: 最適解を求めるべき。</strong>
          1回決めれば長く使うので、計算に何時間かけても割に合います。
          10%短くなれば、10年ぶんの電気代と作業時間がそれだけ減ります。
          200都市では全探索は使えないので、第10回で学ぶ動的計画法や、
          専用の最適化ソフトを使うことになります。</li>
          <li><strong>場面C（5か所を回る順番）: どちらでもよい。</strong>
          5か所なら全探索は24通りしかなく、手で計算しても終わります。
          必ず最短が求まるので、全探索を選ぶほうが確実です。</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        「どれくらいの時間で答えがほしいか」と「最短でなくても許されるか」の2つで決めます。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "貪欲法とは", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("09", NAV, body)
