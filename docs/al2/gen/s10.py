# -*- coding: utf-8 -*-
"""第10回: 巡回セールスマン問題（3）動的計画法 の本文を組み立てる。
例題は「参考（学校など5都市）」と「クリエイティブ演習（ナガシマスパーランドのスタンプカードと、bitDP で求める本当の最短）」の2本立て。"""
import ast
import math
import re
from slides_data import SLIDES
from slide_examples import slide_example
from common import (HERE, plain, slide_submission, slides_for, rubric_section, advanced_section, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, section, setup_guide, write)
from pyhl import highlight   # noqa: E402（common が読みこみ先を追加したあとで読む）

CITIES = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9), ("カフェ", 6, 12), ("公園", 3, 8)]
INF = float("inf")


def template_value(filename, name, pattern):
    """演習のひな形（src のファイル）に書いてある値を読みとる。本文の数値をひな形と必ず一致させるため。"""
    src = (HERE / "src" / filename).read_text(encoding="utf-8")
    return ast.literal_eval(re.search(rf"^{name} = ({pattern})", src, re.S | re.M).group(1))


NAGA = template_value("AL2-10-ex2.py", "spots", r"\[\n.*?\n\]")
assert NAGA == template_value("AL2-10-ex1.py", "spots", r"\[\n.*?\n\]"), "演習1と演習2のひな形の spots がちがう"
BEEN = template_value("AL2-10-ex1.py", "been", r"\[.*?\]")
NEXT = template_value("AL2-10-ex1.py", "NEXT", r'".*?"')
CODE = template_value("AL2-10-ex1.py", "CODE", r"\d+")


def table(cs):
    """距離の表（例題・演習と同じく、小数第1位に丸める）。"""
    n = len(cs)
    return [[round(math.hypot(cs[i][1] - cs[j][1], cs[i][2] - cs[j][2]), 1) for j in range(n)] for i in range(n)]


def bit_dp(cs):
    """例題・演習と同じ bitDP。回る順番・合計・表 best を返す。"""
    t = table(cs)
    n = len(cs)
    best = [[INF] * n for _ in range(1 << n)]
    prev = [[None] * n for _ in range(1 << n)]
    best[1][0] = 0
    for v in range(1 << n):
        for h in range(n):
            if best[v][h] == INF:
                continue
            for x in range(n):
                if v & (1 << x):
                    continue
                if best[v][h] + t[h][x] < best[v | (1 << x)][x]:
                    best[v | (1 << x)][x] = best[v][h] + t[h][x]
                    prev[v | (1 << x)][x] = h
    full = (1 << n) - 1
    answer, last = INF, None
    for h in range(1, n):
        if best[full][h] + t[h][0] < answer:
            answer, last = best[full][h] + t[h][0], h
    route, v, h = [], full, last
    while h is not None:
        route.append(h)
        v, h = v - (1 << h), prev[v][h]
    route.reverse()
    return route, round(answer, 1), best


def greedy(cs):
    t = table(cs)
    n = len(cs)
    route, here = [0], 0
    while len(route) < n:
        nearest = None
        for j in range(n):
            if j in route:
                continue
            if nearest is None or t[here][j] < t[here][nearest]:
                nearest = j
        route.append(nearest)
        here = nearest
    return route, round(sum(t[a][b] for a, b in zip(route, route[1:] + [0])), 1)


def names(cs, route, back=True):
    seq = list(route) + ([route[0]] if back else [])
    return " → ".join(cs[i][0] for i in seq)


def bits(v, n):
    return format(v, f"0{n}b")


def members(cs, v):
    return [cs[i][0] for i in range(len(cs)) if v & (1 << i)]


T5 = table(CITIES)
R5, L5, BEST5 = bit_dp(CITIES)
FILLED5 = sum(1 for row in BEST5 for x in row if x != INF)
TN = table(NAGA)
RN, LN, BESTN = bit_dp(NAGA)
GN, GN_LEN = greedy(NAGA)
PN = round(round(GN_LEN - LN, 1) / LN * 100, 1)
NN = len(NAGA)
NAGA_NAMES = [s[0] for s in NAGA]
assert GN_LEN > LN and FILLED5 == 33


# ────────────────────────────────────────────────────────────
# 図0: 第9回の貪欲法と、今回の bitDP を並べて動かす（ナガシマスパーランドのひな形）
# ────────────────────────────────────────────────────────────
def fig_vs_greedy():
    cs, n, dur = NAGA, NN, 20
    sx, sy = 18, 16

    def pos(i, x0):
        return x0 + 40 + (cs[i][1] - 3) * sx, 124 + (cs[i][2] - 3) * sy

    def show(a, b=None):
        """a の時点で現れる（b があれば、b の時点で消える）アニメーション。時点は 0〜1。"""
        if b is None:
            return (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{a:.3f};{a+0.015:.3f};1" '
                    f'dur="{dur}s" repeatCount="indefinite"/>')
        return (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.015:.3f};{b:.3f};{b+0.015:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')

    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ6か所を、第9回の貪欲法と、今回の bitDP で回る</text>']
    panels = [(20, "第9回: 貪欲法", AMBER), (370, "第10回: bitDP", GREEN)]
    for x0, title, color in panels:
        s.append(f'        <rect x="{x0}" y="42" width="310" height="296" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+155}" y="64" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
    # ── 左: 貪欲法。いちばん近い場所への線が、1本ずつ増える（0.04〜0.40）──
    gx = 20
    loop = GN + [0]
    for k in range(n):
        a, b = loop[k], loop[k + 1]
        (x1, y1), (x2, y2) = pos(max(a, b), gx), pos(min(a, b), gx)
        at = 0.04 + 0.06 * k
        s.append(f'        <g opacity="0">{show(at)}')
        s.append(f'          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AMBER}" stroke-width="3"/>')
        s.append(f'          <text x="{x1+(x2-x1)*0.38:.0f}" y="{y1+(y2-y1)*0.38-6:.0f}" text-anchor="middle" fill="{AMBER}" stroke="#141414" stroke-width="3" paint-order="stroke" font-size="10" font-weight="700">{TN[a][b]}</text>')
        s.append('        </g>')
        label = "最後に、メインゲートへ戻る" if k == n - 1 else f"{k+1}回目: いちばん近い {cs[b][0]} へ"
        s.append(f'        <text x="{gx+155}" y="84" text-anchor="middle" fill="#ccc" font-size="11" opacity="0">{show(at, at+0.045)}{label}</text>')
    s.append(f'        <text x="{gx+155}" y="84" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700" opacity="0">'
             f'{show(0.41)}合計 {GN_LEN}分（えらんだのは {n-1}回だけ）</text>')
    # ── 右: bitDP。表が埋まっていき（0.44〜0.74）、最後に最短ルートが出る（0.78）──
    bx = 370
    cells_by_size = [sum(1 for v in range(1 << n) for h in range(n) if bin(v).count("1") == k and BESTN[v][h] != INF)
                     for k in range(1, n + 1)]
    done = 0
    bar_x, bar_w = bx + 30, 250
    s.append(f'        <g opacity="0">{show(0.43, 0.76)}')
    s.append(f'          <rect x="{bar_x}" y="92" width="{bar_w}" height="8" rx="4" fill="#222" stroke="#444"/>')
    s.append('        </g>')
    total_cells = sum(cells_by_size)
    for k, c in enumerate(cells_by_size):
        done += c
        at = 0.44 + 0.05 * k
        s.append(f'        <rect x="{bar_x}" y="92" width="{bar_w*done/total_cells:.0f}" height="8" rx="4" fill="{GREEN}" opacity="0">{show(at, 0.76)}</rect>')
        s.append(f'        <text x="{bx+155}" y="84" text-anchor="middle" fill="#ccc" font-size="11" opacity="0">{show(at, at+0.035)}'
                 f'表を埋める: {k+1}か所回った状態（ここまで {done}マス）</text>')
    rloop = RN + [0]
    s.append(f'        <g opacity="0">{show(0.78)}')
    for k in range(n):
        a, b = rloop[k], rloop[k + 1]
        (x1, y1), (x2, y2) = pos(max(a, b), bx), pos(min(a, b), bx)      # 数字の位置を左の図とそろえる（番号の大きいほうの近く）
        s.append(f'          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="3"/>')
        s.append(f'          <text x="{x1+(x2-x1)*0.38:.0f}" y="{y1+(y2-y1)*0.38-6:.0f}" text-anchor="middle" fill="{GREEN}" stroke="#141414" stroke-width="3" paint-order="stroke" font-size="10" font-weight="700">{TN[a][b]}</text>')
    s.append(f'          <text x="{bx+155}" y="84" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             f'合計 {LN}分（表の {total_cells}マスを調べて、必ず最短）</text>')
    s.append('        </g>')
    # 場所の丸と名前（線の上に重ねる）
    for x0, _, color in panels:
        for i, (name, _x, _y) in enumerate(cs):
            cx, cy = pos(i, x0)
            s.append(f'        <circle cx="{cx}" cy="{cy}" r="10" fill="#1A1A1A" stroke="{AMBER if i == 0 else color}" stroke-width="2"/>')
            s.append(f'        <text x="{cx}" y="{cy+4}" text-anchor="middle" fill="#E0E0E0" font-size="10" font-weight="700">{i}</text>')
            short = name if len(name) <= 8 else name[:8]
            s.append(f'        <text x="{cx}" y="{cy+23}" text-anchor="middle" fill="{GRAY}" stroke="#141414" stroke-width="3" paint-order="stroke" font-size="9">{short}</text>')
    late = round(GN_LEN - LN, 1)
    s.append(f'        <text x="350" y="362" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700" opacity="0">{show(0.84)}'
             f'貪欲法は {late}分（{PN}%）おそい。bitDP は、全探索と同じ「本当の最短」を出す</text>')
    s.append(f'        <text x="350" y="382" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '線の数字 = 歩く分。貪欲法は目の前の近さだけでえらび、bitDP は全部の状態を表に書いてからえらぶ</text>')
    return fig(700, 396, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図1: 全探索は同じ計算をくり返している
# ────────────────────────────────────────────────────────────
def fig_duplicate():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索は、同じ計算を何度もくり返している</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '2つの道は、通ってきた順番だけがちがう。着いた場所も、回り終えた都市も同じ</text>']
    paths = [("道A", ["0", "1", "2", "3"], 92), ("道B", ["0", "2", "1", "3"], 176)]
    for title, seq, y in paths:
        s.append(f'        <text x="40" y="{y+6}" fill="#ccc" font-size="12" font-weight="700">{title}</text>')
        for k, node in enumerate(seq):
            cx = 130 + k * 78
            col = AMBER if k == len(seq) - 1 else GREEN
            s.append(f'        <circle cx="{cx}" cy="{y}" r="18" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
            s.append(f'        <text x="{cx}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="13" font-weight="700">{node}</text>')
            if k < len(seq) - 1:
                s.append(f'        <line x1="{cx+18}" y1="{y}" x2="{cx+60}" y2="{y}" stroke="{GREEN}" stroke-width="2"/>')
                s.append(f'        <polygon points="{cx+60},{y} {cx+52},{y-4} {cx+52},{y+4}" fill="{GREEN}"/>')
        s.append(f'        <line x1="{130+3*78+18}" y1="{y}" x2="{130+3*78+70}" y2="{y}" stroke="#555" stroke-width="2" stroke-dasharray="5 4"/>')
        s.append(f'        <text x="{130+3*78+80}" y="{y+5}" fill="{GRAY}" font-size="11">この先は同じ</text>')
    s.append(f'        <rect x="112" y="66" width="{3*78+40}" height="146" rx="12" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append(f'        <rect x="130" y="238" width="440" height="86" rx="10" fill="#141414" stroke="{AMBER}"/>')
    s.append(f'        <text x="350" y="262" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '道Aと道Bに共通していること</text>')
    s.append(f'        <text x="350" y="284" text-anchor="middle" fill="#ccc" font-size="11">'
             '回った都市の集合 = 0・1・2・3　／　いまいる都市 = 3</text>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="#ccc" font-size="11">'
             'ここから先のいちばん短い進み方は、どちらの道で来ても同じになる</text>')
    s.append(f'        <text x="350" y="348" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             '短いほうの距離だけを覚えておけば、長いほうは二度と調べなくてよい</text>')
    return fig(700, 364, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: ビットで集合を表す
# ────────────────────────────────────────────────────────────
def fig_bits():
    labels = [c[0] for c in CITIES]
    examples = [(0, "まだどこにも行っていない"), (1, "学校だけ"), (5, "学校と図書館"),
                (7, "学校・郵便局・図書館"), (31, "5つ全部")]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '「回った都市の集合」を、数1つ（2進数）で表す</text>']
    cell = 78
    x0 = 152
    for i, name in enumerate(labels):
        x = x0 + (4 - i) * cell
        s.append(f'        <text x="{x+cell/2-2}" y="66" text-anchor="middle" fill="{GRAY}" font-size="11">{name}</text>')
        s.append(f'        <text x="{x+cell/2-2}" y="82" text-anchor="middle" fill="#555" font-size="9">{i}番</text>')
    for k, (value, label) in enumerate(examples):
        y = 96 + k * 44
        a = (1 - 0.16) * k / len(examples)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{a:.3f};{min(a+0.02,0.999):.3f};1" '
                f'dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <text x="130" y="{y+24}" text-anchor="end" fill="#ccc" font-size="13" font-weight="700">{value}</text>')
        for i in range(5):
            x = x0 + (4 - i) * cell
            on = bool(value & (1 << i))
            s.append(f'          <rect x="{x}" y="{y}" width="{cell-6}" height="34" rx="6" '
                     f'fill="{"#1a2e0a" if on else "#141414"}" stroke="{GREEN if on else "#2e2e2e"}"/>')
            s.append(f'          <text x="{x+(cell-6)/2}" y="{y+23}" text-anchor="middle" '
                     f'fill="{"#93D500" if on else "#555"}" font-size="15" font-weight="700">{1 if on else 0}</text>')
        s.append(f'          <text x="{x0+5*cell+8}" y="{y+23}" fill="{GRAY}" font-size="11">{label}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{96+5*44+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '5個の都市なら、集合は 0 から 31 までの32通りの数で全部表せる（右はしが0番のけた）</text>')
    return fig(700, 96 + 5 * 44 + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 表の作り方（例題2の本当の値で描く）
# ────────────────────────────────────────────────────────────
A_FROM, A_TO = 0b00111, 0b01111        # 図と説明で使う「表の1マスから次のマスへ」の例
A_GOOD = round(BEST5[A_FROM][2] + T5[2][3], 1)       # 図書館（2番）からカフェ（3番）へ
A_BAD = round(BEST5[A_FROM][1] + T5[1][3], 1)        # 郵便局（1番）からカフェ（3番）へ
assert A_GOOD == round(BEST5[A_TO][3], 1) and A_GOOD < A_BAD


def fig_dp_table():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'bitDP が作る表: たてが「回った集合」、よこが「いまいる都市」</text>']
    s.append(f'        <rect x="40" y="52" width="620" height="82" rx="10" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="76" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             'best[回った集合][いまいる都市] = そこまでの、いちばん短い合計距離</text>')
    s.append(f'        <text x="350" y="100" text-anchor="middle" fill="#ccc" font-size="11">'
             f'best[00111][2] = {BEST5[A_FROM][2]:.1f} は「学校・郵便局・図書館を回り終えて、いま2番の図書館にいる」ときの最短距離</text>')
    s.append(f'        <text x="350" y="122" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '同じマスに何通りの道でたどり着いても、いちばん短い値だけを残す</text>')
    s.append(f'        <text x="350" y="164" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">'
             '表の1マスから、次のマスへ値を書きこむ</text>')
    boxes = [(80, "00111 の集合", "いま 2番（図書館）にいる", f"{BEST5[A_FROM][2]:.1f}", GREEN),
             (420, "01111 の集合", "いま 3番（カフェ）にいる", f"{BEST5[A_FROM][2]:.1f} + {T5[2][3]} = {A_GOOD}", AMBER)]
    for x, l1, l2, val, color in boxes:
        s.append(f'        <rect x="{x}" y="188" width="200" height="92" rx="10" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>')
        s.append(f'        <text x="{x+100}" y="212" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">{l1}</text>')
        s.append(f'        <text x="{x+100}" y="232" text-anchor="middle" fill="#ccc" font-size="11">{l2}</text>')
        s.append(f'        <text x="{x+100}" y="262" text-anchor="middle" fill="#E0E0E0" font-size="14" font-weight="700">{val}</text>')
    s.append('        <line x1="286" y1="234" x2="414" y2="234" stroke="#666" stroke-width="2"/>')
    s.append('        <polygon points="414,234 404,229 404,239" fill="#666"/>')
    s.append(f'        <text x="350" y="224" text-anchor="middle" fill="{GRAY}" font-size="11">3番のカフェへ移動</text>')
    s.append(f'        <text x="350" y="252" text-anchor="middle" fill="{GRAY}" font-size="10">距離 {T5[2][3]}</text>')
    s.append(f'        <text x="350" y="308" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'すべてのマスについて同じことをすれば、全部の状態の最短距離が求まる</text>')
    return fig(700, 324, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 増え方の比較
# ────────────────────────────────────────────────────────────
def fig_growth_compare():
    rows = []
    for n in [10, 12, 14, 16, 18, 20]:
        rows.append((n, (1 << n) * n, math.factorial(n - 1)))
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索と bitDP の「調べる量」の増え方</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは、10倍ごとに1目もり（棒が少し長いだけで、数は何けたも大きい）</text>']
    for i, (n, cells, fact) in enumerate(rows):
        y = 64 + i * 62
        s.append(f'        <text x="24" y="{y+24}" fill="#E0E0E0" font-size="12" font-weight="700">{n}か所</text>')
        wf = math.log10(fact) / 19 * 400
        wc = math.log10(cells) / 19 * 400
        s.append(f'        <text x="104" y="{y+16}" fill="{RED}" font-size="10">全探索</text>')
        s.append(f'        <rect x="160" y="{y+2}" width="{wf:.0f}" height="18" rx="4" fill="{RED}" opacity="0.85"/>')
        s.append(f'        <text x="{160+wf+8:.0f}" y="{y+16}" fill="{RED}" font-size="10">{fact:,}通り</text>')
        s.append(f'        <text x="104" y="{y+40}" fill="{GREEN}" font-size="10">bitDP</text>')
        s.append(f'        <rect x="160" y="{y+26}" width="{wc:.0f}" height="18" rx="4" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{160+wc+8:.0f}" y="{y+40}" fill="{GREEN}" font-size="10">{cells:,}マス</text>')
    s.append(f'        <text x="350" y="{64+6*62+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '20か所では、全探索が約12京通り。bitDP は約2千万マスですむ</text>')
    return fig(700, 64 + 6 * 62 + 34, "\n".join(s))


def pycode(src, label):
    """Python のコードを色つきの <pre> にする（本文の説明用）。"""
    return f'<pre data-blanks="0"><span class="code-label">{label}</span>\n{highlight(src)}</pre>'


def level_table():
    """例題2の表が、回った都市の数ごとにどう埋まるか（窓の1手順 = この表の1行）。"""
    rows = []
    n = 5
    for k in range(1, n + 1):
        sets = [v for v in range(1 << n) if bin(v).count("1") == k and v & 1]
        cells = [(v, h) for v in sets for h in range(n) if BEST5[v][h] != INF]
        v, h = cells[-1]
        rows.append(f'          <tr><td style="white-space:nowrap">{k}手順目</td><td>{k}個</td><td>{len(sets)}個</td><td>{len(cells)}個</td>'
                    f'<td><code>best[{bits(v, n)}][{h}] = {BEST5[v][h]:.1f}</code>（{"・".join(members(CITIES, v))}を回って、いま{CITIES[h][0]}）</td></tr>')
    return ('        <table>\n          <tr><th></th><th>回った都市の数</th><th>集合（行）の数</th><th>値が入るマス</th><th>マスの例</th></tr>\n'
            + "\n".join(rows) + f'\n          <tr><td>合計</td><td></td><td>16個</td><td><strong>{FILLED5}個</strong></td>'
            '<td>全探索は24通りの順番を、それぞれ最後まで計算した</td></tr>\n        </table>')


def final_table():
    """全部回った行から答えを出すところ。"""
    full = 31
    rows = []
    for h in range(1, 5):
        total = round(BEST5[full][h] + T5[h][0], 1)
        mark = ' style="color:#76B900;font-weight:700"' if total == L5 else ""
        rows.append(f'          <tr><td>{h}（{CITIES[h][0]}）</td><td>{BEST5[full][h]:.1f}</td><td>{T5[h][0]}</td><td{mark}>{total}</td></tr>')
    return ('        <table>\n          <tr><th>here（最後にいる都市）</th><th>best[11111][here]</th><th>学校へ戻る距離</th><th>合計</th></tr>\n'
            + "\n".join(rows) + "\n        </table>")


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "動的計画法 #sec-explanation",
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("10")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第8回の全探索（すべての順番を試す方法）は必ず最短を出しますが、10か所をこえると待てなくなり、15か所では数時間かかる見積もりでした。
      第9回の貪欲法（いちばん近い場所へ進むことをくり返す方法）は一瞬で終わりますが、最短とはかぎりませんでした（ナガシマスパーランドのひな形では {PN}% おそい回り方でした）。
      第10回で学ぶ<strong>動的計画法</strong>（どうてきけいかくほう）は、
      <strong>必ず最短を出しながら、全探索よりずっと速い</strong>方法です。
      「貪欲法の回り方は、本当の最短より何分おそいのか」を、全探索では確かめられなかった15か所でも確かめられるようになります。
    </p>

{fig_vs_greedy()}

    <p style="margin-bottom:1.5rem">
      上の図は、演習のひな形の6か所を、2つの方法で回ったものです。
      左の貪欲法は、いちばん近い場所を5回えらぶだけで回り方が決まります。
      右の bitDP は、先に表を埋めてから回り方を決めるので手間はかかりますが、出てくるのは必ず最短の回り方です。
      貪欲法は、大観覧車オーロラから近いアクロバットを先にえらんだため、最後に白鯨からメインゲートまでの長い道が残りました。
    </p>

    <div class="analogy">
      ナガシマスパーランドで、友だちと別べつに回って、とちゅうで合流した場面を思い浮かべてください。
      2人とも「スチールドラゴン2000・嵐・白鯨の3つに乗り終えて、いま白鯨の前にいる」とします。
      あなたは「スチールドラゴン → 嵐 → 白鯨」の順で30分、友だちは「嵐 → スチールドラゴン → 白鯨」の順で25分かかりました。
      ここから先、残りの乗り物をどう回るのがいちばん早いかは、<strong>2人ともまったく同じ</strong>です。
      乗り終えたものが同じで、いまいる場所も同じだからです。<strong>どの順番で乗ってきたかは、この先には関係ありません。</strong>
      だとすれば、25分のほうだけをメモしておけばよく、30分かかった順番の続きは、もう考えなくてすみます。
      動的計画法は、この<strong>「同じ状況に着いたら、いちばん良い記録だけをメモして、続きの計算を使い回す」</strong>という考え方です。
    </div>

    <div class="concept-box">
      <h4>全探索のむだ</h4>
      <p style="font-size:0.95rem">
        全探索は「0 → 1 → 2 → 3 → …」と「0 → 2 → 1 → 3 → …」を、まったく別のものとして最後まで調べます。
        しかし2つの道は、4つ目の都市に着いた時点で<strong>状況がまったく同じ</strong>です。
        どちらも「0・1・2・3 を回り終えて、いま 3 にいる」からです。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        残っている都市も同じ、いる場所も同じなので、<strong>ここから先のいちばん短い進み方も同じ</strong>になります。
        ちがうのは「ここまでにかかった距離」だけです。
        <strong>短いほうの距離だけを覚えておけばじゅうぶん</strong>で、長いほうの道の続きは、もう調べる必要がありません。
        全探索は、この「続き」を道Aでも道Bでも1から計算し直していました。
      </p>
    </div>

{fig_duplicate()}

    <div class="concept-box">
      <h4>覚えておく2つのこと ── 「状態」</h4>
      <table>
        <tr><th>覚えること</th><th>意味</th><th>コードでの名前</th></tr>
        <tr><td>回った都市の集合</td><td>どの都市をすでに回ったか（<strong>順番は関係ない</strong>）</td><td><code>visited</code></td></tr>
        <tr><td>いまいる都市</td><td>最後に着いた都市</td><td><code>here</code></td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        この2つの組を<strong>状態</strong>（じょうたい）と呼びます。「いま、どういう状況か」を表す情報、という意味です。
        「集合」（しゅうごう）は、順番を気にしない「ものの集まり」のことです。
        状態が同じなら、そこまでの<strong>いちばん短い距離だけ</strong>を表に書いておきます。
        一度計算した答えをメモしておいて使い回すことを<strong>メモ化</strong>と呼び、動的計画法の中心になる考え方です。
        動的計画法は、英語の Dynamic Programming の頭文字から <strong>DP</strong>（ディーピー）とも呼ばれます。
      </p>
    </div>

{fig_bits()}

    <div class="concept-box">
      <h4>集合を、数1つで表す ── ビット</h4>
      <p style="font-size:0.95rem">
        「回った都市の集合」を、Python のリストではなく<strong>1つの整数</strong>で表します。
        使うのは<strong>2進数</strong>（にしんすう: 0 と 1 だけで書く数の表し方。ふだん使う10進数の 5 は、2進数では 101 と書く）です。
        2進数の1けたを<strong>ビット</strong>と呼びます。
        都市が5個なら5けたの2進数を使い、<strong>i番の都市を回っていれば、右から数えて i番目のけた（右はしが0番）を 1</strong> にします。
        遊園地のスタンプカードで、行った場所のマスにスタンプを押すのと同じです。
      </p>
      <table>
        <tr><th>書き方</th><th>読み方</th><th>意味</th></tr>
        <tr><td style="white-space:nowrap"><code>1 &lt;&lt; i</code></td><td style="white-space:nowrap">左シフト</td><td>i番の都市だけを表す数（1 を左へ i けたずらす。<code>1 &lt;&lt; 3</code> は 2進数の 01000 = 8）</td></tr>
        <tr><td style="white-space:nowrap"><code>visited | (1 &lt;&lt; i)</code></td><td style="white-space:nowrap">または（or）</td><td>集合に i番の都市を<strong>足す</strong>（スタンプを押す）</td></tr>
        <tr><td style="white-space:nowrap"><code>visited &amp; (1 &lt;&lt; i)</code></td><td style="white-space:nowrap">かつ（and）</td><td>集合に i番の都市が<strong>入っているか</strong>調べる（0 以外なら入っている）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        整数1つで集合を表せるので、<code>best[visited][here]</code> のように
        <strong>リストの番号としてそのまま使えます</strong>。
        ビットを使った動的計画法なので、<strong>bitDP</strong>（ビットディーピー）と呼ばれます。
        3つの記号の使い方は、例題1と演習1で練習します。
      </p>
    </div>

{fig_dp_table()}

{fig_growth_compare()}

    <div class="concept-box">
      <h4>3つの方法を並べる</h4>
      <table>
        <tr><th></th><th>全探索（第8回）</th><th>貪欲法（第9回）</th><th>bitDP（第10回）</th></tr>
        <tr><td>答えの質</td><td>必ず最短</td><td>最短とはかぎらない</td><td><strong>必ず最短</strong></td></tr>
        <tr><td>調べる量</td><td>(n−1)! 通りの順番</td><td>n × (n−1) ÷ 2 回の比べ</td><td>2<sup>n</sup> × n マスの表</td></tr>
        <tr><td>10か所</td><td>362,880通り</td><td>45回</td><td>10,240マス</td></tr>
        <tr><td>15か所</td><td>約870億通り（数時間）</td><td>105回</td><td>491,520マス（1秒かからない）</td></tr>
        <tr><td>20か所</td><td>約12京通り（何百年）</td><td>190回</td><td>約2千万マス（数秒〜数十秒）</td></tr>
        <tr><td>弱点</td><td>10か所をこえると待てない</td><td>答えが最短とはかぎらない</td><td>表を覚えておくメモリが要る。25か所をこえるとむずかしい</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        bitDP も万能ではありません。場所が1つ増えるたびに、表の大きさは2倍より少し多く増えます。
        25か所では表が約8億マスになり、時間より先に、パソコンのメモリ（計算のとちゅうの値を覚えておく場所）が足りなくなります。
        それでも、場所が1つ増えるたびに調べる量が何倍にもなる全探索（10か所から11か所で10倍、19か所から20か所で19倍）に比べれば、ずっとゆるやかです。
        「必ず最短がほしくて、20か所くらいまで」なら bitDP、「もっと多い」なら貪欲法、という使い分けになります。
      </p>
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>計算の進み方を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜9回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で表示します。
      例題1・演習1は<strong>集合を表す数の、1 と 0 のけたが変わるようす</strong>を、
      例題2は<strong>bitDP の表が埋まっていくようす</strong>を、
      演習2は<strong>貪欲法のルートと bitDP のルート（本当の最短）を左右に並べたもの</strong>を見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜9回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜9回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各ファイルの<strong>いちばん下</strong>
        （「ここから下は、…pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。</p>
      </div>
    </div>"""

trouble1 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習1）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>SyntaxError</code></td><td>かっこ・<code>"</code> の閉じ忘れ。<code>spots</code> の各行は <code>("白鯨", 15, 3),</code>、<code>been</code> は <code>["嵐", "白鯨"]</code> のように書く。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>been の「○」が spots にない</code></td><td>名前が1文字ちがう（「2000」のあるなし、全角と半角など）。<code>spots</code> の名前をコピーして貼る</td></tr>
          <tr><td><code>been に「○」が2回出てくる</code></td><td>同じ場所を2回書いた。1回だけにする（2回押しても、スタンプカードの数は変わらない）</td></tr>
          <tr><td><code>NEXT の「○」が spots にない</code></td><td>名前のまちがいか、<code>" "</code> で囲んでいない。<code>NEXT = "白鯨"</code> のように書く</td></tr>
          <tr><td><code>CODE は 0 から ○ までの整数で書こう</code></td><td>場所の数で表せる数より大きい（6か所なら 63 まで）。<code>" "</code> で囲まず、数だけを書く</td></tr>
          <tr><td>2進数のけたの数が、参考（5けた）とちがう</td><td>まちがいではない。けたの数 = 場所の数。6か所なら6けた、10か所なら10けたになる</td></tr>
          <tr><td>名前の順に並べたのに、2進数が逆に見える</td><td>2進数は<strong>右はしが0番</strong>。<code>spots</code> のいちばん上（0番）が、いちばん右のけたになる</td></tr>
        </table>
      </div>"""

trouble2 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習2）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td>第9回と貪欲法の時間がちがう</td><td><code>spots</code> か <code>WALK</code> を貼りかえ忘れた。第9回の <code>spots = [</code> から <code>]</code> までと、<code>WALK = …</code> の行をそのまま貼る。
              第9回の演習2で <code>#</code> を付けて減らしていた人は、同じ行に <code>#</code> が付いているかを見る</td></tr>
          <tr><td><code>spots が 17か所 ある。…</code></td><td>bitDP は表を全部覚えておくので、場所が多いとメモリも時間もかかる。残さない場所の行の先頭に <code>#</code> を付けて、<strong>16か所まで</strong>に減らす</td></tr>
          <tr><td><code>spots が少なすぎる。3か所だと …</code></td><td>メインゲートのほかに3か所以上にする</td></tr>
          <tr><td>第9回の全探索の回り方と、順番が逆</td><td>逆回りは同じ道を反対向きに歩くだけなので、合計は同じ。合計の分が同じなら正しい</td></tr>
          <tr><td>11か所以上にしたら、全探索の合計が出なくなった</td><td>まちがいではない。全探索は長すぎるので動かさず、見積もりだけを出している。bitDP の答えが「本当の最短」になる</td></tr>
          <tr><td>かかった時間が、実行のたびに少し変わる</td><td>ほかのアプリの動きなどで時間がゆれるため。だいたいの大きさを見ればよい</td></tr>
          <tr><td>ターミナルに結果が出るまで、数秒かかる</td><td>15〜16か所のときは、いちばん下の時間の表を作るのに bitDP を何回か動かしている。そのまま待つ</td></tr>
          <tr><td>貪欲法と bitDP が同じ時間になった</td><td>まちがいではない。貪欲法が、たまたま最短に当たった。場所を足したり動かしたりすると差が出る</td></tr>
        </table>
      </div>"""

missions1 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> を、<strong>第9回で作った自分のもの</strong>に貼りかえる（<code>spots = [</code> から <code>]</code> まで。16か所まで）。
              <code>been</code>（もう行った場所の名前）と <code>NEXT</code>（次に行きたい場所の名前）を、自分の場所の名前にする。<code>TITLE</code> も自分のものに。
              実行して、自分のスタンプカードの数（2進数と10進数）を確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>なぞの数</td><td><code>CODE</code> を、<strong>「全部の場所に行った」ことを表す数</strong>にする。ターミナルに「Lv2 達成」と出ればよい。
              ヒント: 2進数で 1 が場所の数だけ並ぶ数。まず <code>CODE</code> をいろいろな数にして、どの場所が出るかを試すとよい。場所の数を変えると、答えも変わる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>10か所以上</td><td>場所を<strong>10か所以上</strong>にする。ターミナルに「Lv3 達成」と出ればよい。
              「スタンプカードの種類」「回る順番の数」「bitDP の表のマスの数」の3つを見比べ、順番の数が表のマスの数の何倍あるかを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、自分らしい案内文にする。
              使える材料: <code>stamped</code>（スタンプがある場所の名前のリスト）、<code>left</code>（まだ行っていない場所の名前のリスト）。<code>len(left)</code> で残りの数が出る</td></tr>
        </table>
      </div>"""

missions2 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> と <code>WALK</code> を、<strong>第9回で作った自分のもの</strong>に貼りかえる（16か所まで）。
              bitDP が出した「本当にいちばん早い回り方」と、貪欲法の回り方が<strong>何分ちがうか（何%長いか）</strong>を確かめる。
              10か所までなら全探索も動くので、bitDP と同じ合計になることも確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>12か所以上</td><td>場所を<strong>12か所以上</strong>にして実行する。ターミナルに「Lv2 達成」と出ればよい。
              第9回では全探索が10か所までだったので、<strong>はじめて「12か所以上の本当の最短」が分かる</strong>。全探索ならどれくらいかかる見積もりかも見る</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>bitDP の限界</td><td>場所を<strong>15か所以上</strong>（16か所まで）にして、bitDP のかかった時間を測る。ターミナルに「Lv3 達成」と出ればよい。
              いちばん下の表で、20か所・25か所のときの<strong>3つの方法の時間</strong>を確かめる。<strong>標準課題で使うので、20か所の行をメモしておく</strong></td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、2つの回り方を自分らしく案内する。
              使える材料: <code>greedy_route</code>・<code>best_route</code>（回る場所の名前の並び）、<code>greedy_total</code>・<code>best_total</code>（合計の分）</td></tr>
        </table>
      </div>"""

OR_EXAMPLE = """  01011    visited（学校・郵便局・カフェ）
| 00100    1 << 2（図書館だけ）
-------
  01111    どちらかが 1 のけたは 1 → 図書館が足された"""

AND_EXAMPLE = """  01011    visited（学校・郵便局・カフェ）          01011    visited
& 00100    1 << 2（図書館だけ）                  & 01000    1 << 3（カフェだけ）
-------                                          -------
  00000    両方が 1 のけたがない → 0             01000    両方が 1 のけたがある → 0 ではない
           → 図書館は入っていない                         → カフェは入っている"""

ex1_body = f"""      <p>bitDP を書く前に、集合を数1つで表す練習をします。
      覚える記号は <code>&lt;&lt;</code>（ずらす）、<code>|</code>（足す）、<code>&amp;</code>（入っているか調べる）の3つだけです。
      演習1では、同じしくみで<strong>ナガシマスパーランドの「行った場所のスタンプカード」</strong>を作ります。</p>

      <h4 style="margin:1.8rem 0 0.6rem">3つの記号の使い方</h4>
      <div class="concept-box">
        <h4>① <code>1 &lt;&lt; i</code> ── i番の都市だけを表す数を作る</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>&lt;&lt;</code> は「左へずらす」記号です。<code>1 &lt;&lt; i</code> は、2進数の 1 を左へ i けたずらした数になります。
        <code>1 &lt;&lt; 0</code> は 00001（= 1）、<code>1 &lt;&lt; 1</code> は 00010（= 2）、<code>1 &lt;&lt; 2</code> は 00100（= 4）、<code>1 &lt;&lt; 3</code> は 01000（= 8）です。
        1けたずらすたびに、数は2倍になります。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong>
        「i番のけただけが 1 の数」がほしいからです。この数を、下の <code>|</code> や <code>&amp;</code> と組み合わせて使います。</p>
      </div>
      <div class="concept-box">
        <h4>② <code>visited | (1 &lt;&lt; i)</code> ── 集合に i番の都市を足す</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>|</code>（たて棒。キーボードでは Shift を押しながら <code>¥</code> のキー）は、2つの数を2進数で上下に並べ、
        <strong>けたごとに「どちらかが 1 なら 1」</strong>にします。もともと 1 だったけたはそのままで、i番のけたが新しく 1 になります。</p>
{plain(OR_EXAMPLE, "考え方 ── | で図書館（2番）を足す")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜ <code>+</code> ではだめか:</strong>
        もう入っている都市を <code>+</code> で足すと、くり上がりが起きて別の集合になってしまいます（00100 + 00100 = 01000）。
        <code>|</code> なら、もう入っている都市を足しても何も変わりません。</p>
      </div>
      <div class="concept-box">
        <h4>③ <code>visited &amp; (1 &lt;&lt; i)</code> ── i番の都市が入っているか調べる</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>&amp;</code>（アンド）は、<strong>けたごとに「両方が 1 のときだけ 1」</strong>にします。
        <code>1 &lt;&lt; i</code> は i番のけたしか 1 ではないので、答えは「i番のけたが 1 なら 0 以外、0 なら 0」になります。</p>
{plain(AND_EXAMPLE, "考え方 ── & で、入っているかを調べる")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong><code>if visited &amp; (1 &lt;&lt; i):</code> と書ける理由:</strong>
        Python の <code>if</code> は、数が 0 なら「いいえ」、0 以外なら「はい」として扱います。だから <code>!= 0</code> を書かなくても、「入っていれば」という意味になります。</p>
      </div>

      <p style="margin-top:1rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>1 と 0 のマス</td><td>集合を表す2進数。<strong>右はしが0番</strong>のけた。緑のマス = 1（入っている）</td></tr>
        <tr><td>白いわく</td><td>いま足した（<code>|</code>）、または調べた（<code>&amp;</code>）けた</td></tr>
        <tr><td>橙の式</td><td>その手順で行った計算（2進数どうしの <code>|</code> や <code>&amp;</code>）</td></tr>
        <tr><td>下の2行</td><td>いまの集合の2進数と10進数、入っているものの名前</td></tr>
      </table>

{example_pair('AL2-10-ex1.py', '数 <strong>5</strong> は2進数で <code>00101</code> となり、'
     '右はし（0番の学校）と右から3つ目（2番の図書館）が 1 なので、「学校と図書館を回った」という意味になります。'
     '<code>1 &lt;&lt; 3</code> は <code>01000</code>（= 8）で、3番のカフェだけを表します。'
     '<code>|</code> で都市を1つずつ足していくと、00001 → 00011 → 00111 → 01111 → 11111 と、1 のけたが右から増えていきます。'
     '集合 5 に <code>&amp;</code> を使うと、学校と図書館のときだけ答えが 0 以外になりました。'
     '5個の都市なら、集合の種類は 0 から 31 までの32通りです。',
     creative=missions1)}
{trouble1}"""

BITDP_CODE = """best = []
prev = []
for visited in range(1 << count):             # ① 表を作る（行 = 集合、列 = いまいる都市）
    best.append([INF] * count)
    prev.append([None] * count)
best[1 << 0][0] = 0                           # ② はじめの状態: 0番だけ回って、0番にいる

for visited in range(1 << count):             # ③ 集合を、数の小さいほうから順に見る
    for here in range(count):
        if best[visited][here] == INF:        # ④ たどり着けない状態は飛ばす
            continue
        for next_city in range(count):
            if visited & (1 << next_city):    # ⑤ もう回った都市へは行かない
                continue
            new_visited = visited | (1 << next_city)          # ⑥ next_city を足した集合
            new_length = best[visited][here] + table[here][next_city]
            if new_length < best[new_visited][next_city]:     # ⑦ 短いときだけ書きかえる
                best[new_visited][next_city] = new_length
                prev[new_visited][next_city] = here

answer = INF
for here in range(1, count):                  # ⑧ 全部回った行に、0番へ戻る距離を足す
    total = best[full][here] + table[here][0]
    if total < answer:
        answer = total
        last = here"""

ex2_body = f"""      <p>bitDP で、第8・9回と同じ5つの都市の巡回セールスマン問題を解きます。
      <code>best[visited][here]</code> という表を作り、
      「<code>visited</code> の都市を回り終えて、いま <code>here</code> にいる」ときのいちばん短い距離を書きこんでいきます。
      演習2では、同じしくみで<strong>ナガシマスパーランドの本当にいちばん早い回り方</strong>を求め、第9回の貪欲法と比べます。</p>

      <h4 style="margin:1.8rem 0 0.6rem">bitDP のコードの書き方 ── 8つの大事な行</h4>
      <p>例題2の <code>bit_dp</code> 関数の中心は、次の部分です。
      <code>table</code> は第8回で作った距離の表（<code>table[i][j]</code> = i番から j番までの距離）、<code>count</code> は都市の数、
      <code>full</code> は全部の都市を回った集合（<code>(1 &lt;&lt; count) - 1</code>。5都市なら 11111 = 31）、
      <code>INF</code> は無限大（<code>float("inf")</code>。どんな数よりも大きい数で、「まだたどり着いていない」の印に使う）です。</p>
{pycode(BITDP_CODE, "Python ── 例題2の bitDP の部分（順番をたどる部分を省いたもの）")}

      <div class="concept-box">
        <h4>①② 表を作り、はじめの状態を書く</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>best</code> は、行が <code>1 &lt;&lt; count</code> 個（集合の数。5都市なら32行）、列が <code>count</code> 個（いまいる都市）の表です。
        はじめは全部のマスに INF を入れておきます。
        出発するときは「0番だけ回って（集合は 00001 = <code>1 &lt;&lt; 0</code>）、0番にいる」ので、そのマスだけ 0 にします。
        <code>prev</code>（プレブ: previous = 前の、という意味）は同じ形の表で、「そのマスへ、どの都市から来たか」を覚えておきます。あとで回る順番をたどるために使います。</p>
      </div>

      <div class="concept-box">
        <h4>③④ 集合を小さい数から順に見て、たどり着ける状態だけを使う</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        表のマスを上の行から順に見ていき、値が INF のまま（たどり着けない状態）なら <code>continue</code>（この回の残りを飛ばして次へ進む命令）で飛ばします。
        たとえば「集合が 00011（学校と郵便局）なのに、いま図書館にいる」という状態はありえないので、INF のままです。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜ小さい数から順でよいか:</strong>
        都市を1つ足すと、集合を表す数は必ず大きくなります（けたが1つ 1 になるため）。
        だから、ある行を見るときには、その行へ値を書きこむ計算は<strong>すべて終わっています</strong>。
        その行の値は「もう変わらない、いちばん短い距離」として安心して使えます。</p>
      </div>

      <div class="concept-box">
        <h4>⑤⑥ 次に行く都市をえらび、新しい集合を作る</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        例題1の2つの記号をそのまま使います。<code>visited &amp; (1 &lt;&lt; next_city)</code> が 0 以外なら、もう回った都市なので飛ばします。
        まだなら <code>visited | (1 &lt;&lt; next_city)</code> で、その都市を足した新しい集合 <code>new_visited</code> を作ります。
        第9回の貪欲法は、行った都市をリスト <code>visited = [0, 4, 3]</code> で覚えて <code>j in visited</code> で調べました。
        今回の <code>visited</code> は<strong>数1つ</strong>です。順番は覚えていませんが、表の行の番号としてそのまま使えます。</p>
      </div>

      <div class="concept-box">
        <h4>⑦ <code>if new_length &lt; best[new_visited][next_city]</code> ── 短いときだけ書きかえる</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        「いまの状態までの最短距離 ＋ 次の都市までの距離」を計算し、行き先のマスにいま入っている値より短いときだけ、書きかえます。
        はじめは INF が入っているので、最初にたどり着いた値は必ず書きこまれます。
        2回目からは、短いときだけ書きかえます。第1回から使っている「いまのところ最短」を書きかえる方法と同じです。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>ここが bitDP の中心です。</strong>
        たとえばマス <code>best[01111][3]</code>（学校・郵便局・図書館・カフェを回って、いまカフェ）には、2つの道でたどり着けます。</p>
        <table>
          <tr><th>1つ前の状態</th><th>そこまでの最短</th><th>カフェまでの距離</th><th>合計</th><th></th></tr>
          <tr><td><code>best[00111][1]</code>（いま郵便局）</td><td>{BEST5[A_FROM][1]:.1f}</td><td>{T5[1][3]}</td><td>{A_BAD}</td><td>長いので、書きかえない</td></tr>
          <tr><td><code>best[00111][2]</code>（いま図書館）</td><td>{BEST5[A_FROM][2]:.1f}</td><td>{T5[2][3]}</td><td><strong style="color:#76B900">{A_GOOD}</strong></td><td>短いので、表に残る</td></tr>
        </table>
        <p style="font-size:0.95rem;margin-top:0.6rem">表に残るのは {A_GOOD} だけです。{A_BAD} のほうの道の続きは、このあと一度も計算しません。
        全探索は、この2つの道の続きを両方とも最後まで計算していました。</p>
      </div>

      <div class="concept-box">
        <h4>⑧ 最後に、出発点へ戻る距離を足して答えを出す</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        表がすべて埋まると、いちばん下の行 <code>best[full]</code>（11111 = 全部回った）に、「最後にどの都市にいるか」ごとの最短距離が入っています。
        それぞれに、0番（学校）へ戻る距離を足して、いちばん短いものが答えです。</p>
{final_table()}
        <p style="font-size:0.95rem;margin-top:0.6rem">合計が {L5} になる行が2つあるのは、同じ輪を右回りと左回りに回った2つだからです（第8回で確かめたとおり、逆回りは同じ合計になります）。
        コードは <code>&lt;</code>（より小さい）で比べているので、先に見つけた郵便局のほうをえらびます。
        このあと <code>prev</code> を後ろから前へたどると、回る順番「{names(CITIES, R5)}」が分かります。</p>
      </div>

      <p style="margin-top:0.8rem">例題2の5都市で、表がどう埋まっていくかをまとめると、次のようになります。窓の1手順が、この表の1行にあたります。</p>
{level_table()}

      <p style="margin-top:1rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 表</td><td>行 = 回った都市の集合（2進数。右はしが0番）、列 = いまいる都市（here）。マスの数 = そこまでのいちばん短い距離。「-」= たどり着けない状態</td></tr>
        <tr><td>黄色い行</td><td>その手順で決まった行（回った都市の数が同じ行）。→ キーで、回った都市の数が1つずつ増える</td></tr>
        <tr><td>うすい色の行</td><td>0番（出発点）をふくまない集合。出発点は必ず回っているので、ずっと使われない</td></tr>
        <tr><td>最後の画面</td><td>いちばん下の行の、答えに使われたマスが緑になり、右の地図に最短ルートが出る（丸の数字 = 回る順番、S = 出発点）</td></tr>
      </table>

{example_pair('AL2-10-ex2.py', '表の一部が表示されました。<code>00001</code> の行は「学校だけ回った」状態で、'
     'いま学校（here=0）にいるときだけ 0.0 が入り、ほかは「-」です。'
     '<code>11111</code> の行は全部の都市を回り終えた状態で、最後にいる都市ごとの最短距離が入っています。'
     f'そこに学校へ戻る距離を足すと、いちばん短いのは<strong>{L5}</strong>で、全探索の答えと同じになりました（回る向きは逆ですが、同じ輪です）。'
     f'5都市では、表のマスは160個（値が入ったのは{FILLED5}個）で、全探索の24通りと大きな差はありません。'
     '差が出るのは都市を増やしたときです。最後の表のとおり、15都市では表が約49万マス、全探索は約870億通りになります。',
     creative=missions2)}
{trouble2}

{notion('標準課題は、<strong>自分の場所</strong>をメインゲート＋4〜7か所にして演習2を実行し、ターミナルの「いちばん早い回り方を、表の状態でたどる」を箱と矢印で描く。'
        '2進数のどのけたがどの場所かは、演習1の窓（スタンプカード）で確かめられる。上から4つ目の箱には、別の順番でたどり着いたときの分も書く。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回も、例題（参考）を動かしてしくみをつかんだら、
    <strong>クリエイティブ演習</strong>で自分の作品を作ります。題材は第9回の続きの <strong>ナガシマスパーランド</strong>（三重県桑名市の遊園地）です。
    演習1で「行った場所のスタンプカード」を数1つで作り、演習2で、第9回に作った自分の場所の「本当にいちばん早い回り方」を bitDP で求めます。
    <strong>第9回の <code>AL2-09-ex1.py</code>（または <code>AL2-09-ex2.py</code>）に書いた自分の <code>spots</code> と <code>WALK</code> を使う</strong>ので、
    AL2/No09 フォルダのファイルを開けるようにしておいてください。
    第9回の <code>spots</code> がない人は、ひな形の場所を自分が回りたい場所（乗り物・プール・お店など。行ってみたい別の遊園地でもよい）に書き換えます。まず作業フォルダを用意します。</p>

{setup_guide('10', ['AL2-10-ex1.py', 'AL2-10-ex2.py'])}

{pygame_card}

{keywords([
    ('動的計画法', 'どうてきけいかくほう / DP', '一度計算した答えを表に書いておき、同じ計算をくり返さないようにする方法。'),
    ('状態', 'じょうたい / state', '動的計画法で「表のどのマスか」を決める情報。巡回セールスマン問題では「回った集合」と「いまいる場所」の2つ。'),
    ('メモ化', 'memoization', '一度求めた答えを覚えておいて使い回すこと。動的計画法の中心になる考え方。'),
    ('2進数・ビット', 'にしんすう / bit', '0 と 1 だけで書く数の表し方が2進数。その1けたをビットと呼ぶ。'),
    ('ビット演算', 'ビットえんざん', '2進数のけたごとに行う計算。<code>&lt;&lt;</code>（ずらす）、<code>|</code>（または）、<code>&amp;</code>（かつ）を使う。'),
    ('bitDP', 'ビットディーピー', '「どれを回ったか」を2進数1つで表して行う動的計画法。巡回セールスマン問題で必ず最短を出す。'),
    ('INF', 'インフ / 無限大', '<code>float("inf")</code>。どんな数よりも大きい数で、表の「まだたどり着いていない」マスの印に使う。'),
])}

{example(1, '集合を数1つで表し、ナガシマスパーランドのスタンプカードを作る', ex1_body)}

{example(2, 'bitDP で5都市の最短ルートを求め、ナガシマスパーランドの本当の最短をさがす', ex2_body)}"""


# ── 解答例に載せる、ひな形（書き換える前）の確かめ用の数値 ──
V_BEEN = 1
for _name in BEEN:
    V_BEEN |= 1 << NAGA_NAMES.index(_name)
V_NEXT = V_BEEN | (1 << NAGA_NAMES.index(NEXT))
FULL_N = (1 << NN) - 1


def naga_state_rows():
    rows, v, total = [], 0, 0
    for k, place in enumerate(RN):
        if k:
            total += TN[RN[k - 1]][place]
        v |= 1 << place
        rows.append(f"          <tr><td><code>{bits(v, NN)}</code></td><td>{NAGA[place][0]}</td><td>{round(total, 1)}分</td></tr>")
    return "\n".join(rows)


_a, _b, _c = RN[1], RN[2], RN[3]
THIS_WAY = round(TN[0][_a] + TN[_a][_b] + TN[_b][_c], 1)
OTHER_WAY = round(TN[0][_b] + TN[_b][_a] + TN[_a][_c], 1)

ans = answers([slide_example("10"),
    ("演習1のひな形（書き換える前）の確かめ用", f"""        <p>ひな形のままの{NN}か所の結果です。自分の場所に書き換えたあとは変わります。</p>
        <ul style="margin:0.6rem 0 0 1.2rem;line-height:1.9">
          <li>はじめ（メインゲートだけ）: <code>{bits(1, NN)}</code> = 1</li>
          <li><code>been = {BEEN}</code> のスタンプを押したあと: <code>{bits(V_BEEN, NN)}</code> = <strong>{V_BEEN}</strong>（{"、".join(members(NAGA, V_BEEN))}）</li>
          <li><code>NEXT = "{NEXT}"</code>: <code>&amp;</code> の答えは 0（まだ行っていない）。スタンプを押すと <code>{bits(V_NEXT, NN)}</code> = <strong>{V_NEXT}</strong></li>
          <li><code>CODE = {CODE}</code>: <code>{bits(CODE, NN)}</code> → {"、".join(members(NAGA, CODE))}</li>
          <li>Lv2: {NN}か所なら <code>CODE = {FULL_N}</code>（<code>{bits(FULL_N, NN)}</code>。<code>(1 &lt;&lt; {NN}) - 1</code> でも計算できる）。
              8か所なら 255、10か所なら 1023、16か所なら 65535</li>
          <li>Lv3: 10か所なら、スタンプカードの種類は 1,024通り、順番の数は 362,880通り、表のマスは 10,240個で、順番の数は表のマスの約35倍</li>
        </ul>"""),
    ("演習2のひな形（書き換える前）の確かめ用", f"""        <ul style="margin-left:1.2rem;line-height:1.9">
          <li>貪欲法: {names(NAGA, GN)}（<strong>{GN_LEN}分</strong>）</li>
          <li>bitDP: {names(NAGA, RN)}（<strong>{LN}分</strong>）。全探索も同じ {LN}分</li>
          <li>貪欲法は {round(GN_LEN - LN, 1)}分おそい（<strong>{PN}%</strong> 長い）</li>
        </ul>
        <table>
          <tr><th>スタンプカード</th><th>いまいる場所</th><th>ここまでの分</th></tr>
{naga_state_rows()}
        </table>
        <p style="margin-top:0.6rem">最後に {NAGA[RN[-1]][0]} からメインゲートへ戻る {TN[RN[-1]][0]}分を足して、合計 {LN}分。</p>
        <p style="margin-top:0.6rem">上から4行目の状態には、「{names(NAGA, RN[:4], back=False)}」の <strong>{THIS_WAY}分</strong>と、
        「{names(NAGA, [0, _b, _a, _c], back=False)}」の {OTHER_WAY}分の2つの順番でたどり着けます。表に残るのは {THIS_WAY}分だけです。</p>
        <p style="margin-top:0.6rem">かかった時間と見積もりは、パソコンによって変わります。
        20か所のとき、貪欲法は 0.0001秒より短く、bitDP の見積もりは数秒〜数十秒、全探索の見積もりは数百年〜千年以上になるのがふつうです。
        15か所の bitDP は、0.1〜1秒ほどです。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "動的計画法（bitDP）", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("10", SLIDES),
    advanced_section("10"),
    rubric_section("10"),
    ans,
])

write("10", NAV, body)
