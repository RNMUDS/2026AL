# -*- coding: utf-8 -*-
"""第3回: グラフとデータ構造の再確認 の本文を組み立てる。"""
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, blank_answers, example_pair,
                    AMBER, GRAY, GREEN, answers, code, example, fig, keywords,
                    notion, reveal, run, section, setup_guide, standard,
                    write)

STATIONS = ["新宿", "渋谷", "池袋", "東京", "品川", "上野"]
LINES = [("新宿", "渋谷"), ("新宿", "池袋"), ("新宿", "東京"),
         ("渋谷", "品川"), ("東京", "品川"), ("東京", "上野"), ("池袋", "上野")]
POS = {"池袋": (260, 62), "新宿": (176, 146), "上野": (470, 62),
       "東京": (408, 152), "渋谷": (206, 252), "品川": (356, 252)}


def node(name, x, y, color=GREEN, r=26, fill="#1A1A1A", text_fill="#E0E0E0"):
    return (f'        <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>\n'
            f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="{text_fill}" font-size="12" font-weight="700">{name}</text>')


def edges_svg(color="#555", width=2):
    out = []
    for a, b in LINES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        out.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: グラフの用語
# ────────────────────────────────────────────────────────────
def fig_graph_terms():
    dur = 15
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'グラフの言葉: 頂点と辺</text>']
    s += edges_svg()
    for name, (x, y) in POS.items():
        s.append(node(name, x, y, color="#555"))
    # ① 頂点を光らせる
    for i, (name, (x, y)) in enumerate(POS.items()):
        s.append(f'        <circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{GREEN}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{0.04+i*0.02:.3f};{0.06+i*0.02:.3f};0.30;0.34;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.04;0.08;0.30;0.34;1" dur="{dur}s" repeatCount="indefinite"/>'
             '① 頂点＝ 駅。全部で6個</text>')
    # ② 辺を光らせる
    for i, (a, b) in enumerate(LINES):
        (x1, y1), (x2, y2) = POS[a], POS[b]
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AMBER}" stroke-width="4" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{0.36+i*0.02:.3f};{0.38+i*0.02:.3f};0.62;0.66;1" dur="{dur}s" repeatCount="indefinite"/></line>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.36;0.40;0.62;0.66;1" dur="{dur}s" repeatCount="indefinite"/>'
             '② 辺＝ 路線。全部で7本</text>')
    # ③ 重みの予告
    weights = {("新宿", "渋谷"): 7, ("新宿", "池袋"): 9, ("新宿", "東京"): 14,
               ("渋谷", "品川"): 15, ("東京", "品川"): 11, ("東京", "上野"): 6, ("池袋", "上野"): 12}
    for (a, b), w in weights.items():
        (x1, y1), (x2, y2) = POS[a], POS[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;0.68;0.72;0.94;0.97;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<rect x="{mx-14}" y="{my-11}" width="28" height="22" rx="6" fill="#0A0A0A" stroke="{GRAY}"/>'
                 f'<text x="{mx}" y="{my+5}" text-anchor="middle" fill="#ccc" font-size="12">{w}</text></g>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{GRAY}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.68;0.72;0.94;0.97;1" dur="{dur}s" repeatCount="indefinite"/>'
             '③ 重み＝ 辺ごとの数値。第4回であつかう</text>')
    return fig(700, 322, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 隣接リストと隣接行列は同じグラフを表す
# ────────────────────────────────────────────────────────────
def fig_list_vs_matrix():
    n = len(STATIONS)
    adj = {st: [] for st in STATIONS}
    for a, b in LINES:
        adj[a].append(b)
        adj[b].append(a)
    matrix = [[0] * n for _ in range(n)]
    for a, b in LINES:
        i, j = STATIONS.index(a), STATIONS.index(b)
        matrix[i][j] = matrix[j][i] = 1

    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じグラフを2通りの形で書き写す</text>',
         f'        <text x="175" y="52" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">隣接リスト</text>',
         f'        <text x="175" y="70" text-anchor="middle" fill="{GRAY}" font-size="11">駅ごとに、となりの駅を並べる</text>',
         f'        <text x="500" y="52" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">隣接行列</text>',
         f'        <text x="500" y="70" text-anchor="middle" fill="{GRAY}" font-size="11">表を作り、つながっていれば1を書く</text>',
         '        <line x1="345" y1="44" x2="345" y2="290" stroke="#333" stroke-width="1"/>']
    # 左: 隣接リスト
    for i, st in enumerate(STATIONS):
        y = 96 + i * 30
        s.append(f'        <rect x="24" y="{y-16}" width="300" height="26" rx="6" fill="#141414" stroke="#2e2e2e"/>')
        s.append(f'        <text x="36" y="{y+2}" fill="{GREEN}" font-size="12" font-weight="700">{st}</text>')
        s.append(f'        <text x="90" y="{y+2}" fill="#ccc" font-size="12">→ ' + "、".join(adj[st]) + '</text>')
    # 右: 隣接行列
    cell = 30
    mx0, my0 = 396, 100
    for j, st in enumerate(STATIONS):
        s.append(f'        <text x="{mx0+j*cell+cell/2}" y="{my0-9}" text-anchor="middle" fill="{GRAY}" font-size="10">{st}</text>')
    for i, st in enumerate(STATIONS):
        s.append(f'        <text x="{mx0-8}" y="{my0+i*cell+cell/2+4}" text-anchor="end" fill="{GRAY}" font-size="10">{st}</text>')
        for j in range(n):
            v = matrix[i][j]
            s.append(f'        <rect x="{mx0+j*cell}" y="{my0+i*cell}" width="{cell-2}" height="{cell-2}" rx="4" '
                     f'fill="{"#1a2e0a" if v else "#141414"}" stroke="{AMBER if v else "#2e2e2e"}"/>')
            s.append(f'        <text x="{mx0+j*cell+(cell-2)/2}" y="{my0+i*cell+(cell-2)/2+4}" text-anchor="middle" '
                     f'fill="{"#93D500" if v else "#555"}" font-size="12">{v}</text>')
    # 対応する行を同時に光らせる
    for i in range(n):
        a, b = i / n, (i + 1) / n
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        y = 96 + i * 30
        s.append(f'        <rect x="24" y="{y-16}" width="300" height="26" rx="6" fill="none" stroke="{GREEN}" stroke-width="2.5" opacity="0">{anim}</rect>')
        s.append(f'        <rect x="{mx0-2}" y="{my0+i*cell-2}" width="{n*cell+2}" height="{cell+2}" rx="6" fill="none" stroke="{GREEN}" stroke-width="2.5" opacity="0">{anim}</rect>')
    s.append(f'        <text x="350" y="300" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '左の1行と右の1行は、まったく同じつながりを表している</text>')
    return fig(700, 316, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 駅の数が増えたときの必要なマス数
# ────────────────────────────────────────────────────────────
def fig_size_compare():
    rows = [(10, 100, 30), (100, 10000, 300), (1000, 1000000, 3000), (10000, 100000000, 30000)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '駅の数が増えたとき、書きこむ量はどうなるか</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり（どの駅も、となりの駅が平均3つとして計算）</text>']
    import math
    for i, (count, mat, lst) in enumerate(rows):
        y = 66 + i * 62
        s.append(f'        <text x="24" y="{y+22}" fill="#E0E0E0" font-size="12" font-weight="700">駅{count:,}個</text>')
        for j, (name, v, color) in enumerate([("隣接行列", mat, AMBER), ("隣接リスト", lst, GREEN)]):
            yy = y + j * 26
            w = math.log10(v) / 8 * 400
            s.append(f'        <text x="106" y="{yy+16}" fill="{GRAY}" font-size="10">{name}</text>')
            s.append(f'        <rect x="168" y="{yy+2}" width="{w:.0f}" height="18" rx="4" fill="{color}" opacity="0.85"/>')
            unit = "マス" if name == "隣接行列" else "個"
            s.append(f'        <text x="{168+w+10:.0f}" y="{yy+16}" fill="{color}" font-size="11" font-weight="700">{v:,}{unit}</text>')
    s.append(f'        <text x="350" y="{66+4*62+14}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '駅が1万個になると、隣接行列は隣接リストの約3300倍の量を書きこむことになる</text>')
    return fig(700, 66 + 4 * 62 + 32, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 路線を1本ずつ書き写す（隣接リストと隣接行列が同時に育つ）
# ────────────────────────────────────────────────────────────
def fig_build_steps(steps=3):
    sc, ox = 0.42, -40
    row_h = 150
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '路線を1本ずつ書き写す（手順1〜3）</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '橙 = いま書き写した路線と、そのとき増えたところ。緑 = もう書き写した路線</text>']
    for k in range(steps):
        y0 = 70 + k * row_h
        done, cur = LINES[:k], LINES[k]
        s.append(f'        <text x="20" y="{y0+12}" fill="#E0E0E0" font-size="12" font-weight="700">手順{k+1}</text>')
        s.append(f'        <text x="20" y="{y0+28}" fill="{AMBER}" font-size="11">{cur[0]}—{cur[1]}</text>')
        # 小さなグラフ
        p = {st: (ox + 60 + x * sc, y0 + 10 + y * sc) for st, (x, y) in POS.items()}
        for e in LINES:
            (x1, y1), (x2, y2) = p[e[0]], p[e[1]]
            color, w = ("#333", 1.5)
            if e in done:
                color, w = GREEN, 2.5
            if e == cur:
                color, w = AMBER, 3.5
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="{w}"/>')
        for st, (x, y) in p.items():
            ring = AMBER if st in cur else "#555"
            s.append(f'        <circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="#1A1A1A" stroke="{ring}" stroke-width="1.5"/>')
            s.append(f'        <text x="{x:.0f}" y="{y+3:.0f}" text-anchor="middle" fill="#ddd" font-size="8">{st}</text>')
        # 隣接リスト
        lx = 240
        s.append(f'        <text x="{lx}" y="{y0+8}" fill="{GREEN}" font-size="11" font-weight="700">隣接リスト</text>')
        adj = {st: [] for st in STATIONS}
        for x_, y_ in LINES[:k + 1]:
            adj[x_].append(y_)
            adj[y_].append(x_)
        for i, st in enumerate(STATIONS):
            yy = y0 + 26 + i * 18
            s.append(f'        <text x="{lx}" y="{yy}" fill="{GRAY}" font-size="10">{st} →</text>')
            parts = []
            for nb in adj[st]:
                new = {st, nb} == set(cur)
                bold = ' font-weight="700"' if new else ""
                parts.append(f'<tspan fill="{AMBER if new else "#ddd"}"{bold}>{nb}</tspan>')
            s.append(f'        <text x="{lx+44}" y="{yy}" fill="#ddd" font-size="10">{"、".join(parts)}</text>')
        # 隣接行列
        mx, my, c = 500, y0 + 14, 17
        s.append(f'        <text x="{mx-40}" y="{y0+8}" fill="{AMBER}" font-size="11" font-weight="700">隣接行列</text>')
        idx = [(STATIONS.index(x_), STATIONS.index(y_)) for x_, y_ in LINES[:k + 1]]
        ci, cj = STATIONS.index(cur[0]), STATIONS.index(cur[1])
        for i, st in enumerate(STATIONS):
            s.append(f'        <text x="{mx-4}" y="{my+i*c+12}" text-anchor="end" fill="{GRAY}" font-size="9">{i} {st}</text>')
            for j in range(6):
                v = 1 if (i, j) in idx or (j, i) in idx else 0
                new = (i, j) in ((ci, cj), (cj, ci))
                stroke = AMBER if new else ("#5a8a20" if v else "#2e2e2e")
                s.append(f'        <rect x="{mx+j*c}" y="{my+i*c}" width="{c-2}" height="{c-2}" rx="3" '
                         f'fill="{"#1a2e0a" if v else "#141414"}" stroke="{stroke}" stroke-width="{2 if new else 1}"/>')
                s.append(f'        <text x="{mx+j*c+(c-2)/2}" y="{my+i*c+11}" text-anchor="middle" '
                         f'fill="{"#E0E0E0" if v else "#555"}" font-size="9">{v}</text>')
        s.append(f'        <text x="{mx+6*c+12}" y="{my+40}" fill="{AMBER}" font-size="10">matrix[{ci}][{cj}]</text>')
        s.append(f'        <text x="{mx+6*c+12}" y="{my+56}" fill="{AMBER}" font-size="10">matrix[{cj}][{ci}]</text>')
        s.append(f'        <text x="{mx+6*c+12}" y="{my+72}" fill="{GRAY}" font-size="10">を 1 にする</text>')
        if k < steps - 1:
            s.append(f'        <line x1="20" y1="{y0+row_h-14}" x2="680" y2="{y0+row_h-14}" stroke="#2a2a2a"/>')
    y = 70 + steps * row_h + 4
    s.append(f'        <text x="350" y="{y}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '路線を1本書くたびに、隣接リストは2か所に名前が増え、隣接行列は2マスが 1 になる</text>')
    return fig(700, y + 18, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図5: 迷路をグラフに書き直す
# ────────────────────────────────────────────────────────────
def fig_maze_as_graph():
    maze = ["S.#..", "..#..", "....#", "#.#..", "...#G"]
    cell = 40
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路もグラフ: 1マスが頂点、となり合うマスのつながりが辺</text>']
    x0, y0 = 60, 60
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * cell, y0 + r * cell
            wall = maze[r][c] == "#"
            s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="5" '
                     f'fill="{"#33302a" if wall else "#141414"}" stroke="{"#4a453a" if wall else "#333"}"/>')
            label = maze[r][c] if maze[r][c] in "SG#" else ""
            if label:
                s.append(f'        <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+5}" text-anchor="middle" '
                         f'fill="{"#7a7060" if wall else AMBER}" font-size="14" font-weight="700">{label}</text>')
    s.append(f'        <text x="{x0+2.5*cell}" y="{y0+5*cell+24}" text-anchor="middle" fill="{GRAY}" font-size="12">迷路として見た形</text>')
    # 右: グラフとして見た形
    gx0, gy0 = 380, 60
    gcell = 40
    for r in range(5):
        for c in range(5):
            if maze[r][c] == "#":
                continue
            x, y = gx0 + c * gcell + 18, gy0 + r * gcell + 18
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < 5 and nc < 5 and maze[nr][nc] != "#":
                    s.append(f'        <line x1="{x}" y1="{y}" x2="{gx0+nc*gcell+18}" y2="{gy0+nr*gcell+18}" '
                             f'stroke="{GREEN}" stroke-width="2" opacity="0.7"/>')
    for r in range(5):
        for c in range(5):
            if maze[r][c] == "#":
                continue
            x, y = gx0 + c * gcell + 18, gy0 + r * gcell + 18
            s.append(f'        <circle cx="{x}" cy="{y}" r="13" fill="#1A1A1A" stroke="{GREEN}" stroke-width="1.6"/>')
            s.append(f'        <text x="{x}" y="{y+4}" text-anchor="middle" fill="#bbb" font-size="9">{r},{c}</text>')
    s.append(f'        <text x="{gx0+2.5*gcell}" y="{gy0+5*gcell+24}" text-anchor="middle" fill="{GRAY}" font-size="12">グラフとして見た形</text>')
    s.append(f'        <text x="350" y="{gy0+5*gcell+52}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '壁のマスは頂点にしない。通れるマスどうしだけを辺でつなぐ</text>')
    return fig(700, gy0 + 5 * gcell + 70, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "グラフとは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("03")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第4回からは「電車でいちばん早く着く行き方」のような問題をあつかいます。
      そのためには、まず<strong>路線図をPythonに渡す</strong>必要があります。
      ところが、コンピュータは紙の路線図を目で見ることができません。
      第3回では、路線図や迷路を<strong>グラフ</strong>という形に整理し、それを<strong>数や文字の表</strong>に書き写す方法を学びます。
    </p>

    <div class="analogy">
      第2回の迷路を思い出してください。迷路の絵をそのままPythonに渡したのではなく、
      <code>"S.....#"</code> のような<strong>文字の並び</strong>に書き写してから探索しました。
      路線図も同じで、「どの駅とどの駅がつながっているか」を文字の表に書き写せば、コンピュータが読めるようになります。
      その「書き写し方」が、今回の隣接リストと隣接行列です。
    </div>

    <h3 style="margin:2rem 0 0.8rem">グラフとは</h3>
    <p style="margin-bottom:1rem">
      グラフとは、<strong>「点」と「点どうしのつながり」だけでものごとを表す方法</strong>のことです（棒グラフや折れ線グラフとは別のもの）。
      点のことを<strong>頂点</strong>、つながりのことを<strong>辺</strong>と呼びます。
    </p>

    <div class="analogy">
      路線図を思い浮かべてください。実際の線路は曲がりくねっていますが、路線図では駅を丸で、路線をまっすぐな線で描きます。
      駅の正確な位置や線路の曲がり方は消えていますが、「どの駅とどの駅がつながっているか」は残っています。
      乗りかえを考えるときに必要な情報だけを残した形が、グラフです。
    </div>

{fig_graph_terms()}

    <div class="concept-box">
      <h4>用語</h4>
      <table>
        <tr><th>用語</th><th>意味</th><th>路線図でいうと</th></tr>
        <tr><td><strong>頂点</strong></td><td>グラフの点</td><td>駅</td></tr>
        <tr><td><strong>辺</strong></td><td>頂点どうしのつながり</td><td>駅と駅をつなぐ路線</td></tr>
        <tr><td><strong>隣接</strong></td><td>辺1本で直接つながっていること（となり同士）</td><td>乗りかえなしで次に着く駅</td></tr>
        <tr><td><strong style="color:#76B900">隣接リスト</strong></td><td>頂点ごとに、となりの頂点を並べた表</td><td>「新宿 → 渋谷、池袋、東京」</td></tr>
        <tr><td><strong style="color:#FFB800">隣接行列</strong></td><td>たてよこの表で、つながっていれば1、なければ0を書いたもの。行列は「たてよこに数を並べた表」のこと</td><td>駅×駅の早見表</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>グラフで表せるもの</h4>
      <table>
        <tr><th>あつかうもの</th><th>頂点になるもの</th><th>辺になるもの</th></tr>
        <tr><td>路線図</td><td>駅</td><td>駅と駅をつなぐ路線</td></tr>
        <tr><td>友達関係</td><td>人</td><td>友達であるという関係</td></tr>
        <tr><td>迷路</td><td>通れる1マス</td><td>となり合うマスどうしのつながり</td></tr>
        <tr><td>道路地図</td><td>交差点</td><td>交差点をつなぐ道路</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        見た目はまるで違いますが、どれも「頂点」と「辺」だけで書き直せます。
        書き直してしまえば、<strong>同じ1つのプログラムで4つとも解ける</strong>ようになります。
        第2回の迷路も、下の図のように、通れるマスを頂点、となり合うマスのつながりを辺にすれば、同じグラフとして扱えます。
      </p>
    </div>

{fig_maze_as_graph()}

    <h3 style="margin:2rem 0 0.8rem">グラフをPythonに書き写す2つの方法</h3>
    <p style="margin-bottom:1rem">
      グラフを書き写すときに残す情報は「どの頂点とどの頂点が、辺（となり同士）でつながっているか」だけです。
      書き写し方には、よく使われる方法が2つあります。どちらも<strong>同じグラフ</strong>を表していて、書き方だけが違います。
    </p>
    <ul class="point-list" style="margin-bottom:1rem">
      <li><strong style="color:#76B900">隣接リスト</strong>: 駅ごとに「となりの駅」を並べる。
          電話帳で、名前ごとに連絡先が並んでいるのに近い。Pythonでは<strong>辞書</strong>（鍵 → 値 の組を集めた入れもの）で書く。</li>
      <li><strong style="color:#FFB800">隣接行列</strong>: 駅×駅のたてよこの表を作り、つながっていれば1、つながっていなければ0を書く。
          時刻表の駅と駅の早見表に近い。Pythonでは<strong>リストのリスト</strong>（表の1行ぶんのリストを、行の数だけ並べたもの）で書く。</li>
    </ul>

{fig_list_vs_matrix()}

    <p style="margin:1.5rem 0 0.5rem">
      では、紙の路線図から2つの表を<strong>どうやって作るか</strong>を、1本ずつ追ってみます。
      路線の一覧（新宿—渋谷、新宿—池袋、新宿—東京、…）を上から1本ずつ読み、そのたびに表に書き足します。
      下の図は、最初の3本を書き写したところです。
    </p>

{fig_build_steps()}

    <div class="analogy">
      路線は<strong>行きも帰りも通れる</strong>ので、「新宿—渋谷」を書き写すときは、新宿の行に「渋谷」、渋谷の行に「新宿」と<strong>2か所</strong>に書きます。
      隣接行列でも同じで、<code>matrix[0][1]</code>（新宿の行・渋谷の列）と <code>matrix[1][0]</code>（渋谷の行・新宿の列）の<strong>2マス</strong>を1にします。
      このため、隣接行列は左上から右下へのななめの線を折り目にして、<strong>左右対称</strong>になります。
      7本ぶん書き写し終えると、上の「同じグラフを2通りの形で書き写す」の図になります。
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>グラフを絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題も、第2回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で、
      グラフを丸と線で描き、表に1つずつ書き足していくようすをアニメーションで見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各例題ファイルの<strong>いちばん下</strong>
        （「ここから下は、グラフを pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。
        丸の並べ方は、線の交わりが少なくなるように窓が自動で決めます（紙の路線図と位置がちがっても、つながり方は同じ）。</p>
      </div>
    </div>"""

ex1_body = f"""      <p>6つの駅と7本の路線からなる路線図を、隣接リストの形でPythonに書き写します。
      隣接リストは<strong>辞書</strong>を使い、「駅の名前」を鍵、「となりの駅を並べたリスト」を値にします。
      <code>railway["新宿"]</code> と書けば、新宿のとなりの駅のリストが取り出せます。
      書き写したあとで<strong>辺（路線）の数を数え</strong>、紙の路線図の7本と同じになるかを確かめます。
      同じになれば、書き写しに抜けやまちがいがないと分かります。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>railway = {{ ... }}</code></td><td>路線図を隣接リストに書き写す。1本の路線を、両方の駅の行に1回ずつ書く</td></tr>
        <tr><td><code>for station in railway:</code></td><td>駅を上から1つずつ読み、となりの駅の数 <code>len(railway[station])</code> を名前の合計 <code>name_total</code> に足していく</td></tr>
        <tr><td><code>edge_count = name_total // 2</code></td><td>名前の合計 <code>name_total</code> は、同じ路線を両側の駅から2回数えているので、半分にして路線の本数にする</td></tr>
      </table>

      <p style="margin-top:0.8rem">実行すると、ターミナルに隣接リストと頂点・辺の数が出たあと、窓が開きます。窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: グラフ</td><td>丸 = 頂点（駅）、線 = 辺（路線）。白い枠の丸が「いま読んでいる駅」、緑の丸と線がそのとなり</td></tr>
        <tr><td>左: 線のまん中の数字</td><td>その線（路線）を<strong>何回数えたか</strong>。最後はすべて 2 になる</td></tr>
        <tr><td>右: 隣接リスト</td><td>読み終えた駅の行。右端の「○個」がその駅のとなりの数</td></tr>
        <tr><td>右下</td><td>ここまでに数えた名前の合計 <code>name_total</code>。最後は <code>// 2</code> した辺の数 <code>edge_count</code></td></tr>
      </table>

{example_pair('AL2-03-ex1.py', '6つの駅それぞれについて、となりの駅が一覧で表示されました。'
     '<code>railway["新宿"]</code> と書くだけで、新宿のとなりの駅3つがすぐ取り出せています。'
     '窓の右下を見ると、名前の合計は <strong>14個</strong>、半分にした路線の数は <strong>7本</strong>です。'
     'グラフの線のまん中の数字がすべて <strong>2</strong> になっているのは、'
     '1本の路線（たとえば新宿—渋谷）を「新宿の行」と「渋谷の行」の両方から数えたためです。'
     'だから <code>// 2</code> で半分にします。')}"""

ex2_body = f"""      <p>例題1とまったく同じ路線図を、今度は隣接行列の形で書き写します。
      6つの駅があるので、たて6マス・よこ6マスの表を作ります。駅には <code>stations</code> の中の順番で <strong>0〜5 の番号</strong>をつけ、
      その番号を表の行と列の番号に使います（新宿 = 0、渋谷 = 1、…）。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>matrix = [[0 for j in range(n)] for i in range(n)]</code></td><td>全部のマスが0の、n×n の表を作る</td></tr>
        <tr><td><code>for a, b in lines:</code></td><td>路線の一覧を1本ずつ読む（1章の「路線を1本ずつ書き写す」の図と同じ）</td></tr>
        <tr><td><code>matrix[i][j] = 1</code> と <code>matrix[j][i] = 1</code></td><td>行きと帰りの2マスを1にする</td></tr>
        <tr><td><code>matrix[i][j]</code> を見る</td><td>「i番と j番の駅はつながっているか」が、表の1マスを見るだけで分かる</td></tr>
      </table>

      <p style="margin-top:0.8rem">実行すると、ターミナルに表とマスの数の比較が出たあと、窓が開きます。窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: グラフ</td><td>丸の右上の数字が駅の番号。橙の線が「いま書き写している路線」、緑の線が「もう書き写した路線」</td></tr>
        <tr><td>右: 隣接行列</td><td><code>matrix[行の番号][列の番号]</code>。橙の枠が、いま1にした2マス</td></tr>
        <tr><td>右下</td><td>いまの手順で1にしたマスの場所。最後は「1 のマスの数 = 路線の数 × 2」</td></tr>
      </table>

{example_pair('AL2-03-ex2.py', '同じ路線図が、6×6＝36マスの表になりました。'
     '左上から右下へのななめのマス（新宿と新宿のように、同じ駅どうしの組）はすべて0です。自分自身へ行く路線はないためです。'
     'また、表はそのななめの線を折り目にして<strong>左右対称</strong>になっています。'
     '「新宿と東京はつながっているか」は <code>matrix[0][3]</code> を見るだけで分かります。'
     '36マスのうち1は14マス（路線7本×2）だけで、残りの22マスは0です。'
     '隣接リストなら名前14個を書くだけで済むのに、隣接行列は<strong>つながっていない組の0まで</strong>書いているので、そのぶん場所を使います。'
     '最後の表を見ると、駅の数が1万個になったとき、隣接行列は1億マス、隣接リストは名前3万個で、約3300倍の差が出ています。', fig_size_compare())}

    <div class="concept-box">
      <h4>どちらを使えばよいか</h4>
      <table>
        <tr><th></th><th style="color:#76B900">隣接リスト</th><th style="color:#FFB800">隣接行列</th></tr>
        <tr><td>書きこむ量</td><td>路線の数 × 2 個の名前（少なくて済む）</td><td>駅の数 × 駅の数 マス（駅が多いと大きくなる）</td></tr>
        <tr><td>「となりの駅を全部」</td><td><code>railway["新宿"]</code> ですぐ取り出せる</td><td>その駅の行を左から右まで全部見る必要がある</td></tr>
        <tr><td>「AとBはつながっているか」</td><td>Aの行を探す（<code>"品川" in railway["新宿"]</code>）</td><td><code>matrix[i][j]</code> の1マスを見るだけ</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">実際の路線図や道路地図は、1つの駅や交差点のとなりが数個しかありません。
      そのため、第4回から使う探索（幅優先探索やダイクストラ法）では、「となりを全部取り出す」のが速く、場所も少なくて済む<strong>隣接リスト</strong>を使います。</p>
    </div>

{notion('例題1（実践）の窓を → キーで1手順ずつ進め、線のまん中の数字が 1 から 2 に変わる瞬間を確かめる。'
        'どの駅を読んだときに 2 になったか（＝その路線のもう一方の駅を読んだとき）を、自分の目で確認しておく。'
        '例題2（実践）の窓では、橙の枠の2マスが表のななめの線をはさんで向かい合う位置にあることを確かめる。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1と例題2のコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('03', ['AL2-03-ex1.py', 'AL2-03-ex2.py'])}

{pygame_card}

{keywords([
    ('グラフ', 'graph', '「点」と「点どうしのつながり」だけでものごとを表す方法。棒グラフや折れ線グラフとは別のもの。'),
    ('頂点', 'ちょうてん / vertex', 'グラフの「点」。駅・人・迷路の1マスなどが頂点になる。ノード（node）とも呼ぶ。'),
    ('辺', 'へん / edge', 'グラフの「つながり」。路線・友達関係・となり合うマスの関係などが辺になる。'),
    ('隣接', 'りんせつ / adjacent', '辺1本で直接つながっていること。となり同士。路線図なら、乗りかえなしで次に着く駅。'),
    ('隣接リスト', 'りんせつリスト / adjacency list', '頂点ごとに、となりの頂点を並べた表し方。Pythonでは辞書で書く。路線の数に比例した場所しか使わないので、となりが少ないグラフに向く。'),
    ('隣接行列', 'りんせつぎょうれつ / adjacency matrix', 'たてよこの表を作り、つながっていれば1、なければ0を書く表し方。行列は「たてよこに数を並べた表」。「2点がつながっているか」を1マス見るだけで調べられる。'),
    ('辞書', 'じしょ / dict', '「鍵 → 値」の組を集めたPythonの入れもの。<code>railway["新宿"]</code> のように鍵を書くと値が取り出せる。'),
])}

    <div class="note-warn">
      <strong>穴埋めの注意:</strong> 今回の穴は、まちがえてもプログラムは止まらずに最後まで動きます。
      そのかわり、<strong>数がずれます</strong>（辺の数が 14 本になる、表が左右対称にならない、など）。
      実行結果と窓の画像を、ページの画像と1行ずつ見比べてください。
    </div>

{example(1, '隣接リストで路線図を表す', ex1_body)}

{example(2, '隣接行列で同じ路線図を表す', ex2_body)}"""

ans = answers([slide_example("03"), blank_answers("03"),
    ("理解度チェックの答えの例", """        <p><strong>問い</strong>: まだつながっていない2駅の間に、路線を1本足した。隣接リストでは何か所に名前が増え、隣接行列では何マスが0から1に変わるか。</p>
        <p style="margin-top:0.6rem"><strong>答えの例</strong>（例題の路線図に「新宿—品川」を足した場合）</p>
        <table>
          <tr><th></th><th>変わるところ</th><th>数</th></tr>
          <tr><td><strong style="color:#76B900">隣接リスト</strong></td><td>新宿の行に「品川」、品川の行に「新宿」が増える</td><td><strong>2か所</strong></td></tr>
          <tr><td><strong style="color:#FFB800">隣接行列</strong></td><td><code>matrix[0][4]</code> と <code>matrix[4][0]</code> が0から1になる</td><td><strong>2マス</strong></td></tr>
        </table>
        <p style="margin-top:0.6rem"><strong>理由</strong>: 路線は行きも帰りも通れるので、1本の路線を両方の駅の側に書くため。
        そのため、名前の合計（隣接行列の1の数）は 14 から <strong>16</strong> に、路線の数は 7 から <strong>8</strong> になる。</p>"""),
    ("確かめ用の数値", """        <table>
          <tr><th>駅の数</th><th>隣接行列のマス数</th><th>隣接リストの名前の数</th></tr>
          <tr><td>10</td><td>100マス</td><td>30個</td></tr>
          <tr><td>100</td><td>10,000マス</td><td>300個</td></tr>
          <tr><td>1,000</td><td>1,000,000マス</td><td>3,000個</td></tr>
          <tr><td>10,000</td><td>100,000,000マス</td><td>30,000個</td></tr>
        </table>
        <p style="margin-top:0.6rem">駅の数が10倍になると、隣接行列は<strong>100倍</strong>、隣接リストは<strong>10倍</strong>になります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "グラフとは", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("03", SLIDES),
    advanced_section("03"),
    rubric_section("03"),
    ans,
])

write("03", NAV, body)
