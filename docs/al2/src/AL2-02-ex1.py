# 深さ優先探索（ふかさゆうせんたんさく）で迷路を解く
# 幅優先探索との違いは「メモのどこを読むか」だけ。
#   幅優先探索: いちばん古い行を読む → popleft()
#   深さ優先探索: いちばん新しい行を読む → pop()

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

# --- 深さ優先探索 ---
stack = [start]                 # これから調べる場所を書いたメモ
came_from = {start: None}       # 「その場所へ、どこから来たか」の記録
visited_order = []              # 調べた順番を記録する

while len(stack) > 0:
    current = stack.pop()       # メモのいちばん新しい行を読んで消す
    visited_order.append(current)
    if current == goal:
        break

    r, c = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if maze[nr][nc] == "#":
            continue
        if (nr, nc) in came_from:
            continue
        came_from[(nr, nc)] = current
        stack.append((nr, nc))

# --- ゴールからスタートへ逆にたどって経路を復元する ---
path = []
node = goal
while node is not None:
    path.append(node)
    node = came_from[node]
path.reverse()

print("深さ優先探索が見つけた経路の歩数:", len(path) - 1, "歩")
print("調べたマスの数:", len(visited_order), "マス")
print()

picture = [list(line) for line in maze]
for (r, c) in path:
    if picture[r][c] == ".":
        picture[r][c] = "*"

print("深さ優先探索が見つけた経路（* が通り道）")
for line in picture:
    print("  " + "".join(line))
