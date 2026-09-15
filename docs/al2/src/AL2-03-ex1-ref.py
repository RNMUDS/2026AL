railway = {
    "新宿": ["渋谷", "池袋", "東京"],
    "渋谷": ["新宿", "品川"],
    "池袋": ["新宿", "上野"],
    "東京": ["新宿", "品川", "上野"],
    "品川": ["渋谷", "東京"],
    "上野": ["池袋", "東京"],
}

print("隣接リストで表した路線図")
print("-" * 44)
for station in railway:
    neighbors = railway[station]
    print(f"{station}: " + "、".join(neighbors))
print("-" * 44)

vertex_count = len(railway)

edge_count = 0
for station in railway:
    edge_count = edge_count + len(railway[station])
edge_count = edge_count // 2

print("頂点（駅）の数:", vertex_count)
print("辺（路線）の数:", edge_count)
print()

print("新宿のとなりの駅:", railway["新宿"])
print("品川のとなりの駅:", railway["品川"])
print()

if "品川" in railway["新宿"]:
    print("新宿と品川は直接つながっている")
else:
    print("新宿と品川は直接つながっていない（乗りかえが必要）")
