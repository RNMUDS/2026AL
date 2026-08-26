# ダイクストラ法（4）: 出発点を変えて表を作り、全探索の答えと一致するか確かめる

railway = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}

INF = float("inf")


def dijkstra(start):
    """start から各駅までの最短時間を辞書で返す"""
    distance = {}
    for station in railway:
        distance[station] = INF
    distance[start] = 0
    settled = set()

    while len(settled) < len(railway):
        current = None
        for station in railway:
            if station in settled or distance[station] == INF:
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
    return distance


def brute_force(start):
    """すべての行き方を書き出して、各駅までの最短時間を求める（答え合わせ用）"""
    best = {start: 0}

    def walk(here, total, visited):
        for name, minutes in railway[here]:
            if name in visited:
                continue
            new_total = total + minutes
            if name not in best or new_total < best[name]:
                best[name] = new_total
            walk(name, new_total, visited + [name])

    walk(start, 0, [start])
    return best


stations = list(railway)

print("出発点を変えたときの最短時間の表（分）")
print("-" * 56)
# 駅名は全角なので、見出しは空白5つ＋駅名（全角2文字＝半角4文字ぶん）でそろえる
print("出発点" + "".join("     " + s for s in stations))
for start in stations:
    result = dijkstra(start)
    print(start + "  " + "".join(f"{result[s]:>9}" for s in stations))
print("-" * 56)
print()

print("ダイクストラ法と全探索の答えが一致するか確かめる")
print("-" * 56)
all_same = True
for start in stations:
    fast = dijkstra(start)
    slow = brute_force(start)
    for goal in stations:
        if fast[goal] != slow[goal]:
            print(f"  ちがう: {start} → {goal}  ダイクストラ {fast[goal]} / 全探索 {slow[goal]}")
            all_same = False
if all_same:
    print("  すべての出発点・すべての目的地で、答えは完全に一致した")
print("-" * 56)
print()
print("重みがすべて0以上なら、ダイクストラ法は全探索と同じ答えを、はるかに速く出せる。")
