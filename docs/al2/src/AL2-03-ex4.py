# 迷路もグラフである
# 迷路の1マスを頂点、となり合うマスどうしのつながりを辺と考えると、
# 迷路は「頂点がたくさんあるグラフ」になる。
# 迷路をグラフ（隣接リスト）に変換してから、例題3と同じ幅優先探索で解く。
from collections import deque

maze = [
    "S.#..",
    "..#..",
    "....#",
    "#.#..",
    "...#G",
]

rows = len(maze)
cols = len(maze[0])

print("迷路（S=スタート  G=ゴール  #=壁  .=通路）")
for line in maze:
    print("  " + line)
print()

# --- 手順1: 迷路を隣接リストに変換する ---
graph = {}

for r in range(rows):
    for c in range(cols):
        if maze[r][c] == "#":
            continue                      # 壁は頂点にしない
        name = f"({r},{c})"               # 頂点の名前は「(行,列)」にする
        graph[name] = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if maze[nr][nc] == "#":
                continue
            graph[name].append(f"({nr},{nc})")

print("迷路を隣接リストに変換した結果（最初の6個だけ表示）")
print("-" * 44)
count = 0
for name in graph:
    print(f"  {name}: " + "、".join(graph[name]))
    count = count + 1
    if count == 6:
        break
print("  ...")
print("-" * 44)
print("頂点（通れるマス）の数:", len(graph))
print()

# --- 手順2: 例題3とまったく同じ幅優先探索で解く ---
start = "(0,0)"
goal = f"({rows-1},{cols-1})"

steps = {start: 0}
came_from = {start: None}
queue = deque([start])

while len(queue) > 0:
    current = queue.popleft()
    if current == goal:
        break
    for next_node in graph[current]:
        if next_node in steps:
            continue
        steps[next_node] = steps[current] + 1
        came_from[next_node] = current
        queue.append(next_node)

route = []
node = goal
while node is not None:
    route.append(node)
    node = came_from[node]
route.reverse()

print("スタートからゴールまでの歩数:", steps[goal], "歩")
print("通る順番:")
print("  " + " → ".join(route))
print()

picture = [list(line) for line in maze]
for name in route:
    r, c = name.strip("()").split(",")
    r = int(r)
    c = int(c)
    if picture[r][c] == ".":
        picture[r][c] = "*"

print("最短経路（* が通り道）")
for line in picture:
    print("  " + "".join(line))
