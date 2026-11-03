# -*- coding: utf-8 -*-
"""第7回: ダイクストラ法（3）迷路への応用 の本文を組み立てる。
例題は「参考（床コスト付きの5×5の迷路）」と「クリエイティブ演習（ディズニーランドの園内をマス目にした地図）」の2本立て。"""
import heapq
from collections import deque
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, section, setup_guide, write)

COST5 = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

FLAT = [[1] * 8 for _ in range(8)]
RIVER = [[9 if (c == 3 and r != 4) else 1 for c in range(8)] for r in range(8)]
FOREST = [
    [1, 1, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 5, 5, 5, 5, 1],
    [5, 1, 1, 1, 5, 5, 5, 1],
    [5, 5, 1, 1, 1, 5, 5, 1],
    [5, 5, 5, 1, 1, 1, 5, 1],
    [5, 5, 5, 5, 1, 1, 1, 1],
    [5, 5, 5, 5, 5, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def solve(cost_map):
    size = len(cost_map)
    start, goal = (0, 0), (size - 1, size - 1)
    INF = float("inf")
    dist = {(r, c): INF for r in range(size) for c in range(size)}
    prev = {(r, c): None for r in range(size) for c in range(size)}
    dist[start] = 0
    pq = [(0, start)]
    done = set()
    order = []
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        order.append((u, d))
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and d + cost_map[nr][nc] < dist[(nr, nc)]:
                dist[(nr, nc)] = d + cost_map[nr][nc]
                prev[(nr, nc)] = u
                heapq.heappush(pq, (dist[(nr, nc)], (nr, nc)))
    p, n = [], goal
    while n is not None:
        p.append(n)
        n = prev[n]
    return list(reversed(p)), dist[goal], dist, order


def bfs_route(cost_map):
    size = len(cost_map)
    start, goal = (0, 0), (size - 1, size - 1)
    came = {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            break
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in came:
                came[(nr, nc)] = u
                q.append((nr, nc))
    p, n = [], goal
    while n is not None:
        p.append(n)
        n = came[n]
    p.reverse()
    return p, sum(cost_map[r][c] for r, c in p[1:])


# ────────────────────────────────────────────────────────────
# 図0: 第2回の迷路と第7回の迷路のちがい（何マス歩くか ／ 何分かかるか）
# ────────────────────────────────────────────────────────────
NEW_MAP = ["....." , "S.P.G", "....."]          # まん中の行の P がパレード（9分）
NEW_TIME = {".": 1, "S": 0, "G": 1, "P": 9}
STRAIGHT = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
AROUND = [(1, 0), (1, 1), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4)]


def fig_whats_new():
    cell, dur = 56, 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '第7回はここがちがう: 「何マス歩くか」ではなく「何分かかるか」で道を選ぶ</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '同じ地図を、2つの見方で比べる（S から G へ。まん中の P はパレードのルート）</text>']

    def grid(x0, y0, timed):
        for r, line in enumerate(NEW_MAP):
            for c, ch in enumerate(line):
                x, y = x0 + c * cell, y0 + r * cell
                parade = ch == "P" and timed
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-4}" height="{cell-4}" rx="7" '
                         f'fill="{"#3a1414" if parade else "#141414"}" stroke="{RED if parade else "#3a3a3a"}"/>')
                cx = x + (cell - 4) / 2
                # 文字はマスの上と下に書き、まん中は道の線のために空けておく
                # 文字はマスの角に書き、まん中は道の線のために空けておく
                ex, ey = x + cell - 9, y + cell - 10          # 右下の角
                if ch in "SG":
                    s.append(f'        <text x="{x+6}" y="{y+17}" fill="#fff" font-size="13" font-weight="700">{ch}</text>')
                if timed and ch != "S":
                    s.append(f'        <text x="{ex}" y="{ey}" text-anchor="end" fill="{RED if parade else "#bbb"}" '
                             f'font-size="{12 if parade else 10.5}" font-weight="700">{NEW_TIME[ch]}分</text>')
                    if parade:
                        s.append(f'        <text x="{cx}" y="{y+15}" text-anchor="middle" fill="{RED}" font-size="9">パレード</text>')
                elif not timed and ch != "S":
                    s.append(f'        <text x="{ex}" y="{ey}" text-anchor="end" fill="#777" font-size="10.5">1歩</text>')

    def route(x0, y0, path, color, start, end, dash=""):
        pts = " ".join(f"{x0 + c*cell + (cell-4)/2},{y0 + r*cell + (cell-4)/2}" for r, c in path)
        length = cell * (len(path) - 1)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" '
                 f'stroke-linejoin="round" opacity="0.85" stroke-dasharray="{length}" stroke-dashoffset="{length}">'
                 f'<animate attributeName="stroke-dashoffset" values="{length};{length};0;0" '
                 f'keyTimes="0;{start};{end};1" dur="{dur}s" repeatCount="indefinite"/></polyline>')

    def note(x, y, text, color, at, size=12, weight="700"):
        s.append(f'        <text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}" font-weight="{weight}" opacity="0">'
                 f'{text}<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{at};{at+0.02};1" '
                 f'dur="{dur}s" repeatCount="indefinite"/></text>')

    # 左: 第2回の見方
    lx, y0 = 40, 104
    s.append(f'        <text x="{lx+138}" y="80" text-anchor="middle" fill="{AMBER}" font-size="14" font-weight="700">第2回の迷路: 何マス歩くか</text>')
    grid(lx, y0, False)
    route(lx, y0, STRAIGHT, AMBER, 0.05, 0.25)
    route(lx, y0, AROUND, "#777", 0.27, 0.45)
    note(lx + 138, y0 + 190, "まっすぐ 4歩", AMBER, 0.25)
    note(lx + 138, y0 + 210, "上を回ると 6歩", "#999", 0.45, 11, "400")
    note(lx + 138, y0 + 236, "→ 歩数の少ない「まっすぐ」を選ぶ", AMBER, 0.47)
    s.append(f'        <text x="{lx+138}" y="{y0+266}" text-anchor="middle" fill="{GRAY}" font-size="10.5">どのマスも同じ1歩（パレードのマスも）</text>')
    s.append('        <line x1="350" y1="66" x2="350" y2="382" stroke="#333"/>')
    # 右: 第7回の見方
    rx = 382
    s.append(f'        <text x="{rx+138}" y="80" text-anchor="middle" fill="{GREEN}" font-size="14" font-weight="700">第7回の迷路: 何分かかるか</text>')
    grid(rx, y0, True)
    route(rx, y0, STRAIGHT, RED, 0.52, 0.68)
    route(rx, y0, AROUND, GREEN, 0.70, 0.86)
    note(rx + 138, y0 + 190, "まっすぐ 4マス: 1 + 9 + 1 + 1 = 12分", RED, 0.68, 11.5)
    note(rx + 138, y0 + 210, "上を回る 6マス: 1 + 1 + 1 + 1 + 1 + 1 = 6分", GREEN, 0.86, 11.5)
    note(rx + 138, y0 + 236, "→ 2マス多くても早い「上を回る」を選ぶ", GREEN, 0.88)
    s.append(f'        <text x="{rx+138}" y="{y0+266}" text-anchor="middle" fill="{GRAY}" font-size="10.5">マスごとに通る時間がちがう（数字 = そのマスに入る時間）</text>')
    # 下のまとめ
    y = y0 + 288
    s.append(f'        <rect x="40" y="{y}" width="620" height="54" rx="10" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="{y+22}" text-anchor="middle" fill="#ddd" font-size="12">'
             f'第2回の幅優先探索は<tspan fill="{AMBER}" font-weight="700">歩数</tspan>がいちばん少ない道、'
             f'第7回のダイクストラ法は<tspan fill="{GREEN}" font-weight="700">合計時間</tspan>がいちばん短い道を求める</text>')
    s.append(f'        <text x="350" y="{y+42}" text-anchor="middle" fill="{GRAY}" font-size="11">'
             'どのマスも1分なら、合計時間 = 歩数 になるので、2つの答えは同じになる</text>')
    return fig(700, y + 70, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図1: マスのコストは辺の重みになる
# ────────────────────────────────────────────────────────────
def fig_cell_to_edge():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路のマスのコストは、グラフの「辺の重み」として表す</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '「そのマスに入るのにかかる時間」を、そのマスへ向かう辺の重みにする</text>']
    cells = [("A", 1, 60), ("B", 9, 230), ("C", 1, 400), ("D", 1, 570)]
    for name, v, x in cells:
        deep = v >= 9
        s.append(f'        <rect x="{x-36}" y="90" width="72" height="72" rx="10" '
                 f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#444"}" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="126" text-anchor="middle" fill="{AMBER if deep else "#ccc"}" font-size="22" font-weight="700">{v}</text>')
        s.append(f'        <text x="{x}" y="150" text-anchor="middle" fill="{GRAY}" font-size="11">マス{name}</text>')
    for i in range(3):
        x1 = cells[i][2] + 36
        x2 = cells[i + 1][2] - 36
        w = cells[i + 1][1]
        s.append(f'        <line x1="{x1}" y1="126" x2="{x2}" y2="126" stroke="{GREEN}" stroke-width="2"/>')
        s.append(f'        <polygon points="{x2},126 {x2-9},121 {x2-9},131" fill="{GREEN}"/>')
    s.append(f'        <text x="350" y="196" text-anchor="middle" fill="#ccc" font-size="12">'
             'マスAからマスBへ進むときは、マスBのコスト9を払う</text>')
    s.append(f'        <rect x="90" y="216" width="520" height="76" rx="12" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="242" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'コードの上では、迷路をグラフに変換する必要はない</text>')
    s.append(f'        <text x="350" y="264" text-anchor="middle" fill="#ccc" font-size="11">'
             'となりのマスへ進むときに <tspan font-family="JetBrains Mono, monospace" fill="#cdd6f4">total + cost_map[nr][nc]</tspan> と書けば、</text>')
    s.append(f'        <text x="350" y="282" text-anchor="middle" fill="#ccc" font-size="11">'
             'それがそのまま「辺の重みを足す」ことになっている</text>')
    return fig(700, 306, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 幅優先探索とダイクストラ法の広がり方
# ────────────────────────────────────────────────────────────
def fig_spread():
    route, best, dist, order = solve(COST5)
    bfs_p, bfs_cost = bfs_route(COST5)
    # 幅優先探索の歩数
    size = 5
    steps = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        u = q.popleft()
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in steps:
                steps[(nr, nc)] = steps[u] + 1
                q.append((nr, nc))

    cell = 52
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '広がり方のちがい: 歩数の順か、コストの順か</text>']
    panels = [("幅優先探索: 歩数の順に広がる", 34, AMBER, steps, sorted(steps, key=lambda k: steps[k])),
              ("ダイクストラ法: コストの順に広がる", 386, GREEN, dist, [u for u, d in order])]
    for title, x0, color, table, seq in panels:
        s.append(f'        <text x="{x0+130}" y="54" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 66
        for r in range(5):
            for c in range(5):
                x, y = x0 + c * cell, y0 + r * cell
                v = COST5[r][c]
                deep = v >= 9
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" '
                         f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#2e2e2e"}"/>')
                s.append(f'        <text x="{x+8}" y="{y+16}" fill="{AMBER if deep else "#555"}" font-size="10">{v}</text>')
        for k, u in enumerate(seq):
            r, c = u
            x, y = x0 + c * cell, y0 + r * cell
            a = (1 - 0.16) * k / len(seq)
            s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
                     f'keyTimes="0;{a:.3f};{min(a+0.015,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
            s.append(f'          <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" fill="#1a2e0a" stroke="{color}" stroke-width="1.6"/>')
            s.append(f'          <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+8}" text-anchor="middle" fill="{color}" font-size="16" font-weight="700">{table[u]}</text>')
            s.append('        </g>')
        note = "数字はスタートからの歩数" if color == AMBER else "数字はスタートからの合計コスト"
        s.append(f'        <text x="{x0+130}" y="{y0+5*cell+22}" text-anchor="middle" fill="{GRAY}" font-size="11">{note}</text>')
    s.append('        <line x1="350" y1="44" x2="350" y2="356" stroke="#333" stroke-width="1"/>')
    s.append(f'        <text x="350" y="{66+5*cell+48}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'ダイクストラ法は、9のマスをできるだけ後回しにして広がっていく</text>')
    return fig(700, 66 + 5 * cell + 66, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 迷路の大きさと実行時間
# ────────────────────────────────────────────────────────────
def fig_scale():
    rows = [("50×50", 2500, 0.002), ("100×100", 10000, 0.009),
            ("200×200", 40000, 0.040), ("400×400", 160000, 0.192)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'マスの数が4倍になると、時間もだいたい4倍（少し多め）になる</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '例題2（参考）で測った一例。秒数はパソコンによって変わる</text>']
    for i, (size, cells, t) in enumerate(rows):
        y = 66 + i * 52
        w = t / 0.192 * 400
        s.append(f'        <text x="24" y="{y+22}" fill="#E0E0E0" font-size="12" font-weight="700">{size}</text>')
        s.append(f'        <text x="118" y="{y+22}" fill="{GRAY}" font-size="10">{cells:,}マス</text>')
        s.append(f'        <rect x="200" y="{y+6}" width="{max(w,3):.0f}" height="22" rx="5" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{200+max(w,3)+10:.0f}" y="{y+23}" fill="{GREEN}" font-size="12" font-weight="700">{t:.3f}秒</text>')
    y = 66 + 4 * 52 + 10
    s.append(f'        <rect x="24" y="{y}" width="652" height="60" rx="10" fill="#2b1a00" stroke="{RED}"/>')
    s.append(f'        <text x="350" y="{y+24}" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             '第4回の全探索: 6マス×6マス（36マス）で 約7秒</text>')
    s.append(f'        <text x="350" y="{y+45}" text-anchor="middle" fill="#ccc" font-size="11">'
             'ダイクストラ法なら160,000マスが1秒もかからない。あつかえる大きさがまるで違う</text>')
    return fig(700, y + 78, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 地形が変わると通る道が変わる
# ────────────────────────────────────────────────────────────
def fig_terrains():
    maps = [(FLAT, "地形A 平地だけ"), (RIVER, "地形B 川がある"), (FOREST, "地形C 森がある")]
    cell = 24
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ大きさの地図でも、地形が変わると通る道が変わる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '1 = 平地1秒　／　5 = 森5秒　／　9 = 川9秒</text>']
    for i, (cmap, title) in enumerate(maps):
        route, best, dist, order = solve(cmap)
        x0 = 24 + i * 228
        s.append(f'        <text x="{x0+96}" y="72" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">{title}</text>')
        y0 = 84
        mark = set(route)
        for r in range(8):
            for c in range(8):
                x, y = x0 + c * cell, y0 + r * cell
                v = cmap[r][c]
                on = (r, c) in mark
                if v >= 9:
                    fill, stroke, tc = "#2b1a00", "#5a3d00", AMBER
                elif v >= 5:
                    fill, stroke, tc = "#1e1a10", "#3d3520", "#8a7a50"
                else:
                    fill, stroke, tc = "#141414", "#2a2a2a", "#555"
                if on:
                    fill, stroke, tc = "#1a2e0a", GREEN, "#93D500"
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" fill="{fill}" stroke="{stroke}"/>')
                s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+4}" text-anchor="middle" fill="{tc}" font-size="10">{v}</text>')
        pts = " ".join(f"{x0+c*cell+(cell-2)/2},{y0+r*cell+(cell-2)/2}" for r, c in route)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="2.5" '
                 f'stroke-linejoin="round" stroke-dasharray="600" stroke-dashoffset="600">'
                 f'<animate attributeName="stroke-dashoffset" values="600;0;0" keyTimes="0;0.7;1" dur="9s" repeatCount="indefinite"/></polyline>')
        s.append(f'        <text x="{x0+96}" y="{y0+8*cell+20}" text-anchor="middle" fill="#ccc" font-size="11">'
                 f'{len(route)-1}歩 ／ 合計 {best}秒</text>')
    s.append(f'        <text x="350" y="{84+8*cell+48}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'どの地形でも14歩・14秒。歩数も合計も同じだが、通る道はまったく違う</text>')
    return fig(700, 84 + 8 * cell + 66, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "迷路とダイクストラ法 #sec-explanation",
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("07")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回・第6回では、駅や園内の場所を丸、道を線にした<strong>路線図のようなグラフ</strong>でダイクストラ法を動かしました。
      第7回は、同じダイクストラ法を<strong>マス目の迷路</strong>に使います。第2回の迷路と同じ形ですが、
      今回はマスごとに「そのマスに入るのにかかる時間」（<strong>床コスト</strong>: ゆかのコスト）がちがいます。
      第2回の幅優先探索は<strong>歩数</strong>がいちばん少ない道を見つけますが、マスの時間は見ません。
      ダイクストラ法なら、<strong>合計時間</strong>がいちばん短い道を見つけられます。
    </p>

{fig_whats_new()}

    <div class="concept-box">
      <h4>これまでの回とのちがい</h4>
      <table>
        <tr><th></th><th>第2回（迷路）</th><th>第5・6回（路線図・園内の地図）</th><th>第7回（今回）</th></tr>
        <tr><td>地図の形</td><td>マス目</td><td>丸と線（グラフ）</td><td><strong>マス目</strong></td></tr>
        <tr><td>マスや道の重さ</td><td>なし（どこも1歩）</td><td>道ごとに時間がちがう</td><td><strong>マスごとに時間がちがう</strong></td></tr>
        <tr><td>使う探索</td><td>幅優先探索</td><td>ダイクストラ法</td><td><strong>両方を同じ地図で比べる</strong></td></tr>
        <tr><td>選ぶ道</td><td>歩数がいちばん少ない道</td><td>合計時間がいちばん短い道</td><td>合計時間がいちばん短い道（歩数は多いこともある）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        一言でいうと、第2回は<strong>「何マス歩くか」</strong>、第7回は<strong>「何分かかるか」</strong>で道を選びます。
        しくみ（ダイクストラ法）は第5・6回と同じで、地図の形が第2回のマス目にもどっただけです。
      </p>
    </div>

    <div class="analogy">
      ディズニーランドでパレードが通っているとき、パレードのルートを横切るのは大変です。
      地図の上では近道でも、パレードの前で待たされると、かえって時間がかかります。
      少し遠回りでも、パレードをよけた道のほうが早く着くことがあります。
      園内をマス目に分けて、ふつうの道は1分、人ごみは3分、パレードのルートは9分、のように<strong>マスごとの時間</strong>を決めれば、
      ダイクストラ法で「いちばん早く着く道」が求まります。今回のクリエイティブ演習では、この園内マップを自分で作ります。
    </div>

{fig_cell_to_edge()}

    <div class="concept-box">
      <h4>迷路をグラフに書き直さなくてよい理由</h4>
      <p style="font-size:0.95rem">
        第3回では、迷路も「1マスが頂点、となり合うマスのつながりが辺」のグラフとして扱えることを見ました。
        第5回の <code>park</code> のような隣接リスト（場所ごとに、となりと時間を並べた表）に書き直してから解くこともできます。
        じつは書き直さなくても、<strong>となりのマスを調べるところで、直接そのマスの時間を足せば</strong>同じことになります。
      </p>
<pre><span class="code-label">Python ── となりのマスへ進む部分（例題1）</span>
<span class="kw">for</span> nxt <span class="kw">in</span> neighbors(current[<span class="num">0</span>], current[<span class="num">1</span>]):        <span class="cmt"># 上・下・左・右のマス</span>
    new_total = total + cost_map[nxt[<span class="num">0</span>]][nxt[<span class="num">1</span>]]   <span class="cmt"># ← ここが「辺の重みを足す」ことになっている</span></pre>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        <code>cost_map[nxt[0]][nxt[1]]</code>（<code>nxt</code> = となりのマスの (行, 列)）が、そのマスへ入る辺の重みです。
        迷路のように「となりがどこか」が計算で分かる問題では、隣接リストを作らずに直接あつかうのがふつうです。
        それ以外（heapq の箱・読み飛ばし・距離表）は、第6回とまったく同じです。
      </p>
    </div>

{fig_spread()}

    <div class="concept-box">
      <h4>2つの探索の広がり方のちがい</h4>
      <table>
        <tr><th></th><th>幅優先探索（第2回）</th><th>ダイクストラ法（第5・6回）</th></tr>
        <tr><td>広がる順番</td><td>歩数が少ないマスから</td><td>合計時間（コスト）が小さいマスから</td></tr>
        <tr><td>使う入れもの</td><td>キュー（<code>deque</code>: 古い順に取り出す）</td><td>優先度付きキュー（<code>heapq</code>: 小さい順に取り出す）</td></tr>
        <tr><td>求まるもの</td><td>歩数がいちばん少ない道</td><td>合計時間がいちばん小さい道</td></tr>
        <tr><td>すべてのマスの時間が同じとき</td><td colspan="2" style="text-align:center">同じ合計時間の道が求まる</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        すべてのマスの時間が1なら、合計時間は歩数と同じ値になります。
        つまり<strong>幅優先探索は、ダイクストラ法の「全部のマスが同じ時間」の場合</strong>だと言えます。
        マスの時間がちがう迷路では、幅優先探索の道はパレードの上を平気で通ってしまいます。
      </p>
    </div>

    <div class="concept-box">
      <h4>ゴールで止めてもよい ／ 止めずに最後まで動かすと、全部のマスの時間が分かる</h4>
      <p style="font-size:0.95rem">
        ダイクストラ法では、マスは<strong>時間の小さい順に</strong>確定します（第5回で確かめた「確定してよい理由」）。
        だから、<strong>ゴールのマスが確定した時点で</strong>、それより早くゴールに着く道はもうありません。
        例題1・演習1では、ここで <code>break</code> して止めています。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        反対に、止めずに queue（heapq の箱）が空になるまで続けると、<strong>スタートから全部のマスへの最短時間</strong>が1回で求まります。
        同じ時間で着くマスを同じ色でぬると、地図の等高線（同じ高さの所を結んだ線）のような図になります。
        これを今回は<strong>時間マップ</strong>と呼びます。例題2・演習2で作ります。
      </p>
    </div>

{fig_terrains()}

    <h3 style="margin:2rem 0 0.8rem">迷路を大きくすると、どれくらい時間がかかるか</h3>
    <p style="margin-bottom:1rem">
      第4回の全探索（すべての道順を1つずつ試す方法）は、マスが少し増えるだけで、試す道順の数が爆発的に増えました。
      ダイクストラ法は、1つのマスを1回だけ確定し、となりの4マスを調べるだけです。
      heapq の出し入れも、第6回で見たとおり箱の中身が100万個でも20回程度の並べ直しですみます。
      そのため、マスの数が4倍になると、かかる時間もだいたい4倍（heapq のぶんだけ少し多め）にしかなりません。
    </p>

{fig_scale()}"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>迷路と探索の進み方を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜6回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で表示します。
      例題1・演習1は<strong>幅優先探索とダイクストラ法の2つの迷路を左右に並べて</strong>、例題2・演習2は<strong>時間マップ</strong>を、1手順ずつ見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜6回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜6回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（1マス確定するごと。標準課題の図を描くときに便利）</td></tr>
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
          <tr><td><code>SyntaxError</code></td><td>カンマ・かっこ・<code>"</code> の閉じ忘れ。<code>park_map</code> の各行は <code>"G..~.....#.",</code> のように <code>"</code> で囲んで、最後にカンマ。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>park_map の ○行目の長さが …</code></td><td>行によって文字数がちがう。どの行も同じ文字数にする（空白も1文字に数えるので、空白は使わず <code>.</code> にする）</td></tr>
          <tr><td><code>park_map の (r,c) の「○」が COST にない</code></td><td>地図に、COST にない文字を書いた（全角の「．」「＃」や、小文字・大文字のちがいも別の文字）。COST に行を足すか、地図の文字を直す</td></tr>
          <tr><td><code>S が2つある</code> ／ <code>park_map に S（出発）と G …</code></td><td>S と G は<strong>1つずつ</strong>。ほかの行きたい場所は <code>.</code> にしておく</td></tr>
          <tr><td><code>COST の "○" の時間がおかしい</code></td><td>時間を <code>"3"</code> のように <code>" "</code> で囲んだか、<code>2.5</code> のような小数・マイナスにした。<code>3</code> のような 0 以上の整数で書く</td></tr>
          <tr><td><code>S から G へ行けない</code></td><td><code>#</code> で道がふさがっている。窓かターミナルの地図を見て、どこかの <code>#</code> を <code>.</code> にする</td></tr>
          <tr><td>「2つの道の合計時間が同じ」と出る</td><td>幅優先探索の道の上に、時間のかかるマスがない。ターミナルの「幅優先探索の道（*）」を見て、その上に <code>P</code> や <code>~</code> を置く</td></tr>
        </table>
      </div>"""

trouble2 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習2）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>park_map の (r,c) の「○」が COST にない</code></td><td>演習1で COST に足した記号の行を、演習2の COST に足し忘れた。<code>COST = { ... }</code> をまるごと演習1から貼りかえる</td></tr>
          <tr><td><code>park_map に S（エントランス）がない</code></td><td>貼りかえるときに S の行を消した。演習1の <code>park_map = [</code> から <code>]</code> までを、そのまま貼る</td></tr>
          <tr><td><code>bands の … がおかしい</code></td><td><code>(5, "すぐ着く")</code> のように (時間, "名前") の順で書き、組と組のあいだにカンマ。時間は <code>" "</code> で囲まない</td></tr>
          <tr><td><code>bands の ○ が、1つ前の … より小さいか同じ</code></td><td>区切りは時間の<strong>小さい順</strong>に並べる（5, 10, 15, 20 のように）</td></tr>
          <tr><td>G の時間が演習1とちがう</td><td><code>park_map</code> か <code>COST</code> が演習1とちがっている。2つとも演習1からそのまま貼りかえる</td></tr>
          <tr><td>速さを測るところで、なかなか終わらない</td><td><code>SIZES</code> に大きすぎる数を入れた（128 で数百万マス）。Ctrl+C で止めて、64 までにする</td></tr>
        </table>
      </div>"""

missions1 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の地図</td><td><code>park_map</code> を書き換えて、自分の園内マップにする（行き先 G を好きな場所に動かす、<code>#</code> の建物や <code>~</code> の人ごみ・<code>P</code> のパレードを置き直す など）。
              <code>TITLE</code> と <code>GOAL_NAME</code> も自分のものにする。S と G は1つずつ、どの行も同じ文字数にする</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>遠回りが早い</td><td>ダイクストラ法の道のほうが<strong>歩数は多いのに、合計時間は短い</strong>地図にする（ひな形はどちらも13歩）。
              ターミナルに「Lv2 達成」と出ればよい。コツ: ダイクストラ法の道（*）の途中に <code>#</code> を置いてふさぎ、少し遠回りの、パレードのない抜け道を作る</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>新しい記号</td><td><code>COST</code> に新しい記号を1つ足して、地図で使う（例: <code>"w": 2,</code> 水たまり、<code>"F": 4,</code> フードワゴンの行列）。
              窓で、その記号のマスの色と左上の数字を確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、自分らしい案内文にする。
              使える材料: <code>route</code>（通るマスの並び）、<code>minutes</code>（合計時間）、<code>len(route) - 1</code>（歩数）、<code>GOAL_NAME</code></td></tr>
        </table>
{plain('''park_map = [
    "G..~.....#.",
    "##.~.###.#.",      # ← (1,0) を # にした（池で左の小道がふさがる）
    ".#...###...",
    ".#.PPPPPPP#",      # ← (3,2) を . にした（建物のあいだの抜け道）
    ...（ここから下はひな形と同じ）''', "Lv2 の例: 2マスだけ書き換えると、幅優先探索 13歩・39分、ダイクストラ法 15歩・19分")}
      </div>"""

missions2 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の地図</td><td><code>park_map</code> と <code>COST</code> を、<strong>演習1で作った自分のもの</strong>に貼りかえる。
              ターミナルの「G までの時間」が、演習1のダイクストラ法の合計時間と<strong>同じ</strong>になることを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>時間の区切り</td><td><code>bands</code> を書き換えて、<strong>4段階以上</strong>の時間マップにする。名前も自分の言葉にする（例: <code>(3, "ダッシュで行ける")</code>）。
              窓の色分けが、自分の区切りどおりになっていることを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>園を広げる</td><td><code>SIZES</code> に <code>64</code> を足して（<code>SIZES = [4, 8, 16, 32, 64]</code>）、園を 64×64 枚ぶんに広げたときの時間を測る。
              「前の何倍」の列を見て、マスの数が4倍になると時間が何倍になるかを確かめる</td></tr>
        </table>
      </div>"""

ex1_body = f"""      <p>例題1（参考）は、1章の図と同じ5×5の迷路（数字はそのマスに入る秒数、9 はぬかるみ）を、
      <strong>幅優先探索</strong>と<strong>ダイクストラ法</strong>の2つで解いて比べるプログラムです。
      窓では2つの迷路を左右に並べて、マスが決まっていく順番を1手順ずつ見せます。
      演習1では、同じしくみで<strong>ディズニーランドの園内マップ</strong>を作り、パレードをよける道をさがします。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>neighbors(r, c)</code></td><td>上・下・左・右のうち、迷路の中にあるマスを返す（第2回と同じ）</td></tr>
        <tr><td><code>current = memo.popleft()</code></td><td>幅優先探索: メモ（キュー）のいちばん古いマスを取り出す。マスの秒数は見ない</td></tr>
        <tr><td><code>total, current = heapq.heappop(queue)</code></td><td>ダイクストラ法: 合計秒数がいちばん小さい組を取り出す（第6回と同じ）</td></tr>
        <tr><td><code>new_total = total + cost_map[nxt[0]][nxt[1]]</code></td><td>となりのマス <code>nxt</code> の秒数を足す。これが「辺の重みを足す」こと</td></tr>
        <tr><td><code>if current == goal: break</code></td><td>ゴールが確定したら止める（それより早い道はもうない）</td></tr>
        <tr><td><code>build_route(came_from)</code></td><td>ゴールから1つ前のマスを逆にたどって、道順を組み立てる（第5回と同じ）</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 幅優先探索（橙の枠）</td><td>決まったマスの数字 = スタートからの<strong>歩数</strong></td></tr>
        <tr><td>右: ダイクストラ法（緑の枠）</td><td>決まったマスの数字 = スタートからの<strong>合計秒数</strong>（演習1では合計時間（分））</td></tr>
        <tr><td>マスの色と、左上の小さい数字</td><td>そのマスに入る時間。赤 = 9（ぬかるみ、パレード）、むらさき = 少し時間がかかる（人ごみ）、灰色のブロック = 通れない建物</td></tr>
        <tr><td>白い枠</td><td>いま決まったマス。ゴールに着いたあとは、通り道のマスが白い枠になる</td></tr>
      </table>

{example_pair('AL2-07-ex1.py', '幅優先探索は<strong>8歩・16秒</strong>、ダイクストラ法は<strong>12歩・12秒</strong>という結果でした。'
     '幅優先探索の道は、左の列を下る途中で 9 のマス（ぬかるみ）を1つ通っています（1 × 7 + 9 = 16秒）。'
     'ダイクストラ法の道は、歩数は4歩多いのに 9 のマスを1つも通らず、1 のマスだけを歩いています。'
     '窓の右側では、9 のマスが後回しになり、1 のマスが先に広がっていくのが見えます。'
     '「決めたマス」は、幅優先探索が25マス（ゴールがいちばん遠い右下なので全部）、ダイクストラ法がゴールで止めたので18マスです。',
     creative=missions1)}
{trouble1}

{notion('標準課題の①は、演習1の<strong>自分の園内マップ</strong>を使う。ターミナルの「幅優先探索の道（*）」と「ダイクストラ法の道（*）」の地図を見て、'
        '2本の道を描き分ける。歩数と合計時間は、ターミナルの表から写す。窓を → キーで進めると、どちらの探索がどの順でマスを決めたかが分かる。')}"""

ex2_body = f"""      <p>例題2（参考）は、例題1と同じ迷路で、ダイクストラ法を<strong>ゴールで止めずに最後まで</strong>動かし、すべてのマスへの最小の秒数を求めるプログラムです。
      窓では、マスが確定する順に、時間の区切り（<code>bands</code>）ごとの色でぬっていきます（時間マップ）。
      後半では、迷路を 50×50 から 400×400 まで大きくして、ダイクストラ法にかかる時間を測ります。
      演習2では、<strong>演習1の自分の園内マップ</strong>の時間マップを作り、園を広げたときの速さを測ります。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>dijkstra_all(cost_map, start)</code></td><td>例題1のダイクストラ法から <code>if current == goal: break</code> を外したもの。queue が空になるまで続けて、距離表 <code>distance</code> と確定した順番 <code>order</code> を返す</td></tr>
        <tr><td><code>bands = [(4, "すぐ着く"), …]</code></td><td>時間マップの色の区切り。「4秒まで」「8秒まで」…の順に並べる</td></tr>
        <tr><td><code>random.choice([1, 1, 1, 5, 9])</code></td><td>大きな迷路のマスの秒数を、1・5・9 からでたらめに選ぶ（1 が出やすい）。<code>random.seed(7)</code> で毎回同じでたらめにしている</td></tr>
        <tr><td><code>time.perf_counter()</code></td><td>いまの時刻（秒）。ダイクストラ法の前と後で読んで、差をかかった時間にする</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: マス目</td><td>マスの数字 = スタートからの最小の時間。色 = その時間が入る区切り。同じ色のマスは、同じくらいの時間で着くマス</td></tr>
        <tr><td>右上</td><td>いま確定したマスと、その時間。最後の画面では、いちばん遠いマス（いちばん最後に確定したマス）</td></tr>
        <tr><td>右: 時間の区切り（色）</td><td>色ごとの時間の範囲と名前、その色のマスの数</td></tr>
      </table>

{example_pair('AL2-07-ex2.py', '確定した順番は (0,0)=0秒 → (0,1)=1秒 → (0,2)=2秒 → (1,2)=3秒 … と、'
     '<strong>秒数が小さいマスから順</strong>になっています。'
     'いちばん最後に確定した (3,3) は20秒で、9 のマスに囲まれているため時間がかかります。'
     '右上の (0,3) は11秒、(0,4) は12秒と、9 のマスをよけて遠回りしてたどり着く形になっています。'
     '後半の表では、マスの数が4倍になるたびに、かかった時間もおよそ4倍（少し多め）になっています。'
     '秒数そのものはパソコンによって変わりますが、「前の何倍」はどのパソコンでもだいたい4〜5倍です。',
     creative=missions2)}
{trouble2}

{notion('標準課題の②は、演習2の<strong>自分の時間マップ</strong>を使う。ターミナルの時間マップの数字を見て、マスを <code>bands</code> の区切りの色でぬる。'
        '窓を → キーで進めると、S の近くから順に色が広がっていくようすが見える。Lv3 で測った「前の何倍」も、メモしておく。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回も、例題（参考）を動かして迷路でのダイクストラ法の進み方をつかんだら、
    <strong>クリエイティブ演習</strong>で、第5・6回に続いてディズニーランドを題材に自分の作品を作ります。
    演習1で「パレードをよける園内マップ」を作って幅優先探索と比べ、演習2でその地図の「時間マップ」を作ります。</p>
    <p style="margin-bottom:1.5rem">演習のひな形の園内マップは、第5回の地図と同じく、下にエントランス、まん中にシンデレラ城、左上にウエスタンランドがある形をマス目にしたものです
    （東京ディズニーリゾート公式ブログ
    「<a href="https://www.tokyodisneyresort.jp/tdrblog/detail/190415/" style="color:#76B900" target="_blank" rel="noopener">開園当時のマップをご紹介</a>」の、今のマップを参考にした）。
    マスの時間やパレードのルートは例なので、自由に変えてかまいません。まず作業フォルダを用意します。</p>

{setup_guide('07', ['AL2-07-ex1.py', 'AL2-07-ex2.py'])}

{pygame_card}

{keywords([
    ('床コスト', 'ゆかコスト / terrain cost', 'マスごとに決まっている「そのマスに入るのにかかる時間や手間」。そのマスへ入る辺の重みとして扱う。'),
    ('幅優先探索', 'はばゆうせんたんさく / BFS', '第2回の探索。スタートから歩数の少ないマスから順に調べる。マスの時間は見ないので、歩数がいちばん少ない道が求まる。'),
    ('ダイクストラ法', 'Dijkstra', '第5・6回の探索。合計時間のいちばん小さいマスから順に確定する。合計時間がいちばん短い道が求まる（時間が 0 以上のとき）。'),
    ('時間マップ', 'じかんマップ', 'スタートから全部のマスへの最短時間を、同じくらいの時間ごとに色分けした地図。地図の等高線（同じ高さの所を結んだ線）に似ている。'),
    ('time.perf_counter()', 'パフォーマンス・カウンター', 'いまの時刻を秒で返す命令。処理の前と後で読んで引き算すると、かかった時間が分かる。'),
])}

{example(1, '床コスト付きの迷路を2つの方法で解き、パレードをよける園内マップを作る', ex1_body)}

{example(2, 'すべてのマスへの時間を求めて、自分の時間マップを作り、速さを測る', ex2_body)}"""

ans = answers([slide_example("07"),
    ("演習1のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの園内マップの結果です。自分の地図に書き換えたあとは変わります。</p>
        <table>
          <tr><th>方法</th><th>歩数</th><th>合計時間</th><th>決めたマス</th><th>通るマス</th></tr>
          <tr><td>幅優先探索</td><td>13歩</td><td>39分</td><td>72マス</td><td>エントランスからまっすぐ北へ。P を3回、~ を1回通る（9 + 9 × 3 + 3 = 39分）</td></tr>
          <tr><td>ダイクストラ法</td><td>13歩</td><td>15分</td><td>33マス</td><td>エントランスから西へ回り、左の小道を北へ。P は通らず、~ を1回だけ（12 + 3 = 15分）</td></tr>
        </table>
        <p style="margin-top:0.6rem">どちらも13歩ですが、合計時間は24分ちがいます。幅優先探索は歩数しか見ていないので、パレードの上を通る道を選んでいます。
        Lv2 の例（(1,0) を <code>#</code>、(3,2) を <code>.</code> にする）では、幅優先探索 13歩・39分、ダイクストラ法 <strong>15歩・19分</strong> になり、「Lv2 達成」と出ます。</p>"""),
    ("演習2のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの園内マップの時間マップです。</p>
        <ul style="margin-left:1.2rem;line-height:1.9">
          <li>G (0,0) までの時間: <strong>15分</strong>（演習1のダイクストラ法と同じ）</li>
          <li>確定したマス: 73マス（# 以外のマスの数と同じ）</li>
          <li>いちばん遠いマス: (3,9) = <strong>35分</strong>（右上のパレードのルートの角。入るだけで9分かかるうえ、となりのマスまでも26分かかる）</li>
          <li>色の区切りごとのマスの数: 0〜5分 13マス、6〜10分 8マス、11〜15分 14マス、16分〜 38マス</li>
        </ul>
        <p style="margin-top:0.6rem">園を広げたときの時間は、パソコンによって変わります。マスの数が4倍になるたびに、「前の何倍」がだいたい4〜5倍になっていれば正しく測れています。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "迷路とダイクストラ法", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("07", SLIDES),
    advanced_section("07"),
    rubric_section("07"),
    ans,
])

write("07", NAV, body)
