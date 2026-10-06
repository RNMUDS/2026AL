# グラフを「隣接リスト」で表す
# グラフ = 「点（頂点）」と「点どうしのつながり（辺）」だけでものごとを表す方法
# 隣接リスト = それぞれの頂点について「となり（直接つながっている頂点）」を並べた表
#   隣接（りんせつ）は「となり合っている」「直接つながっている」という意味

# 6つの駅と、駅どうしをつなぐ路線をグラフにする。頂点 = 駅、辺 = 路線
# 辞書 { 鍵: 値, ... } を使う。鍵 = 駅の名前、値 = となりの駅を並べたリスト
# 例 railway["横浜"] と書くと、横浜のとなりの駅のリスト ["川崎", "鶴見", "大森"] が取り出せる
# 路線は行きも帰りも通れるので、横浜の行に「川崎」を書いたら、川崎の行にも「横浜」を書く
railway = {
    "横浜": ["川崎", "鶴見", "大森"],
    "川崎": ["横浜", "蒲田", "鶴見", "生麦"],
    "鶴見": ["横浜", "生麦", "川崎"],
    "大森": ["横浜", "蒲田"],
    "蒲田": ["川崎", "大森"],
    "生麦": ["鶴見", "川崎"],
}

print("隣接リストで表した路線図")
print("-" * 44)
# for station in railway: で、辞書の鍵（駅の名前）を上から1つずつ station に入れてくり返す
for station in railway:
    neighbors = railway[station]                # その駅のとなりの駅のリスト
    print(f"{station}: " + "、".join(neighbors))  # "、".join(リスト) はリストの中身を「、」でつないだ文字にする
print("-" * 44)

# 頂点の数 = 辞書の鍵の数。len(辞書) で数えられる
vertex_count = len(railway)

# 辺（路線）の数を数える。
# なぜ数えるか: 紙の路線図の線の本数と同じになれば、書き写しに抜けやまちがいがないと確かめられる
# まず、各駅の「となりの駅の数」を全部足して、隣接リストに書いた名前の合計 name_total を求める
name_total = 0
count_log = []                  # 駅ごとの「ここまでの合計」の記録（窓の表示に使う）
for station in railway:
    # len(リスト) はリストに入っている個数。横浜なら3
    name_total = name_total + len(railway[station])
    # append(x) はリストの最後に x を足す。(station, name_total) は2つを1組にしたもの
    count_log.append((station, name_total))
# name_total はまだ辺の数ではない。1本の路線（例 横浜—川崎）は、横浜の行と川崎の行の
# 両方に書かれているので2回数えている。だから半分にする（// は「割り算して、あまりを捨てる」記号）
edge_count = name_total // 2

print("頂点（駅）の数:", vertex_count)
print("辺（路線）の数:", edge_count)
print()

# となりの駅をすぐに取り出せることが、隣接リストの長所
print("横浜のとなりの駅:", railway["横浜"])
print("蒲田のとなりの駅:", railway["蒲田"])
print()

# 「横浜と蒲田は直接つながっているか」を調べる
# A in リスト は「A がリストの中にあれば True（はい）」。横浜のとなりの一覧に蒲田があるかを見る
if "蒲田" in railway["横浜"]:
    print("横浜と蒲田は直接つながっている")
else:
    print("横浜と蒲田は直接つながっていない（乗りかえが必要）")


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


def show_window(railway, count_log, edge_count):
    """隣接リストを1駅ずつ読み、名前を数えていくようすをアニメーション表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("隣接リストを読む")
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names = list(railway)
    # となりの一覧には書いたのに、鍵（左側）に書き忘れた駅も、丸として描けるように足しておく
    missing = []
    for a in railway:
        for b in railway[a]:
            if b not in railway and b not in missing:
                missing.append(b)
    names = names + missing
    edges = []                  # 線を1本ずつ（同じ線を2回入れない）
    for a in railway:
        for b in railway[a]:
            if (a, b) not in edges and (b, a) not in edges:
                edges.append((a, b))
    pos = _layout(names, edges)
    n = len(count_log)
    row_h = min(40, (HEIGHT - 260) // max(n, 1))    # 駅が多いときは行の間をつめる

    def draw(k):
        done = k > n
        step = min(k, n)
        tally = {}
        for s, _ in count_log[:step]:
            for nb in railway[s]:
                tally[(s, nb)] = 1
        current = None if (k == 0 or done) else count_log[k - 1][0]
        hot_nodes = railway[current] if current else ()
        hot_edges = [(current, nb) for nb in railway[current]] if current else ()
        screen.blit(big.render("グラフ（丸 = 頂点、線 = 辺）", True, GREEN), (30, 20))
        screen.blit(small.render("線のまん中の数字 = その線を何回数えたか", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, hot_edges, hot_nodes, current, tally)
        x0 = 540
        screen.blit(big.render("隣接リスト railway を1駅ずつ読む", True, GREEN), (x0, 20))
        screen.blit(small.render("for station in railway: で、上の駅から順に読む", True, SUB), (x0, 52))
        for i, (s, total) in enumerate(count_log[:step]):
            y = 84 + i * row_h
            on = s == current
            box = pygame.Rect(x0, y, 490, row_h - 6)
            pygame.draw.rect(screen, (30, 30, 38), box, border_radius=6)
            pygame.draw.rect(screen, (255, 255, 255) if on else (70, 70, 80), box, width=3 if on else 1, border_radius=6)
            font = mid if row_h >= 34 else small
            ty = y + (row_h - 6 - font.get_height()) // 2
            screen.blit(font.render(s, True, GREEN), (x0 + 10, ty))
            screen.blit(font.render("→ " + "、".join(railway[s]), True, TEXT), (x0 + 100, ty))
            t = small.render(f"{len(railway[s])}個", True, AMBER)
            screen.blit(t, (x0 + 480 - t.get_width(), y + (row_h - 6 - t.get_height()) // 2))
        by = HEIGHT - 160
        info3, color = "", AMBER
        if k == 0:
            info, info2, color = "スペースで開始／→で1手順", "", SUB
        elif not done:
            info = f"手順{k}  {current} のとなりの駅 {len(railway[current])}個 を数える"
            info2, color = f"ここまでに数えた名前の合計 name_total = {count_log[k - 1][1]}", SUB
        else:
            info = f"名前の合計 {count_log[-1][1]}個 → 辺の数 edge_count = {edge_count}本"
            once = [e for e in edges if tally.get(e, 0) + tally.get((e[1], e[0]), 0) < 2]
            if missing:
                info2, color = f"「{'、'.join(missing)}」が railway の左側（鍵）にない", RED
                info3 = "→ その駅の行を足して、となりの駅を書く"
            elif once:
                info2, color = "数字が 1 の線がある = 片方の駅の行にしか書いていない", RED
                info3 = f"→ {once[0][1]} の行に {once[0][0]} を足す（ほかの 1 の線も同じ）"
            elif edge_count != len(edges):
                info2, color = f"線は {len(edges)}本 なのに edge_count が {edge_count}本", RED
                info3 = "→ 名前の合計の数え方と、半分にする式を見直す"
            else:
                info2 = f"線のまん中がすべて 2 = 1本の路線を両側の駅から2回数えた"
                info3 = f"だから 名前の合計 {count_log[-1][1]} ÷ 2 = {edge_count}本"
        screen.blit(mid.render(info, True, TEXT), (x0, by))
        screen.blit(mid.render(info2, True, color), (x0, by + 32))
        screen.blit(mid.render(info3, True, color), (x0, by + 64))

    _loop(screen, fonts, n + 1, draw)


# --- 窓を開いて、隣接リストを1駅ずつ読むようすをアニメーション表示する ---
# 左にグラフ（丸と線）、右に隣接リスト。線のまん中の数字は「その線を何回数えたか」。
# スペースで再生／一時停止、→ で1手順ずつ進む。窓を閉じるとプログラムが終わる
show_window(railway, count_log, edge_count)
