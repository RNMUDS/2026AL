# 第7回 クリエイティブ演習2: 自分の園内マップの「時間マップ」を作り、園を大きくしたときの速さを測る
# 演習1の地図で、ダイクストラ法をゴールで止めずに最後まで動かし、エントランスから園内のすべてのマスへの時間を求める。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: park_map と COST を、演習1で作った自分のものに貼りかえる（G の時間が演習1のダイクストラ法と同じになるか確かめる）
#   Lv2: bands を書き換えて、4段階以上の時間マップにする（名前も自分の言葉で）
#   Lv3: SIZES に 64 を足して、園を 64×64 枚ぶんに広げたときの時間を測る。マスの数が4倍になると、時間は何倍になるかを見る
import heapq
import time

# ★ 窓のいちばん上に出る題名
TITLE = "エントランスから何分？ わたしの時間マップ"

# ★ 園内の地図（演習1と同じ書き方）。演習1で作った park_map = [ ... ] を、そのまま貼りかえてよい
park_map = [
    "G..~.....#.",
    ".#.~.###.#.",
    ".#...###...",
    ".##PPPPPPP#",
    "..~P.....P.",
    "#.~P.###.P.",
    "#..PPP.PPP.",
    "##~~...~~##",
    "##...S...##",
]

# ★ 記号ごとの時間（分）。演習1で記号を足した人は、ここにも同じ行を足す（COST = { ... } をまるごと貼りかえてよい）
COST = {
    ".": 1,     # ふつうの道
    "S": 1,     # エントランス
    "G": 1,     # 行きたい場所
    "~": 3,     # 人ごみ
    "P": 9,     # パレードのルート
}

# ★ 時間マップの色の区切り。(この時間まで, 名前) を、時間の小さい順に並べる
#   最後の区切りより遠いマスは「それより遠い」の色になる
bands = [
    (5, "すぐ着く"),
    (10, "ちょっと歩く"),
    (15, "けっこう遠い"),
]

# ★ 速さを測るときの広さ。地図をタイルのように縦横にならべる枚数で、4 = 4×4 枚、8 = 8×8 枚 …
#   ひな形の地図は1枚 99マスなので、4×4 枚 = 約1,600マス、32×32 枚 = 約10万マス（1 にすると地図そのまま）
SIZES = [4, 8, 16, 32]


# ------------------------------------------------------------
# ここから先は本体（書き換えずに読むだけ）。例題2（参考）と同じ「すべてのマスへの時間を求める」ダイクストラ法。
#   参考の cost_map[nr][nc] が、ここでは COST[the_map[nr][nc]] に変わり、# のマスへは進まない
# ------------------------------------------------------------

# 書きまちがいを先に見つける（演習1と同じ検査）
if len(park_map) == 0:
    raise SystemExit("park_map が空っぽ。演習1の park_map = [ ... ] を貼りかえよう")
for mark in COST:
    if type(COST[mark]) != int or COST[mark] < 0:
        raise SystemExit(f"COST の \"{mark}\" の時間がおかしい。時間は \" \" で囲まず、0 以上の整数（3 など）で書こう")
start = None
for r in range(len(park_map)):
    if len(park_map[r]) != len(park_map[0]):
        raise SystemExit(f"park_map の {r}行目（上から {r + 1}番目）の長さが {len(park_map[r])}文字で、"
                         f"0行目の {len(park_map[0])}文字とちがう。どの行も同じ文字数にしよう")
    for c in range(len(park_map[r])):
        mark = park_map[r][c]
        if mark in " 　":
            raise SystemExit(f"park_map の {r}行目（上から {r + 1}番目）に空白がまじっている。空白を消して . にしよう")
        if mark != "#" and mark not in COST:
            raise SystemExit(f"park_map の ({r},{c}) の「{mark}」が COST にない。演習1で足した記号の行を、COST にも足そう")
        if mark == "S":
            start = (r, c)
if start is None:
    raise SystemExit("park_map に S（エントランス）がない。演習1と同じ地図を貼ろう")
if "." not in COST:
    raise SystemExit("COST に \".\" の行がない。園を広げるときに S と G を . にするので、\".\": 1, の行を残そう")
if type(SIZES) != list or len(SIZES) == 0:
    raise SystemExit("SIZES は [4, 8, 16] のように [ ] で囲み、数を1つ以上書こう")
for i in range(len(bands)):
    if type(bands[i]) != tuple or len(bands[i]) != 2 or type(bands[i][0]) != int:
        raise SystemExit(f"bands の {bands[i]} がおかしい。(5, \"すぐ着く\") のように (時間, \"名前\") の組で書こう")
    if i > 0 and bands[i][0] <= bands[i - 1][0]:
        raise SystemExit(f"bands の {bands[i][0]} が、1つ前の {bands[i - 1][0]} より小さいか同じ。時間の小さい順に並べよう")
INF = float("inf")


def dijkstra_all(the_map, start):
    """start から the_map のすべてのマスへの最小の時間（距離表）と、確定した順番を返す。
    ゴールで止めずに、queue が空になるまで続ける"""
    rows = len(the_map)
    cols = len(the_map[0])
    distance = {}
    for r in range(rows):
        for c in range(cols):
            distance[(r, c)] = INF
    distance[start] = 0
    settled = set()
    order = []                                # 確定した順の (マス, 時間)
    queue = [(0, start)]
    while len(queue) > 0:
        total, current = heapq.heappop(queue)
        if current in settled:
            continue                          # 古い組は読み飛ばす
        settled.add(current)
        order.append((current, total))
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or the_map[nr][nc] == "#":
                continue
            new_total = total + COST[the_map[nr][nc]]   # となりのマスに入る時間を足す（グラフの「辺の重み」にあたる）
            if new_total < distance[(nr, nc)]:
                distance[(nr, nc)] = new_total
                heapq.heappush(queue, (new_total, (nr, nc)))
    return distance, order


def band_of(minutes):
    """minutes が bands の何番目の区切りに入るか（どれにも入らなければ len(bands)）"""
    for i in range(len(bands)):
        if minutes <= bands[i][0]:
            return i
    return len(bands)


distance, order = dijkstra_all(park_map, start)

print(f"{TITLE}（S からの最小の時間。# は建物、- は行けないマス）")
for r in range(len(park_map)):
    line = ""
    for c in range(len(park_map[0])):
        if park_map[r][c] == "#":
            line = line + "   #"
        elif distance[(r, c)] == INF:
            line = line + "   -"
        else:
            line = line + f"{distance[(r, c)]:>4}"
    print(" " + line)
print()
for r in range(len(park_map)):
    for c in range(len(park_map[0])):
        if park_map[r][c] == "G":
            if distance[(r, c)] == INF:
                print(f"G ({r},{c}) へは行けない（# でふさがっている）。演習1と同じ地図を貼ろう")
            else:
                print(f"G ({r},{c}) までの時間: {distance[(r, c)]}分（演習1のダイクストラ法と同じになるはず）")
far_cell, far_minutes = order[-1]             # いちばん最後に確定したマスが、いちばん遠い
print(f"いちばん遠いマス: {far_cell} = {far_minutes}分")
print()
count = [0] * (len(bands) + 1)
for cell, minutes in order:
    count[band_of(minutes)] += 1
lower = 0
for i in range(len(bands)):
    print(f"  {lower:>3}〜{bands[i][0]:>3}分  {count[i]:>4}マス  {bands[i][1]}")
    lower = bands[i][0] + 1
print(f"  {lower:>3}分〜      {count[len(bands)]:>4}マス  それより遠い")
print()

# ---- 園を広げて、かかる時間を測る ----
# 地図を n×n 枚ならべた大きな地図を作る（S と G は1枚目の S だけを使い、ほかは . にする）
print("園を広げたときに、ダイクストラ法にかかる時間（パソコンによって変わる）")
print("-" * 56)
print("       広さ      マスの数      かかった時間   前の何倍")
plain_map = []
for line in park_map:
    plain_map.append(line.replace("S", ".").replace("G", "."))   # 文字列.replace(a, b) で、a を b に置きかえる
before = None
for n in SIZES:
    if type(n) != int or n < 1:
        raise SystemExit(f"SIZES の {n} がおかしい。1 以上の整数で書こう")
    big_map = []
    for i in range(n):
        for line in plain_map:
            big_map.append(line * n)          # 文字列 * n で、横に n 枚ならべる
    begin = time.perf_counter()               # 測りはじめの時刻（秒）
    dijkstra_all(big_map, start)
    seconds = time.perf_counter() - begin     # 終わった時刻 − はじめの時刻 = かかった時間
    times = "" if before is None else f"{seconds / before:.1f}倍"
    cells = len(big_map) * len(big_map[0])
    print(f"  {str(n) + '×' + str(n) + '枚':>9}  {cells:>10,}マス   {seconds:>10.3f}秒   {times:>6}")
    before = seconds
print("-" * 56)
print("横の枚数が2倍になるたびに、マスの数は4倍になる。時間もだいたい4倍（少し多め）になる")


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


# --- 窓を開いて、マスが確定する順に、bands の色でぬっていく（自分の時間マップ） ---
labels = {}
for r in range(len(park_map)):
    for c in range(len(park_map[0])):
        if park_map[r][c] in "SG":
            labels[(r, c)] = park_map[r][c]
grid = [[None if mark == "#" else COST[mark] for mark in line] for line in park_map]
show_window(grid, labels, order, bands, TITLE, "分", [
    "マスの数字 = エントランス（S）からの最小の時間",
    "同じ色のマス = 同じくらいの時間で着くマス（等高線）",
    "白い枠 = いま確定したマス　灰色のブロック = 建物",
])
