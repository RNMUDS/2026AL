# 作品テンプレートB: 配達ルート最適化アプリ
# 配達先を並べると、貪欲法と全探索でルートを作り、比べて表示する。
import math
import time
from itertools import permutations

# ここを書き換えれば、自分の配達先が作れる（8件までなら全探索が使える）
places = [
    ("営業所", 5, 5),
    ("田中宅", 12, 3),
    ("鈴木宅", 2, 11),
    ("佐藤宅", 15, 12),
    ("高橋宅", 8, 14),
    ("伊藤宅", 19, 1),
    ("渡辺宅", 1, 2),
]

n = len(places)


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


distance = []
for i in range(n):
    row = []
    for j in range(n):
        d = math.sqrt((places[i][1] - places[j][1]) ** 2 + (places[i][2] - places[j][2]) ** 2)
        row.append(d)
    distance.append(row)


def route_length(order):
    """0番から出発し、order の順に回って0番へ戻るまでの合計距離を返す"""
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    return total + distance[here][0]


def greedy():
    """貪欲法: いまいる場所からいちばん近いところへ進むことをくり返す"""
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
    return tuple(visited[1:])


def brute_force():
    """全探索: すべての順番を試して、いちばん短いものを返す"""
    best = None
    best_order = None
    for order in permutations(range(1, n)):
        value = route_length(order)
        if best is None or value < best:
            best = value
            best_order = order
    return best_order


def show(order, title):
    """ルートと合計距離を表示する"""
    print(title)
    names = [places[0][0]]
    for city in order:
        names.append(places[city][0])
    names.append(places[0][0])
    print("  " + " → ".join(names))
    print(f"  合計距離: {round(route_length(order), 1)}")
    print()


print("=" * 54)
print("  配達ルート最適化アプリ")
print("=" * 54)
print(f"  配達先: {n - 1}件")
print()

print("配達先の位置")
print("-" * 34)
for name, x, y in places:
    print("  " + pad(name, 14) + f"(x={x:>2}, y={y:>2})")
print("-" * 34)
print()

print("地図（左上が (0,0)。E = 営業所）")
print("-" * 44)
for y in range(16):
    line = ""
    for x in range(20):
        mark = " ."
        for i in range(n):
            if places[i][1] == x and places[i][2] == y:
                mark = " E" if i == 0 else f" {i}"
        line = line + mark
    print("  " + line)
print("-" * 44)
print()

began = time.time()
greedy_order = greedy()
greedy_time = time.time() - began

began = time.time()
best_order = brute_force()
brute_time = time.time() - began

show(greedy_order, f"貪欲法のルート（{greedy_time:.6f}秒で作成）")
show(best_order, f"全探索のルート（{brute_time:.6f}秒で作成）")

greedy_value = route_length(greedy_order)
best_value = route_length(best_order)
print("-" * 54)
print(f"  貪欲法: {round(greedy_value, 1)}")
print(f"  最　適: {round(best_value, 1)}")
print(f"  むだになった距離: {round(greedy_value - best_value, 1)}"
      f"（{round((greedy_value / best_value - 1) * 100, 1)}% 長い）")
print("-" * 54)
