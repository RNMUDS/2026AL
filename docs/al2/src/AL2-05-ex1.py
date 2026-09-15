# ダイクストラ法（1）: 距離表が1ステップずつ決まっていく様子を見る
# 出発点から各駅までの「合計時間がいちばん短い行き方」を求める。

railway = {
    "横浜": [("川崎", 9), ("鶴見", 6), ("蒲田", 28)],
    "川崎": [("横浜", 9), ("蒲田", 11)],
    "鶴見": [("横浜", 6), ("目黒", 8)],
    "目黒": [("鶴見", 8), ("大森", 14)],
    "大森": [("目黒", 14), ("蒲田", 5)],
    "蒲田": [("横浜", 28), ("川崎", 11), ("大森", 5)],
}

start = "横浜"
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
        parts.append(f"{station}:{text:>3}")
    print(f"手順{step} {chosen}を選ぶ  " + " ".join(parts))


print("ダイクストラ法で、横浜から各駅までの最短時間を求める")
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
print("横浜から各駅までの最短時間")
for station in railway:
    print(f"  {station}: {distance[station]}分")
