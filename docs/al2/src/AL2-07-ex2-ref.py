# 第7回 例題2（参考）: ダイクストラ法を止めずに最後まで動かし、すべてのマスへの最小の秒数を求める
# 後半では、迷路を大きくしていったときに、ダイクストラ法にかかる時間を測る。
import heapq
import random
import time

cost_map = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]
start = (0, 0)

# 時間マップの色の区切り（この秒数まで, 名前）
bands = [(4, "すぐ着く"), (8, "少し歩く"), (12, "遠い")]

INF = float("inf")


def dijkstra_all(cost_map, start):
    """start からすべてのマスへの最小の秒数（距離表）と、確定した順番を返す。
    例題1とちがい、ゴールで止めずに queue が空になるまで続ける"""
    rows = len(cost_map)
    cols = len(cost_map[0])
    distance = {}
    for r in range(rows):
        for c in range(cols):
            distance[(r, c)] = INF
    distance[start] = 0
    settled = set()
    order = []                                # 確定した順の (マス, 秒数)
    queue = [(0, start)]
    while len(queue) > 0:
        total, current = heapq.heappop(queue)
        if current in settled:
            continue
        settled.add(current)
        order.append((current, total))
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            new_total = total + cost_map[nr][nc]      # となりのマスに入る秒数を足す（グラフの「辺の重み」にあたる）
            if new_total < distance[(nr, nc)]:
                distance[(nr, nc)] = new_total
                heapq.heappush(queue, (new_total, (nr, nc)))
    return distance, order


distance, order = dijkstra_all(cost_map, start)

print("確定した順番（秒数の小さいマスから順に決まっていく）")
print("-" * 60)
line = ""
for i, (cell, total) in enumerate(order):     # enumerate で、何番目か（i）と中身を同時に取り出す
    line = line + f"{str(cell) + '=' + str(total) + '秒':<14}"
    if (i + 1) % 4 == 0:
        print("  " + line)
        line = ""
if line != "":
    print("  " + line)
print("-" * 60)
print()
print("スタート (0,0) から各マスまでの最小の秒数（時間マップ）")
for r in range(len(cost_map)):
    line = ""
    for c in range(len(cost_map[0])):
        line = line + f"{distance[(r, c)]:>5}"
    print("  " + line)
print()

# ---- 迷路を大きくして、かかる時間を測る ----
# マスの秒数は 1, 1, 1, 5, 9 からでたらめに選ぶ（random.seed で、毎回同じでたらめにする）
print("迷路を大きくしたときに、ダイクストラ法にかかる時間（パソコンによって変わる）")
print("-" * 52)
print("   大きさ       マスの数      かかった時間   前の何倍")
random.seed(7)
before = None
for size in [50, 100, 200, 400]:
    big_map = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(random.choice([1, 1, 1, 5, 9]))
        big_map.append(row)
    begin = time.perf_counter()               # 測りはじめの時刻（秒）
    dijkstra_all(big_map, (0, 0))
    seconds = time.perf_counter() - begin     # 終わった時刻 − はじめの時刻 = かかった時間
    times = "" if before is None else f"{seconds / before:.1f}倍"
    print(f"  {size:>3}×{size:<3}   {size * size:>9,}マス   {seconds:>10.3f}秒   {times:>6}")
    before = seconds
print("-" * 52)
print("マスの数が4倍になると、時間もだいたい4倍（少し多め）になる")


# ============================================================
# ここから下は、時間マップを pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1マス確定   R = 最初から   Esc = 終わる
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

BAND_COLORS = [(46, 110, 40), (96, 140, 20), (150, 140, 10), (170, 100, 20), (160, 60, 40), (120, 40, 90), (70, 60, 130)]


def _band(minutes, bands):
    """minutes が bands の何番目の区切りに入るか（どれにも入らなければ最後の次）。"""
    for i, (limit, _) in enumerate(bands):
        if minutes <= limit:
            return i
    return len(bands)


def show_window(grid, labels, order, bands, title, unit, legend):
    """ダイクストラ法でマスが確定していく順に、時間の区切りごとの色でぬっていく（時間マップ）。窓を閉じると終わる。
    order = [(マス, 時間), ...] 確定した順、bands = [(この時間まで, 名前), ...]"""
    pygame.init()
    rows, cols = len(grid), len(grid[0])
    cell = max(18, min(52, 520 // cols, 470 // rows))
    width = 30 + 22 + cols * cell + 40 + 420
    height = max(70 + rows * cell + 70, 70 + 60 + 52 + 32 * (len(bands) + 1) + 10 + 24 * len(legend) + 50)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names = [name for _, name in bands] + ["それより遠い"]
    last_step = len(order)
    gx, gy = 52, 70
    x0 = gx + cols * cell + 40

    def draw(k):
        shown = order[:k]
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        for c in range(cols):
            t = small.render(str(c), True, SUB)
            screen.blit(t, (gx + c * cell + cell // 2 - t.get_width() // 2, gy - 20))
        for r in range(rows):
            t = small.render(str(r), True, SUB)
            screen.blit(t, (30, gy + r * cell + cell // 2 - t.get_height() // 2))
        _draw_cells(screen, fonts, grid, labels, gx, gy, cell)
        count = [0] * len(names)
        for (r, c), v in shown:
            b = _band(v, bands)
            count[b] += 1
            rect = pygame.Rect(gx + c * cell + 1, gy + r * cell + 1, cell - 2, cell - 2)
            pygame.draw.rect(screen, BAND_COLORS[b % len(BAND_COLORS)], rect, border_radius=5)
            if (r, c) in labels:
                screen.blit(small.render(labels[(r, c)], True, WHITE), (rect.x + 3, rect.y + 1))
            elif grid[r][c] > 1 and cell >= 30:      # 人ごみやパレードのマスは、入る時間を左上に残す
                screen.blit(small.render(str(grid[r][c]), True, (255, 200, 200)), (rect.x + 3, rect.y + 1))
            if cell >= 24:
                _number(screen, mid if cell >= 34 else small, str(v), rect, TEXT)
        if shown and k < last_step:
            (r, c), v = shown[-1]
            rect = pygame.Rect(gx + c * cell + 1, gy + r * cell + 1, cell - 2, cell - 2)
            pygame.draw.rect(screen, WHITE, rect, width=4, border_radius=5)
        # 右がわ: いまの手順と、色の区切りの表
        y = gy - 4
        if k == 0:
            lines = [("スペースで開始／→で1マス確定", TEXT)]
        elif k < last_step:
            (r, c), v = shown[-1]
            lines = [(f"{k}マス目の確定: ({r},{c}) = {v}{unit}", TEXT),
                     (f"いままででいちばん遠いのは {v}{unit}", SUB)]
        else:
            (r, c), v = order[-1]
            lines = [(f"全部で {len(order)}マス 確定した", TEXT),
                     (f"いちばん遠いマス: ({r},{c}) = {v}{unit}", AMBER)]
        for text, color in lines:
            screen.blit(mid.render(_fit(mid, text, 400), True, color), (x0, y))
            y += 30
        y += 16
        screen.blit(big.render("時間の区切り（色）", True, GREEN), (x0, y))
        y += 36
        lower = 0
        for i, name in enumerate(names):
            box = pygame.Rect(x0, y, 30, 24)
            pygame.draw.rect(screen, BAND_COLORS[i % len(BAND_COLORS)], box, border_radius=5)
            if i < len(bands):
                rng = f"{lower}〜{bands[i][0]}{unit}"
                lower = bands[i][0] + 1
            else:
                rng = f"{lower}{unit}〜"
            screen.blit(small.render(_fit(small, f"{rng}  {name}", 300), True, TEXT), (x0 + 40, y + 3))
            t = small.render(f"{count[i]}マス", True, SUB)
            screen.blit(t, (x0 + 400 - t.get_width(), y + 3))
            y += 32
        y += 10
        for text in legend:
            screen.blit(small.render(_fit(small, text, 410), True, SUB), (x0, y))
            y += 24

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1マス確定   R: 最初から   Esc: 終わる")


# --- 窓を開いて、マスが確定する順に、時間の区切りの色でぬっていく ---
show_window(cost_map, {start: "S"}, order, bands, "すべてのマスへの最小の秒数（時間マップ）", "秒", [
    "マスの数字 = スタートからの最小の秒数",
    "同じ色のマス = 同じくらいの秒数で着くマス（等高線）",
    "白い枠 = いま確定したマス",
])
