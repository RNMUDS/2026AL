# ダイクストラ法が「どのマスにいくらでたどり着けるか」を全部求めていることを見る
import heapq

cost_map = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

rows = len(cost_map)
cols = len(cost_map[0])
start = (0, 0)
INF = float("inf")

distance = {}
order = []                 # 確定した順番を記録する
for r in range(rows):
    for c in range(cols):
        distance[(r, c)] = INF
distance[start] = 0

pq = [(0, start)]
settled = set()

while len(pq) > 0:
    total, current = heapq.heappop(pq)
    if current in settled:
        continue
    settled.add(current)
    order.append((current, total))
    r, c = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        new_total = total + cost_map[nr][nc]
        if new_total < distance[(nr, nc)]:
            distance[(nr, nc)] = new_total
            heapq.heappush(pq, (new_total, (nr, nc)))

print("確定した順番（コストが小さいマスから順に決まっていく）")
print("-" * 60)
line = ""
for i, (cell, total) in enumerate(order):
    line = line + f"{cell}={total}秒  "
    if (i + 1) % 4 == 0:
        print("  " + line)
        line = ""
if line != "":
    print("  " + line)
print("-" * 60)
print()

print("スタート(0,0)から各マスまでの最小コスト")
print("-" * 30)
for r in range(rows):
    print("  " + "".join(f"{distance[(r, c)]:>5}" for c in range(cols)))
print("-" * 30)
print()

print("もとの迷路（そのマスを通るのにかかる秒数）")
print("-" * 30)
for r in range(rows):
    print("  " + "".join(f"{cost_map[r][c]:>5}" for c in range(cols)))
print("-" * 30)
print()
print("ダイクストラ法は、ゴールだけでなく全部のマスへの最小コストを同時に求めている")
