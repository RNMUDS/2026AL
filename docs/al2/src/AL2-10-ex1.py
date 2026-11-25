# 第10回 クリエイティブ演習1: ナガシマスパーランドの「行った場所のスタンプカード」を、数1つで作る
# 行った場所のけたを 1、まだの場所のけたを 0 にした2進数が、スタンプカードになる（右はしが0番の場所）。
# 演習2の bitDP（ビットディーピー）は、このスタンプカードの数を、表の行の番号としてそのまま使う。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: spots を第9回で作った自分のものに貼りかえ、been（もう行った場所）と NEXT（次に行く場所）を自分で決める
#   Lv2: CODE を「全部の場所に行った」ことを表す数にする（ひな形の 21 は、まだ未達成）
#   Lv3: 場所を10か所以上にして、「集合の数」と「順番の数」のちがいを確かめる（16か所まで増やせる）
#   Lv4: announce 関数の print を書き換え、自分らしい案内文にする
import math

# ★ 窓のいちばん上に出る題名
TITLE = "ナガシマスパーランド: 行った場所のスタンプカード"

# ★ 回りたい場所 (名前, x, y)。第9回の演習で作った spots をそのまま貼る。0番は入り口（メインゲート）
#   位置 x・y は、この演習1では使わない（演習2で使う）。番号は、上から 0番、1番、2番、…
#   各行の最後のカンマ , を忘れない（忘れると 'tuple' object is not callable というエラーになる）
spots = [
    ("メインゲート", 9, 14),
    ("スチールドラゴン2000", 3, 5),
    ("白鯨", 15, 3),
    ("嵐", 6, 10),
    ("大観覧車オーロラ", 12, 8),
    ("アクロバット", 17, 10),
]

# ★ もう行った場所の名前（0番のメインゲートは、入った時点で「行った」になるので書かなくてよい）
been = ["嵐", "スチールドラゴン2000"]

# ★ 次に行きたい場所の名前
NEXT = "白鯨"

# ★ なぞの数。スタンプカードにもどすと、どの場所に行ったことになるかを読みとく
CODE = 21


def announce(stamped, left):
    """★ 案内文を表示する。stamped = スタンプがある場所の名前のリスト、left = まだ行っていない場所の名前のリスト"""
    print(f"【スタンプカード】 いま {len(stamped)}か所。あと {len(left)}か所で全部！")
    if len(left) > 0:
        print("   まだ行っていない場所: " + "、".join(left))


# ------------------------------------------------------------
# ここから先は計算の本体（書き換えずに読むだけ）。例題1（参考）と同じ3つの記号 <<  |  & を使っている
#   参考の city_names が spots の名前に変わっている。
#   参考より増えているのは、書きまちがいの検査と、CODE（数から場所を読みとく）の部分
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
#   raise SystemExit("…") は、「…」を表示してプログラムを終わらせる命令
if type(TITLE) != str:
    raise SystemExit("TITLE は \"ナガシマ\" のように \" \" で囲んだ文字で書こう")
if type(spots) not in (list, tuple):
    raise SystemExit("spots は [ ] の中に (\"名前\", x, y), を1行ずつ並べて書こう")
if len(spots) < 3:
    raise SystemExit("spots が少なすぎる。メインゲートのほかに2か所以上を (\"名前\", x, y), の形で書こう")
if len(spots) > 16:
    raise SystemExit(f"spots が {len(spots)}か所ある。窓に入りきらなくなるので16か所までにしよう")
names = []                            # 場所の名前だけの並び（names[i] = i番の場所の名前）
for i in range(len(spots)):
    spot = spots[i]
    if type(spot) != tuple or len(spot) != 3:
        raise SystemExit(f"spots の {i}番目が (\"名前\", x, y) の形になっていない。かっこ ( ) と、カンマ2つで書こう")
    if type(spot[0]) != str or spot[0] == "":
        raise SystemExit(f"spots の {i}番目の名前が文字になっていない。\"白鯨\" のように \" \" で囲もう")
    if spot[0] in names:
        raise SystemExit(f"「{spot[0]}」が2回出てくる。名前は1つずつちがうものにしよう")
    names.append(spot[0])
if type(been) not in (list, tuple):
    raise SystemExit("been は [\"嵐\", \"白鯨\"] のように、[ ] の中に名前をカンマで区切って書こう（1つもないときは [] ）")
for name in been:
    if name not in names:
        raise SystemExit(f"been の「{name}」が spots にない。spots の名前を1文字もちがえずに書こう（コピーして貼るとよい）")
    if been.count(name) > 1:
        raise SystemExit(f"been に「{name}」が2回出てくる。同じ場所は1回だけ書こう")
if NEXT not in names:
    raise SystemExit(f"NEXT の「{NEXT}」が spots にない。番号ではなく、spots の名前を1文字もちがえずに、\" \" で囲んで書こう")

n = len(spots)                        # 場所の数
full = (1 << n) - 1                   # 全部の場所に行ったことを表す数（1 が n 個ならぶ。6か所なら 111111 = 63）
if type(CODE) != int or CODE < 0 or CODE > full:
    raise SystemExit(f"CODE は 0 から {full} までの整数で書こう（{n}か所なので、{n}けたの2進数で表せる数まで）")

frames = []                           # 窓に見せる記録 (説明, 式, スタンプカードの数, 注目するけた)


def binary(bits):
    """bits を、場所の数と同じけた数の2進数の文字にする（6か所なら 5 → "000101"）"""
    return format(bits, "0" + str(n) + "b")


def members(bits):
    """bits が表すスタンプカードで、スタンプがある場所の名前をリストにして返す"""
    result = []
    for i in range(n):
        if bits & (1 << i):           # i番のけたが 1 なら、i番の場所に行った
            result.append(names[i])
    return result


# ---- (1) 場所1つを表す数: 1 << i ----
print(f"{TITLE}: {n}か所")
print("場所1つを表す数（1 << i = 1 を左へ i けたずらした数）")
print("-" * 64)
for i in range(n):
    print(f"  {i:>2}番: 1 << {i:<2} = {1 << i:>5} = 2進数 {binary(1 << i)}   {names[i]}")
print("-" * 64)
print()

# ---- (2) 行った場所のスタンプを押す: visited | (1 << i) ----
visited = 1 << 0                      # はじめは、0番（入り口）だけ行った状態（= 1）
frames.append((f"はじめ: 0番の{names[0]}だけ", "visited = 1 << 0", visited, 0))
print("行った場所のスタンプを押す（visited | (1 << i)）")
print("-" * 64)
print(f"  はじめ    : {binary(visited)} = {visited:>5}   （0番の {names[0]} だけ）")
for name in been:
    i = names.index(name)             # 名前が何番の場所かを調べる
    before = visited
    visited = visited | (1 << i)      # i番のけたを 1 にする（もう 1 なら、何も変わらない）
    print(f"  {i:>2}番を押す: {binary(visited)} = {visited:>5}   （{name}）")
    frames.append((f"{name}（{i}番）のスタンプを押す", f"{binary(before)} | {binary(1 << i)} = {binary(visited)}", visited, i))
print("-" * 64)
print(f"いまのスタンプカード: {binary(visited)} = {visited}   行った場所: " + "、".join(members(visited)))
print()

# ---- (3) 次に行きたい場所は、もう行ったか: visited & (1 << i) ----
i = names.index(NEXT)
result = visited & (1 << i)           # 行っていれば 0 以外、まだなら 0
print(f"次に行きたい {NEXT}（{i}番）は、もう行ったか（visited & (1 << i)）")
print(f"  {binary(visited)} & {binary(1 << i)} = {binary(result)}")
if result:                            # 0 以外の数は、if では「はい」として扱われる
    print(f"  → 0 ではないので、もう行った。bitDP では、行った場所へは進まない")
    frames.append((f"{NEXT}（{i}番）は、もう行った（& の答えが 0 ではない）",
                   f"{binary(visited)} & {binary(1 << i)} = {binary(result)}", visited, i))
else:
    before = visited
    visited = visited | (1 << i)
    print(f"  → 0 なので、まだ行っていない。行ってスタンプを押すと {binary(visited)} = {visited}")
    frames.append((f"{NEXT}（{i}番）は、まだ行っていない（& の答えが 0）",
                   f"{binary(before)} & {binary(1 << i)} = {binary(result)}", before, i))
    frames.append((f"{NEXT}（{i}番）へ行って、スタンプを押す", f"{binary(before)} | {binary(1 << i)} = {binary(visited)}", visited, i))
print()

# ---- (4) 数から、行った場所を読みとく ----
print(f"なぞの数 CODE = {CODE} を、スタンプカードにもどす")
print(f"  {CODE} = 2進数 {binary(CODE)}   行った場所: " + ("、".join(members(CODE)) if CODE else "（なし）"))
frames.append((f"なぞの数 CODE = {CODE} を、スタンプカードにもどす", f"CODE = {CODE}", CODE, None))
if CODE == full:
    print(f"Lv2 達成: {CODE} は、{n}か所ぜんぶに行ったことを表す数（1 が {n}個ならぶ。(1 << {n}) - 1 でも計算できる）")
else:
    print(f"Lv2 はまだ: 「{n}か所ぜんぶに行った」を表す数を CODE に書こう（ヒント: 2進数で 1 が {n}個ならぶ数）")
print()

# ---- (5) スタンプカードは何種類あるか ----
print(f"スタンプカードの種類（集合の数）: 2の{n}乗 = {1 << n:,} 通り（0 から {full:,} まで）")
print(f"回る順番の数（全探索が試す数）  : ({n}-1)! = {math.factorial(n - 1):,} 通り")
print(f"bitDP の表のマスの数            : {1 << n:,} × {n} = {(1 << n) * n:,} 個（集合の数 × いまいる場所）")
if n >= 10:
    times = math.factorial(n - 1) / ((1 << n) * n)
    print(f"Lv3 達成: {n}か所では、順番の数が表のマスの数の 約{times:,.0f}倍 ある。bitDP は、マス1つにつき次の場所を {n}通り ためすだけですむ")
else:
    print(f"Lv3 はまだ: いまは {n}か所。10か所以上にして、順番の数と表のマスの数を比べよう")
print()

stamped = members(visited)
left = []                             # まだ行っていない場所
for i in range(n):
    if not (visited & (1 << i)):      # i番のスタンプがない
        left.append(names[i])
announce(stamped, left)


# ============================================================
# ここから下は、数のけた（1 と 0）を pygame の窓に絵で表示するための道具です。
# 中身は読まなくてかまいません（アルゴリズムは上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

STEP_MS = 900                   # 1手順あたりの時間（ミリ秒）
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



def _draw_legend(screen, fonts, names, top, columns):
    """けたの番号と名前の対応を、窓の下に並べる。"""
    small = fonts[2]
    for i, name in enumerate(names):
        col, row = i % columns, i // columns
        t = small.render(_fit(small, f"{i}番 = {name}", 218), True, AMBER if i == 0 else SUB)
        screen.blit(t, (30 + col * 230, top + row * 22))


def show_window(names, frames, title):
    """集合を表す数を、1 と 0 のマスの列で表示する（右はしが0番のけた）。
    frames = [(説明, 式, 集合を表す数, 注目するけた), …] を、1手順に1つずつ見せる。"""
    pygame.init()
    n = len(names)
    width = 980
    cell = min(110, (width - 60) // n)             # マス1つの幅
    left = (width - cell * n) // 2
    height = 150 + 96 + 150 + 22 * ((n + 3) // 4) + 46
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    digit = _font(40, True)
    last_step = len(frames) - 1

    def draw(k):
        caption, formula, bits, focus = frames[k]
        screen.blit(big.render(_fit(big, title, width - 60), True, GREEN), (30, 18))
        screen.blit(mid.render(_fit(mid, f"{k}手順目: {caption}", width - 60), True, TEXT), (30, 62))
        screen.blit(mid.render(_fit(mid, formula, width - 60), True, AMBER), (30, 94))
        for i in range(n):
            x = left + (n - 1 - i) * cell          # 0番のけたを、いちばん右に置く
            on = bool(bits & (1 << i))
            box = pygame.Rect(x + 4, 150, cell - 8, 96)
            pygame.draw.rect(screen, (26, 46, 10) if on else PANEL, box, border_radius=10)
            pygame.draw.rect(screen, WHITE if i == focus else (GREEN if on else LINE), box, 4 if i == focus else 2,
                             border_radius=10)
            t = digit.render("1" if on else "0", True, GREEN if on else LINE)
            screen.blit(t, (box.centerx - t.get_width() // 2, box.centery - t.get_height() // 2 + 2))
            label = small.render(f"{i}番", True, AMBER if i == 0 else SUB)
            screen.blit(label, (box.centerx - label.get_width() // 2, 128))
            if cell >= 90:                         # マスが広いときは、名前も下に書く
                name = small.render(_fit(small, names[i], cell - 6), True, TEXT if on else SUB)
                screen.blit(name, (box.centerx - name.get_width() // 2, 252))
        by = 290
        number = format(bits, "0" + str(n) + "b")
        screen.blit(big.render(f"2進数 {number}  =  10進数 {bits}", True, TEXT), (30, by))
        inside = [names[i] for i in range(n) if bits & (1 << i)]
        text = "入っているもの: " + ("、".join(inside) if inside else "（なし）")
        screen.blit(mid.render(_fit(mid, text, width - 60), True, GREEN), (30, by + 40))
        note = "緑のマス = 1（入っている）。白いわく = いま足した・調べたけた。右はしが0番のけた"
        screen.blit(small.render(_fit(small, note, width - 60), True, SUB), (30, by + 76))
        _draw_legend(screen, fonts, names, by + 106, 4)

    _loop(screen, fonts, last_step, draw,
          "スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる")


# --- 窓を開いて、スタンプカードが変わっていくようすを表示する ---
show_window(names, frames, TITLE)
