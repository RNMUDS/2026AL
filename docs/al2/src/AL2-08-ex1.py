# 巡回セールスマン問題の準備: 都市の位置から距離の表を作る
import math

# 都市の名前と位置（x, y）
cities = [
    ("学校", 2, 2),
    ("郵便局", 10, 3),
    ("図書館", 14, 9),
    ("カフェ", 6, 12),
    ("公園", 3, 8),
]

n = len(cities)

print("都市の位置")
print("-" * 34)
for name, x, y in cities:
    print(f"  {name}: (x={x}, y={y})")
print("-" * 34)
print()

# 2つの都市のあいだの直線距離を計算して表にする
distance = []
for i in range(n):
    row = []
    for j in range(n):
        x1 = cities[i][1]
        y1 = cities[i][2]
        x2 = cities[j][1]
        y2 = cities[j][2]
        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        row.append(round(d, 1))
    distance.append(row)

print("都市の番号")
for i in range(n):
    print(f"  {i} = {cities[i][0]}")
print()

print("距離の表（きょり行列）")
print("-" * 40)
print("      " + "".join(f"{j:>7}" for j in range(n)))
for i in range(n):
    print(f"  {i}   " + "".join(f"{distance[i][j]:>7}" for j in range(n)))
print("-" * 40)
print()

print("読み方: 0行1列 =", distance[0][1], "→ 学校から郵便局までの距離")
print("ななめの線（自分自身との距離）はすべて 0.0")
print("表は左上から右下の線を軸にして対称になっている")
print()

# 地図として絵にしてみる
width = 20
height = 15
print("都市の位置を絵にしたもの（左上が (0,0)、右へ x、下へ y）")
print("-" * (width * 2 + 4))
for y in range(height):
    line = ""
    for x in range(width):
        mark = " ."
        for i in range(n):
            if cities[i][1] == x and cities[i][2] == y:
                mark = f" {i}"
        line = line + mark
    print("  " + line)
print("-" * (width * 2 + 4))
