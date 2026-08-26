# 「どの都市を回ったか」を2進数1つで表す練習
# 都市が5個あるとき、「回った・回っていない」を5けたの0と1で表す。
#   いちばん右のけたが 0番の都市、その左が 1番の都市、…

city_names = ["学校", "郵便局", "図書館", "カフェ", "公園"]
n = len(city_names)


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def show(bits):
    """bits を2進数と、回った都市の名前で表示する"""
    binary = format(bits, "05b")          # 5けたの2進数にそろえる
    visited = []
    for i in range(n):
        if bits & (1 << i):               # i番目のけたが1かどうかを調べる
            visited.append(city_names[i])
    if len(visited) == 0:
        names = "（まだどこにも行っていない）"
    else:
        names = "、".join(visited)
    print(f"  {bits:>2} = 2進数 {binary}  →  {names}")


print("2進数1つで「回った都市の集合」を表す")
print("-" * 52)
show(0)
show(1)
show(3)
show(5)
show(31)
print("-" * 52)
print()

print("1つの都市を表す数（1 << i は「1を左へ i けたずらす」という意味）")
print("-" * 52)
for i in range(n):
    print("  " + pad(city_names[i], 8) + f"→ 1 << {i} = {1 << i:>2} = 2進数 {format(1 << i, '05b')}")
print("-" * 52)
print()

print("集合に都市を1つ足す（| は「または」。けたごとに 1 があれば 1 にする）")
print("-" * 52)
bits = 0
for i in range(n):
    before = bits
    bits = bits | (1 << i)                # i番の都市を「回った」ことにする
    print(f"  {format(before, '05b')} に {city_names[i]} を足す → {format(bits, '05b')}")
print("-" * 52)
print()

print("集合に都市が入っているか調べる（& は「かつ」。両方 1 のけただけ 1 にする）")
print("-" * 52)
bits = 5                                   # 2進数 00101 = 学校 と 図書館
print(f"  いまの集合: {format(bits, '05b')}")
for i in range(n):
    if bits & (1 << i):
        print(f"    {city_names[i]}: 入っている")
    else:
        print(f"    {city_names[i]}: 入っていない")
print("-" * 52)
print()
print("5個の都市なら、集合の種類は 2の5乗 = 32 通り（0 から 31 まで）")
