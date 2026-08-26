# 出発する都市を変えると、貪欲法の答えはどう変わるか
import math
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


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


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
    for order in permutations(range(1, n)):
        total = 0.0
        here = 0
        for city in order:
            total = total + distance[here][city]
            here = city
        total = total + distance[here][0]
        if best_length is None or total < best_length:
            best_length = total
    return best_length


best_length = brute_force()

print("出発する都市を変えて、貪欲法の答えを比べる")
print(f"（全探索で求めた本当の最短は {round(best_length, 1)}）")
print("-" * 68)
print("出発する都市        合計距離    最短との差    ルート")

results = []
for start in range(n):
    route, total = greedy(start)
    results.append((round(total, 1), start, route))
    names = " → ".join(cities[i][0] for i in route)
    print(pad(cities[start][0], 16)
          + f"{round(total, 1):>8}"
          + f"{round(total - best_length, 1):>12}    " + names)

print("-" * 68)
print()

results.sort()
print("いちばん良かった出発点:", cities[results[0][1]][0], "→", results[0][0])
print("いちばん悪かった出発点:", cities[results[-1][1]][0], "→", results[-1][0])
print()
if results[0][0] == round(best_length, 1):
    print("書店から出発したときだけ、貪欲法が本当の最短ルートを見つけている。")
    print("出発点を変えるだけで答えが14以上も変わる。貪欲法は運に左右される。")
