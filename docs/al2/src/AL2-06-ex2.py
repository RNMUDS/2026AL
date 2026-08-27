# heapq を使ったダイクストラ法
# 第5回では「まだ決まっていない駅を全部見て、いちばん小さい駅をさがす」ことをしていた。
# heapq を使うと、その「さがす」作業を任せられる。
import heapq

railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
INF = float("inf")

distance = {}
came_from = {}
for station in railway:
    distance[station] = INF
    came_from[station] = None
distance[start] = 0

# queue の中身は (出発点からの時間, 駅の名前) の組
queue = [(0, start)]
settled = set()

print("heapq から取り出した順番")
print("-" * 56)

while len(queue) > 0:
    minutes, current = heapq.heappop(queue)   # いちばん時間が小さい組を取り出す

    if current in settled:
        # 同じ駅の古い（時間の大きい）組が残っていることがあるので読み飛ばす
        print(f"  ({minutes}分, {current}) → すでに確定済みなので読み飛ばす")
        continue

    settled.add(current)
    print(f"  ({minutes}分, {current}) → {current} を {minutes}分で確定")

    for name, weight in railway[current]:
        new_distance = minutes + weight
        if new_distance < distance[name]:
            distance[name] = new_distance
            came_from[name] = current
            heapq.heappush(queue, (new_distance, name))
            print(f"        {name} を {new_distance}分として queue に入れた")

print("-" * 56)
print()


def build_route(goal):
    """ゴールからスタートへ逆にたどって道順を組み立てる"""
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route


print("新宿から各駅への最短の行き方")
print("-" * 56)
for station in railway:
    if station == start:
        continue
    print(f"{station:<4} {distance[station]:>3}分   " + " → ".join(build_route(station)))
print("-" * 56)
print()
print("第5回の例題1・例題2と、まったく同じ答えになっている")
