# 20都市の巡回セールスマン問題を、5つの方法で解いて比べる
import heapq
import math
import random
import time

random.seed(2026)

cities = []
for i in range(20):
    cities.append(((i * 7) % 23, (i * 11) % 19))

n = len(cities)
INF = float("inf")

distance = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(math.sqrt((cities[i][0] - cities[j][0]) ** 2
                             + (cities[i][1] - cities[j][1]) ** 2))
    distance.append(row)


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def tour_length(order):
    """0番から出発し、order の順に回って0番へ戻るまでの合計距離を返す"""
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    return total + distance[here][0]


def greedy_from(start):
    """start を出発点にして、貪欲法でルートを作る"""
    visited = [start]
    here = start
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        visited.append(nearest)
        here = nearest
    # 0番から始まる形に直して長さを求める
    total = 0.0
    for i in range(len(visited)):
        total = total + distance[visited[i]][visited[(i + 1) % n]]
    return total, visited


def greedy():
    """貪欲法（出発点は0番の都市に固定）"""
    total, visited = greedy_from(0)
    return total


def greedy_all_starts():
    """すべての都市を出発点にして貪欲法を試し、いちばん良い答えを選ぶ"""
    best = None
    for start in range(n):
        total, visited = greedy_from(start)
        if best is None or total < best:
            best = total
    return best


def annealing():
    """焼きなまし法: 悪くなる変更もときどき受け入れながら、少しずつ短くする"""
    total, visited = greedy_from(0)
    order = visited[1:]
    current = tour_length(order)
    best = current
    temperature = 10.0
    for step in range(20000):
        i = random.randrange(n - 1)
        j = random.randrange(n - 1)
        if i == j:
            continue
        candidate = list(order)
        candidate[i], candidate[j] = candidate[j], candidate[i]
        new_length = tour_length(candidate)
        difference = new_length - current
        if difference < 0 or random.random() < math.exp(-difference / temperature):
            order = candidate
            current = new_length
            if current < best:
                best = current
        temperature = temperature * 0.9995
    return best


def genetic():
    """遺伝的アルゴリズム: 良いルートどうしを組み合わせて世代を進める"""
    population = []
    for i in range(100):
        order = list(range(1, n))
        random.shuffle(order)
        population.append(order)
    best_order = min(population, key=tour_length)
    best = tour_length(best_order)

    for generation in range(1000):
        next_population = [list(best_order)]
        while len(next_population) < 100:
            parents = []
            for k in range(2):
                # 3つをランダムに選び、その中でいちばん短いものを親にする
                three = []
                for t in range(3):
                    three.append(random.choice(population))
                best_of_three = three[0]
                for candidate in three:
                    if tour_length(candidate) < tour_length(best_of_three):
                        best_of_three = candidate
                parents.append(best_of_three)
            size = n - 1
            left = random.randrange(size)
            right = random.randrange(size)
            if left > right:
                left, right = right, left
            child = [None] * size
            for i in range(left, right + 1):
                child[i] = parents[0][i]
            used = set(child[left:right + 1])
            position = 0
            for city in parents[1]:
                if city in used:
                    continue
                while child[position] is not None:
                    position = position + 1
                child[position] = city
            if random.random() < 0.3:
                i = random.randrange(size)
                j = random.randrange(size)
                child[i], child[j] = child[j], child[i]
            next_population.append(child)
        population = next_population
        for order in population:
            length = tour_length(order)
            if length < best:
                best = length
                best_order = list(order)
    return best


def bit_dp():
    """動的計画法（bitDP）: 「回った集合」と「いまいる都市」で表を作り、最適解を求める"""
    full = (1 << n) - 1
    best = []
    for visited in range(1 << n):
        best.append([INF] * n)
    best[1][0] = 0.0
    for visited in range(1 << n):
        row = best[visited]
        for here in range(n):
            if row[here] == INF:
                continue
            for nxt in range(n):
                if visited & (1 << nxt):
                    continue
                if row[here] + distance[here][nxt] < best[visited | (1 << nxt)][nxt]:
                    best[visited | (1 << nxt)][nxt] = row[here] + distance[here][nxt]
    answer = INF
    for here in range(n):
        if best[full][here] < INF:
            answer = min(answer, best[full][here] + distance[here][0])
    return answer


methods = [
    ("貪欲法", greedy, "第9回", "近似解"),
    ("貪欲法(全出発点)", greedy_all_starts, "第11回", "近似解"),
    ("焼きなまし法", annealing, "第15回", "近似解"),
    ("遺伝的アルゴリズム", genetic, "第15回", "近似解"),
    ("bitDP", bit_dp, "第10回", "必ず最適"),
]

print(f"{n}都市の巡回セールスマン問題を5つの方法で解く")
print("（全探索なら 19! ＝ 約12京通り。まったく終わらない）")
print("=" * 76)
print(pad("方法", 24) + pad("答え", 10) + pad("最適との差", 18)
      + pad("かかった時間", 16) + "学んだ回")

results = []
for name, function, week, note in methods:
    began = time.time()
    value = function()
    elapsed = time.time() - began
    results.append((name, value, elapsed, week, note))

best_value = None
for name, value, elapsed, week, note in results:
    if best_value is None or value < best_value:
        best_value = value
for name, value, elapsed, week, note in results:
    gap = value - best_value
    print(pad(name, 24) + pad(f"{round(value, 1)}", 10)
          + pad(f"+{round(gap, 1)}（{round(gap/best_value*100, 1)}%）" if gap > 0 else "最適", 18)
          + pad(f"{elapsed:.3f}秒", 16) + week)
print("=" * 76)
print()
print("bitDP だけが「必ず最適」を保証する。ほかの4つは近似解。")
print("しかし都市が25個を超えると bitDP も使えなくなり、近似解に頼るしかなくなる。")
