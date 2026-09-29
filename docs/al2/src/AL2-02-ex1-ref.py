maze = [
    "S.....#",
    ".####.#",
    ".#....#",
    ".#.##..",
    ".#..#.#",
    ".##.#.#",
    "......G",
]

rows = len(maze)
cols = len(maze[0])

for r in range(rows):
    for c in range(cols):
        if maze[r][c] == "S":
            start = (r, c)
        if maze[r][c] == "G":
            goal = (r, c)

stack = [start]
came_from = {start: None}
visited_order = []
memo_log = []

while len(stack) > 0:
    current = stack.pop()
    visited_order.append(current)
    if current == goal:
        break

    r, c = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if maze[nr][nc] == "#":
            continue
        if (nr, nc) in came_from:
            continue
        came_from[(nr, nc)] = current
        stack.append((nr, nc))
    memo_log.append((current, list(stack)))

path = []
node = goal
while node is not None:
    path.append(node)
    node = came_from[node]
path.reverse()

print("深さ優先探索が見つけた経路の歩数:", len(path) - 1, "歩")
print("調べたマスの数:", len(visited_order), "マス")


# ---- ここから下は、迷路を窓に絵で表示するための道具（読まなくてよい） ----
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

CELL = 48
STEP_MS = 350
BG = (18, 18, 24)
FLOOR = (38, 40, 52)
WALL = (92, 98, 118)
WALL_DARK = (66, 70, 86)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
COLORS = [(118, 185, 0), (255, 184, 0)]
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


def _memo_at(log, goal, k):
    """k 手順目（1から）に読んだマスと、そのあとのメモ。ゴールを読んだ手順は記録がないので作る。"""
    if k - 1 < len(log):
        return log[k - 1]
    memo = [cell for cell in log[-1][1] if cell != goal] if log else []
    return goal, memo


def _draw_panel(screen, fonts, maze, run, k, x0, y0, color):
    title, order, path, log = run
    rows, cols = len(maze), len(maze[0])
    goal = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "G")
    k = min(k, len(order))
    done = k == len(order)
    number = {cell: i + 1 for i, cell in enumerate(order[:k])}
    current, memo = _memo_at(log, goal, k) if k > 0 else (None, [])
    next_cell = None if done else order[k]

    big, mid, small = fonts
    screen.blit(big.render(title, True, color), (x0, y0))
    gy = y0 + 44
    for c in range(cols):
        t = small.render(str(c), True, SUB)
        screen.blit(t, (x0 + 22 + c * CELL + CELL // 2 - t.get_width() // 2, gy - 2))
    for r in range(rows):
        t = small.render(str(r), True, SUB)
        screen.blit(t, (x0 + 4, gy + 18 + r * CELL + CELL // 2 - t.get_height() // 2))
    gx, gy = x0 + 22, gy + 18
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(gx + c * CELL + 2, gy + r * CELL + 2, CELL - 4, CELL - 4)
            ch = maze[r][c]
            if ch == "#":
                pygame.draw.rect(screen, WALL, rect, border_radius=6)
                pygame.draw.rect(screen, WALL_DARK, rect.inflate(-14, -14), border_radius=4)
                continue
            fill = FLOOR
            if (r, c) in number:
                fill = tuple(int(f * 0.55 + col * 0.45) for f, col in zip(FLOOR, color))
            pygame.draw.rect(screen, fill, rect, border_radius=6)
            if (r, c) in memo:
                pygame.draw.rect(screen, color, rect, width=3, border_radius=6)
            if (r, c) == current and not done:
                pygame.draw.rect(screen, (255, 255, 255), rect, width=4, border_radius=6)
    if done and len(path) > 1:
        for r, c in path:
            rect = pygame.Rect(gx + c * CELL + 2, gy + r * CELL + 2, CELL - 4, CELL - 4)
            pygame.draw.rect(screen, (255, 255, 255), rect, width=3, border_radius=6)
        points = [(gx + c * CELL + CELL // 2, gy + r * CELL + CELL // 2) for r, c in path]
        pygame.draw.lines(screen, (255, 255, 255), False, points, 3)
    for r in range(rows):
        for c in range(cols):
            ch = maze[r][c]
            if ch == "#":
                continue
            rect = pygame.Rect(gx + c * CELL + 2, gy + r * CELL + 2, CELL - 4, CELL - 4)
            if ch in "SG":
                label = small.render(ch, True, (255, 255, 255) if ch == "S" else (255, 215, 64))
                screen.blit(label, (rect.x + 3, rect.y))
            if (r, c) in number:
                t = mid.render(str(number[(r, c)]), True, TEXT)
                shadow = mid.render(str(number[(r, c)]), True, (0, 0, 0))
                tx, ty = rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2 + 4
                screen.blit(shadow, (tx + 1, ty + 1))
                screen.blit(t, (tx, ty))
            if (r, c) == next_cell:
                t = small.render("次", True, color)
                screen.blit(t, (rect.right - t.get_width() - 3, rect.y + 1))
    by = gy + rows * CELL + 12
    if k == 0:
        info = "スペースで開始／→で1手順"
    elif done:
        info = f"ゴール！ 通り道 {len(path) - 1}歩 ／ 調べたマス {len(order)}マス"
    else:
        info = f"手順{k}  読んだマス ({current[0]},{current[1]})"
    screen.blit(mid.render(info, True, TEXT), (x0, by))
    screen.blit(small.render("メモ（左が古い行、右が新しい行）", True, SUB), (x0, by + 30))
    bx = x0
    width = cols * CELL + 22
    for i, (r, c) in enumerate(memo):
        t = small.render(f"({r},{c})", True, color if (r, c) == next_cell else TEXT)
        w = t.get_width() + 12
        if bx + w > x0 + width - 20:
            screen.blit(small.render("…", True, SUB), (bx, by + 56))
            break
        box = pygame.Rect(bx, by + 52, w, 26)
        pygame.draw.rect(screen, (30, 30, 38), box, border_radius=5)
        pygame.draw.rect(screen, color if (r, c) == next_cell else (80, 80, 90), box,
                         width=2 if (r, c) == next_cell else 1, border_radius=5)
        screen.blit(t, (bx + 6, by + 55))
        bx += w + 4


def show_window(maze, runs):
    """runs の探索を横に並べて、1手順ずつアニメーション表示する。窓を閉じると終わる。"""
    global CELL
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    CELL = max(20, min(48, 1100 // (len(runs) * cols + 1), 620 // (rows + 1)))
    panel_w = max(cols * CELL + 22, 340)
    panel_h = 44 + 18 + rows * CELL + 100
    width = max(30 + len(runs) * (panel_w + 30), 800)
    height = panel_h + 84
    capture = os.environ.get("AL2_CAPTURE")
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("迷路の探索")
    fonts = (_font(22, True), _font(18), _font(14))
    longest = max(len(run[1]) for run in runs)
    k = longest if capture else 0
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
                if event.key == pygame.K_RIGHT and k < longest:
                    k += 1
                    playing = False
                if event.key == pygame.K_r:
                    k, playing = 0, False
        if playing and pygame.time.get_ticks() - last >= STEP_MS:
            last = pygame.time.get_ticks()
            if k < longest:
                k += 1
            else:
                playing = False
        screen.fill(BG)
        for i, run in enumerate(runs):
            _draw_panel(screen, fonts, maze, run, k, 30 + i * (panel_w + 30), 20,
                        COLORS[1] if run[0].startswith("深さ") else COLORS[0])
        legend = fonts[2].render("色つき = 調べたマス（数字は何番目か）   枠だけ = メモにあるマス   白い線 = 通り道   灰色のブロック = 壁",
                                 True, SUB)
        screen.blit(legend, (30, height - 56))
        hint = fonts[2].render("スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる", True, SUB)
        screen.blit(hint, (30, height - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)


show_window(maze, [("深さ優先探索", visited_order, path, memo_log)])
