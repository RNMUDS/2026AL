# 前期の復習: 幅優先探索（はばゆうせんたんさく）で迷路の最短経路を求める
from collections import deque

# S = スタート、G = ゴール、# = 壁、. = 通路
maze = [
    "S.....#",
    ".####.#",
    ".#....#",
    ".#.##..",
    ".#..#.#",
    ".##.#.#",
    "......G",
]

rows = len(maze)
cols = len(maze[0])

# スタートとゴールの位置（行, 列）を探す
for r in range(rows):
    for c in range(cols):
        if maze[r][c] == "S":
            start = (r, c)
        if maze[r][c] == "G":
            goal = (r, c)

print("迷路（S=スタート  G=ゴール  #=壁  .=通路）")
for line in maze:
    print("  " + line)
print()

# --- 幅優先探索 ---
# queue = これから調べる場所を書いたメモ。先に書いたものから先に読む。
queue = deque()
queue.append(start)

# came_from = 「その場所へ、どこから来たか」を記録する辞書
came_from = {start: None}

while len(queue) > 0:
    current = queue.popleft()          # メモのいちばん古い行を読んで消す
    if current == goal:
        break

    r, c = current
    # 上・下・左・右の4方向を順に調べる
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue                   # 迷路の外なので調べない
        if maze[nr][nc] == "#":
            continue                   # 壁なので通れない
        if (nr, nc) in came_from:
            continue                   # すでに来たことがある場所
        came_from[(nr, nc)] = current
        queue.append((nr, nc))

# --- ゴールからスタートへ逆にたどって経路を復元する ---
path = []
node = goal
while node is not None:
    path.append(node)
    node = came_from[node]
path.reverse()

print("最短経路の歩数:", len(path) - 1, "歩")
print("通った場所の数:", len(path), "マス")
print()

# 経路を * で塗って表示する
picture = [list(line) for line in maze]
for (r, c) in path:
    if picture[r][c] == ".":
        picture[r][c] = "*"

print("最短経路（* が通り道）")
for line in picture:
    print("  " + "".join(line))
