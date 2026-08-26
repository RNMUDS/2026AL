# 発展手法その2: 遺伝的アルゴリズム（いでんてきアルゴリズム / Genetic Algorithm）
# 考え方: たくさんのルートを「集団」として持ち、
#         良いルートどうしを組み合わせて次の世代を作ることをくり返す。
#         生き物の進化をまねた方法。
import math
import random

random.seed(2026)

cities = []
for i in range(20):
    cities.append(((i * 7) % 23, (i * 11) % 19))

n = len(cities)
distance = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(math.sqrt((cities[i][0] - cities[j][0]) ** 2
                             + (cities[i][1] - cities[j][1]) ** 2))
    distance.append(row)


def tour_length(order):
    total = 0.0
    here = 0
    for city in order:
        total = total + distance[here][city]
        here = city
    return total + distance[here][0]


def make_random_order():
    """0番以外の都市をばらばらに並べたルートを1つ作る"""
    order = list(range(1, n))
    random.shuffle(order)
    return order


def choose_parent(population):
    """3つをランダムに選び、その中でいちばん短いものを親にする（トーナメント選択）"""
    a = random.choice(population)
    b = random.choice(population)
    c = random.choice(population)
    return min([a, b, c], key=tour_length)


def crossover(parent1, parent2):
    """2つの親から子を作る。
    親1の一部をそのまま使い、残りを親2に出てくる順に並べる。"""
    size = len(parent1)
    left = random.randrange(size)
    right = random.randrange(size)
    if left > right:
        left, right = right, left

    child = [None] * size
    for i in range(left, right + 1):
        child[i] = parent1[i]              # 親1から受けつぐ部分

    used = set(child[left:right + 1])
    position = 0
    for city in parent2:
        if city in used:
            continue
        while child[position] is not None:
            position = position + 1
        child[position] = city             # 残りは親2の順に入れる
    return child


def mutate(order):
    """まれに2か所を入れかえる（突然変異）"""
    if random.random() < 0.3:
        i = random.randrange(len(order))
        j = random.randrange(len(order))
        order[i], order[j] = order[j], order[i]
    return order


population_size = 100
generations = 1000

# 第1世代をランダムに作る
population = []
for i in range(population_size):
    population.append(make_random_order())

best_order = min(population, key=tour_length)
best_length = tour_length(best_order)

print("遺伝的アルゴリズムで20都市のルートを短くしていく")
print("-" * 62)
print(f"  集団の大きさ: {population_size} ／ 世代数: {generations}")
print()
print("  世代      集団の平均      いちばん良いルート")
print("  " + "-" * 46)

for generation in range(generations):
    # 次の世代を作る
    next_population = [list(best_order)]        # いちばん良いものは必ず残す
    while len(next_population) < population_size:
        parent1 = choose_parent(population)
        parent2 = choose_parent(population)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_population.append(child)
    population = next_population

    for order in population:
        length = tour_length(order)
        if length < best_length:
            best_length = length
            best_order = list(order)

    if generation % 100 == 0:
        average = sum(tour_length(o) for o in population) / len(population)
        print(f"  {generation:>4}   {round(average, 1):>12}   {round(best_length, 1):>18}")

print("  " + "-" * 46)
print()
print(f"  最後のルート: {round(best_length, 1)}")
print("-" * 62)
print()
print("最初はばらばらのルートしかないが、良いものどうしを組み合わせるうちに短くなっていく。")
print("集団の平均も、世代が進むにつれて下がっていく。")
