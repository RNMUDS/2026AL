# 同じアイテム集めパズルを全探索で解いて、貪欲法と比べる
from collections import deque
from itertools import permutations

maze = [
    "S..#....",
    ".#.#.##.",
    ".#...#..",
    ".###.#..",
    ".....#..",
    "#.##....",
    "...#.##.",
    ".#......",
]

items = {
    "A": (0, 2),
    "B": (1, 7),
    "C": (2, 0),
    "D": (2, 3),
}

rows = len(maze)
cols = len(maze[0])
start = (0, 0)
goal = (rows - 1, cols - 1)


def steps_from(origin):
    """origin から、通れるすべてのマスまでの歩数を求める（幅優先探索）"""
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
    table[name] = {}
    for other, other_position in places.items():
        table[name][other] = dist[other_position]


def route_steps(order):
    """S から order の順にアイテムを拾い、G へ行くまでの合計歩数"""
    total = table["S"][order[0]]
    for i in range(len(order) - 1):
        total = total + table[order[i]][order[i + 1]]
    total = total + table[order[-1]]["G"]
    return total


print("4つのアイテムを拾う順番は 4×3×2×1 = 24通り")
print("すべて試して合計歩数を求める")
print("-" * 44)

best_order = None
best_steps = None
for order in permutations("ABCD"):
    steps = route_steps(order)
    mark = ""
    if best_steps is None or steps < best_steps:
        best_steps = steps
        best_order = order
        mark = "  ← いまのところ最短"
    print(f"  S → {' → '.join(order)} → G   {steps:>3}歩" + mark)

print("-" * 44)
print()

greedy_order = ("A", "D", "B", "C")
print("貪欲法の答え（例題2）")
print(f"  S → {' → '.join(greedy_order)} → G   {route_steps(greedy_order)}歩")
print()
print("全探索の答え（本当の最短）")
print(f"  S → {' → '.join(best_order)} → G   {best_steps}歩")
print()
print("差:", route_steps(greedy_order) - best_steps, "歩")
print(f"貪欲法は最短より {round((route_steps(greedy_order) / best_steps - 1) * 100)}% 長い")
print()
print("貪欲法は最初にAへ向かったが、最短ルートは先にCを拾っている。")
print("Cはスタートのすぐ近くにあるのに、貪欲法は後回しにして遠回りしてしまった。")
