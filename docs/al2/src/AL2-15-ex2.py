# 発展手法その1: 焼きなまし法（やきなましほう / Simulated Annealing）
# 考え方: 「いまより悪くなる変更も、たまには受け入れる」
#         最初は悪い変更もよく受け入れ、だんだん受け入れなくなっていく。
#         鉄を熱してゆっくり冷ますと、内部のひずみが取れることに由来する名前。
import math
import random

# 乱数の種を決めておくと、何度実行しても同じ結果になる
random.seed(2026)

# 20都市。全探索では 19! ＝ 約12京通りになり、まったく終わらない
cities = []
for i in range(20):
    cities.append(((i * 7) % 23, (i * 11) % 19))

n = len(cities)
distance = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(math.sqrt((cities[i][0] - cities[j][0]) ** 2
                             + (cities[i][1] - cities[j][1]) ** 2))
    distance.append(row)


def tour_length(order):
    """0番から出発し、order の順に回って0番へ戻るまでの合計距離"""
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    return total + distance[here][0]


def greedy_order():
    """出発点にする最初のルートを、貪欲法で作る"""
    visited = [0]
    here = 0
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        visited.append(nearest)
        here = nearest
    return visited[1:]


order = greedy_order()
current = tour_length(order)
best_order = list(order)
best_length = current

temperature = 10.0          # 最初の「熱さ」。大きいほど悪い変更も受け入れる
cooling = 0.9995            # 1回ごとに温度をかける数（1より少し小さい）
steps = 20000

accepted_worse = 0
print("焼きなまし法で20都市のルートを短くしていく")
print("-" * 62)
print(f"  はじめのルート（貪欲法）: {round(current, 1)}")
print()
print("  途中経過")
print("  " + "-" * 58)
print("  ステップ      温度     いまのルート   いちばん良いルート")

for step in range(steps):
    # 2つの都市を選んで、順番を入れかえてみる
    i = random.randrange(n - 1)
    j = random.randrange(n - 1)
    if i == j:
        continue
    candidate = list(order)
    candidate[i], candidate[j] = candidate[j], candidate[i]
    new_length = tour_length(candidate)

    difference = new_length - current
    if difference < 0:
        accept = True                       # 短くなったので必ず受け入れる
    else:
        # 悪くなる場合でも、温度が高いうちは受け入れることがある
        chance = math.exp(-difference / temperature)
        accept = random.random() < chance
        if accept:
            accepted_worse = accepted_worse + 1

    if accept:
        order = candidate
        current = new_length
        if current < best_length:
            best_length = current
            best_order = list(order)

    temperature = temperature * cooling

    if step % 4000 == 0:
        print(f"  {step:>8}   {temperature:>7.3f}   {round(current, 1):>14}"
              f"   {round(best_length, 1):>18}")

print("  " + "-" * 58)
print()
print(f"  最後のルート: {round(best_length, 1)}")
print(f"  はじめから何%短くなったか: "
      f"{round((1 - best_length / tour_length(greedy_order())) * 100, 1)}%")
print(f"  「悪くなる変更」を受け入れた回数: {accepted_worse:,}回")
print("-" * 62)
print()
print("わざと悪くなる変更を受け入れることで、")
print("貪欲法がはまりこむ「局所最適」から抜け出せる。")
print("温度が下がるにつれて悪い変更を受け入れなくなり、答えが落ち着いていく。")
