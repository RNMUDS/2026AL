# 第9回 例題1（参考）: 貪欲法（どんよくほう）で、巡回セールスマン問題の「そこそこ短いルート」をすばやく作る
# 作戦は1つだけ: 「いまいる都市から、まだ行っていない都市のうち、いちばん近い都市へ進む」をくり返す。
# 最後に、第8回の全探索の答え（本当の最短）と比べる。
import math
from itertools import permutations

# 都市の名前と位置 (名前, x, y)。第8回と同じ5都市
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
]

n = len(cities)               # 都市の数


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


def greedy(table, start):
    """貪欲法。start 番を出発し、いちばん近い都市へ進むことをくり返す。回る順番・合計距離・えらんだ記録を返す"""
    count = len(table)                # 都市の数
    visited = [start]                 # 行った都市の番号を、行った順に入れるリスト（はじめは出発点だけ）
    total = 0                         # ここまでに進んだ距離の合計
    here = start                      # いまいる都市
    steps = []                        # えらんだ記録 (いまいる都市, 候補の一覧, えらんだ都市)。表示に使う
    while len(visited) < count:       # まだ行っていない都市がある間、くり返す
        nearest = None                # 候補の中で、いまのところいちばん近い都市（まだないので None）
        candidates = []               # 候補 = まだ行っていない都市
        for j in range(count):
            if j in visited:          # もう行った都市は、候補にしない
                continue
            candidates.append(j)
            if nearest is None or table[here][j] < table[here][nearest]:
                nearest = j           # これまでの候補より近ければ、書きかえる
                                      # （同じ近さなら書きかえない。先に見つけた、番号の小さいほうのまま）
        steps.append((here, candidates, nearest))
        total = total + table[here][nearest]
        visited.append(nearest)       # えらんだ都市を「行った」に足して
        here = nearest                # そこへ移動する
    total = total + table[here][start]              # 最後に出発点へ戻る
    return visited, round(total, 1), steps


def brute_force(table):
    """全探索（第8回と同じ）。0番を出発する順番をすべて試して、いちばん短い順番と合計距離を返す"""
    best_order = None
    best_length = None
    for order in permutations(range(1, len(table))):
        total = 0
        here = 0
        for city in order:
            total = total + table[here][city]
            here = city
        total = total + table[here][0]
        if best_length is None or total < best_length:
            best_length = total
            best_order = order
    return [0] + list(best_order), round(best_length, 1)


def route_name(route):
    """回る順番を「学校 → 公園 → … → 学校」という文字列にする（最後に出発点を足す）"""
    names = []
    for city in route:
        names.append(cities[city][0])
    names.append(cities[route[0]][0])
    return " → ".join(names)


distance = make_table(cities)

# ---- 貪欲法で回る ----
route, length, steps = greedy(distance, 0)
print("貪欲法の進み方（[ ] の中 = まだ行っていない都市と、そこまでの距離）")
print("-" * 72)
looked = 0                            # 調べた候補の数（のべ）
for k in range(len(steps)):
    here, candidates, nearest = steps[k]
    text = ""
    for j in candidates:
        text = text + f"{cities[j][0]} {distance[here][j]}  "
    looked = looked + len(candidates)
    print(f"  {k + 1}回目: {cities[here][0]} にいる  [ {text}] → いちばん近い {cities[nearest][0]} へ")
last = route[-1]                      # 最後に行った都市（route[-1] は「リストのいちばん後ろ」）
print(f"  最後  : {cities[last][0]} から、出発点の {cities[0][0]} へ戻る（{distance[last][0]}）")
print("-" * 72)
print("貪欲法の答え")
print(" ", route_name(route))
print("  合計距離:", length)
print()

# ---- 全探索の答え（本当の最短）と比べる ----
best_route, best_length = brute_force(distance)
print("全探索の答え（本当の最短）")
print(" ", route_name(best_route))
print("  合計距離:", best_length)
print()
print("差:", round(length - best_length, 1))
# [1:] は「1番目から後ろ」（出発点の0番をのぞいた並び）、reversed は「並びを逆にする」
if best_route[1:] == list(reversed(route[1:])):
    print("（2つのルートは逆回り。同じ輪を反対向きに回っているだけなので、合計は同じになる）")
print(f"貪欲法: えらんだのは {len(steps)}回（調べた候補は、のべ {looked}か所）")
print(f"全探索: 試した順番は {math.factorial(n - 1)}通り（1通りごとに {n}本の道を足し算）")


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


def show_window(places, table, steps, route, total, title, unit):
    """左に地図、右に候補の一覧を出し、貪欲法が「いちばん近い地点」を1つずつえらぶ様子を表示する。
    steps = [(いまいる地点, 候補の一覧, えらんだ地点), ...]  route = 回る順番  total = 合計"""
    pygame.init()
    n = len(places)
    start = route[0]
    map_w = 500
    map_h = max(440, 60 + 22 * (n + 2))            # 地点が多いときは、右の一覧に合わせて地図もたてに広げる
    list_w = 440
    width = 30 + map_w + 30 + list_w + 30
    height = 66 + map_h + 60 + 22 * ((n + 3) // 4) + 40
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    view = _MapView(places, 30, 66, map_w, map_h)
    last_step = len(steps) + 1                     # 最後の1手順 = 出発点へ戻る

    def draw(k):
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        _draw_panel(screen, view)
        tx, ty = 30 + map_w + 30, 66
        by = 66 + map_h + 14
        if k == 0:
            _draw_places(screen, fonts, view, places, None, start)
            screen.blit(mid.render("スペースで開始／→で1手順", True, TEXT), (tx, ty))
            screen.blit(small.render(f"{n}地点 → 「いちばん近い地点」をえらぶのは {n - 1}回", True, SUB), (tx, ty + 32))
            info = f"橙の丸 = 出発点（{places[start][0]}）"
        elif k < last_step:
            here, candidates, nearest = steps[k - 1]
            for j in candidates:                    # いまいる地点から、候補へのうすい線と数字
                a, b = view.pos(places[here]), view.pos(places[j])
                chosen = j == nearest
                pygame.draw.line(screen, WHITE if chosen else LINE, a, b, 4 if chosen else 2)
                t = small.render(f"{table[here][j]}", True, WHITE if chosen else SUB)
                lx, ly = int(a[0] + (b[0] - a[0]) * 0.55), int(a[1] + (b[1] - a[1]) * 0.55)
                back = pygame.Rect(lx - t.get_width() // 2 - 3, ly - t.get_height() // 2, t.get_width() + 6, t.get_height())
                pygame.draw.rect(screen, PANEL, back, border_radius=4)
                screen.blit(t, (back.x + 3, back.y + 1))
            _draw_route(screen, view, places, route, k - 1, GREEN, 6)
            _draw_places(screen, fonts, view, places, None, start)
            pygame.draw.circle(screen, WHITE, view.pos(places[here]), 21, 3)      # いまいる地点を白い輪でかこむ
            screen.blit(mid.render(_fit(mid, f"{k}回目: いま {here}番（{places[here][0]}）にいる", list_w), True, TEXT), (tx, ty))
            screen.blit(small.render("まだ行っていない地点（候補）と、そこまでの" + ("歩く時間" if unit else "距離"), True, SUB), (tx, ty + 32))
            for row, j in enumerate(candidates):
                text = f"{j}番  {places[j][0]}"
                value = f"{table[here][j]}{unit}" + ("  ← いちばん近い" if j == nearest else "")
                color = GREEN if j == nearest else TEXT
                screen.blit(small.render(_fit(small, text, 230), True, color), (tx + 8, ty + 62 + row * 22))
                screen.blit(small.render(value, True, color), (tx + 250, ty + 62 + row * 22))
            went = " → ".join(str(p) for p in route[:k])
            screen.blit(small.render(_fit(small, f"行った順（visited）: {went}", list_w), True, SUB),
                        (tx, ty + 62 + len(candidates) * 22 + 12))
            info = f"白い線 = えらんだ道（{places[here][0]} → {places[nearest][0]}  {table[here][nearest]}{unit}）　太い緑 = ここまでに通った道"
        else:
            _draw_route(screen, view, places, route, n, GREEN, 6)
            _draw_places(screen, fonts, view, places, _order_marks(route), start)
            screen.blit(mid.render(f"貪欲法のルートができた！ 合計 {total}{unit}", True, GREEN), (tx, ty))
            loop = list(route) + [route[0]]
            for row in range(n):
                a, b = loop[row], loop[row + 1]
                text = f"{places[a][0]} → {places[b][0]}"
                screen.blit(small.render(_fit(small, text, 330), True, TEXT), (tx + 8, ty + 40 + row * 22))
                screen.blit(small.render(f"{table[a][b]}{unit}", True, TEXT), (tx + 350, ty + 40 + row * 22))
            screen.blit(small.render(_fit(small, "最後の1本は、出発点へ戻る道（えらべないので、遠くても行く）", list_w), True, AMBER),
                        (tx, ty + 40 + n * 22 + 10))
            info = "丸の数字 = 回る順番（S から 1, 2, … と回って S へ戻る）"
        screen.blit(mid.render(_fit(mid, info, width - 60), True, TEXT), (30, by))
        if k < last_step:
            _draw_legend(screen, fonts, places, start, by + 36, 4)

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、貪欲法が「いちばん近い都市」を1つずつえらぶ様子をアニメーション表示する ---
# 左 = 地図（白い線 = えらんだ道、うすい線 = ほかの候補）、右 = いまいる都市から候補までの距離
show_window(cities, distance, steps, route, length, "貪欲法: いちばん近い都市へ進むことをくり返す", "")
