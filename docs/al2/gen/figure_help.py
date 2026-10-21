# -*- coding: utf-8 -*-
"""標準課題の「描き方」を示す小さな図。課題セクションに入れる（答えは含まない）。"""
from common import fig, GREEN, AMBER, GRAY


def tree_help(unit="か所", root="出発点", names=("A", "B"), unit_word="分"):
    """枝分かれ図（木）とは何かを、2か所だけ回る小さな例で示す。
    3か所の答えは含まない（学生が自分で6本に広げる）。"""
    a, b = names
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         f'枝分かれ図（木）の描き方 ── 2{unit}を回る場合の例</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '上から下へ「次にどこへ行くか」で枝を分け、いちばん下に合計を書く</text>']

    def box(x, y, w, h, text, color="#444", fill="#141414", tcolor="#E0E0E0", bold=False):
        s.append(f'        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        weight = ' font-weight="700"' if bold else ""
        s.append(f'        <text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" fill="{tcolor}" font-size="12"'
                 f'{weight}>{text}</text>')

    def arrow(x1, y1, x2, y2):
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="2"/>')
        s.append(f'        <polygon points="{x2},{y2} {x2 - 5},{y2 - 9} {x2 + 5},{y2 - 9}" fill="#777"/>')

    # 根
    box(230, 62, 80, 30, root, GREEN, "#0f1f08", GREEN, True)
    # 1段目: 2つに分かれる
    for i, first in enumerate((a, b)):
        x = 130 + i * 200
        arrow(270, 92, x + 40, 122)
        box(x, 124, 80, 30, first)
        second = b if first == a else a
        arrow(x + 40, 154, x + 40, 184)
        box(x, 186, 80, 30, second)
        arrow(x + 40, 216, x + 40, 246)
        box(x, 248, 80, 30, f"{root}へ戻る", "#444", "#141414", "#bbb")
        arrow(x + 40, 278, x + 40, 308)
        box(x - 6, 310, 92, 30, f"合計 ○○{unit_word}", AMBER, "#1a1200", AMBER, True)
    # 説明
    s.append(f'        <text x="470" y="140" fill="{GRAY}" font-size="11">← 最初に行く場所で枝が分かれる</text>')
    s.append(f'        <text x="470" y="202" fill="{GRAY}" font-size="11">← 残りの場所（2{unit}なら1つしか残らない）</text>')
    s.append(f'        <text x="470" y="326" fill="{AMBER}" font-size="11">← 枝の先に、その順番の合計を書く</text>')
    s.append(f'        <text x="350" y="366" text-anchor="middle" fill="#E0E0E0" font-size="12">'
             f'3{unit}を回るときは、1段目が3つ、2段目が2つに分かれて、枝の先は 3×2×1 = 6本になる</text>')
    s.append(f'        <text x="350" y="386" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '合計は実行結果から写す。そのあと1本目から順に比べ、「いまのところ最短」がどう変わるかを描く</text>')
    return fig(700, 400, "\n".join(s))


def graph_help():
    """グラフ・隣接リスト・隣接行列の描き方を、3頂点 A・B・C の小さな例で示す。
    下半分はスライドの配置の例。学生の頂点（5つ以上）の答えは含まない。"""
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '描き方の例 ── 3つの頂点 A・B・C、辺 A—B と A—C の場合</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '自分の頂点（5つ以上）で、同じ3つを描く</text>']

    def t(x, y, text, size=12, fill="#E0E0E0", anchor="middle", bold=False):
        w = ' font-weight="700"' if bold else ""
        s.append(f'        <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-size="{size}"{w}>{text}</text>')

    # ① グラフ
    t(110, 74, "① グラフ", 13, GREEN, bold=True)
    pos = {"A": (110, 108), "B": (60, 186), "C": (160, 186)}
    for a, b in (("A", "B"), ("A", "C")):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="2.5"/>')
    for i, (name, (x, y)) in enumerate(pos.items()):
        s.append(f'        <circle cx="{x}" cy="{y}" r="20" fill="#1A1A1A" stroke="{GREEN}" stroke-width="2"/>')
        t(x, y + 5, name, 13, bold=True)
        t(x + 20, y - 16, str(i), 11, AMBER, bold=True)
    t(110, 232, "頂点3個 ／ 辺2本", 12, GREEN, bold=True)
    t(110, 250, "丸の右上に番号（0から）", 10, GRAY)

    # ② 隣接リスト
    t(340, 74, "② 隣接リスト", 13, GREEN, bold=True)
    rows = [("A", "B、C"), ("B", "A"), ("C", "A")]
    for i, (k, v) in enumerate(rows):
        y = 96 + i * 38
        s.append(f'        <rect x="270" y="{y}" width="44" height="30" rx="6" fill="#222" stroke="#555"/>')
        t(292, y + 20, k, 13, GREEN, bold=True)
        s.append(f'        <rect x="314" y="{y}" width="96" height="30" rx="6" fill="#141414" stroke="#555"/>')
        t(324, y + 20, "→ " + v, 12, anchor="start")
    t(340, 232, "辺 A—B は A の行と", 10, GRAY)
    t(340, 248, "B の行の両方に書く", 10, GRAY)

    # ③ 隣接行列
    t(570, 74, "③ 隣接行列", 13, AMBER, bold=True)
    c, mx, my = 34, 520, 104
    m = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
    for j in range(3):
        t(mx + j * c + c / 2, my - 8, str(j), 11, GRAY)
    for i, name in enumerate("ABC"):
        t(mx - 8, my + i * c + 22, f"{i} {name}", 11, GRAY, "end")
        for j in range(3):
            v = m[i][j]
            s.append(f'        <rect x="{mx + j * c}" y="{my + i * c}" width="{c - 3}" height="{c - 3}" rx="5" '
                     f'fill="{"#1a2e0a" if v else "#141414"}" stroke="{"#76B900" if v else "#3a3a3a"}"/>')
            t(mx + j * c + (c - 3) / 2, my + i * c + 21, str(v), 13, "#E0E0E0" if v else "#666", bold=bool(v))
    s.append(f'        <line x1="{mx}" y1="{my}" x2="{mx + 3 * c - 3}" y2="{my + 3 * c - 3}" stroke="{AMBER}" '
             'stroke-width="1.2" stroke-dasharray="4 3"/>')
    t(570, 232, "番号で行と列を並べる", 10, GRAY)
    t(570, 248, "点線をはさんで左右対称になる", 10, GRAY)

    s.append('        <line x1="225" y1="66" x2="225" y2="254" stroke="#333"/>')
    s.append('        <line x1="455" y1="66" x2="455" y2="254" stroke="#333"/>')

    # スライドの配置の例
    y0 = 290
    t(350, y0 - 6, "スライドの配置の例（1枚に収まらなければ分けてよい）", 13, GREEN, bold=True)
    s.append(f'        <rect x="110" y="{y0 + 6}" width="480" height="270" rx="8" fill="#F4F4F4" stroke="#888"/>')
    t(126, y0 + 30, "第3回: ○○（自分の頂点）のグラフを書き写す", 12, "#222", "start", True)
    s.append(f'        <line x1="126" y1="{y0 + 40}" x2="574" y2="{y0 + 40}" stroke="#ccc"/>')
    boxes = [(126, "① グラフ", "丸と線、番号、", "頂点と辺の数"), (276, "② 隣接リスト", "頂点ごとに", "1行ずつ"),
             (426, "③ 隣接行列", "0 と 1 の表", "（番号つき）")]
    for x, title, l1, l2 in boxes:
        s.append(f'        <rect x="{x}" y="{y0 + 52}" width="140" height="150" rx="6" fill="#FFFFFF" '
                 'stroke="#999" stroke-dasharray="5 4"/>')
        t(x + 70, y0 + 112, title, 12, "#3E7A00" if "③" not in title else "#B26A00", bold=True)
        t(x + 70, y0 + 134, l1, 10, "#777")
        t(x + 70, y0 + 150, l2, 10, "#777")
    s.append(f'        <rect x="126" y="{y0 + 212}" width="440" height="50" rx="6" fill="#FFFFFF" '
             'stroke="#999" stroke-dasharray="5 4"/>')
    t(346, y0 + 234, "理解度チェックの答え（1〜2行）", 12, "#222", bold=True)
    t(346, y0 + 252, "足す辺の2頂点の名前と、変わる「か所」「マス」の数、理由", 10, "#777")
    t(350, y0 + 300, "図の中の頂点の名前・番号は、すべて自分で決めたものにする（A・B・C や授業の駅名は使わない）",
      11, "#E0E0E0")
    return fig(700, y0 + 316, "\n".join(s))


def weighted_help():
    """重み付きグラフ・幅優先探索の道・いちばん短い道の描き方を、3頂点 A・B・C の小さな例で示す。
    下半分はスライドの配置の例。学生の頂点（5つ以上）の答えは含まない。"""
    BLUE = "#5AAAFF"
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '描き方の例 ── 頂点 A・B・C、出発 A → ゴール C の場合</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '自分の頂点（5つ以上）と時間で、同じ3つを描く</text>']

    def t(x, y, text, size=12, fill="#E0E0E0", anchor="middle", bold=False):
        w = ' font-weight="700"' if bold else ""
        s.append(f'        <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-size="{size}"{w}>{text}</text>')

    def graph(cx, title, tcolor, route=None, color=None, order=None):
        t(cx, 74, title, 13, tcolor, bold=True)
        pos = {"A": (cx - 60, 190), "B": (cx, 104), "C": (cx + 60, 190)}
        edges = [("A", "B", 3), ("B", "C", 4), ("A", "C", 10)]
        on = set()
        if route:
            on = {frozenset((route[i], route[i + 1])) for i in range(len(route) - 1)}
        for a, b, w in edges:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            hot = frozenset((a, b)) in on
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color if hot else "#888"}" '
                     f'stroke-width="{5 if hot else 2.5}"/>')
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            s.append(f'        <rect x="{mx - 18}" y="{my - 10}" width="36" height="20" rx="6" fill="#0A0A0A" '
                     f'stroke="{color if hot else "#555"}"/>')
            t(mx, my + 5, f"{w}分", 11, color if hot else "#ddd")
        for name, (x, y) in pos.items():
            s.append(f'        <circle cx="{x}" cy="{y}" r="19" fill="#1A1A1A" stroke="{GREEN}" stroke-width="2"/>')
            t(x, y + 5, name, 13, bold=True)
            if order and name in order:
                t(x + 30, y + 5, "①②③"[order.index(name)], 13, BLUE, bold=True)

    graph(110, "① 重み付きグラフ", GREEN)
    t(110, 232, "線のまん中に時間を書く", 10, GRAY)
    graph(340, "② 幅優先探索の道（色1）", BLUE, ["A", "C"], BLUE, ["A", "B", "C"])
    t(340, 232, "取り出した順 ①A ②B ③C", 10, GRAY)
    t(340, 250, "路線1本 ／ 合計 10分", 12, BLUE, bold=True)
    graph(570, "③ いちばん短い道（色2）", GREEN, ["A", "B", "C"], GREEN)
    t(570, 232, "3 + 4 = 7", 10, GRAY)
    t(570, 250, "路線2本 ／ 合計 7分", 12, GREEN, bold=True)
    s.append('        <line x1="225" y1="66" x2="225" y2="258" stroke="#333"/>')
    s.append('        <line x1="455" y1="66" x2="455" y2="258" stroke="#333"/>')

    y0 = 294
    t(350, y0 - 6, "スライドの配置の例（1枚に収まらなければ分けてよい）", 13, GREEN, bold=True)
    s.append(f'        <rect x="110" y="{y0 + 6}" width="480" height="270" rx="8" fill="#F4F4F4" stroke="#888"/>')
    t(126, y0 + 30, "第4回: ○○（自分の頂点）で、乗りかえが少ない道と時間が短い道", 12, "#222", "start", True)
    s.append(f'        <line x1="126" y1="{y0 + 40}" x2="574" y2="{y0 + 40}" stroke="#ccc"/>')
    boxes = [(126, "① 重み付きグラフ", "#3E7A00", "丸と線、", "線ごとの時間"),
             (276, "② 幅優先探索の道", "#1565C0", "取り出した順の番号、", "本数と合計（色1）"),
             (426, "③ いちばん短い道", "#3E7A00", "本数と合計、", "足し算の式（色2）")]
    for x, title, color, l1, l2 in boxes:
        s.append(f'        <rect x="{x}" y="{y0 + 52}" width="140" height="150" rx="6" fill="#FFFFFF" '
                 'stroke="#999" stroke-dasharray="5 4"/>')
        t(x + 70, y0 + 112, title, 12, color, bold=True)
        t(x + 70, y0 + 134, l1, 10, "#777")
        t(x + 70, y0 + 150, l2, 10, "#777")
    s.append(f'        <rect x="126" y="{y0 + 212}" width="440" height="50" rx="6" fill="#FFFFFF" '
             'stroke="#999" stroke-dasharray="5 4"/>')
    t(346, y0 + 234, "理解度チェックの答え（1〜2行）", 12, "#222", bold=True)
    t(346, y0 + 252, "書き換える辺と時間、そうすると一致する理由", 10, "#777")
    t(350, y0 + 300, "図の中の頂点の名前・時間は、すべて自分で決めたものにする（A・B・C や授業の駅名は使わない）",
      11, "#E0E0E0")
    return fig(700, y0 + 316, "\n".join(s))


def dijkstra_help():
    """確定の順番・書き直し・道順の組み立ての描き方を、4頂点 A・B・C・D の小さな例で示す。
    下半分はスライドの配置の例。学生の地図の答えは含まない。"""
    BLUE = "#5AAAFF"
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '描き方の例 ── 場所 A・B・C・D、出発 A の場合</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '自分の地図（ひな形より場所が2つ以上多い）と自分のナビで、同じ3つを描く</text>']

    def t(x, y, text, size=12, fill="#E0E0E0", anchor="middle", bold=False):
        w = ' font-weight="700"' if bold else ""
        s.append(f'        <text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-size="{size}"{w}>{text}</text>')

    def node(x, y, name, ring=GREEN):
        s.append(f'        <circle cx="{x}" cy="{y}" r="19" fill="#1A1A1A" stroke="{ring}" stroke-width="2"/>')
        t(x, y + 5, name, 13, bold=True)

    def edge(p, q, w, color="#888", width=2.5):
        s.append(f'        <line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{color}" stroke-width="{width}"/>')
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        s.append(f'        <rect x="{mx - 18}" y="{my - 10}" width="36" height="20" rx="6" fill="#0A0A0A" stroke="#555"/>')
        t(mx, my + 5, f"{w}分", 11, color if color != "#888" else "#ddd")

    # ① 地図: 確定の順番と最後の時間
    t(150, 74, "① 地図に、確定の順番と最後の時間", 13, GREEN, bold=True)
    pos = {"A": (60, 160), "B": (150, 100), "C": (150, 220), "D": (250, 160)}
    for a, b, w in [("A", "B", 2), ("A", "C", 6), ("B", "C", 3), ("C", "D", 2), ("B", "D", 8)]:
        edge(pos[a], pos[b], w)
    for (name, (x, y)), order, minutes in zip(pos.items(), ["1番", "2番", "3番", "4番"], [0, 2, 5, 7]):
        node(x, y, name)
        lx, ly = {"A": (x, y - 26), "B": (x + 50, y + 5), "C": (x, y + 38), "D": (x, y - 26)}[name]
        t(lx, ly, f"{order} {minutes}分", 12, BLUE, bold=True)
    s.append('        <line x1="316" y1="66" x2="316" y2="258" stroke="#333"/>')

    # ② 書き直し1つ
    t(340, 74, "② 書き直し1つ、足し算の式つきで", 13, AMBER, "start", True)
    t(340, 100, "B を確定したとき", 11, GRAY, "start")
    node(370, 128, "B")
    t(370, 164, "2分", 11, GREEN, bold=True)
    edge((389, 128), (481, 128), 3, AMBER, 4)
    node(500, 128, "C", AMBER)
    t(530, 124, "6分 → 5分", 13, AMBER, "start", True)
    t(530, 144, "2 + 3 = 5", 12, "#E0E0E0", "start")
    s.append('        <line x1="330" y1="178" x2="690" y2="178" stroke="#333"/>')

    # ③ 道順の組み立て（ゴール D から came_from で逆にたどる）
    t(340, 198, "③ 演習2の1区間を、ゴールから came_from でたどる", 13, BLUE, "start", True)
    trace = ["D", "C", "B", "A"]
    for i, name in enumerate(trace):
        x = 365 + i * 92
        node(x, 226, name, BLUE)
        if i < len(trace) - 1:
            s.append(f'        <line x1="{x + 70}" y1="226" x2="{x + 27}" y2="226" stroke="{BLUE}" stroke-width="2"/>')
            s.append(f'        <polygon points="{x + 21},226 {x + 29},222 {x + 29},230" fill="{BLUE}"/>')
            t(x + 46, 258, f"came_from[{name}]={trace[i + 1]}", 9, BLUE)
    t(340, 286, "ひっくり返すと A → B → C → D（2 + 3 + 2 = 7分）", 12, "#E0E0E0", "start", True)

    y0 = 316
    t(350, y0 - 6, "スライドの配置の例（1枚に収まらなければ分けてよい）", 13, GREEN, bold=True)
    s.append(f'        <rect x="110" y="{y0 + 6}" width="480" height="270" rx="8" fill="#F4F4F4" stroke="#888"/>')
    t(126, y0 + 30, "第5回: 自分のディズニー地図で、距離表の書き直しと道順の組み立て", 12, "#222", "start", True)
    s.append(f'        <line x1="126" y1="{y0 + 40}" x2="574" y2="{y0 + 40}" stroke="#ccc"/>')
    boxes = [(126, 200, "① 自分の地図", "#3E7A00", "丸・線・時間、", "確定の順番と最後の時間"),
             (334, 104, "② 書き直し1つ", "#B26A00", "前 → 新、", "足し算の式"),
             (446, 120, "③ 道順の組み立て", "#1565C0", "came_from の矢印、", "道順と区間の時間")]
    for x, w, title, color, l1, l2 in boxes:
        s.append(f'        <rect x="{x}" y="{y0 + 52}" width="{w}" height="150" rx="6" fill="#FFFFFF" '
                 'stroke="#999" stroke-dasharray="5 4"/>')
        t(x + w / 2, y0 + 112, title, 12, color, bold=True)
        t(x + w / 2, y0 + 134, l1, 10, "#777")
        t(x + w / 2, y0 + 150, l2, 10, "#777")
    s.append(f'        <rect x="126" y="{y0 + 212}" width="440" height="50" rx="6" fill="#FFFFFF" '
             'stroke="#999" stroke-dasharray="5 4"/>')
    t(346, y0 + 234, "理解度チェックの答え（1〜2行）", 12, "#222", bold=True)
    t(346, y0 + 252, "通行止めにした道、予想、実行した結果", 10, "#777")
    t(350, y0 + 300, "図の中の場所の名前・時間は、すべて自分の地図のものにする（A・B・C・D や授業の駅名は使わない）",
      11, "#E0E0E0")
    return fig(700, y0 + 316, "\n".join(s))
