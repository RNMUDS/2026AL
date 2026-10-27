# ダイクストラ法（2）: heapq で「時間がいちばん小さい駅」を取り出す
# 第5回の例題1と同じ路線図で、同じ答えが出ることを確かめる。
import heapq

# 第4回・第5回と同じ重み付きグラフ（数字は乗車時間・分）
railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
INF = float("inf")      # inf は無限大。「まだ行き方が1つも見つかっていない」印に使う

# distance = 距離表、came_from = その駅へいちばん早く来るときの1つ前の駅（第5回と同じ）
distance = {}
came_from = {}
for station in railway:
    distance[station] = INF
    came_from[station] = None
distance[start] = 0

settled = set()         # 確定した駅
queue = [(0, start)]    # heapq の箱。(その駅までの時間, 駅名) の組を入れる。最初は出発点だけ
# 取り出すごとの記録（窓の表示に使う）: (取り出した組, 確定か読み飛ばしか, 距離表, 確定済み, 箱の中身, 書き直し)
log = [(None, "start", dict(distance), set(settled), list(queue), [])]

print("heapq から取り出した順番")
print("-" * 56)
while len(queue) > 0:
    # ① 箱から、時間がいちばん小さい組を取り出す（第5回の「全部の駅を見てさがす」ループが、この1行になる）
    minutes, current = heapq.heappop(queue)

    # 同じ駅が箱に2回以上入ることがある。確定済みの駅の組は、古い（大きい）時間なので読み飛ばす
    if current in settled:
        print(f"  ({minutes}分, {current}) → すでに確定済みなので読み飛ばす")
        log.append(((minutes, current), "skip", dict(distance), set(settled), list(queue), []))
        continue

    # ② 取り出した駅を確定する
    settled.add(current)
    print(f"  ({minutes}分, {current}) → {current} を {minutes}分で確定")

    # ③ となりの駅について、current を通るほうが短ければ書き直し、その組を箱に入れる
    changes = []
    for name, weight in railway[current]:      # name = となりの駅、weight = その区間の時間
        if name in settled:
            continue
        new_distance = minutes + weight
        if new_distance < distance[name]:
            old = distance[name]
            distance[name] = new_distance
            came_from[name] = current
            heapq.heappush(queue, (new_distance, name))     # 書き直した時間を、組にして箱に入れる
            changes.append((name, old, new_distance, weight))
            print(f"        {name} を {new_distance}分として queue に入れた")
    log.append(((minutes, current), "settle", dict(distance), set(settled), list(queue), changes))

print("-" * 56)
print()


def build_route(goal):
    """ゴールから came_from を逆にたどって道順を組み立てる（第5回の例題2と同じ）"""
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


print("新宿から各駅への最短の行き方")
print("-" * 56)
for station in railway:
    if station == start:
        continue
    print(f"{station:<4} {distance[station]:>3}分   " + " → ".join(build_route(station)))
print("-" * 56)
print("第5回の例題1・例題2と、まったく同じ答えになっている")


# ============================================================
# ここから下は、重み付きグラフ・queue・距離表を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1つ取り出す   R = 最初から   Esc = 終わる
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
    k = int(os.environ.get("AL2_STEP", last_step)) if capture else 0
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
        hint = fonts[2].render("スペース: 再生／一時停止   →: 1つ取り出す   R: 最初から   Esc: 終わる", True, SUB)
        screen.blit(hint, (30, HEIGHT - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)




def _item(entry):
    """queue の組 (時間, 名前) を、窓に書く文字にする。"""
    return f"({entry[0]}, {entry[1]})"


def show_window(graph, start, log, title, closed=(), where=None):
    """heapq を使うダイクストラ法で、queue（箱）から1つずつ取り出して距離表を埋めていくようすを表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names, edges = _graph_parts(graph)
    pos = _placed(names, edges, where) if where else _layout(names, edges)
    problems = _problems(graph, names, log[-1][2])
    pops = sum(1 for entry in log if entry[0] is not None)
    skips = sum(1 for entry in log if entry[1] == "skip")
    last_step = len(log)                            # 最後の1つは「まとめ」の画面
    x0 = 560

    def chips(queue, y):
        """queue の中身を、リストの並び順のまま札にして並べる。先頭（いちばん小さい組）は緑。下の端の y を返す。"""
        screen.blit(big.render("queue（heapq の箱）", True, GREEN), (x0, y))
        screen.blit(small.render("リストの並び順のまま。緑の先頭（0番目）が次に取り出される", True, SUB), (x0, y + 32))
        x, y = x0, y + 58
        if not queue:
            screen.blit(mid.render("（空っぽ）", True, SUB), (x, y))
            return y + 30
        for i, entry in enumerate(queue):
            t = small.render(_item(entry), True, GREEN if i == 0 else TEXT)
            w = t.get_width() + 16
            if x + w > x0 + 470:
                x, y = x0, y + 30
            box = pygame.Rect(x, y, w, 26)
            pygame.draw.rect(screen, (26, 44, 10) if i == 0 else (30, 30, 38), box, border_radius=6)
            pygame.draw.rect(screen, GREEN if i == 0 else LINE, box, width=2 if i == 0 else 1, border_radius=6)
            screen.blit(t, (x + 8, y + 4))
            x += w + 6
        return y + 30

    def table(dist, settled, current, changes, top):
        changed = {name: (old, new) for name, old, new, _ in changes}
        row_h = max(20, min(32, (HEIGHT - 40 - 4 * 26 - 30 - top) // max(len(names), 1)))   # 下に説明を4行書ける高さを残す
        font = mid if row_h >= 28 else small
        screen.blit(small.render("場所", True, SUB), (x0 + 10, top))
        screen.blit(small.render("時間（距離表）", True, SUB), (x0 + 200, top))
        for i, name in enumerate(names):
            y = top + 22 + i * row_h
            box = pygame.Rect(x0, y, 460, row_h - 3)
            done = name in settled
            pygame.draw.rect(screen, (26, 44, 10) if done else (30, 30, 38), box, border_radius=6)
            if name == current:
                pygame.draw.rect(screen, WHITE, box, width=3, border_radius=6)
            ty = y + (row_h - 3 - font.get_height()) // 2
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
        return top + 22 + len(names) * row_h

    def draw(k):
        final = k == len(log)
        popped, kind, dist, settled, queue, changes = log[min(k, len(log) - 1)]
        current = popped[1] if popped and not final else None
        rings = {n: AMBER for n in names if dist.get(n, INF) != INF}
        rings.update({n: GREEN for n in settled})
        colored = []
        if current:
            rings[current] = RED if kind == "skip" else WHITE
            colored = [([(current, n) for n, *_ in changes], AMBER, 6)]
        labels = {n: (_minutes(dist.get(n, INF)), GREEN if n in settled else (AMBER if dist.get(n, INF) != INF else SUB))
                  for n in names}
        screen.blit(big.render(_fit(big, title, 500), True, GREEN), (30, 20))
        screen.blit(small.render(f"出発 {start}　丸の外の数字 = 距離表の時間", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, colored, rings, labels, closed)
        bottom = chips(queue, 16)
        bottom = table(dist, settled, None if final or kind == "skip" else current, [] if final else changes, bottom + 8)
        lines = []
        if k == 0:
            lines = [(f"はじめ: queue に ({0}, {start}) だけ入れた", TEXT), ("スペースで開始／→で1つ取り出す", SUB)]
        elif final:
            lines = [(f"queue が空になったので終わり。heappop {pops}回（うち読み飛ばし {skips}回）", TEXT)]
            lines += [(p, RED) for p in problems]
        elif kind == "skip":
            lines = [(f"{k}回目の heappop: {_item(popped)} を取り出した", TEXT),
                     (f"{popped[1]} はもう確定済み → 古い組なので読み飛ばす", RED)]
        else:
            lines = [(f"{k}回目の heappop: {_item(popped)} → {popped[1]} を {popped[0]}分で確定", TEXT)]
            for n, o, v, w in changes:
                verb = f"{_minutes(o)} → {v}分" if o != INF else f"{v}分"
                lines.append((f"{n} {verb}（{popped[0]} + {w}）→ queue に ({v}, {n})",
                              AMBER if o != INF else TEXT))
            if not changes:
                lines.append(("queue に入れたものはない（となりは確定済みか、表の時間が同じか短い）", SUB))
        room = max(1, (HEIGHT - 40 - bottom) // 26)
        if len(lines) > room:
            lines = lines[:room - 1] + [(f"ほか {len(lines) - room + 1} 件", SUB)]
        for i, (text, color) in enumerate(lines):
            screen.blit(small.render(_fit(small, text, 480), True, color), (x0, bottom + 6 + i * 26))

    _loop(screen, fonts, last_step, draw)


# --- 窓を開いて、queue から1つずつ取り出して距離表が埋まっていくようすをアニメーション表示する ---
# 白い枠 = いま確定した駅、赤い枠 = 読み飛ばした駅、橙の線 = 書き直して queue に入れた区間
show_window(railway, start, log, "heapq でダイクストラ法")
