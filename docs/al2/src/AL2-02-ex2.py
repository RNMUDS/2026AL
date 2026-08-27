# 幅優先探索と深さ優先探索を、同じ迷路で走らせて比べる
from collections import deque

maze = [
    "S.....#",
    ".####.#",
    ".#....#",
    ".#.##..",
    ".#..#.#",
    ".##.#.#",
    "......G",
]

rows = len(maze)
cols = len(maze[0])

for r in range(rows):
    for c in range(cols):
        if maze[r][c] == "S":
            start = (r, c)
        if maze[r][c] == "G":
            goal = (r, c)


def neighbors(r, c):
    """上・下・左・右のうち、迷路の中にあって壁ではない場所を返す"""
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue
        if maze[nr][nc] == "#":
            continue
        result.append((nr, nc))
    return result


def search(mode):
    """mode が "bfs" なら幅優先探索、"dfs" なら深さ優先探索で迷路を解く"""
    memo = deque([start])           # これから調べる場所のメモ
    came_from = {start: None}
    checked = 0                     # 何マス調べたか

    while len(memo) > 0:
        if mode == "bfs":
            current = memo.popleft()    # いちばん古い行を読む
        else:
            current = memo.pop()        # いちばん新しい行を読む
        checked = checked + 1
        if current == goal:
            break
        for next_cell in neighbors(current[0], current[1]):
            if next_cell in came_from:
                continue
            came_from[next_cell] = current
            memo.append(next_cell)

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path, checked


bfs_path, bfs_checked = search("bfs")
dfs_path, dfs_checked = search("dfs")

print("同じ迷路を2つの方法で解いた結果")
print("-" * 46)
print("方法               歩数   調べたマス数")
print("幅優先探索      ", f"{len(bfs_path)-1:>4}歩", f"{bfs_checked:>10}マス")
print("深さ優先探索    ", f"{len(dfs_path)-1:>4}歩", f"{dfs_checked:>10}マス")
print("-" * 46)


def draw(path, title):
    """通り道に * を付けて迷路を表示する"""
    picture = [list(line) for line in maze]
    for (r, c) in path:
        if picture[r][c] == ".":
            picture[r][c] = "*"
    print(title)
    for line in picture:
        print("  " + "".join(line))
    print()


print()
draw(bfs_path, "幅優先探索の経路（12歩・最短）")
draw(dfs_path, "深さ優先探索の経路（18歩・最短ではない）")
