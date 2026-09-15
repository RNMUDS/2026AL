# 優先度付きキュー（heapq）の使い方を確かめる
# heapq を使うと、「入れた中でいちばん小さいもの」をいつでも速く取り出せる。
import heapq

# --- その1: 数を入れて取り出す ---
numbers = []                    # ふつうのリストを用意する

for value in [6, 4, 7, 2, 8, 1]:
    heapq.heappush(numbers, value)      # heappush で1つずつ入れる
    print(f"{value} を入れた → 中身: {numbers}")

print()
print("中身の並びはバラバラに見えるが、先頭は必ずいちばん小さい数になっている")
print("いまの先頭:", numbers[0])
print()

print("取り出す順番")
while len(numbers) > 0:
    smallest = heapq.heappop(numbers)   # heappop でいちばん小さいものを取り出す
    print(f"  取り出した: {smallest}   残り: {numbers}")

print()
print("入れた順番は 8, 3, 5, 1, 9, 2 だが、取り出す順番は小さい順になる")
print("-" * 52)
print()

# --- その2: (数, 名前) の組を入れる ---
# タプルを入れると、1番目の要素で比べてくれる。
# ダイクストラ法では (今わかっている時間, 駅の名前) の組を入れる。
tasks = []
heapq.heappush(tasks, (13, "蒲田"))
heapq.heappush(tasks, (9, "川崎"))
heapq.heappush(tasks, (25, "目黒"))
heapq.heappush(tasks, (6, "鶴見"))

print("(時間, 駅名) の組を入れて取り出す")
while len(tasks) > 0:
    minutes, station = heapq.heappop(tasks)
    print(f"  {minutes}分の {station} を取り出した")

print()
print("1番目の要素（時間）が小さい順に出てくる")
