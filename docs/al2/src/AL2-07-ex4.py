# 地形を変えると、いちばん安い経路がどう変わるかを見る
import heapq

# 3種類の地形（1 = 平地1秒、5 = 森5秒、9 = 川や崖9秒）
flat_land = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

river = [
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 1],
]

forest = [
    [1, 1, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 5, 5, 5, 5, 1],
    [5, 1, 1, 1, 5, 5, 5, 1],
    [5, 5, 1, 1, 1, 5, 5, 1],
    [5, 5, 5, 1, 1, 1, 5, 1],
    [5, 5, 5, 5, 1, 1, 1, 1],
    [5, 5, 5, 5, 5, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def solve(cost_map):
    """左上から右下までの最小コスト経路を返す"""
    size = len(cost_map)
    start = (0, 0)
    goal = (size - 1, size - 1)
    INF = float("inf")

    distance = {}
    came_from = {}
    for r in range(size):
        for c in range(size):
            distance[(r, c)] = INF
            came_from[(r, c)] = None
    distance[start] = 0

    pq = [(0, start)]
    settled = set()
    while len(pq) > 0:
        total, current = heapq.heappop(pq)
        if current in settled:
            continue
        settled.add(current)
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                continue
            new_total = total + cost_map[nr][nc]
            if new_total < distance[(nr, nc)]:
                distance[(nr, nc)] = new_total
                came_from[(nr, nc)] = current
                heapq.heappush(pq, (new_total, (nr, nc)))

    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route, distance[goal]


def show(cost_map, name):
    """地形の名前・最短ルート・地図をまとめて表示する"""
    route, best = solve(cost_map)
    print(f"{name}: {len(route)-1}歩 ／ 合計 {best}秒")
    for r in range(len(cost_map)):
        line = ""
        for c in range(len(cost_map[0])):
            if (r, c) in route:
                line = line + f"{cost_map[r][c]:>3}*"
            else:
                line = line + f"{cost_map[r][c]:>3} "
        print("  " + line)
    print()


print("同じ大きさの地図でも、地形が変わると通る道が変わる")
print("（1 = 平地1秒、5 = 森5秒、9 = 川9秒。* が通り道）")
print("-" * 44)
print()

show(flat_land, "地形A 平地だけ")
show(river, "地形B まん中に川がある（4行目だけ橋がかかっている）")
show(forest, "地形C ななめに森が広がっている")

print("-" * 44)
print("地形Aでは道順は何通りもあるが、どれも同じ14秒になる。")
print("地形Bでは、わざわざ橋のある行まで回り道して川をわたっている。")
print("地形Cでは、森を避けてななめの細い平地をたどっている。")
