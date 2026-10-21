# 第5回 クリエイティブ演習1: 自分だけのディズニーランドの地図を作る
# ダイクストラ法で、エントランスから園内の各場所まで「いちばん早く着く時間」を求める。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: 好きなアトラクションやお店を場所として2つ以上足し、時間も自分の感覚で決める
#   Lv2: 「まっすぐ行くより、寄り道したほうが早い」しかけを作る（ひな形の書き直しは2回。自分の地図でも2回以上に）
#   Lv3: closed に道を入れて通行止めにし、どの場所の時間が変わるかを窓で確かめる

# ★ 窓のいちばん上に出る題名
TITLE = "わたしのディズニー地図"

# ★ 園内の地図（重み付きグラフ）。（となりの場所, 歩いてかかる時間（分））の組で並べる
#   東京ディズニーリゾート公式ブログ「開園当時のマップをご紹介」（2019年）の、今のマップをもとにした
#   （テーマランドどうしのつながり方は地図のとおり。時間は歩く時間の目安なので、自分の感覚で変えてよい）
#   ワールドバザールの横の通路（アーケード）は人が多いので、プラザを通るより時間がかかることにしている
#   1本の道は、両方の場所の行に、同じ時間で書く（第4回の路線図と同じ）
#   場所を足すときは、その場所の行を足し、つなぐ相手の行にも足した場所を書く
park = {
    "エントランス": [("ワールドバザール", 3)],
    "ワールドバザール": [("エントランス", 3), ("プラザ", 3), ("アドベンチャーランド", 7), ("トゥモローランド", 7)],
    "プラザ": [("ワールドバザール", 3), ("アドベンチャーランド", 3), ("トゥモローランド", 3), ("シンデレラ城", 1)],
    "シンデレラ城": [("プラザ", 1), ("ファンタジーランド", 2)],
    "アドベンチャーランド": [("ワールドバザール", 7), ("プラザ", 3), ("ウエスタンランド", 3)],
    "ウエスタンランド": [("アドベンチャーランド", 3), ("クリッターカントリー", 4), ("ファンタジーランド", 5)],
    "クリッターカントリー": [("ウエスタンランド", 4)],
    "ファンタジーランド": [("シンデレラ城", 2), ("ウエスタンランド", 5), ("トゥーンタウン", 4), ("トゥモローランド", 6)],
    "トゥーンタウン": [("ファンタジーランド", 4), ("トゥモローランド", 5)],
    "トゥモローランド": [("ワールドバザール", 7), ("プラザ", 3), ("ファンタジーランド", 6), ("トゥーンタウン", 5)],
}

# ★ 窓に描くときの位置（横, 縦）。0〜100 の数で、左上が (0, 0)、右下が (100, 100)
#   公式ブログのマップを見て決めた。場所を足したときは、ここにも足すと地図の上のその位置に描かれる
#   （書かなかった場所は、つながっている場所の近くに自動で置かれる）
where = {
    "エントランス": (62, 100),
    "ワールドバザール": (62, 76),
    "プラザ": (62, 52),
    "シンデレラ城": (62, 26),
    "ファンタジーランド": (64, 0),
    "トゥーンタウン": (95, 0),
    "トゥモローランド": (92, 52),
    "アドベンチャーランド": (32, 60),
    "ウエスタンランド": (28, 28),
    "クリッターカントリー": (4, 0),
}

# ★ 出発する場所（park に書いた場所の名前）
start = "エントランス"

# ★ パレードなどで通れない道。("場所", "場所") の組をカンマで区切って書く。最初は空っぽ
#   例: closed = [("プラザ", "シンデレラ城")]   ← お城の前をパレードが通っている
#   いちばん早い道の上にある道を通行止めにすると、時間が変わる
closed = []


# ------------------------------------------------------------
# ここから下は、例題1（参考）と同じダイクストラ法。読みながら、窓のアニメーションと見比べよう
#   参考の railway が park（graph）、station が place に変わっている。
#   参考より増えているのは、書きまちがいの検査と、通行止めの道を外した地図 graph を作る部分
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
#   raise SystemExit("…") は、「…」を表示してプログラムを終わらせる命令
#   park の各行の左側（辞書の「鍵」）が場所の名前。となりに書いた場所にも、その場所の行が要る
for place in park:
    for road in park[place]:
        if type(road) != tuple or len(road) != 2:
            raise SystemExit(f"{place} の行の {road} がおかしい。(\"場所\", 3) のように ( ) で囲んで書こう")
        name, minutes = road        # name = となりの場所、minutes = そこまで歩く時間
        if type(minutes) != int:
            raise SystemExit(f"{place} の行の {road} の時間がおかしい。時間は \" \" で囲まず、3 のような数で書こう")
        if minutes < 0:
            raise SystemExit(f"{place} の行の {road} の時間がマイナス。時間は 0 以上の数で書こう（ダイクストラ法は、時間が 0 以上の地図でしか正しく動かないため）")
        if name not in park:
            raise SystemExit(f"park に「{name}」の行がない（{place} の行に書いてある）。行を足すか、名前を直そう")
        if (place, minutes) not in park[name]:
            raise SystemExit(f"{place} の行に（{name}, {minutes}）があるのに、{name} の行に（{place}, {minutes}）がない。"
                             "1本の道は、両方の行に同じ時間で書こう")
for place in where:
    if place not in park:
        raise SystemExit(f"where の「{place}」が park にない。park と同じ名前にするか、where から消そう")
    if type(where[place]) != tuple or len(where[place]) != 2:
        raise SystemExit(f"where の「{place}」の位置は、(62, 50) のように (横, 縦) の2つの数で書こう")
if start not in park:
    raise SystemExit(f"start の「{start}」が park にない。名前を park と同じにしよう")
if type(closed) != list:
    raise SystemExit("closed は [ ] で囲もう。例: closed = [(\"プラザ\", \"シンデレラ城\")]")
for road in closed:
    if type(road) != tuple or len(road) != 2 or road[0] not in park or road[1] not in park:
        raise SystemExit(f"closed の {road} がおかしい。[ ] の中に (\"場所\", \"場所\") の組を並べ、名前は park と同じにしよう")
    joined = False
    for name, minutes in park[road[0]]:
        if name == road[1]:
            joined = True
    if not joined:
        raise SystemExit(f"closed の {road[0]} と {road[1]} の間には、もともと道がない。park で道を確かめよう")

# 通行止めの道を外した地図 graph を、新しく作る（park はそのまま残す）
graph = {}
for place in park:
    graph[place] = []
    for name, minutes in park[place]:
        if (place, name) in closed or (name, place) in closed:
            continue                # 通れない道は入れない
        graph[place].append((name, minutes))

INF = float("inf")      # inf は無限大。「まだ行き方が1つも見つかっていない」印に使う

# distance = 距離表。出発点からその場所までの、今わかっているいちばん短い時間
distance = {}
for place in graph:
    distance[place] = INF
distance[start] = 0     # 出発点だけは 0分

# settled = 「もう変わらない」と決まった（確定した）場所を入れる集合
settled = set()
# 手順ごとの記録（窓の表示に使う）。dict( ) と set( ) でその時の中身を写して残す
#   （写さずに distance をそのまま入れると、あとで書き直したときに記録まで変わってしまう）
log = [(None, dict(distance), set(settled), [])]

print(f"ダイクストラ法で、{start}から園内の各場所までの最短時間を求める")
for a, b in closed:
    print(f"通行止め: {a} — {b}")
print("-" * 56)
step = 0                # 手順の番号（①②③を1回やるごとに1つ増える）
while len(settled) < len(graph):
    step = step + 1

    # ① まだ確定していない場所のうち、時間がいちばん小さい場所を選ぶ
    current = None
    for place in graph:
        if place in settled or distance[place] == INF:
            continue
        if current is None or distance[place] < distance[current]:
            current = place
    if current is None:
        break                   # 残りの場所には、どこからも行けない

    # ② 選んだ場所を確定する（この場所の時間は、もう変わらない）
    settled.add(current)
    print(f"手順{step}  {current}（{distance[current]}分）を確定")

    # ③ となりの場所について、current を通るほうが短ければ書き直す
    changes = []
    for name, minutes in graph[current]:        # name = となりの場所、minutes = そこまで歩く時間
        if name in settled:
            continue
        new_distance = distance[current] + minutes
        if new_distance < distance[name]:
            old = distance[name]
            distance[name] = new_distance
            changes.append((name, old, new_distance, minutes))
            if old == INF:
                print(f"        {name} に {new_distance}分 を書き込んだ（{current} {distance[current]} + {minutes}）")
            else:
                print(f"        {name} を {old}分 → {new_distance}分 に書き直した（{current} {distance[current]} + {minutes}）")
    log.append((current, dict(distance), set(settled), changes))

print("-" * 56)
print(f"{start}から園内の各場所までの最短時間")
for place in graph:
    if distance[place] == INF:
        print(f"  {place}: 行けない（道がつながっていないか、通行止めで切れている）")
    else:
        print(f"  {place}: {distance[place]}分")


# ============================================================
# ここから下は、重み付きグラフと距離表を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import math
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

WIDTH, HEIGHT = 1060, 620       # 窓の大きさ（ピクセル）
STEP_MS = 1100                  # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
LINE = (80, 84, 100)
NODE = (38, 40, 52)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
GREEN = (118, 185, 0)
AMBER = (255, 184, 0)
BLUE = (90, 170, 255)
RED = (255, 110, 110)
WHITE = (255, 255, 255)
# 日本語が出せるフォントの場所（Mac → Windows の順にさがす）
FONT_FILES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
]
FONT_NAMES = "hiraginosans,yugothic,meiryo,msgothic,notosanscjkjp,notosansjp"


def _font(size, bold=False):
    for path in FONT_FILES:
        if os.path.exists(path):
            return pygame.font.Font(path, size)
    return pygame.font.SysFont(FONT_NAMES, size, bold=bold)


def _graph_parts(graph):
    """隣接リストから、丸にする場所の名前と、線（場所, 場所, 時間）の一覧を作る。"""
    names = list(graph)
    for a in graph:
        for b, _ in graph[a]:
            if b not in names:
                names.append(b)
    edges = []
    for a in graph:
        for b, w in graph[a]:
            if not any({a, b} == {x, y} for x, y, _ in edges):
                edges.append((a, b, w))
    return names, edges


def _weight(graph, a, b):
    """a から b への時間。直接つながっていなければ None。"""
    for name, w in graph.get(a, []):
        if name == b:
            return w
    return None


def _problems(graph, names, final_distance):
    """地図の書きまちがいを、赤い字で知らせる文の一覧にする。"""
    out = []
    for a in graph:
        for b, w in graph[a]:
            if w < 0:
                out.append(f"{a}—{b} がマイナス（{w}分）。正しく動かない")
            back = _weight(graph, b, a)
            if back is None:
                out.append(f"{b} の行に {a} がない（道は両方の行に書く）")
            elif back != w and names.index(a) < names.index(b):
                out.append(f"{a}—{b}: 行き{w}分・帰り{back}分（そろえる）")
    for name in names:
        if final_distance.get(name, INF) == INF:
            out.append(f"{name} へは行けない（道がつながっていない）")
    return out


def _crossings(order, edges):
    """円の上に order の順で頂点を並べたとき、線どうしが何回交わるかを数える。"""
    at = {name: i for i, name in enumerate(order)}
    count = 0
    for i, (a, b, _) in enumerate(edges):
        lo, hi = sorted((at[a], at[b]))
        for c, d, _ in edges[i + 1:]:
            if len({a, b, c, d}) < 4:
                continue
            inside = (lo < at[c] < hi) + (lo < at[d] < hi)
            count += inside == 1
    return count


def _segments_cross(p1, p2, p3, p4):
    """線分 p1-p2 と p3-p4 が交わるか。"""
    def side(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (side(p1, p2, p3) * side(p1, p2, p4) < 0) and (side(p3, p4, p1) * side(p3, p4, p2) < 0)


def _spring(names, edges, seed):
    """線をばね、丸どうしを反発する磁石とみなして、少しずつ動かして並べる。"""
    import random
    rng = random.Random(seed)
    p = {n: [rng.random(), rng.random()] for n in names}
    k = 1.6 / math.sqrt(len(names))
    for it in range(300):
        move = {n: [0.0, 0.0] for n in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                dx, dy = p[a][0] - p[b][0], p[a][1] - p[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = k * k / d
                move[a][0] += dx / d * f
                move[a][1] += dy / d * f
                move[b][0] -= dx / d * f
                move[b][1] -= dy / d * f
        for a, b, _ in edges:
            dx, dy = p[a][0] - p[b][0], p[a][1] - p[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = d * d / k
            move[a][0] -= dx / d * f
            move[a][1] -= dy / d * f
            move[b][0] += dx / d * f
            move[b][1] += dy / d * f
        heat = 0.1 * (1 - it / 300)
        for n in names:
            d = math.hypot(*move[n]) or 0.01
            p[n][0] += move[n][0] / d * min(d, heat)
            p[n][1] += move[n][1] / d * min(d, heat)
    return p


def _placed(names, edges, where, cx=265, cy=326, radius=196):
    """where = {場所: (横, 縦)}（0〜100）で決めた位置に置く。where にない場所は、つながっている場所の近くに置く。"""
    r = _node_radius(names)
    left, right = 30 + r, 530 - r
    top, bottom = 100 + r * 0.4, HEIGHT - 52 - r
    pos = {n: [left + (right - left) * where[n][0] / 100, top + (bottom - top) * where[n][1] / 100]
           for n in names if n in where}
    fixed = set(pos)
    for _ in range(len(names)):
        for i, n in enumerate(names):
            if n in pos:
                continue
            near = [pos[b if a == n else a] for a, b, _ in edges if n in (a, b) and (b if a == n else a) in pos]
            if near or not pos:
                bx = sum(p[0] for p in near) / len(near) if near else cx
                by = sum(p[1] for p in near) / len(near) if near else cy
                best = None                 # まわり16方向のうち、ほかの丸からいちばん離れた所を選ぶ
                for k in range(16):
                    for dist in (2.6 * r, 3.6 * r):
                        c = (min(max(bx + math.cos(k * math.pi / 8) * dist, left), right),
                             min(max(by + math.sin(k * math.pi / 8) * dist, top), bottom))
                        room = min((math.hypot(c[0] - q[0], c[1] - q[1]) for q in pos.values()), default=9999)
                        if best is None or room > best[0] + 0.5:
                            best = (room, c)
                pos[n] = list(best[1])
    for i, n in enumerate(names):                   # どこともつながっていない場所は、左下に並べる
        if n not in pos:
            pos[n] = [left + i * 2.2 * r % (right - left), bottom]
    gap = 2 * r + 30
    for _ in range(200):
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                if d < gap:
                    for n, sign in ((a, 1), (b, -1)):
                        if n not in fixed:
                            share = 1 if (a in fixed or b in fixed) else 0.5
                            pos[n][0] += sign * dx / d * (gap - d) * share
                            pos[n][1] += sign * dy / d * (gap - d) * share
        for n in names:
            pos[n][0] = min(max(pos[n][0], left), right)
            pos[n][1] = min(max(pos[n][1], top), bottom)
    return {n: tuple(v) for n, v in pos.items()}


def _layout(names, edges, cx=265, cy=326, radius=196):
    """頂点の位置を決める。
    8個以下: 円の上に等間隔で並べ、線の交わりがいちばん少なくなる順番を全部試して選ぶ。
    9個以上: ばねのしくみで並べ、線の交わりがいちばん少ないものを選ぶ。"""
    order = list(names)
    n = len(order)
    if n <= 8:
        if n > 3:
            from itertools import permutations
            best = None
            for rest in permutations(order[1:]):
                cand = [order[0], *rest]
                k = _crossings(cand, edges)
                if best is None or k < best[0]:
                    best = (k, cand)
            order = best[1]
        return {name: (cx + radius * math.sin(2 * math.pi * i / n), cy - radius * math.cos(2 * math.pi * i / n))
                for i, name in enumerate(order)}
    best = None
    for seed in range(12):
        p = _spring(order, edges, seed)
        k = sum(_segments_cross(p[a], p[b], p[c], p[d])
                for i, (a, b, _) in enumerate(edges) for c, d, _ in edges[i + 1:] if len({a, b, c, d}) == 4)
        if best is None or k < best[0]:
            best = (k, p)
    p = best[1]
    xs, ys = [v[0] for v in p.values()], [v[1] for v in p.values()]
    w, h = (max(xs) - min(xs)) or 1, (max(ys) - min(ys)) or 1
    pos = {name: [cx - radius * 1.12 + (p[name][0] - min(xs)) / w * radius * 2.24,
                  cy - radius + (p[name][1] - min(ys)) / h * radius * 2] for name in order}
    gap = 2 * _node_radius(order) + 46          # 丸どうしが近すぎるときは押し広げる
    for _ in range(200):
        for i, a in enumerate(order):
            for b in order[i + 1:]:
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                if d < gap:
                    push = (gap - d) / 2
                    pos[a][0] += dx / d * push
                    pos[a][1] += dy / d * push
                    pos[b][0] -= dx / d * push
                    pos[b][1] -= dy / d * push
        for name in order:
            pos[name][0] = min(max(pos[name][0], cx - radius * 1.12), cx + radius * 1.12)
            pos[name][1] = min(max(pos[name][1], cy - radius), cy + radius)
    return {name: tuple(v) for name, v in pos.items()}


def _node_radius(names):
    return 38 if len(names) <= 10 else (34 if len(names) <= 12 else 28)


def _draw_graph(screen, fonts, names, edges, pos, colored=(), rings=None, labels=None, closed=()):
    """丸（頂点）と線（辺）と、線のまん中の重み（時間）を描く。
    colored = [(場所の組の一覧, 色, 太さ), ...]。rings = {場所: 枠の色}。
    labels = {場所: (文字, 色)} は丸の外側に書く（距離表の値）。closed は通れない道（赤い点線）。"""
    big, mid, small = fonts
    r = _node_radius(names)
    edge_color = {}
    shut = {frozenset(p) for p in closed}
    for a, b, _ in edges:
        if frozenset((a, b)) in shut:
            _dashed(screen, RED, pos[a], pos[b])
        else:
            pygame.draw.line(screen, LINE, pos[a], pos[b], 2)
    for pairs, color, width in colored:
        for a, b in pairs:
            if a in pos and b in pos:
                pygame.draw.line(screen, color, pos[a], pos[b], width)
                edge_color[frozenset((a, b))] = color
    for a, b, w in edges:
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        key = frozenset((a, b))
        color = RED if key in shut else edge_color.get(key, TEXT)
        t = small.render("通行止め" if key in shut else f"{w}分", True, color)
        box = pygame.Rect(0, 0, t.get_width() + 12, t.get_height() + 4)
        box.center = (mx, my)
        pygame.draw.rect(screen, BG, box, border_radius=8)
        pygame.draw.rect(screen, color if key in edge_color or key in shut else LINE, box, width=1, border_radius=8)
        screen.blit(t, (box.x + 6, box.y + 2))
    spots = _label_spots(names, edges, pos, r) if labels else {}
    for name in names:
        x, y = pos[name]
        ring = (rings or {}).get(name, LINE)
        pygame.draw.circle(screen, NODE, (x, y), r)
        pygame.draw.circle(screen, ring, (x, y), r, 5 if ring != LINE else 3)
        _name_in_circle(screen, fonts, name, x, y, r)
        if labels and name in labels:
            text, color = labels[name]
            t = mid.render(text, True, color)
            box = pygame.Rect(0, 0, t.get_width() + 8, t.get_height())
            box.center = spots[name]
            pygame.draw.rect(screen, BG, box, border_radius=6)
            screen.blit(t, (box.x + 4, box.y))


def _near_segment(c, p, q):
    """点 c と線分 p-q のいちばん近いところまでの長さ。"""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = max(0, min(1, ((c[0] - p[0]) * dx + (c[1] - p[1]) * dy) / ((dx * dx + dy * dy) or 1)))
    return math.hypot(c[0] - p[0] - t * dx, c[1] - p[1] - t * dy)


def _label_spots(names, edges, pos, r):
    """丸の外に書く数字の位置を、丸の周り8方向から、線や他の丸とぶつからないところを選んで決める。"""
    spots = {}
    for name in names:
        x, y = pos[name]
        best = None
        for i in range(8):
            ang = math.pi / 2 + i * math.pi / 4          # 真下から順に試す
            c = (x + math.cos(ang) * (r + 24), y + math.sin(ang) * (r + 14))
            cost = i * 0.01
            if not (32 < c[0] < 525 and 78 < c[1] < HEIGHT - 44):
                cost += 100
            for other in names:
                if other != name:
                    cost += max(0, 2 * r + 10 - math.hypot(c[0] - pos[other][0], c[1] - pos[other][1]))
            for a, b, _ in edges:
                cost += max(0, 22 - _near_segment(c, pos[a], pos[b])) * 2
                mid = ((pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2)
                cost += max(0, 44 - math.hypot(c[0] - mid[0], c[1] - mid[1])) * 2
            for sx, sy in spots.values():
                cost += max(0, 50 - math.hypot(c[0] - sx, c[1] - sy)) * 2
            if best is None or cost < best[0]:
                best = (cost, c)
        spots[name] = best[1]
    return spots


def _split_at(name):
    """2行に分ける位置を決める。「ー」や小さい字で始まる行を作らず、「ー」の後ろや漢字の前で切ると読みやすい。"""
    def score(i):
        s = abs(i - len(name) / 2)
        if name[i - 1] in "ー・ ":
            s -= 1.5
        if ("\u4e00" <= name[i] <= "\u9fff") != ("\u4e00" <= name[i - 1] <= "\u9fff"):
            s -= len(name)
        return (s, -i)
    spots = [i for i in range(1, len(name)) if name[i] not in "ーァィゥェォッャュョヮンぁぃぅぇぉっゃゅょん、。）」"]
    return min(spots, key=score) if spots else (len(name) + 1) // 2


def _shrink(t, width):
    """t（文字の絵）が width より広ければ、width に収まるように縮める。"""
    if t.get_width() <= width:
        return t
    k = width / t.get_width()
    return pygame.transform.smoothscale(t, (int(t.get_width() * k), int(t.get_height() * k)))


def _name_in_circle(screen, fonts, name, x, y, r):
    """丸の中に名前を書く。長い名前は小さい文字にし、それでも長ければ2行に分ける。"""
    _, mid, small = fonts
    t = mid.render(name, True, TEXT)
    if t.get_width() > 2 * r - 6:
        t = small.render(name, True, TEXT)
    if t.get_width() > 2 * r - 6:
        half = _split_at(name)
        t1, t2 = small.render(name[:half], True, TEXT), small.render(name[half:].lstrip("・ "), True, TEXT)
        t1, t2 = _shrink(t1, 2 * r - 4), _shrink(t2, 2 * r - 4)     # それでも丸からはみ出す行は、文字を縮める
        screen.blit(t1, (x - t1.get_width() / 2, y - t1.get_height()))
        screen.blit(t2, (x - t2.get_width() / 2, y))
        return
    screen.blit(t, (x - t.get_width() / 2, y - t.get_height() / 2))


def _dashed(screen, color, p, q, dash=10):
    """p から q へ点線を引く。"""
    length = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
    for i in range(0, int(length), dash * 2):
        a, b = i / length, min(i + dash, length) / length
        pygame.draw.line(screen, color, (p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a),
                         (p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b), 3)


def _fit(font, text, width):
    """text が width ピクセルに収まらなければ、後ろを「…」にして縮める。"""
    if font.size(text)[0] <= width:
        return text
    while text and font.size(text + "…")[0] > width:
        text = text[:-1]
    return text + "…"


def _minutes(v):
    return "－" if v == INF else f"{v}分"


def _loop(screen, fonts, last_step, draw):
    """窓のくり返し処理。draw(k) が k 手順目の画面を描く。"""
    capture = os.environ.get("AL2_CAPTURE")      # 授業ページの画像を作るときだけ使う
    k = last_step if capture else 0
    playing = False
    clock = pygame.time.Clock()
    last = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE:
                    playing = not playing
                if event.key == pygame.K_RIGHT and k < last_step:
                    k += 1
                    playing = False
                if event.key == pygame.K_r:
                    k, playing = 0, False
        if playing and pygame.time.get_ticks() - last >= STEP_MS:
            last = pygame.time.get_ticks()
            if k < last_step:
                k += 1
            else:
                playing = False
        screen.fill(BG)
        draw(k)
        hint = fonts[2].render("スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる", True, SUB)
        screen.blit(hint, (30, HEIGHT - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)


def show_window(graph, start, log, title, closed=(), where=None):
    """ダイクストラ法で距離表が1手順ずつ埋まっていくようすを、グラフと表で表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names, edges = _graph_parts(graph)
    pos = _placed(names, edges, where) if where else _layout(names, edges)
    problems = _problems(graph, names, log[-1][1])
    rewrites = sum(1 for entry in log for _, old, _, _ in entry[3] if old != INF)
    last_step = len(log)                            # 最後の1つは「まとめ」の画面
    row_h = max(22, min(38, (HEIGHT - 300) // max(len(names), 1)))
    x0 = 560

    def table(dist, settled, current, changes):
        changed = {name: (old, new) for name, old, new, _ in changes}
        screen.blit(small.render("場所", True, SUB), (x0 + 10, 90))
        screen.blit(small.render("時間（距離表）", True, SUB), (x0 + 200, 90))
        font = mid if row_h >= 30 else small
        for i, name in enumerate(names):
            y = 114 + i * row_h
            box = pygame.Rect(x0, y, 460, row_h - 4)
            done = name in settled
            pygame.draw.rect(screen, (26, 44, 10) if done else (30, 30, 38), box, border_radius=6)
            if name == current:
                pygame.draw.rect(screen, WHITE, box, width=3, border_radius=6)
            ty = y + (row_h - 4 - font.get_height()) // 2
            screen.blit(font.render(_fit(font, name, 180), True, TEXT), (x0 + 10, ty))
            if name in changed:
                old, new = changed[name]
                text, color = f"{_minutes(old)} → {new}分", AMBER
            else:
                text, color = _minutes(dist.get(name, INF)), (GREEN if done else TEXT)
            screen.blit(font.render(text, True, color), (x0 + 200, ty))
            if done:
                t = font.render("確定", True, GREEN)
                screen.blit(t, (x0 + 450 - t.get_width(), ty))

    def draw(k):
        final = k == len(log)
        current, dist, settled, changes = log[min(k, len(log) - 1)]
        rings = {n: AMBER for n in names if dist.get(n, INF) != INF}
        rings.update({n: GREEN for n in settled})
        colored = []
        if current and not final:
            rings[current] = WHITE
            colored = [([(current, n) for n, *_ in changes], AMBER, 6)]
        labels = {n: (_minutes(dist.get(n, INF)), GREEN if n in settled else (AMBER if dist.get(n, INF) != INF else SUB))
                  for n in names}
        screen.blit(big.render(_fit(big, title, 500), True, GREEN), (30, 20))
        screen.blit(small.render(f"出発 {start}　丸の外の数字 = 距離表の時間", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, colored, rings, labels, closed)
        screen.blit(big.render("距離表", True, GREEN), (x0, 20))
        screen.blit(small.render("緑 = 確定した場所　橙 = この手順で書き込み・書き直した時間", True, SUB), (x0, 52))
        table(dist, settled, None if final else current, [] if final else changes)
        by = 114 + len(names) * row_h + 16
        lines = []
        if k == 0:
            lines = [(f"はじめ: {start} だけ 0分、ほかは「－」（inf）", TEXT), ("スペースで開始／→で1手順", SUB)]
        elif not final:
            lines = [(f"手順{k}  {current}（{dist[current]}分）を確定", TEXT)]
            for n, o, v, w in changes:
                verb = "書き直し" if o != INF else "書き込み"
                lines.append((f"{verb}: {n} {_minutes(o)} → {v}分（{dist[current]} + {w}）",
                              AMBER if o != INF else TEXT))
            if not changes:
                lines.append(("書き直しなし（となりは、表の時間が同じか短い）", SUB))
        else:
            lines = [(f"すべて確定。いちど書いた時間を書き直した回数: {rewrites}回", TEXT)]
            lines += [(p, RED) for p in problems]
        room = max(1, (HEIGHT - 40 - by) // 28)
        if len(lines) > room:
            lines = lines[:room - 1] + [(f"ほか {len(lines) - room + 1} 件", SUB)]
        for i, (text, color) in enumerate(lines):
            screen.blit(mid.render(_fit(mid, text, 480), True, color), (x0, by + i * 28))

    _loop(screen, fonts, last_step, draw)


# --- 窓を開いて、自分の地図で距離表が1手順ずつ埋まっていくようすをアニメーション表示する ---
# 白い枠 = いま確定した場所、橙の線 = その場所から時間を書き直した道、赤い点線 = 通行止め
show_window(park, start, log, TITLE, closed, where)
