# 第9回 例題2（参考）: 都市を8個に増やして、貪欲法と全探索を「答えの良さ」と「速さ」で比べる
# 後半では、出発する都市を変えると貪欲法の答えがどう変わるかを調べる。
import math
import time
from itertools import permutations

# 都市の名前と位置 (名前, x, y)。例題1の5都市に、駅・病院・書店を足した8都市
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
    ("駅", 17, 4),
    ("病院", 12, 13),
    ("書店", 8, 7),
]

n = len(cities)               # 都市の数


def make_table(places):
    """例題1と同じ距離の表を作る。table[i][j] = i番から j番までの直線距離（小数第1位まで）"""
    table = []
    for i in range(len(places)):
        row = []
        for j in range(len(places)):
            dx = places[i][1] - places[j][1]
            dy = places[i][2] - places[j][2]
            row.append(round(math.sqrt(dx ** 2 + dy ** 2), 1))
        table.append(row)
    return table


def greedy(table, start):
    """貪欲法（例題1と同じ。表示用の記録 steps だけ省いた）。回る順番と合計距離を返す"""
    count = len(table)
    visited = [start]                 # 行った都市の番号を、行った順に入れるリスト
    total = 0
    here = start                      # いまいる都市
    while len(visited) < count:       # まだ行っていない都市がある間、くり返す
        nearest = None
        for j in range(count):
            if j in visited:          # もう行った都市は、候補にしない
                continue
            if nearest is None or table[here][j] < table[here][nearest]:
                nearest = j           # これまでの候補より近ければ、書きかえる
                                      # （同じ近さなら書きかえない。先に見つけた、番号の小さいほうのまま）
        total = total + table[here][nearest]
        visited.append(nearest)
        here = nearest
    total = total + table[here][start]              # 最後に出発点へ戻る
    return visited, round(total, 1)


def brute_force(table):
    """全探索（第8回と同じ）。いちばん短い順番・合計距離・試した順番の数を返す"""
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

# ---- 2つの方法で解いて、かかった時間を測る（time.perf_counter() は、いまの時刻を秒で返す）----
begin = time.perf_counter()
greedy_route, greedy_length = greedy(distance, 0)
greedy_seconds = time.perf_counter() - begin

begin = time.perf_counter()
best_route, best_length, tried = brute_force(distance)
brute_seconds = time.perf_counter() - begin

print(f"{n}つの都市で、貪欲法と全探索を比べる")
print("-" * 66)
print("貪欲法")
print(" ", route_name(greedy_route))
print(f"  合計距離: {greedy_length}   かかった時間: {greedy_seconds:.6f}秒")
print()
print("全探索（本当の最短）")
print(" ", route_name(best_route))
print(f"  合計距離: {best_length}   かかった時間: {brute_seconds:.6f}秒")
print(f"  試した順番の数: {tried:,}通り")
print("-" * 66)
difference = round(greedy_length - best_length, 1)
percent = round(difference / best_length * 100, 1)       # 差が、最短の何%にあたるか
print(f"距離の差: {difference}（貪欲法は、本当の最短より {percent}% 長い）")
print(f"速さの差: 貪欲法は、全探索の 約{brute_seconds / greedy_seconds:,.0f}倍 速い（倍率はパソコンや実行のたびに変わる）")
print()

# ---- 出発する都市を変えて、貪欲法をやり直す ----
#   全探索の答えは「輪」なので、どこから出発しても合計は同じ。貪欲法は、出発点でえらび方が変わる
print("出発する都市を変えると、貪欲法の答えはどう変わるか")
print("-" * 46)
for start in range(n):
    route, length = greedy(distance, start)
    late = round(length - best_length, 1)
    mark = "  ← 本当の最短と同じ" if late == 0 else ""
    print(f"  {cities[start][0]}から出発:  合計 {length:>5}   最短との差 {late:>5}" + mark)
print("-" * 46)
print("貪欲法は速いが、最短ルートを見つけるとはかぎらない。出発点しだいで答えが変わる。")


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


def show_window(places, greedy_route, greedy_total, best_route, best_total, title, unit):
    """左に貪欲法のルート、右に全探索のルート（本当の最短）を並べて表示する。
    左は1本ずつ線が増えていき、最後の手順で右に全探索の答えが出る。"""
    pygame.init()
    n = len(places)
    start = greedy_route[0]
    map_w, map_h = 450, 420
    width = 30 + map_w + 30 + map_w + 30
    height = 66 + 34 + map_h + 96 + 22 * ((n + 3) // 4) + 40
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    left = _MapView(places, 30, 100, map_w, map_h)
    right = _MapView(places, 30 + map_w + 30, 100, map_w, map_h)
    last_step = n + 1                              # n本の線を引いたあと、最後の1手順で全探索の答えを出す
    # 全探索のルートを、貪欲法と同じ出発点から始まるように並べなおす（同じ輪なので、合計は変わらない）
    at = list(best_route).index(start)
    best_from_start = list(best_route[at:]) + list(best_route[:at])

    def draw(k):
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        _draw_panel(screen, left)
        _draw_panel(screen, right)
        legs = min(k, n)
        _draw_route(screen, left, places, greedy_route, legs, AMBER, 5)
        finished = k >= last_step
        _draw_places(screen, fonts, left, places, _order_marks(greedy_route) if legs == n else None, start)
        head = f"貪欲法: 合計 {greedy_total}{unit}" if legs == n else f"貪欲法: {legs}本目まで"
        screen.blit(mid.render(head, True, AMBER), (30, 68))
        if finished:
            _draw_route(screen, right, places, best_from_start, n, GREEN, 5)
            _draw_places(screen, fonts, right, places, _order_marks(best_from_start), start)
            screen.blit(mid.render(f"全探索（本当の最短）: 合計 {best_total}{unit}", True, GREEN), (30 + map_w + 30, 68))
        else:
            _draw_places(screen, fonts, right, places, None, start)
            screen.blit(mid.render("全探索（本当の最短）: 最後に表示", True, SUB), (30 + map_w + 30, 68))
        by = 100 + map_h + 14
        if k == 0:
            info = "スペースで開始／→で1手順（左の地図に、貪欲法の線が1本ずつ増える）"
        elif not finished:
            loop = list(greedy_route) + [greedy_route[0]]
            a, b = loop[legs - 1], loop[legs]
            info = f"{legs}本目: {places[a][0]} → {places[b][0]}" + ("（出発点へ戻る）" if legs == n else "（いちばん近い所へ）")
        else:
            late = round(greedy_total - best_total, 1)
            if late > 0:
                info = f"貪欲法は、本当の最短より {late}{unit}（{round(late / best_total * 100, 1)}%）長い"
            else:
                info = "貪欲法が、たまたま本当の最短と同じになった（いつもそうなるとはかぎらない）"
        screen.blit(mid.render(_fit(mid, info, width - 60), True, TEXT), (30, by))
        if legs == n:
            note = "丸の数字 = 回る順番（S から 1, 2, … と回って S へ戻る）。逆回りは同じ道なので、同じ合計になる"
            screen.blit(small.render(_fit(small, note, width - 60), True, SUB), (30, by + 32))
        _draw_legend(screen, fonts, places, start, by + 60, 4)

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、貪欲法のルート（左）と全探索のルート（右）を並べて表示する ---
show_window(cities, greedy_route, greedy_length, best_route, best_length, "8都市: 貪欲法と全探索をくらべる", "")
