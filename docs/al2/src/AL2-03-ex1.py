# グラフを「隣接リスト」で表す
# 隣接リスト = それぞれの頂点について「となりにある頂点」を並べた表

# 6つの駅と、駅どうしをつなぐ路線をグラフにする
# 頂点（ちょうてん） = 駅、辺（へん） = 路線
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

# 頂点の数と辺の数を数える
vertex_count = len(railway)

edge_count = 0
for station in railway:
    edge_count = edge_count + len(railway[station])
edge_count = edge_count // 2      # 1本の路線が両方の駅から数えられるので半分にする

print("頂点（駅）の数:", vertex_count)
print("辺（路線）の数:", edge_count)
print()

# となりの駅をすぐに取り出せることが、隣接リストの長所
print("新宿のとなりの駅:", railway["新宿"])
print("品川のとなりの駅:", railway["品川"])
print()

# 「新宿と品川は直接つながっているか」を調べる
if "品川" in railway["新宿"]:
    print("新宿と品川は直接つながっている")
else:
    print("新宿と品川は直接つながっていない（乗りかえが必要）")
