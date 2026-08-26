# レポートに載せる「表」と「グラフ」を、文字だけで作る
import math
from itertools import permutations


def pad(text, width):
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def make_distance(count):
    cities = []
    for i in range(count):
        cities.append(((i * 7) % 23, (i * 11) % 19))
    table = []
    for i in range(count):
        row = []
        for j in range(count):
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
    here = 0
    total = 0.0
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


# --- データを集める ---
sizes = [5, 6, 7, 8, 9, 10]
results = []
for count in sizes:
    distance = make_distance(count)
    best = brute_force(distance)
    fast = greedy(distance)
    results.append((count, round(best, 1), round(fast, 1),
                    round((fast / best - 1) * 100, 1)))


# --- 表にする ---
print("表1: 都市の数と、2つの方法が出した答え")
print("-" * 56)
print(pad("都市の数", 12) + pad("最適解", 12) + pad("貪欲法", 12) + pad("何%長いか", 12))
for count, best, fast, gap in results:
    print(pad(f"{count}都市", 12) + pad(str(best), 12) + pad(str(fast), 12) + pad(f"{gap}%", 12))
print("-" * 56)
print()


# --- 文字だけでグラフにする ---
def bar(value, biggest, width):
    """value の大きさに合わせて # を並べる"""
    length = int(value / biggest * width)
    if length < 1:
        length = 1
    return "#" * length


print("図1: 貪欲法が最適解より何%長いか")
print("-" * 56)
biggest = max(gap for _, _, _, gap in results)
if biggest == 0:
    biggest = 1
for count, best, fast, gap in results:
    print(pad(f"{count}都市", 10) + pad(bar(gap, biggest, 30), 32) + f"{gap}%")
print("-" * 56)
print()

print("図2: 最適解と貪欲法の答えを並べて比べる")
print("-" * 56)
biggest = max(max(best, fast) for _, best, fast, _ in results)
for count, best, fast, gap in results:
    print(pad(f"{count}都市", 10) + "最適 " + pad(bar(best, biggest, 30), 32) + str(best))
    print(pad("", 10) + "貪欲 " + pad(bar(fast, biggest, 30), 32) + str(fast))
print("-" * 56)
print()
print("表と図をレポートに載せるときは、必ず「表1」「図1」のように番号と題を付ける。")
print("本文からは「表1のとおり」のように番号で指す。")
