# 同じグラフを、3つの探索アルゴリズムで解いて比べる
import heapq
from collections import deque

# 重み付きグラフ（数字は乗車時間・分）
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
INF = float("inf")


def route_minutes(route):
    """駅を順に通ったときの合計時間"""
    total = 0
    for i in range(len(route) - 1):
        for name, minutes in railway[route[i]]:
            if name == route[i + 1]:
                total = total + minutes
                break
    return total


def build(came_from, goal):
    """ゴールからスタートへ逆にたどって道順を組み立てる"""
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


def bfs():
    """幅優先探索: 乗る路線の本数がいちばん少ない道"""
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
    """深さ優先探索: 行けるところまで進む道"""
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
    """ダイクストラ法: 合計時間がいちばん短い道"""
    distance = {}
    came_from = {}
    for station in railway:
        distance[station] = INF
        came_from[station] = None
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


def pad(text, width):
    """全角文字を2文字ぶんとして数え、表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


print(f"{start} から {goal} まで、3つの方法で経路を求める")
print("-" * 66)
print("方法            路線の本数   合計時間   経路")
for name, function in [("幅優先探索", bfs), ("深さ優先探索", dfs), ("ダイクストラ法", dijkstra)]:
    route = function()
    print(pad(name, 16)
          + f"{len(route)-1:>8}本"
          + f"{route_minutes(route):>9}分   "
          + " → ".join(route))
print("-" * 66)
print()
print("幅優先探索は「本数」を、ダイクストラ法は「時間」を最小にしている。")
print("深さ優先探索はどちらも最小にしない。ゴールへ行けることだけを確かめる方法。")
