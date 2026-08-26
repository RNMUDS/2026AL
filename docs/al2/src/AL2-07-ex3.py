# 迷路を大きくしたとき、ダイクストラ法がどれくらいの時間で解けるかを測る
import heapq
import time


def make_cost_map(size):
    """size × size の床コスト付き迷路を作る。
    計算で決めるので、何度実行しても同じ迷路になる。"""
    cost_map = []
    for r in range(size):
        row = []
        for c in range(size):
            if (r * 3 + c * 7) % 11 == 0:
                row.append(9)          # ぬかるみ
            else:
                row.append(1)          # 舗装路
        cost_map.append(row)
    cost_map[0][0] = 1
    cost_map[size - 1][size - 1] = 1
    return cost_map


def dijkstra(cost_map):
    """左上から右下までの最小コストと、調べたマスの数を返す"""
    size = len(cost_map)
    start = (0, 0)
    goal = (size - 1, size - 1)
    INF = float("inf")

    distance = {}
    for r in range(size):
        for c in range(size):
            distance[(r, c)] = INF
    distance[start] = 0

    pq = [(0, start)]
    settled = set()

    while len(pq) > 0:
        total, current = heapq.heappop(pq)
        if current in settled:
            continue
        settled.add(current)
        if current == goal:
            break
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                continue
            new_total = total + cost_map[nr][nc]
            if new_total < distance[(nr, nc)]:
                distance[(nr, nc)] = new_total
                heapq.heappush(pq, (new_total, (nr, nc)))

    return distance[goal], len(settled)


print("迷路の大きさを変えて、ダイクストラ法の実行時間を測る")
print("-" * 62)
print("迷路の大きさ      マスの数      最小コスト   調べたマス   かかった時間")

for size in [50, 100, 200, 400]:
    cost_map = make_cost_map(size)
    began = time.time()
    best, checked = dijkstra(cost_map)
    elapsed = time.time() - began
    print(f"{size:>4}×{size:<4}   {size*size:>10,}   {best:>10}   {checked:>9,}   {elapsed:>9.3f}秒")

print("-" * 62)
print()
print("マスの数が4倍になっても、時間は4倍すこしにしかならない。")
print("第4回の全探索が6マス四方で約7秒かかったことと比べてみよう。")
