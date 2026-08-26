# 床にコストがある迷路
# マスごとに「通り抜けるのにかかる時間」が決まっている迷路を考える。
#   1 = 舗装された道（1秒）
#   9 = ぬかるみ（9秒）

cost_map = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

rows = len(cost_map)
cols = len(cost_map[0])

print("床コスト付き迷路（数字はそのマスを通るのにかかる秒数）")
print("  S = スタート(0,0)   G = ゴール(4,4)")
print("-" * 30)
for r in range(rows):
    line = "  "
    for c in range(cols):
        mark = " "
        if (r, c) == (0, 0):
            mark = "S"
        if (r, c) == (rows - 1, cols - 1):
            mark = "G"
        line = line + f"{cost_map[r][c]:>4}{mark}"
    print(line)
print("-" * 30)
print()


def route_cost(route):
    """通る順番が route のとき、合計で何秒かかるかを求める。
    スタートのマスは「入る」わけではないので数えない。"""
    total = 0
    for i in range(1, len(route)):
        r, c = route[i]
        total = total + cost_map[r][c]
    return total


def draw(route, title):
    """通り道のマスに * を付けて迷路を表示する"""
    picture = []
    for r in range(rows):
        line = []
        for c in range(cols):
            if (r, c) in route:
                line.append(f"{cost_map[r][c]:>4}*")
            else:
                line.append(f"{cost_map[r][c]:>4} ")
        picture.append("".join(line))
    print(title)
    for line in picture:
        print("  " + line)
    print()


# 3通りの行き方を比べる（* が通り道）
route_a = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
           (4, 1), (4, 2), (4, 3), (4, 4)]

route_b = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
           (1, 4), (2, 4), (3, 4), (4, 4)]

route_c = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2),
           (2, 1), (2, 0), (3, 0), (4, 0),
           (4, 1), (4, 2), (4, 3), (4, 4)]

print("行き方A: 左の列を下りて、下の行を右へ進む")
draw(route_a, f"  歩数 {len(route_a)-1}歩 ／ 合計 {route_cost(route_a)}秒")

print("行き方B: 上の行を右へ進んで、右の列を下りる")
draw(route_b, f"  歩数 {len(route_b)-1}歩 ／ 合計 {route_cost(route_b)}秒")

print("行き方C: いったん右へ出てから左へもどり、下の行を右へ進む")
draw(route_c, f"  歩数 {len(route_c)-1}歩 ／ 合計 {route_cost(route_c)}秒")

print("-" * 44)
print(f"行き方A: {len(route_a)-1}歩 ／ {route_cost(route_a)}秒")
print(f"行き方B: {len(route_b)-1}歩 ／ {route_cost(route_b)}秒")
print(f"行き方C: {len(route_c)-1}歩 ／ {route_cost(route_c)}秒")
print("-" * 44)
print("歩数がいちばん多い行き方Cが、合計時間ではいちばん短い")
