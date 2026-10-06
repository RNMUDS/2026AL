# 同じグラフを「隣接行列」で表して、隣接リストと比べる
# 隣接行列 = たてよこの表（マス目）を作り、つながっていれば1、つながっていなければ0を書く
#   行列（ぎょうれつ）は「たてよこに数を並べた表」のこと。横の並びを行、たての並びを列という

# 駅の一覧。リストの何番目か（0 から数える）を、その駅の番号として使う
# 例 "横浜" は 0番、"川崎" は 1番
stations = ["横浜", "川崎", "鶴見", "大森", "蒲田", "生麦"]

# 路線（辺）の一覧。("横浜", "川崎") は「横浜と川崎をつなぐ路線が1本ある」という意味
lines = [
    ("横浜", "川崎"),
    ("横浜", "鶴見"),
    ("横浜", "大森"),
    ("川崎", "蒲田"),
    ("川崎", "鶴見"),
    ("大森", "蒲田"),
    ("鶴見", "生麦"),
    ("川崎", "生麦"),
]

n = len(stations)               # 駅の数（表のたて・よこのマスの数）

# 全部のマスを0にした n×n の表を作る。matrix[i][j] が「i行目・j列目」のマス
# [0 for j in range(n)] は「0 を n 個並べたリスト」（表の1行ぶん）。それを n 行ぶん作る
matrix = [[0 for j in range(n)] for i in range(n)]
matrix_log = []                 # 路線を1本書くごとの表の記録（窓の表示に使う）

# 路線があるマスだけ1にする
# for a, b in lines: は、組 ("横浜", "川崎") を取り出して a = "横浜"、b = "川崎" のように分けて入れる
for a, b in lines:
    # index() は「リストの中で何番目にあるか」を返す。stations.index("川崎") なら 1
    i = stations.index(a)
    j = stations.index(b)
    matrix[i][j] = 1            # 「i番の駅から j番の駅へ行ける」
    # 路線は行きも帰りも通れるので、行と列を入れかえたマスにも1を書く
    matrix[j][i] = 1
    # [row[:] for row in matrix] で表の中身をコピーして記録する（コピーしないと、あとで書き換わってしまう）
    matrix_log.append([row[:] for row in matrix])

# 表の見出しには、駅の名前ではなく番号を使う（そのほうが桁がそろって読みやすい）
print("駅の番号")
for i in range(n):
    print(f"  {i} = {stations[i]}")
print()

print("隣接行列（1 = つながっている、0 = つながっていない）")
print("-" * 40)
# f"{j:>4}" は「j を4文字ぶんの幅で右にそろえて書く」という意味（表の桁をそろえるため）
# "".join(...) は、並べた文字を1つの文字につなぐ
# 駅の名前の長さがちがっても桁がそろうように、いちばん長い名前の文字数 width に合わせる
# ljust(width, "　") は、短い名前のうしろに全角スペースを足して width 文字にする
width = max(len(name) for name in stations)
print(" " * (6 + 2 * width) + "".join(f"{j:>4}" for j in range(n)))
for i in range(n):
    name = stations[i].ljust(width, "　")
    row = "".join(f"{matrix[i][j]:>4}" for j in range(n))
    print(f"  {i} {name}  " + row)
print("-" * 40)
print()

# 隣接行列は「2つの駅がつながっているか」を、表の1マスを見るだけで調べられる
# ここからは for の外。a と b に、調べたい2つの駅を入れ直している
# 路線の一覧に ("横浜", "蒲田") はないので 0、("横浜", "大森") はあるので 1 になるはず
a = "横浜"
b = "蒲田"
i = stations.index(a)
j = stations.index(b)
print(f"{a} と {b} はつながっているか → matrix[{i}][{j}] =", matrix[i][j])

a = "横浜"
b = "大森"
i = stations.index(a)
j = stations.index(b)
print(f"{a} と {b} はつながっているか → matrix[{i}][{j}] =", matrix[i][j])
print()

# 2つの書き写し方が、どれだけの量を書きこむかを比べる
# なぜ比べるか: 駅が増えたとき、表が大きくなりすぎると、コンピュータの記憶する場所が足りなくなるため
matrix_cells = n * n            # 隣接行列は、たて n マス × よこ n マスに 0 か 1 を書く
# 隣接リストでは、1本の路線が両方の駅の行に1回ずつ書かれる（つながっていない組は書かない）
list_names = len(lines) * 2
print("隣接行列が書くマスの数:", matrix_cells, "マス（駅の数の2乗）")
print("隣接リストが書く名前の数:", list_names, "個（路線の数の2倍）")
print()

# 駅の数を増やすと差がどうなるか。実際の路線図では、1つの駅のとなりは数個しかない。
# そこで、どの駅も、となりの駅が平均3つあるとして計算する
# 隣接行列 = 駅の数 × 駅の数 マス、隣接リスト = 駅の数 × 3 個（各駅の行に名前が3つずつ）
print("駅の数を増やしたときの比較（となりの駅が平均3つの場合）")
print("-" * 48)
print("    駅の数   隣接行列のマス数   隣接リストの名前の数")
for count in [10, 100, 1000, 10000]:
    print(f"{count:>10}   {count*count:>16}   {count*3:>18}")
print("-" * 48)


# ============================================================
# ここから下は、グラフを pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import math
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

WIDTH, HEIGHT = 1060, 620       # 窓の大きさ（ピクセル）
STEP_MS = 900                   # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
LINE = (80, 84, 100)
NODE = (38, 40, 52)
TEXT = (230, 230, 235)
SUB = (150, 150, 160)
GREEN = (118, 185, 0)
AMBER = (255, 184, 0)
RED = (255, 110, 110)
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


def _crossings(order, edges):
    """円の上に order の順で頂点を並べたとき、線どうしが何回交わるかを数える。"""
    at = {name: i for i, name in enumerate(order)}
    count = 0
    for i, (a, b) in enumerate(edges):
        lo, hi = sorted((at[a], at[b]))
        for c, d in edges[i + 1:]:
            if len({a, b, c, d}) < 4:
                continue
            inside = (lo < at[c] < hi) + (lo < at[d] < hi)
            count += inside == 1
    return count


def _layout(names, edges, cx=250, cy=300, radius=190):
    """頂点を円の上に等間隔で並べる（いちばん上から時計回り）。
    頂点が8個以下なら、線の交わりがいちばん少なくなる並べ方を全部試して選ぶ。"""
    order = list(names)
    if 3 < len(order) <= 8:
        from itertools import permutations
        best = None
        for rest in permutations(order[1:]):
            cand = [order[0], *rest]
            k = _crossings(cand, edges)
            if best is None or k < best[0]:
                best = (k, cand)
        order = best[1]
    n = len(order)
    return {name: (cx + radius * math.sin(2 * math.pi * i / n), cy - radius * math.cos(2 * math.pi * i / n))
            for i, name in enumerate(order)}


def _draw_graph(screen, fonts, names, edges, pos, hot_edges=(), hot_nodes=(), current=None, tally=None,
                numbers=False, focus_edge=None):
    """丸（頂点）と線（辺）を描く。hot_* は緑にする辺・頂点、current は白い枠をつける頂点、
    focus_edge は橙で太く描く辺。tally を渡すと、線のまん中に「その線を何回数えたか」を書く。
    numbers=True なら頂点の番号も書く。"""
    big, mid, small = fonts
    for a, b in edges:
        hot = (a, b) in hot_edges or (b, a) in hot_edges
        pygame.draw.line(screen, GREEN if hot else LINE, pos[a], pos[b], 6 if hot else 2)
    if focus_edge is not None:
        a, b = focus_edge
        pygame.draw.line(screen, AMBER, pos[a], pos[b], 9)
    if tally is not None:
        for a, b in edges:
            k = tally.get((a, b), 0) + tally.get((b, a), 0)
            if k == 0:
                continue
            # 線のまん中より少し a 寄りに書く（まん中どうしが重なる線があっても読めるように）
            mx, my = pos[a][0] * 0.58 + pos[b][0] * 0.42, pos[a][1] * 0.58 + pos[b][1] * 0.42
            color = AMBER if k >= 2 else GREEN
            pygame.draw.circle(screen, BG, (mx, my), 14)
            pygame.draw.circle(screen, color, (mx, my), 14, 2)
            t = small.render(f"{k}", True, color)
            screen.blit(t, (mx - t.get_width() / 2, my - t.get_height() / 2))
    for i, name in enumerate(names):
        x, y = pos[name]
        ring = (255, 255, 255) if name == current else (GREEN if name in hot_nodes else LINE)
        if focus_edge is not None and name in focus_edge:
            ring = AMBER
        pygame.draw.circle(screen, NODE, (x, y), 34)
        pygame.draw.circle(screen, ring, (x, y), 34, 5 if name == current else 3)
        t = mid.render(name, True, TEXT)
        if t.get_width() > 62:                  # 長い名前は小さい文字にして丸に収める
            t = small.render(name, True, TEXT)
        screen.blit(t, (x - t.get_width() / 2, y - t.get_height() / 2))
        if numbers:
            n = small.render(str(i), True, AMBER)
            screen.blit(n, (x + 26, y - 40))


def _loop(screen, fonts, last_step, draw):
    """窓のくり返し処理。draw(k) が k 手順目の画面を描く。"""
    capture = os.environ.get("AL2_CAPTURE")      # 授業ページの画像を作るときだけ使う
    k = last_step if capture else 0
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
        hint = fonts[2].render("スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる", True, SUB)
        screen.blit(hint, (30, HEIGHT - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)


def show_window(stations, lines, matrix_log):
    """路線を1本ずつ読み、隣接行列に1を書いていくようすをアニメーション表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("隣接行列に書き写す")
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    pos = _layout(stations, lines)
    n = len(stations)
    steps = len(matrix_log)
    cell = max(28, min(52, 380 // n))
    empty = [[0] * n for _ in range(n)]

    def draw(k):
        done = k > steps
        step = min(k, steps)
        now = matrix_log[step - 1] if step > 0 else empty
        before = matrix_log[step - 2] if step > 1 else empty
        focus = None if (k == 0 or done) else lines[k - 1]
        screen.blit(big.render("グラフ（丸 = 頂点、数字 = 駅の番号）", True, GREEN), (30, 20))
        screen.blit(small.render("緑の線 = もう表に書いた路線、橙 = いま書いている路線", True, SUB), (30, 52))
        _draw_graph(screen, fonts, stations, lines, pos, hot_edges=lines[:step], numbers=True,
                    focus_edge=focus)
        x0, y0 = 600, 110
        screen.blit(big.render("隣接行列 matrix", True, GREEN), (x0 - 40, 20))
        screen.blit(small.render("matrix[行の番号][列の番号]。1 = つながっている", True, SUB), (x0 - 40, 52))
        for j in range(n):
            t = small.render(str(j), True, SUB)
            screen.blit(t, (x0 + j * cell + cell / 2 - t.get_width() / 2, y0 - 24))
        for i in range(n):
            t = small.render(f"{i} {stations[i]}", True, SUB)
            screen.blit(t, (x0 - 8 - t.get_width(), y0 + i * cell + cell / 2 - t.get_height() / 2))
            for j in range(n):
                v = now[i][j]
                new = (not done) and v != before[i][j]
                rect = pygame.Rect(x0 + j * cell + 2, y0 + i * cell + 2, cell - 4, cell - 4)
                fill = (40, 70, 20) if v else (30, 30, 38)
                pygame.draw.rect(screen, fill, rect, border_radius=5)
                pygame.draw.rect(screen, AMBER if new else ((90, 140, 30) if v else (60, 60, 70)), rect,
                                 width=4 if new else 1, border_radius=5)
                t = mid.render(str(v), True, TEXT if v else (90, 90, 100))
                screen.blit(t, (rect.centerx - t.get_width() / 2, rect.centery - t.get_height() / 2))
        by = HEIGHT - 160
        info3, color = "", AMBER
        if k == 0:
            info, info2, color = "スペースで開始／→で1手順", f"最初は {n}×{n} = {n * n}マス がすべて 0", SUB
        elif not done:
            a, b = focus
            i, j = stations.index(a), stations.index(b)
            info = f"手順{k}  路線 {a}—{b}（{i}番と{j}番）"
            info2 = f"→ matrix[{i}][{j}] と matrix[{j}][{i}] の2マスを 1 にする"
        else:
            ones = sum(sum(row) for row in now)
            symmetric = all(now[i][j] == now[j][i] for i in range(n) for j in range(n))
            info = f"{n * n}マス のうち 1 は {ones}マス"
            if not symmetric:
                info2, color = "表が左右対称になっていない", RED
                info3 = "→ 行と列を入れかえたマスにも 1 を書いたか見直す"
            elif ones != len(lines) * 2:
                info2, color = f"路線 {len(lines)}本 × 2 = {len(lines) * 2}マス にならない", RED
                info3 = "→ 同じ路線を2回書いていないか、lines を見直す"
            else:
                info2 = f"= 路線 {len(lines)}本 × 2（行きと帰りで2マスずつ）"
                info3 = f"残りの {n * n - ones}マス は 0 のまま（つながっていない組）"
        screen.blit(mid.render(info, True, TEXT), (x0 - 40, by))
        screen.blit(mid.render(info2, True, color), (x0 - 40, by + 32))
        screen.blit(mid.render(info3, True, color), (x0 - 40, by + 64))

    _loop(screen, fonts, steps + 1, draw)


# --- 窓を開いて、路線を1本ずつ隣接行列に書き写すようすをアニメーション表示する ---
# 左にグラフ（丸と線、丸の右上の数字が駅の番号）、右に隣接行列。橙の枠が、いま 1 にしたマス。
# スペースで再生／一時停止、→ で1手順ずつ進む。窓を閉じるとプログラムが終わる
show_window(stations, lines, matrix_log)
