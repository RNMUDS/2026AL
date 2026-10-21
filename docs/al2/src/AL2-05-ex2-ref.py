# ダイクストラ法（2）: 最短時間だけでなく「どの道を通ったか」も記録して、道順を組み立てる
# 時間を書き直すときに「どこから来たか（came_from）」も一緒に書き直しておくと、あとで道順を組み立てられる。

# 例題1と同じ重み付きグラフ（数字は乗車時間・分）
railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
goal = "東京"
INF = float("inf")      # inf は無限大。「まだ行き方が1つも見つかっていない」印に使う


def dijkstra(start):
    """start から各駅までの最短時間 distance と、来た駅の記録 came_from を求める（例題1と同じ手順）。
    地図は、上で作った railway を使う。"""
    distance = {}
    came_from = {}                  # 鍵 = 駅、値 = その駅へいちばん早く来るときの、1つ前の駅
    for station in railway:
        distance[station] = INF
        came_from[station] = None   # None は「まだ分からない」（出発点は最後まで None のまま）
    distance[start] = 0
    settled = set()
    log = [(None, dict(distance), set(settled), dict(came_from))]   # 手順ごとの記録（窓の表示に使う）
    while len(settled) < len(railway):
        current = None
        for station in railway:
            if station in settled or distance[station] == INF:
                continue
            if current is None or distance[station] < distance[current]:
                current = station
        if current is None:
            break
        settled.add(current)
        for name, minutes in railway[current]:     # name = となりの駅
            if name in settled:
                continue
            new_distance = distance[current] + minutes
            if new_distance < distance[name]:
                distance[name] = new_distance
                came_from[name] = current       # 時間を書き直すときに、「current から来た」も書き直す
        log.append((current, dict(distance), set(settled), dict(came_from)))
    return distance, came_from, log


def build_route(goal, came_from):
    """ゴールから came_from を逆にたどって、道順（駅の並び）を作る。"""
    route = []
    node = goal
    while node is not None:         # 出発点の came_from は None なので、そこで止まる
        route.append(node)
        node = came_from[node]      # 1つ前の駅へもどる
    route.reverse()                 # ゴール → 出発点 の順を、出発点 → ゴール の順にひっくり返す
    return route


distance, came_from, log = dijkstra(start)

print(f"{start}から各駅への最短時間と道順")
print("-" * 52)
for station in railway:
    if station != start:
        # :>2 は数を2けたの幅で右にそろえる。" → ".join(リスト) はリストの中身を「 → 」でつないだ文字にする
        print(f"  {station}: {distance[station]:>2}分  " + " → ".join(build_route(station, came_from)))
print("-" * 52)
print("came_from の中身（その駅へいちばん早く来るときの、1つ前の駅）")
for station in railway:
    if came_from[station] is None:
        print(f"  {station}: None（出発点）")
    else:
        print(f"  {station}: {came_from[station]}")
print()
route = build_route(goal, came_from)
print(f"{goal}から逆にたどる: " + " ← ".join(reversed(route)))   # reversed(route) は route を後ろから読む
print("ひっくり返すと道順: " + " → ".join(route) + f"（{distance[goal]}分）")


# ============================================================
# ここから下は、重み付きグラフと道順を pygame の窓に絵で表示するための道具です。
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


def _wrap(font, text, width):
    """「 → 」の区切りで、width ピクセルに収まるように何行かに分ける。"""
    out, line = [], ""
    for part in text.split(" → "):
        cand = part if not line else line + " → " + part
        if line and font.size(cand)[0] > width:
            out.append(line + " →")
            line = part
        else:
            line = cand
    return out + [line]


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


def show_window(graph, legs, title, closed=(), where=None):
    """ダイクストラ法で came_from が書かれていくようすと、ゴールから逆にたどって道順を組み立てるようすを表示する。
    legs = [(出発, ゴール, 手順の記録, 道順), ...]。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names, edges = _graph_parts(graph)
    pos = _placed(names, edges, where) if where else _layout(names, edges)
    colors = [GREEN, AMBER, BLUE, (255, 120, 200), (180, 140, 255)]
    frames = [("start", 0, 0)]
    for li, (_, _, log, route) in enumerate(legs):
        frames += [("search", li, j) for j in range(1, len(log))]
        frames += [("back", li, i) for i in range(1, len(route) + 1)]
    frames.append(("end", 0, 0))
    problems = _problems(graph, names, {n: 0 for n in names})
    row_h = max(22, min(36, (HEIGHT - 300) // max(len(names), 1)))
    x0 = 560

    def table(dist, came, settled, current, changed):
        font = mid if row_h >= 30 else small
        screen.blit(small.render("場所", True, SUB), (x0 + 10, 90))
        screen.blit(small.render("時間", True, SUB), (x0 + 190, 90))
        screen.blit(small.render("came_from（1つ前の場所）", True, SUB), (x0 + 270, 90))
        for i, name in enumerate(names):
            y = 114 + i * row_h
            box = pygame.Rect(x0, y, 460, row_h - 4)
            pygame.draw.rect(screen, (26, 44, 10) if name in settled else (30, 30, 38), box, border_radius=6)
            if name == current:
                pygame.draw.rect(screen, WHITE, box, width=3, border_radius=6)
            ty = y + (row_h - 4 - font.get_height()) // 2
            hot = AMBER if name in changed else None
            screen.blit(font.render(_fit(font, name, 170), True, TEXT), (x0 + 10, ty))
            screen.blit(font.render(_minutes(dist.get(name, INF)), True, hot or (GREEN if name in settled else TEXT)), (x0 + 190, ty))
            screen.blit(font.render(_fit(font, str(came.get(name) or "－"), 180), True, hot or TEXT), (x0 + 270, ty))

    def info(lines):
        by = 114 + len(names) * row_h + 16
        room = max(1, (HEIGHT - 40 - by) // 28)
        if len(lines) > room:
            lines = lines[:room - 1] + [(f"ほか {len(lines) - room + 1} 件", SUB)]
        for i, (text, color) in enumerate(lines):
            screen.blit(mid.render(_fit(mid, text, 480), True, color), (x0, by + i * 28))

    def draw(k):
        kind, li, j = frames[k]
        colored, rings, labels, lines = [], {}, None, []
        head, sub = "道順を組み立てる", ""
        if kind == "start" and not legs:
            lines = [("行ける区間が1つもない（ターミナルの説明を見る）", RED)]
            table({}, {}, set(), None, set())
        elif kind == "start":
            here, there = legs[0][0], legs[0][1]
            rings = {here: WHITE, there: AMBER}
            sub = "区間: " + "、".join(f"{a}→{b}" for a, b, _, _ in legs)
            lines = [(f"まず {here} から {there} への道をさがす", TEXT), ("スペースで開始／→で1手順", SUB)]
            table({}, {}, set(), None, set())
        elif kind == "search":
            here, there, log, route = legs[li]
            current, dist, settled, came = log[j]
            before = log[j - 1][3]
            changed = {n for n in names if came.get(n) != before.get(n)}
            tree = [(came[n], n) for n in came if came[n] is not None]
            colored = [(tree, GREEN, 5)]
            rings = {n: AMBER for n in names if dist.get(n, INF) != INF}
            rings.update({n: GREEN for n in settled})
            rings[current] = WHITE
            labels = {n: (_minutes(dist.get(n, INF)), GREEN if n in settled else (AMBER if dist.get(n, INF) != INF else SUB))
                      for n in names}
            head = f"区間{li + 1}: {here} → {there}"
            sub = "緑の線 = came_from（その場所へ、いちばん早く来た道）"
            table(dist, came, settled, current, changed)
            lines = [(f"{current}（{dist[current]}分）を確定", TEXT)]
            for n in names:
                if n in changed:
                    old = before.get(n)
                    lines.append((f"came_from[{n}] = {current}" + (f"（{old} から書き直し）" if old else ""),
                                  AMBER if old else TEXT))
            if len(lines) == 1:
                lines.append(("came_from の書き直しなし", SUB))
        elif kind == "back":
            here, there, log, route = legs[li]
            _, dist, settled, came = log[-1]
            part = route[-j:]
            colored = [([(came[n], n) for n in came if came[n] is not None], (60, 90, 30), 4),
                       (list(zip(part, part[1:])), colors[li % len(colors)], 9)]
            rings = {n: colors[li % len(colors)] for n in part}
            rings[part[0]] = WHITE
            head = f"区間{li + 1}: {there} から逆にたどる"
            sub = "came_from を1つずつ読んで、1つ前の場所へもどる"
            table(dist, came, settled, part[0], set())
            for n in reversed(part):
                lines.append((f"came_from[{n}] = {came[n] or 'None（出発点に着いた）'}", TEXT))
            if j == len(route):
                lines.append(("ひっくり返す: " + " → ".join(route) + f"（{dist[there]}分）", colors[li % len(colors)]))
        else:
            total = 0
            for i, (here, there, log, route) in enumerate(legs):
                colored.append((list(zip(route, route[1:])), colors[i % len(colors)], max(4, 12 - 3 * i)))
                rings.update({n: colors[i % len(colors)] for n in route if n not in rings})
                minutes = log[-1][1][there]
                total += minutes
                lines.append((f"{i + 1}. {here} → {there}（{minutes}分）", colors[i % len(colors)]))
                lines += [("    " + t, SUB) for t in _wrap(small, " → ".join(route), 400)]
            head = "できあがった道順"
            sub = "区間ごとに色を変えて描いた道順（区間1がいちばん太い）"
            screen.blit(big.render(f"合計 {total}分", True, GREEN), (x0, 90))
            lines = lines + [(p, RED) for p in problems]
            y = 134
            for text, color in lines:
                font = small if color == SUB else mid
                if y < HEIGHT - 50:
                    screen.blit(font.render(_fit(font, text, 480), True, color), (x0, y))
                y += 24 if color == SUB else 30
            lines = []
        screen.blit(big.render(_fit(big, title, 500), True, GREEN), (30, 20))
        if labels:
            screen.blit(small.render("丸の外の数字 = 出発点からの時間", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, colored, rings, labels, closed)
        screen.blit(big.render(_fit(big, head, 480), True, GREEN), (x0, 20))
        screen.blit(small.render(_fit(small, sub, 480), True, SUB), (x0, 52))
        if lines:
            info(lines)

    _loop(screen, fonts, len(frames) - 1, draw)


# --- 窓を開いて、came_from が書かれていくようすと、ゴールから逆にたどるようすをアニメーション表示する ---
show_window(railway, [(start, goal, log, route)], "ダイクストラ法で道順を組み立てる")
