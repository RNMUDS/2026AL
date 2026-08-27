# レポートに載せる「実行時間の測り方」
# 1回だけ測ると、たまたま遅かった値をつかむことがある。何度か測って平均を取る。
import math
import time
from itertools import permutations


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def make_distance(count):
    """都市どうしの直線距離を表にして返す"""
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
    """全探索: すべての順番を試して、いちばん短いものを返す"""
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


def measure(function, argument, times):
    """function を times 回動かして、毎回の時間を返す"""
    records = []
    for i in range(times):
        began = time.time()
        function(argument)
        records.append(time.time() - began)
    return records


print("同じ処理を5回ずつ測ってみる（10都市の全探索）")
print("-" * 58)
distance = make_distance(10)
records = measure(brute_force, distance, 5)
for i, value in enumerate(records):
    print(f"  {i+1}回目: {value:.4f}秒")
print("-" * 58)
print(f"  いちばん速い: {min(records):.4f}秒")
print(f"  いちばん遅い: {max(records):.4f}秒")
print(f"  平均:         {sum(records)/len(records):.4f}秒")
print(f"  ばらつき（遅い÷速い）: {max(records)/min(records):.2f}倍")
print("-" * 58)
print()
print("同じ処理でも、測るたびに時間が違う。1回だけの結果を書くのは正しくない。")
print("レポートには「5回測った平均」のように、測り方も書く。")
print()

print("=" * 58)
print("レポート用の表（都市の数を変えて、5回ずつ測った平均）")
print("=" * 58)
print(pad("都市の数", 12) + pad("平均", 12) + pad("最速", 12) + pad("最遅", 12))
for count in [7, 8, 9, 10]:
    distance = make_distance(count)
    records = measure(brute_force, distance, 5)
    average = sum(records) / len(records)
    print(pad(f"{count}都市", 12)
          + pad(f"{average:.4f}秒", 12)
          + pad(f"{min(records):.4f}秒", 12)
          + pad(f"{max(records):.4f}秒", 12))
print("=" * 58)
print()
print("測り方の書き方の例:")
print("  「MacBook Air (M4) 上の Python 3.11 で、同じ処理を5回ずつ実行し、")
print("   その平均を記録した。時間は time.time() で計測した。」")
