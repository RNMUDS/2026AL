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
for station in railway:
    distance[station] = INF
distance[start] = 0

settled = set()

def show_table(step, chosen):
    """今の距離表を1行で表示する"""
    parts = []
    for station in railway:
        value = distance[station]
        text = "-" if value == INF else str(value)
        if station in settled:
            text = text + "*"
        parts.append(f"{station}:{text:>3}")
    print(f"手順{step} {chosen}を選ぶ  " + " ".join(parts))

print("ダイクストラ法で、新宿から各駅までの最短時間を求める")
print("（* が付いている駅は「もう変わらないと決まった駅」）")
print("-" * 74)
show_table(0, "なし")

step = 0
while len(settled) < len(railway):
    step = step + 1

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
            old = "-" if distance[name] == INF else distance[name]
            distance[name] = new_distance
            print(f"        {name} の時間を {old} から {new_distance} に書き直した"
                  f"（{current} 経由: {distance[current]} + {minutes}）")

    show_table(step, current)

print("-" * 74)
print()
print("新宿から各駅までの最短時間")
for station in railway:
    print(f"  {station}: {distance[station]}分")
