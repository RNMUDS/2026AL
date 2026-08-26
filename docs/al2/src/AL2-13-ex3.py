# 作品テンプレートC: アイテム収集パズル
# 迷路の中のアイテムを全部拾ってゴールへ向かう。貪欲法と全探索の両方で解く。
from collections import deque
from itertools import permutations

# ここを書き換えれば、自分のステージが作れる
maze = [
    "S.....#...",
    ".####.#.#.",
    ".#..#...#.",
    ".#.##.###.",
    ".....#....",
    "####.#.##.",
    "...#.#.#..",
    ".#...#.#.#",
    ".#.###...#",
    ".........G",
]

items = {
    "A": (0, 3),
    "B": (2, 7),
    "C": (3, 0),
    "D": (6, 8),
}

rows = len(maze)
cols = len(maze[0])
start = (0, 0)
goal = (rows - 1, cols - 1)


def steps_from(origin):
    dist = {origin: 0}
    queue = deque([origin])
    while len(queue) > 0:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if maze[nr][nc] == "#":
                continue
            if (nr, nc) in dist:
                continue
            dist[(nr, nc)] = dist[(r, c)] + 1
            queue.append((nr, nc))
    return dist


places = {"S": start, "G": goal}
for name, position in items.items():
    places[name] = position

table = {}
for name, position in places.items():
    dist = steps_from(position)
    for other, other_position in places.items():
        if other_position not in dist:
            print(f"エラー: {name} から {other} へ行けません。迷路を作り直してください。")
            raise SystemExit
    table[name] = {other: dist[places[other]] for other in places}


def route_steps(order):
    total = table["S"][order[0]]
    for i in range(len(order) - 1):
        total = total + table[order[i]][order[i + 1]]
    return total + table[order[-1]]["G"]


print("=" * 40)
print("  アイテム収集パズル  ステージ1")
print("=" * 40)
picture = [list(line) for line in maze]
picture[0][0] = "S"
picture[rows - 1][cols - 1] = "G"
for name, (r, c) in items.items():
    picture[r][c] = name
for line in picture:
    print("  " + "".join(line))
print("-" * 40)
print()

names = ["S", "A", "B", "C", "D", "G"]
print("地点どうしの歩数")
print("      " + "".join(f"{m:>5}" for m in names))
for name in names:
    print(f"  {name}   " + "".join(f"{table[name][m]:>5}" for m in names))
print()

# 貪欲法
here = "S"
remaining = ["A", "B", "C", "D"]
greedy_order = []
while len(remaining) > 0:
    nearest = min(remaining, key=lambda name: table[here][name])
    greedy_order.append(nearest)
    remaining.remove(nearest)
    here = nearest

# 全探索
best_order = None
best_steps = None
for order in permutations("ABCD"):
    steps = route_steps(order)
    if best_steps is None or steps < best_steps:
        best_steps = steps
        best_order = order

print("-" * 40)
print(f"  貪欲法: S → {' → '.join(greedy_order)} → G   {route_steps(greedy_order)}歩")
print(f"  最　適: S → {' → '.join(best_order)} → G   {best_steps}歩")
print(f"  差: {route_steps(greedy_order) - best_steps}歩")
print("-" * 40)
