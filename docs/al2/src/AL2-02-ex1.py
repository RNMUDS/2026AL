# 深さ優先探索で迷路を解く
# 幅優先探索との違いは「メモのどこを読むか」だけ。
#   幅優先探索: いちばん古い行（先に書いた行）を読む → popleft()
#     （popleft() は deque の先頭を取り出す命令。前期の幅優先探索で使った）
#   深さ優先探索: いちばん新しい行を読む → pop()

# S = スタート、G = ゴール、# = 壁、. = 通路
# 文字列のリスト。maze[行][列] で1マスの文字が取り出せる（行・列は 0 から数える）
# 例 maze[0][0] は "S"、maze[0][3] は "#"
maze = [
    "S..#...",
    ".#.#.#.",
    ".#...#.",
    ".####..",
    "...#.#.",
    ".#.#.#.",
    ".#....G",
]

rows = len(maze)        # 行の数（縦のマス数）
cols = len(maze[0])     # 列の数（横のマス数）。1行目の文字数で数える

# S と G の場所をさがす。場所は (行, 列) の組（タプル）で表す
for r in range(rows):
    for c in range(cols):
        if maze[r][c] == "S":
            start = (r, c)
        if maze[r][c] == "G":
            goal = (r, c)

# --- 深さ優先探索 ---
# stack は「これから調べる場所」を書いたメモ。最初はスタートだけが書いてある。
# 分かれ道では行ける場所が2つ以上見えるが、体は1つなので、
# 1つに進むあいだ、残りは「あとで見る場所」としてメモに書いておく。
# 深さ優先探索ではメモを積み重ねた本のように使う（スタック: 最後に置いたものを最初に取る）
stack = [start]
# came_from は「その場所へ、どこから来たか」の記録（辞書）。
# 例 came_from[(0, 1)] = (0, 0) なら「(0,1) へは (0,0) から来た」
came_from = {start: None}
visited_order = []              # 調べた順番を記録する
memo_log = []                   # 手順ごとの「読んだマス」と「そのあとのメモ」の記録（窓の表示に使う）

while len(stack) > 0:           # メモが空になるまでくり返す
    # pop() はリストの最後（いちばん新しく書いた行）を取り出して消す。
    # だから、いま見つけたばかりの道の先へ、どんどん進んでいく
    current = stack.pop()
    visited_order.append(current)
    if current == goal:         # ゴールを読んだら終わり（break はくり返しを抜ける）
        break

    r, c = current              # (行, 列) の組を、r（行）と c（列）の2つの変数に分けて入れる
    # (-1, 0) は上、(1, 0) は下、(0, -1) は左、(0, 1) は右へ1マス動くことを表す
    # for dr, dc in ... は、組 (-1, 0) を取り出して dr = -1、dc = 0 のように2つの変数に分けて入れる
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        # 迷路の外に出てしまう場所は飛ばす（continue は「この回を飛ばして次へ」）
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if maze[nr][nc] == "#":     # 壁も飛ばす
            continue
        # すでにメモに書いた場所をもう一度書くと、同じマスを何度も調べてしまうので飛ばす
        if (nr, nc) in came_from:
            continue
        came_from[(nr, nc)] = current
        stack.append((nr, nc))  # メモの最後（いちばん新しい行）に書き足す
    # list(stack) でメモの中身をコピーして記録する。stack はこのあとも書き換わるので、コピーしないと残らない
    memo_log.append((current, list(stack)))

# --- ゴールからスタートへ逆にたどって経路を復元する ---
path = []
node = goal
# None は「何もない」を表す特別な値。スタートの came_from は None なので、そこで止まる
while node is not None:
    path.append(node)
    node = came_from[node]
path.reverse()              # ゴール→スタートの順を、スタート→ゴールの順に直す

# 歩数は「通ったマスの数 - 1」（スタートのマスは歩数に数えない）
print("深さ優先探索が見つけた経路の歩数:", len(path) - 1, "歩")
print("調べたマスの数:", len(visited_order), "マス")


# ============================================================
# ここから下は、迷路を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

CELL = 48                       # 1マスの大きさ（ピクセル）
STEP_MS = 350                   # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
FLOOR = (38, 40, 52)
WALL = (92, 98, 118)
WALL_DARK = (66, 70, 86)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
COLORS = [(118, 185, 0), (255, 184, 0)]     # 1つ目の探索は緑、2つ目は橙
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
    next_cell = None if done else order[k]     # 次の手順で読まれるマス

    big, mid, small = fonts
    screen.blit(big.render(title, True, color), (x0, y0))
    gy = y0 + 44
    # 列・行の番号
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
    # 通り道（最後まで調べ終えたら、白い枠と線で示す）
    if done and len(path) > 1:
        for r, c in path:
            rect = pygame.Rect(gx + c * CELL + 2, gy + r * CELL + 2, CELL - 4, CELL - 4)
            pygame.draw.rect(screen, (255, 255, 255), rect, width=3, border_radius=6)
        points = [(gx + c * CELL + CELL // 2, gy + r * CELL + CELL // 2) for r, c in path]
        pygame.draw.lines(screen, (255, 255, 255), False, points, 3)
    # マスの中の文字（S・G・調べた番号・次）
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
    # 下の説明
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
    # 大きな迷路でも窓が画面に収まるように、マスの大きさを決める（最大48、最小20ピクセル）
    CELL = max(20, min(48, 1100 // (len(runs) * cols + 1), 620 // (rows + 1)))
    panel_w = max(cols * CELL + 22, 340)
    panel_h = 44 + 18 + rows * CELL + 100
    width = max(30 + len(runs) * (panel_w + 30), 800)
    height = panel_h + 84
    capture = os.environ.get("AL2_CAPTURE")      # 授業ページの画像を作るときだけ使う
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

# --- 窓を開いて、深さ優先探索が進むようすをアニメーション表示する ---
# マスの数字は「何番目に調べたか」。最後まで進むと、通り道が線で示される。
# スペースで再生／一時停止、→ で1手順ずつ進む。窓を閉じるとプログラムが終わる
show_window(maze, [("深さ優先探索", visited_order, path, memo_log)])
