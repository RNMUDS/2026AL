# heapq を使ったダイクストラ法で、大きめの重み付き迷路を解く
import heapq

# 10マス×10マスの床コスト付き迷路（数字はそのマスを通り抜けるのにかかる秒数）
cost_map = [
    [1, 1, 1, 9, 9, 9, 1, 1, 1, 1],
    [9, 9, 1, 9, 1, 1, 1, 9, 9, 1],
    [1, 1, 1, 9, 1, 9, 9, 9, 1, 1],
    [1, 9, 9, 9, 1, 1, 1, 9, 1, 9],
    [1, 1, 1, 1, 1, 9, 1, 9, 1, 1],
    [9, 9, 9, 9, 1, 9, 1, 1, 1, 9],
    [1, 1, 1, 9, 1, 9, 9, 9, 1, 1],
    [1, 9, 1, 9, 1, 1, 1, 9, 9, 1],
    [1, 9, 1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 9, 9, 1],
]

rows = len(cost_map)
cols = len(cost_map[0])
start = (0, 0)
goal = (rows - 1, cols - 1)
INF = float("inf")

distance = {}
came_from = {}
for r in range(rows):
    for c in range(cols):
        distance[(r, c)] = INF
        came_from[(r, c)] = None
distance[start] = 0

queue = [(0, start)]
settled = set()

while len(queue) > 0:
    total, current = heapq.heappop(queue)
    if current in settled:
        continue
    settled.add(current)
    if current == goal:
        break

    r, c = current
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        new_total = total + cost_map[nr][nc]
        if new_total < distance[(nr, nc)]:
            distance[(nr, nc)] = new_total
            came_from[(nr, nc)] = current
            heapq.heappush(queue, (new_total, (nr, nc)))

# 経路を復元する
route = []
node = goal
while node is not None:
    route.append(node)
    node = came_from[node]
route.reverse()

print("床コスト付き迷路（数字はそのマスを通るのにかかる秒数）")
print("-" * 44)
for r in range(rows):
    print("  " + "".join(f"{cost_map[r][c]:>4}" for c in range(cols)))
print("-" * 44)
print()

print("ダイクストラ法が見つけた最短コスト経路（* が通り道）")
print("-" * 44)
for r in range(rows):
    line = ""
    for c in range(cols):
        if (r, c) in route:
            line = line + f"{cost_map[r][c]:>3}*"
        else:
            line = line + f"{cost_map[r][c]:>3} "
    print("  " + line)
print("-" * 44)
print()

print("歩数:", len(route) - 1, "歩")
print("合計コスト:", distance[goal], "秒")
print("調べたマスの数:", len(settled), "マス")
print()

# 比べるために、歩数がいちばん少ない経路（右と下だけで進む）のコストも出す
simple_route = []
for c in range(cols):
    simple_route.append((0, c))
for r in range(1, rows):
    simple_route.append((r, cols - 1))
simple_cost = 0
for i in range(1, len(simple_route)):
    r, c = simple_route[i]
    simple_cost = simple_cost + cost_map[r][c]

print("参考: 上の行を右へ進んでから右の列を下りる経路")
print("  歩数:", len(simple_route) - 1, "歩 ／ 合計コスト:", simple_cost, "秒")
