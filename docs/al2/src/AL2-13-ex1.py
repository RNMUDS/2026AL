# 作品テンプレートA: コスト付き迷路ゲーム
# プレイヤーが選んだ道と、ダイクストラ法が見つけた最短の道を比べて点数を付ける。
import heapq

# ここを書き換えれば、自分のステージが作れる
cost_map = [
    [1, 1, 5, 9, 9, 1, 1, 1],
    [9, 1, 5, 1, 1, 1, 9, 1],
    [1, 1, 1, 1, 9, 1, 9, 1],
    [1, 9, 9, 5, 9, 1, 1, 1],
    [1, 1, 5, 5, 1, 1, 9, 5],
    [9, 1, 1, 9, 1, 9, 9, 1],
    [1, 1, 9, 9, 1, 1, 1, 1],
    [5, 1, 1, 1, 1, 9, 5, 1],
]

# プレイヤーが選んだ道（"D" = 下へ、"R" = 右へ、"U" = 上へ、"L" = 左へ）
player_moves = "DDRRDDRRDDRRDR"

rows = len(cost_map)
cols = len(cost_map[0])
start = (0, 0)
goal = (rows - 1, cols - 1)
INF = float("inf")


def move_to_route(moves):
    """"DDRR..." のような文字列を、通るマスの並びに変える"""
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
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return None                    # 迷路の外に出た
        route.append((r, c))
    return route


def route_cost(route):
    total = 0
    for i in range(1, len(route)):
        r, c = route[i]
        total = total + cost_map[r][c]
    return total


def solve():
    """ダイクストラ法で最小コスト経路を求める"""
    distance = {}
    came_from = {}
    for r in range(rows):
        for c in range(cols):
            distance[(r, c)] = INF
            came_from[(r, c)] = None
    distance[start] = 0
    queue = [(0, start)]
    settled = set()
    while len(queue) > 0:
        total, current = heapq.heappop(queue)
        if current in settled:
            continue
        settled.add(current)
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if total + cost_map[nr][nc] < distance[(nr, nc)]:
                distance[(nr, nc)] = total + cost_map[nr][nc]
                came_from[(nr, nc)] = current
                heapq.heappush(queue, (distance[(nr, nc)], (nr, nc)))
    route = []
    node = goal
    while node is not None:
        route.append(node)
        node = came_from[node]
    route.reverse()
    return route, distance[goal]


def draw(route, title):
    print(title)
    for r in range(rows):
        line = ""
        for c in range(cols):
            if (r, c) in route:
                line = line + f"{cost_map[r][c]:>3}*"
            else:
                line = line + f"{cost_map[r][c]:>3} "
        print("  " + line)
    print()


print("=" * 46)
print("  コスト迷路ゲーム  ステージ1")
print("=" * 46)
print("  1 = 舗装路(1秒)  5 = 砂地(5秒)  9 = 沼(9秒)")
print("  左上(S)から右下(G)まで、できるだけ短い時間で行こう")
print()

best_route, best_cost = solve()
player_route = move_to_route(player_moves)

if player_route is None:
    print("プレイヤーの道は迷路の外に出てしまった")
elif player_route[-1] != goal:
    print("プレイヤーの道はゴールに着いていない")
else:
    player_cost = route_cost(player_route)
    draw(player_route, f"プレイヤーの道: {len(player_route)-1}歩 ／ {player_cost}秒")
    draw(best_route, f"最短の道: {len(best_route)-1}歩 ／ {best_cost}秒")

    print("-" * 46)
    print(f"  プレイヤー: {player_cost}秒")
    print(f"  最短:       {best_cost}秒")
    score = int(best_cost / player_cost * 100)
    print(f"  スコア: {score}点（最短と同じなら100点）")
    if score == 100:
        print("  評価: 完璧！ 最短の道を見つけた")
    elif score >= 80:
        print("  評価: あと少し。もっと短い道がある")
    else:
        print("  評価: 沼をよけると、ぐっと短くなる")
    print("-" * 46)
