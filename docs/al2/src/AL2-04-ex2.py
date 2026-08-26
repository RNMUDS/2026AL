# 幅優先探索は「重みの合計」を最小にできないことを確かめる
from collections import deque

railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
goal = "品川"


def route_minutes(route):
    """駅を順に通ったときの合計時間を求める"""
    total = 0
    for i in range(len(route) - 1):
        for name, minutes in railway[route[i]]:
            if name == route[i + 1]:
                total = total + minutes
                break
    return total


# --- 方法1: 幅優先探索（乗る路線の本数がいちばん少ない道をさがす） ---
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

bfs_route = []
node = goal
while node is not None:
    bfs_route.append(node)
    node = came_from[node]
bfs_route.reverse()


# --- 方法2: すべての行き方を書き出して、合計時間がいちばん短い道をさがす ---
def all_routes(here, goal, visited):
    """here から goal までの、同じ駅を2度通らない行き方をすべて返す"""
    if here == goal:
        return [[goal]]
    result = []
    for name, minutes in railway[here]:
        if name in visited:
            continue
        for rest in all_routes(name, goal, visited + [name]):
            result.append([here] + rest)
    return result


every_route = all_routes(start, goal, [start])

print("新宿から品川までの行き方をすべて書き出す")
print("-" * 52)
for route in every_route:
    print(f"  {' → '.join(route)}: 路線{len(route)-1}本 ／ {route_minutes(route)}分")
print("-" * 52)
print("行き方の数:", len(every_route), "通り")
print()

best_route = every_route[0]
for route in every_route:
    if route_minutes(route) < route_minutes(best_route):
        best_route = route

print("方法1: 幅優先探索が選んだ道")
print(f"  {' → '.join(bfs_route)}: 路線{len(bfs_route)-1}本 ／ {route_minutes(bfs_route)}分")
print()
print("方法2: 合計時間がいちばん短い道")
print(f"  {' → '.join(best_route)}: 路線{len(best_route)-1}本 ／ {route_minutes(best_route)}分")
print()
print("差:", route_minutes(bfs_route) - route_minutes(best_route), "分")
print()
print("幅優先探索は「路線の本数」を最小にする。「合計時間」は最小にならない。")
