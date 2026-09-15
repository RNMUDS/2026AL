# グラフを「隣接リスト」で表す
# 隣接リスト = それぞれの頂点について「となりにある頂点」を並べた表

# 6つの駅と、駅どうしをつなぐ路線をグラフにする
# 頂点 = 駅、辺 = 路線
railway = {
    "横浜": ["川崎", "鶴見", "大森"],
    "川崎": ["横浜", "蒲田", "鶴見"],
    "鶴見": ["横浜", "目黒", "川崎"],
    "大森": ["横浜", "蒲田"],
    "蒲田": ["川崎", "大森"],
    "目黒": ["鶴見"],
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
print("横浜のとなりの駅:", railway["横浜"])
print("蒲田のとなりの駅:", railway["蒲田"])
print()

# 「横浜と蒲田は直接つながっているか」を調べる
if "蒲田" in railway["横浜"]:
    print("横浜と蒲田は直接つながっている")
else:
    print("横浜と蒲田は直接つながっていない（乗りかえが必要）")
