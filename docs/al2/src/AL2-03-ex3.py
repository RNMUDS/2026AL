# グラフの上を幅優先探索する
# 迷路と同じ考え方で、「新宿から各駅まで何本の路線に乗ればよいか」を求める
from collections import deque

railway = {
    "新宿": ["渋谷", "池袋", "東京"],
    "渋谷": ["新宿", "品川"],
    "池袋": ["新宿", "上野"],
    "東京": ["新宿", "品川", "上野"],
    "品川": ["渋谷", "東京"],
    "上野": ["池袋", "東京"],
}

start = "新宿"

# rides = 「その駅まで何本の路線に乗ればよいか」を記録する辞書
rides = {start: 0}
came_from = {start: None}

queue = deque([start])

print("幅優先探索の進み方")
print("-" * 44)

while len(queue) > 0:
    current = queue.popleft()
    print(f"{current} を調べる（乗る路線の数: {rides[current]}本）")
    for next_station in railway[current]:
        if next_station in rides:
            continue                     # すでに調べた駅
        rides[next_station] = rides[current] + 1
        came_from[next_station] = current
        queue.append(next_station)
        print(f"    → {next_station} は {rides[next_station]}本でたどり着ける")

print("-" * 44)
print()

print(f"{start} から各駅までに乗る路線の数")
print("-" * 44)
for station in railway:
    print(f"  {station}: {rides[station]}本")
print("-" * 44)
print()

# 経路を復元して表示する
for goal in ["品川", "上野"]:
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    print(f"{start} から {goal} への行き方:", " → ".join(route))
