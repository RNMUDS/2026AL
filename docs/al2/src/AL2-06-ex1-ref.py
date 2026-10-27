# heapq の使い方: 入れた順番に関係なく、いちばん小さいものから取り出せる箱
import heapq

log = []        # 窓の表示に使う記録
taken = []      # 取り出したものを、取り出した順に並べる（窓の表示に使う）


def record(text, kind, box, item=None):
    """いまの箱の中身を、窓の表示のために写して残す（kind は "push"・"pop"・"info" のどれか）"""
    hot = box.index(item) if item in box else None
    log.append((text, kind, list(box), hot, list(taken)))


# ---- 前半: 数を入れて取り出す ----
numbers = []            # heapq の箱。ふつうのリストを使う
record("前半: 空っぽの箱に、数を1つずつ heappush で入れる", "info", numbers)
for value in [8, 3, 5, 1, 9, 2]:
    heapq.heappush(numbers, value)                  # 箱に1つ入れる
    print(f"{value} を入れた → 中身: {numbers}")
    record(f"heappush で {value} を入れた", "push", numbers, value)

print()
print("中身の並びはバラバラに見えるが、先頭は必ずいちばん小さい数になっている")
print("いまの先頭:", numbers[0])                     # numbers[0] で、取り出さずに先頭を見る
print()

print("取り出す順番")
while len(numbers) > 0:
    smallest = heapq.heappop(numbers)               # いちばん小さい数を取り出す（箱からは消える）
    taken.append(smallest)
    print(f"  取り出した: {smallest}   残り: {numbers}")
    record(f"heappop で {smallest} を取り出した（いちばん小さい数）", "pop", numbers)

print()
print("入れた順番は 8, 3, 5, 1, 9, 2 だが、取り出す順番は小さい順になる")
print("-" * 52)
print()

# ---- 後半: (時間, 駅名) の組を入れて取り出す ----
taken = []
tasks = []
# 組どうしは1番目の数（時間）でくらべる。1番目が同じときは、2番目（駅名）でくらべる
record("後半: (時間, 駅名) の組を入れる。組は1番目の数（時間）でくらべる", "info", tasks)
for pair in [(16, "品川"), (7, "渋谷"), (21, "上野"), (9, "池袋")]:
    heapq.heappush(tasks, pair)
    record(f"heappush で {pair} を入れた", "push", tasks, pair)

print("(時間, 駅名) の組を入れて取り出す")
while len(tasks) > 0:
    minutes, station = heapq.heappop(tasks)         # 取り出した組を、時間と駅名に分けて受け取る
    taken.append((minutes, station))
    print(f"  {minutes}分の {station} を取り出した")
    record(f"heappop で ({minutes}, {station}) を取り出した", "pop", tasks)

print()
print("1番目の要素（時間）が小さい順に出てくる")
print("ダイクストラ法では、この形をそのまま使う")


# ============================================================
# ここから下は、heapq の箱の中身を pygame の窓に「木の形」と「リスト」で表示するための道具です。
# 中身は読まなくてかまいません（heapq の使い方は上の部分にあります）。
# 操作: スペース = 再生／一時停止   → = 1手順すすめる   R = 最初から   Esc = 終わる
# ============================================================
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")   # pygame のあいさつ文を出さない
import pygame

WIDTH, HEIGHT = 1060, 620       # 窓の大きさ（ピクセル）
STEP_MS = 1100                  # 1手順あたりの時間（ミリ秒）
BG = (18, 18, 24)
LINE = (80, 84, 100)
NODE = (38, 40, 52)
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


def _shrink(t, width):
    """t（文字の絵）が width より広ければ、width に収まるように縮める。"""
    if t.get_width() <= width:
        return t
    k = width / t.get_width()
    return pygame.transform.smoothscale(t, (int(t.get_width() * k), int(t.get_height() * k)))


def _lines(item):
    """箱の中の1つを、木の札に書く1〜2行の文字にする。(40, "名前") の組なら「40分」と「名前」の2行。"""
    if type(item) == tuple:
        return [f"{item[0]}分", str(item[1])]
    return [str(item)]


def _short(item):
    """箱の中の1つを、1行の短い文字にする。"""
    return f"({item[0]}, {item[1]})" if type(item) == tuple else str(item)


def _loop(screen, fonts, last_step, draw):
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
        hint = fonts[2].render("スペース: 再生／一時停止   →: 1手順すすめる   R: 最初から   Esc: 終わる", True, SUB)
        screen.blit(hint, (30, HEIGHT - 30))
        pygame.display.flip()
        if capture:
            pygame.image.save(screen, capture)
            pygame.quit()
            return
        clock.tick(30)


def show_window(log, title, done_label="取り出した順"):
    """heapq の箱の中身が、heappush と heappop で変わっていくようすを表示する。窓を閉じると終わる。
    log = [(説明, 色の名前, 箱の中身, 光らせる番号, 取り出したものの一覧), ...]"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    fonts = (_font(22, True), _font(18), _font(14))
    big, mid, small = fonts
    colors = {"push": AMBER, "pop": GREEN, "skip": RED, "info": TEXT}
    last_step = len(log) - 1
    tree_w = 640                                # 木を描く場所の幅（左側）
    x1 = 680                                    # リストを描く場所の左端（右側）

    def tree(heap, hot):
        """箱の中身を木の形で描く。i 番目の子は 2*i+1 番目と 2*i+2 番目。"""
        if not heap:
            screen.blit(mid.render("（箱は空っぽ）", True, SUB), (tree_w // 2 - 60, 200))
            return
        depth = len(heap).bit_length()          # 何段になるか
        gap_y = min(110, (HEIGHT - 300) // max(depth - 1, 1))
        spots = []
        for i in range(len(heap)):
            level = (i + 1).bit_length() - 1
            first = 2 ** level - 1
            slot = tree_w / 2 ** level
            spots.append((20 + slot * (i - first + 0.5), 170 + level * gap_y))
        w = min(150, tree_w / 2 ** (depth - 1) - 10)
        h = 50 if type(heap[0]) == tuple else 40
        for i in range(1, len(heap)):
            px, py = spots[(i - 1) // 2]
            x, y = spots[i]
            bad = heap[(i - 1) // 2] > heap[i]  # きまり（親 ≦ 子）が崩れていたら赤（ふつうは起きない）
            pygame.draw.line(screen, RED if bad else LINE, (px, py + h / 2), (x, y - h / 2), 2)
        for i, item in enumerate(heap):
            x, y = spots[i]
            box = pygame.Rect(0, 0, w, h)
            box.center = (x, y)
            ring = GREEN if i == 0 else (AMBER if i == hot else LINE)
            pygame.draw.rect(screen, NODE, box, border_radius=10)
            pygame.draw.rect(screen, ring, box, width=4 if ring != LINE else 2, border_radius=10)
            rows = _lines(item)
            for j, text in enumerate(rows):
                t = _shrink((mid if j == 0 else small).render(text, True, TEXT), w - 10)
                ty = y - len(rows) * 11 + j * 22
                screen.blit(t, (x - t.get_width() / 2, ty))
            n = small.render(f"[{i}]", True, SUB)
            screen.blit(n, (box.right - n.get_width() + 2, box.top - 18))

    def listing(heap, hot, taken):
        """右側: リストとしての中身と、取り出したものの一覧。"""
        screen.blit(big.render("リストとしての中身", True, GREEN), (x1, 20))
        screen.blit(small.render("[0] が先頭（いちばん小さいもの）", True, SUB), (x1, 52))
        row_h = max(20, min(30, 250 // max(len(heap), 1)))
        for i, item in enumerate(heap):
            y = 80 + i * row_h
            color = GREEN if i == 0 else (AMBER if i == hot else TEXT)
            screen.blit(small.render(f"[{i}]", True, SUB), (x1, y))
            screen.blit(small.render(_fit(small, _short(item), 300), True, color), (x1 + 40, y))
        y = 350
        screen.blit(big.render(done_label, True, GREEN), (x1, y))
        for i, item in enumerate(taken[-9:]):
            n = len(taken) - len(taken[-9:]) + i + 1
            screen.blit(small.render(_fit(small, f"{n}. {_short(item)}", 340), True, TEXT), (x1, y + 34 + i * 22))

    def draw(k):
        text, kind, heap, hot, taken = log[k]
        screen.blit(big.render(_fit(big, title, 600), True, GREEN), (30, 20))
        screen.blit(small.render("木の形: 親（上）は必ず子（下）より小さいか同じ。緑 = 先頭、橙 = いま入れたもの", True, SUB), (30, 52))
        screen.blit(mid.render(_fit(mid, text, 620), True, colors[kind]), (30, 76))
        tree(heap, hot)
        listing(heap, hot, taken)

    _loop(screen, fonts, last_step, draw)


# --- 窓を開いて、箱の中身が木の形でどう変わるかをアニメーション表示する ---
# 緑 = 先頭（次に取り出されるもの）、橙 = いま入れたもの。窓を閉じるとプログラムが終わる
show_window(log, "heapq の箱の中身")
