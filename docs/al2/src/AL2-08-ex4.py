# 最短ルートの中身を、区間ごとに分けて見る
import math
from itertools import permutations

all_cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
    ("駅", 17, 4),
    ("病院", 12, 13),
    ("書店", 8, 7),
]


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def make_distance(cities):
    """都市どうしの直線距離を表にして返す"""
    n = len(cities)
    table = []
    for i in range(n):
        row = []
        for j in range(n):
            d = math.sqrt((cities[i][1] - cities[j][1]) ** 2
                          + (cities[i][2] - cities[j][2]) ** 2)
            row.append(d)
        table.append(row)
    return table


def best_tour(cities):
    """全探索で最短ルートを求める"""
    n = len(cities)
    distance = make_distance(cities)
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
    return best_order, best_length


def draw_map(cities, order):
    """都市の位置を絵にする。数字は「何番目に訪れるか」"""
    visit = {0: 0}
    step = 1
    for city in order:
        visit[city] = step
        step = step + 1
    print("  " + "  訪れる順番を数字で表した地図（S = 出発点の学校）")
    for y in range(15):
        line = ""
        for x in range(20):
            mark = " ."
            for i in range(len(cities)):
                if cities[i][1] == x and cities[i][2] == y:
                    if i == 0:
                        mark = " S"
                    else:
                        mark = f" {visit[i]}"
            line = line + mark
        print("  " + line)


def show(count):
    """先頭から count 個の都市で最短ルートを求め、区間ごとに表示する"""
    cities = all_cities[:count]
    order, length = best_tour(cities)
    distance = make_distance(cities)

    print(f"■ {count}都市のときの最短ルート")
    print("-" * 52)
    route = [0] + list(order) + [0]
    total = 0.0
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        d = distance[a][b]
        total = total + d
        print("  " + pad(cities[a][0], 8) + "→ " + pad(cities[b][0], 8) + f"{round(d, 1):>6}")
    print("-" * 52)
    print(f"  合計距離: {round(total, 1)}")
    print()
    draw_map(cities, order)
    print()


show(5)
show(8)

print("=" * 52)
print("都市が5個から8個に増えると、ルートの形も大きく変わる。")
print("5都市のときの順番をそのまま使って都市を足すことはできない。")
