# 重み付きグラフを隣接リストで表す
# 重み = 辺ごとに付いている数値。ここでは「乗車時間（分）」を重みにする。

# となりの駅を (駅名, かかる時間) の形で並べる
railway = {
    "横浜": [("川崎", 9), ("鶴見", 6), ("蒲田", 28)],
    "川崎": [("横浜", 9), ("蒲田", 11)],
    "鶴見": [("横浜", 6), ("目黒", 8)],
    "目黒": [("鶴見", 8), ("大森", 14)],
    "大森": [("目黒", 14), ("蒲田", 5)],
    "蒲田": [("横浜", 28), ("川崎", 11), ("大森", 5)],
}

print("重み付きグラフ（数字は乗車時間・分）")
print("-" * 46)
for station in railway:
    parts = []
    for name, minutes in railway[station]:
        parts.append(f"{name}({minutes}分)")
    print(f"{station}: " + "、".join(parts))
print("-" * 46)
print()


def route_minutes(route):
    """駅を順に通ったときの合計時間を求める。つながっていない駅があれば None を返す。"""
    total = 0
    for i in range(len(route) - 1):
        here = route[i]
        next_station = route[i + 1]
        found = False
        for name, minutes in railway[here]:
            if name == next_station:
                total = total + minutes
                found = True
                break
        if not found:
            return None
    return total


# 横浜から蒲田まで、3通りの行き方を比べる
routes = [
    ["横浜", "蒲田"],
    ["横浜", "川崎", "蒲田"],
    ["横浜", "鶴見", "目黒", "大森", "蒲田"],
]

print("横浜から蒲田までの行き方を比べる")
print("-" * 46)
for route in routes:
    minutes = route_minutes(route)
    print(f"{' → '.join(route)}")
    print(f"    乗りかえの回数: {len(route)-2}回 ／ 合計時間: {minutes}分")
print("-" * 46)
print()
print("直通（乗りかえ0回）がいちばん時間がかかっている")
