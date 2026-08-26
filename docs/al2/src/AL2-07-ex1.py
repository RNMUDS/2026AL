# 床コスト付き迷路を、幅優先探索とダイクストラ法の両方で解いて比べる
import heapq
from collections import deque

# 第4回の例題3と同じ迷路（1 = 舗装路1秒、9 = ぬかるみ9秒）
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
goal = (rows - 1, cols - 1)
INF = float("inf")


def neighbors(r, c):
    """上・下・左・右のうち、迷路の中にあるマスを返す"""
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            result.append((nr, nc))
    return result


def route_cost(route):
    """通った順番 route の合計コストを求める（スタートのマスは数えない）"""
    total = 0
    for i in range(1, len(route)):
        r, c = route[i]
        total = total + cost_map[r][c]
    return total


def build_route(came_from, goal):
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


# --- 方法1: 幅優先探索（歩数がいちばん少ない道をさがす） ---
came_from_bfs = {start: None}
queue = deque([start])
while len(queue) > 0:
    current = queue.popleft()
    if current == goal:
        break
    for nxt in neighbors(current[0], current[1]):
        if nxt in came_from_bfs:
            continue
        came_from_bfs[nxt] = current
        queue.append(nxt)
bfs_route = build_route(came_from_bfs, goal)


# --- 方法2: ダイクストラ法（合計コストがいちばん小さい道をさがす） ---
distance = {}
came_from_dij = {}
for r in range(rows):
    for c in range(cols):
        distance[(r, c)] = INF
        came_from_dij[(r, c)] = None
distance[start] = 0

pq = [(0, start)]
settled = set()
while len(pq) > 0:
    total, current = heapq.heappop(pq)
    if current in settled:
        continue
    settled.add(current)
    for nxt in neighbors(current[0], current[1]):
        new_total = total + cost_map[nxt[0]][nxt[1]]
        if new_total < distance[nxt]:
            distance[nxt] = new_total
            came_from_dij[nxt] = current
            heapq.heappush(pq, (new_total, nxt))
dij_route = build_route(came_from_dij, goal)


def draw(route, title):
    print(title)
    for r in range(rows):
        line = ""
        for c in range(cols):
            if (r, c) in route:
                line = line + f"{cost_map[r][c]:>4}*"
            else:
                line = line + f"{cost_map[r][c]:>4} "
        print("  " + line)
    print()


print("床コスト付き迷路（数字はそのマスを通るのにかかる秒数）")
print("-" * 30)
for r in range(rows):
    print("  " + "".join(f"{cost_map[r][c]:>5}" for c in range(cols)))
print("-" * 30)
print()

draw(bfs_route, f"幅優先探索の経路: {len(bfs_route)-1}歩 ／ 合計 {route_cost(bfs_route)}秒")
draw(dij_route, f"ダイクストラ法の経路: {len(dij_route)-1}歩 ／ 合計 {route_cost(dij_route)}秒")

print("-" * 44)
print(f"幅優先探索      {len(bfs_route)-1:>3}歩  {route_cost(bfs_route):>3}秒")
print(f"ダイクストラ法  {len(dij_route)-1:>3}歩  {route_cost(dij_route):>3}秒")
print("-" * 44)
print("幅優先探索は歩数を、ダイクストラ法は合計コストを、それぞれ最小にしている")
