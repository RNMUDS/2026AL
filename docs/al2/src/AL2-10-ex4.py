# 動的計画法（bitDP）で、都市をどこまで増やせるかを確かめる
import math
import time

# 都市の位置は計算で決めるので、何度実行しても同じ配置になる
def make_cities(count):
    cities = []
    for i in range(count):
        x = (i * 7) % 23
        y = (i * 11) % 19
        cities.append((f"都市{i}", x, y))
    return cities


def bit_dp(cities):
    """動的計画法で最短ルートの長さを求める"""
    n = len(cities)
    INF = float("inf")

    distance = []
    for i in range(n):
        row = []
        for j in range(n):
            d = math.sqrt((cities[i][1] - cities[j][1]) ** 2
                          + (cities[i][2] - cities[j][2]) ** 2)
            row.append(d)
        distance.append(row)

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
            for next_city in range(n):
                if visited & (1 << next_city):
                    continue
                new_visited = visited | (1 << next_city)
                new_length = row[here] + distance[here][next_city]
                if new_length < best[new_visited][next_city]:
                    best[new_visited][next_city] = new_length

    answer = INF
    for here in range(n):
        if best[full][here] == INF:
            continue
        total = best[full][here] + distance[here][0]
        if total < answer:
            answer = total
    return answer, (1 << n) * n


print("動的計画法（bitDP）で都市を増やしたときの表の大きさと時間")
print("-" * 66)
print("都市の数     表のマスの数       最短距離     かかった時間     全探索なら")

for count in [10, 12, 14, 16, 18, 20]:
    cities = make_cities(count)
    began = time.time()
    answer, cells = bit_dp(cities)
    elapsed = time.time() - began

    brute_orders = 1
    for k in range(1, count):
        brute_orders = brute_orders * k

    print(f"{count:>6}都市   {cells:>12,}   {round(answer, 1):>10}   {elapsed:>10.3f}秒"
          f"   {brute_orders:>16,}通り")

print("-" * 66)
print()
print("表のマスの数は 2の(都市の数)乗 × 都市の数。都市が1つ増えると約2倍になる。")
print("全探索の順番の数は、都市が1つ増えると (都市の数-1) 倍になる。")
print("増え方が「2倍ずつ」と「11倍・12倍…」では、大きな違いがある。")
print()
print("bitDP でも 25都市を超えると表が大きすぎて解けなくなる。")
print("それでも全探索の限界（12都市くらい）よりはずっと先まで解ける。")
