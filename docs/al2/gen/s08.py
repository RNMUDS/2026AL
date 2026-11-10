# -*- coding: utf-8 -*-
"""第8回: 巡回セールスマン問題（1）概要 の本文を組み立てる。
例題は「参考（学校など5都市）」と「クリエイティブ演習（USJ で回りたい場所を全部回る順番）」の2本立て。"""
import math
from itertools import permutations
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, section, setup_guide, write)
from pyhl import highlight   # noqa: E402（common が読みこみ先を追加したあとで読む）

CITIES = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9),
          ("カフェ", 6, 12), ("公園", 3, 8), ("駅", 17, 4),
          ("病院", 12, 13), ("書店", 8, 7)]


def dist_table(cities, rounded=False):
    """都市どうしの直線距離の表。rounded=True なら例題1・例題2と同じく小数第1位に丸める。"""
    n = len(cities)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            d = math.sqrt((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2)
            row.append(round(d, 1) if rounded else d)
        out.append(row)
    return out


def tour_len(order, table):
    total, here = 0.0, 0
    for c in order:
        total += table[here][c]
        here = c
    return total + table[here][0]


def best_tour(cities):
    table = dist_table(cities, rounded=True)       # 例題2と同じく、小数第1位に丸めた表で計算する
    best, bo = None, None
    for order in permutations(range(1, len(cities))):
        t = tour_len(order, table)
        if best is None or t < best:
            best, bo = t, order
    return bo, round(best, 1)


def city_dot(x, y, label, sx, sy, ox, oy, color=GREEN, r=14, sub=None):
    cx, cy = ox + x * sx, oy + y * sy
    out = [f'        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>',
           f'        <text x="{cx}" y="{cy+4}" text-anchor="middle" fill="#E0E0E0" font-size="{r-3}" font-weight="700">{label}</text>']
    if sub:
        out.append(f'        <text x="{cx}" y="{cy-r-6}" text-anchor="middle" fill="{GRAY}" font-size="10">{sub}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 巡回セールスマン問題とは
# ────────────────────────────────────────────────────────────
def fig_tsp_intro():
    cities = CITIES[:5]
    order, best = best_tour(cities)
    sx, sy, ox, oy = 31, 21, 44, 52
    route = [0] + list(order) + [0]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '巡回セールスマン問題: 全ての都市を1回ずつ回って出発点へ戻る最短ルート</text>']
    # 都市どうしの線（薄く）
    for i in range(5):
        for j in range(i + 1, 5):
            x1, y1 = ox + cities[i][1] * sx, oy + cities[i][2] * sy
            x2, y2 = ox + cities[j][1] * sx, oy + cities[j][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2a2a2a" stroke-width="1"/>')
    # ルートを順に引く
    table = dist_table(cities)
    for k in range(len(route) - 1):
        a, b = route[k], route[k + 1]
        x1, y1 = ox + cities[a][1] * sx, oy + cities[a][2] * sy
        x2, y2 = ox + cities[b][1] * sx, oy + cities[b][2] * sy
        p0 = (1 - 0.2) * k / (len(route) - 1)
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                 f'dur="{dur}s" repeatCount="indefinite"/></line>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'        <text x="{mx}" y="{my-6}" text-anchor="middle" fill="{GREEN}" font-size="11" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                 f'dur="{dur}s" repeatCount="indefinite"/>{round(table[a][b],1)}</text>')
    for i, (name, x, y) in enumerate(cities):
        color = AMBER if i == 0 else GREEN
        s += city_dot(x, y, str(i), sx, sy, ox, oy, color, 16, name)
    s.append(f'        <rect x="430" y="60" width="240" height="88" rx="10" fill="#141414" stroke="#333"/>')
    s.append(f'        <text x="550" y="84" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">3つのきまり</text>')
    for i, t in enumerate(["すべての都市を回る", "同じ都市は1回だけ", "最後は出発点へ戻る"]):
        s.append(f'        <text x="550" y="{106+i*18}" text-anchor="middle" fill="#ccc" font-size="11">{t}</text>')
    s.append(f'        <text x="350" y="{oy+13*sy+30}" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             f'最短ルート: 学校 → 郵便局 → 図書館 → カフェ → 公園 → 学校　合計 {best}</text>')
    return fig(700, oy + 13 * sy + 48, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 都市の数と順番の数
# ────────────────────────────────────────────────────────────
def fig_factorial():
    rows = []
    for n in [5, 8, 10, 12, 15, 20]:
        total = 1
        for k in range(1, n):
            total *= k
        rows.append((n, total))
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が1つ増えるだけで、試す順番の数は何倍にもなる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり。右の時間は、10都市が0.14秒だった例題2の実測からの見積もり</text>']
    notes = {5: "一瞬", 8: "一瞬", 10: "約0.14秒", 12: "約15秒",
             15: "約9時間", 20: "約1,500年"}
    for i, (n, total) in enumerate(rows):
        y = 66 + i * 46
        big = total > 10 ** 9
        color = RED if big else GREEN
        w = math.log10(total) / 18 * 380
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{n}都市</text>')
        s.append(f'        <rect x="92" y="{y+4}" width="{max(w,3):.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{92+max(w,3)+10:.0f}" y="{y+21}" fill="{color}" font-size="11" font-weight="700">{total:,}通り</text>')
        s.append(f'        <text x="676" y="{y+21}" text-anchor="end" fill="{GRAY}" font-size="11">{notes[n]}</text>')
    s.append(f'        <text x="350" y="{66+6*46+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '全探索では、都市が1つ増えるだけで、かかる時間が何倍にもなる</text>')
    return fig(700, 66 + 6 * 46 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 全探索が24通りを順に試す
# ────────────────────────────────────────────────────────────
def fig_bruteforce():
    cities = CITIES[:5]
    table = dist_table(cities, rounded=True)
    orders = [(1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (2, 1, 3, 4),
              (3, 2, 1, 4), (4, 3, 2, 1)]
    sx, sy = 12, 10
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索: 24通りの順番を1つずつ試して、いちばん短いものを選ぶ</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '24通りのうち6通りを表示（0 = 学校）</text>']
    for i, order in enumerate(orders):
        px = 20 + (i % 3) * 226
        py = 0 if i < 3 else 180
        length = round(tour_len(order, table), 1)
        best = (length == 34.9)
        color = GREEN if best else "#666"
        s.append(f'        <rect x="{px}" y="{56+py}" width="212" height="164" rx="10" fill="#141414" stroke="{color if best else "#333"}" stroke-width="{2.5 if best else 1}"/>')
        route = [0] + list(order) + [0]
        for k in range(len(route) - 1):
            a, b = route[k], route[k + 1]
            x1 = px + 22 + cities[a][1] * sx
            y1 = 74 + py + cities[a][2] * sy
            x2 = px + 22 + cities[b][1] * sx
            y2 = 74 + py + cities[b][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>')
        for j, (name, x, y) in enumerate(cities):
            cx = px + 22 + x * sx
            cy = 74 + py + y * sy
            s.append(f'        <circle cx="{cx}" cy="{cy}" r="8" fill="#1A1A1A" stroke="{AMBER if j == 0 else color}" stroke-width="1.5"/>')
            s.append(f'        <text x="{cx}" y="{cy+3}" text-anchor="middle" fill="#ccc" font-size="8">{j}</text>')
        s.append(f'        <text x="{px+106}" y="{212+py}" text-anchor="middle" fill="{color if best else "#999"}" '
                 f'font-size="12" font-weight="700">{"".join(str(c) for c in order)} → {length}{"  最短" if best else ""}</text>')
        a0 = (1 - 0.2) * i / len(orders)
        s.append(f'        <rect x="{px-2}" y="{54+py}" width="216" height="168" rx="12" fill="none" stroke="{AMBER}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a0:.3f};{a0+0.01:.3f};{a0+0.11:.3f};{a0+0.12:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="350" y="418" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '全探索は必ず正しい答えを出すが、都市が増えると終わらなくなる</text>')
    return fig(700, 434, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 5都市と8都市の最適ルート
# ────────────────────────────────────────────────────────────
def fig_five_vs_eight():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が増えると、ルートの形そのものが変わる</text>']
    for panel, count in enumerate([5, 8]):
        cities = CITIES[:count]
        order, best = best_tour(cities)
        table = dist_table(cities)
        x0 = 20 + panel * 350
        sx, sy = 15.5, 12.5
        ox, oy = x0 + 22, 74
        s.append(f'        <rect x="{x0}" y="46" width="330" height="252" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="66" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
                 f'{count}都市の最短ルート: 合計 {best}</text>')
        route = [0] + list(order) + [0]
        for k in range(len(route) - 1):
            a, b = route[k], route[k + 1]
            x1, y1 = ox + cities[a][1] * sx, oy + cities[a][2] * sy
            x2, y2 = ox + cities[b][1] * sx, oy + cities[b][2] * sy
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{GREEN}" stroke-width="2.5"/>')
        visit = {0: "S"}
        for k, c in enumerate(order):
            visit[c] = str(k + 1)
        for i, (name, x, y) in enumerate(cities):
            cx, cy = ox + x * sx, oy + y * sy
            color = AMBER if i == 0 else GREEN
            s.append(f'        <circle cx="{cx:.0f}" cy="{cy:.0f}" r="11" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>')
            s.append(f'        <text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" fill="#E0E0E0" font-size="10" font-weight="700">{visit[i]}</text>')
            s.append(f'        <text x="{cx:.0f}" y="{cy-15:.0f}" text-anchor="middle" fill="{GRAY}" font-size="9">{name}</text>')
    s.append(f'        <text x="350" y="320" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '5都市の答えに3都市を足すだけでは、8都市の最短ルートにはならない</text>')
    return fig(700, 336, "\n".join(s))


def pycode(src, label):
    """Python のコードを色つきの <pre> にする（本文の説明用）。"""
    return f'<pre data-blanks="0"><span class="code-label">{label}</span>\n{highlight(src)}</pre>'


# ────────────────────────────────────────────────────────────
# 図: 2点のあいだの距離（三平方の定理）── 公園(3,8) と カフェ(6,12) は 3・4・5 の直角三角形
# ────────────────────────────────────────────────────────────
def fig_distance():
    u, ox, oy = 46, 70, 70              # 1目もり = 46px、方眼の左上 = (x=2, y=7)
    x0, y0 = 2, 7

    def P(x, y):
        return ox + (x - x0) * u, oy + (y - y0) * u
    s = [f'        <text x="350" y="28" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '2点のあいだの直線距離 = よこの差とたての差でできる直角三角形の、ななめの辺</text>']
    for gx in range(2, 8):                                  # 方眼
        X, _ = P(gx, 0)
        s.append(f'        <line x1="{X}" y1="{oy}" x2="{X}" y2="{oy + 6 * u}" stroke="#222"/>')
        s.append(f'        <text x="{X}" y="{oy - 8}" text-anchor="middle" fill="{GRAY}" font-size="10">{gx}</text>')
    for gy in range(7, 14):
        _, Y = P(0, gy)
        s.append(f'        <line x1="{ox}" y1="{Y}" x2="{ox + 5 * u}" y2="{Y}" stroke="#222"/>')
        s.append(f'        <text x="{ox - 10}" y="{Y + 4}" text-anchor="end" fill="{GRAY}" font-size="10">{gy}</text>')
    s.append(f'        <text x="{ox + 5 * u + 6}" y="{oy - 8}" fill="{GRAY}" font-size="10">x →</text>')
    s.append(f'        <text x="{ox - 10}" y="{oy + 6 * u + 18}" text-anchor="end" fill="{GRAY}" font-size="10">y ↓</text>')
    ax, ay = P(3, 8)
    bx, by = P(6, 12)
    cx, cy = P(6, 8)                                        # 直角の角
    s.append(f'        <line x1="{ax}" y1="{ay}" x2="{cx}" y2="{cy}" stroke="{AMBER}" stroke-width="4"/>')
    s.append(f'        <line x1="{cx}" y1="{cy}" x2="{bx}" y2="{by}" stroke="#4FC3F7" stroke-width="4"/>')
    s.append(f'        <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{GREEN}" stroke-width="4"/>')
    s.append(f'        <rect x="{cx - 12}" y="{cy}" width="12" height="12" fill="none" stroke="#999"/>')
    s.append(f'        <text x="{(ax + cx) / 2}" y="{ay - 10}" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">よこの差 6 − 3 = 3</text>')
    s.append(f'        <text x="{cx + 10}" y="{(cy + by) / 2 + 4}" fill="#4FC3F7" font-size="13" font-weight="700">たての差 12 − 8 = 4</text>')
    s.append(f'        <text x="{(ax + bx) / 2 - 16}" y="{(ay + by) / 2 + 10}" text-anchor="end" fill="{GREEN}" font-size="13" font-weight="700">ななめ = 5</text>')
    for (x, y, name, sub) in [(ax, ay, "4", "公園 (3, 8)"), (bx, by, "3", "カフェ (6, 12)")]:
        s.append(f'        <circle cx="{x}" cy="{y}" r="13" fill="#1A1A1A" stroke="{GREEN}" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="{y + 4}" text-anchor="middle" fill="#E0E0E0" font-size="11" font-weight="700">{name}</text>')
        s.append(f'        <text x="{x - 18}" y="{y + 4}" text-anchor="end" fill="#E0E0E0" font-size="11">{sub}</text>')
    steps = [("① よこの差", "dx = 6 − 3 = 3", AMBER),
             ("② たての差", "dy = 12 − 8 = 4", "#4FC3F7"),
             ("③ それぞれ2乗して足す", "3**2 + 4**2 = 9 + 16 = 25", "#E0E0E0"),
             ("④ 平方根（ルート）", "math.sqrt(25) = 5.0", GREEN)]
    s.append(f'        <rect x="405" y="62" width="280" height="214" rx="10" fill="#141414" stroke="#333"/>')
    s.append(f'        <text x="545" y="86" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">Python で計算する順番</text>')
    for k, (head, calc, color) in enumerate(steps):
        y = 114 + k * 42
        s.append(f'        <text x="420" y="{y}" fill="{GRAY}" font-size="11">{head}</text>')
        s.append(f'        <text x="434" y="{y + 18}" fill="{color}" font-size="13" font-weight="700" font-family="monospace">{calc}</text>')
    s.append(f'        <text x="350" y="{oy + 6 * u + 44}" text-anchor="middle" fill="#ccc" font-size="12">'
             '三平方の定理: ななめ² = よこ² + たて²　→　ななめ = √(よこ² + たて²)</text>')
    s.append(f'        <text x="350" y="{oy + 6 * u + 64}" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '差が負の数（3 − 6 = −3）になっても、2乗すると同じ 9 になるので、引く順番は気にしなくてよい</text>')
    return fig(700, oy + 6 * u + 80, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図: 表の半分だけ計算して、ななめの反対側に写す（例題1の5都市）
# ────────────────────────────────────────────────────────────
def fig_half_table():
    table = dist_table(CITIES[:5], rounded=True)
    n, cw, ch, ox, oy = 5, 62, 40, 70, 84
    order = {}
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            k += 1
            order[(i, j)] = k
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '計算するのは右上の半分（10組）だけ。左下へは同じ数を写す。ななめは 0 のまま</text>',
         f'        <text x="{ox + n * cw / 2}" y="{oy - 30}" text-anchor="middle" fill="{GRAY}" font-size="11">j（列）= 行き先の番号</text>',
         f'        <text x="{ox - 44}" y="{oy + n * ch / 2}" text-anchor="middle" fill="{GRAY}" font-size="11" '
         f'transform="rotate(-90 {ox - 44} {oy + n * ch / 2})">i（行）= 出発の番号</text>']
    for c in range(n):
        s.append(f'        <text x="{ox + c * cw + cw / 2}" y="{oy - 8}" text-anchor="middle" fill="#ccc" font-size="12" font-weight="700">{c}</text>')
    for r in range(n):
        s.append(f'        <text x="{ox - 14}" y="{oy + r * ch + ch / 2 + 5}" text-anchor="middle" fill="#ccc" font-size="12" font-weight="700">{r}</text>')
        for c in range(n):
            x, y = ox + c * cw, oy + r * ch
            if r == c:
                fill, stroke, text, tc = "#222", "#333", "0", GRAY
            elif r < c:
                fill, stroke, text, tc = "#1f3310", GREEN, str(table[r][c]), "#E0E0E0"
            else:
                fill, stroke, text, tc = "#2a2210", AMBER, str(table[r][c]), "#bbb"
            s.append(f'        <rect x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="5" fill="{fill}" stroke="{stroke}"/>')
            s.append(f'        <text x="{x + cw / 2}" y="{y + ch / 2 + 5}" text-anchor="middle" fill="{tc}" font-size="12">{text}</text>')
            if r < c:
                s.append(f'        <text x="{x + 8}" y="{y + 14}" fill="{GREEN}" font-size="9" font-weight="700">{order[(r, c)]}</text>')
    # 0行1列 → 1行0列 の写し方を矢印で
    x1, y1 = ox + 1 * cw + cw / 2, oy + 0 * ch + ch - 4
    x2, y2 = ox + 0 * cw + cw - 6, oy + 1 * ch + ch / 2
    s.append(f'        <path d="M{x1},{y1} Q{x1},{y2} {x2},{y2}" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    s.append(f'        <polygon points="{x2},{y2} {x2 + 9},{y2 - 5} {x2 + 9},{y2 + 5}" fill="{AMBER}"/>')
    lx = ox + n * cw + 30
    notes = [(GREEN, "緑 = 計算するマス（i < j）"), (GREEN, "左上の小さい数 = 計算する順番（pairs の順）"),
             (AMBER, "橙 = 写すだけのマス（i > j）"), (GRAY, "灰色 = ななめ（i = j）。自分自身なので 0")]
    for k2, (color, text) in enumerate(notes):
        s.append(f'        <text x="{lx}" y="{oy + 14 + k2 * 24}" fill="{color}" font-size="12">{text}</text>')
    s.append(f'        <text x="{lx}" y="{oy + 128}" fill="#ccc" font-size="12">25マスのうち、計算は10回だけ</text>')
    s.append(f'        <text x="{lx}" y="{oy + 148}" fill="#ccc" font-size="12">（5 × 4 ÷ 2 = 10）</text>')
    s.append(f'        <text x="{lx}" y="{oy + 176}" fill="{AMBER}" font-size="12">例: [0][1] = 8.1 を計算したら</text>')
    s.append(f'        <text x="{lx}" y="{oy + 196}" fill="{AMBER}" font-size="12">　　[1][0] にも 8.1 を入れる</text>')
    return fig(700, oy + n * ch + 24, "\n".join(s))

# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "巡回セールスマン問題 #sec-explanation",
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("08")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回から第7回まででは、<strong>2地点のあいだ</strong>の最短経路を求めました。
      第8回からは問題の形が変わります。求めるのは<strong>すべての地点を1回ずつ回って出発点へ戻る、いちばん短いルート</strong>です。
      巡回セールスマン問題（じゅんかいセールスマンもんだい）と呼ばれ、
      英語の頭文字をとって<strong>TSP</strong>と書かれることもあります。
    </p>

    <div class="analogy">
      USJ（ユニバーサル・スタジオ・ジャパン）で、ハリー・ポッターのエリア、ミニオン・パーク、ジュラシック・パーク、
      スーパー・ニンテンドー・ワールドの4か所を全部回って、エントランスに戻ってくる場面を思い浮かべてください。
      どこから回るかで、歩く時間の合計が変わります。左上と右上を行ったり来たりすると、それだけで何十分も歩くことになります。
      同じ問題は、宅配便のドライバーが荷物を届ける順番、基板に穴をあける機械のドリルの動かし方など、いろいろな場面に現れます。
      今回のクリエイティブ演習では、<strong>自分が回りたい場所</strong>で、いちばん早い回り方をさがします。
    </div>

{fig_tsp_intro()}

    <div class="concept-box">
      <h4>ダイクストラ法との違い</h4>
      <table>
        <tr><th></th><th>ダイクストラ法（第5〜7回）</th><th>巡回セールスマン問題（第8〜10回）</th></tr>
        <tr><td>求めるもの</td><td>出発点から目的地までの最短経路</td><td>すべての地点を1回ずつ回って戻る最短ルート</td></tr>
        <tr><td>通らなくてよい地点</td><td>ある（近道でないなら通らない）</td><td>ない（全部必ず1回通る）</td></tr>
        <tr><td>決めるもの</td><td>どの道を通るか</td><td>どの順番で回るか</td></tr>
        <tr><td>速く解く方法</td><td>ある（ダイクストラ法）</td><td>まだ見つかっていない</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>順番の数え方</h4>
      <p style="font-size:0.95rem">
        都市が5個あり、そのうち1個を出発点とします。残りの4個を回る順番は
        <strong>4 × 3 × 2 × 1 = 24通り</strong>です。
        最初に選べる都市が4通り、次が3通り、その次が2通り、最後は1通りに決まるためです。
        1から順にかけ算した値を<strong>階乗</strong>（かいじょう）と呼び、<code>4!</code> と書きます。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        都市が n 個なら <code>(n-1)!</code> 通りです。
        6都市なら120通り、8都市なら5,040通り、12都市なら約4,000万通りになります。
        都市が1つ増えるたびに、順番の数は「<strong>増やしたあとの都市の数 − 1</strong>」倍になります（9都市→10都市なら9倍）。
      </p>
    </div>

{fig_factorial()}
    <p style="font-size:0.9rem;color:#888;margin:-0.6rem 0 1.5rem">秒数はパソコンによって変わります。
    演習2の見積もりの表は、自分のパソコンで測った速さから出すので、この図と少しちがう時間になります。</p>

    <div class="note-warn">
      <strong>NP困難（エヌピーこんなん）:</strong>
      巡回セールスマン問題には、<strong>どんな都市の配置でも</strong>、都市が増えても現実的な時間で<strong>必ず</strong>最適解を出せる方法が、
      <strong>いまだに見つかっていません</strong>（2026年現在）。
      「そんな方法は存在しない」と多くの研究者が考えていますが、証明もされていません。
      この問題（P≠NP予想）を解決した人には、100万ドルの賞金がかけられています。
      <br><br>
      ただし、<strong>全探索しか方法がないわけではありません</strong>。
      工夫した解き方では、2025年に韓国の約8万2千か所を回る最短ルートが、最短であることの証明付きで求められました。
      第9回では「だいたい短い」ルートをすばやく出す貪欲法（どんよくほう）、第10回では全探索よりずっと速く最適解を出す動的計画法を学びます。
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>地図と計算の進み方を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜7回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で表示します。
      例題1・演習1は<strong>距離の表が1組ずつ埋まっていくようす</strong>を、例題2・演習2は<strong>全探索が順番を1つずつ試すようす</strong>を見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜7回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜7回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（表の1組、または順番1つごと。標準課題の図を描くときに便利）</td></tr>
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
          <tr><td><code>SyntaxError</code></td><td>かっこ・<code>"</code> の閉じ忘れ。<code>spots</code> の各行は <code>("ミニオン・パーク", 14, 11),</code> のように書く。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>TypeError: 'tuple' object is not callable</code></td><td><code>spots</code> の行の<strong>最後のカンマ</strong>を書き忘れた。<code>( … )</code> の後ろに <code>,</code> を付ける</td></tr>
          <tr><td><code>spots の ○番目の位置がおかしい</code></td><td>x や y を <code>"7"</code> のように <code>" "</code> で囲んだ。数は囲まずに <code>7</code> と書く</td></tr>
          <tr><td><code>spots の ○番目が ("名前", x, y) の形になっていない</code></td><td>名前・x・y の3つがそろっていない。カンマが2つあるかを見る</td></tr>
          <tr><td><code>「○」が2回出てくる</code> ／ <code>同じ位置にある</code></td><td>同じ名前か同じ位置の場所が2つある。名前か x・y のどちらかを変える</td></tr>
          <tr><td><code>spots が ○か所ある</code></td><td>11か所以上にした。表が大きくなりすぎるので10か所までにする</td></tr>
          <tr><td><code>spots が少なすぎる</code></td><td>エントランスのほかに2か所以上ないと、回る順番を考えられない。場所の行を足す</td></tr>
          <tr><td><code>WALK は 0 より大きい数 …</code></td><td><code>WALK = "2"</code> のように囲んだか、0 やマイナスにした。<code>WALK = 2</code> のように書く</td></tr>
        </table>
      </div>"""

trouble2 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習2）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td>演習1と時間がちがう</td><td><code>spots</code> か <code>WALK</code> を貼りかえ忘れた。演習1の <code>spots = [</code> から <code>]</code> までと、<code>WALK = …</code> の行をそのまま貼る</td></tr>
          <tr><td><code>FIRST_VISIT の「○」が spots にない</code></td><td>名前が1文字ちがう（「・」のあるなし、全角と半角など）。<code>spots</code> の名前をコピーして貼る</td></tr>
          <tr><td><code>FIRST_VISIT に0番の「…」は選べない</code></td><td>出発するエントランスを書いた。1番から後ろの場所の名前にする</td></tr>
          <tr><td><code>spots が 11か所 ある。全探索だと …</code></td><td>11か所だと 10! ＝ 約363万通りで、何秒も（パソコンによっては何十秒も）かかる。10か所までにする。なぜ増やせないのかが今回のテーマ</td></tr>
          <tr><td>ターミナルに順番が24通りしか出ない</td><td>画面があふれないように、最初の24通りだけ表示している。残りも全部試している（「試した順番」の数を見る）</td></tr>
          <tr><td>窓の再生がとびとびになる</td><td>順番が多いとき（7か所以上）は、窓には「いまのところ最短」が変わった所を中心に、とびとびに表示している</td></tr>
        </table>
      </div>"""

missions1 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> を、<strong>自分が回りたい場所</strong>にする（名前と位置 x・y を書き換える）。0番はエントランスのまま。
              <code>TITLE</code> も自分のものにする。位置は、USJ 公式サイトのパークマップなどを見て、だいたいでよい（1目もり = 歩いて1分くらい）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>6か所以上</td><td>場所を<strong>6か所以上</strong>（エントランス＋5か所以上）にする。ターミナルに「Lv2 達成」と出ればよい。
              計算した組の数が <code>n × (n-1) ÷ 2</code> になっていることを確かめる（6か所なら15組）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>歩く速さ</td><td><code>WALK</code> を書き換えて、歩く速さを変える（例: 人ごみやベビーカーで <code>WALK = 2</code>）。表の数がすべて何倍になるかを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、自分らしい案内文にする。
              使える材料: <code>near</code>（いちばん近い2か所: <code>near[0]</code> と <code>near[1]</code> が名前、<code>near[2]</code> が分）、<code>far</code>（いちばん遠い2か所）</td></tr>
        </table>
      </div>"""

missions2 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> と <code>WALK</code> を、<strong>演習1で作った自分のもの</strong>に貼りかえる。
              いちばん早い順番と、その<strong>逆回り</strong>が同じ時間になることを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>8か所以上</td><td>場所を<strong>8か所以上</strong>にして実行する（10か所まで）。「試した順番」が5か所の24通りから何倍になったかを見る
              （5か所の時間は 0.000秒 と短すぎて比べられないので、時間は8か所以上の値を見る）。
              見積もりの表で、15か所・20か所なら何時間（何年）かかるかを確かめる。<strong>標準課題で使うので、ここで出た数をメモしておく</strong></td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>最初に行きたい</td><td><code>FIRST_VISIT</code> に、いちばん最初に行きたい場所の名前を書く（例: <code>FIRST_VISIT = "ジュラシック・パーク"</code>）。
              いちばん早い順番より<strong>何分おそくなるか</strong>が表示される。おそくならない場所もあるので、何か所か試す</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、自分らしい「回り方の案内」にする。
              使える材料: <code>route</code>（回る場所の名前の並び。<code>route[1]</code> が最初に行く場所）、<code>total</code>（合計の分）</td></tr>
        </table>
      </div>"""

TABLE_CODE = """distance = []
for i in range(n):
    distance.append([0] * n)          # ① 全部 0 の n行n列の表を用意する
pairs = []
for i in range(n):
    for j in range(i + 1, n):         # ② i より大きい j だけを調べる
        d = straight_distance(cities[i], cities[j])
        distance[i][j] = d            # ③ 表の2か所に同じ距離を入れる
        distance[j][i] = d
        pairs.append((i, j))          # ④ 計算した組を順に記録する"""

TABLE_SHAPE = """distance = [[0, 0, 0, 0, 0],     # 0行目 = 0番（学校）から各都市への距離を入れる行
            [0, 0, 0, 0, 0],     # 1行目 = 1番（郵便局）から
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]     # distance[0][1] は「0行目の1列目」"""

ex1_body = f"""      <p>巡回セールスマン問題を解く準備として、地点の位置から<strong>距離の表</strong>（距離行列）を作ります。
      表があれば、どんな順番で回っても、合計距離を表の数の足し算だけで出せます。
      演習1では、同じしくみで<strong>USJ で回りたい場所を歩く時間の表</strong>を作ります。</p>

      <div class="concept-box">
        <h4>2点のあいだの距離</h4>
        <p style="font-size:0.95rem">点(x1, y1) と点(x2, y2) のあいだの直線距離は、
        よこの差とたての差から <code>math.sqrt((x1-x2)**2 + (y1-y2)**2)</code> で求まります（三平方の定理）。
        <code>**2</code> は2乗（同じ数を2回かける。<code>3**2</code> は 3 × 3 = 9）、
        <code>math.sqrt</code> は平方根（ルート。2乗するとその数になる数。<code>math.sqrt(25)</code> は 5.0）を求める命令です。
        下の図は、例題1の公園 (3, 8) とカフェ (6, 12) のあいだの距離を求めるようすです。</p>
      </div>

{fig_distance()}

      <p style="margin-top:0.4rem">2点をよこ線とたて線で結ぶと、直角三角形ができます。よこの辺が 3、たての辺が 4 なので、
      ななめの辺（2点を結ぶ直線）は <code>math.sqrt(3**2 + 4**2)</code> = <code>math.sqrt(25)</code> = <strong>5.0</strong> です。
      例題1の表の「3行4列」と「4行3列」が 5.0 になっているのは、この計算の結果です。
      ほかの組も同じ計算ですが、ふつうはきれいな整数にならないので、<code>round(…, 1)</code> で小数第1位までに丸めています（8.062… → 8.1）。</p>

      <h4 style="margin:1.8rem 0 0.6rem">表（距離行列）を作るコードの書き方 ── 4つの大事な行</h4>
      <p>例題1で表を作る部分は、次の数行です。どれも、これからの回でも何度も出てくる大事な書き方なので、1行ずつ「何をしているか」と「なぜそう書くか」を見ていきます。
      演習1（USJ）でも、表の名前が <code>distance</code> から <code>minutes</code>（歩く時間）に変わるだけで、まったく同じ書き方をしています。</p>
{pycode(TABLE_CODE, "Python ── 例題1で表を作る部分")}

{fig_half_table()}

      <div class="concept-box">
        <h4>① <code>distance.append([0] * n)</code> ── はじめに、全部 0 の表を用意する</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>[0] * n</code> は「0 を n 個ならべたリスト」です。n = 5 なら <code>[0, 0, 0, 0, 0]</code> になります。
        これを <code>for i in range(n)</code> で n 回 <code>append</code>（リストの最後に足す）するので、
        「0 が5個の行」が5本ならんだ <strong>5行5列の表</strong>ができます。
        表の中の1マスは <code>distance[行の番号][列の番号]</code> で読み書きします。</p>
{plain(TABLE_SHAPE, "①のあとの distance の中身（n = 5）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong>
        ③で <code>distance[i][j] = d</code> と書きこむには、そのマスが<strong>先に用意されていないといけない</strong>からです。
        空のリスト <code>[]</code> のまま <code>distance[0][1] = 8.1</code> と書くと、
        「そんな場所はない」という <code>IndexError</code> になります。
        また、0 を入れておくと、計算しない<strong>ななめのマス</strong>（<code>distance[0][0]</code> など、自分から自分への距離）が
        そのまま正しい値 0 になります。</p>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">注意: <code>[[0] * n] * n</code> と1行で書きたくなりますが、これは<strong>同じ1本の行を5回ならべた</strong>ものになり、
        1か所を書きかえると5行ぜんぶが変わってしまいます。行は <code>for</code> と <code>append</code> で1本ずつ作るのが安全です。</p>
      </div>

      <div class="concept-box">
        <h4>② <code>for j in range(i + 1, n)</code> ── i より大きい j だけを調べる</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>range(i + 1, n)</code> は「i + 1 から n − 1 まで」です。外側の i が1つ進むたびに、内側の j が始まる場所も1つ右にずれます。
        5都市なら、調べる組は次のとおりで、<strong>全部で10組</strong>です（上の図の緑のマスの番号の順）。</p>
        <table>
          <tr><th>i（外側）</th><th>j がとる値（内側）</th><th>調べる組</th><th>組の数</th></tr>
          <tr><td>0</td><td>1, 2, 3, 4</td><td>(0,1) (0,2) (0,3) (0,4)</td><td>4</td></tr>
          <tr><td>1</td><td>2, 3, 4</td><td>(1,2) (1,3) (1,4)</td><td>3</td></tr>
          <tr><td>2</td><td>3, 4</td><td>(2,3) (2,4)</td><td>2</td></tr>
          <tr><td>3</td><td>4</td><td>(3,4)</td><td>1</td></tr>
          <tr><td>4</td><td>（なし。range(5, 5) は空）</td><td>―</td><td>0</td></tr>
        </table>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong> 理由は2つあります。</p>
        <ul style="margin-left:1.2rem;line-height:1.9;font-size:0.95rem">
          <li><strong>行きと帰りは同じ距離だから。</strong>学校→郵便局 と 郵便局→学校 は同じ道なので、(0,1) を計算すれば (1,0) は計算しなくてよい。</li>
          <li><strong>自分自身との組はいらないから。</strong>j を i + 1 から始めるので、(0,0) のような i = j の組が出てこない。ななめは①で入れた 0 のまま。</li>
        </ul>
        <p style="font-size:0.95rem">これで計算の回数は 25回 → <strong>10回</strong>（<code>n × (n − 1) ÷ 2</code>）に減ります。
        もし <code>range(n)</code> と書けば、同じ距離を2回ずつ計算するうえ、自分自身との距離まで計算してしまいます（答えは同じですが、むだが多い）。
        この「<strong>i &lt; j の組だけを調べる二重ループ</strong>」は、「2つずつの組み合わせを全部、重ならずに調べる」ときの決まった書き方です。</p>
      </div>

      <div class="concept-box">
        <h4>③ <code>distance[i][j] = d</code> と <code>distance[j][i] = d</code> ── 表の2か所に同時に入れる</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        1回計算した距離 d を、表の<strong>i行j列</strong>と<strong>j行i列</strong>の2か所に入れます。
        たとえば (i, j) = (0, 1) のとき、d = 8.1 を <code>distance[0][1]</code>（学校→郵便局）と
        <code>distance[1][0]</code>（郵便局→学校）の両方に入れます（上の図の橙の矢印）。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong>
        ②で半分しか計算しないので、<strong>残りの半分を埋めるのがこの2行目</strong>です。
        これがないと、左下の半分が 0 のままになり、例題2で「郵便局から学校へ戻る」距離を <code>distance[1][0]</code> で読んだときに 0 になってしまいます。
        どちらの向きで読んでも同じ数になるように、表をななめの線をはさんで<strong>左右対称</strong>にしておくのです。
        表を作っておけば、例題2では距離をもう計算せず、<code>distance[here][city]</code> と表を読むだけで足し算ができます
        （24通りの順番で同じ距離を何度も使うので、毎回計算するよりずっと速い）。</p>
      </div>

      <div class="concept-box">
        <h4>④ <code>pairs.append((i, j))</code> ── 計算した組を順に記録する</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>(i, j)</code> は2つの数をひとまとめにした<strong>タプル</strong>（かっこで囲んだ組）です。
        計算するたびに、その組をリスト <code>pairs</code> の最後に足していきます。
        最後には <code>[(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), …, (3, 4)]</code> の10組が、計算した順にならびます。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong>
        あとで「どの組を、どの順番で計算したか」を使うためです。例題1では2か所で使っています。</p>
        <ul style="margin-left:1.2rem;line-height:1.9;font-size:0.95rem">
          <li><strong>いちばん近い組・遠い組をさがす</strong>: <code>for i, j in pairs:</code> と書けば、10組だけを重なりなく見られる（25マス全部を見ると、0 のななめや同じ組の2回目まで見てしまう）。</li>
          <li><strong>窓のアニメーション</strong>: <code>pairs</code> の順に1組ずつ線を引き、表を埋めていく。</li>
        </ul>
        <p style="font-size:0.95rem">組の数は <code>len(pairs)</code> で数えられるので、ターミナルの「計算した組: 10組」もこれで出しています。
        「処理した順に記録しておき、あとで使う」書き方は、第2回から使っている <code>order</code>（調べた順の記録）と同じ考え方です。</p>
      </div>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 地図</td><td>丸の数字 = 地点の番号（橙の丸が0番 = 出発点）。線の数字 = 計算した2地点のあいだの距離（演習1では歩く時間）</td></tr>
        <tr><td>右: 表</td><td>行の番号から列の番号までの距離。<code>?</code> = まだ計算していないマス、灰色 = ななめ（自分自身との距離 0）</td></tr>
        <tr><td>白い線・白い枠</td><td>いま計算した組。表の2か所が同時に埋まる</td></tr>
      </table>

{example_pair('AL2-08-ex1.py', '5つの都市について、5行5列の距離の表ができました。'
     'ななめの線（0行0列、1行1列、…）はすべて 0 です。自分自身との距離は0だからです。'
     'また、0行1列と1行0列がどちらも 8.1 のように、表は<strong>ななめの線をはさんで左右対称</strong>になっています。'
     '行きと帰りで同じ距離だからです。そのため、計算したのは 5 × 4 ÷ 2 = <strong>10組</strong>だけです。'
     'いちばん近いのはカフェと公園（5.0）、いちばん遠いのは学校と図書館（13.9）でした。',
     creative=missions1)}
{trouble1}"""

ex2_body = f"""      <p>出発点を0番とし、残りの地点を回る順番を<strong>すべて</strong>書き出して、いちばん短いルートをさがします（全探索）。
      並べ方をすべて作るには <code>itertools</code> の <code>permutations</code> を使います。
      後半では、都市を5個から10個まで増やして、全探索にかかる時間を測ります。
      演習2では、<strong>演習1の自分の場所</strong>を全部回って、エントランスへ戻るいちばん早い順番をさがします。</p>

      <div class="concept-box">
        <h4>permutations（順列）</h4>
        <p style="font-size:0.95rem">
          <code>permutations([1, 2, 3])</code> と書くと、
          <code>(1,2,3) (1,3,2) (2,1,3) (2,3,1) (3,1,2) (3,2,1)</code> の6通りをすべて作ってくれます。
          自分で入れ子のループを書かなくてよいので、全探索のコードがとても短くなります。
          0番（出発点）は最初と最後に決まっているので、並べるのは1番から後ろだけです。
        </p>
      </div>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>tour_length(order, table)</code></td><td>0番から <code>order</code> の順に回り、最後に0番へ戻るまでの距離を、表の数を足して求める</td></tr>
        <tr><td><code>for order in permutations(range(1, n))</code></td><td>1番〜(n-1)番の並べ方を1つずつ取り出す。<code>(n-1)!</code> 通り</td></tr>
        <tr><td><code>if best_length is None or length &lt; best_length</code></td><td>いまのところ最短より短ければ、記録を書きかえる（第1回の「全部試して選ぶ」と同じ）</td></tr>
        <tr><td><code>time.perf_counter()</code></td><td>いまの時刻（秒）。全探索の前と後で読んで、差をかかった時間にする（第7回と同じ）</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 橙の線</td><td>いま試している順番のルート</td></tr>
        <tr><td>左: 太い緑の線</td><td>いまのところ最短のルート。最後の画面では最短ルートだけになり、丸の数字が回る順番（S = 出発点）になる</td></tr>
        <tr><td>右: 試した順番の一覧</td><td>新しいものが下。緑の行 = 「いまのところ最短」を更新した順番</td></tr>
      </table>

{example_pair('AL2-08-ex2.py', '24通りすべての合計距離が表示され、最短は<strong>34.9</strong>でした。'
     'ルートは「学校 → 郵便局 → 図書館 → カフェ → 公園 → 学校」です。'
     '逆回りのルートも、同じ34.9になっています。同じ道を反対向きに走るだけなので、距離が変わらないためです。'
     '24通りの中には、実際には12通りの「別のルート」しかなく、残り12通りはその逆回りだということです。'
     '後半の表では、都市が1つ増えるたびに、かかった時間が「増やしたあとの都市の数 − 1」倍くらいずつ増えています（9都市→10都市で約9倍）。'
     '秒数そのものはパソコンによって変わります。',
     fig_bruteforce(), creative=missions2)}
{trouble2}

{fig_five_vs_eight()}

{notion('標準課題は、先に演習2の Lv2（8か所以上）の結果をメモしてから、<strong>自分の場所</strong>をエントランス＋3か所に減らして実行し、6通りの順番を枝分かれ図（木）に描く。'
        '窓を → キーで進めると、どの順番で「いまのところ最短」が書きかわったかが分かる。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回も、例題（参考）を動かして距離の表と全探索の進み方をつかんだら、
    <strong>クリエイティブ演習</strong>で自分の作品を作ります。題材は <strong>USJ（ユニバーサル・スタジオ・ジャパン）</strong>です。
    演習1で「回りたい場所の歩く時間の表」を作り、演習2で「全部回ってエントランスへ戻る、いちばん早い順番」をさがします。</p>
    <p style="margin-bottom:1.5rem">ひな形の場所の位置は、下にエントランス、左上にハリー・ポッターのエリア、上にジュラシック・パーク、
    右上にスーパー・ニンテンドー・ワールド、右にミニオン・パークがある、という<strong>おおまかな例</strong>です。
    実際の位置は USJ 公式サイトのパークマップを見て、自由に直してかまいません。まず作業フォルダを用意します。</p>

{setup_guide('08', ['AL2-08-ex1.py', 'AL2-08-ex2.py'])}

{pygame_card}

{keywords([
    ('巡回セールスマン問題', 'じゅんかいセールスマンもんだい / TSP', 'すべての地点を1回ずつ回って出発点へ戻る、合計距離がいちばん短いルートを求める問題。'),
    ('距離行列', 'きょりぎょうれつ / distance matrix', 'すべての地点の組み合わせについて距離を書き並べた表。第3回の隣接行列と同じ形。'),
    ('階乗', 'かいじょう / factorial', '1からその数までを順にかけた値。<code>4!</code> は 4×3×2×1＝24。地点がn個のときのルート数は <code>(n-1)!</code> 通り。'),
    ('permutations', 'じゅんれつ / 順列', 'Pythonの <code>itertools</code> にある道具。並べ方をすべて作ってくれる。'),
    ('全探索', 'ぜんたんさく / brute force', '考えられる答えをすべて試して、いちばん良いものを選ぶ方法。必ず正しい答えが出るが、数が増えると終わらなくなる。'),
    ('NP困難', 'エヌピーこんなん / NP-hard', '地点が増えると、現実的な時間で必ず最適解を出す方法が知られていない問題のこと。巡回セールスマン問題はその代表例。'),
])}

{example(1, '地点の位置から距離の表を作り、USJ の歩く時間の表を作る', ex1_body)}

{example(2, '全探索で最短ルートを求め、USJ を全部回るいちばん早い順番をさがす', ex2_body)}"""

ans = answers([slide_example("08"),
    ("演習1のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの5か所の結果です。自分の場所に書き換えたあとは変わります。</p>
        <table>
          <tr><th></th><th>0 エントランス</th><th>1 ハリー・ポッター</th><th>2 ミニオン・パーク</th><th>3 ジュラシック・パーク</th><th>4 ニンテンドー</th></tr>
          <tr><td>0</td><td>0</td><td>11.2</td><td>7.6</td><td>13.2</td><td>13.5</td></tr>
          <tr><td>1</td><td>11.2</td><td>0</td><td>13.9</td><td>7.6</td><td>15.0</td></tr>
          <tr><td>2</td><td>7.6</td><td>13.9</td><td>0</td><td>11.2</td><td>6.7</td></tr>
          <tr><td>3</td><td>13.2</td><td>7.6</td><td>11.2</td><td>0</td><td>8.9</td></tr>
          <tr><td>4</td><td>13.5</td><td>15.0</td><td>6.7</td><td>8.9</td><td>0</td></tr>
        </table>
        <p style="margin-top:0.6rem">計算した組は10組。いちばん近いのはミニオン・パークとスーパー・ニンテンドー・ワールド（6.7分）、
        いちばん遠いのはハリー・ポッターとスーパー・ニンテンドー・ワールド（15.0分）。
        <code>WALK = 2</code> にすると、表の数がすべて2倍になります（13.5 → 27.0 など）。</p>"""),
    ("演習2のひな形（書き換える前）の確かめ用", """        <ul style="margin-left:1.2rem;line-height:1.9">
          <li>試した順番: 24通り。「いまのところ最短」は 58.7 → 53.9 → 50.2 → <strong>42.0分</strong> と4回書きかわる</li>
          <li>いちばん早い順番: エントランス → ハリー・ポッター → ジュラシック・パーク → スーパー・ニンテンドー・ワールド → ミニオン・パーク → エントランス（<strong>42.0分</strong>）。逆回りも42.0分</li>
          <li>いちばんおそい順番は 66.8分（左上と右上を行ったり来たりする順番）。いちばん早い順番と24.8分ちがう</li>
          <li>Lv3（<code>FIRST_VISIT</code>）: ハリー・ポッターかミニオン・パークを最初にすると<strong>おそくならない</strong>（いちばん早い順番かその逆回りの1番目だから）。
              ジュラシック・パークは<strong>8.1分</strong>、スーパー・ニンテンドー・ワールドは<strong>8.2分</strong>おそくなる</li>
        </ul>
        <p style="margin-top:0.6rem">かかった時間と見積もりは、パソコンによって変わります。場所が1つ増えるたびに、順番の数が「そのときの場所の数 − 1」倍になり、
        時間もそれに近い倍率で増えていれば正しく測れています。15か所で数時間、20か所で千年以上になるのがふつうです。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "巡回セールスマン問題とは", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("08", SLIDES),
    advanced_section("08"),
    rubric_section("08"),
    ans,
])

write("08", NAV, body)
