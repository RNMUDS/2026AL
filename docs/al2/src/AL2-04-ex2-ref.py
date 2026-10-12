from collections import deque               # 幅優先探索のキューに使う

railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
goal = "品川"


def route_minutes(route):
    """route（駅を通る順に並べたリスト）の合計時間を求める（例題1と同じ）。"""
    total = 0
    for i in range(len(route) - 1):
        for name, minutes in railway[route[i]]:
            if name == route[i + 1]:            # 次に行く駅が見つかったら
                total = total + minutes         # ★ その区間の時間を、いままでの合計に足す（1 を足すのではない）
    return total


# --- 方法1: 幅優先探索。キューの左から取り出し、まだ見つけていないとなりを右に入れる ---
# minutes も取り出しているが使っていない。つまり時間（重み）は見ていない
came_from = {start: None}                   # 鍵 = 見つけた駅、値 = どの駅から来たか
queue = deque([start])
bfs_log = []
while len(queue) > 0:
    current = queue.popleft()
    if current == goal:
        bfs_log.append((current, list(queue)))
        break
    for name, minutes in railway[current]:
        if name in came_from:               # 先に見つけた道を残し、あとから来た道は捨てる
            continue
        came_from[name] = current
        queue.append(name)
    bfs_log.append((current, list(queue)))

# ゴールから came_from を逆にたどって道を作る
bfs_route = []
node = goal
while node is not None:
    bfs_route.append(node)
    node = came_from[node]
bfs_route.reverse()

# --- 方法2: 全探索。書きかけの道をスタックに積み、1駅ずつのばしてすべての行き方を集める ---
every_route = []
stack = [[start]]
while len(stack) > 0:
    route = stack.pop()
    here = route[-1]                        # 道の先にいる駅
    if here == goal:
        every_route.append(route)
        continue
    for name, minutes in railway[here]:
        if name not in route:               # 同じ駅を2度通らない
            stack.append(route + [name])

print("新宿から品川までの行き方をすべて書き出す（全探索）")
print("-" * 56)
route_log = []
for route in every_route:
    minutes = route_minutes(route)
    route_log.append((route, minutes))
    text = " → ".join(route)
    print(f"  {text}: 路線{len(route) - 1}本 ／ {minutes}分")
print("-" * 56)
print("行き方の数:", len(every_route), "通り")
print()

# 1つ目を仮の答え（best_route）にして、もっと良い道が出てきたら入れかえる
best_route = every_route[0]
best_log = []
for route in every_route:
    # ★ 比べるのは「合計時間」。いま見ている道の時間が best_route の時間より小さいときだけ入れかえる
    #    （駅の数 len(...) で比べると、幅優先探索と同じ「本数が少ない道」になってしまう）
    if route_minutes(route) < route_minutes(best_route):
        best_route = route
    best_log.append(best_route)

print("方法1: 幅優先探索が選んだ道")
text = " → ".join(bfs_route)
print(f"  {text}: 路線{len(bfs_route) - 1}本 ／ {route_minutes(bfs_route)}分")
print()
print("方法2: 全探索で選んだ、合計時間がいちばん短い道")
text = " → ".join(best_route)
print(f"  {text}: 路線{len(best_route) - 1}本 ／ {route_minutes(best_route)}分")
print()
print("差:", route_minutes(bfs_route) - route_minutes(best_route), "分")
print()
print("幅優先探索は「路線の本数」を最小にする。「合計時間」は最小になるとはかぎらない。")

# ---- ここから下は、重み付きグラフを窓に絵で表示するための道具（読まなくてよい） ----
import math
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

WIDTH, HEIGHT = 1060, 620
STEP_MS = 900
BG = (18, 18, 24)
LINE = (80, 84, 100)
NODE = (38, 40, 52)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
GREEN = (118, 185, 0)
AMBER = (255, 184, 0)
BLUE = (90, 170, 255)
RED = (255, 110, 110)

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

def _graph_parts(railway):
    """隣接リストから、丸にする駅の名前と、線（駅, 駅, 時間）の一覧を作る。
    となりの一覧には書いたのに、鍵（左側）に書き忘れた駅も丸として描けるように足しておく。"""
    names = list(railway)
    for a in railway:
        for b, _ in railway[a]:
            if b not in names:
                names.append(b)
    edges = []
    for a in railway:
        for b, w in railway[a]:
            if not any({a, b} == {x, y} for x, y, _ in edges):
                edges.append((a, b, w))
    return names, edges

def _weight(railway, a, b):
    """a から b への時間。直接つながっていなければ None。"""
    for name, w in railway.get(a, []):
        if name == b:
            return w
    return None

def _pairs(route):
    """道（駅の並び）を、隣り合う2駅の組の一覧にする。"""
    return [(route[i], route[i + 1]) for i in range(len(route) - 1)]

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

def _layout(names, edges, cx=255, cy=320, radius=200):
    """頂点を円の上に等間隔で並べる（いちばん上から時計回り）。
    頂点が8個以下なら、線の交わりがいちばん少なくなる並べ方を全部試して選ぶ。"""
    order = list(names)
    if 3 < len(order) <= 8:
        from itertools import permutations
        best = None
        for rest in permutations(order[1:]):
            cand = [order[0], *rest]
            k = _crossings(cand, edges)
            if best is None or k < best[0]:
                best = (k, cand)
        order = best[1]
    n = len(order)
    return {name: (cx + radius * math.sin(2 * math.pi * i / n), cy - radius * math.cos(2 * math.pi * i / n))
            for i, name in enumerate(order)}

def _draw_graph(screen, fonts, names, edges, pos, colored=(), rings=None, dim_weights=False):
    """丸（頂点）と線（辺）と、線のまん中の重み（時間）を描く。
    colored = [(駅の組の一覧, 色, 太さ), ...]。あとのものほど上に重ねて描く。
    rings = {駅の名前: 枠の色}。dim_weights=True なら重みを暗く描く（幅優先探索は重みを見ないため）。"""
    big, mid, small = fonts
    edge_color = {}
    for a, b, _ in edges:
        pygame.draw.line(screen, LINE, pos[a], pos[b], 2)
    for pairs, color, width in colored:
        for a, b in pairs:
            if a in pos and b in pos:
                pygame.draw.line(screen, color, pos[a], pos[b], width)
                edge_color[frozenset((a, b))] = color
    for a, b, w in edges:
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        color = edge_color.get(frozenset((a, b)), SUB if dim_weights else TEXT)
        t = small.render(f"{w}分", True, color)
        box = pygame.Rect(0, 0, t.get_width() + 12, t.get_height() + 4)
        box.center = (mx, my)
        pygame.draw.rect(screen, BG, box, border_radius=8)
        pygame.draw.rect(screen, color if frozenset((a, b)) in edge_color else LINE, box, width=1, border_radius=8)
        screen.blit(t, (box.x + 6, box.y + 2))
    for name in names:
        x, y = pos[name]
        ring = (rings or {}).get(name, LINE)
        pygame.draw.circle(screen, NODE, (x, y), 34)
        pygame.draw.circle(screen, ring, (x, y), 34, 5 if ring != LINE else 3)
        t = mid.render(name, True, TEXT)
        if t.get_width() > 62:
            t = small.render(name, True, TEXT)
        if t.get_width() > 62:
            half = (len(name) + 1) // 2
            t1, t2 = small.render(name[:half], True, TEXT), small.render(name[half:], True, TEXT)
            screen.blit(t1, (x - t1.get_width() / 2, y - t1.get_height()))
            screen.blit(t2, (x - t2.get_width() / 2, y))
            continue
        screen.blit(t, (x - t.get_width() / 2, y - t.get_height() / 2))

def _fit(font, text, width):
    """text が width ピクセルに収まらなければ、後ろを「…」にして縮める。"""
    if font.size(text)[0] <= width:
        return text
    while text and font.size(text + "…")[0] > width:
        text = text[:-1]
    return text + "…"

def _loop(screen, fonts, last_step, draw):
    """窓のくり返し処理。draw(k) が k 手順目の画面を描く。"""
    capture = os.environ.get("AL2_CAPTURE")
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

def show_window(railway, start, goal, bfs_log, came_from, bfs_route, route_log, best_log):
    """幅優先探索の進み方と、全探索で行き方を1つずつ比べるようすをアニメーション表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("幅優先探索と全探索をくらべる")
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names, edges = _graph_parts(railway)
    pos = _layout(names, edges)
    b_steps = len(bfs_log)
    r_steps = len(route_log)
    last_step = b_steps + 1 + r_steps + 1
    true_min = {}
    for route, _ in route_log:
        ws = [_weight(railway, a, b) for a, b in _pairs(route)]
        true_min[tuple(route)] = None if None in ws else sum(ws)
    bfs_minutes = sum(_weight(railway, a, b) or 0 for a, b in _pairs(bfs_route))
    row_h = min(40, (HEIGHT - 280) // max(r_steps, 1))

    def bfs_state(j):
        popped = [c for c, _ in bfs_log[:j]]
        found = [start] + [v for v in came_from if came_from[v] in popped]
        tree = [(came_from[v], v) for v in found if came_from[v] is not None]
        return popped, found, tree

    def route_rows(upto, best_i, frames):
        for i in range(upto):
            route, minutes = route_log[i]
            y = 128 + i * row_h
            box = pygame.Rect(540, y, 490, row_h - 6)
            frame = frames.get(i, (70, 70, 80))
            pygame.draw.rect(screen, (30, 30, 38), box, border_radius=6)
            pygame.draw.rect(screen, frame, box, width=1 if frame == (70, 70, 80) else 3, border_radius=6)
            font = mid if row_h >= 34 else small
            ty = y + (row_h - 6 - font.get_height()) // 2
            mark = "★" if i == best_i else "  "
            text = f"{mark} {' → '.join(route)}"
            tfont = font if font.size(text)[0] <= 360 else small
            screen.blit(tfont.render(_fit(tfont, text, 360), True, TEXT), (550, y + (row_h - 6 - tfont.get_height()) // 2))
            t = font.render(f"{len(route) - 1}本 ／ {minutes}分", True, AMBER if i == best_i else SUB)
            screen.blit(t, (1020 - t.get_width(), ty))

    def draw(k):
        x0 = 540
        colored, rings, dim = [], {}, False
        info2, info3, color = "", "", SUB
        if k == 0:
            title, sub = "これから2つの方法で道をさがす", "方法1 = 幅優先探索、方法2 = 全探索"
            info = "スペースで開始／→で1手順"
            rings = {start: (255, 255, 255), goal: AMBER}
        elif k <= b_steps:
            dim = True
            current, queue_now = bfs_log[k - 1]
            popped, found, tree = bfs_state(k)
            colored = [(tree, GREEN, 6)]
            rings = {v: AMBER for v in found}
            rings.update({v: GREEN for v in popped})
            rings[current] = (255, 255, 255)
            title, sub = "方法1: 幅優先探索", "キューの左から取り出し、となりを右に入れる（時間は見ない）"
            screen.blit(mid.render("キュー（左から取り出す）", True, SUB), (x0, 90))
            bx = x0
            for name in queue_now:
                t = mid.render(name, True, TEXT)
                box = pygame.Rect(bx, 120, t.get_width() + 20, 38)
                pygame.draw.rect(screen, (30, 30, 38), box, border_radius=6)
                pygame.draw.rect(screen, AMBER, box, width=2, border_radius=6)
                screen.blit(t, (bx + 10, 126))
                bx += box.width + 8
            if not queue_now:
                screen.blit(mid.render("（からっぽ）", True, SUB), (x0, 126))
            screen.blit(mid.render("取り出した順", True, SUB), (x0, 190))
            screen.blit(mid.render(_fit(mid, " → ".join(popped), 490), True, GREEN), (x0, 220))
            screen.blit(small.render("緑の線 = どの駅から見つけたか（came_from）", True, SUB), (x0, 270))
            info = f"手順{k}  {current} を取り出した"
            if current == goal:
                info2, color = "ゴールを取り出したので、幅優先探索はここで終わり", AMBER
            else:
                new = [v for v in found if came_from.get(v) == current]
                info2 = "新しく見つけた駅: " + ("、".join(new) if new else "なし")
        elif k == b_steps + 1:
            colored = [(_pairs(bfs_route), BLUE, 8)]
            rings = {v: BLUE for v in bfs_route}
            title, sub = "方法1の答え: 幅優先探索が選んだ道", "ゴールから came_from を逆にたどった道"
            screen.blit(mid.render(_fit(mid, " → ".join(bfs_route), 490), True, BLUE), (x0, 100))
            info = f"路線{len(bfs_route) - 1}本 ／ 合計 {bfs_minutes}分"
            info2 = "幅優先探索は、路線の本数がいちばん少ない道を選ぶ"
            info3 = "時間（線の数字）は1回も見ていない"
        elif k <= b_steps + 1 + r_steps:
            r = k - b_steps - 1
            route = route_log[r - 1][0]
            best = best_log[r - 1]
            colored = [(_pairs(best), GREEN, 8), (_pairs(route), AMBER, 5)]
            rings = {v: AMBER for v in route}
            title, sub = "方法2: 全探索", "行き方を1つずつ調べ、★ = いまのところいちばん短い道"
            best_i = max(i for i in range(r) if route_log[i][0] == best)
            route_rows(r, best_i, {r - 1: (255, 255, 255)})
            info = f"手順{k}  {r}通り目: {route_log[r - 1][1]}分"
            if r > 1 and best_log[r - 1] != best_log[r - 2]:
                info2, color = "前の ★ より短いので、★ を入れかえた", AMBER
            elif r > 1:
                info2 = "★ より短くないので、★ はそのまま"
            else:
                info2 = "1つ目を仮の ★ にする"
        else:
            best = best_log[-1]
            colored = [(_pairs(bfs_route), BLUE, 10), (_pairs(best), GREEN, 6)]
            rings = {v: GREEN for v in best}
            rings.update({v: BLUE for v in bfs_route if v not in best})
            title, sub = "くらべる: 青 = 幅優先探索、緑 = 全探索の答え", "右の一覧の青い枠と緑の枠"
            best_i = max(i for i in range(r_steps) if route_log[i][0] == best)
            frames = {i: BLUE for i in range(r_steps) if route_log[i][0] == bfs_route}
            frames[best_i] = GREEN
            route_rows(r_steps, best_i, frames)
            real = min((v for v in true_min.values() if v is not None), default=None)
            best_real = true_min.get(tuple(best))
            wrong = [(rt, m) for rt, m in route_log if m != true_min[tuple(rt)]]
            info = f"青 {len(bfs_route) - 1}本 {bfs_minutes}分 ／ 緑 {len(best) - 1}本 {best_real}分"
            if wrong:
                rt, m = wrong[0]
                info2, color = f"{' → '.join(rt)} の答えが {m}分", RED
                info3 = f"→ 足すと {true_min[tuple(rt)]}分のはず。route_minutes を見直す"
            elif best_real != real:
                info2, color = f"★ の道が {best_real}分 だが、もっと短い {real}分 の道がある", RED
                info3 = "→ best_route を入れかえる条件（比べる式）を見直す"
            elif bfs_minutes > best_real:
                info2, color = f"差 {bfs_minutes - best_real}分。幅優先探索は本数しか見ないので、", AMBER
                info3 = "合計時間がいちばん短い道を選べない"
            else:
                info2, color = "この時間では、2つの方法の答えが同じになった", AMBER
                info3 = "→ 時間を書き換えると、答えがずれることがある"
        screen.blit(big.render("重み付きグラフ（線の数字 = 時間）", True, GREEN), (30, 20))
        screen.blit(small.render(f"出発 {start} → ゴール {goal}", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, colored, rings, dim)
        screen.blit(big.render(title, True, GREEN), (x0, 20))
        screen.blit(small.render(sub, True, SUB), (x0, 52))
        by = HEIGHT - 150
        screen.blit(mid.render(_fit(mid, info, 500), True, TEXT), (x0, by))
        screen.blit(mid.render(_fit(mid, info2, 500), True, color), (x0, by + 32))
        screen.blit(mid.render(_fit(mid, info3, 500), True, color), (x0, by + 64))

    _loop(screen, fonts, last_step, draw)

show_window(railway, start, goal, bfs_log, came_from, bfs_route, route_log, best_log)
