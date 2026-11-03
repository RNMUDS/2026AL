# 第7回 クリエイティブ演習1: ディズニーランドの園内をマス目の地図にして、パレードをよける道をさがす
# 同じ地図を、幅優先探索（第2回）とダイクストラ法（第6回の heapq 版）の2つで解いて比べる。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: park_map を自分の地図にする（S と G は1つずつ。行の長さはそろえる）。TITLE と GOAL_NAME も自分のものに
#   Lv2: ダイクストラ法の道のほうが「歩数は多いのに、合計時間は短い」地図にする（ひな形はどちらも13歩なので、まだ未達成）
#   Lv3: COST に新しい記号を1つ足して、地図で使う（例: "w": 2 水たまり、"F": 4 フードワゴンの行列）
#   Lv4: announce 関数の print を書き換え、自分らしい案内文にする
import heapq
from collections import deque

# ★ 窓のいちばん上に出る題名
TITLE = "パレードをよけてビッグサンダーへ"

# ★ 行きたい場所の名前（地図の G のマス）
GOAL_NAME = "ビッグサンダー・マウンテン"

# ★ 園内の地図。1文字が1マス（歩いて1分くらいの広さ）。上が北
#   S = エントランス（出発）  G = 行きたい場所  # = 建物や池（通れない）
#   . = ふつうの道  ~ = 人ごみ  P = パレードのルート（横切るのに時間がかかる）
#   ひな形: 下のまん中がエントランス、まん中の # がシンデレラ城、そのまわりを P のパレードが回っている。
#           G は左上のウエスタンランド（ビッグサンダー・マウンテン）
#   どの行も同じ文字数にする（行の長さがちがうとエラーになる）
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

# ★ 記号ごとの「そのマスに入るのにかかる時間（分）」。# は通れないのでここには書かない
#   新しい記号を足すときは、"w": 2, のように1行足す（時間は 0 以上の整数）
COST = {
    ".": 1,     # ふつうの道
    "S": 1,     # エントランス
    "G": 1,     # 行きたい場所
    "~": 3,     # 人ごみ
    "P": 9,     # パレードのルート
}


def announce(route, minutes):
    """★ ダイクストラ法で見つけた道の案内文を表示する。route = 通るマスの並び、minutes = 合計時間"""
    print(f"【エントランス から {GOAL_NAME} へ】 パレードをよけて {minutes}分")
    print(f"   {len(route) - 1}マス歩く道です")


# ------------------------------------------------------------
# ここから先は探索の本体（書き換えずに読むだけ）。例題1（参考）と同じ2つの探索なので、窓のアニメーションと見比べよう
#   参考の cost_map[r][c]（マスの秒数）が、ここでは COST[park_map[r][c]]（記号の時間）に変わっている。
#   参考より増えているのは、書きまちがいの検査と、# のマスへ進まないようにする部分
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
#   raise SystemExit("…") は、「…」を表示してプログラムを終わらせる命令
if len(park_map) == 0:
    raise SystemExit("park_map が空っぽ。\"G..~..\" のような行を [ ] の中に並べよう")
for mark in COST:
    if type(COST[mark]) != int or COST[mark] < 0:
        raise SystemExit(f"COST の \"{mark}\" の時間がおかしい。時間は \" \" で囲まず、0 以上の整数（3 など）で書こう")
for r in range(len(park_map)):
    if len(park_map[r]) != len(park_map[0]):
        raise SystemExit(f"park_map の {r}行目（上から {r + 1}番目）の長さが {len(park_map[r])}文字で、"
                         f"0行目の {len(park_map[0])}文字とちがう。どの行も同じ文字数にしよう")
    for c in range(len(park_map[r])):
        mark = park_map[r][c]
        if mark in " 　":
            raise SystemExit(f"park_map の {r}行目（上から {r + 1}番目）に空白がまじっている。空白を消して . にしよう")
        if mark != "#" and mark not in COST:
            raise SystemExit(f"park_map の ({r},{c}) の「{mark}」が COST にない。COST に \"{mark}\": 2, のような行を足すか、地図の文字を直そう")

rows = len(park_map)          # 行の数（縦のマス数）
cols = len(park_map[0])       # 列の数（横のマス数）
start = None
goal = None
for r in range(rows):
    for c in range(cols):
        if park_map[r][c] == "S":
            if start is not None:
                raise SystemExit(f"S が2つある（{start} と ({r}, {c})）。出発する場所は1つにしよう")
            start = (r, c)
        if park_map[r][c] == "G":
            if goal is not None:
                raise SystemExit(f"G が2つある（{goal} と ({r}, {c})）。行きたい場所は1つにしよう")
            goal = (r, c)
if start is None or goal is None:
    raise SystemExit("park_map に S（出発）と G（行きたい場所）を1つずつ書こう")
INF = float("inf")


def neighbors(r, c):
    """上・下・左・右のうち、地図の中にあって建物（#）ではないマスを返す（第2回と同じ）"""
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if park_map[nr][nc] == "#":
            continue
        result.append((nr, nc))
    return result


def cost(cell):
    """マス cell に入るのにかかる時間（分）。記号を COST で時間に直す"""
    return COST[park_map[cell[0]][cell[1]]]


def build_route(came_from):
    """ゴールから came_from を逆にたどって道順を組み立てる（第5回と同じ）"""
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


def route_minutes(route):
    """道順 route の合計時間（スタートのマスは数えない。入ったマスの時間を足す）"""
    total = 0
    for cell in route[1:]:
        total = total + cost(cell)
    return total


# ---- 幅優先探索（第2回）: 歩数の少ないマスから順に調べる。マスの時間は見ない ----
steps = {start: 0}            # スタートから何歩か
came_bfs = {start: None}      # そのマスへ来るときの1つ前のマス
bfs_order = []                # 調べた順の (マス, 歩数)。窓の表示に使う
memo = deque([start])         # あとで調べるマスのメモ（第2回のキュー。heapq の queue とは別もの）
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
if goal not in came_bfs:
    raise SystemExit("S から G へ行けない（# で道がふさがっている）。# を . にして道を開けよう")
bfs_route = build_route(came_bfs)

# ---- ダイクストラ法（第6回の heapq 版）: 合計時間の小さいマスから順に確定する ----
distance = {}                 # 距離表: スタートからそのマスまでの、いま分かっているいちばん短い時間
came_dij = {}
for r in range(rows):
    for c in range(cols):
        distance[(r, c)] = INF
        came_dij[(r, c)] = None
distance[start] = 0
settled = set()               # 確定したマス
dij_order = []                # 確定した順の (マス, 合計時間)。窓の表示に使う
queue = [(0, start)]          # heapq の箱。(そのマスまでの時間, マス) の組を入れる
while len(queue) > 0:
    total, current = heapq.heappop(queue)     # ① 時間がいちばん小さい組を取り出す
    if current in settled:
        continue                              # 古い組は読み飛ばす（第6回）
    settled.add(current)                      # ② 確定する
    dij_order.append((current, total))
    if current == goal:
        break                                 # ゴールが確定したら、もっと早い道はないので止めてよい
    for nxt in neighbors(current[0], current[1]):
        new_total = total + cost(nxt)         # ③ となりのマスに入る時間を足す（これがグラフの「辺の重み」にあたる）
        if new_total < distance[nxt]:
            distance[nxt] = new_total
            came_dij[nxt] = current
            heapq.heappush(queue, (new_total, nxt))
dij_route = build_route(came_dij)


def show(route, title):
    """通り道のマスを * にして地図を表示する（S と G はそのまま）"""
    print(title)
    for r in range(rows):
        line = ""
        for c in range(cols):
            mark = park_map[r][c]
            if (r, c) in route and mark not in "SG":
                mark = "*"
            line = line + mark + " "
        print("  " + line)
    print()


bfs_steps, bfs_min = len(bfs_route) - 1, route_minutes(bfs_route)
dij_steps, dij_min = len(dij_route) - 1, route_minutes(dij_route)
show([], f"{TITLE}（S = エントランス、G = {GOAL_NAME}）")
show(bfs_route, f"幅優先探索の道（*）: {bfs_steps}歩 ／ 合計 {bfs_min}分")
show(dij_route, f"ダイクストラ法の道（*）: {dij_steps}歩 ／ 合計 {dij_min}分")
print("-" * 46)
print("方法               歩数   合計時間   決めたマス")
print(f"幅優先探索      {bfs_steps:>5}歩 {bfs_min:>7}分 {len(bfs_order):>8}マス")
print(f"ダイクストラ法  {dij_steps:>5}歩 {dij_min:>7}分 {len(dij_order):>8}マス")
print("-" * 46)
if dij_steps > bfs_steps and dij_min < bfs_min:
    print(f"Lv2 達成: ダイクストラ法の道は {dij_steps - bfs_steps}歩 多いのに、{bfs_min - dij_min}分 早い")
elif dij_min < bfs_min:
    print(f"ダイクストラ法の道のほうが {bfs_min - dij_min}分 早い（歩数の差は {dij_steps - bfs_steps}歩）")
else:
    print("2つの道の合計時間が同じ。P や ~ のマスを、幅優先探索の道の上に置いてみよう")
print()
announce(dij_route, dij_min)


# ============================================================
# ここから下は、地図と探索の進み方を pygame の窓に絵で表示するための道具です。
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
# 左 = 幅優先探索（マスの数字は歩数）、右 = ダイクストラ法（マスの数字は合計時間）、最後に白い枠 = 通り道
grid = [[None if mark == "#" else COST[mark] for mark in line] for line in park_map]
show_window(grid, {start: "S", goal: "G"}, [
    ("幅優先探索: 歩数の少ない順", AMBER, bfs_order, bfs_route, f"G に着いた！ {bfs_steps}歩 ／ 合計 {bfs_min}分"),
    ("ダイクストラ法: 合計時間の小さい順", GREEN, dij_order, dij_route, f"G に着いた！ {dij_steps}歩 ／ 合計 {dij_min}分"),
], TITLE, [
    "枠の色つきのマス = 決まったマス（数字: 左は歩数、右は合計時間）   白い枠 = いま決まったマス（最後は通り道のマス）",
    "マスの左上の小さい数字 = そのマスに入る時間（むらさき = 人ごみ、赤 = パレード、灰色のブロック = 建物）",
])
