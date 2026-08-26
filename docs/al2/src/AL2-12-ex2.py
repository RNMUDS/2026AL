# アイテム集めパズルを貪欲法で解く
# 迷路の中に4つのアイテムがある。全部拾ってゴールへ行くまでの歩数を短くしたい。
from collections import deque

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


print("迷路（S=スタート  G=ゴール  #=壁）とアイテムの位置")
print("-" * 30)
picture = [list(line) for line in maze]
picture[0][0] = "S"
picture[rows - 1][cols - 1] = "G"
for name, (r, c) in items.items():
    picture[r][c] = name
for line in picture:
    print("  " + "".join(line))
print("-" * 30)
print()

# すべての地点どうしの歩数を、幅優先探索で先に求めておく
places = {"S": start, "G": goal}
for name, position in items.items():
    places[name] = position

table = {}
for name, position in places.items():
    dist = steps_from(position)
    table[name] = {}
    for other, other_position in places.items():
        table[name][other] = dist[other_position]

print("地点どうしの歩数の表")
print("-" * 44)
names = ["S", "A", "B", "C", "D", "G"]
print("      " + "".join(f"{m:>6}" for m in names))
for name in names:
    print(f"  {name}   " + "".join(f"{table[name][m]:>6}" for m in names))
print("-" * 44)
print()

# --- 貪欲法: いまいる場所からいちばん近いアイテムへ向かう ---
here = "S"
remaining = ["A", "B", "C", "D"]
total = 0
order = ["S"]

print("貪欲法の進み方")
while len(remaining) > 0:
    nearest = None
    for name in remaining:
        if nearest is None or table[here][name] < table[here][nearest]:
            nearest = name
    print(f"  {here} にいる → いちばん近いアイテムは {nearest}（{table[here][nearest]}歩）")
    total = total + table[here][nearest]
    order.append(nearest)
    remaining.remove(nearest)
    here = nearest

total = total + table[here]["G"]
order.append("G")
print(f"  {here} からゴールへ（{table[here]['G']}歩）")
print()

print("貪欲法の答え")
print("  拾う順番:", " → ".join(order))
print("  合計歩数:", total, "歩")
