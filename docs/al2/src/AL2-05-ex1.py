# ダイクストラ法（1）: 距離表が1ステップずつ決まっていく様子を見る
# 出発点から各駅までの「合計時間がいちばん短い行き方」を求める。

railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

start = "新宿"
INF = float("inf")      # inf は「まだ行き方が分かっていない」ことを表す無限大

# distance = 出発点からその駅までの、今わかっているいちばん短い時間
distance = {}
for station in railway:
    distance[station] = INF
distance[start] = 0

# settled = 「もう変わらないと決まった駅」を入れる集合
settled = set()


def show_table(step, chosen):
    """今の距離表を1行で表示する"""
    parts = []
    for station in railway:
        value = distance[station]
        text = "-" if value == INF else str(value)
        if station in settled:
            text = text + "*"
        parts.append(f"{station}:{text:>4}")
    print(f"手順{step}  選んだ駅: {chosen:<4}  " + " ".join(parts))


print("ダイクストラ法で、新宿から各駅までの最短時間を求める")
print("（* が付いている駅は「もう変わらないと決まった駅」）")
print("-" * 74)
show_table(0, "なし")

step = 0
while len(settled) < len(railway):
    step = step + 1

    # 手順1: まだ決まっていない駅のうち、距離がいちばん小さい駅を選ぶ
    current = None
    for station in railway:
        if station in settled:
            continue
        if distance[station] == INF:
            continue
        if current is None or distance[station] < distance[current]:
            current = station

    if current is None:
        break                       # どこにもたどり着けない駅が残っている場合

    # 手順2: 選んだ駅を「決まった」ことにする
    settled.add(current)

    # 手順3: 選んだ駅のとなりの駅について、より短い行き方が見つかれば書き直す
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
