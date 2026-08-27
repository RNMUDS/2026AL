# 境界値テスト: わざと「特別な入力」を与えて、プログラムが正しく動くか確かめる
# テンプレートAの「プレイヤーの道」を受け取る部分をテストする。

cost_map = [
    [1, 1, 5],
    [9, 1, 1],
    [1, 1, 1],
]

rows = len(cost_map)
cols = len(cost_map[0])
start = (0, 0)
goal = (rows - 1, cols - 1)


def move_to_route_buggy(moves):
    """"DDRR" を通るマスの並びに変える（バグあり）"""
    route = [start]
    r, c = start
    for move in moves:
        if move == "D":
            r = r + 1
        elif move == "R":
            c = c + 1
        route.append((r, c))
    return route


def move_to_route_fixed(moves):
    """"DDRR" を通るマスの並びに変える（修正版）"""
    route = [start]
    r, c = start
    for move in moves:
        if move == "D":
            r = r + 1
        elif move == "U":
            r = r - 1
        elif move == "R":
            c = c + 1
        elif move == "L":
            c = c - 1
        else:
            return None, f"「{move}」は使えない文字です（D/U/R/L だけ使えます）"
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return None, "迷路の外に出てしまいました"
        route.append((r, c))
    if route[-1] != goal:
        return None, "ゴールに着いていません"
    return route, "OK"


tests = [
    ("ふつうの道", "DDRR"),
    ("空の道", ""),
    ("迷路の外に出る道", "DDDDDD"),
    ("ゴールに着かない道", "DR"),
    ("使えない文字が入った道", "DDXR"),
    ("行ったり戻ったりする道", "DRLDRR"),
]

print("バグのある関数に、6種類の入力を与えてみる")
print("=" * 58)
for name, moves in tests:
    print(f"入力: {name}（\"{moves}\"）")
    route = move_to_route_buggy(moves)
    last = route[-1]
    inside = 0 <= last[0] < rows and 0 <= last[1] < cols
    print(f"  最後にいるマス: {last}   迷路の中か: {inside}")
    if not inside:
        print("  → 迷路の外を指している。このあと cost_map[r][c] でエラーになる")
    print()

print("=" * 58)
print("修正版に、同じ6種類の入力を与えてみる")
print("=" * 58)
for name, moves in tests:
    route, message = move_to_route_fixed(moves)
    if route is None:
        print(f"入力: {name}（\"{moves}\"）")
        print(f"  → 受けつけない: {message}")
    else:
        total = 0
        for i in range(1, len(route)):
            r, c = route[i]
            total = total + cost_map[r][c]
        print(f"入力: {name}（\"{moves}\"）")
        print(f"  → OK: {len(route)-1}歩 ／ {total}秒")
print("=" * 58)
print()
print("修正版は、どの入力でもエラーで止まらず、理由を教えてくれる。")
print("「わざと変な入力を試す」ことをテストと呼ぶ。作品を提出する前に必ず行う。")
