# print デバッグ: プログラムの途中に print を入れて、変数の中身を目で見る
# ここでは「貪欲法で配達ルートを作る関数」にバグを1つしこんである。
import math

places = [
    ("営業所", 0, 0),
    ("A宅", 3, 1),
    ("B宅", 1, 4),
    ("C宅", 6, 2),
]

n = len(places)
distance = []
for i in range(n):
    row = []
    for j in range(n):
        d = math.sqrt((places[i][1] - places[j][1]) ** 2 + (places[i][2] - places[j][2]) ** 2)
        row.append(round(d, 2))
    distance.append(row)

print("距離の表")
print("      " + "".join(f"{j:>8}" for j in range(n)))
for i in range(n):
    print(f"  {i}   " + "".join(f"{distance[i][j]:>8}" for j in range(n)))
print()


def greedy_buggy():
    """貪欲法でルートを作る（バグあり）"""
    visited = [0]
    here = 0
    while len(visited) < n:
        nearest = 0                       # ← ここがバグ。0番はすでに訪問済みなのに初期値にしている
        for j in range(n):
            if j in visited:
                continue
            if distance[here][j] < distance[here][nearest]:
                nearest = j
        visited.append(nearest)
        here = nearest
    return visited


def greedy_with_print():
    """同じ関数に print を入れて、中で何が起きているかを見る"""
    visited = [0]
    here = 0
    while len(visited) < n:
        nearest = 0
        print(f"  [ここまで] visited={visited}  here={here}  nearest の初期値={nearest}")
        for j in range(n):
            if j in visited:
                print(f"      j={j} はすでに訪問済み → とばす")
                continue
            print(f"      j={j}: distance[{here}][{j}]={distance[here][j]}"
                  f"  vs  distance[{here}][{nearest}]={distance[here][nearest]}")
            if distance[here][j] < distance[here][nearest]:
                nearest = j
                print(f"        → nearest を {j} に更新")
        print(f"  [結果] nearest={nearest} を訪問する")
        print()
        visited.append(nearest)
        here = nearest
    return visited


def greedy_fixed():
    """修正版: nearest の初期値を None にして、最初の1件で必ず更新されるようにする"""
    visited = [0]
    here = 0
    while len(visited) < n:
        nearest = None
        for j in range(n):
            if j in visited:
                continue
            if nearest is None or distance[here][j] < distance[here][nearest]:
                nearest = j
        visited.append(nearest)
        here = nearest
    return visited


print("=" * 62)
print("バグのある関数の結果")
print("=" * 62)
result = greedy_buggy()
print("  訪問した順番:", result)
print("  同じ場所が2回入っていないか:", len(result) != len(set(result)))
print()

print("=" * 62)
print("print を入れて、中で何が起きているかを見る")
print("=" * 62)
greedy_with_print()

print("=" * 62)
print("修正版の結果")
print("=" * 62)
result = greedy_fixed()
print("  訪問した順番:", result)
names = [places[i][0] for i in result]
print("  ルート:", " → ".join(names) + " → " + places[0][0])
print()
print("print を入れると、どの行で判断がおかしくなったかが目で見える。")
print("バグが直ったら、入れた print は消す。")
