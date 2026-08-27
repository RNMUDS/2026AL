# 巡回セールスマン問題を全探索で解く
# 学校（0番）を出発し、ほかの4つの都市をすべて1回ずつ回って、学校へ戻る。
# 回る順番をすべて書き出し、いちばん短いものをさがす。
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


def tour_length(order):
    """0番を出発し、order の順に回って0番へ戻るまでの合計距離"""
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    total = total + distance[here][0]
    return round(total, 1)


def tour_name(order):
    """ルートを「学校 → 郵便局 → …」という文字列にして返す"""
    names = [cities[0][0]]
    for city in order:
        names.append(cities[city][0])
    names.append(cities[0][0])
    return " → ".join(names)


# permutations は「並べ方をすべて作る」道具
# 1, 2, 3, 4 の並べ方は 4×3×2×1 = 24通り
all_orders = list(permutations([1, 2, 3, 4]))

print("学校を出発して4つの都市を回り、学校へ戻る順番をすべて試す")
print("-" * 62)

best_order = None
best_length = None

for order in all_orders:
    length = tour_length(order)
    mark = ""
    if best_length is None or length < best_length:
        best_length = length
        best_order = order
        mark = "  ← いまのところ最短"
    print(f"  {order}  {length:>6}" + mark)

print("-" * 62)
print("試した順番の数:", len(all_orders), "通り")
print()
print("いちばん短いルート")
print(" ", tour_name(best_order))
print("  合計距離:", best_length)
print()

# 逆回りは同じ長さになることを確かめる
reversed_order = tuple(reversed(best_order))
print("逆回りのルート")
print(" ", tour_name(reversed_order))
print("  合計距離:", tour_length(reversed_order))
