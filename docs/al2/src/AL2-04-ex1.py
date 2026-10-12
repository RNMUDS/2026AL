# 重み付きグラフを隣接リストで表し、行き方ごとの合計時間を求める
# 重み = 辺（路線）ごとに書き込んだ数値。ここでは「乗車時間（分）」を重みにする
# 重み付きグラフ = すべての辺に重みが付いているグラフ

# 第3回の隣接リストでは、となりの駅の名前だけを並べた（例 "横浜": ["川崎", "鶴見", "蒲田"]）
# 今回は、となりの駅を (駅の名前, 時間) の2つ組で並べる。( ) で値をまとめたものをタプルと呼ぶ
# 例 ("川崎", 12) は「川崎へ行ける。12分かかる」という意味
# 路線は行きも帰りも通れて、どちら向きでも同じ時間がかかる。だから両方の駅の行に同じ時間を書く
railway = {
    "横浜": [("川崎", 12), ("鶴見", 5), ("蒲田", 26)],
    "川崎": [("横浜", 12), ("蒲田", 10), ("鶴見", 3)],
    "鶴見": [("横浜", 5), ("川崎", 3), ("生麦", 4)],
    "生麦": [("鶴見", 4), ("大森", 9)],
    "大森": [("生麦", 9), ("蒲田", 4)],
    "蒲田": [("横浜", 26), ("川崎", 10), ("大森", 4)],
}

print("重み付きグラフ（数字は乗車時間・分）")
print("-" * 50)
for station in railway:
    parts = []
    # for name, minutes in リスト: で、2つ組の1つ目を name に、2つ目を minutes に入れてくり返す
    for name, minutes in railway[station]:
        parts.append(f"{name}({minutes}分)")
    print(f"{station}: " + "、".join(parts))    # "、".join(リスト) はリストの中身を「、」でつないだ文字にする
print("-" * 50)
print()


def route_minutes(route):
    """route（駅を通る順に並べたリスト）の合計時間を求める。"""
    total = 0
    # 隣り合う2駅（here と next_station）の組を、前から順に1組ずつ見る
    # 駅が3つなら組は2つなので、len(route) - 1 回くり返す
    for i in range(len(route) - 1):
        here = route[i]
        next_station = route[i + 1]
        # here のとなりの一覧から next_station を探し、見つかったらその路線の時間を合計に足す
        for name, minutes in railway[here]:
            if name == next_station:
                total = total + minutes
    return total


# 横浜から蒲田まで、3通りの行き方を比べる（どれも、駅を通る順に書く）
routes = [
    ["横浜", "蒲田"],
    ["横浜", "川崎", "蒲田"],
    ["横浜", "鶴見", "川崎", "蒲田"],
]

print("横浜から蒲田までの行き方を比べる")
print("-" * 50)
results = []                    # (行き方, 合計時間) の記録（窓の表示にも使う）
for route in routes:
    minutes = route_minutes(route)
    results.append((route, minutes))
    # 乗る路線の本数 = 駅の数 - 1。乗りかえの回数 = 路線の本数 - 1
    print(" → ".join(route))
    print(f"    路線{len(route) - 1}本（乗りかえ{len(route) - 2}回） ／ 合計時間: {minutes}分")
print("-" * 50)
print()

# 「路線の本数がいちばん少ない道」と「合計時間がいちばん短い道」を、それぞれ選ぶ
# まず1つ目を仮の答えにして、それより良いものが出てきたら入れかえる（第1回の全探索と同じ）
fewest = results[0]
fastest = results[0]
for route, minutes in results:
    if len(route) < len(fewest[0]):     # 駅の数が少ない = 路線の本数が少ない
        fewest = (route, minutes)
    if minutes < fastest[1]:            # fastest[1] は fastest の2つ目（合計時間）
        fastest = (route, minutes)
print("路線の本数がいちばん少ない道:", " → ".join(fewest[0]), f"（{fewest[1]}分）")
print("合計時間がいちばん短い道　　:", " → ".join(fastest[0]), f"（{fastest[1]}分）")
if fewest[0] != fastest[0]:
    print("→ 2つは別の道。路線の本数が少ないからといって、時間が短いとはかぎらない")
else:
    print("→ 2つは同じ道になった")


# ============================================================
# ここから下は、重み付きグラフを pygame の窓に絵で表示するための道具です。
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
BLUE = (90, 170, 255)
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


def _graph_parts(railway):
    """隣接リストから、丸にする駅の名前と、線（駅, 駅, 時間）の一覧を作る。
    となりの一覧には書いたのに、鍵（左側）に書き忘れた駅も丸として描けるように足しておく。"""
    names = list(railway)
    for a in railway:
        for b, _ in railway[a]:
            if b not in names:
                names.append(b)
    edges = []
    for a in railway:
        for b, w in railway[a]:
            if not any({a, b} == {x, y} for x, y, _ in edges):
                edges.append((a, b, w))
    return names, edges


def _weight(railway, a, b):
    """a から b への時間。直接つながっていなければ None。"""
    for name, w in railway.get(a, []):
        if name == b:
            return w
    return None


def _pairs(route):
    """道（駅の並び）を、隣り合う2駅の組の一覧にする。"""
    return [(route[i], route[i + 1]) for i in range(len(route) - 1)]


def _crossings(order, edges):
    """円の上に order の順で頂点を並べたとき、線どうしが何回交わるかを数える。"""
    at = {name: i for i, name in enumerate(order)}
    count = 0
    for i, (a, b, _) in enumerate(edges):
        lo, hi = sorted((at[a], at[b]))
        for c, d, _ in edges[i + 1:]:
            if len({a, b, c, d}) < 4:
                continue
            inside = (lo < at[c] < hi) + (lo < at[d] < hi)
            count += inside == 1
    return count


def _layout(names, edges, cx=255, cy=320, radius=200):
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


def _draw_graph(screen, fonts, names, edges, pos, colored=(), rings=None, dim_weights=False):
    """丸（頂点）と線（辺）と、線のまん中の重み（時間）を描く。
    colored = [(駅の組の一覧, 色, 太さ), ...]。あとのものほど上に重ねて描く。
    rings = {駅の名前: 枠の色}。dim_weights=True なら重みを暗く描く（幅優先探索は重みを見ないため）。"""
    big, mid, small = fonts
    edge_color = {}
    for a, b, _ in edges:
        pygame.draw.line(screen, LINE, pos[a], pos[b], 2)
    for pairs, color, width in colored:
        for a, b in pairs:
            if a in pos and b in pos:
                pygame.draw.line(screen, color, pos[a], pos[b], width)
                edge_color[frozenset((a, b))] = color
    for a, b, w in edges:
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        color = edge_color.get(frozenset((a, b)), SUB if dim_weights else TEXT)
        t = small.render(f"{w}分", True, color)
        box = pygame.Rect(0, 0, t.get_width() + 12, t.get_height() + 4)
        box.center = (mx, my)
        pygame.draw.rect(screen, BG, box, border_radius=8)
        pygame.draw.rect(screen, color if frozenset((a, b)) in edge_color else LINE, box, width=1, border_radius=8)
        screen.blit(t, (box.x + 6, box.y + 2))
    for name in names:
        x, y = pos[name]
        ring = (rings or {}).get(name, LINE)
        pygame.draw.circle(screen, NODE, (x, y), 34)
        pygame.draw.circle(screen, ring, (x, y), 34, 5 if ring != LINE else 3)
        t = mid.render(name, True, TEXT)
        if t.get_width() > 62:                  # 長い名前は小さい文字にして丸に収める
            t = small.render(name, True, TEXT)
        if t.get_width() > 62:                  # それでも長ければ2行に分ける
            half = (len(name) + 1) // 2
            t1, t2 = small.render(name[:half], True, TEXT), small.render(name[half:], True, TEXT)
            screen.blit(t1, (x - t1.get_width() / 2, y - t1.get_height()))
            screen.blit(t2, (x - t2.get_width() / 2, y))
            continue
        screen.blit(t, (x - t.get_width() / 2, y - t.get_height() / 2))


def _fit(font, text, width):
    """text が width ピクセルに収まらなければ、後ろを「…」にして縮める。"""
    if font.size(text)[0] <= width:
        return text
    while text and font.size(text + "…")[0] > width:
        text = text[:-1]
    return text + "…"


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


def show_window(railway, results):
    """行き方ごとに、区間の時間を1つずつ足していくようすをアニメーション表示する。窓を閉じると終わる。"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("重み付きグラフで合計時間を求める")
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    names, edges = _graph_parts(railway)
    pos = _layout(names, edges)
    steps = []                  # (何本目の行き方か, 何区間目まで足したか)
    for ri, (route, _) in enumerate(results):
        for si in range(1, len(route)):
            steps.append((ri, si))
    true_total = []             # 窓が自分で足した合計（つながっていない区間は None）
    for route, _ in results:
        ws = [_weight(railway, a, b) for a, b in _pairs(route)]
        true_total.append(None if None in ws else sum(ws))
    n = len(results)
    row_h = min(96, (HEIGHT - 300) // max(n, 1))

    def calc_text(route, upto):
        ws = [_weight(railway, a, b) for a, b in _pairs(route)[:upto]]
        shown = ["?" if w is None else str(w) for w in ws]
        total = sum(w for w in ws if w is not None)
        return " + ".join(shown) + f" = {total}分"

    def draw(k):
        done = k > len(steps)
        ri, si = (None, 0) if (k == 0 or done) else steps[k - 1]
        colored, rings = [], {}
        if ri is not None:
            route = results[ri][0]
            pairs = _pairs(route)
            colored = [(pairs[:si - 1], GREEN, 6), (pairs[si - 1:si], AMBER, 9)]
            rings = {name: GREEN for name in route[:si]}
            rings[route[si]] = AMBER
        fewest = fastest = None
        if done:
            ok = [i for i in range(n) if true_total[i] is not None]
            if ok:
                fewest = min(ok, key=lambda i: len(results[i][0]))
                fastest = min(ok, key=lambda i: true_total[i])
                colored = [(_pairs(results[fewest][0]), BLUE, 7), (_pairs(results[fastest][0]), GREEN, 7)]
                if fewest == fastest:
                    colored = [(_pairs(results[fastest][0]), GREEN, 7)]
        screen.blit(big.render("重み付きグラフ（線の数字 = 時間）", True, GREEN), (30, 20))
        screen.blit(small.render("橙 = いま足した区間、緑 = もう足した区間", True, SUB), (30, 52))
        _draw_graph(screen, fonts, names, edges, pos, colored, rings)
        x0 = 540
        screen.blit(big.render("route_minutes で合計時間を求める", True, GREEN), (x0, 20))
        screen.blit(small.render("隣り合う2駅の時間を、前から順に total に足す", True, SUB), (x0, 52))
        last_ri = n - 1 if done else (ri if ri is not None else -1)
        for i in range(last_ri + 1):
            route, minutes = results[i]
            y = 84 + i * row_h
            on = i == ri
            box = pygame.Rect(x0, y, 490, row_h - 8)
            frame = (255, 255, 255) if on else (70, 70, 80)
            if done and i == fastest:
                frame = GREEN
            elif done and i == fewest:
                frame = BLUE
            pygame.draw.rect(screen, (30, 30, 38), box, border_radius=6)
            pygame.draw.rect(screen, frame, box, width=3 if (on or done) else 1, border_radius=6)
            font = mid if row_h >= 80 else small
            screen.blit(font.render(_fit(font, " → ".join(route), 470), True, TEXT), (x0 + 10, y + 6))
            upto = si if on else len(route) - 1
            screen.blit(font.render(_fit(font, calc_text(route, upto), 470), True, AMBER), (x0 + 10, y + 6 + font.get_height() + 2))
            if not on and row_h >= 80:
                screen.blit(small.render(f"路線{len(route) - 1}本 ／ route_minutes の答え {minutes}分", True, SUB),
                            (x0 + 10, y + 10 + 2 * font.get_height()))
        by = HEIGHT - 150
        info2, info3, color = "", "", SUB
        if k == 0:
            info = "スペースで開始／→で1手順"
        elif not done:
            route = results[ri][0]
            a, b = route[si - 1], route[si]
            w = _weight(railway, a, b)
            if w is None:
                info, info2, color = f"手順{k}  {a} → {b}", f"{a} と {b} は直接つながっていない", RED
                info3 = "→ routes の書き方か、railway の線を見直す"
            else:
                info = f"手順{k}  {a} → {b} は {w}分。total に {w} を足す"
                info2 = f"ここまでの合計 total = {calc_text(route, si).split(' = ')[1]}"
        else:
            info = "路線の本数が少ない道（青）と、合計時間が短い道（緑）"
            wrong = [i for i in range(n) if results[i][1] != true_total[i]]
            if wrong:
                i = wrong[0]
                info2, color = f"{' → '.join(results[i][0])} の答えが {results[i][1]}分", RED
                info3 = f"→ 区間の時間を足すと {true_total[i]}分。穴を見直す"
                if true_total[i] is None:
                    info3 = "→ 直接つながっていない2駅がある。routes を見直す"
            elif fewest is not None and fewest != fastest:
                info2, color = f"青: 路線{len(results[fewest][0]) - 1}本 {true_total[fewest]}分 ／ 緑: 路線{len(results[fastest][0]) - 1}本 {true_total[fastest]}分", AMBER
                info3 = "本数が少ない道が、時間も短いとはかぎらない"
            else:
                info2, color = "本数がいちばん少ない道が、時間もいちばん短かった", AMBER
                info3 = "→ 時間を書き換えると、2つが別の道になることがある"
        screen.blit(mid.render(info, True, TEXT), (x0, by))
        screen.blit(mid.render(_fit(mid, info2, 500), True, color), (x0, by + 32))
        screen.blit(mid.render(_fit(mid, info3, 500), True, color), (x0, by + 64))

    _loop(screen, fonts, len(steps) + 1, draw)


# --- 窓を開いて、行き方ごとに区間の時間を1つずつ足していくようすをアニメーション表示する ---
# 左に重み付きグラフ、右に行き方ごとの足し算。最後に「本数が少ない道（青）」と「時間が短い道（緑）」を並べる。
# スペースで再生／一時停止、→ で1手順ずつ進む。窓を閉じるとプログラムが終わる
show_window(railway, results)
