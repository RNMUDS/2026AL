# 第7回 例題1（参考）: 床コスト付きの迷路を、幅優先探索とダイクストラ法の2つで解いて比べる
# 数字は「そのマスに入るのにかかる秒数」。9 のマスはぬかるみで、通るのに時間がかかる。
import heapq
from collections import deque

cost_map = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

rows = len(cost_map)          # 行の数（縦のマス数）
cols = len(cost_map[0])       # 列の数（横のマス数）
start = (0, 0)                # 左上
goal = (rows - 1, cols - 1)   # 右下
INF = float("inf")


def neighbors(r, c):
    """上・下・左・右のうち、迷路の中にあるマスを返す（第2回と同じ）"""
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            result.append((nr, nc))
    return result


def build_route(came_from):
    """ゴールから came_from を逆にたどって道順を組み立てる（第5回と同じ）"""
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


def route_seconds(route):
    """道順 route の合計秒数（スタートのマスは数えない。入ったマスの秒数を足す）"""
    total = 0
    for r, c in route[1:]:
        total = total + cost_map[r][c]
    return total


# ---- 幅優先探索（第2回）: 歩数の少ないマスから順に調べる。マスの秒数は見ない ----
steps = {start: 0}            # スタートから何歩か
came_bfs = {start: None}
bfs_order = []                # 調べた順の (マス, 歩数)。窓の表示に使う
memo = deque([start])         # あとで調べるマスのメモ（第2回のキュー）
while len(memo) > 0:
    current = memo.popleft()
    bfs_order.append((current, steps[current]))
    if current == goal:
        break
    for nxt in neighbors(current[0], current[1]):
        if nxt in came_bfs:
            continue
        came_bfs[nxt] = current
        steps[nxt] = steps[current] + 1
        memo.append(nxt)
bfs_route = build_route(came_bfs)

# ---- ダイクストラ法（第6回の heapq 版）: 合計秒数の小さいマスから順に確定する ----
distance = {}
came_dij = {}
for r in range(rows):
    for c in range(cols):
        distance[(r, c)] = INF
        came_dij[(r, c)] = None
distance[start] = 0
settled = set()
dij_order = []                # 確定した順の (マス, 合計秒数)。窓の表示に使う
queue = [(0, start)]
while len(queue) > 0:
    total, current = heapq.heappop(queue)
    if current in settled:
        continue                              # 古い組は読み飛ばす（第6回）
    settled.add(current)
    dij_order.append((current, total))
    if current == goal:
        break                                 # ゴールが確定したら、もっと早い道はないので止めてよい
    for nxt in neighbors(current[0], current[1]):
        new_total = total + cost_map[nxt[0]][nxt[1]]   # ← となりのマスに入る秒数を足す（グラフの「辺の重み」にあたる）
        if new_total < distance[nxt]:
            distance[nxt] = new_total
            came_dij[nxt] = current
            heapq.heappush(queue, (new_total, nxt))
dij_route = build_route(came_dij)


def show(route, title):
    """通り道のマスに * を付けて迷路を表示する"""
    print(title)
    for r in range(rows):
        line = ""
        for c in range(cols):
            mark = "*" if (r, c) in route else " "
            line = line + f"{cost_map[r][c]:>4}{mark}"
        print("  " + line)
    print()


print("床コスト付きの迷路（数字はそのマスに入るのにかかる秒数）")
show([], "-" * 30)
show(bfs_route, f"幅優先探索の通り道（*）: {len(bfs_route) - 1}歩 ／ 合計 {route_seconds(bfs_route)}秒")
show(dij_route, f"ダイクストラ法の通り道（*）: {len(dij_route) - 1}歩 ／ 合計 {route_seconds(dij_route)}秒")
print("-" * 46)
print("方法               歩数   合計秒数   決めたマス")
print(f"幅優先探索      {len(bfs_route) - 1:>5}歩 {route_seconds(bfs_route):>7}秒 {len(bfs_order):>8}マス")
print(f"ダイクストラ法  {len(dij_route) - 1:>5}歩 {route_seconds(dij_route):>7}秒 {len(dij_order):>8}マス")
print("-" * 46)
print("幅優先探索は歩数を、ダイクストラ法は合計秒数を、いちばん小さくしている")


# ============================================================
# ここから下は、迷路と探索の進み方を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

STEP_MS = 260                   # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
FLOOR = (38, 40, 52)
WALL = (92, 98, 118)
WALL_DARK = (66, 70, 86)
LINE = (80, 84, 100)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
GREEN = (118, 185, 0)
AMBER = (255, 184, 0)
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


def _terrain_color(cost):
    """マスの時間（コスト）で床の色を決める。1 = ふつうの床、大きいほど赤っぽく暗い色。"""
    if cost <= 1:
        return FLOOR
    if cost <= 4:
        return (58, 44, 78)         # むらさき = 少し時間がかかる（人ごみなど）
    if cost <= 8:
        return (78, 52, 30)         # 茶色 = 時間がかかる
    return (92, 34, 34)             # 赤 = とても時間がかかる（パレードなど）


def _fit(font, text, width):
    """text が width ピクセルに収まらなければ、後ろを「…」にして縮める。"""
    if font.size(text)[0] <= width:
        return text
    while text and font.size(text + "…")[0] > width:
        text = text[:-1]
    return text + "…"


def _draw_cells(screen, fonts, grid, labels, gx, gy, cell):
    """マス目を描く。grid[r][c] はそのマスに入る時間（None は通れない建物）。labels = {(r, c): "S"} など。"""
    _, _, small = fonts
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            rect = pygame.Rect(gx + c * cell + 1, gy + r * cell + 1, cell - 2, cell - 2)
            if grid[r][c] is None:
                pygame.draw.rect(screen, WALL, rect, border_radius=5)
                pygame.draw.rect(screen, WALL_DARK, rect.inflate(-cell // 3, -cell // 3), border_radius=3)
                continue
            pygame.draw.rect(screen, _terrain_color(grid[r][c]), rect, border_radius=5)
            if (r, c) in labels:
                t = small.render(labels[(r, c)], True, WHITE if labels[(r, c)] == "S" else AMBER)
            else:
                t = small.render(str(grid[r][c]), True, SUB if grid[r][c] <= 1 else TEXT)
            if cell >= 30:
                screen.blit(t, (rect.x + 3, rect.y + 1))


def _number(screen, font, text, rect, color):
    """マスのまん中に、影つきで数字を書く。"""
    t = font.render(text, True, color)
    shadow = font.render(text, True, (0, 0, 0))
    tx, ty = rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2 + 3
    screen.blit(shadow, (tx + 1, ty + 1))
    screen.blit(t, (tx, ty))


def _loop(screen, fonts, last_step, draw, hint):
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
        h = fonts[2].render(hint, True, SUB)
        screen.blit(h, (30, screen.get_height() - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)


def show_window(grid, labels, runs, title, legend):
    """2つの探索を横に並べて、マスが決まっていく順番を1手順ずつ表示する。窓を閉じると終わる。
    runs = [(見出し, 色, [(マス, 数), ...] 決まった順, 通り道, 最後に出す文), ...]"""
    pygame.init()
    rows, cols = len(grid), len(grid[0])
    cell = max(18, min(46, 470 // cols, 470 // rows))
    panel_w = max(cols * cell + 22, 440)
    width = 30 + len(runs) * (panel_w + 30)
    height = 70 + 26 + rows * cell + 150
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    last_step = max(len(run[2]) for run in runs)

    def panel(run, k, x0, y0):
        head, color, order, route, summary = run
        done = k >= len(order)
        shown = order[:k]
        value = dict(shown)
        screen.blit(big.render(head, True, color), (x0, y0))
        gx, gy = x0 + 22, y0 + 48
        for c in range(cols):
            t = small.render(str(c), True, SUB)
            screen.blit(t, (gx + c * cell + cell // 2 - t.get_width() // 2, gy - 20))
        for r in range(rows):
            t = small.render(str(r), True, SUB)
            screen.blit(t, (x0 + 4, gy + r * cell + cell // 2 - t.get_height() // 2))
        _draw_cells(screen, fonts, grid, labels, gx, gy, cell)
        for (r, c), v in shown:
            rect = pygame.Rect(gx + c * cell + 1, gy + r * cell + 1, cell - 2, cell - 2)
            on_route = done and (r, c) in route
            pygame.draw.rect(screen, WHITE if on_route else color, rect, width=4 if on_route else 2, border_radius=5)
            _number(screen, mid if cell >= 34 else small, str(v), rect, WHITE if on_route else TEXT)
        if shown and not done:
            (r, c), v = shown[-1]
            rect = pygame.Rect(gx + c * cell + 1, gy + r * cell + 1, cell - 2, cell - 2)
            pygame.draw.rect(screen, WHITE, rect, width=4, border_radius=5)
        by = gy + rows * cell + 12
        if k == 0:
            info, note = "スペースで開始／→で1手順", ""
        elif done:
            info, note = summary, f"決めたマス {len(order)}マス"
        else:
            (r, c), v = shown[-1]
            info, note = f"手順{k}  マス ({r},{c}) が {v} に決まった", f"決めたマス {k}マス"
        screen.blit(mid.render(_fit(mid, info, panel_w - 10), True, TEXT), (x0, by))
        screen.blit(small.render(note, True, SUB), (x0, by + 30))

    def draw(k):
        for i, run in enumerate(runs):
            panel(run, k, 30 + i * (panel_w + 30), 18)
        for i, text in enumerate(legend):
            screen.blit(small.render(text, True, SUB), (30, height - 104 + i * 24))

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、2つの探索でマスが決まっていく順番を並べてアニメーション表示する ---
# 左 = 幅優先探索（マスの数字は歩数）、右 = ダイクストラ法（マスの数字は合計秒数）、最後に白い枠 = 通り道
show_window(cost_map, {start: "S", goal: "G"}, [
    ("幅優先探索: 歩数の少ない順", AMBER, bfs_order, bfs_route,
     f"ゴール！ {len(bfs_route) - 1}歩 ／ 合計 {route_seconds(bfs_route)}秒"),
    ("ダイクストラ法: 合計秒数の小さい順", GREEN, dij_order, dij_route,
     f"ゴール！ {len(dij_route) - 1}歩 ／ 合計 {route_seconds(dij_route)}秒"),
], "床コスト付きの迷路", [
    "枠の色つきのマス = 決まったマス（数字: 左は歩数、右は合計秒数）   白い枠 = いま決まったマス（最後は通り道のマス）",
    "マスの左上の小さい数字 = そのマスに入る秒数（赤いマス = 9秒のぬかるみ）",
])
