# 巡回セールスマン問題を4つの方法で解いて比べる
import math
import time
from itertools import permutations

cities = [
    ("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9), ("カフェ", 6, 12),
    ("公園", 3, 8), ("駅", 17, 4), ("病院", 12, 13), ("書店", 8, 7),
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
    """全探索: すべての順番を試して、いちばん短いものを返す"""
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


def greedy_from(start):
    """start を出発点にして、貪欲法でルートを作る"""
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
    return total + distance[here][start]


def greedy():
    """貪欲法（出発点は0番の都市に固定）"""
    return greedy_from(0)


def greedy_all_starts():
    """すべての都市を出発点にして貪欲法を試し、いちばん良い答えを選ぶ"""
    best = None
    for start in range(n):
        value = greedy_from(start)
        if best is None or value < best:
            best = value
    return best


def bit_dp():
    """動的計画法（bitDP）: 「回った集合」と「いまいる都市」で表を作り、最適解を求める"""
    full = (1 << n) - 1
    best = []
    for visited in range(1 << n):
        best.append([INF] * n)
    best[1][0] = 0.0
    for visited in range(1 << n):
        for here in range(n):
            if best[visited][here] == INF:
                continue
            for nxt in range(n):
                if visited & (1 << nxt):
                    continue
                new_length = best[visited][here] + distance[here][nxt]
                if new_length < best[visited | (1 << nxt)][nxt]:
                    best[visited | (1 << nxt)][nxt] = new_length
    answer = INF
    for here in range(n):
        if best[full][here] == INF:
            continue
        answer = min(answer, best[full][here] + distance[here][0])
    return answer


methods = [
    ("全探索", brute_force, "必ず最適"),
    ("貪欲法", greedy, "最適とはかぎらない"),
    ("貪欲法(全出発点)", greedy_all_starts, "最適とはかぎらない"),
    ("bitDP", bit_dp, "必ず最適"),
]

results = []
for name, function, note in methods:
    began = time.time()
    value = function()
    elapsed = time.time() - began
    results.append((name, value, elapsed, note))

best_value = None
for name, value, elapsed, note in results:
    if best_value is None or value < best_value:
        best_value = value

print(f"{n}都市の巡回セールスマン問題を4つの方法で解く")
print("-" * 72)
print("方法                    答え  最適との差          時間   性質")
for name, value, elapsed, note in results:
    print(pad(name, 20)
          + f"{round(value, 1):>8}"
          + f"{round(value - best_value, 1):>12}"
          + f"{elapsed:>12.6f}秒   " + note)
print("-" * 72)
print()
print("貪欲法は出発点を全部試すだけで、答えが最適に近づく。")
print("それでも全探索や bitDP より圧倒的に速い。")
