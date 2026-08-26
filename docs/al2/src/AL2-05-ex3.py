# ダイクストラ法（3）: マイナスの重みがあると答えを間違える
# 3つのお店をめぐる。辺の重みは「かかる金額（円）」。
# B店を通ると5円のクーポンがもらえるので、B店からA店へ行く辺の重みは -5 になる。

shops = {
    "スタート": [("A店", 1), ("B店", 2)],
    "B店": [("A店", -5)],
    "A店": [],
}

start = "スタート"
INF = float("inf")


def dijkstra():
    """ダイクストラ法で、スタートから各店までの最小金額を求める"""
    distance = {}
    for shop in shops:
        distance[shop] = INF
    distance[start] = 0
    settled = set()

    print("ダイクストラ法の進み方")
    while len(settled) < len(shops):
        current = None
        for shop in shops:
            if shop in settled or distance[shop] == INF:
                continue
            if current is None or distance[shop] < distance[current]:
                current = shop
        if current is None:
            break
        settled.add(current)
        print(f"  {current} を「{distance[current]}円で確定」とした")
        for name, price in shops[current]:
            if name in settled:
                print(f"      {name} へ {distance[current]} + ({price}) = "
                      f"{distance[current] + price} 円で行けるが、"
                      f"{name} はすでに確定しているので無視された")
                continue
            new_price = distance[current] + price
            if new_price < distance[name]:
                distance[name] = new_price
    return distance


def all_routes(here, visited):
    """同じ店を2度通らない行き方をすべて返す"""
    result = [[here]]
    for name, price in shops[here]:
        if name in visited:
            continue
        for rest in all_routes(name, visited + [name]):
            result.append([here] + rest)
    return result


def route_price(route):
    total = 0
    for i in range(len(route) - 1):
        for name, price in shops[route[i]]:
            if name == route[i + 1]:
                total = total + price
                break
    return total


print("お店のつながり（数字は金額・円。マイナスはクーポンで安くなることを表す）")
for shop in shops:
    if len(shops[shop]) == 0:
        print(f"  {shop}: つながる先なし")
    else:
        print(f"  {shop}: " + "、".join(f"{n}({p}円)" for n, p in shops[shop]))
print("-" * 60)
print()

result = dijkstra()
print()
print("ダイクストラ法が出した答え")
for shop in shops:
    print(f"  {shop}: {result[shop]}円")
print()

print("すべての行き方を書き出して確かめる")
best = {}
for route in all_routes(start, [start]):
    goal = route[-1]
    price = route_price(route)
    print(f"  {' → '.join(route)}: {price}円")
    if goal not in best or price < best[goal]:
        best[goal] = price
print()
print("本当の最小金額")
for shop in shops:
    print(f"  {shop}: {best[shop]}円")
print()
print("A店について、ダイクストラ法は", result["A店"], "円と答えたが、本当は", best["A店"], "円で行ける。")
print("マイナスの重みがあると、ダイクストラ法は正しい答えを出せない。")
