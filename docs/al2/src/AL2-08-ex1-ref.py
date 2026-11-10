# 第8回 例題1（参考）: 都市の位置（座標）から、2都市のあいだの距離の表（距離行列）を作る
# 巡回セールスマン問題を解く前の準備。表ができれば、どんな順番で回っても合計距離を足し算だけで出せる。
import math

# 都市の名前と位置 (名前, x, y)。左上が (0, 0)、右へ x、下へ y がふえる
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
]

n = len(cities)               # 都市の数

print("都市の位置")
print("-" * 34)
for i in range(n):
    name, x, y = cities[i]
    print(f"  {i} = {name}: (x={x}, y={y})")
print("-" * 34)
print()


def straight_distance(a, b):
    """都市 a と都市 b のあいだの直線距離（三平方の定理）。小数第1位までに丸める"""
    dx = a[1] - b[1]                  # よこの差
    dy = a[2] - b[2]                  # たての差
    return round(math.sqrt(dx ** 2 + dy ** 2), 1)


# ---- 距離の表を作る: distance[i][j] = i番の都市から j番の都市までの距離 ----
#   はじめは全部 0 の n行n列の表を用意し、i < j の組だけ計算して、[i][j] と [j][i] の両方に入れる
#   （行きと帰りは同じ距離なので、半分だけ計算すればよい）
distance = []
for i in range(n):
    distance.append([0] * n)
pairs = []                            # 計算した順の組 (i, j)。窓の表示に使う
for i in range(n):
    for j in range(i + 1, n):
        d = straight_distance(cities[i], cities[j])
        distance[i][j] = d
        distance[j][i] = d
        pairs.append((i, j))

print("距離の表（距離行列）")
print("-" * 46)
# 表を見やすくそろえて表示する（{j:>7} は「7文字の幅で右にそろえる」という書き方）
line = "      "
for j in range(n):
    line = line + f"{j:>7}"          # いちばん上の行: 列の番号
print(line)
for i in range(n):
    line = f"  {i}   "                 # 行の番号
    for j in range(n):
        line = line + f"{distance[i][j]:>7}"
    print(line)
print("-" * 46)
print(f"計算した組: {len(pairs)}組（{n} × {n - 1} ÷ 2）  表のマス: {n * n}マス")
print()
print("読み方: 0行1列 =", distance[0][1], "→", cities[0][0], "から", cities[1][0], "までの距離")
print("ななめの線（自分自身との距離）はすべて 0")
print("ななめをはさんで左右対称（行きと帰りが同じ距離だから）")

# いちばん近い組と、いちばん遠い組をさがす
near = pairs[0]
far = pairs[0]
for i, j in pairs:
    if distance[i][j] < distance[near[0]][near[1]]:
        near = (i, j)
    if distance[i][j] > distance[far[0]][far[1]]:
        far = (i, j)
print()
print(f"いちばん近い: {cities[near[0]][0]} と {cities[near[1]][0]}（{distance[near[0]][near[1]]}）")
print(f"いちばん遠い: {cities[far[0]][0]} と {cities[far[1]][0]}（{distance[far[0]][far[1]]}）")


# ============================================================
# ここから下は、地図と計算の進み方を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

STEP_MS = 420                   # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
PANEL = (28, 29, 38)
LINE = (70, 74, 92)
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


def _fit(font, text, width):
    """text が width ピクセルに収まらなければ、後ろを「…」にして縮める。"""
    if font.size(text)[0] <= width:
        return text
    while text and font.size(text + "…")[0] > width:
        text = text[:-1]
    return text + "…"


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


class _MapView:
    """地点の (x, y) を、窓の中の四角 (left, top, w, h) に収まるように置きかえる。"""

    def __init__(self, places, left, top, w, h):
        xs = [p[1] for p in places]
        ys = [p[2] for p in places]
        self.x0, self.y0 = min(xs), min(ys)
        self.scale = min((w - 80) / max(max(xs) - self.x0, 1), (h - 70) / max(max(ys) - self.y0, 1))
        self.left = left + 40 + ((w - 80) - (max(xs) - self.x0) * self.scale) / 2
        self.top = top + 40 + ((h - 70) - (max(ys) - self.y0) * self.scale) / 2
        self.rect = pygame.Rect(left, top, w, h)

    def pos(self, place):
        return (int(self.left + (place[1] - self.x0) * self.scale),
                int(self.top + (place[2] - self.y0) * self.scale))


def _draw_places(screen, fonts, view, places, marks=None):
    """地図の背景と、地点の丸・番号・名前を描く。0番（出発）は橙。marks = {番号: 丸の中に書く文字}"""
    pygame.draw.rect(screen, PANEL, view.rect, border_radius=10)
    _draw_places_again(screen, fonts, view, places, marks)


def _draw_tour(screen, view, places, tour, color, width):
    """0番 → tour の順 → 0番 の線を引く。"""
    route = [0] + list(tour) + [0]
    for a, b in zip(route, route[1:]):
        pygame.draw.line(screen, color, view.pos(places[a]), view.pos(places[b]), width)


def _draw_places_again(screen, fonts, view, places, marks):
    """線の上に、地点の丸と名前をもう一度描く（線に名前が隠れないように）。"""
    _, mid, small = fonts
    for i, place in enumerate(places):
        x, y = view.pos(place)
        pygame.draw.circle(screen, (26, 26, 26), (x, y), 15)
        pygame.draw.circle(screen, AMBER if i == 0 else GREEN, (x, y), 15, 3)
        t = mid.render((marks or {}).get(i, str(i)), True, TEXT)
        screen.blit(t, (x - t.get_width() // 2, y - t.get_height() // 2 + 2))
        name = small.render(_fit(small, place[0], 210), True, SUB)
        ny = y - 36 if y - 36 > view.rect.top + 4 else y + 18
        nx = min(max(x - name.get_width() // 2, view.rect.left + 4), view.rect.right - name.get_width() - 4)
        back = pygame.Rect(nx - 3, ny, name.get_width() + 6, name.get_height())
        pygame.draw.rect(screen, PANEL, back, border_radius=4)
        screen.blit(name, (nx, ny))


def show_window(places, table, pairs, title, unit, header):
    """左に地図、右に距離の表を出し、2地点の組を1つずつ計算して表を埋めていく様子を表示する。
    pairs = [(i, j), ...] 計算した順の組（i < j）。表は [i][j] と [j][i] の2か所に同時に入る。"""
    pygame.init()
    n = len(places)
    cell_w, cell_h = max(46, min(70, 460 // (n + 1))), 34
    table_w = max(470, 40 + (n + 1) * cell_w)
    map_w, map_h = 470, 430
    width = 30 + map_w + 30 + table_w + 30
    height = 66 + max(map_h, 40 + (n + 1) * cell_h + 120) + 60 + 22 * ((n + 1) // 2)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    view = _MapView(places, 30, 66, map_w, map_h)
    last_step = len(pairs)

    def draw(k):
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        _draw_places(screen, fonts, view, places)
        done = pairs[:k]
        for (i, j) in done:
            a, b = view.pos(places[i]), view.pos(places[j])
            now = (i, j) == done[-1] and k < last_step
            pygame.draw.line(screen, WHITE if now else LINE, a, b, 4 if now else 2)
            t = small.render(f"{table[i][j]}", True, WHITE if now else SUB)
            lx = int(a[0] + (b[0] - a[0]) * 0.4)        # 線の4割の所に数字を書く（交わる線の数字が重ならないように）
            ly = int(a[1] + (b[1] - a[1]) * 0.4)
            back = pygame.Rect(lx - t.get_width() // 2 - 3, ly - t.get_height() // 2, t.get_width() + 6, t.get_height())
            pygame.draw.rect(screen, PANEL, back, border_radius=4)
            screen.blit(t, (back.x + 3, back.y + 1))
        _draw_places_again(screen, fonts, view, places, None)     # 線の上に丸をもう一度描く
        # 右: 距離の表
        tx, ty = 30 + map_w + 30, 66
        screen.blit(mid.render(header, True, TEXT), (tx, ty))
        gy = ty + 40
        filled = set()
        for (i, j) in done:
            filled.add((i, j))
            filled.add((j, i))
        for c in range(n):
            t = mid.render(str(c), True, SUB)
            screen.blit(t, (tx + 40 + (c + 1) * cell_w - cell_w // 2 - t.get_width() // 2, gy))
        for r in range(n):
            y = gy + (r + 1) * cell_h
            t = mid.render(str(r), True, SUB)
            screen.blit(t, (tx + 40 + cell_w // 2 - t.get_width() // 2 - 20, y + 6))
            for c in range(n):
                rect = pygame.Rect(tx + 40 + c * cell_w + cell_w // 2, y, cell_w - 4, cell_h - 4)
                now = k < last_step and k > 0 and (min(r, c), max(r, c)) == done[-1]
                if r == c:
                    pygame.draw.rect(screen, (40, 40, 48), rect, border_radius=4)
                    t = small.render("0", True, SUB)
                elif (r, c) in filled:
                    pygame.draw.rect(screen, (34, 52, 20) if not now else (70, 70, 40), rect, border_radius=4)
                    t = small.render(f"{table[r][c]}", True, WHITE if now else TEXT)
                else:
                    pygame.draw.rect(screen, PANEL, rect, border_radius=4)
                    t = small.render("?", True, LINE)
                if now:
                    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=4)
                screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2 + 2))
        iy = gy + (n + 1) * cell_h + 16
        if k == 0:
            info = "スペースで開始／→で1手順"
            note = f"{n}地点 → 計算する組は {n} × {n - 1} ÷ 2 = {len(pairs)}組"
        elif k < last_step:
            i, j = done[-1]
            info = f"手順{k}  {i}番 と {j}番 のあいだ = {table[i][j]}{unit}"
            note = f"表の [{i}][{j}] と [{j}][{i}] に同じ数が入る（行きと帰りは同じ）"
        else:
            info = f"表ができた！ {len(pairs)}組を計算して、{n * n}マスが埋まった"
            note = "ななめは 0（自分自身）、ななめをはさんで左右対称"
        screen.blit(mid.render(_fit(mid, info, table_w), True, TEXT), (tx, iy))
        screen.blit(small.render(_fit(small, note, table_w), True, SUB), (tx, iy + 30))
        ly = 66 + map_h + 16
        for i, place in enumerate(places):
            col, row = i % 2, i // 2
            t = small.render(_fit(small, f"{i} = {place[0]}", 228), True, AMBER if i == 0 else SUB)
            screen.blit(t, (30 + col * 240, ly + row * 22))

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、2都市の組を1つずつ計算して表を埋めていく様子をアニメーション表示する ---
# 左 = 都市の地図（線の数字 = 2都市のあいだの距離）、右 = 距離の表（? = まだ計算していないマス）
show_window(cities, distance, pairs, "5都市の距離の表を作る", "", "距離の表（距離行列）")
