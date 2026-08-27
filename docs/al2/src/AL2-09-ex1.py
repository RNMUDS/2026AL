# 貪欲法（どんよくほう）で巡回セールスマン問題を解く
# 作戦はとても単純: 「いまいる都市から、まだ行っていない都市のうち
# いちばん近いところへ進む」をくり返すだけ。
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

distance = []
for i in range(n):
    row = []
    for j in range(n):
        d = math.sqrt((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2)
        row.append(round(d, 1))
    distance.append(row)


def greedy(start):
    """いちばん近い都市へ進むことをくり返して、ルートを作る"""
    visited = [start]
    total = 0.0
    here = start

    print("貪欲法の進み方")
    while len(visited) < n:
        # まだ行っていない都市の中で、いちばん近いものをさがす
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j

        print(f"  {cities[here][0]} にいる → まだ行っていない都市の中で"
              f"いちばん近いのは {cities[nearest][0]}（{distance[here][nearest]}）")
        total = total + distance[here][nearest]
        visited.append(nearest)
        here = nearest

    total = total + distance[here][start]
    print(f"  {cities[here][0]} から出発点の {cities[start][0]} へ戻る（{distance[here][start]}）")
    return visited, round(total, 1)


def brute_force():
    """全探索で最短ルートを求める（答え合わせ用）"""
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
    return [0] + list(best_order), round(best_length, 1)


def route_names(route):
    """ルートを都市名でつないだ文字列にして返す"""
    names = [cities[i][0] for i in route]
    names.append(cities[route[0]][0])
    return " → ".join(names)


greedy_route, greedy_length = greedy(0)
print()
print("貪欲法の答え")
print(" ", route_names(greedy_route))
print("  合計距離:", greedy_length)
print()

best_route, best_length = brute_force()
print("全探索の答え（本当の最短）")
print(" ", route_names(best_route))
print("  合計距離:", best_length)
print()

print("差:", round(greedy_length - best_length, 1))
print("貪欲法は 24通り すべてを試すことなく、たった 4回の比較でルートを作った。")
