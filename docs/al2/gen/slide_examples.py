# -*- coding: utf-8 -*-
"""標準課題の「スライドの例」を SVG で描く（解答セクション用）。

例題に入っている数値（学生が自分の数値に書き換える前のもの）で描いた1枚。
「こういう図なら課題要件を満たす」という見本であって、答えそのものではない。
"""
from common import fig

# スライドの中で使う色（白い紙の上に描くので、ページの色より濃い）
INK = "#222222"
GRAY = "#777777"
GREEN = "#3E7A00"
AMBER = "#B26A00"
BLUE = "#1565C0"
RED = "#C62828"
LIGHT = "#F4F4F4"

W, H = 640, 360          # スライドの大きさ（16:9）


def _t(x, y, text, size=11, fill=INK, anchor="middle", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'font-size="{size}"{w}>{text}</text>')


def _box(x, y, w, h, fill="#FFFFFF", stroke="#999", sw=1, rx=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def _arrow(x1, y1, x2, y2, color=GRAY, sw=1.5):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 8 * math.cos(ang), y2 - 8 * math.sin(ang)
    px, py = 4 * math.sin(ang), -4 * math.cos(ang)
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{color}" stroke-width="{sw}"/>'
            f'<polygon points="{x2},{y2} {hx+px:.1f},{hy+py:.1f} {hx-px:.1f},{hy-py:.1f}" fill="{color}"/>')


def _slide(week, topic, inner, caption):
    """白いスライドの枠。見出し・中身・下の1〜2行の文章。"""
    n = int(week)
    s = [f'<rect x="30" y="20" width="{W}" height="{H}" rx="6" fill="#FFFFFF" stroke="#555"/>',
         _t(30 + 18, 20 + 28, f"第{n}回: {topic}", 15, INK, "start", 700),
         f'<line x1="48" y1="56" x2="{30 + W - 18}" y2="56" stroke="#DDD"/>',
         f'<g transform="translate(30,20)">{inner}</g>']
    for i, line in enumerate(caption):
        s.append(_t(30 + 18, 20 + H - 26 + i * 15, line, 10.5, "#333", "start"))
    s.append(_t(30 + W / 2, 20 + H + 24, "スライドの例（例題の数値で描いたもの。自分の数値に置きかえて描く）", 11, "#999"))
    return fig(W + 60, H + 56, "\n".join("        " + x for x in s), dark=False)


# ────────────────────────────────────────────────────────────
def ex01():
    order = [("郵便局", [("図書館", "カフェ", 26), ("カフェ", "図書館", 36)]),
             ("図書館", [("郵便局", "カフェ", 32), ("カフェ", "郵便局", 36)]),
             ("カフェ", [("郵便局", "図書館", 32), ("図書館", "郵便局", 26)])]
    s = [_box(290, 62, 60, 24, LIGHT, GREEN, 1.5), _t(320, 79, "学校", 11, INK, "middle", 700)]
    leaf = 0
    for i, (first, rest) in enumerate(order):
        x1 = 130 + i * 190
        s.append(_arrow(320, 86, x1 + 30, 118))
        s.append(_box(x1, 118, 60, 24)); s.append(_t(x1 + 30, 135, first))
        for j, (second, third, total) in enumerate(rest):
            x2 = x1 - 45 + j * 90
            s.append(_arrow(x1 + 30, 142, x2 + 30, 174))
            s.append(_box(x2, 174, 60, 24)); s.append(_t(x2 + 30, 191, second))
            s.append(_arrow(x2 + 30, 198, x2 + 30, 226))
            s.append(_box(x2, 226, 60, 24)); s.append(_t(x2 + 30, 243, third))
            best = total == 26
            s.append(_box(x2 - 4, 262, 68, 26, "#E8F5D8" if best else LIGHT, GREEN if best else "#999", 2 if best else 1))
            s.append(_t(x2 + 30, 280, f"{total}分", 12, GREEN if best else INK, "middle", 700 if best else None))
            if best:
                s.append(_t(x2 + 30, 304, "★最短", 10, GREEN))
            leaf += 1
    s.append(_t(610, 79, "最後は学校へ戻る", 9.5, GRAY, "end"))
    return _slide("01", "6通りの順番と合計時間", "\n".join(s),
                  ["学校→郵便局→図書館→カフェ と 学校→カフェ→図書館→郵便局 が 26分でいちばん短い（逆回りは同じ時間になる）。"])


def ex02():
    maze = ["S.....#", ".####.#", ".#....#", ".#.##..", ".#..#.#", ".##.#.#", "......G"]
    dist = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 4, (0, 5): 5, (1, 0): 1, (1, 5): 6,
            (2, 0): 2, (2, 2): 10, (2, 3): 9, (2, 4): 8, (2, 5): 7, (3, 0): 3, (3, 2): 11, (3, 5): 8, (3, 6): 9,
            (4, 0): 4, (4, 2): 12, (4, 3): 11, (4, 5): 9, (5, 0): 5, (5, 3): 10, (5, 5): 10,
            (6, 0): 6, (6, 1): 7, (6, 2): 8, (6, 3): 9, (6, 4): 10, (6, 5): 11, (6, 6): 12}
    cell = 34; ox, oy = 60, 66
    s = []
    for r in range(7):
        for c in range(7):
            x, y = ox + c * cell, oy + r * cell
            wall = maze[r][c] == "#"
            s.append(_box(x, y, cell, cell, "#555" if wall else "#FFFFFF", "#AAA", 1, 0))
            if not wall:
                label = "S" if maze[r][c] == "S" else ("G" if maze[r][c] == "G" else str(dist[(r, c)]))
                color = GREEN if label in "SG" else INK
                s.append(_t(x + cell / 2, y + cell / 2 + 4, label, 12, color, "middle", 700 if label in "SG" else None))
    path = [(r, 0) for r in range(7)] + [(6, c) for c in range(1, 7)]
    pts = " ".join(f"{ox + c * cell + cell / 2},{oy + r * cell + cell / 2}" for r, c in path)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="3" opacity="0.6"/>')
    s.append(_arrow(ox + 5 * cell + cell / 2, oy + 6 * cell + cell / 2, ox + 6 * cell + 8, oy + 6 * cell + cell / 2, GREEN, 3))
    s.append(_t(340, 90, "数字 = スタートからの歩数", 11, INK, "start", 700))
    s.append(_t(340, 110, "同じ数字のマスが「同時に」調べられる", 10.5, "#444", "start"))
    s.append(_t(340, 126, "（幅優先探索は近い順に広がる）", 10.5, "#444", "start"))
    s.append(_box(340, 146, 14, 14, "#555", "#555")); s.append(_t(360, 157, "壁（# のマス）", 10.5, INK, "start"))
    s.append(f'<line x1="340" y1="182" x2="380" y2="182" stroke="{GREEN}" stroke-width="3" opacity="0.6"/>')
    s.append(_t(388, 186, "ゴールまでの通り道（12歩）", 10.5, INK, "start"))
    s.append(_t(340, 215, "実行結果: 幅優先探索 12歩 ／ 31マス", 11, GREEN, "start", 700))
    s.append(_t(340, 233, "→ G の数字 12 と一致", 10.5, GREEN, "start"))
    return _slide("02", "幅優先探索の広がり方", "\n".join(s),
                  ["自分の迷路では、歩数が S から 1 ずつ増えて広がり、G は 12 になった。実行結果の 12歩 と一致した。"])


def ex03():
    pos = {"新宿": (110, 110), "渋谷": (70, 200), "池袋": (170, 70), "東京": (220, 150), "品川": (150, 250), "上野": (280, 90)}
    edges = [("新宿", "渋谷"), ("新宿", "池袋"), ("新宿", "東京"), ("渋谷", "品川"), ("東京", "品川"), ("東京", "上野"), ("池袋", "上野")]
    s = []
    for a, b in edges:
        s.append(f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[b][0]}" y2="{pos[b][1]}" stroke="#888" stroke-width="2"/>')
    for name, (x, y) in pos.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="18" fill="#E8F5D8" stroke="{GREEN}" stroke-width="1.5"/>')
        s.append(_t(x, y + 4, name, 11, INK, "middle", 700))
    s.append(_t(160, 300, "頂点（丸）6個 ／ 辺（線）7本", 11, GREEN, "middle", 700))
    adj = [("新宿", "渋谷、池袋、東京"), ("渋谷", "新宿、品川"), ("池袋", "新宿、上野"),
           ("東京", "新宿、品川、上野"), ("品川", "渋谷、東京"), ("上野", "池袋、東京")]
    s.append(_t(360, 82, "隣接リスト（となりの表）", 12, INK, "start", 700))
    for i, (k, v) in enumerate(adj):
        y = 100 + i * 30
        s.append(_box(360, y, 60, 24, LIGHT, "#BBB")); s.append(_t(390, y + 16, k, 11, INK, "middle", 700))
        s.append(_box(420, y, 200, 24, "#FFFFFF", "#BBB")); s.append(_t(428, y + 16, v, 11, INK, "start"))
    s.append(_t(360, 296, "表の名前の数 = 14 = 辺7本 × 2", 10.5, GRAY, "start"))
    return _slide("03", "グラフと隣接リスト", "\n".join(s),
                  ["自分で決めた6駅では、辺が7本になり、隣接リストの中身は線と一致した。実行結果の辺の数 7 と一致。"])


def ex04():
    pos = {"新宿": (90, 150), "渋谷": (200, 240), "池袋": (200, 60), "上野": (330, 60), "東京": (400, 150), "品川": (330, 240)}
    edges = [("新宿", "渋谷", 7), ("新宿", "池袋", 9), ("新宿", "品川", 30), ("渋谷", "品川", 9), ("池袋", "上野", 12), ("上野", "東京", 6), ("東京", "品川", 11)]
    s = []
    for a, b, w in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        color, sw = "#999", 2
        if (a, b) == ("新宿", "品川"):
            color, sw = BLUE, 5
        if (a, b) in [("新宿", "渋谷"), ("渋谷", "品川")]:
            color, sw = GREEN, 5
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" opacity="0.8"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'<rect x="{mx - 14}" y="{my - 9}" width="28" height="18" rx="3" fill="#FFFFFF" stroke="#DDD"/>')
        s.append(_t(mx, my + 4, f"{w}分", 10, INK))
    for name, (x, y) in pos.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="18" fill="#FFFFFF" stroke="#666" stroke-width="1.5"/>')
        s.append(_t(x, y + 4, name, 11, INK, "middle", 700))
    s.append(f'<line x1="460" y1="100" x2="500" y2="100" stroke="{BLUE}" stroke-width="5"/>')
    s.append(_t(508, 104, "幅優先探索の道", 11, INK, "start", 700))
    s.append(_t(508, 120, "新宿→品川 路線1本 30分", 10.5, BLUE, "start"))
    s.append(f'<line x1="460" y1="160" x2="500" y2="160" stroke="{GREEN}" stroke-width="5"/>')
    s.append(_t(508, 164, "いちばん短い道", 11, INK, "start", 700))
    s.append(_t(508, 180, "新宿→渋谷→品川 16分", 10.5, GREEN, "start"))
    s.append(_t(460, 220, "差 14分", 12, RED, "start", 700))
    return _slide("04", "乗りかえが少ない道と時間が短い道", "\n".join(s),
                  ["自分の時間では、幅優先探索は路線1本の道（30分）を選び、いちばん短い道は2本の道（16分）だった。"])


def ex05():
    stations = ["新宿", "渋谷", "池袋", "上野", "東京", "品川"]
    steps = [("手順1 新宿を選ぶ", ["0*", "7", "9", "-", "-", "30"], [1, 2, 5]),
             ("手順2 渋谷を選ぶ", ["0*", "7*", "9", "-", "-", "16"], [5]),
             ("手順3 池袋を選ぶ", ["0*", "7*", "9*", "21", "-", "16"], [3])]
    s = [_t(320, 78, "距離表（新宿からの時間）が手順ごとに書き直されていく", 11.5, INK, "middle", 700)]
    for i, (title, vals, changed) in enumerate(steps):
        x0 = 44 + i * 200
        s.append(_t(x0 + 88, 104, title, 11, GREEN, "middle", 700))
        for j, (name, v) in enumerate(zip(stations, vals)):
            y = 114 + j * 26
            fixed = v.endswith("*")
            s.append(_box(x0, y, 60, 24, "#E8F5D8" if fixed else LIGHT, "#BBB", 1, 0))
            s.append(_t(x0 + 30, y + 16, name, 10.5))
            s.append(_box(x0 + 60, y, 56, 24, "#FFF3D6" if j in changed else "#FFFFFF", AMBER if j in changed else "#BBB", 1.5 if j in changed else 1, 0))
            s.append(_t(x0 + 88, y + 16, v.replace("*", " ★"), 10.5, AMBER if j in changed else INK, "middle", 700 if j in changed else None))
        if i < 2:
            s.append(_arrow(x0 + 122, 185, x0 + 196, 185, GRAY, 2))
    s.append(_t(64, 292, "★ = 確定した駅（もう変わらない）　オレンジ = この手順で書き直した値", 10.5, GRAY, "start"))
    s.append(_t(64, 308, "手順2: 品川 30 → 16（渋谷経由 7+9）　手順3: 上野 - → 21（池袋経由 9+12）", 10.5, AMBER, "start"))
    return _slide("05", "ダイクストラ法の距離表", "\n".join(s),
                  ["自分の時間では、手順2で品川が 30 から 16 に書き直され、確定した順は 新宿→渋谷→池袋 だった（実行結果と一致）。"])


def ex06():
    nodes = {0: (320, 90, 1), 1: (220, 160, 3), 2: (420, 160, 2), 3: (170, 230, 8), 4: (270, 230, 9), 5: (370, 230, 5)}
    s = [_t(320, 70, "6つ入れ終わったときの heapq の中身 [1, 3, 2, 8, 9, 5] を木で描く", 11.5, INK, "middle", 700)]
    for child, parent in [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2)]:
        (x1, y1, _), (x2, y2, _) = nodes[parent], nodes[child]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="2"/>')
    for i, (x, y, v) in nodes.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="20" fill="{"#E8F5D8" if i == 0 else "#FFFFFF"}" stroke="{GREEN if i == 0 else "#666"}" stroke-width="2"/>')
        s.append(_t(x, y + 5, str(v), 14, INK, "middle", 700))
        s.append(_t(x + 26, y - 10, f"[{i}]", 9, GRAY, "start"))
    s.append(_t(320, 275, "どの親も子より小さい（1 ≦ 3, 2 ／ 3 ≦ 8, 9 ／ 2 ≦ 5）", 11, GREEN, "middle", 700))
    s.append(_t(320, 300, "取り出される順番: 1 → 2 → 3 → 5 → 8 → 9（毎回いちばん上を取る）", 11, INK))
    s.append(_t(560, 90, "[ ] は中身の何番目か", 9.5, GRAY, "end"))
    return _slide("06", "heapq の木", "\n".join(s),
                  ["自分の6つの数では中身が [1, 3, 2, 8, 9, 5] になった。並びはばらばらだが、木にすると親≦子が守られている。"])


def ex07():
    cost = [[1, 1, 1, 9, 1], [9, 9, 1, 9, 1], [1, 1, 1, 9, 1], [1, 9, 9, 9, 1], [1, 1, 1, 1, 1]]
    bfs = [(r, 0) for r in range(5)] + [(4, c) for c in range(1, 5)]
    dij = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    cell = 44; ox, oy = 70, 72
    s = []
    for r in range(5):
        for c in range(5):
            x, y = ox + c * cell, oy + r * cell
            s.append(_box(x, y, cell, cell, "#FFE0B2" if cost[r][c] == 9 else "#FFFFFF", "#AAA", 1, 0))
            s.append(_t(x + cell / 2, y + cell / 2 + 4, str(cost[r][c]), 12, INK))
    for path, color, dx in [(bfs, BLUE, -7), (dij, GREEN, 7)]:
        pts = " ".join(f"{ox + c * cell + cell / 2 + dx},{oy + r * cell + cell / 2 + dx}" for r, c in path)
        s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="4" opacity="0.7"/>')
    s.append(_t(ox, oy - 8, "S", 11, GREEN, "start", 700)); s.append(_t(ox + 5 * cell, oy + 5 * cell + 12, "G", 11, GREEN, "end", 700))
    s.append(f'<line x1="330" y1="100" x2="370" y2="100" stroke="{BLUE}" stroke-width="4"/>')
    s.append(_t(378, 104, "幅優先探索: 8歩 ／ 16秒", 11.5, INK, "start", 700))
    s.append(_t(378, 120, "歩数は最少だが 9 のマスを1つ通る", 10.5, "#444", "start"))
    s.append(f'<line x1="330" y1="160" x2="370" y2="160" stroke="{GREEN}" stroke-width="4"/>')
    s.append(_t(378, 164, "ダイクストラ法: 12歩 ／ 12秒", 11.5, INK, "start", 700))
    s.append(_t(378, 180, "4歩よけいに歩くが 9 のマスを通らない", 10.5, "#444", "start"))
    s.append(_box(330, 205, 14, 14, "#FFE0B2", "#AAA")); s.append(_t(350, 216, "コスト 9 のマス（ぬかるみ）", 10.5, INK, "start"))
    s.append(_t(330, 250, "分かれ目: 幅優先探索は S からすぐ下（9）へ、", 10.5, RED, "start"))
    s.append(_t(330, 266, "ダイクストラ法は右へ回りこんで 9 を避ける", 10.5, RED, "start"))
    return _slide("07", "床コスト迷路の2つの経路", "\n".join(s),
                  ["自分のコストでは、幅優先探索 8歩16秒・ダイクストラ法 12歩12秒で、2つの経路は S の直後で分かれた（実行結果と一致）。"])


def ex08():
    order = [("郵便局", [("図書館", "カフェ", 34.6), ("カフェ", "図書館", 40.3)]),
             ("図書館", [("郵便局", "カフェ", 41.7), ("カフェ", "郵便局", 40.3)]),
             ("カフェ", [("郵便局", "図書館", 41.7), ("図書館", "郵便局", 34.6)])]
    s = [_box(290, 62, 60, 24, LIGHT, GREEN, 1.5), _t(320, 79, "学校", 11, INK, "middle", 700),
         _t(560, 79, "4都市（学校＋3か所）", 9.5, GRAY, "start")]
    for i, (first, rest) in enumerate(order):
        x1 = 130 + i * 190
        s.append(_arrow(320, 86, x1 + 30, 118))
        s.append(_box(x1, 118, 60, 24)); s.append(_t(x1 + 30, 135, first))
        for j, (second, third, total) in enumerate(rest):
            x2 = x1 - 45 + j * 90
            s.append(_arrow(x1 + 30, 142, x2 + 30, 174))
            s.append(_box(x2, 174, 60, 24)); s.append(_t(x2 + 30, 191, second))
            s.append(_arrow(x2 + 30, 198, x2 + 30, 226))
            s.append(_box(x2, 226, 60, 24)); s.append(_t(x2 + 30, 243, third))
            best = total == 34.6
            s.append(_box(x2 - 4, 262, 68, 26, "#E8F5D8" if best else LIGHT, GREEN if best else "#999", 2 if best else 1))
            s.append(_t(x2 + 30, 280, f"{total}", 12, GREEN if best else INK, "middle", 700 if best else None))
            if best:
                s.append(_t(x2 + 30, 304, "★最短", 10, GREEN))
    return _slide("08", "全探索の枝分かれ", "\n".join(s),
                  ["自分の座標では枝が 3×2×1 = 6本になり、最短は 34.6（2通り、逆回り）。実行結果の6通りの合計と一致した。"])


def ex09():
    cities = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9), ("カフェ", 6, 12), ("公園", 3, 8)]
    def P(x, y):
        return 70 + x * 22, 300 - y * 18
    s = []
    route = [(0, 4, "6.1"), (4, 3, "5.0"), (3, 2, "8.5"), (2, 1, "7.2"), (1, 0, "8.1")]
    for k, (a, b, d) in enumerate(route, 1):
        (x1, y1), (x2, y2) = P(cities[a][1], cities[a][2]), P(cities[b][1], cities[b][2])
        s.append(_arrow(x1, y1, x2, y2, GREEN, 2.5))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'<circle cx="{mx}" cy="{my}" r="10" fill="#FFFFFF" stroke="{GREEN}"/>')
        s.append(_t(mx, my + 4, "①②③④⑤"[k - 1], 11, GREEN, "middle", 700))
        s.append(_t(mx + 13, my - 8, d, 10, AMBER, "start"))
    for name, x, y in cities:
        px, py = P(x, y)
        s.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{INK}"/>')
        s.append(_t(px + 9, py - 6, f"{name}({x},{y})", 10, INK, "start"))
    s.append(_t(430, 100, "貪欲法の進み方", 12, INK, "start", 700))
    for k, line in enumerate(["① 学校 → 公園 6.1", "② 公園 → カフェ 5.0", "③ カフェ → 図書館 8.5", "④ 図書館 → 郵便局 7.2", "⑤ 郵便局 → 学校 8.1"]):
        s.append(_t(430, 122 + k * 20, line, 11, INK, "start"))
    s.append(_t(430, 236, "合計 34.9", 13, GREEN, "start", 700))
    s.append(_t(430, 258, "毎回「いちばん近い都市」を選ぶ", 10.5, GRAY, "start"))
    return _slide("09", "貪欲法の進み方", "\n".join(s),
                  ["自分の座標では、学校→公園→カフェ→図書館→郵便局→学校 の順に進み、合計 34.9 になった（実行結果と一致）。"])


def ex10():
    names = ["公園", "カフェ", "図書館", "郵便局", "学校"]
    bits = "00101"
    s = [_t(320, 78, "5けたの 0/1 で「回った場所」を表す（右のけたが0番）", 11.5, INK, "middle", 700)]
    for i, (name, b) in enumerate(zip(names, bits)):
        x = 130 + i * 80
        s.append(_t(x + 30, 108, f"{4 - i}番", 10, GRAY))
        s.append(_t(x + 30, 124, name, 11, INK, "middle", 700))
        on = b == "1"
        s.append(_box(x, 134, 60, 50, "#E8F5D8" if on else "#FFFFFF", GREEN if on else "#999", 2 if on else 1))
        s.append(_t(x + 30, 168, b, 22, GREEN if on else "#BBB", "middle", 700))
    s.append(_t(320, 214, "bits = 5 → 2進数 00101", 12, INK, "middle", 700))
    s.append(_t(320, 236, "1 のけた: 0番（学校）と 2番（図書館）", 11.5, GREEN, "middle", 700))
    s.append(_t(320, 262, "回った場所 = {学校, 図書館}　まだ = {郵便局, カフェ, 公園}", 11, INK))
    s.append(_t(320, 290, "確かめ方: 00101 & (1 << 2) = 00100 ≠ 0 なので図書館は入っている", 10.5, GRAY))
    return _slide("10", "集合を2進数で表す", "\n".join(s),
                  ["自分で決めた数 5 は 00101 で、回った場所は学校と図書館。実行結果の「いまの集合: 00101」と一致した。"])


def ex11():
    s = [_arrow(80, 300, 600, 300, INK, 2), _arrow(80, 300, 80, 70, INK, 2),
         _t(600, 318, "必ず最適か →", 11, INK, "end", 700), _t(80, 62, "↑ 速いか", 11, INK, "start", 700),
         _t(130, 318, "近似解", 10, GRAY), _t(560, 318, "必ず最適", 10, GRAY),
         _t(60, 100, "速い", 10, GRAY, "end"), _t(60, 290, "遅い", 10, GRAY, "end")]
    for name, x, y, t, color in [("貪欲法", 160, 100, "12都市: 0.00001秒（答え 80.5）", AMBER),
                                 ("bitDP", 520, 150, "12都市: 0.009秒（答え 73.1）", GREEN),
                                 ("全探索", 520, 260, "12都市: 8.25秒（答え 73.1）", BLUE)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{color}"/>')
        s.append(_t(x + 14, y + 4, name, 12, INK, "start", 700))
        s.append(_t(x + 14, y + 20, t, 10, "#444", "start"))
    s.append(_t(340, 200, "同じ「必ず最適」でも bitDP は全探索の 900倍 速い", 10.5, RED, "middle", 700))
    s.append(_t(340, 216, "貪欲法は最速だが答えは 10% 長い", 10.5, RED, "middle", 700))
    return _slide("11", "アルゴリズムの使い分け", "\n".join(s),
                  ["自分の都市数（12）の実測: 全探索 8.25秒・bitDP 0.009秒・貪欲法 0.00001秒。地図の位置と矛盾しない。"])


def ex12():
    rounds = [("はじめ", 1, 100, None, 100), ("1回目", 51, 100, 50, 50), ("2回目", 51, 74, 75, 24), ("3回目", 63, 74, 62, 12), ("4回目", 69, 74, 68, 6)]
    s = [_t(320, 78, "秘密の数 73 を「中央を聞く」作戦で当てる", 11.5, INK, "middle", 700)]
    def X(v):
        return 90 + (v - 1) * 5
    for i, (label, lo, hi, asked, count) in enumerate(rounds):
        y = 100 + i * 38
        s.append(_t(84, y + 14, label, 10.5, INK, "end", 700))
        s.append(_box(X(1), y, 500, 20, "#EEE", "#CCC", 1, 3))
        s.append(_box(X(lo), y, X(hi) - X(lo) + 5, 20, "#E8F5D8", GREEN, 1.5, 3))
        s.append(_t(X(lo) + 2, y - 3, str(lo), 9, GREEN, "start"))
        s.append(_t(X(hi) + 5, y - 3, str(hi), 9, GREEN, "end"))
        s.append(f'<line x1="{X(73) + 2}" y1="{y - 2}" x2="{X(73) + 2}" y2="{y + 22}" stroke="{RED}" stroke-width="2"/>')
        if asked:
            s.append(f'<circle cx="{X(asked) + 2}" cy="{y + 10}" r="5" fill="{AMBER}"/>')
            s.append(_t(84, y + 28, f"聞いた {asked}", 9, AMBER, "end"))
        s.append(_t(606, y + 14, f"{count}個", 10.5, GREEN, "start", 700))
    s.append(_t(320, 300, "候補は 100 → 50 → 24 → 12 → 6 と半分ずつ減る（赤い線 = 73）", 11, INK))
    return _slide("12", "候補が半分に減る", "\n".join(s),
                  ["自分の数 73 では、聞いた数が 50・75・62・68 で、残りの候補は 50・24・12・6 個。実行結果の作戦Bの列と一致した。"])


def ex13():
    boxes = [("s", "開始"), ("p", "迷路とプレイヤーの道を読む"), ("p", "道を座標の列に直す"), ("j", "道はゴールに着く？"),
             ("a", "ダイクストラ法で最短の秒数を求める"), ("p", "プレイヤーの秒数と比べてスコアを出す"), ("p", "2つの道とスコアを表示する"), ("s", "終了")]
    cx = 200; s = []
    for i, (kind, label) in enumerate(boxes):
        y = 66 + i * 33
        if kind == "s":
            s.append(_box(cx - 40, y, 80, 22, "#E8F5D8", GREEN, 1.5, 11))
        elif kind == "j":
            s.append(f'<polygon points="{cx},{y - 4} {cx + 110},{y + 11} {cx},{y + 26} {cx - 110},{y + 11}" fill="#FFF3D6" stroke="{AMBER}" stroke-width="1.5"/>')
        else:
            s.append(_box(cx - 100, y, 200, 22, "#FFF3D6" if kind == "a" else "#FFFFFF", AMBER if kind == "a" else "#888", 2 if kind == "a" else 1, 0))
        s.append(_t(cx, y + 15, label, 10, AMBER if kind in "aj" else INK, "middle", 700 if kind == "a" else None))
        if i < len(boxes) - 1:
            s.append(_arrow(cx, y + (26 if kind == "j" else 22), cx, y + 33 - (4 if boxes[i + 1][0] == "j" else 0), GRAY, 1.5))
    jy = 66 + 3 * 33
    s.append(_t(cx + 6, jy + 38, "はい", 9, GREEN, "start"))
    s.append(_t(cx + 114, jy + 6, "いいえ", 9, RED, "start"))
    s.append(_arrow(cx + 110, jy + 11, cx + 160, jy + 11, GRAY, 1.5))
    s.append(_box(cx + 160, jy, 70, 22, "#FFFFFF", "#888", 1, 0)); s.append(_t(cx + 195, jy + 15, "「着かない」", 9))
    ey = 66 + 7 * 33 + 11
    s.append(f'<path d="M {cx + 195} {jy + 22} L {cx + 195} {ey} L {cx + 46} {ey}" fill="none" stroke="{GRAY}" stroke-width="1.5"/>')
    s.append(_box(455, 80, 170, 130, LIGHT, "#BBB"))
    s.append(_t(465, 100, "自分の入力", 11, INK, "start", 700))
    s.append(_t(465, 118, "cost_map: 5×5（9 が 6マス）", 10, INK, "start"))
    s.append(_t(465, 134, "player_moves:", 10, INK, "start"))
    s.append(_t(465, 148, "\"DDRRDDRRDDRRDR\"", 10, INK, "start"))
    s.append(_t(465, 172, "実行結果の出力", 11, INK, "start", 700))
    s.append(_t(465, 190, "プレイヤー 42秒 ／ 最短 18秒", 10, GREEN, "start"))
    s.append(_t(465, 204, "スコア 42点", 10, GREEN, "start"))
    s.append(_t(455, 240, "オレンジ = アルゴリズムが働く箱", 10, AMBER, "start"))
    s.append(_t(455, 256, "ひし形 = if で分かれるところ", 10, AMBER, "start"))
    return _slide("13", "プログラムのフローチャート", "\n".join(s),
                  ["テンプレートAの流れ。自分の道 DDRRDDRRDDRRDR ではゴールに着く（はい）ので、ダイクストラ法へ進み 42点と表示された。"])


def ex14():
    rows = [("\"\"（空）", "(0,0) 迷路の中", "受けつけない: ゴールに着いていません", False),
            ("\"DDDDDD\"（外へ）", "(6,0) 迷路の外 → エラー", "受けつけない: 迷路の外に出てしまいました", True),
            ("\"DR\"（届かない）", "(1,1) 迷路の中", "受けつけない: ゴールに着いていません", False),
            ("\"DDXR\"（使えない文字）", "(2,1) X を無視", "受けつけない: 「X」は使えない文字です", True)]
    s = [_t(320, 78, "自分で決めた4つの入力を、バグあり／直したあとの両方に入れる", 11.5, INK, "middle", 700)]
    heads = [("入力", 44, 150), ("バグあり", 194, 170), ("直したあと", 364, 250)]
    for label, x, w in heads:
        s.append(_box(x, 92, w, 24, LIGHT, "#BBB", 1, 0)); s.append(_t(x + w / 2, 108, label, 11, INK, "middle", 700))
    for i, (inp, buggy, fixed, bad) in enumerate(rows):
        y = 116 + i * 40
        s.append(_box(44, y, 150, 40, "#FFFFFF", "#DDD", 1, 0)); s.append(_t(50, y + 24, inp, 10, INK, "start"))
        s.append(_box(194, y, 170, 40, "#FDE0DC" if bad else "#FFFFFF", RED if bad else "#DDD", 1.5 if bad else 1, 0))
        s.append(_t(200, y + 24, buggy, 10, RED if bad else INK, "start", 700 if bad else None))
        s.append(_box(364, y, 250, 40, "#E8F5D8", GREEN, 1, 0)); s.append(_t(370, y + 24, fixed, 9.5, GREEN, "start"))
    s.append(_t(44, 296, "赤 = バグあり版で変な動きになったもの（原因: 迷路の外を指しても止めない／知らない文字を無視する）", 9.5, RED, "start"))
    return _slide("14", "テスト入力と結果", "\n".join(s),
                  ["自分の4つの入力のうち、外へ出る道と使えない文字の道で、バグあり版は変な動きをした。直したあとは4つとも理由を返した。"])


def ex15():
    s = [_t(120, 80, "前期「探す」", 12, GRAY, "middle", 700), _t(440, 80, "後期「いちばん良いものを選ぶ」", 12, GREEN, "middle", 700)]
    left = [("線形探索", 110), ("二分探索", 160), ("幅優先探索", 210), ("全探索", 260)]
    for name, y in left:
        s.append(_box(60, y - 14, 120, 26, LIGHT, "#999")); s.append(_t(120, y + 4, name, 11))
    s.append(_box(260, 96, 170, 190, "#E8F5D8", GREEN, 1.5)); s.append(_t(345, 114, "必ず最適", 11, GREEN, "middle", 700))
    s.append(_box(450, 96, 170, 190, "#FFF3D6", AMBER, 1.5)); s.append(_t(535, 114, "速い（近似解）", 11, AMBER, "middle", 700))
    opt = [("幅優先探索（重みなし）", 140), ("ダイクストラ法", 180), ("全探索", 220), ("bitDP  91.1 / 6.2秒", 260)]
    fast = [("貪欲法  105.7 / 0.000秒", 140), ("全出発点  95.0 / 0.000秒", 180), ("焼きなまし法  95.2 / 0.01秒", 220), ("遺伝的  96.3 / 0.69秒", 260)]
    for name, y in opt:
        s.append(_box(270, y - 13, 150, 24, "#FFFFFF", "#AAA")); s.append(_t(345, y + 4, name, 9.5))
    for name, y in fast:
        s.append(_box(460, y - 13, 150, 24, "#FFFFFF", "#AAA")); s.append(_t(535, y + 4, name, 9.5))
    s.append(_arrow(180, 210, 270, 180, GRAY, 1.5)); s.append(_arrow(180, 210, 270, 140, GRAY, 1.5))
    s.append(_arrow(180, 260, 270, 220, GRAY, 1.5)); s.append(_arrow(180, 260, 270, 260, GRAY, 1.5))
    s.append(_arrow(180, 160, 460, 140, GRAY, 1.5))
    s.append(_t(60, 300, "二分探索の「中央を聞く」は貪欲法の考え方", 9.5, GRAY, "start"))
    s.append(_t(610, 300, "箱の中の数値 = 20都市の実行結果（答え / 時間）", 9.5, GRAY, "end"))
    return _slide("15", "前期と後期のつながり", "\n".join(s),
                  ["自分の種（学籍番号）では bitDP 91.1 が最適、焼きなまし法 95.2・遺伝的 96.3 が近似解だった。",
                   "前期の探索が後期の各手法につながっている。"])


EXAMPLES = {"01": ex01, "02": ex02, "03": ex03, "04": ex04, "05": ex05, "06": ex06, "07": ex07, "08": ex08,
            "09": ex09, "10": ex10, "11": ex11, "12": ex12, "13": ex13, "14": ex14, "15": ex15}


def slide_example(week):
    """解答セクションに入れる (見出し, 本文HTML)。"""
    body = f"""        <p>自分の数値に書き換える前の、例題の数値で描いた例です。
        図形（四角・丸・矢印・テキストボックス）だけで描いてあり、図の中に数値が入っています。
        文章は下の1〜2行だけです。自分の数値で同じように描けば、課題要件を満たします。</p>
{EXAMPLES[week]()}"""
    return ("標準課題のスライドの例（あくまで例）", body)
