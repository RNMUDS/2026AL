# 第10回 例題1（参考）: 「どの都市を回ったか」を、数1つ（2進数）で表す練習
# 都市が5個あるとき、「回った・回っていない」を5けたの 1 と 0 で表す。
#   いちばん右のけたが 0番の都市、その左が 1番の都市、…（1 = 回った、0 = まだ）
# 使う記号は3つだけ:  <<（ずらす）   |（集合に入れる）   &（入っているか調べる）

# 都市の名前。第8・9回と同じ5都市（0番 = 学校、1番 = 郵便局、…）
city_names = ["学校", "郵便局", "図書館", "カフェ", "公園"]
n = len(city_names)           # 都市の数

frames = []                   # 窓に見せる記録 (説明, 式, 集合を表す数, 注目するけた)


def binary(bits):
    """bits を、都市の数と同じけた数の2進数の文字にする（5都市なら 5 → "00101"）"""
    return format(bits, "0" + str(n) + "b")


def members(bits):
    """bits が表す集合に入っている都市の名前を、リストにして返す"""
    result = []
    for i in range(n):
        if bits & (1 << i):           # i番のけたが 1 なら、i番の都市が入っている
            result.append(city_names[i])
    return result


def show(bits):
    """bits を「10進数 = 2進数 → 都市の名前」の形で表示する"""
    names = "、".join(members(bits))
    if names == "":
        names = "（まだどこにも行っていない）"
    print(f"  {bits:>2} = 2進数 {binary(bits)}  →  {names}")


# ---- (1) 数1つが、集合1つを表す ----
print("数1つで「回った都市の集合」を表す")
print("-" * 52)
for bits in [0, 1, 3, 5, 31]:
    show(bits)
print("-" * 52)
print()

# ---- (2) 1つの都市だけを表す数: 1 << i（1 を左へ i けたずらす）----
print("1つの都市だけを表す数（1 << i は「1 を左へ i けたずらす」）")
print("-" * 52)
for i in range(n):
    print(f"  {i}番: 1 << {i} = {1 << i:>2} = 2進数 {binary(1 << i)}   {city_names[i]}")
print("-" * 52)
print()

# ---- (3) 集合に都市を1つ足す: visited | (1 << i) ----
#   | は、けたごとに「どちらかが 1 なら 1」にする。もとの 1 はそのままで、i番のけたが 1 になる
#   ふつうの足し算（+）とはちがい、もう入っている都市を足しても変わらない（5 | 1 は 5 のまま）
print("集合に都市を1つ足す（visited | (1 << i)）")
print("-" * 52)
visited = 0                           # はじめは、どこにも行っていない（00000）
frames.append(("はじめ: まだどこにも行っていない", "visited = 0", visited, None))
for i in range(n):
    before = visited
    visited = visited | (1 << i)      # i番の都市を足す
    print(f"  {binary(before)} に {city_names[i]} を足す → {binary(visited)}（= {visited}）")
    frames.append((f"{city_names[i]}を足す（{i}番のけたが 1 になる）",
                   f"{binary(before)} | {binary(1 << i)} = {binary(visited)}", visited, i))
print("-" * 52)
print()

# ---- (4) 集合に都市が入っているか調べる: visited & (1 << i) ----
#   & は、けたごとに「両方が 1 のときだけ 1」にする。i番のけたが 0 なら、答えは 0 になる
print("集合に都市が入っているか調べる（visited & (1 << i)）")
print("-" * 52)
visited = 5                           # 00101 = 学校と図書館
print(f"  いまの集合: {binary(visited)}（= {visited}）")
frames.append(("集合を 5 にして、入っているかを1つずつ調べる", "visited = 5", visited, None))
for i in range(n):
    result = visited & (1 << i)       # 入っていれば 0 以外、入っていなければ 0
    if result:                        # 0 以外の数は、if では「はい」として扱われる
        answer = "入っている"
    else:
        answer = "入っていない"
    print(f"    {city_names[i]}: {binary(visited)} & {binary(1 << i)} = {binary(result)} → {answer}")
    frames.append((f"{city_names[i]}は{answer}", f"{binary(visited)} & {binary(1 << i)} = {binary(result)}", visited, i))
print("-" * 52)
print()
# 1 << n は「1 を左へ n けたずらした数」= 2 を n 回かけた数（2の n乗）
print(f"{n}個の都市なら、集合の種類は 2の{n}乗 = {1 << n} 通り（0 から {(1 << n) - 1} まで）")


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


# --- 窓を開いて、集合を表す数が変わっていくようすを表示する ---
show_window(city_names, frames, "集合を数1つで表す: | で足す、& で調べる")
