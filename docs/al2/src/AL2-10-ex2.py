# 動的計画法（bitDP）で巡回セールスマン問題を解く
# 考え方: 「どの都市を回ったか」と「いまどこにいるか」が同じなら、
#         そこまでの最小距離だけ覚えておけばよい。
import math
from itertools import permutations

cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
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

full = (1 << n) - 1        # 全部の都市を回った状態（2進数で 11111）

# best[visited][here] = 「visited の都市を回り終えて、いま here にいる」ときの最小距離
best = []
for visited in range(1 << n):
    best.append([INF] * n)

# 最初は 0番の都市だけを回った状態で、0番にいる。距離は 0。
best[1 << 0][0] = 0.0

# 回った都市の集合を、小さい順に1つずつ調べていく
for visited in range(1 << n):
    for here in range(n):
        if best[visited][here] == INF:
            continue                       # まだたどり着けていない状態
        for next_city in range(n):
            if visited & (1 << next_city):
                continue                   # すでに回った都市には行かない
            new_visited = visited | (1 << next_city)
            new_length = best[visited][here] + distance[here][next_city]
            if new_length < best[new_visited][next_city]:
                best[new_visited][next_city] = new_length

# 全部回り終えたあと、0番へ戻る分を足していちばん短いものを選ぶ
answer = INF
last_city = None
for here in range(n):
    if best[full][here] == INF:
        continue
    total = best[full][here] + distance[here][0]
    if total < answer:
        answer = total
        last_city = here

print("動的計画法（bitDP）の表の一部")
print("（visited = 回った都市の集合を2進数で表したもの、here = いまいる都市）")
print("-" * 62)
print("visited           here=0 here=1   here=2   here=3   here=4")
for visited in [1, 3, 7, 15, 31]:
    line = f"   {format(visited, '05b')}        "
    for here in range(n):
        value = best[visited][here]
        if value == INF:
            line = line + "     -   "
        else:
            line = line + f"{round(value, 1):>8} "
    print(line)
print("-" * 62)
print("「-」は「その状態にはたどり着けない」ことを表す")
print()

print("bitDP の答え:", round(answer, 1))
print("最後に立ち寄った都市:", cities[last_city][0])
print()

# 答え合わせ: 全探索でも解いてみる
brute_best = None
for order in permutations(range(1, n)):
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    total = total + distance[here][0]
    if brute_best is None or total < brute_best:
        brute_best = total

print("全探索の答え:", round(brute_best, 1))
if abs(answer - brute_best) < 0.0001:
    print("2つの答えは一致した。bitDP は必ず最適解を出す。")

print()
print("表のマスの数:", (1 << n) * n, "個（2の5乗 × 5）")
print("全探索が試した順番の数: 24 通り")
