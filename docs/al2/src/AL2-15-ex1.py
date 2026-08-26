# 後期のまとめ: 学んだ6つのアルゴリズムを、一度にすべて動かす
import heapq
import math
import time
from collections import deque
from itertools import permutations

INF = float("inf")


def pad(text, width):
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


# ============================================================
# 前半: 2地点間の経路をさがす3つの方法
# ============================================================
railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}
start = "新宿"
goal = "東京"


def build(came_from, goal):
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


def route_minutes(route):
    total = 0
    for i in range(len(route) - 1):
        for name, minutes in railway[route[i]]:
            if name == route[i + 1]:
                total = total + minutes
                break
    return total


def bfs():
    came_from = {start: None}
    queue = deque([start])
    while len(queue) > 0:
        current = queue.popleft()
        if current == goal:
            break
        for name, minutes in railway[current]:
            if name in came_from:
                continue
            came_from[name] = current
            queue.append(name)
    return build(came_from, goal)


def dfs():
    came_from = {start: None}
    stack = [start]
    while len(stack) > 0:
        current = stack.pop()
        if current == goal:
            break
        for name, minutes in railway[current]:
            if name in came_from:
                continue
            came_from[name] = current
            stack.append(name)
    return build(came_from, goal)


def dijkstra():
    distance = {s: INF for s in railway}
    came_from = {s: None for s in railway}
    distance[start] = 0
    queue = [(0, start)]
    settled = set()
    while len(queue) > 0:
        minutes, current = heapq.heappop(queue)
        if current in settled:
            continue
        settled.add(current)
        for name, weight in railway[current]:
            if minutes + weight < distance[name]:
                distance[name] = minutes + weight
                came_from[name] = current
                heapq.heappush(queue, (distance[name], name))
    return build(came_from, goal)


print("=" * 68)
print("  前半: 新宿から東京までの経路をさがす")
print("=" * 68)
print(pad("方法", 20) + pad("路線の本数", 14) + pad("合計時間", 12) + "経路")
for name, function, learned in [("幅優先探索", bfs, "第1〜3回"),
                                ("深さ優先探索", dfs, "第2回"),
                                ("ダイクストラ法", dijkstra, "第5〜7回")]:
    route = function()
    print(pad(name, 20) + pad(f"{len(route)-1}本", 14)
          + pad(f"{route_minutes(route)}分", 12) + " → ".join(route))
print()


# ============================================================
# 後半: 全部回って戻る最短ルートをさがす3つの方法
# ============================================================
cities = [
    ("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9), ("カフェ", 6, 12),
    ("公園", 3, 8), ("駅", 17, 4), ("病院", 12, 13), ("書店", 8, 7),
    ("銀行", 16, 12), ("市役所", 5, 5),
]
n = len(cities)
distance = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(math.sqrt((cities[i][1] - cities[j][1]) ** 2
                             + (cities[i][2] - cities[j][2]) ** 2))
    distance.append(row)


def brute_force():
    best = None
    for order in permutations(range(1, n)):
        total = 0.0
        here = 0
        for city in order:
            total = total + distance[here][city]
            here = city
        total = total + distance[here][0]
        if best is None or total < best:
            best = total
    return best


def greedy():
    visited = [0]
    here = 0
    total = 0.0
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        total = total + distance[here][nearest]
        visited.append(nearest)
        here = nearest
    return total + distance[here][0]


def bit_dp():
    full = (1 << n) - 1
    best = [[INF] * n for _ in range(1 << n)]
    best[1][0] = 0.0
    for visited in range(1 << n):
        row = best[visited]
        for here in range(n):
            if row[here] == INF:
                continue
            for nxt in range(n):
                if visited & (1 << nxt):
                    continue
                if row[here] + distance[here][nxt] < best[visited | (1 << nxt)][nxt]:
                    best[visited | (1 << nxt)][nxt] = row[here] + distance[here][nxt]
    answer = INF
    for here in range(n):
        if best[full][here] < INF:
            answer = min(answer, best[full][here] + distance[here][0])
    return answer


print("=" * 68)
print(f"  後半: {n}都市を全部回って戻る最短ルートをさがす")
print("=" * 68)
print(pad("方法", 20) + pad("合計距離", 14) + pad("かかった時間", 16) + "性質")
for name, function, note in [("全探索", brute_force, "必ず最適（第8回）"),
                             ("貪欲法", greedy, "近似解（第9回）"),
                             ("bitDP", bit_dp, "必ず最適（第10回）")]:
    began = time.time()
    value = function()
    elapsed = time.time() - began
    print(pad(name, 20) + pad(f"{round(value, 1)}", 14)
          + pad(f"{elapsed:.4f}秒", 16) + note)
print("=" * 68)
print()
print("6つのアルゴリズムはすべて、後期の授業で1行ずつ書いてきたもの。")
