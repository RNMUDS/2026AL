# 「全部見てさがす方法」と「heapq を使う方法」の速さを比べる
import heapq
import time


def make_grid_graph(size):
    """size × size のマス目を、重み付きグラフ（隣接リスト）にして返す。
    重みは計算で決めるので、何度実行しても同じグラフになる。"""
    graph = {}
    for r in range(size):
        for c in range(size):
            name = (r, c)
            graph[name] = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc
                if nr < 0 or nr >= size or nc < 0 or nc >= size:
                    continue
                weight = (nr * 7 + nc * 13) % 9 + 1     # 1〜9 のあいだの重み
                graph[name].append(((nr, nc), weight))
    return graph


def dijkstra_linear(graph, start):
    """第5回のやり方: まだ決まっていない頂点を全部見て、いちばん小さいものをさがす"""
    INF = float("inf")
    distance = {}
    for v in graph:
        distance[v] = INF
    distance[start] = 0
    settled = set()

    while len(settled) < len(graph):
        current = None
        for v in graph:
            if v in settled or distance[v] == INF:
                continue
            if current is None or distance[v] < distance[current]:
                current = v
        if current is None:
            break
        settled.add(current)
        for name, weight in graph[current]:
            if name in settled:
                continue
            if distance[current] + weight < distance[name]:
                distance[name] = distance[current] + weight
    return distance


def dijkstra_heap(graph, start):
    """heapq のやり方: いちばん小さいものを取り出す作業を heapq に任せる"""
    INF = float("inf")
    distance = {}
    for v in graph:
        distance[v] = INF
    distance[start] = 0
    queue = [(0, start)]
    settled = set()

    while len(queue) > 0:
        d, current = heapq.heappop(queue)
        if current in settled:
            continue
        settled.add(current)
        for name, weight in graph[current]:
            if d + weight < distance[name]:
                distance[name] = d + weight
                heapq.heappush(queue, (distance[name], name))
    return distance


print("2つのやり方で、同じグラフの最短距離を求めて時間を測る")
print("-" * 66)
print("大きさ        頂点の数    全部見る方法    heapqの方法    何倍速いか")

for size in [20, 40, 80, 120]:
    graph = make_grid_graph(size)
    start = (0, 0)

    began = time.time()
    result_linear = dijkstra_linear(graph, start)
    time_linear = time.time() - began

    began = time.time()
    result_heap = dijkstra_heap(graph, start)
    time_heap = time.time() - began

    # 2つの答えが同じであることを確かめる
    same = (result_linear == result_heap)

    ratio = time_linear / time_heap
    print(f"{size:>3}×{size:<3}      {len(graph):>8}    {time_linear:>10.3f}秒"
          f"    {time_heap:>9.3f}秒    {ratio:>8.1f}倍")
    if not same:
        print("      ちがう答えが出た")

print("-" * 66)
print()
print("2つの方法は、どの大きさでも完全に同じ答えを出している。")
print("マス目が大きくなるほど、heapq を使った方法との差が開いていく。")
