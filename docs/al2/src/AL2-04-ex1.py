# 重み付きグラフを隣接リストで表す
# 重み（おもみ）= 辺ごとに付いている数値。ここでは「乗車時間（分）」を重みにする。

# となりの駅を (駅名, かかる時間) の形で並べる
railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
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


# 新宿から品川まで、3通りの行き方を比べる
routes = [
    ["新宿", "品川"],
    ["新宿", "渋谷", "品川"],
    ["新宿", "池袋", "上野", "東京", "品川"],
]

print("新宿から品川までの行き方を比べる")
print("-" * 46)
for route in routes:
    minutes = route_minutes(route)
    print(f"{' → '.join(route)}")
    print(f"    乗りかえの回数: {len(route)-2}回 ／ 合計時間: {minutes}分")
print("-" * 46)
print()
print("直通（乗りかえ0回）がいちばん時間がかかっている")
