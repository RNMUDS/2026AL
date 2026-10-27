# 第6回 クリエイティブ演習1: 待ち時間の短い順に回る「待ち時間ボード」を作る
# アトラクションを (待ち時間, 名前) の組で heapq の箱に入れると、待ち時間の短い順に取り出せる。
# とちゅうで待ち時間が短くなったお知らせが来たら、新しい組をもう1つ箱に入れる（古い組は読み飛ばす）。
# これは、例題2のダイクストラ法で「同じ駅が箱に2回入り、古い組を読み飛ばす」のと同じしくみ。
#
# ★ が付いた部分は、自由に書き換えてよい（それ以外はそのままでよい）。
#   Lv1: waits を、自分が乗りたいアトラクション6つ以上と、自分で決めた待ち時間にする（TITLE も）
#        news の名前も自分の waits の名前に直す（まだ決めないなら news = [] にして、Lv3 で足す）
#   Lv2: 待ち時間が同じアトラクションを2つ作り、どちらが先に出てくるかを予想してから確かめる
#        （待ち時間が同じ組は、2番目の名前でくらべる。本文1章の「組（タプル）を入れると…」の表を見よう）
#   Lv3: news にお知らせを足して、「読み飛ばす」を2回以上出す
#   Lv4: comment 関数で、待ち時間によって3通り以上のちがうひとことを出す（if / elif / else）

import heapq

# ★ 窓のいちばん上に出る題名
TITLE = "わたしの待ち時間ボード"

# ★ 乗りたいアトラクションと待ち時間（分）。(待ち時間, "名前") の組をカンマで区切って並べる
#   待ち時間は自分で決めてよい（公式アプリの待ち時間を見て決めてもよい）
waits = [
    (40, "ビッグサンダー・マウンテン"),
    (25, "カリブの海賊"),
    (60, "美女と野獣"),
    (15, "イッツ・ア・スモールワールド"),
    (50, "プーさんのハニーハント"),
    (20, "ホーンテッドマンション"),
]

# ★ 待ち時間のお知らせ。(乗った数, 新しい待ち時間, "名前") の組で並べる
#   例: (2, 10, "プーさんのハニーハント") = 2つ乗ったところで、プーさんのハニーハントが 10分 になった
#   待ち時間が「短くなった」お知らせだけが箱に入る（例題2で、時間が短くなったときだけ queue に入れるのと同じ）
#   waits を自分のアトラクションに替えたら、ここの名前も waits と同じ名前に直す
news = [
    (2, 10, "プーさんのハニーハント"),
]


def comment(minutes):
    """★ 待ち時間 minutes に合わせたひとことを返す"""
    if minutes <= 20:               # 20分を境にひとことを変える（数は好きに変えてよい）
        return "すぐ乗れる！"
    # elif minutes <= 45:           ← elif を足すと、3通り以上に分けられる（Lv4）
    #     return "ちょっと並ぶ"
    else:                           # 最後は必ず else で return する（return しない分岐があると None と表示される）
        return "がまんして並ぶ"


# ------------------------------------------------------------
# ここから下は、例題1（参考）と同じ heapq の使い方。読みながら、窓のアニメーションと見比べよう
# ------------------------------------------------------------

# 書きまちがいを先に見つける（見つけたら、直し方を表示して止まる）
#   raise SystemExit("…") は、「…」を表示してプログラムを終わらせる命令
if type(waits) != list or len(waits) < 2:
    raise SystemExit("waits は [ ] で囲んで、(待ち時間, \"名前\") の組を2つ以上並べよう")
names = []
for pair in waits:
    if type(pair) != tuple or len(pair) != 2:
        raise SystemExit(f"waits の {pair} がおかしい。(40, \"名前\") のように ( ) で囲んで、待ち時間を先に書こう")
    minutes, name = pair
    if type(minutes) != int or type(name) != str:
        raise SystemExit(f"waits の {pair} がおかしい。待ち時間は \" \" で囲まない整数（小数は不可）、名前は \" \" で囲んだ文字で、(40, \"名前\") の順に書こう")
    if minutes < 0:
        raise SystemExit(f"waits の {pair} の待ち時間がマイナス。0 以上の数で書こう")
    if name in names:
        raise SystemExit(f"waits に「{name}」が2回ある。同じアトラクションは1回だけ書こう")
    names.append(name)
if type(news) != list:
    raise SystemExit("news は [ ] で囲もう。お知らせがないときは news = [] にする")
for item in news:
    if type(item) != tuple or len(item) != 3 or type(item[0]) != int or type(item[1]) != int:
        raise SystemExit(f"news の {item} がおかしい。(乗った数, 新しい待ち時間, \"名前\") の順に、( ) で囲んで書こう（数は \" \" で囲まない整数）")
    if item[2] not in names:
        raise SystemExit(f"news の「{item[2]}」が waits にない。名前を waits と同じにしよう")
    if item[0] < 0 or item[0] >= len(waits) or item[1] < 0:
        raise SystemExit(f"news の {item} の数がおかしい。乗った数は 0〜{len(waits) - 1}、待ち時間は 0 以上で書こう")

log = []        # 窓の表示に使う記録
taken = []      # 箱から取り出した組を、取り出した順に並べる（窓の表示に使う）


def record(text, kind, box, item=None):
    """いまの箱の中身を、窓の表示のために写して残す（kind は "push"・"pop"・"skip"・"info" のどれか）"""
    hot = box.index(item) if item in box else None
    log.append((text, kind, list(box), hot, list(taken)))


board = []      # heapq の箱。(待ち時間, 名前) の組を入れる
latest = {}     # アトラクションごとの、いまわかっている待ち時間（例題2の距離表 distance にあたる）
done = set()    # もう乗ったアトラクション（例題2の確定済み settled にあたる）
ridden = []     # 乗った順番

print("待ち時間ボードに、アトラクションを heappush で入れる")
record("空っぽの箱に、(待ち時間, 名前) の組を heappush で入れていく", "info", board)
for minutes, name in waits:
    heapq.heappush(board, (minutes, name))
    latest[name] = minutes
    print(f"  ({minutes}, {name}) を入れた")
    record(f"heappush で ({minutes}, {name}) を入れた", "push", board, (minutes, name))
print("箱の中身（リストの並び）:")
for i in range(len(board)):
    print(f"  [{i}] {board[i]}")
print("-" * 60)


def check_news(count):
    """乗った数が count のときのお知らせを見て、待ち時間が短くなっていれば新しい組を箱に入れる"""
    for when, minutes, name in news:
        if when != count:
            continue
        if name in done:
            print(f"  お知らせ: {name} が {minutes}分 → もう乗ったので使わない")
        elif minutes < latest[name]:
            print(f"  お知らせ: {name} が {latest[name]}分 → {minutes}分 に短くなった")
            print(f"      → ({minutes}, {name}) も箱に入れる")
            latest[name] = minutes
            heapq.heappush(board, (minutes, name))
            record(f"お知らせ: {name} が {minutes}分に → ({minutes}, {name}) も入れる", "push", board, (minutes, name))
        else:
            print(f"  お知らせ: {name} が {minutes}分 → 短くなっていないので入れない")


check_news(0)
while len(board) > 0:
    minutes, name = heapq.heappop(board)            # 待ち時間がいちばん短い組を取り出す
    taken.append((minutes, name))

    # 同じアトラクションが箱に2回入っていることがある。もう乗ったものは、古い組なので読み飛ばす
    if name in done:
        print(f"  ({minutes}, {name}) → もう乗ったので読み飛ばす")
        record(f"heappop で ({minutes}, {name}) → もう乗ったので読み飛ばす", "skip", board)
        continue

    done.add(name)
    ridden.append((minutes, name))
    print(f"{len(ridden)}番目: {name}（{minutes}分待ち）{comment(minutes)}")
    record(f"heappop で ({minutes}, {name}) → {len(ridden)}番目に乗る", "pop", board)
    check_news(len(ridden))

print("-" * 60)
total = 0
for minutes, name in ridden:
    total = total + minutes
print(f"{len(ridden)}つ乗って、待ち時間は合計 {total}分")
record(f"ぜんぶ乗った。待ち時間は合計 {total}分", "info", board)


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


# --- 窓を開いて、待ち時間ボード（箱の中身）が木の形でどう変わるかをアニメーション表示する ---
# 緑 = 先頭（次に乗るもの）、橙 = いま入れたもの、赤い字 = 読み飛ばし。窓を閉じるとプログラムが終わる
show_window(log, TITLE, "箱から取り出した順")
