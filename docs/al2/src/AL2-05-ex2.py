# ダイクストラ法（2）: 最短時間だけでなく「どの道を通ったか」も記録する
# 距離を書き直したときに「どこから来たか」も一緒に記録しておけば、あとで道順を復元できる。

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

settled = set()

while len(settled) < len(railway):
    current = None
    for station in railway:
        if station in settled:
            continue
        if distance[station] == INF:
            continue
        if current is None or distance[station] < distance[current]:
            current = station
    if current is None:
        break

    settled.add(current)

    for name, minutes in railway[current]:
        if name in settled:
            continue
        new_distance = distance[current] + minutes
        if new_distance < distance[name]:
            distance[name] = new_distance
            came_from[name] = current      # 「どこから来たか」を記録する


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
print("-" * 60)
for station in railway:
    if station == start:
        continue
    route = build_route(station)
    print(f"{station:<4} {distance[station]:>3}分   " + " → ".join(route))
print("-" * 60)
print()

# 「どこから来たか」の記録そのものを表示する
print("came_from の中身（どの駅へは、どこから来るのがいちばん早いか）")
for station in railway:
    print(f"  {station}: {came_from[station]}")
print()
print("came_from をゴールから逆にたどると、道順ができあがる")
