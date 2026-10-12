# -*- coding: utf-8 -*-
"""第4回: 重み付きグラフとは の本文を組み立てる。"""
import math
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, blank_answers, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, reveal, section, setup_guide, write)

POS = {"新宿": (170, 96), "渋谷": (170, 246), "品川": (390, 246),
       "池袋": (390, 66), "上野": (560, 66), "東京": (560, 196)}
EDGES = [("新宿", "渋谷", 7), ("新宿", "池袋", 9), ("新宿", "品川", 30),
         ("渋谷", "品川", 9), ("池袋", "上野", 12), ("上野", "東京", 6),
         ("東京", "品川", 11)]

COST_MAP = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]
ROUTE_A = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
ROUTE_B = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
ROUTE_C = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0),
           (4, 1), (4, 2), (4, 3), (4, 4)]


def draw_graph(highlight=None, hcolor=GREEN, show_weight=True):
    """路線図を描く。highlight は強調する経路（駅名の並び）。"""
    out = []
    hedges = set()
    if highlight:
        for i in range(len(highlight) - 1):
            hedges.add(frozenset((highlight[i], highlight[i + 1])))
    for a, b, w in EDGES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        on = frozenset((a, b)) in hedges
        out.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="{hcolor if on else "#555"}" stroke-width="{5 if on else 2}"/>')
    if show_weight:
        for a, b, w in EDGES:
            (x1, y1), (x2, y2) = POS[a], POS[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            on = frozenset((a, b)) in hedges
            out.append(f'        <rect x="{mx-17}" y="{my-11}" width="34" height="22" rx="6" '
                       f'fill="#0A0A0A" stroke="{hcolor if on else GRAY}"/>')
            out.append(f'        <text x="{mx}" y="{my+5}" text-anchor="middle" '
                       f'fill="{hcolor if on else "#bbb"}" font-size="11" font-weight="{700 if on else 400}">{w}分</text>')
    for name, (x, y) in POS.items():
        on = highlight and name in highlight
        out.append(f'        <circle cx="{x}" cy="{y}" r="26" fill="{"#1a2e0a" if on else "#1A1A1A"}" '
                   f'stroke="{hcolor if on else "#555"}" stroke-width="2"/>')
        out.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" '
                   f'font-size="12" font-weight="700">{name}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 直通より乗りかえのほうが早い
# ────────────────────────────────────────────────────────────
def fig_weighted_graph():
    dur = 15
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '辺に「かかる時間」を書き込んだグラフ（重み付きグラフ）</text>']
    s += draw_graph()
    phases = [
        (0.02, 0.34, ["新宿", "品川"], AMBER, "直通: 路線1本 ／ 合計 30分", "辺の数はいちばん少ない"),
        (0.36, 0.66, ["新宿", "渋谷", "品川"], GREEN, "乗りかえ1回: 路線2本 ／ 合計 16分", "辺の数は多いが、合計時間はいちばん短い"),
        (0.68, 0.98, ["新宿", "池袋", "上野", "東京", "品川"], RED, "遠回り: 路線4本 ／ 合計 38分", "辺の数も合計時間も多い"),
    ]
    for a, b, route, color, label, note in phases:
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s += ["  " + line for line in draw_graph(route, color)]
        s.append(f'          <text x="350" y="300" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{label}</text>')
        s.append(f'          <text x="350" y="322" text-anchor="middle" fill="{GRAY}" font-size="11">{note}</text>')
        s.append('        </g>')
    return fig(700, 336, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 重みなしと重みありの書き方の違い
# ────────────────────────────────────────────────────────────
def fig_notation():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '隣接リストに重みを書き足す</text>']
    boxes = [
        (24, "重みなし（第3回）", GRAY, [
            '"新宿": ["渋谷", "池袋", "品川"]',
            '',
            'となりの駅の名前だけを並べる',
            '「どこへ行けるか」しか分からない',
        ]),
        (364, "重みあり（第4回）", GREEN, [
            '"新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)]',
            '',
            '（駅の名前, かかる時間）の組で並べる',
            '「どこへ行けるか」＋「いくらかかるか」が分かる',
        ]),
    ]
    for x0, title, color, lines in boxes:
        s.append(f'        <rect x="{x0}" y="46" width="312" height="150" rx="12" fill="#141414" stroke="{color}" stroke-width="1.6"/>')
        s.append(f'        <text x="{x0+156}" y="72" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        for i, ln in enumerate(lines):
            if not ln:
                continue
            mono = ' font-family="JetBrains Mono, monospace"' if ln.startswith('"') else ""
            size = 10 if ln.startswith('"') else 11
            fill = "#cdd6f4" if ln.startswith('"') else "#bbb"
            s.append(f'        <text x="{x0+156}" y="{100+i*24}" text-anchor="middle" fill="{fill}" font-size="{size}"{mono}>{ln}</text>')
    s.append(f'        <text x="350" y="222" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '重みを書き足すだけで、「乗りかえの少なさ」ではなく「かかる時間の短さ」を考えられるようになる</text>')
    return fig(700, 238, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 床コスト付き迷路の3つの行き方
# ────────────────────────────────────────────────────────────
def fig_cost_maze():
    cell = 46
    dur = 15
    x0, y0 = 246, 62
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '床コスト付き迷路: 歩数が多くても合計時間は短いことがある</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'マスの数字は、そのマスを通り抜けるのにかかる秒数</text>']
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * cell, y0 + r * cell
            v = COST_MAP[r][c]
            deep = v >= 9
            s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" '
                     f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#333"}"/>')
            s.append(f'        <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+6}" text-anchor="middle" '
                     f'fill="{AMBER if deep else "#bbb"}" font-size="15" font-weight="{700 if deep else 400}">{v}</text>')
    s.append(f'        <text x="{x0+8}" y="{y0+14}" fill="{GREEN}" font-size="11" font-weight="700">S</text>')
    s.append(f'        <text x="{x0+4*cell+30}" y="{y0+4*cell+38}" fill="{GREEN}" font-size="11" font-weight="700">G</text>')

    phases = [
        (0.02, 0.32, ROUTE_A, AMBER, "行き方A: 8歩 ／ 合計 16秒"),
        (0.34, 0.64, ROUTE_B, AMBER, "行き方B: 8歩 ／ 合計 16秒"),
        (0.66, 0.98, ROUTE_C, GREEN, "行き方C: 12歩 ／ 合計 12秒（いちばん短い）"),
    ]
    for a, b, route, color, label in phases:
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        pts = " ".join(f"{x0+c*cell+(cell-3)/2},{y0+r*cell+(cell-3)/2}" for r, c in route)
        s.append(f'          <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="5" '
                 f'stroke-linejoin="round" stroke-linecap="round" opacity="0.85"/>')
        s.append(f'          <text x="350" y="{y0+5*cell+28}" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{label}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{y0+5*cell+54}" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '9のマス（ぬかるみ）を1つ通るだけで、1のマスを8回通るより時間がかかる</text>')
    return fig(700, y0 + 5 * cell + 70, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 全探索の通り数の爆発
# ────────────────────────────────────────────────────────────
def fig_explosion():
    rows = [("3×3", 12, ""), ("4×4", 184, "前の約15倍"),
            ("5×5", 8512, "前の約46倍"), ("6×6", 1262816, "前の約148倍"),
            ("7×7", 575780564, "前の約456倍")]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路が1マス大きくなるだけで、行き方の数は数十〜数百倍に増える</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '壁のない迷路で、左上から右下まで同じマスを2度通らない行き方の数（棒の長さは10倍ごとの目もり）</text>']
    for i, (size, count, note) in enumerate(rows):
        y = 66 + i * 44
        big = count > 10 ** 6
        color = RED if big else GREEN
        w = math.log10(count) / 9 * 400
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{size}</text>')
        s.append(f'        <rect x="86" y="{y+4}" width="{w:.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{86+w+10:.0f}" y="{y+21}" fill="{color}" font-size="12" font-weight="700">{count:,}通り</text>')
        s.append(f'        <text x="676" y="{y+21}" text-anchor="end" fill="{GRAY}" font-size="11">{note}</text>')
    s.append(f'        <text x="350" y="{66+5*44+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '全探索では現実的な時間で終わらない。第5回から学ぶダイクストラ法が必要になる</text>')
    return fig(700, 66 + 5 * 44 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図5: 合計時間を1区間ずつ足していく（route_minutes のしくみ）
# ────────────────────────────────────────────────────────────
def fig_sum_steps():
    dur = 14
    chains = [
        (["新宿", "池袋", "上野", "東京", "品川"], [9, 12, 6, 11], RED),
        (["新宿", "渋谷", "品川"], [7, 9], GREEN),
    ]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '合計時間の求め方: 隣り合う2駅の時間を、前から順に total に足す</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '最初は total = 0。1区間進むたびに total = total + その区間の時間</text>']
    k = 0
    total_steps = sum(len(w) for _, w, _ in chains) + 2
    for ci, (route, ws, color) in enumerate(chains):
        y = 92 + ci * 130
        gap = 640 / (len(route) - 1) if len(route) > 2 else 320
        xs = [40 + i * min(gap, 150) for i in range(len(route))]
        s.append(f'        <text x="24" y="{y-26}" fill="{color}" font-size="12" font-weight="700">'
                 f'行き方{"ABC"[ci]}: ' + " → ".join(route) + '</text>')
        s.append(f'        <g opacity="0">{reveal(k, total_steps, dur)}'
                 f'<text x="{xs[0]}" y="{y+62}" text-anchor="middle" fill="{GRAY}" font-size="11">total = 0</text></g>')
        k += 1
        for i, name in enumerate(route):
            s.append(f'        <rect x="{xs[i]-30}" y="{y-14}" width="60" height="28" rx="8" fill="#1A1A1A" stroke="#555"/>')
            s.append(f'        <text x="{xs[i]}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
        total = 0
        for i, w in enumerate(ws):
            total += w
            x1, x2 = xs[i] + 30, xs[i + 1] - 30
            mx = (x1 + x2) / 2
            s.append(f'        <g opacity="0">{reveal(k, total_steps, dur)}'
                     f'<line x1="{x1}" y1="{y}" x2="{x2-6}" y2="{y}" stroke="{color}" stroke-width="3"/>'
                     f'<polygon points="{x2},{y} {x2-8},{y-5} {x2-8},{y+5}" fill="{color}"/>'
                     f'<text x="{mx}" y="{y-8}" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">{w}分</text>'
                     f'<text x="{xs[i+1]}" y="{y+40}" text-anchor="middle" fill="#bbb" font-size="11">{total - w} + {w}</text>'
                     f'<text x="{xs[i+1]}" y="{y+62}" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">total = {total}</text></g>')
            k += 1
        s.append(f'        <text x="676" y="{y-26}" text-anchor="end" fill="{color}" font-size="12" font-weight="700" opacity="0">'
                 f'{reveal(k - 1, total_steps, dur)}路線{len(ws)}本 ／ 合計 {total}分</text>')
    s.append(f'        <text x="350" y="{92+2*130-10}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '路線の本数は A のほうが多いのに、合計時間は B のほうが短い。数えるもので「短い道」が変わる</text>')
    return fig(700, 92 + 2 * 130 + 6, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図6: 幅優先探索を重み付きグラフで動かすと（時間を見ずに直通を選ぶ）
# ────────────────────────────────────────────────────────────
def fig_bfs_trace():
    sc, row_h = 0.46, 132
    steps = [
        ("新宿", ["渋谷", "池袋", "品川"], ["新宿"], {"渋谷": "新宿", "池袋": "新宿", "品川": "新宿"},
         "となりの 渋谷・池袋・品川 を見つけて、キューの右に入れる",
         "品川の「来た駅」が、ここで 新宿 に決まる（時間 30分 は見ていない）", None),
        ("渋谷", ["池袋", "品川"], ["新宿", "渋谷"], {"渋谷": "新宿", "池袋": "新宿", "品川": "新宿"},
         "となりの 新宿・品川 は、どちらももう見つけている → 何もしない",
         "渋谷 → 品川（9分）を使う 16分の道は、ここで捨てられる", ("渋谷", "品川")),
        ("池袋", ["品川", "上野"], ["新宿", "渋谷", "池袋"], {"渋谷": "新宿", "池袋": "新宿", "品川": "新宿", "上野": "池袋"},
         "となりの 上野 を見つけて、キューの右に入れる", "", None),
        ("品川", ["上野"], ["新宿", "渋谷", "池袋", "品川"], {"渋谷": "新宿", "池袋": "新宿", "品川": "新宿", "上野": "池袋"},
         "ゴールの品川を取り出したので終わり。came_from を逆にたどる",
         "品川 ← 新宿 なので、答えは 直通（路線1本・30分）", None),
    ]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '幅優先探索で 新宿 → 品川 をさがす（手順1〜4）</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '白い枠 = いま取り出した駅、緑の線 = どの駅から見つけたか（came_from）、橙 = キューに入っている駅</text>']
    for k, (cur, queue, popped, came, line1, line2, cut) in enumerate(steps):
        y0 = 62 + k * row_h
        p = {st: (20 + (x - 150) * sc, y0 + 14 + (y - 50) * sc) for st, (x, y) in POS.items()}
        tree = {frozenset((v, u)) for v, u in came.items()}
        for a, b, w in EDGES:
            (x1, y1), (x2, y2) = p[a], p[b]
            on = frozenset((a, b)) in tree
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="{GREEN if on else "#3a3a3a"}" stroke-width="{3 if on else 1.5}"/>')
            dx = -9 if abs(x1 - x2) < 5 else 0        # たての線は、数字を線の左にずらす
            s.append(f'        <text x="{(x1+x2)/2+dx:.0f}" y="{(y1+y2)/2-3:.0f}" text-anchor="middle" fill="#666" font-size="8">{w}</text>')
        if cut:
            (x1, y1), (x2, y2) = p[cut[0]], p[cut[1]]
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{RED}" stroke-width="3" stroke-dasharray="5 4"/>')
        for st, (x, y) in p.items():
            ring = "#444"
            if st in queue:
                ring = AMBER
            if st in popped:
                ring = GREEN
            if st == cur:
                ring = "#FFFFFF"
            s.append(f'        <circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="#1A1A1A" stroke="{ring}" stroke-width="{2.5 if st == cur else 1.5}"/>')
            s.append(f'        <text x="{x:.0f}" y="{y+3:.0f}" text-anchor="middle" fill="#ddd" font-size="8">{st}</text>')
        tx = 250
        s.append(f'        <text x="{tx}" y="{y0+20}" fill="#E0E0E0" font-size="12" font-weight="700">手順{k+1}　{cur} を取り出す</text>')
        s.append(f'        <text x="{tx}" y="{y0+42}" fill="#bbb" font-size="11">{line1}</text>')
        if line2:
            s.append(f'        <text x="{tx}" y="{y0+62}" fill="{RED if cut or k == 3 else AMBER}" font-size="11" font-weight="700">{line2}</text>')
        s.append(f'        <text x="{tx}" y="{y0+88}" fill="{GRAY}" font-size="11">キュー:</text>')
        bx = tx + 46
        for name in queue:
            s.append(f'        <rect x="{bx}" y="{y0+74}" width="44" height="22" rx="5" fill="#1a1200" stroke="{AMBER}"/>')
            s.append(f'        <text x="{bx+22}" y="{y0+89}" text-anchor="middle" fill="{AMBER}" font-size="11">{name}</text>')
            bx += 50
        if k < len(steps) - 1:
            s.append(f'        <line x1="20" y1="{y0+row_h-12}" x2="680" y2="{y0+row_h-12}" stroke="#2a2a2a"/>')
    y = 62 + len(steps) * row_h + 2
    s.append(f'        <text x="350" y="{y}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '幅優先探索は「先に見つけた道」を残す。線の数字（時間）は1回も使っていない</text>')
    return fig(700, y + 18, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "重みとは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("04")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第3回では、路線図を「どの駅とどの駅がつながっているか」だけの<strong>グラフ</strong>に書き写しました。
      しかし、乗換案内で知りたいのは「つながっているか」だけではありません。
      同じ1駅ぶんでも、急行で3分の区間もあれば、30分かかる区間もあります。
      第4回では、辺ごとに<strong>かかる時間</strong>を書き込んだグラフを作り、
      これまでの幅優先探索では「いちばん早く着く道」が求められない場面を確かめます。
    </p>

    <div class="analogy">
      乗換案内アプリで経路を調べると、「乗りかえ0回・所要45分」と「乗りかえ2回・所要28分」のように、
      性質の違う候補が並びます。乗りかえの回数がいちばん少ない行き方と、所要時間がいちばん短い行き方は、別のものです。
      第1回から第3回までの幅優先探索が求めていたのは、前者の「乗りかえの回数がいちばん少ない行き方」でした。
    </div>

{fig_weighted_graph()}

    <div class="concept-box">
      <h4>用語</h4>
      <table>
        <tr><th>用語</th><th>意味</th><th>路線図でいうと</th></tr>
        <tr><td><strong>重み</strong></td><td>辺ごとに書き込む数値。その辺を通るのにかかるもの</td><td>区間の乗車時間（分）</td></tr>
        <tr><td><strong style="color:#76B900">重み付きグラフ</strong></td><td>すべての辺に重みが付いているグラフ</td><td>区間ごとに時間を書いた路線図</td></tr>
        <tr><td><strong>コスト</strong></td><td>重みの言いかえ。「その道を通るために支払うもの」という意味で使う</td><td>時間・運賃</td></tr>
        <tr><td><strong>経路</strong></td><td>出発点から目的地までの、頂点の並び（道）</td><td>新宿 → 渋谷 → 品川</td></tr>
        <tr><td><strong style="color:#FFB800">経路の長さ（合計コスト）</strong></td><td>経路が通る辺の重みを全部足したもの</td><td>7分 ＋ 9分 ＝ 16分</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>重みになるもの</h4>
      <table>
        <tr><th>あつかうもの</th><th>重みになるもの</th><th>小さいほど良いか</th></tr>
        <tr><td>路線図</td><td>乗車時間（分）</td><td>小さいほど良い</td></tr>
        <tr><td>道路地図</td><td>距離（km）、通行料金（円）</td><td>小さいほど良い</td></tr>
        <tr><td>床コスト付き迷路</td><td>そのマスを通り抜ける時間（秒）</td><td>小さいほど良い</td></tr>
        <tr><td>通信ネットワーク</td><td>通信の遅れ（ミリ秒）</td><td>小さいほど良い</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        後期の授業であつかう重みは、すべて<strong>0以上の数値</strong>です。
        マイナスの重みが混ざると、第5回から学ぶダイクストラ法は正しく動きません。理由は第5回で確かめます。
        第2回の迷路も、下の図のようにマスごとに「通り抜ける時間」を書けば重み付きグラフになります（第7回であつかう）。
      </p>
    </div>

{fig_cost_maze()}

    <h3 style="margin:2rem 0 0.8rem">重み付きグラフをPythonに書き写す</h3>
    <p style="margin-bottom:1rem">
      第3回の隣接リストに、時間を<strong>書き足す</strong>だけです。
      となりの駅の名前だけを並べていたところを、<code>("駅の名前", 時間)</code> の<strong>2つ組</strong>（タプル: 丸かっこで値をまとめたもの）にします。
      路線は行きも帰りも同じ時間なので、第3回と同じく、1本の路線を<strong>両方の駅の行</strong>に書きます。
    </p>

{fig_notation()}

    <h3 style="margin:2rem 0 0.8rem">経路の合計時間を求める</h3>
    <p style="margin-bottom:1rem">
      「新宿 → 渋谷 → 品川」の合計時間は、隣り合う2駅の組（新宿—渋谷、渋谷—品川）ごとに時間を調べて足せば求まります。
      例題1の <code>route_minutes</code> 関数は、これを前から1組ずつくり返します。
    </p>

{fig_sum_steps()}

    <h3 style="margin:2rem 0 0.8rem">幅優先探索は時間を見ていない</h3>
    <p style="margin-bottom:1rem">
      では、第1〜3回の幅優先探索で 新宿 → 品川 をさがすとどうなるでしょうか。
      幅優先探索は、キューの左から駅を取り出し、まだ見つけていないとなりの駅をキューの右に入れる、をくり返すのでした。
      下の図で、1手順ずつ追ってみます。
    </p>

{fig_bfs_trace()}

    <div class="analogy">
      幅優先探索は、出発点から「路線1本で行ける駅」「2本で行ける駅」「3本で行ける駅」…の順に、同心円のように広げていきます。
      品川は新宿から<strong>路線1本</strong>で行けるので、手順1で見つかり、「来た駅 = 新宿」がその場で決まります。
      あとから渋谷経由の 16分 の道が出てきても、品川はもう見つけた駅なので、書き直しません。
      幅優先探索がいちばん少なくするのは<strong>路線の本数</strong>で、<strong>時間の合計</strong>ではありません。
    </div>

    <div class="concept-box">
      <h4>「最短」には2つの意味がある</h4>
      <table>
        <tr><th>言い方</th><th>意味</th><th>求める方法</th></tr>
        <tr><td>辺の数が最も少ない経路</td><td>乗りかえや歩数がいちばん少ない行き方</td><td>幅優先探索（第1〜3回）</td></tr>
        <tr><td>重みの合計が最も小さい経路</td><td>かかる時間や料金がいちばん小さい行き方</td><td>全探索（今回の例題2）、ダイクストラ法（第5回から）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        重みがすべて同じ値なら、2つの答えは一致します。
        重みがばらばらのときは、例題2で確かめるように<strong>答えがずれることがあります</strong>。
      </p>
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>グラフを絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題も、第2・3回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で、
      重み付きグラフを丸と線と数字で描き、時間を足していくようすや探索の進み方をアニメーションで見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2・3回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2・3回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各例題ファイルの<strong>いちばん下</strong>
        （「ここから下は、重み付きグラフを pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。
        丸の並べ方は、線の交わりが少なくなるように窓が自動で決めます（紙の路線図と位置がちがっても、つながり方と時間は同じ）。</p>
      </div>
    </div>"""

ex1_body = f"""      <p>6つの駅からなる路線図に、区間ごとの乗車時間を重みとして書き込み、隣接リストでPythonに書き写します。
      そのうえで、出発駅から目的駅までの<strong>3通りの行き方</strong>について、路線の本数と合計時間を求めて比べます。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>railway = {{ ... }}</code></td><td>重み付きの隣接リスト。となりの駅を <code>("駅の名前", 時間)</code> の2つ組で並べる</td></tr>
        <tr><td><code>for name, minutes in railway[station]:</code></td><td>2つ組の1つ目（駅の名前）を <code>name</code>、2つ目（時間）を <code>minutes</code> に入れて1つずつ見る</td></tr>
        <tr><td><code>def route_minutes(route):</code></td><td>行き方 <code>route</code> の隣り合う2駅ごとに時間を探し、合計 <code>total</code> に足していく（1章の「合計時間の求め方」の図と同じ）</td></tr>
        <tr><td><code>fewest</code> と <code>fastest</code></td><td>「路線の本数がいちばん少ない道」と「合計時間がいちばん短い道」を、それぞれ選ぶ</td></tr>
      </table>

      <p style="margin-top:0.8rem">実行すると、ターミナルに隣接リストと3通りの比較が出たあと、窓が開きます。窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 重み付きグラフ</td><td>丸 = 駅、線 = 路線、線のまん中の数字 = 時間。橙の線が「いま足した区間」、緑の線が「もう足した区間」</td></tr>
        <tr><td>右: 行き方ごとの箱</td><td>上の行が行き方、下の行が足し算（例 <code>12 + 10 = 22分</code>）。<code>route_minutes</code> の答えも並べて出る</td></tr>
        <tr><td>最後の画面</td><td><strong style="color:#5AAAFF">青</strong> = 路線の本数がいちばん少ない道、<strong style="color:#76B900">緑</strong> = 合計時間がいちばん短い道</td></tr>
      </table>

{example_pair('AL2-04-ex1.py', '新宿から品川へは、直通（路線1本）が<strong>30分</strong>、'
     '渋谷で1回乗りかえる行き方（路線2本）が<strong>16分</strong>、大回りの行き方（路線4本）が<strong>38分</strong>でした。'
     '路線の本数が少ない順に並べると 30分 → 16分 → 38分 で、本数と時間はまったく対応していません。'
     '窓の最後の画面では、青（本数がいちばん少ない直通）と緑（時間がいちばん短い渋谷経由）が別の線になっています。'
     '右の箱の <code>7 + 9 = 16分</code> は、<code>route_minutes</code> が隣り合う2駅の時間を前から順に足した結果です。')}"""

ex2_body = f"""      <p>例題1と同じ路線図で、出発駅から目的駅までの道を<strong>2つの方法</strong>でさがし、答えを比べます。</p>
      <ul class="point-list" style="margin-bottom:1rem">
        <li><strong style="color:#5AAAFF">方法1: 幅優先探索</strong>（第1〜3回と同じ）。路線の本数がいちばん少ない道を求める。</li>
        <li><strong style="color:#76B900">方法2: 全探索</strong>（第1回と同じ考え方）。同じ駅を2度通らない行き方を<strong>すべて</strong>書き出し、合計時間がいちばん短いものを選ぶ。
            書きかけの道を第2回の<strong>スタック</strong>に積んで、1駅ずつのばしていく。</li>
      </ul>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>queue.popleft()</code> と <code>came_from</code></td><td>幅優先探索。<code>for name, minutes in ...</code> で時間も取り出しているが、<strong>使っていない</strong></td></tr>
        <tr><td><code>stack.pop()</code> と <code>route + [name]</code></td><td>全探索。書きかけの道を取り出し、まだ通っていないとなりの駅を1つ足した道を積みなおす。ゴールに着いた道を <code>every_route</code> にためる</td></tr>
        <tr><td><code>best_route</code></td><td>1つ目を仮の答えにして、合計時間がもっと短い道が出てきたら入れかえる</td></tr>
      </table>

      <p style="margin-top:0.8rem">実行すると、ターミナルにすべての行き方と2つの方法の答えが出たあと、窓が開きます。窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓の場面</th><th>読み方</th></tr>
        <tr><td>前半: 方法1（幅優先探索）</td><td>白い枠 = いま取り出した駅、緑の線 = どの駅から見つけたか（<code>came_from</code>）。右にキューの中身。線の数字は暗く表示（使わないため）</td></tr>
        <tr><td>中ほど: 方法1の答え</td><td>青い線が、幅優先探索が選んだ道</td></tr>
        <tr><td>後半: 方法2（全探索）</td><td>橙の線 = いま調べている行き方、緑の線と ★ = いまのところいちばん短い道</td></tr>
        <tr><td>最後の画面</td><td><strong style="color:#5AAAFF">青</strong> = 幅優先探索の道、<strong style="color:#76B900">緑</strong> = 合計時間がいちばん短い道と、その差</td></tr>
      </table>

{example_pair('AL2-04-ex2.py', '幅優先探索が選んだのは<strong>直通の30分</strong>の道でした。'
     '一方、全探索で3通りをすべて比べると、いちばん短いのは<strong>渋谷で乗りかえる16分</strong>の道で、その差は14分です。'
     '1章の「幅優先探索で 新宿 → 品川 をさがす」の図のとおり、品川は手順1で新宿から直接見つかるため、幅優先探索は渋谷経由の道を考えません。'
     '重みの合計を最小にしたいとき、幅優先探索は使えません。')}

    <div class="concept-box">
      <h4>全探索なら、いつでも正しい答えが出るのでは？</h4>
      <p style="font-size:0.95rem">全探索は、すべての行き方を調べるので必ず正しい答えが出ます。
      ところが、地図が少し大きくなるだけで、行き方の数は<strong>爆発的に</strong>増えます。下の図は、壁のない迷路で左上から右下まで行く行き方の数です。</p>
    </div>

{fig_explosion()}

{notion('例題2（実践）の窓を → キーで1手順ずつ進め、幅優先探索が蒲田（ゴール）を見つけた手順と、そのときの came_from を確かめる。'
        'そのうえで、幅優先探索が選んだ道と合計時間、全探索で選んだ道と合計時間、その差を書く。'
        'あわせて、幅優先探索が短いほうの道を選べない理由を、1章の図「幅優先探索で 新宿 → 品川 をさがす」と結びつけて説明する。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1と例題2のコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('04', ['AL2-04-ex1.py', 'AL2-04-ex2.py'])}

{pygame_card}

{keywords([
    ('重み', 'weight', '辺ごとに書き込む数値。乗車時間・距離・料金など「その辺を通るのにかかるもの」を表す。'),
    ('重み付きグラフ', 'weighted graph', 'すべての辺に重みが付いているグラフ。重みのないグラフは、すべての重みが1のグラフと考えることもできる。'),
    ('コスト', 'cost', '重みの言いかえ。「その道を通るために支払うもの」という意味で使う。合計コストが小さいほど良い。'),
    ('タプル', 'tuple', '<code>("渋谷", 7)</code> のように、丸かっこでいくつかの値をまとめたもの。リストと違って、あとから中身を書き換えられない。'),
    ('関数', 'function', '<code>def 名前(引数):</code> で作る、ひとまとまりの処理。<code>route_minutes(route)</code> のように呼ぶと、<code>return</code> の値が返ってくる。'),
    ('全探索', 'brute force', '考えられる候補をすべて書き出して1つずつ調べる方法。必ず正しい答えが出るが、候補が増えると終わらなくなる。'),
])}

    <div class="note-warn">
      <strong>穴埋めの注意:</strong> 今回の穴は、まちがえてもプログラムは止まらずに最後まで動きます。
      そのかわり、<strong>数がずれます</strong>（合計時間が 0分 になる、いちばん短い道が選ばれない、など）。
      窓の最後の画面に<strong style="color:#FF6E6E">赤い文字</strong>が出たら、どこかの穴がまちがっています。実行結果と窓の画像を、ページの画像と見比べてください。
    </div>

{example(1, '重み付きグラフで、行き方ごとの合計時間を求める', ex1_body)}

{example(2, '幅優先探索では合計時間がいちばん短い道を求められない', ex2_body)}"""

ans = answers([slide_example("04"), blank_answers("04"),
    ("理解度チェックの答えの例", """        <p><strong>問い</strong>: 辺の時間を1本だけ書き換えて、幅優先探索の道が「合計時間がいちばん短い道」にもなるようにしたい。どの辺を何分にすればよいか。</p>
        <p style="margin-top:0.6rem"><strong>答えの例</strong>（例題の路線図、新宿 → 品川 の場合）</p>
        <p>新宿—品川（直通）を <strong>15分以下</strong>（たとえば 12分）にする。
        幅優先探索は時間を見ないので、時間を変えても選ぶ道は直通のまま。
        直通の時間を、渋谷経由の 16分 より短くすれば、いちばん短い道のほうが直通に変わって、2つの答えが一致する。</p>
        <table>
          <tr><th>行き方</th><th>30分のとき</th><th>12分のとき</th></tr>
          <tr><td>新宿 → 品川</td><td>30分</td><td><strong style="color:#76B900">12分</strong></td></tr>
          <tr><td>新宿 → 渋谷 → 品川</td><td><strong style="color:#76B900">16分</strong></td><td>16分</td></tr>
          <tr><td>新宿 → 池袋 → 上野 → 東京 → 品川</td><td>38分</td><td>38分</td></tr>
        </table>
        <p style="margin-top:0.6rem">ただし<strong>一致は偶然</strong>です。幅優先探索は重みを見ていないので、時間を戻せば答えはまたずれます。
        （16分ちょうどにすると同じ時間の道が2本になり、どちらも「いちばん短い道」になる。）</p>"""),
    ("確かめ用の数値（例題の実践）", """        <table>
          <tr><th>行き方（横浜 → 蒲田）</th><th>路線の本数</th><th>合計時間</th></tr>
          <tr><td>横浜 → 蒲田</td><td>1本</td><td>26分（<strong style="color:#5AAAFF">幅優先探索の道</strong>）</td></tr>
          <tr><td>横浜 → 川崎 → 蒲田</td><td>2本</td><td>22分</td></tr>
          <tr><td>横浜 → 鶴見 → 川崎 → 蒲田</td><td>3本</td><td><strong style="color:#76B900">18分（いちばん短い）</strong></td></tr>
          <tr><td>横浜 → 鶴見 → 生麦 → 大森 → 蒲田</td><td>4本</td><td>22分</td></tr>
          <tr><td>横浜 → 川崎 → 鶴見 → 生麦 → 大森 → 蒲田</td><td>5本</td><td>32分</td></tr>
        </table>
        <p style="margin-top:0.6rem">差は 26 − 18 = <strong>8分</strong>。路線の本数がいちばん少ない道（1本）と、合計時間がいちばん短い道（3本）は別の道です。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "重み付きグラフとは", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("04", SLIDES),
    advanced_section("04"),
    rubric_section("04"),
    ans,
])

write("04", NAV, body)
