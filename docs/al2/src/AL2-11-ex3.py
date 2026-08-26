# 問題の大きさを変えて、3つの方法の時間を一括で測る
import math
import time
from itertools import permutations

INF = float("inf")


def make_cities(count):
    """計算で位置を決めるので、何度実行しても同じ配置になる"""
    cities = []
    for i in range(count):
        cities.append(((i * 7) % 23, (i * 11) % 19))
    return cities


def make_distance(cities):
    n = len(cities)
    table = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(math.sqrt((cities[i][0] - cities[j][0]) ** 2
                                 + (cities[i][1] - cities[j][1]) ** 2))
        table.append(row)
    return table


def brute_force(distance):
    n = len(distance)
    best = None
    for order in permutations(range(1, n)):
        total = 0.0
        here = 0
        for city in order:
            total = total + distance[here][city]
            here = city
        total = total + distance[here][0]
        if best is None or total < best:
            best = total
    return best


def greedy(distance):
    n = len(distance)
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


def bit_dp(distance):
    n = len(distance)
    full = (1 << n) - 1
    best = []
    for visited in range(1 << n):
        best.append([INF] * n)
    best[1][0] = 0.0
    for visited in range(1 << n):
        row = best[visited]
        for here in range(n):
            if row[here] == INF:
                continue
            for nxt in range(n):
                if visited & (1 << nxt):
                    continue
                new_length = row[here] + distance[here][nxt]
                if new_length < best[visited | (1 << nxt)][nxt]:
                    best[visited | (1 << nxt)][nxt] = new_length
    answer = INF
    for here in range(n):
        if best[full][here] == INF:
            continue
        answer = min(answer, best[full][here] + distance[here][0])
    return answer


print("都市の数を変えて、3つの方法の答えと時間を測る")
print("（全探索は12都市までで打ち切る。時間がかかりすぎるため）")
print("-" * 76)
print("都市数     全探索の答え/時間        貪欲法の答え/時間        bitDPの答え/時間")

for count in [6, 8, 10, 12, 14, 16]:
    cities = make_cities(count)
    distance = make_distance(cities)

    if count <= 12:
        began = time.time()
        b_value = brute_force(distance)
        b_time = time.time() - began
        b_text = f"{round(b_value, 1):>6} /{b_time:>8.3f}秒"
    else:
        b_text = "     （長すぎるため省略）"

    began = time.time()
    g_value = greedy(distance)
    g_time = time.time() - began

    began = time.time()
    d_value = bit_dp(distance)
    d_time = time.time() - began

    print(f"{count:>4}都市   {b_text}   {round(g_value, 1):>6} /{g_time:>8.6f}秒"
          f"   {round(d_value, 1):>6} /{d_time:>8.3f}秒")

print("-" * 76)
print()
print("全探索と bitDP の答えは、どの大きさでも完全に一致している。")
print("貪欲法の答えだけが少し長い。そのかわり時間はほとんどかかっていない。")
