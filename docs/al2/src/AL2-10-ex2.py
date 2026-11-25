# 第10回 クリエイティブ演習2: ナガシマスパーランドの「本当にいちばん早い回り方」を、bitDP（ビットディーピー）で求める
# 第9回の全探索は10か所までしか動かせなかった。bitDP なら、15か所でも1秒かからずに「必ず最短」の答えが出る。
# 貪欲法（第9回）・全探索（第8回）・bitDP（今回）の3つを、答えの良さと速さで比べる。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: spots と WALK を、第9回（今回の演習1）で作った自分のものに貼りかえる（16か所まで）
#   Lv2: 場所を12か所以上にして、全探索では待てなかった数を bitDP で解く
#   Lv3: 場所を15か所以上にして bitDP の時間を測り、いちばん下の表で「bitDP にも限界がある」ことを確かめる
#   Lv4: announce 関数の print を書き換え、2つの回り方を自分らしく案内する
import math
import random
import time
from itertools import permutations

# ★ 窓のいちばん上に出る題名
TITLE = "ナガシマスパーランド: bitDP で本当の最短をさがす"

# ★ 回りたい場所 (名前, x, y)。第9回の spots をそのまま貼る。0番は出発して最後に戻る場所（メインゲート）
#   各行の最後のカンマ , を忘れない（忘れると 'tuple' object is not callable というエラーになる）
spots = [
    ("メインゲート", 9, 14),
    ("スチールドラゴン2000", 3, 5),
    ("白鯨", 15, 3),
    ("嵐", 6, 10),
    ("大観覧車オーロラ", 12, 8),
    ("アクロバット", 17, 10),
]

# ★ 地図の1目もりを歩くのにかかる時間（分）。第9回と同じにする
WALK = 1


def announce(greedy_route, greedy_total, best_route, best_total):
    """★ 2つの回り方の案内文を表示する。route = 回る場所の名前の並び（最初と最後は0番の場所）、total = 合計の分"""
    print(f"【さっと決めるコース（貪欲法）】 {greedy_total}分")
    print("   " + " → ".join(greedy_route))
    print(f"【必ずいちばん早いコース（bitDP）】 {best_total}分")
    print("   " + " → ".join(best_route))


# ------------------------------------------------------------
# ここから先は計算の本体（書き換えずに読むだけ）。bit_dp は例題2（参考）と同じ方法
#   参考の cities が spots に、距離が「歩く時間（分）」に変わっている。
#   参考より増えているのは、書きまちがいの検査・貪欲法（第9回）との比べ・場所を増やしたときの時間の表の部分
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
#   raise SystemExit("…") は、「…」を表示してプログラムを終わらせる命令
if type(TITLE) != str:
    raise SystemExit("TITLE は \"ナガシマ\" のように \" \" で囲んだ文字で書こう")
if type(spots) not in (list, tuple):
    raise SystemExit("spots は [ ] の中に (\"名前\", x, y), を1行ずつ並べて書こう")
if len(spots) < 4:
    raise SystemExit("spots が少なすぎる。3か所だと回り方が1通りしかなく、比べられない。"
                     "メインゲートのほかに3か所以上を (\"名前\", x, y), の形で書こう")
if len(spots) > 16:
    raise SystemExit(f"spots が {len(spots)}か所ある。bitDP の表が {(1 << len(spots)) * len(spots):,}マスになって"
                     "時間もメモリもかかるので、行の先頭に # を付けて、16か所までに減らそう")
for i in range(len(spots)):
    spot = spots[i]
    if type(spot) != tuple or len(spot) != 3:
        raise SystemExit(f"spots の {i}番目が (\"名前\", x, y) の形になっていない。かっこ ( ) と、カンマ2つで書こう")
    if type(spot[0]) != str or spot[0] == "":
        raise SystemExit(f"spots の {i}番目の名前が文字になっていない。\"白鯨\" のように \" \" で囲もう")
    if type(spot[1]) not in (int, float) or type(spot[2]) not in (int, float):
        raise SystemExit(f"spots の {i}番目（{spot[0]}）の位置がおかしい。x と y は \" \" で囲まず、7 のような数で書こう")
    for j in range(i):
        if spots[j][0] == spot[0]:
            raise SystemExit(f"「{spot[0]}」が2回出てくる（{j}番目と{i}番目）。名前は1つずつちがうものにしよう")
        if spots[j][1:] == spot[1:]:
            raise SystemExit(f"{spots[j][0]} と {spot[0]} が同じ位置 {spot[1:]} にある。どちらかの x か y を変えよう")
if type(WALK) not in (int, float) or WALK < 0.1:
    raise SystemExit("WALK は 0.1 以上の数（1 や 1.5 など）で書こう")

n = len(spots)                        # 場所の数
INF = float("inf")                    # 無限大。「まだたどり着いていない」の印として表に入れておく


def make_table(places):
    """歩く時間の表を作る（第8・9回と同じ計算）。table[i][j] = i番から j番まで歩く分"""
    table = []
    for i in range(len(places)):
        row = []
        for j in range(len(places)):
            dx = places[i][1] - places[j][1]
            dy = places[i][2] - places[j][2]
            row.append(round(math.sqrt(dx ** 2 + dy ** 2) * WALK, 1))
        table.append(row)
    return table


def bit_dp(table):
    """bitDP（例題2と同じ）。0番を出発して全部回り、0番へ戻るいちばん早い順番と合計の分を返す"""
    count = len(table)                # 場所の数
    full = (1 << count) - 1           # 全部の場所に行ったスタンプカード（1 が count 個ならぶ数）
    best = []                         # best[visited][here] = その状態までの、いちばん短い分
    prev = []                         # prev[visited][here] = その状態へ、どの場所から来たか
    for visited in range(1 << count):             # 表を作る。行は 2のcount乗 個（スタンプカードの種類）
        best.append([INF] * count)
        prev.append([None] * count)
    best[1 << 0][0] = 0               # はじめの状態: 0番だけ行って、0番にいる。0分

    # スタンプカードの数の、小さいほうから順に見る。スタンプを1つ押すと、数は必ず大きくなるので、
    # 小さい順に見れば、ある行を読むときには、その行の値はもう決まっている
    for visited in range(1 << count):
        for here in range(count):
            if best[visited][here] == INF:        # たどり着けない状態は飛ばす
                continue
            for next_place in range(count):       # ここから次に行く場所を、全部ためす
                if visited & (1 << next_place):   # もう行った場所へは行かない（演習1の & ）
                    continue
                new_visited = visited | (1 << next_place)         # スタンプを1つ押す（演習1の | ）
                new_total = best[visited][here] + table[here][next_place]
                if new_total < best[new_visited][next_place]:     # いま表にある値より早いときだけ、書きかえる
                    best[new_visited][next_place] = new_total
                    prev[new_visited][next_place] = here

    answer = INF                      # 全部行った行のうち、0番へ戻る分を足して、いちばん早いものをえらぶ
    last = None
    for here in range(1, count):
        total = best[full][here] + table[here][0]
        if total < answer:
            answer = total
            last = here

    route = []                        # prev を後ろから前へたどって、回る順番を作る
    visited = full
    here = last
    while here is not None:
        route.append(here)
        came_from = prev[visited][here]           # here へ来る前にいた場所
        visited = visited - (1 << here)
        here = came_from
    route.reverse()
    return route, round(answer, 1)


def greedy(table, start):
    """貪欲法（第9回と同じ）。いちばん近い場所へ進むことをくり返す。回る順番と合計の分を返す"""
    count = len(table)
    visited = [start]                 # こちらの visited は、行った場所の番号を行った順に入れるリスト
    total = 0
    here = start
    while len(visited) < count:
        nearest = None
        for j in range(count):
            if j in visited:
                continue
            if nearest is None or table[here][j] < table[here][nearest]:
                nearest = j
        total = total + table[here][nearest]
        visited.append(nearest)
        here = nearest
    total = total + table[here][start]
    return visited, round(total, 1)


def brute_force(table):
    """全探索（第8回と同じ）。いちばん早い順番・合計の分・試した順番の数を返す"""
    best_order = None
    best_total = None
    tried = 0
    for order in permutations(range(1, len(table))):
        total = 0
        here = 0
        for place in order:
            total = total + table[here][place]
            here = place
        total = total + table[here][0]
        tried = tried + 1
        if best_total is None or total < best_total:
            best_total = total
            best_order = order
    return [0] + list(best_order), round(best_total, 1), tried


def route_names(route):
    """回る順番（番号）を、名前の並びにする（最後に、出発した場所を足す）"""
    result = []
    for place in route:
        result.append(spots[place][0])
    result.append(spots[route[0]][0])
    return result


def how_long(sec):
    """秒を、読みやすい単位（秒・分・時間・日・年）の文字にする。とても大きいときは「10の何乗 年」と書く"""
    years = sec / (365 * 24 * 3600)
    if years >= 1000000:
        return f"約10の{len(str(int(years))) - 1}乗 年"
    for size, unit in [(365 * 24 * 3600, "年"), (24 * 3600, "日"), (3600, "時間"), (60, "分")]:
        if sec >= size:
            return f"約{sec / size:,.1f}{unit}"
    if sec < 0.01:
        return "0.01秒より短い"
    return f"約{sec:.2f}秒"


minutes = make_table(spots)

# ---- 貪欲法と bitDP で解いて、かかった時間を測る（time.perf_counter() は、いまの時刻を秒で返す）----
begin = time.perf_counter()
greedy_route, greedy_total = greedy(minutes, 0)
greedy_seconds = time.perf_counter() - begin

begin = time.perf_counter()
best_route, best_total = bit_dp(minutes)
dp_seconds = time.perf_counter() - begin

# ---- 全探索の速さを測る: 7か所ぶんの全探索を 0.3秒 以上くり返し、1秒あたりに試せる順番の数を出す（第8回と同じ）----
sample = make_table(spots[:7])
repeat = 0
begin = time.perf_counter()
while time.perf_counter() - begin < 0.3:
    repeat = repeat + brute_force(sample)[2]
speed = repeat / (time.perf_counter() - begin)

print(f"{TITLE}: {n}か所（{spots[0][0]}＋{n - 1}か所）")
print("-" * 66)
print("貪欲法（第9回: いちばん近い場所へ進む）")
print("  " + " → ".join(route_names(greedy_route)))
print(f"  合計: {greedy_total}分   かかった時間: {greedy_seconds:.6f}秒")
print()
print("bitDP（今回: 表を埋めて、必ずいちばん早い回り方を出す）")
print("  " + " → ".join(route_names(best_route)))
print(f"  合計: {best_total}分   かかった時間: {dp_seconds:.6f}秒   表のマス: {(1 << n) * n:,}個")
print()
print("全探索（第8回: 全部の順番を試す）")
if n <= 10:                           # 10か所までは、全探索も本当に動かして、bitDP と同じ答えになるかを確かめる
    begin = time.perf_counter()
    brute_route, brute_total, tried = brute_force(minutes)
    brute_seconds = time.perf_counter() - begin
    print(f"  合計: {brute_total}分   かかった時間: {brute_seconds:.6f}秒   試した順番: {tried:,}通り")
    if brute_total == best_total:
        print("  → bitDP と同じ合計。bitDP は、全探索と同じく必ず最短を出す")
    else:
        print("  → bitDP と合計がちがう。bit_dp 関数を書きかえていないか、参考と見比べよう")
else:                                 # 11か所以上は、全探索を動かすと長すぎるので、見積もりだけ出す
    print(f"  試す順番が {math.factorial(n - 1):,}通りあり、このパソコンでは {how_long(math.factorial(n - 1) / speed)} かかる見積もり（動かさない）")
print("-" * 66)
late = round(greedy_total - best_total, 1)
percent = round(late / best_total * 100, 1)        # 差が、いちばん早い回り方の何%にあたるか
if late > 0:
    print(f"貪欲法は、いちばん早い回り方より {late}分 おそい（{percent}% 長い）")
else:
    print("貪欲法が、いちばん早い回り方と同じ時間になった（たまたま当たった。いつもそうなるとはかぎらない）")
if n >= 12:
    print(f"Lv2 達成: 全探索なら {how_long(math.factorial(n - 1) / speed)} かかる {n}か所を、bitDP は {dp_seconds:.2f}秒 で解いた")
else:
    print(f"Lv2 はまだ: いまは {n}か所。12か所以上にして、全探索では待てない数を bitDP で解こう")
if n >= 15:
    print(f"Lv3 達成: {n}か所（表は {(1 << n) * n:,}マス）を {dp_seconds:.2f}秒 で解いた。下の表で、20か所・25か所の見積もりを見よう")
else:
    print("Lv3 はまだ: 場所を15か所以上にして、bitDP の時間を測ろう")
print()

# ---- いちばん早い回り方を、表の状態（スタンプカード, いまいる場所）でたどる ----
#   bitDP の表では、1か所進むたびに「スタンプが1つ増えた行」の「いまいる場所の列」へ移っていく
print("いちばん早い回り方を、表の状態（スタンプカード, いまいる場所）でたどる")
print("-" * 66)
visited = 0                           # スタンプカード（演習1と同じ数）
total = 0.0                           # ここまでに歩いた分
for k in range(n):
    place = best_route[k]
    if k > 0:
        total = total + minutes[best_route[k - 1]][place]
    visited = visited | (1 << place)  # place 番のスタンプを押す
    print(f"  {format(visited, '0' + str(n) + 'b')}  ここまで {round(total, 1):>5}分   いま {spots[place][0]}")
back = minutes[best_route[-1]][0]
print(f"  最後に {spots[0][0]} へ戻る {back}分 を足して、合計 {best_total}分")
print("-" * 66)
# 同じ状態に、別の順番でもたどり着ける。表には、早いほうだけが残る
p1 = best_route[1]                    # いちばん早い回り方で、1番目・2番目・3番目に行く場所の番号
p2 = best_route[2]
p3 = best_route[3]
this_way = round(minutes[0][p1] + minutes[p1][p2] + minutes[p2][p3], 1)
other_way = round(minutes[0][p2] + minutes[p2][p1] + minutes[p1][p3], 1)       # 1番目と2番目を入れかえた順番
state = (1 << 0) | (1 << p1) | (1 << p2) | (1 << p3)
print(f"上から4行目の状態（{format(state, '0' + str(n) + 'b')}, いま {spots[p3][0]}）には、2つの順番でたどり着ける")
print(f"  {spots[0][0]} → {spots[p1][0]} → {spots[p2][0]} → {spots[p3][0]}: {this_way}分")
print(f"  {spots[0][0]} → {spots[p2][0]} → {spots[p1][0]} → {spots[p3][0]}: {other_way}分")
if this_way < other_way:
    print(f"  → 表に残るのは、早いほうの {this_way}分だけ。おそいほうの続きは、もう調べない")
else:
    print(f"  → 2つは同じ {this_way}分。表には、その1つの値だけが残る")
print()

# ---- 場所を増やすと、3つの方法の時間はどうなるか ----
#   貪欲法: でたらめな位置の場所を作って、本当に動かして測る
#   bitDP : 15か所（自分の場所がもっと多ければ、その数）までは本当に動かす。それより多い数は、
#           「調べる量 = 2のn乗 × n × n」が何倍になるかから見積もる
#   全探索: 上で測った速さから見積もる
print("場所を増やしたときの時間（「見積もり」と書いていないものは、でたらめな位置の場所で本当に動かした時間）")
print("-" * 78)
random.seed(10)                       # でたらめな数の出方を固定する（毎回同じ場所になる）
measured = max(n, 15)                 # bitDP を本当に動かす、いちばん多い場所の数
base_seconds = None                   # measured か所のときの、bitDP の時間
counts = [10, 12, 15, 20, 25]         # 調べる場所の数（自分の場所の数が入っていなければ足す）
if n not in counts:
    counts.append(n)
    counts.sort()                     # 小さい順に並べなおす
for count in counts:
    places = []
    for i in range(count):
        places.append((f"場所{i}", random.randint(0, 99), random.randint(0, 99)))
    table = make_table(places)
    begin = time.perf_counter()
    greedy(table, 0)
    seconds = time.perf_counter() - begin
    if count <= measured:
        begin = time.perf_counter()
        bit_dp(table)
        dp_time = time.perf_counter() - begin
        dp_text = how_long(dp_time)
        if count == measured:
            base_seconds = dp_time
    else:
        times = ((1 << count) * count * count) / ((1 << measured) * measured * measured)   # 調べる量が何倍か
        dp_text = how_long(base_seconds * times) + "（見積もり）"
    brute_text = how_long(math.factorial(count - 1) / speed) + "（見積もり）"
    print(f"  {count:>2}か所: 貪欲法 {seconds:.6f}秒 / bitDP {dp_text} / 全探索 {brute_text}")
print("-" * 78)
print(f"  25か所の bitDP の表は {(1 << 25) * 25:,}マス。時間より先に、パソコンのメモリ（覚えておける量）が足りなくなる")
print()
announce(route_names(greedy_route), greedy_total, route_names(best_route), best_total)


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
    """左に貪欲法のルート、右に bitDP のルート（本当の最短）を並べて表示する。
    左は1本ずつ線が増えていき、最後の手順で右に bitDP の答えが出る。"""
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
    last_step = n + 1                              # n本の線を引いたあと、最後の1手順で bitDP の答えを出す
    # bitDP のルートを、貪欲法と同じ出発点から始まるように並べなおす（同じ輪なので、合計は変わらない）
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
            screen.blit(mid.render(f"bitDP（本当の最短）: 合計 {best_total}{unit}", True, GREEN), (30 + map_w + 30, 68))
        else:
            _draw_places(screen, fonts, right, places, None, start)
            screen.blit(mid.render("bitDP（本当の最短）: 最後に表示", True, SUB), (30 + map_w + 30, 68))
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


# --- 窓を開いて、貪欲法の回り方（左）と bitDP の回り方（右）を並べて表示する ---
show_window(spots, greedy_route, greedy_total, best_route, best_total, TITLE, "分")
