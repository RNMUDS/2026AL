# 壁のない広場で、2つの探索がどれだけ違う道を選ぶかを見る
from collections import deque


def search(size, mode):
    """size × size の壁のない広場を、左上から右下まで探索する"""
    start = (0, 0)
    goal = (size - 1, size - 1)

    memo = deque([start])
    came_from = {start: None}
    checked = 0

    while len(memo) > 0:
        if mode == "bfs":
            current = memo.popleft()
        else:
            current = memo.pop()
        checked = checked + 1
        if current == goal:
            break
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                continue
            if (nr, nc) in came_from:
                continue
            came_from[(nr, nc)] = current
            memo.append((nr, nc))

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path, checked


print("壁のない広場（左上から右下まで）")
print("-" * 62)
print("広さ        幅優先の歩数  幅優先の調査数   深さ優先の歩数  深さ優先の調査数")
for size in [10, 20, 40]:
    bfs_path, bfs_checked = search(size, "bfs")
    dfs_path, dfs_checked = search(size, "dfs")
    print(f"{size:>2}×{size:<2}     {len(bfs_path)-1:>8}歩 {bfs_checked:>12}マス"
          f" {len(dfs_path)-1:>12}歩 {dfs_checked:>12}マス")
print("-" * 62)
print()

# 10×10 の広場で、それぞれの経路を絵にして比べる
for mode, title in [("bfs", "幅優先探索の経路（最短）"), ("dfs", "深さ優先探索の経路（遠回り）")]:
    path, checked = search(10, mode)
    picture = [["." for _ in range(10)] for _ in range(10)]
    for (r, c) in path:
        picture[r][c] = "*"
    picture[0][0] = "S"
    picture[9][9] = "G"
    print(title, "／", len(path) - 1, "歩")
    for line in picture:
        print("  " + "".join(line))
    print()
