# 同じ「探す」でも、やり方によって手数がどれだけ違うかを数える


def linear_search_count(data, target):
    """先頭から1つずつ調べる（逐次探索）。調べた回数を返す"""
    count = 0
    for value in data:
        count = count + 1
        if value == target:
            return count
    return count


def binary_search_count(data, target):
    """まん中と比べて半分ずつ捨てる（二分探索）。調べた回数を返す"""
    low = 0
    high = len(data) - 1
    count = 0
    while low <= high:
        count = count + 1
        middle = (low + high) // 2
        if data[middle] == target:
            return count
        elif data[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return count


print("データの個数     逐次探索の回数     二分探索の回数")
print("-" * 50)

for size in [10, 100, 1000, 10000, 100000]:
    data = list(range(1, size + 1))   # 1, 2, 3, ... という並んだデータを作る
    target = size                     # いちばん最後の数をさがす
    times_linear = linear_search_count(data, target)
    times_binary = binary_search_count(data, target)
    print(f"{size:>10}   {times_linear:>14}   {times_binary:>14}")

print("-" * 50)
print("データが10倍になっても、二分探索の回数はほとんど増えない")
