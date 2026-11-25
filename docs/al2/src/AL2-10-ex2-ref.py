# 第10回 例題2（参考）: 動的計画法（bitDP）で、巡回セールスマン問題の「本当の最短ルート」を求める
# 表 best[visited][here] に、「visited の都市を回り終えて、いま here にいる」ときのいちばん短い距離を書きこんでいく。
#   visited = 回った都市の集合を表す数（例題1の2進数）、here = いまいる都市の番号
# 同じマスに別の順番でたどり着いても、短いほうだけを残す。だから、全部の順番を試さなくてよい。
# 最後に、第8回の全探索の答えと比べる。
import math
from itertools import permutations

# 都市の名前と位置 (名前, x, y)。第8・9回と同じ5都市
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
]

n = len(cities)               # 都市の数
INF = float("inf")            # 無限大。「まだたどり着いていない」の印として表に入れておく（どんな数よりも大きい）


def make_table(places):
    """第8回と同じ距離の表を作る。table[i][j] = i番から j番までの直線距離（小数第1位まで）"""
    table = []
    for i in range(len(places)):
        row = []
        for j in range(len(places)):
            dx = places[i][1] - places[j][1]
            dy = places[i][2] - places[j][2]
            row.append(round(math.sqrt(dx ** 2 + dy ** 2), 1))
        table.append(row)
    return table


def bit_dp(table):
    """bitDP。0番を出発して全部の都市を回り、0番へ戻るいちばん短い順番・合計距離・表 best を返す"""
    count = len(table)                # 都市の数
    full = (1 << count) - 1           # 全部の都市を回った集合（5都市なら 11111 = 31）
    best = []                         # best[visited][here] = その状態までの、いちばん短い距離
    prev = []                         # prev[visited][here] = その状態へ、どの都市から来たか（あとで順番をたどるため）
    for visited in range(1 << count):             # 表を作る。行は 2のcount乗 個（集合の数）、列は count 個
        best.append([INF] * count)
        prev.append([None] * count)
    best[1 << 0][0] = 0               # はじめの状態: 0番だけ回って（00001）、0番にいる。距離は 0

    # 集合を表す数の、小さいほうから順に見る。都市を1つ足した集合は、いまより必ず大きい数になるので、
    # 小さい順に見れば、ある行を読むときには、その行の値はもう決まっている
    for visited in range(1 << count):
        for here in range(count):
            if best[visited][here] == INF:        # たどり着けない状態は飛ばす
                continue
            for next_city in range(count):        # ここから次に行く都市を、全部ためす
                if visited & (1 << next_city):    # もう回った都市へは行かない
                    continue
                new_visited = visited | (1 << next_city)          # next_city を足した集合
                new_length = best[visited][here] + table[here][next_city]
                if new_length < best[new_visited][next_city]:     # いま表にある値より短いときだけ、書きかえる
                    best[new_visited][next_city] = new_length
                    prev[new_visited][next_city] = here           # どこから来たかも覚えておく

    # 全部回った状態（full の行）のうち、0番へ戻る距離を足して、いちばん短くなるものをえらぶ
    answer = INF
    last = None                       # 最後に立ちよる都市
    for here in range(1, count):
        total = best[full][here] + table[here][0]
        if total < answer:
            answer = total
            last = here

    # prev を後ろから前へたどって、回る順番を作る
    route = []
    visited = full
    here = last
    while here is not None:           # 0番の prev は None なので、0番まで来たら終わる
        route.append(here)
        came_from = prev[visited][here]           # here へ来る前にいた都市
        visited = visited - (1 << here)           # here のけたを 0 にもどす（here を回る前の集合）
        here = came_from
    route.reverse()                   # 後ろからたどったので、前後を逆にする
    return route, round(answer, 1), best


def brute_force(table):
    """全探索（第8回と同じ）。0番を出発する順番をすべて試して、いちばん短い順番・合計距離・試した数を返す"""
    best_order = None
    best_length = None
    tried = 0
    for order in permutations(range(1, len(table))):
        total = 0
        here = 0
        for city in order:
            total = total + table[here][city]
            here = city
        total = total + table[here][0]
        tried = tried + 1
        if best_length is None or total < best_length:
            best_length = total
            best_order = order
    return [0] + list(best_order), round(best_length, 1), tried


def route_name(route):
    """回る順番を「学校 → 公園 → … → 学校」という文字列にする（最後に出発点を足す）"""
    names = []
    for city in route:
        names.append(cities[city][0])
    names.append(cities[route[0]][0])
    return " → ".join(names)


distance = make_table(cities)
route, length, best = bit_dp(distance)
full = (1 << n) - 1

# ---- 表の一部を表示する（都市を1つずつ足していった5つの行）----
print("bitDP の表の一部（visited = 回った都市の集合、here = いまいる都市）")
print("-" * 66)
header = "  visited      "
for here in range(n):
    header = header + f"here={here}   "
print(header)
for visited in [1, 3, 7, 15, 31]:
    line = f"   {format(visited, '05b')}       "
    for here in range(n):
        value = best[visited][here]
        if value == INF:
            line = line + "     -   "
        else:
            line = line + f"{value:>6.1f}   "
    print(line)
print("-" * 66)
print("「-」は、たどり着けない状態（here が visited に入っていない、など）")
print()

# ---- 最後の行（11111）から、答えを出す ----
print("全部回った行（11111）の値に、学校へ戻る距離を足す")
for here in range(1, n):
    total = round(best[full][here] + distance[here][0], 1)
    mark = "  ← いちばん短い" if total == length else ""
    print(f"  {best[full][here]:>5.1f} + {distance[here][0]:>5} = {total:>5}  （最後が {cities[here][0]}）" + mark)
print("  （同じ合計が2つあるのは、同じ輪を右回りと左回りに回った2つ。どちらも正しい）")
print()
print("bitDP の答え")
print(" ", route_name(route))
print("  合計距離:", length)
print()

# ---- 全探索の答えと比べる ----
brute_route, brute_length, tried = brute_force(distance)
print("全探索の答え（第8回）")
print(" ", route_name(brute_route))
print("  合計距離:", brute_length)
if length == brute_length:
    print("2つの合計は同じ。bitDP は、全探索と同じく、必ず最短を出す（回る向きが逆のことはある）")
print()

# ---- 調べる量を比べる ----
filled = 0                            # 値が入ったマスの数
for visited in range(1 << n):
    for here in range(n):
        if best[visited][here] != INF:
            filled = filled + 1
print(f"表のマスの数: {(1 << n) * n}個（2の{n}乗 × {n}）。そのうち値が入ったのは {filled}個（1マスごとに、次の都市を {n}通り ためす）")
print(f"全探索が試した順番: {tried}通り")
print()
print("都市を増やすと（表のマスの数 と 全探索の順番の数）")
print("-" * 52)
for count in [5, 10, 15, 20]:
    print(f"  {count:>2}都市:  表 {(1 << count) * count:>12,}個    順番 {math.factorial(count - 1):>26,}通り")
print("-" * 52)


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


def _draw_panel(screen, view):
    """地図の背景（角の丸い四角）を描く。"""
    pygame.draw.rect(screen, PANEL, view.rect, border_radius=10)


def _draw_route(screen, view, places, route, legs, color, width):
    """route の順に、最初の legs 本ぶんの線を引く（最後の1本は、出発点へ戻る線）。"""
    loop = list(route) + [route[0]]
    for k in range(min(legs, len(loop) - 1)):
        pygame.draw.line(screen, color, view.pos(places[loop[k]]), view.pos(places[loop[k + 1]]), width)


def _draw_places(screen, fonts, view, places, marks, start):
    """地点の丸・番号・名前を描く。出発点（start）は橙。marks = {番号: 丸の中に書く文字}"""
    _, mid, small = fonts
    for i, place in enumerate(places):
        x, y = view.pos(place)
        pygame.draw.circle(screen, (26, 26, 26), (x, y), 15)
        pygame.draw.circle(screen, AMBER if i == start else GREEN, (x, y), 15, 3)
        t = mid.render((marks or {}).get(i, str(i)), True, TEXT)
        screen.blit(t, (x - t.get_width() // 2, y - t.get_height() // 2 + 2))
        name = small.render(_fit(small, place[0], 190), True, SUB)
        ny = y - 36 if y - 36 > view.rect.top + 4 else y + 18
        nx = min(max(x - name.get_width() // 2, view.rect.left + 4), view.rect.right - name.get_width() - 4)
        back = pygame.Rect(nx - 3, ny, name.get_width() + 6, name.get_height())
        pygame.draw.rect(screen, PANEL, back, border_radius=4)
        screen.blit(name, (nx, ny))


def _order_marks(route):
    """回る順番を、丸の中に書く文字にする（出発点は S、あとは 1, 2, …）。"""
    marks = {route[0]: "S"}
    for k in range(1, len(route)):
        marks[route[k]] = str(k)
    return marks


def _draw_legend(screen, fonts, places, start, top, columns):
    """丸の数字（地点の番号）と名前の対応を、窓の下に並べる。"""
    small = fonts[2]
    for i, place in enumerate(places):
        col, row = i % columns, i // columns
        t = small.render(_fit(small, f"{i} = {place[0]}", 228), True, AMBER if i == start else SUB)
        screen.blit(t, (30 + col * 240, top + row * 22))



def show_window(places, best, route, total, title):
    """左に bitDP の表（行 = 回った集合、列 = いまいる都市）、右に地図を表示する。
    1手順ごとに「回った都市の数」が1つ多い行が埋まっていき、最後の手順で最短ルートが出る。"""
    pygame.init()
    n = len(places)
    rows = 1 << n
    row_h, col_w, label_w = 17, 70, 96
    table_w = label_w + col_w * n
    map_w, map_h = 430, 360
    top = 128
    width = 30 + table_w + 30 + map_w + 30
    height = top + row_h * rows + 22 * ((n + 3) // 4) + 64
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    tiny = _font(12)
    view = _MapView(places, 30 + table_w + 30, top - 22, map_w, map_h)
    last_step = n + 1                              # n 手順で表が全部埋まり、最後の1手順でルートを出す
    inf = float("inf")
    full = rows - 1
    # 全部回った行のうち、答えに使われたマス（ルートの最後の都市）
    final = route[-1]

    def draw(k):
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        size = min(k, n)                           # ここまでに埋まった「回った都市の数」
        if k == 0:
            info = "スペースで開始／→で1手順（回った都市の数が少ない行から、表が埋まっていく）"
        elif k <= n:
            count = sum(1 for v in range(rows) for h in range(n)
                        if bin(v).count("1") == k and best[v][h] != inf)
            info = f"{k}手順目: 都市を {k}個 回った状態（黄色い行）が決まった。値が入ったマスは {count}個"
        else:
            info = f"最後の行（全部回った）に、出発点へ戻る距離を足して、いちばん短いものが答え: 合計 {total}"
        screen.blit(mid.render(_fit(mid, info, width - 60), True, TEXT), (30, 58))
        # 表の見出し
        screen.blit(small.render("visited", True, SUB), (34, top - 22))
        for h in range(n):
            t = small.render(f"here={h}", True, AMBER if h == 0 else SUB)
            screen.blit(t, (30 + label_w + col_w * h + (col_w - t.get_width()) // 2, top - 22))
        for v in range(rows):
            y = top + v * row_h
            ones = bin(v).count("1")
            shown = 1 <= ones <= size and v & 1    # 0番をふくまない集合（偶数）は、ずっと使われない
            new = shown and ones == k
            if new:
                pygame.draw.rect(screen, (60, 52, 14), (30, y, table_w, row_h - 1))
            elif v % 2 == 0:
                pygame.draw.rect(screen, (22, 22, 29), (30, y, table_w, row_h - 1))
            color = TEXT if shown else LINE
            screen.blit(tiny.render(format(v, "0" + str(n) + "b"), True, AMBER if new else color), (38, y + 1))
            for h in range(n):
                value = best[v][h]
                if not shown or value == inf:
                    text, c = "-", LINE
                else:
                    text, c = f"{value:.1f}", (GREEN if (k > n and v == full and h == final) else TEXT)
                t = tiny.render(text, True, c)
                screen.blit(t, (30 + label_w + col_w * h + (col_w - t.get_width()) // 2, y + 1))
        pygame.draw.rect(screen, LINE, (30, top, table_w, row_h * rows), 1)
        # 地図
        _draw_panel(screen, view)
        if k > n:
            _draw_route(screen, view, places, route, n, GREEN, 5)
            _draw_places(screen, fonts, view, places, _order_marks(route), 0)
        else:
            _draw_places(screen, fonts, view, places, None, 0)
        nx = view.rect.left
        ny = view.rect.bottom + 14
        notes = ["表の読み方", "行 = 回った都市の集合（2進数。右はしが0番）", "列 = いまいる都市（here）",
                 "マスの数 = そこまでのいちばん短い距離", "「-」 = たどり着けない状態",
                 "0番（出発点）をふくまない行は、使われない"]
        for i, note in enumerate(notes):
            screen.blit(small.render(note, True, AMBER if i == 0 else SUB), (nx, ny + i * 22))
        if k > n:
            screen.blit(mid.render(f"最短ルート: 合計 {total}", True, GREEN), (nx, ny + len(notes) * 22 + 10))
        _draw_legend(screen, fonts, places, 0, top + row_h * rows + 12, 4)

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、bitDP の表が埋まっていくようすと、求めた最短ルートを表示する ---
show_window(cities, best, route, length, "bitDP: 表を埋めて、本当の最短ルートを求める")
