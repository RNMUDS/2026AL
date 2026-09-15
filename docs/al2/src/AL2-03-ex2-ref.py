stations = ["新宿", "渋谷", "池袋", "東京", "品川", "上野"]

lines = [
    ("新宿", "渋谷"),
    ("新宿", "池袋"),
    ("新宿", "東京"),
    ("渋谷", "品川"),
    ("東京", "品川"),
    ("東京", "上野"),
    ("池袋", "上野"),
]

n = len(stations)

matrix = [[0 for j in range(n)] for i in range(n)]

for a, b in lines:

    i = stations.index(a)
    j = stations.index(b)
    matrix[i][j] = 1
    matrix[j][i] = 1

print("駅の番号")
for i in range(n):
    print(f"  {i} = {stations[i]}")
print()

print("隣接行列（1 = つながっている、0 = つながっていない）")
print("-" * 40)
print("          " + "".join(f"{j:>4}" for j in range(n)))
for i in range(n):
    row = "".join(f"{matrix[i][j]:>4}" for j in range(n))
    print(f"  {i} {stations[i]}  " + row)
print("-" * 40)
print()

a = "新宿"
b = "品川"
i = stations.index(a)
j = stations.index(b)
print(f"{a} と {b} はつながっているか → matrix[{i}][{j}] =", matrix[i][j])

a = "新宿"
b = "東京"
i = stations.index(a)
j = stations.index(b)
print(f"{a} と {b} はつながっているか → matrix[{i}][{j}] =", matrix[i][j])
print()

matrix_cells = n * n
list_cells = len(lines) * 2
print("隣接行列が使うマスの数:", matrix_cells, "マス（駅の数の2乗）")
print("隣接リストが使うマスの数:", list_cells, "マス（路線の数の2倍）")
print()

print("駅の数を増やしたときの比較（1駅あたり3路線とした場合）")
print("-" * 48)
print("    駅の数   隣接行列のマス数   隣接リストのマス数")
for count in [6, 50, 500, 5000]:
    print(f"{count:>10}   {count*count:>16}   {count*3*2:>18}")
print("-" * 48)
