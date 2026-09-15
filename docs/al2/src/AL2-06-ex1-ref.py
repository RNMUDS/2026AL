import heapq

numbers = []

for value in [8, 3, 5, 1, 9, 2]:
    heapq.heappush(numbers, value)
    print(f"{value} を入れた → 中身: {numbers}")

print()
print("中身の並びはバラバラに見えるが、先頭は必ずいちばん小さい数になっている")
print("いまの先頭:", numbers[0])
print()

print("取り出す順番")
while len(numbers) > 0:
    smallest = heapq.heappop(numbers)
    print(f"  取り出した: {smallest}   残り: {numbers}")

print()
print("入れた順番は 8, 3, 5, 1, 9, 2 だが、取り出す順番は小さい順になる")
print("-" * 52)
print()

tasks = []
heapq.heappush(tasks, (16, "品川"))
heapq.heappush(tasks, (7, "渋谷"))
heapq.heappush(tasks, (21, "上野"))
heapq.heappush(tasks, (9, "池袋"))

print("(時間, 駅名) の組を入れて取り出す")
while len(tasks) > 0:
    minutes, station = heapq.heappop(tasks)
    print(f"  {minutes}分の {station} を取り出した")

print()
print("1番目の要素（時間）が小さい順に出てくる")
