# 全探索・貪欲法・動的計画法（bitDP）の3つを同じ問題で比べる
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
INF = float("inf")

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


def brute_force():
    """全探索: すべての順番を試す"""
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


def greedy():
    """貪欲法: いちばん近い都市へ進むことをくり返す"""
    visited = [0]
    total = 0.0
    here = 0
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
    return total + distance[here][0]


def bit_dp():
    """動的計画法: 「回った集合」と「いまいる都市」で表を作る"""
    full = (1 << n) - 1
    best = []
    for visited in range(1 << n):
        best.append([INF] * n)
    best[1 << 0][0] = 0.0

    for visited in range(1 << n):
        for here in range(n):
            if best[visited][here] == INF:
                continue
            for next_city in range(n):
                if visited & (1 << next_city):
                    continue
                new_visited = visited | (1 << next_city)
                new_length = best[visited][here] + distance[here][next_city]
                if new_length < best[new_visited][next_city]:
                    best[new_visited][next_city] = new_length

    answer = INF
    for here in range(n):
        if best[full][here] == INF:
            continue
        total = best[full][here] + distance[here][0]
        if total < answer:
            answer = total
    return answer


results = []
for name, function in [("全探索", brute_force), ("貪欲法", greedy), ("bitDP", bit_dp)]:
    began = time.time()
    value = function()
    elapsed = time.time() - began
    results.append((name, round(value, 1), elapsed))

print(f"{n}都市の巡回セールスマン問題を3つの方法で解く")
print("-" * 60)
print("方法          答え（合計距離）      かかった時間      最適か")
best_value = min(v for _, v, _ in results)
for name, value, elapsed in results:
    judge = "最適" if value == best_value else f"最適より{round(value - best_value, 1)}長い"
    print(pad(name, 8) + f"   {value:>14}   {elapsed:>12.6f}秒   {judge}")
print("-" * 60)
print()
print("全探索と bitDP は同じ答えを出している。どちらも必ず最適解になる。")
print("貪欲法だけ答えが長い。速さと引きかえに最適解をあきらめている。")
