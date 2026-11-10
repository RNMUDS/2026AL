# 第8回 クリエイティブ演習2: USJ で回りたい場所を全部回って、エントランスに戻る「いちばん早い順番」を全探索でさがす
# 演習1の歩く時間の表を使い、回る順番をすべて試して、合計の歩く時間がいちばん短いものを選ぶ。
# 場所を増やすと、試す順番の数と時間がどれくらい増えるかも測る。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: spots と WALK を、演習1で作った自分のものに貼りかえる
#   Lv2: 場所を8か所以上にして、全探索にかかる時間と「15か所・20か所なら何時間・何年か」の見積もりを確かめる
#   Lv3: FIRST_VISIT に「いちばん最初に行きたい場所」の名前を書き、いちばん早い順番から何分おそくなるかを確かめる
#   Lv4: announce 関数の print を書き換え、自分らしい「回り方の案内」にする
import math
import time
from itertools import permutations

# ★ 窓のいちばん上に出る題名
TITLE = "USJ を全部回る、いちばん早い順番"

# ★ 回りたい場所 (名前, x, y)。演習1の spots をそのまま貼る。0番は出発して最後に戻る場所（エントランス）
spots = [
    ("エントランス", 7, 14),
    ("ハリー・ポッター", 2, 4),
    ("ミニオン・パーク", 14, 11),
    ("ジュラシック・パーク", 9, 1),
    ("スーパー・ニンテンドー・ワールド", 17, 5),
]

# ★ 地図の1目もりを歩くのにかかる時間（分）。演習1と同じにする
WALK = 1

# ★ いちばん最初に行きたい場所の名前（例: "ハリー・ポッター"）。決めないときは None のまま
FIRST_VISIT = None


def announce(route, total):
    """★ いちばん早い回り方の案内文を表示する。route = 回る場所の名前の並び（最初と最後はエントランス）、total = 合計の分"""
    print(f"【おすすめの回り方】 歩く時間は合計 {total}分")
    for k in range(1, len(route) - 1):
        print(f"   {k}番目: {route[k]}")
    print(f"   最後に {route[-1]} へ戻る")


# ------------------------------------------------------------
# ここから先は全探索の本体（書き換えずに読むだけ）。例題2（参考）と同じ方法なので、窓のアニメーションと見比べよう
#   参考の cities が spots に、距離が「歩く時間（分）」に変わっている。
#   参考より増えているのは、書きまちがいの検査と、FIRST_VISIT（最初に行く場所の指定）と、時間の見積もりの部分
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
if type(spots) not in (list, tuple):
    raise SystemExit("spots は [ ] の中に (\"名前\", x, y), を1行ずつ並べて書こう")
if len(spots) < 3:
    raise SystemExit("spots が少なすぎる。エントランスのほかに2か所以上を (\"名前\", x, y), の形で書こう")
if len(spots) > 10:
    raise SystemExit(f"spots が {len(spots)}か所ある。全探索だと {math.factorial(len(spots) - 1):,}通りになり、"
                     "とても時間がかかる。10か所までにしよう（なぜ増やせないのかが、今回のテーマ）")
for i in range(len(spots)):
    spot = spots[i]
    if type(spot) != tuple or len(spot) != 3:
        raise SystemExit(f"spots の {i}番目が (\"名前\", x, y) の形になっていない。かっこ ( ) と、カンマ2つで書こう")
    if type(spot[0]) != str or spot[0] == "":
        raise SystemExit(f"spots の {i}番目の名前が文字になっていない。\"ミニオン・パーク\" のように \" \" で囲もう")
    if type(spot[1]) not in (int, float) or type(spot[2]) not in (int, float):
        raise SystemExit(f"spots の {i}番目（{spot[0]}）の位置がおかしい。x と y は \" \" で囲まず、7 のような数で書こう")
    for j in range(i):
        if spots[j][0] == spot[0]:
            raise SystemExit(f"「{spot[0]}」が2回出てくる（{j}番目と{i}番目）。名前は1つずつちがうものにしよう")
        if spots[j][1:] == spot[1:]:
            raise SystemExit(f"{spots[j][0]} と {spot[0]} が同じ位置 {spot[1:]} にある。どちらかの x か y を変えよう")
if type(WALK) not in (int, float) or WALK <= 0:
    raise SystemExit("WALK は 0 より大きい数（1 や 1.5 など）で書こう")
names = []                            # 場所の名前だけの並び
for spot in spots:
    names.append(spot[0])
first = None                          # 最初に行く場所の番号（決めないときは None）
if FIRST_VISIT is not None:
    if type(FIRST_VISIT) != str:
        raise SystemExit("FIRST_VISIT には場所の名前を \"ハリー・ポッター\" のように \" \" で囲んで書こう（決めないときは None）")
    if FIRST_VISIT == names[0]:
        raise SystemExit(f"FIRST_VISIT に0番の「{names[0]}」は選べない（出発する場所だから）。1番から後ろの場所の名前を書こう")
    if FIRST_VISIT not in names:
        raise SystemExit(f"FIRST_VISIT の「{FIRST_VISIT}」が spots にない。"
                         f"spots の名前を1文字もちがえずに書くか、None にもどそう")
    first = names.index(FIRST_VISIT)

n = len(spots)


def walk_minutes(a, b):
    """場所 a から場所 b まで歩く時間（分）。演習1と同じ計算"""
    dx = a[1] - b[1]
    dy = a[2] - b[2]
    return round(math.sqrt(dx ** 2 + dy ** 2) * WALK, 1)


minutes = []                          # 演習1と同じ歩く時間の表（こちらは半分にせず、全部のマスを計算する）
for i in range(n):
    row = []
    for j in range(n):
        row.append(walk_minutes(spots[i], spots[j]))
    minutes.append(row)


def tour_minutes(order):
    """エントランス（0番）を出て、order の順に回ってエントランスへ戻るまでの合計の分"""
    total = 0
    here = 0                          # いまいる場所（はじめはエントランス）
    for place in order:
        total = total + minutes[here][place]
        here = place
    total = total + minutes[here][0]  # 最後にエントランスへ戻る
    return round(total, 1)


def route_names(order):
    """順番を、名前の並び（最初と最後はエントランス）にする"""
    route = [names[0]]
    for place in order:
        route.append(names[place])
    route.append(names[0])
    return route


def route_numbers(order):
    """順番を「0 → 1 → 3 → … → 0」という番号の文字列にする（名前だと長くなるので）"""
    text = "0"
    for place in order:
        text = text + " → " + str(place)
    return text + " → 0"


# ---- 全探索: 0番以外の場所の並べ方を permutations ですべて作り、1つずつ合計の分を計算する ----
print(f"{TITLE}: {n}か所（エントランス＋{n - 1}か所）")
for i in range(n):
    print(f"  {i} = {names[i]}")
print(f"試す順番は ({n}-1)! = {math.factorial(n - 1):,}通り")
print("下の ( ) の中の数 = 0番を出たあとに回る場所の番号を、回る順に並べたもの（最後に0番へ戻る）")
print("-" * 50)
best_order = None                     # いまのところ最短の順番
best_total = None
first_order = None                    # FIRST_VISIT を最初に回る順番のうち、最短のもの
first_total = None
tried = []                            # 試した順の (順番, 合計)。窓の表示に使う
begin = time.perf_counter()           # いまの時刻（秒）
for order in permutations(range(1, n)):
    total = tour_minutes(order)
    tried.append((order, total))
    mark = ""
    if best_total is None or total < best_total:
        best_total = total            # 記録を書きかえる
        best_order = order
        mark = "  ← いまのところ最短"
    if first is not None and order[0] == first:
        if first_total is None or total < first_total:
            first_total = total
            first_order = order
    if len(tried) <= 24:              # 多いと画面があふれるので、最初の24通りだけ表示する
        print(f"  {order}  {total:>6}分" + mark)
seconds = time.perf_counter() - begin
if len(tried) > 24:
    print(f"  …（ここまで24通り。残りの {len(tried) - 24:,}通りは表示を省略）")
print("-" * 50)
print(f"試した順番: {len(tried):,}通り   かかった時間: {seconds:.3f}秒")
print()
print("いちばん早い順番:", route_numbers(best_order), f"（{best_total}分）")
back = tuple(reversed(best_order))    # 順番を逆に並べる（逆回り）
print("その逆回り      :", route_numbers(back), f"（{tour_minutes(back)}分。同じ道を反対向きに回るだけ）")
if first is not None:
    print()
    print(f"最初に {FIRST_VISIT} へ行く順番:", route_numbers(first_order), f"（{first_total}分）")
    late = round(first_total - best_total, 1)
    if late > 0:
        print(f"Lv3 達成: 最初に {FIRST_VISIT} へ行くと、いちばん早い順番より {late}分 おそくなる")
    else:
        print(f"Lv3: 最初に {FIRST_VISIT} へ行っても、いちばん早い順番と同じ {best_total}分（おそくならない場所だった）")
print()

# ---- 場所を増やしたら何秒かかるかを、このパソコンの速さから見積もる ----
#   試した順番が少ないと一瞬で終わって正しく測れないので、同じ全探索を 0.3秒 以上になるまでくり返して速さを測る
repeat = 0                            # くり返して試した順番の数
begin = time.perf_counter()
while time.perf_counter() - begin < 0.3:
    for order in permutations(range(1, n)):
        tour_minutes(order)
    repeat = repeat + len(tried)
speed = repeat / (time.perf_counter() - begin)     # 1秒あたりに試せる順番の数


def how_long(sec):
    """秒を、読みやすい単位（秒・分・時間・日・年）の文字にする。大きい単位から順に、1以上になる単位を使う"""
    for size, unit in [(365 * 24 * 3600, "年"), (24 * 3600, "日"), (3600, "時間"), (60, "分")]:
        if sec >= size:
            return f"約{sec / size:,.1f}{unit}"
    return f"約{sec:.2f}秒"


print(f"このパソコンは1秒に約 {speed:,.0f}通り を試せる。その速さで、場所を増やしたときの時間を見積もると")
print("-" * 46)
for places_count in sorted(set([n, 8, 10, 12, 15, 20])):
    if places_count < n:
        continue
    ways = math.factorial(places_count - 1)       # (場所の数 - 1)! 通り
    print(f"  {places_count:>3}か所   {ways:>22,}通り   {how_long(ways / speed)}")
print("-" * 46)
if n >= 8:
    print(f"Lv2 達成: {n}か所で {len(tried):,}通りを {seconds:.3f}秒 で全部試した")
print()
announce(route_names(best_order), best_total)


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


# --- 窓を開いて、全探索が順番を1つずつ試す様子をアニメーション表示する ---
# 橙の線 = いま試している順番、太い緑の線 = いまのところ最短。最後はいちばん早い順番と回る順番（丸の数字）
show_window(spots, tried, best_order, TITLE, "分")
