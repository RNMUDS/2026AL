# 都市を8個に増やして、貪欲法と全探索を比べる
import math
import time
from itertools import permutations

cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
    ("駅", 17, 4),
    ("病院", 12, 13),
    ("書店", 8, 7),
]

n = len(cities)

distance = []
for i in range(n):
    row = []
    for j in range(n):
        d = math.sqrt((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2)
        row.append(d)
    distance.append(row)


def greedy(start):
    visited = [start]
    total = 0.0
    here = start
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        total = total + distance[here][nearest]
        visited.append(nearest)
        here = nearest
    total = total + distance[here][start]
    return visited, total


def brute_force():
    best_length = None
    best_order = None
    tried = 0
    for order in permutations(range(1, n)):
        total = 0.0
        here = 0
        for city in order:
            total = total + distance[here][city]
            here = city
        total = total + distance[here][0]
        tried = tried + 1
        if best_length is None or total < best_length:
            best_length = total
            best_order = order
    return [0] + list(best_order), best_length, tried


def show(route):
    names = [cities[i][0] for i in route]
    names.append(cities[route[0]][0])
    return " → ".join(names)


began = time.time()
greedy_route, greedy_length = greedy(0)
greedy_time = time.time() - began

began = time.time()
best_route, best_length, tried = brute_force()
brute_time = time.time() - began

print("8つの都市で、貪欲法と全探索を比べる")
print("-" * 62)
print("貪欲法")
print(" ", show(greedy_route))
print(f"  合計距離: {round(greedy_length, 1)}   かかった時間: {greedy_time:.6f}秒")
print()
print("全探索")
print(" ", show(best_route))
print(f"  合計距離: {round(best_length, 1)}   かかった時間: {brute_time:.6f}秒")
print(f"  試した順番の数: {tried:,}通り")
print("-" * 62)
print()

difference = greedy_length - best_length
ratio = greedy_length / best_length
print(f"距離の差: {round(difference, 1)}")
print(f"貪欲法は最短ルートより {round((ratio - 1) * 100, 1)}% 長い")
print(f"速さの差: 貪欲法は全探索の {round(brute_time / greedy_time)} 倍速い")
print()
print("貪欲法は速いが、最短ルートを見つけるとはかぎらない。")
