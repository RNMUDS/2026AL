# 都市の数が増えると、試す順番の数がどれくらい増えるかを測る
import math
import time
from itertools import permutations

# 12個の都市（前から順に使う）
all_cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
    ("駅", 17, 4),
    ("病院", 12, 13),
    ("書店", 8, 7),
    ("銀行", 16, 12),
    ("市役所", 5, 5),
    ("体育館", 11, 10),
    ("美術館", 19, 9),
]


def solve(count):
    """先頭から count 個の都市を使って、全探索で最短ルートを求める"""
    cities = all_cities[:count]
    n = len(cities)

    distance = []
    for i in range(n):
        row = []
        for j in range(n):
            d = math.sqrt((cities[i][1] - cities[j][1]) ** 2
                          + (cities[i][2] - cities[j][2]) ** 2)
            row.append(d)
        distance.append(row)

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

    return tried, round(best_length, 1), best_order


print("都市の数を増やしたときの、試す順番の数とかかる時間")
print("-" * 60)
print("都市の数     試した順番の数        最短距離     かかった時間")

for count in [5, 8, 10, 11, 12]:
    began = time.time()
    tried, best, order = solve(count)
    elapsed = time.time() - began
    print(f"{count:>6}都市   {tried:>14,}通り   {best:>10}   {elapsed:>10.3f}秒")

print("-" * 60)
print()

# 都市が増えたときの順番の数だけを計算で出す（実際には試さない）
print("実際に試さずに、順番の数だけを計算した結果")
print("-" * 60)
print("都市の数     試す順番の数")
for city_count in range(5, 16):
    total_orders = 1
    for k in range(1, city_count):
        total_orders = total_orders * k
    print(f"{city_count:>6}都市   {total_orders:>22,}通り")
print("-" * 60)
print()
print("15都市では 87,178,291,200 通り。1秒に100万通り調べても24時間以上かかる。")
