# 前期の復習: 幅優先探索（はばゆうせんたんさく）で迷路の最短経路を求める
# 幅優先探索 = スタートに近いマスから順に、しらみつぶしに調べていく探索。
# 近い順に調べるので、最初にゴールに着いたときの道が最短経路になる。

# import は「他のファイル（ライブラリ）にある道具を使えるようにする」文。
# from collections import deque で、collections という道具箱の中の
# deque（デック）だけを取り出して使えるようにしている
from collections import deque

# --- 迷路のデータ ---
# S = スタート、G = ゴール、# = 壁、. = 通路
# [ ... ] はリスト。ここでは「文字列を 7 個ならべたリスト」で迷路を表す。
# maze[0] が 1 行目の文字列 "S.....#"、maze[0][0] がその 1 文字目 "S"
maze = [
    "S.....#",
    ".####.#",
    ".#....#",
    ".#.##..",
    ".#..#.#",
    ".##.#.#",
    "......G",
]

# len() はリストなら要素数、文字列なら文字数を返す
rows = len(maze)                    # 行の数（縦のマス数）= 7
cols = len(maze[0])                 # 列の数（横のマス数）= 1 行目の文字数 = 7

# --- スタートとゴールの位置（行, 列）を探す ---
# range(rows) は 0 から rows - 1 までの整数を順に作る。例 range(3) は 0, 1, 2
# for を 2 つ重ねて、すべての行 r とすべての列 c の組み合わせを調べる
for r in range(rows):
    for c in range(cols):
        # maze[r][c] は「r 行目の文字列の c 文字目」= マス (r, c) の文字
        if maze[r][c] == "S":
            # (r, c) はタプル。2 つの値をひとまとめにしたもので、
            # 「行 r・列 c の位置」を 1 つの値として扱える。例 (0, 0)
            start = (r, c)
        if maze[r][c] == "G":
            goal = (r, c)

print("迷路（S=スタート  G=ゴール  #=壁  .=通路）")
for line in maze:                   # 迷路を 1 行ずつ取り出して表示する
    print("  " + line)              # 文字列 + 文字列 は 2 つをつなげる
print()                             # print() だけだと空の行を表示する

# --- 幅優先探索 ---
# queue = これから調べる場所を書いたメモ。先に書いたものから先に読む。
queue = deque()                 # 簡単に言うと「先入れ先出し」のリスト
# deque は「double-ended queue」の略で、
# 両端から要素を追加・削除できるリストのこと
# つまり、queue.append() で末尾に追加、
# queue.popleft() で先頭から取り出すことができる
# 例 [1, 2, 3] という deque があったとき、
# queue.append(4) をすると [1, 2, 3, 4] になり、
# queue.popleft() をすると先頭の 1 が取り出されて [2, 3, 4] になる
queue.append(start)             # スタート地点を最初に調べる場所として追加する

# came_from = 「その場所へ、どこから来たか」を記録する辞書
# 辞書（dict）は {キー: 値} の形で「キーから値を引ける」データ。
# 例 {"りんご": 100} なら、辞書["りんご"] で 100 が取り出せる
# ここではキーがマスの位置（タプル）、値が「1 つ前のマスの位置」。
# スタートには前のマスがないので None（何もない、という特別な値）を入れる。
# この辞書は「もう来たことがある場所の一覧」としても使う
came_from = {start: None}

# メモ（queue）に調べる場所が残っているあいだ、くり返す
while len(queue) > 0:
    current = queue.popleft()          # メモのいちばん古い行を読んで消す
    if current == goal:                # ゴールに着いたら
        break                          # break でくり返しを終える

    # r, c = current で、タプル (行, 列) の中身を 2 つの変数に分けて取り出す
    # 例 current が (2, 5) なら r = 2, c = 5 になる
    r, c = current
    # 上・下・左・右の4方向を順に調べる
    # (dr, dc) は「行と列をどれだけ動かすか」。(-1, 0) は上へ 1、(0, 1) は右へ 1
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr                    # となりのマスの行（n は next の n）
        nc = c + dc                    # となりのマスの列
        # or は「どれか 1 つでも正しければ正しい」。行か列が範囲の外なら…
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            # continue は「この回の残りを飛ばして、for の次の回へ進む」命令
            continue                   # 迷路の外なので調べない
        if maze[nr][nc] == "#":
            continue                   # 壁なので通れない
        # 辞書の in は「そのキーが辞書にあるか」を調べる（あれば True）
        if (nr, nc) in came_from:
            continue                   # すでに来たことがある場所
        # 辞書[キー] = 値 で、新しい組を辞書に書きこむ
        # 「(nr, nc) へは current から来た」と記録する
        came_from[(nr, nc)] = current
        queue.append((nr, nc))         # あとで調べるようにメモの末尾に追加

# --- ゴールからスタートへ逆にたどって経路を復元する ---
# came_from を使うと、ゴール → その前のマス → さらに前 … とたどれる。
# スタートまでたどると None になるので、そこで止める
path = []                           # 通った場所を入れる空のリスト
node = goal                         # ゴールから始める
# is not None は「None ではない（まだスタートを通り過ぎていない）」という条件
while node is not None:
    path.append(node)               # リストの末尾に追加する
    node = came_from[node]          # 1 つ前のマスへ戻る
# ゴールから順に入っているので、reverse() でリストの並びを逆にする
# 例 [3, 2, 1] が [1, 2, 3] になる
path.reverse()

# path にはスタートも入っているので、歩数は「マスの数 - 1」
print("最短経路の歩数:", len(path) - 1, "歩")
print("通った場所の数:", len(path), "マス")
print()

# --- 経路を * で塗って表示する ---
# 文字列は 1 文字だけ書きかえることができないので、いったんリストに変える。
# list("S..") は ["S", ".", "."] のように 1 文字ずつのリストになる。
# [list(line) for line in maze] はリスト内包表記といい、
# 「maze の各行 line について list(line) を作り、それを並べたリスト」を作る。
# 結果は「リストの中にリストが入った」二次元のリストになる
picture = [list(line) for line in maze]
for (r, c) in path:                 # 経路の各マス (r, c) について
    if picture[r][c] == ".":        # 通路なら（S と G はそのまま残す）
        picture[r][c] = "*"         # * に書きかえる

print("最短経路（* が通り道）")
for line in picture:
    # "".join(リスト) は、リストの要素をつなげて 1 つの文字列にする
    # 例 "".join(["a", "b", "c"]) は "abc"
    print("  " + "".join(line))
