# 第8回 例題2（参考）: 全探索で、巡回セールスマン問題の最短ルートを求める
# 学校（0番）を出発し、残りの都市を1回ずつ回って学校へ戻る順番を「すべて」試して、いちばん短いものを選ぶ。
# 後半では、都市を増やすと試す順番の数と時間がどれくらい増えるかを測る。
import math
import time
from itertools import permutations

# 都市の名前と位置 (名前, x, y)。例題1と同じ5都市
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
]


def make_table(places):
    """例題1と同じ距離の表を作る（こちらは半分にせず、全部のマスを計算する）。distance[i][j] = i番から j番までの直線距離（小数第1位まで）"""
    n = len(places)
    table = []
    for i in range(n):
        row = []
        for j in range(n):
            dx = places[i][1] - places[j][1]
            dy = places[i][2] - places[j][2]
            row.append(round(math.sqrt(dx ** 2 + dy ** 2), 1))
        table.append(row)
    return table


def tour_length(order, table):
    """0番を出発し、order の順に回って0番へ戻るまでの合計距離"""
    total = 0
    here = 0                          # いまいる都市（はじめは0番）
    for city in order:
        total = total + table[here][city]
        here = city
    total = total + table[here][0]    # 最後に0番へ戻る
    return round(total, 1)


def tour_name(order, places):
    """ルートを「学校 → 郵便局 → … → 学校」という文字列にする"""
    names = [places[0][0]]
    for city in order:
        names.append(places[city][0])
    names.append(places[0][0])
    return " → ".join(names)


distance = make_table(cities)
n = len(cities)

# ---- 全探索: 0番以外の都市の並べ方を permutations ですべて作り、1つずつ合計距離を計算する ----
#   permutations([1, 2, 3, 4]) は (1,2,3,4) (1,2,4,3) … の 4×3×2×1 = 24通りを順に作る
print(f"{cities[0][0]}を出発して{n - 1}つの都市を回り、{cities[0][0]}へ戻る順番をすべて試す")
for i in range(n):
    print(f"  {i} = {cities[i][0]}")
print("下の ( ) の中の数 = 0番を出たあとに回る都市の番号を、回る順に並べたもの（最後に0番へ戻る）")
print("-" * 50)
best_order = None                     # いまのところ最短の順番
best_length = None                    # その合計距離
tried = []                            # 試した順の (順番, 合計距離)。窓の表示に使う
for order in permutations(range(1, n)):
    length = tour_length(order, distance)
    tried.append((order, length))
    mark = ""
    if best_length is None or length < best_length:
        best_length = length          # 記録を書きかえる
        best_order = order
        mark = "  ← いまのところ最短"
    print(f"  {order}  {length:>6}" + mark)
print("-" * 50)
print("試した順番の数:", len(tried), "通り")
print()
print("いちばん短いルート")
print(" ", tour_name(best_order, cities))
print("  合計距離:", best_length)
back = tuple(reversed(best_order))    # 順番を逆に並べる（逆回り）
print("逆回りのルート（同じ道を反対向きに回る）")
print(" ", tour_name(back, cities))
print("  合計距離:", tour_length(back, distance))
print()

# ---- 都市を増やして、全探索にかかる時間を測る ----
#   都市が n 個なら、試す順番は (n-1)! 通り（4! = 4×3×2×1 = 24 のような「階乗」）
more = cities + [("駅", 17, 4), ("病院", 12, 13), ("書店", 8, 7), ("市役所", 16, 1), ("体育館", 1, 13)]
print("都市の数   試す順番の数      かかった時間")
print("-" * 46)
for count in range(5, len(more) + 1):
    places = more[:count]
    table = make_table(places)
    begin = time.perf_counter()       # いまの時刻（秒）
    best = None
    for order in permutations(range(1, count)):
        length = tour_length(order, table)
        if best is None or length < best:
            best = length
    seconds = time.perf_counter() - begin
    print(f"  {count:>3}都市   {math.factorial(count - 1):>12,}通り   {seconds:>10.4f}秒")
print("-" * 46)
print("都市が1つ増えるたびに、時間が「増やしたあとの都市の数 − 1」倍くらいずつ増えていく（9都市→10都市なら約9倍。秒数はパソコンで変わる）")


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


def show_window(places, tried, best_tour, title, unit):
    """左に地図、右に試した順番の一覧を出し、全探索が順番を1つずつ試す様子を表示する。
    tried = [(順番, 合計), ...] 試した順。順番が多いときは、とびとびに表示する（いまのところ最短が変わった所は必ず出す）。"""
    pygame.init()
    n = len(places)
    map_w, map_h = 500, 440
    list_w = 440
    width = 30 + map_w + 30 + list_w + 30
    height = 66 + map_h + 100 + 22 * ((n + 3) // 4)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    view = _MapView(places, 30, 66, map_w, map_h)
    record = []                                    # その時点の「いまのところ最短」
    best = None
    for k, (tour, total) in enumerate(tried):
        if best is None or total < best[1]:
            best = (tour, total, k)
        record.append(best)
    every = max(1, len(tried) // 150)              # 多いときは、とびとびに表示する
    frames = sorted(set(range(0, len(tried), every)) | {r[2] for r in record} | {len(tried) - 1})
    last_step = len(frames) + 1                    # 最後の1手順 = 全部試し終わった画面

    def draw(k):
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        _draw_places(screen, fonts, view, places)
        tx, ty = 30 + map_w + 30, 66
        if k == 0:
            screen.blit(mid.render("スペースで開始／→で1手順", True, TEXT), (tx, ty))
            screen.blit(small.render(f"{n}地点 → 試す順番は {len(tried):,}通り", True, SUB), (tx, ty + 32))
            return
        finished = k >= last_step
        idx = len(tried) - 1 if finished else frames[k - 1]
        tour, total = tried[idx]
        b_tour, b_total, b_idx = record[idx]
        if finished:
            marks = {0: "S"}
            for pos, place in enumerate(best_tour):
                marks[place] = str(pos + 1)
            _draw_tour(screen, view, places, best_tour, GREEN, 6)
            _draw_places_again(screen, fonts, view, places, marks)
        else:
            _draw_tour(screen, view, places, b_tour, (60, 96, 20), 9)
            _draw_tour(screen, view, places, tour, AMBER, 3)
            _draw_places_again(screen, fonts, view, places, None)
        # 右: 試した順番の一覧（新しいものが下）
        screen.blit(mid.render(f"試した順番  {idx + 1:,} / {len(tried):,}通り", True, TEXT), (tx, ty))
        start = max(0, idx - 11)
        for row, j in enumerate(range(start, idx + 1)):
            t_tour, t_total = tried[j]
            text = "0→" + "→".join(str(p) for p in t_tour) + f"→0   {t_total}{unit}"
            is_rec = record[j][2] == j
            color = GREEN if is_rec else (TEXT if j == idx else SUB)
            line = small.render(_fit(small, text + ("  ← 最短を更新" if is_rec else ""), list_w), True, color)
            screen.blit(line, (tx, ty + 38 + row * 24))
        if finished:
            text = f"いちばん短い {b_total}{unit}（左の地図の S → 1 → 2 → … → S の順）"
            screen.blit(small.render(_fit(small, text, list_w), True, GREEN), (tx, ty + 38 + 12 * 24 + 10))
        by = 66 + map_h + 14
        if finished:
            info = f"全部試した！ いちばん短い順番 = {b_total}{unit}（丸の数字 = 回る順番。S から 1, 2, … と回って S へ戻る）"
        else:
            info = f"橙 = いま試している順番 {total}{unit}　　太い緑 = いまのところ最短 {b_total}{unit}"
        screen.blit(mid.render(_fit(mid, info, width - 60), True, TEXT), (30, by))
        if finished:                                # 最後の画面: 丸の数字（回る順番）と名前の対応
            legend = [f"S = {places[0][0]}"] + [f"{k + 1}番目 = {places[p][0]}" for k, p in enumerate(best_tour)]
        else:                                       # 途中の画面: 丸の数字（場所の番号）と名前の対応
            legend = [f"{i} = {place[0]}" for i, place in enumerate(places)]
        for i, text in enumerate(legend):
            col, row = i % 4, i // 4
            t = small.render(_fit(small, text, 228), True, AMBER if i == 0 else SUB)
            screen.blit(t, (30 + col * 240, by + 36 + row * 22))

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、全探索が5都市の24通りの順番を1つずつ試す様子をアニメーション表示する ---
# 橙の線 = いま試している順番、太い緑の線 = いまのところ最短。最後は最短ルートと回る順番（丸の数字）
show_window(cities, tried, best_order, "全探索: 5都市の24通りを1つずつ試す", "")
