# 貪欲法が大きく損をする配達先の配置
# 遠くにぽつんと1軒だけ離れた家があると、貪欲法はその家を最後まで残してしまう。
import math
from itertools import permutations

houses = [
    ("営業所", 0, 8),
    ("A宅", 1, 5),
    ("遠方のD宅", 11, 2),
    ("B宅", 6, 4),
    ("E宅", 0, 12),
    ("C宅", 5, 9),
]

n = len(houses)

distance = []
for i in range(n):
    row = []
    for j in range(n):
        d = math.sqrt((houses[i][1] - houses[j][1]) ** 2 + (houses[i][2] - houses[j][2]) ** 2)
        row.append(d)
    distance.append(row)


def greedy(start):
    visited = [start]
    total = 0.0
    here = start
    steps = []
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        steps.append((houses[here][0], houses[nearest][0], round(distance[here][nearest], 1)))
        total = total + distance[here][nearest]
        visited.append(nearest)
        here = nearest
    steps.append((houses[here][0], houses[start][0], round(distance[here][start], 1)))
    total = total + distance[here][start]
    return visited, total, steps


def brute_force():
    best_length = None
    best_order = None
    for order in permutations(range(1, n)):
        total = 0.0
        here = 0
        for city in order:
            total = total + distance[here][city]
            here = city
        total = total + distance[here][0]
        if best_length is None or total < best_length:
            best_length = total
            best_order = order
    return [0] + list(best_order), best_length


def show(route):
    names = [houses[i][0] for i in route]
    names.append(houses[route[0]][0])
    return " → ".join(names)


print("配達先の位置")
print("-" * 40)
for name, x, y in houses:
    print(f"  {name}: (x={x}, y={y})")
print("-" * 40)
print()

print("地図（左上が (0,0)。E = 営業所）")
print("-" * 30)
for y in range(14):
    line = ""
    for x in range(13):
        mark = " ."
        for i in range(n):
            if houses[i][1] == x and houses[i][2] == y:
                mark = " E" if i == 0 else f" {i}"
        line = line + mark
    print("  " + line)
print("-" * 30)
print()

greedy_route, greedy_length, steps = greedy(0)
print("貪欲法の進み方")
for a, b, d in steps:
    print(f"  {a} → {b}  {d}")
print()
print("貪欲法の答え")
print(" ", show(greedy_route))
print("  合計距離:", round(greedy_length, 1))
print()

best_route, best_length = brute_force()
print("全探索の答え（本当の最短）")
print(" ", show(best_route))
print("  合計距離:", round(best_length, 1))
print()

print("距離の差:", round(greedy_length - best_length, 1))
print(f"貪欲法は最短ルートより {round((greedy_length / best_length - 1) * 100, 1)}% 長い")
print()
print("貪欲法は近い家から順に回るため、遠方のD宅を最後まで残してしまう。")
print("最後にD宅へ行って営業所へ戻る2回の移動だけで、27以上かかっている。")
