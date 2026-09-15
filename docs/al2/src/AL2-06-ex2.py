# heapq を使ったダイクストラ法
# 第5回では「まだ決まっていない駅を全部見て、いちばん小さい駅をさがす」ことをしていた。
# heapq を使うと、その「さがす」作業を任せられる。
import heapq

railway = {
    "横浜": [("川崎", 9), ("鶴見", 6), ("蒲田", 28)],
    "川崎": [("横浜", 9), ("蒲田", 11)],
    "鶴見": [("横浜", 6), ("目黒", 8)],
    "目黒": [("鶴見", 8), ("大森", 14)],
    "大森": [("目黒", 14), ("蒲田", 5)],
    "蒲田": [("横浜", 28), ("川崎", 11), ("大森", 5)],
}

start = "横浜"
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


print("横浜から各駅への最短の行き方")
print("-" * 56)
for station in railway:
    if station == start:
        continue
    print(f"{station:<4} {distance[station]:>3}分   " + " → ".join(build_route(station)))
print("-" * 56)
print()
print("第5回の例題1・例題2と、まったく同じ答えになっている")
