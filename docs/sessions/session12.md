# 第12回: アルゴリズムの効率比較

## 学習目標

- **Big O 記法**で主要な計算量を理解し、アルゴリズムの効率を比較できる
- **幅優先探索**（BFS）をキューを使って実装し、最短経路を見つけられる
- **深さ優先探索**（DFS）をスタック/再帰で実装できる
- BFS と DFS の違いを迷路探索で体感する

---

## 1. 説明

### 1.1 Big O 記法（計算量の表し方）

アルゴリズムの効率を表すために **Big O 記法** を使います。
データ量 n が増えたとき、処理時間がどのように増加するかを示します。

| Big O | 名前 | 例 | n=1000 のとき |
|-------|------|-----|--------------|
| O(1) | 定数時間 | 配列のインデックスアクセス | 1回 |
| O(log n) | 対数時間 | 二分探索 | 約10回 |
| O(n) | 線形時間 | 配列の全要素走査 | 1,000回 |
| O(n log n) | 線形対数時間 | マージソート、Timsort | 約10,000回 |
| O(n^2) | 二乗時間 | 挿入ソート、バブルソート | 1,000,000回 |
| O(2^n) | 指数時間 | 全組み合わせ探索 | 天文学的数字 |

```
処理時間
 ↑
 |                                        / O(2^n)
 |                                      /
 |                                    /
 |                              ___/ O(n^2)
 |                        ___/
 |                  ___/
 |           ___--- O(n log n)
 |     __--- ̄ ̄ ̄ ̄ O(n)
 | _-- ̄ ̄ ̄ ̄ ̄ ̄ ̄ ̄ O(log n)
 |_________________________ O(1)
 +----------------------------→ データ量 n
```

### 1.2 これまで学んだアルゴリズムの計算量

| アルゴリズム | 最良 | 平均 | 最悪 | 空間 |
|---|---|---|---|---|
| 挿入ソート | O(n) | O(n^2) | O(n^2) | O(1) |
| 二分挿入ソート | O(n log n) | O(n^2) | O(n^2) | O(1) |
| バブルソート | O(n) | O(n^2) | O(n^2) | O(1) |
| 選択ソート | O(n^2) | O(n^2) | O(n^2) | O(1) |
| シェルソート | O(n log n) | O(n^1.3) | O(n^2) | O(1) |
| 分布数えソート | O(n+k) | O(n+k) | O(n+k) | O(n+k) |
| Python sorted() | O(n) | O(n log n) | O(n log n) | O(n) |

### 1.3 グラフ探索: BFS と DFS

迷路を解くなどの「経路探索」には、2つの基本的な方法があります。

**BFS（幅優先探索 / Breadth-First Search）**
- **キュー**（先入れ先出し: FIFO）を使う
- スタート地点から近い順に探索する
- **最短経路が見つかる**

```
探索順序: 近い場所から順に広がる
  1 → 2 → 3 → 4 → 5 → 6 → 7 → ...
     ↗   ↗       ↗   ↗
  1近傍   2近傍    3近傍

キュー: [スタート] → [近傍1, 近傍2] → [近傍2, 近傍1の近傍] → ...
```

**DFS（深さ優先探索 / Depth-First Search）**
- **スタック**（後入れ先出し: LIFO）または**再帰**を使う
- 行けるところまで深く進み、行き止まりで戻る
- 最短経路とは限らないが、メモリ使用量が少ない

```
探索順序: 深く深く進んでから戻る
  1 → 2 → 4 → 8（行き止まり）
                ↓ 戻る
           4 → 9 → ...

スタック: [スタート] → [近傍1] → [近傍1の近傍] → ...
```

### 1.4 迷路の表現

迷路を2次元リスト（グリッド）で表します。

```
0 = 通路（通れる）
1 = 壁（通れない）

maze = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]
スタート = (0, 0)  左上
ゴール   = (4, 4)  右下
```

---

## 2. 例題

### 例題1: 2次元グリッドで迷路を表現して表示する

```python
def create_maze():
    """5x5の迷路を2次元リストで作成する"""

    maze = [  # 0=通路、1=壁
        [0, 0, 0, 0, 0],  # 0行目: 全て通路
        [1, 1, 1, 1, 0],  # 1行目: ほぼ壁
        [0, 0, 0, 0, 0],  # 2行目: 全て通路
        [0, 1, 1, 1, 1],  # 3行目: ほぼ壁
        [0, 0, 0, 0, 0],  # 4行目: 全て通路
    ]
    return maze  # 迷路を返す


def display_maze(maze, start, goal, path=None):
    """迷路を絵文字で表示する"""

    path_set = set()  # 経路のマスを集合に格納する
    if path is not None:  # 経路がある場合
        for pos in path:  # 各座標を追加する
            path_set.add(pos)  # 集合に追加する

    rows = len(maze)  # 行数を取得する
    cols = len(maze[0])  # 列数を取得する

    for r in range(rows):  # 各行を処理する
        line = ""  # 1行分の文字列を初期化する
        for c in range(cols):  # 各列を処理する
            if (r, c) == start:  # スタート地点の場合
                line += "\U0001f6b6"  # 歩く人の絵文字
            elif (r, c) == goal:  # ゴール地点の場合
                line += "\U0001f3c1"  # チェッカーフラグの絵文字
            elif (r, c) in path_set:  # 経路上のマスの場合
                line += "\U0001f43e"  # 足跡の絵文字
            elif maze[r][c] == 1:  # 壁の場合
                line += "\U0001f7eb"  # 茶色の四角
            else:  # 通路の場合
                line += "\U0001f7e9"  # 緑色の四角
        print(line)  # 1行を表示する


# --- 実行 ---
maze = create_maze()  # 迷路を作成する
start = (0, 0)  # スタート地点を設定する
goal = (4, 4)  # ゴール地点を設定する

print("===== 迷路 =====")  # タイトルを表示する
display_maze(maze, start, goal)  # 迷路を表示する
```

### 例題2: deque を使った BFS の基本実装

```python
from collections import deque  # 両端キューを読み込む

def bfs_solve(maze, start, goal):
    """BFSで迷路を解いて最短経路を返す"""

    rows = len(maze)  # 行数を取得する
    cols = len(maze[0])  # 列数を取得する

    visited = []  # 訪問済みマップを用意する
    for r in range(rows):  # 各行を初期化する
        visited.append([False] * cols)  # 全てFalseで初期化する

    parent = []  # 経路復元用マップを用意する
    for r in range(rows):  # 各行を初期化する
        parent.append([None] * cols)  # 全てNoneで初期化する

    queue = deque()  # キューを作成する
    queue.append(start)  # スタートをキューに入れる
    visited[start[0]][start[1]] = True  # スタートを訪問済みにする

    explored_count = 0  # 探索したマス数を初期化する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右の移動方向

    while queue:  # キューが空になるまで繰り返す
        x, y = queue.popleft()  # キューの先頭を取り出す（FIFO）
        explored_count += 1  # 探索カウントを増やす

        if (x, y) == goal:  # ゴールに到達した場合
            path = []  # 経路リストを用意する
            pos = goal  # ゴールから逆にたどる
            while pos is not None:  # スタートに戻るまで
                path.append(pos)  # 現在位置を追加する
                pos = parent[pos[0]][pos[1]]  # 親をたどる
            path.reverse()  # スタートからゴールの順にする
            return path, explored_count  # 経路と探索数を返す

        for dx, dy in directions:  # 4方向を探索する
            nx, ny = x + dx, y + dy  # 隣接マスの座標を計算する
            if nx < 0 or nx >= rows or ny < 0 or ny >= cols:  # 範囲外ならスキップ
                continue  # 次の方向へ
            if maze[nx][ny] == 1:  # 壁ならスキップ
                continue  # 次の方向へ
            if visited[nx][ny]:  # 訪問済みならスキップ
                continue  # 次の方向へ
            visited[nx][ny] = True  # 訪問済みにする
            parent[nx][ny] = (x, y)  # 親を記録する
            queue.append((nx, ny))  # キューに追加する

    return None, explored_count  # ゴールに到達できなかった


# --- 実行 ---
maze = [  # テスト迷路
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]
start = (0, 0)  # スタート
goal = (4, 4)  # ゴール

path, explored = bfs_solve(maze, start, goal)  # BFSを実行する
if path:  # 経路が見つかった場合
    print(f"最短経路（{len(path)}マス）: {path}")  # 経路を表示する
    print(f"探索したマス数: {explored}")  # 探索数を表示する
```

### 例題3: 経路復元とパス表示

```python
from collections import deque  # 両端キューを読み込む

def bfs_with_path_display(maze, start, goal):
    """BFSで経路を見つけて迷路上に表示する"""

    rows = len(maze)  # 行数を取得する
    cols = len(maze[0])  # 列数を取得する

    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化する
        visited.append([False] * cols)  # Falseで埋める

    parent = []  # 経路復元用マップ
    for r in range(rows):  # 初期化する
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キューを作成する
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済みにする

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    # --- BFS本体 ---
    found = False  # ゴール到達フラグ
    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        if (x, y) == goal:  # ゴールに到達したら
            found = True  # フラグを立てる
            break  # ループを抜ける
        for dx, dy in directions:  # 4方向を探索する
            nx, ny = x + dx, y + dy  # 隣接マスを計算する
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内なら
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問なら
                    visited[nx][ny] = True  # 訪問済みにする
                    parent[nx][ny] = (x, y)  # 親を記録する
                    queue.append((nx, ny))  # キューに追加する

    if not found:  # ゴールに到達できなかった場合
        print("ゴールに到達できませんでした")  # メッセージ
        return None  # Noneを返す

    # --- 経路を復元する ---
    path = []  # 経路リスト
    pos = goal  # ゴールから開始する
    while pos is not None:  # スタートに戻るまで
        path.append(pos)  # 現在位置を追加する
        pos = parent[pos[0]][pos[1]]  # 親をたどる
    path.reverse()  # 順序を反転する

    # --- 経路をステップごとに表示する ---
    print("経路の復元過程:")  # タイトル
    for i in range(len(path)):  # 各ステップを処理する
        if i == 0:  # 最初のステップ
            print(f"  ステップ0: スタート {path[i]}")  # スタートを表示する
        else:  # 以降のステップ
            prev = path[i - 1]  # 前のマスを取得する
            curr = path[i]  # 現在のマスを取得する
            dx = curr[0] - prev[0]  # 行の移動量を計算する
            dy = curr[1] - prev[1]  # 列の移動量を計算する
            direction = ""  # 方向文字列を初期化する
            if dx == -1:  # 上に移動した場合
                direction = "上"
            elif dx == 1:  # 下に移動した場合
                direction = "下"
            elif dy == -1:  # 左に移動した場合
                direction = "左"
            elif dy == 1:  # 右に移動した場合
                direction = "右"
            print(f"  ステップ{i}: {prev} → {direction} → {curr}")  # 移動を表示する

    return path  # 経路を返す


# --- 実行 ---
maze = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]
start = (0, 0)  # スタート
goal = (4, 4)  # ゴール

path = bfs_with_path_display(maze, start, goal)  # BFSを実行する

if path:  # 経路がある場合
    print(f"\n最短経路の長さ: {len(path)} マス")  # 長さを表示する
    display_maze(maze, start, goal, path)  # 迷路を表示する
```

### 例題4: DFS（スタック版）の基本実装

```python
def dfs_solve(maze, start, goal):
    """DFS（スタック版）で迷路を解く"""

    rows = len(maze)  # 行数を取得する
    cols = len(maze[0])  # 列数を取得する

    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化する
        visited.append([False] * cols)  # Falseで埋める

    parent = []  # 経路復元用マップ
    for r in range(rows):  # 初期化する
        parent.append([None] * cols)  # Noneで埋める

    stack = [start]  # スタックにスタートを入れる
    visited[start[0]][start[1]] = True  # 訪問済みにする
    explored_count = 0  # 探索カウントを初期化する

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while stack:  # スタックが空になるまで
        x, y = stack.pop()  # スタックの末尾を取り出す（LIFO）
        explored_count += 1  # 探索カウントを増やす

        if (x, y) == goal:  # ゴールに到達した場合
            path = []  # 経路リスト
            pos = goal  # ゴールから逆にたどる
            while pos is not None:  # スタートに戻るまで
                path.append(pos)  # 追加する
                pos = parent[pos[0]][pos[1]]  # 親をたどる
            path.reverse()  # 順序を反転する
            return path, explored_count  # 経路と探索数を返す

        for dx, dy in directions:  # 4方向を探索する
            nx, ny = x + dx, y + dy  # 隣接マスの座標
            if nx < 0 or nx >= rows or ny < 0 or ny >= cols:  # 範囲外ならスキップ
                continue  # 次へ
            if maze[nx][ny] == 1:  # 壁ならスキップ
                continue  # 次へ
            if visited[nx][ny]:  # 訪問済みならスキップ
                continue  # 次へ
            visited[nx][ny] = True  # 訪問済みにする
            parent[nx][ny] = (x, y)  # 親を記録する
            stack.append((nx, ny))  # スタックに追加する

    return None, explored_count  # ゴール未到達


# --- 実行 ---
maze = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]
start = (0, 0)  # スタート
goal = (4, 4)  # ゴール

# --- BFS ---
bfs_path, bfs_explored = bfs_solve(maze, start, goal)  # BFSを実行する
print("【BFS】")  # タイトル
if bfs_path:  # 経路がある場合
    print(f"  経路長: {len(bfs_path)}, 探索マス: {bfs_explored}")  # 結果を表示する

# --- DFS ---
dfs_path, dfs_explored = dfs_solve(maze, start, goal)  # DFSを実行する
print("【DFS】")  # タイトル
if dfs_path:  # 経路がある場合
    print(f"  経路長: {len(dfs_path)}, 探索マス: {dfs_explored}")  # 結果を表示する

# --- 比較 ---
print("\n【比較】")  # タイトル
print(f"  BFS経路長={len(bfs_path)}, DFS経路長={len(dfs_path)}")  # 比較を表示する
if len(bfs_path) <= len(dfs_path):  # BFSが短い場合
    print("  BFSは最短経路を保証します")  # 説明する
```

### 例題5: 大きな迷路でBFS vs DFS のベンチマーク

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む
from collections import deque  # 両端キューを読み込む

def generate_maze(size, wall_rate=0.3):
    """ランダムな迷路を生成する"""

    maze = []  # 迷路リスト
    for i in range(size):  # 各行を生成する
        row = []  # 行リスト
        for j in range(size):  # 各列を生成する
            if random.random() < wall_rate:  # 壁率で判定する
                row.append(1)  # 壁を配置する
            else:  # 通路の場合
                row.append(0)  # 通路を配置する
        maze.append(row)  # 行を追加する

    maze[0][0] = 0  # スタートを通路にする
    maze[size - 1][size - 1] = 0  # ゴールを通路にする
    return maze  # 迷路を返す


def ensure_path(maze, start, goal):
    """BFSで到達可能か確認し、不可能なら経路を作る"""

    size = len(maze)  # サイズを取得する
    visited = []  # 訪問済みマップ
    for r in range(size):  # 初期化する
        visited.append([False] * size)  # Falseで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み

    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        if (x, y) == goal:  # ゴールに到達したら
            return True  # 到達可能
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < size and 0 <= ny < size:  # 範囲内なら
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済みにする
                    queue.append((nx, ny))  # 追加する

    # --- 到達不可能なので経路を作る ---
    x, y = start  # スタートから
    while x < goal[0]:  # 下方向に進む
        maze[x][y] = 0  # 通路にする
        x += 1  # 下に移動する
    while y < goal[1]:  # 右方向に進む
        maze[x][y] = 0  # 通路にする
        y += 1  # 右に移動する
    maze[goal[0]][goal[1]] = 0  # ゴールを通路にする
    return False  # 経路を作ったことを返す


def bfs_benchmark(maze, start, goal):
    """BFSのベンチマーク版"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化する
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化する
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数

    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        explored += 1  # 探索数を増やす
        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加する
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転する
            return path, explored  # 返す
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加
    return None, explored  # 未到達


def dfs_benchmark(maze, start, goal):
    """DFSのベンチマーク版"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化する
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化する
        parent.append([None] * cols)  # Noneで埋める

    stack = [start]  # スタック
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数

    while stack:  # スタックが空になるまで
        x, y = stack.pop()  # 末尾を取り出す
        explored += 1  # 探索数を増やす
        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加する
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転する
            return path, explored  # 返す
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    stack.append((nx, ny))  # 追加
    return None, explored  # 未到達


# --- ベンチマーク ---
random.seed(42)  # シードを固定する
size = 100  # 迷路サイズ
start = (0, 0)  # スタート
goal = (size - 1, size - 1)  # ゴール

maze = generate_maze(size, 0.3)  # 迷路を生成する
ensure_path(maze, start, goal)  # 経路を保証する

# --- BFS ---
start_time = time.time()  # 計測開始
bfs_path, bfs_explored = bfs_benchmark(maze, start, goal)  # BFS実行
bfs_time = time.time() - start_time  # 時間を計算する

# --- DFS ---
start_time = time.time()  # 計測開始
dfs_path, dfs_explored = dfs_benchmark(maze, start, goal)  # DFS実行
dfs_time = time.time() - start_time  # 時間を計算する

# --- 結果を表示する ---
print(f"迷路サイズ: {size}x{size}")  # サイズを表示する
print(f"\n{'指標':>10} {'BFS':>10} {'DFS':>10}")  # ヘッダー
print("-" * 32)  # 区切り線
if bfs_path and dfs_path:  # 両方見つかった場合
    print(f"{'経路長':>10} {len(bfs_path):>10} {len(dfs_path):>10}")  # 経路長
    print(f"{'探索マス':>10} {bfs_explored:>10} {dfs_explored:>10}")  # 探索数
    print(f"{'時間(秒)':>10} {bfs_time:>10.4f} {dfs_time:>10.4f}")  # 時間
```

---

## 3. 標準課題

### 標準課題1（超やさしい）: 5x5の迷路を2次元リストで作成して表示する

5x5の迷路を2次元リストで定義し、壁と通路を文字で表示してください。

**要件:**
- 0を通路、1を壁として迷路を定義する
- `#` を壁、`.` を通路として表示する
- スタート(0,0)を `S`、ゴール(4,4)を `G` で表示する

### 標準課題2（超やさしい）: 迷路を絵文字で表示する

課題1の迷路を絵文字で表示してください。

**要件:**
- 壁、通路、スタート、ゴールにそれぞれ絵文字を使う
- 10x10の迷路で実装する
- 迷路のサイズ（行数x列数）と壁の数も表示する

### 標準課題3（やさしい）: BFSで迷路を解いて経路を表示する

`deque` を使った BFS で5x5迷路を解き、見つかった経路を表示してください。

**要件:**
- `collections.deque` を使ってキューを実装する
- 経路を座標のリストとして表示する
- 経路の長さ（マス数）を表示する

### 標準課題4（やさしい）: BFSで10x10迷路を解いて経路を迷路上に描画する

10x10の迷路を BFS で解き、経路を迷路上に絵文字で表示してください。

**要件:**
- 経路上のマスを足跡の絵文字で表示する
- 探索したマスの数も表示する
- 経路が見つからない場合のエラーメッセージも実装する

### 標準課題5（やややさしい）: BFSの経路復元をステップごとに表示する

BFS でゴールに到達した後、ゴールからスタートへの経路復元過程をステップごとに表示してください。

**要件:**
- `parent` マップを使ってゴールから逆順にたどる
- 各ステップで「どこから来たか」を表示する
- 最終的にスタートからゴールへの経路を表示する

### 標準課題6（やややさしい）: 経路上に方向矢印を表示する

BFS の経路を迷路上に表示する際、移動方向を矢印（上下左右）で示してください。

**要件:**
- 上移動を `^`、下を `v`、左を `<`、右を `>` で表示する
- スタートとゴールは絵文字のまま
- テキスト版と絵文字版の両方で表示する

### 標準課題7（やや普通）: DFS（スタック版）を実装して経路を表示する

DFS をスタック（リスト）で実装し、BFS と同じ迷路を解いてください。

**要件:**
- `list.append()` と `list.pop()` でスタックを実装する
- 経路と探索マス数を表示する
- BFS の結果と経路長を比較する

### 標準課題8（やや普通）: BFS と DFS の経路を並べて比較する

同じ10x10迷路に対して BFS と DFS を実行し、2つの経路を並べて表示してください。

**要件:**
- BFS と DFS の迷路をそれぞれ絵文字で表示する
- 経路長・探索マス数の比較表を出力する
- BFS が最短であることを確認する

### 標準課題9（普通）: ランダム迷路を生成して BFS で解く

指定サイズのランダム迷路を生成し、BFS で解くプログラムを作成してください。

**要件:**
- 迷路サイズと壁の割合を引数で指定できる
- スタートからゴールへの経路が存在することを保証する
- 経路が見つかった場合は迷路上に描画する
- 20x20 の迷路で動作確認する

### 標準課題10（普通）: 複数サイズの迷路で BFS vs DFS の性能を分析する

50x50、100x100、200x200 のランダム迷路で BFS と DFS の実行時間・探索マス数・経路長を比較し、考察してください。

**要件:**
- 各サイズで3回計測して平均を取る
- 結果を表形式で表示する
- BFS と DFS の特徴を考察する

---

## 4. 発展課題

### 発展課題1: A* 探索の入門実装

BFS を拡張して、ゴールまでの推定距離（マンハッタン距離）を使った A* 探索を実装してください。

**要件:**
- 優先度キュー（`heapq`）を使う
- マンハッタン距離をヒューリスティック関数にする
- BFS と A* の探索マス数を比較する
- 同じ迷路で両方を実行して結果を比較する

### 発展課題2: アイテム収集迷路

迷路内に複数のアイテムが配置されており、全てのアイテムを収集してゴールにたどり着くプログラムを作成してください。

**要件:**
- 迷路に3つのアイテムを配置する
- BFS を使って最寄りのアイテムから順に収集する
- 全アイテム収集後にゴールへ向かう
- 各区間の経路を迷路上に表示する

---

## 5. 解答例

### 課題1の解答例

```python
def create_maze_5x5():
    """5x5の迷路を作成する"""

    maze = [  # 0=通路、1=壁
        [0, 0, 0, 1, 0],  # 0行目
        [1, 1, 0, 1, 0],  # 1行目
        [0, 0, 0, 0, 0],  # 2行目
        [0, 1, 1, 1, 0],  # 3行目
        [0, 0, 0, 0, 0],  # 4行目
    ]
    return maze  # 迷路を返す


def display_text(maze, start, goal):
    """迷路をテキストで表示する"""

    rows = len(maze)  # 行数を取得する
    cols = len(maze[0])  # 列数を取得する

    for r in range(rows):  # 各行を処理する
        line = ""  # 行文字列を初期化する
        for c in range(cols):  # 各列を処理する
            if (r, c) == start:  # スタートの場合
                line += "S "  # Sを表示する
            elif (r, c) == goal:  # ゴールの場合
                line += "G "  # Gを表示する
            elif maze[r][c] == 1:  # 壁の場合
                line += "# "  # #を表示する
            else:  # 通路の場合
                line += ". "  # .を表示する
        print(line)  # 行を出力する


# --- 実行 ---
maze = create_maze_5x5()  # 迷路を作成する
start = (0, 0)  # スタートを設定する
goal = (4, 4)  # ゴールを設定する

print("===== 5x5 迷路 =====")  # タイトルを表示する
display_text(maze, start, goal)  # 迷路を表示する
```

### 課題2の解答例

```python
def display_emoji(maze, start, goal, path=None):
    """迷路を絵文字で表示する"""

    path_set = set()  # 経路のマス集合
    if path is not None:  # 経路がある場合
        for pos in path:  # 各座標を追加する
            path_set.add(pos)  # 集合に追加する

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    wall_count = 0  # 壁の数を初期化する

    for r in range(rows):  # 各行を処理する
        line = ""  # 行文字列
        for c in range(cols):  # 各列を処理する
            if (r, c) == start:  # スタート
                line += "\U0001f6b6"  # 歩く人
            elif (r, c) == goal:  # ゴール
                line += "\U0001f3c1"  # チェッカーフラグ
            elif (r, c) in path_set:  # 経路上
                line += "\U0001f43e"  # 足跡
            elif maze[r][c] == 1:  # 壁
                line += "\U0001f7eb"  # 茶色
                wall_count += 1  # 壁カウントを増やす
            else:  # 通路
                line += "\U0001f7e9"  # 緑色
        print(line)  # 行を出力する

    print(f"\n迷路サイズ: {rows}x{cols}")  # サイズを表示する
    print(f"壁の数: {wall_count}")  # 壁の数を表示する


# --- 実行 ---
maze_10x10 = [  # 10x10の迷路
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
start = (0, 0)  # スタート
goal = (9, 9)  # ゴール

print("===== 10x10 迷路 =====")  # タイトル
display_emoji(maze_10x10, start, goal)  # 表示する
```

### 課題3の解答例

```python
from collections import deque  # 両端キューを読み込む

def bfs_basic(maze, start, goal):
    """BFSで迷路を解く基本実装"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数

    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化する
        visited.append([False] * cols)  # Falseで埋める

    parent = []  # 経路復元用
    for r in range(rows):  # 初期化する
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キューを作成する
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済みにする

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        if (x, y) == goal:  # ゴールに到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加する
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転する
            return path  # 経路を返す

        for dx, dy in directions:  # 4方向を探索する
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済みにする
                    parent[nx][ny] = (x, y)  # 親を記録する
                    queue.append((nx, ny))  # キューに追加する

    return None  # ゴール未到達


# --- 実行 ---
maze = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
start = (0, 0)  # スタート
goal = (4, 4)  # ゴール

path = bfs_basic(maze, start, goal)  # BFSを実行する

if path:  # 経路がある場合
    print(f"経路が見つかりました!")  # メッセージ
    print(f"経路: {path}")  # 経路を表示する
    print(f"経路の長さ: {len(path)} マス")  # 長さを表示する
else:  # 経路がない場合
    print("ゴールに到達できませんでした")  # メッセージ
```

### 課題4の解答例

```python
from collections import deque  # 両端キューを読み込む

def bfs_with_count(maze, start, goal):
    """BFSで迷路を解く（探索マス数付き）"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済みマップ
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        explored += 1  # 探索数を増やす
        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加する
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転する
            return path, explored  # 返す
        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加

    return None, explored  # 未到達


# --- 実行 ---
maze_10x10 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
start = (0, 0)  # スタート
goal = (9, 9)  # ゴール

path, explored = bfs_with_count(maze_10x10, start, goal)  # BFS実行

if path:  # 経路がある場合
    print(f"経路が見つかりました!")  # メッセージ
    print(f"経路の長さ: {len(path)} マス")  # 長さ
    print(f"探索したマス: {explored} マス")  # 探索数
    display_emoji(maze_10x10, start, goal, path)  # 絵文字で表示する
else:  # 経路がない場合
    print(f"ゴールに到達できませんでした（探索マス: {explored}）")  # メッセージ
```

### 課題5の解答例

```python
from collections import deque  # 両端キューを読み込む

def bfs_trace_path(maze, start, goal):
    """BFSで経路復元過程を表示する"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    found = False  # 発見フラグ
    while queue:  # キューが空になるまで
        x, y = queue.popleft()  # 先頭を取り出す
        if (x, y) == goal:  # ゴール到達
            found = True  # フラグ
            break  # 終了
        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加

    if not found:  # 見つからなかった場合
        print("ゴールに到達できませんでした")  # メッセージ
        return None  # Noneを返す

    # --- 経路復元をステップごとに表示する ---
    print("【経路復元（ゴール → スタート）】")  # タイトル
    backward_path = []  # 逆順経路リスト
    pos = goal  # ゴールから開始する
    step = 0  # ステップカウンタ

    while pos is not None:  # スタートに戻るまで
        backward_path.append(pos)  # 追加する
        parent_pos = parent[pos[0]][pos[1]]  # 親を取得する
        if parent_pos is not None:  # 親がある場合
            print(f"  ステップ{step}: {pos} ← 親は {parent_pos}")  # 表示する
        else:  # スタートの場合
            print(f"  ステップ{step}: {pos} ← スタート（親なし）")  # 表示する
        pos = parent_pos  # 親に移動する
        step += 1  # ステップを増やす

    # --- 正順にする ---
    forward_path = backward_path[::-1]  # 反転する
    print(f"\n【経路（スタート → ゴール）】")  # タイトル
    print(f"  {' → '.join([str(p) for p in forward_path])}")  # 経路を表示する
    print(f"  経路の長さ: {len(forward_path)} マス")  # 長さを表示する

    return forward_path  # 経路を返す


# --- 実行 ---
maze = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
bfs_trace_path(maze, (0, 0), (4, 4))  # 経路復元を実行する
```

### 課題6の解答例

```python
from collections import deque  # 両端キューを読み込む

def bfs_with_directions(maze, start, goal):
    """BFSで経路に方向矢印を付けて表示する"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    found = False  # 発見フラグ
    while queue:  # ループ
        x, y = queue.popleft()  # 取り出す
        if (x, y) == goal:  # ゴール到達
            found = True  # フラグ
            break  # 終了
        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加

    if not found:  # 見つからなかった場合
        return None  # Noneを返す

    # --- 経路を復元する ---
    path = []  # 経路リスト
    pos = goal  # ゴールから
    while pos is not None:  # たどる
        path.append(pos)  # 追加
        pos = parent[pos[0]][pos[1]]  # 親へ
    path.reverse()  # 反転する

    # --- 方向マップを作成する ---
    direction_map = {}  # 座標→矢印のマップ
    for i in range(len(path) - 1):  # 各ステップを処理する
        curr = path[i]  # 現在位置
        nxt = path[i + 1]  # 次の位置
        dx = nxt[0] - curr[0]  # 行の差
        dy = nxt[1] - curr[1]  # 列の差
        if dx == -1:  # 上移動
            direction_map[curr] = "^"  # 上矢印
        elif dx == 1:  # 下移動
            direction_map[curr] = "v"  # 下矢印
        elif dy == -1:  # 左移動
            direction_map[curr] = "<"  # 左矢印
        elif dy == 1:  # 右移動
            direction_map[curr] = ">"  # 右矢印

    # --- テキスト版を表示する ---
    print("【テキスト版】")  # タイトル
    for r in range(rows):  # 各行
        line = ""  # 行文字列
        for c in range(cols):  # 各列
            if (r, c) == start:  # スタート
                line += "S "  # Sを表示する
            elif (r, c) == goal:  # ゴール
                line += "G "  # Gを表示する
            elif (r, c) in direction_map:  # 経路上
                line += direction_map[(r, c)] + " "  # 矢印を表示する
            elif maze[r][c] == 1:  # 壁
                line += "# "  # #を表示する
            else:  # 通路
                line += ". "  # .を表示する
        print(line)  # 出力する

    return path  # 経路を返す


# --- 実行 ---
maze = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
bfs_with_directions(maze, (0, 0), (4, 4))  # 方向矢印付きで表示する
```

### 課題7の解答例

```python
def dfs_basic(maze, start, goal):
    """DFS（スタック版）で迷路を解く"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める

    stack = [start]  # スタックにスタートを入れる
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while stack:  # スタックが空になるまで
        x, y = stack.pop()  # 末尾を取り出す（LIFO）
        explored += 1  # 探索数を増やす
        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転
            return path, explored  # 返す
        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    stack.append((nx, ny))  # スタックに追加

    return None, explored  # 未到達


# --- BFS も実行して比較する ---
from collections import deque  # 両端キューを読み込む

maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
start = (0, 0)  # スタート
goal = (9, 9)  # ゴール

# DFS
dfs_path, dfs_explored = dfs_basic(maze, start, goal)  # DFS実行
print("【DFS結果】")  # タイトル
if dfs_path:  # 経路がある場合
    print(f"  経路長: {len(dfs_path)}, 探索マス: {dfs_explored}")  # 表示する

# BFS
bfs_path, bfs_explored = bfs_with_count(maze, start, goal)  # BFS実行
print("【BFS結果】")  # タイトル
if bfs_path:  # 経路がある場合
    print(f"  経路長: {len(bfs_path)}, 探索マス: {bfs_explored}")  # 表示する

# 比較
print("\n【比較】")  # タイトル
if bfs_path and dfs_path:  # 両方ある場合
    print(f"  BFS経路長: {len(bfs_path)}（最短保証）")  # BFS結果
    print(f"  DFS経路長: {len(dfs_path)}（最短とは限らない）")  # DFS結果
```

### 課題8の解答例

```python
from collections import deque  # 両端キューを読み込む

def solve_and_display(maze, start, goal):
    """BFS/DFSで解いて並べて表示する"""

    # --- BFS ---
    bfs_path, bfs_explored = bfs_with_count(maze, start, goal)  # BFS実行

    # --- DFS ---
    dfs_path, dfs_explored = dfs_basic(maze, start, goal)  # DFS実行

    # --- BFS の迷路を表示する ---
    print("===== BFS の経路 =====")  # タイトル
    if bfs_path:  # 経路がある場合
        display_emoji(maze, start, goal, bfs_path)  # 表示する
    print()  # 空行

    # --- DFS の迷路を表示する ---
    print("===== DFS の経路 =====")  # タイトル
    if dfs_path:  # 経路がある場合
        display_emoji(maze, start, goal, dfs_path)  # 表示する

    # --- 比較表 ---
    print(f"\n{'指標':>10} {'BFS':>8} {'DFS':>8}")  # ヘッダー
    print("-" * 28)  # 区切り線
    if bfs_path and dfs_path:  # 両方ある場合
        print(f"{'経路長':>10} {len(bfs_path):>8} {len(dfs_path):>8}")  # 経路長
        print(f"{'探索マス':>10} {bfs_explored:>8} {dfs_explored:>8}")  # 探索数
        print(f"\nBFS経路は最短: {len(bfs_path) <= len(dfs_path)}")  # 確認


# --- 実行 ---
maze_10x10 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
solve_and_display(maze_10x10, (0, 0), (9, 9))  # 解いて表示する
```

### 課題9の解答例

```python
import random  # 乱数モジュールを読み込む
from collections import deque  # 両端キューを読み込む

def generate_random_maze(size, wall_rate=0.3):
    """ランダム迷路を生成する"""

    maze = []  # 迷路リスト
    for i in range(size):  # 各行
        row = []  # 行リスト
        for j in range(size):  # 各列
            if random.random() < wall_rate:  # 壁率で判定
                row.append(1)  # 壁
            else:  # 通路
                row.append(0)  # 通路
        maze.append(row)  # 行を追加する

    maze[0][0] = 0  # スタートを通路にする
    maze[size - 1][size - 1] = 0  # ゴールを通路にする
    return maze  # 迷路を返す


def guarantee_path(maze, start, goal):
    """経路の存在を保証する"""

    size = len(maze)  # サイズ
    visited = []  # 訪問済み
    for r in range(size):  # 初期化
        visited.append([False] * size)  # Falseで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み

    while queue:  # ループ
        x, y = queue.popleft()  # 取り出す
        if (x, y) == goal:  # ゴール到達
            return  # 経路がある
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < size and 0 <= ny < size:  # 範囲内
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    queue.append((nx, ny))  # 追加

    # --- 経路を作る ---
    x, y = start  # スタートから
    while x < goal[0]:  # 下に進む
        maze[x][y] = 0  # 通路にする
        x += 1  # 下へ
    while y < goal[1]:  # 右に進む
        maze[x][y] = 0  # 通路にする
        y += 1  # 右へ
    maze[goal[0]][goal[1]] = 0  # ゴールを通路にする


# --- 実行 ---
random.seed(42)  # シードを固定する
size = 20  # 20x20の迷路
start = (0, 0)  # スタート
goal = (size - 1, size - 1)  # ゴール

maze = generate_random_maze(size, 0.3)  # 迷路を生成する
guarantee_path(maze, start, goal)  # 経路を保証する

path, explored = bfs_with_count(maze, start, goal)  # BFSで解く

if path:  # 経路がある場合
    print(f"迷路サイズ: {size}x{size}")  # サイズ
    print(f"経路の長さ: {len(path)} マス")  # 経路長
    print(f"探索マス数: {explored}")  # 探索数
    print()  # 空行
    display_emoji(maze, start, goal, path)  # 表示する
```

### 課題10の解答例

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む
from collections import deque  # 両端キューを読み込む

def bfs_timed(maze, start, goal):
    """BFS（タイマー付き）"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める
    queue = deque()  # キュー
    queue.append(start)  # スタートを追加する
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数
    while queue:  # ループ
        x, y = queue.popleft()  # 取り出す
        explored += 1  # カウント
        if (x, y) == goal:  # ゴール
            path = []  # 経路
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転
            return len(path), explored  # 経路長と探索数を返す
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加
    return 0, explored  # 未到達


def dfs_timed(maze, start, goal):
    """DFS（タイマー付き）"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める
    stack = [start]  # スタック
    visited[start[0]][start[1]] = True  # 訪問済み
    explored = 0  # 探索数
    while stack:  # ループ
        x, y = stack.pop()  # 取り出す
        explored += 1  # カウント
        if (x, y) == goal:  # ゴール
            path = []  # 経路
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転
            return len(path), explored  # 返す
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if not visited[nx][ny] and maze[nx][ny] == 0:  # 通路かつ未訪問
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    stack.append((nx, ny))  # 追加
    return 0, explored  # 未到達


# --- ベンチマーク ---
sizes = [50, 100, 200]  # テストサイズ
trials = 3  # 計測回数

print(f"{'サイズ':>6} {'指標':>8} {'BFS':>10} {'DFS':>10}")  # ヘッダー
print("-" * 40)  # 区切り線

for size in sizes:  # 各サイズで計測する
    bfs_times = []  # BFS時間リスト
    dfs_times = []  # DFS時間リスト
    bfs_paths = []  # BFS経路長リスト
    dfs_paths = []  # DFS経路長リスト
    bfs_exps = []  # BFS探索数リスト
    dfs_exps = []  # DFS探索数リスト

    for t in range(trials):  # 各試行
        random.seed(42 + t)  # シードを設定する
        maze = generate_random_maze(size, 0.3)  # 迷路を生成する
        start = (0, 0)  # スタート
        goal = (size - 1, size - 1)  # ゴール
        guarantee_path(maze, start, goal)  # 経路を保証する

        # BFS
        st = time.time()  # 開始
        bp, be = bfs_timed(maze, start, goal)  # BFS実行
        bfs_times.append(time.time() - st)  # 時間を記録
        bfs_paths.append(bp)  # 経路長を記録
        bfs_exps.append(be)  # 探索数を記録

        # DFS
        st = time.time()  # 開始
        dp, de = dfs_timed(maze, start, goal)  # DFS実行
        dfs_times.append(time.time() - st)  # 時間を記録
        dfs_paths.append(dp)  # 経路長を記録
        dfs_exps.append(de)  # 探索数を記録

    # 平均を計算する
    avg_bt = sum(bfs_times) / trials  # BFS平均時間
    avg_dt = sum(dfs_times) / trials  # DFS平均時間
    avg_bp = sum(bfs_paths) / trials  # BFS平均経路長
    avg_dp = sum(dfs_paths) / trials  # DFS平均経路長
    avg_be = sum(bfs_exps) / trials  # BFS平均探索数
    avg_de = sum(dfs_exps) / trials  # DFS平均探索数

    print(f"{size:>4}x{size:<4} {'経路長':>6} {avg_bp:>10.1f} {avg_dp:>10.1f}")  # 経路長
    print(f"{'':>6} {'探索数':>8} {avg_be:>10.1f} {avg_de:>10.1f}")  # 探索数
    print(f"{'':>6} {'時間(s)':>8} {avg_bt:>10.4f} {avg_dt:>10.4f}")  # 時間

# --- 考察 ---
print("\n【考察】")  # タイトル
print("1. BFS は常に最短経路を見つける（経路長が最小）")  # 結論1
print("2. DFS は最短経路を保証しない（経路が長くなることがある）")  # 結論2
print("3. BFS はキューのメモリ使用量が大きい（幅に比例）")  # 結論3
print("4. DFS はスタックのメモリ使用量が小さい（深さに比例）")  # 結論4
print("5. 最短経路が必要ならBFS、全探索ならDFSが適切")  # 結論5
```

### 発展課題1の解答例

```python
import heapq  # 優先度キューモジュールを読み込む
from collections import deque  # 両端キューを読み込む

def manhattan_distance(pos, goal):
    """マンハッタン距離を計算する"""

    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # 行の差 + 列の差


def astar_solve(maze, start, goal):
    """A*探索で迷路を解く"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数

    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める
    g_cost = []  # スタートからの実コスト
    for r in range(rows):  # 初期化
        g_cost.append([float("inf")] * cols)  # 無限大で初期化

    g_cost[start[0]][start[1]] = 0  # スタートのコストは0
    h_cost = manhattan_distance(start, goal)  # ヒューリスティック
    heap = [(h_cost, 0, start)]  # 優先度キュー: (f, g, pos)
    explored = 0  # 探索数

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while heap:  # ヒープが空になるまで
        f, g, (x, y) = heapq.heappop(heap)  # 最小fを取り出す

        if visited[x][y]:  # 訪問済みならスキップ
            continue  # 次へ
        visited[x][y] = True  # 訪問済みにする
        explored += 1  # 探索数を増やす

        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転
            return path, explored  # 返す

        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] == 0 and not visited[nx][ny]:  # 通路かつ未訪問
                    new_g = g + 1  # 新しいgコスト
                    if new_g < g_cost[nx][ny]:  # より良い経路なら
                        g_cost[nx][ny] = new_g  # gコストを更新する
                        parent[nx][ny] = (x, y)  # 親を記録する
                        h = manhattan_distance((nx, ny), goal)  # ヒューリスティック
                        heapq.heappush(heap, (new_g + h, new_g, (nx, ny)))  # ヒープに追加

    return None, explored  # 未到達


# --- 比較 ---
import random  # 乱数モジュール

random.seed(42)  # シードを固定する
size = 30  # 30x30の迷路
maze = generate_random_maze(size, 0.25)  # 迷路を生成する
start = (0, 0)  # スタート
goal = (size - 1, size - 1)  # ゴール
guarantee_path(maze, start, goal)  # 経路を保証する

# BFS
bfs_path, bfs_explored = bfs_with_count(maze, start, goal)  # BFS実行

# A*
astar_path, astar_explored = astar_solve(maze, start, goal)  # A*実行

print(f"迷路サイズ: {size}x{size}")  # サイズ
print(f"\n{'指標':>10} {'BFS':>8} {'A*':>8}")  # ヘッダー
print("-" * 28)  # 区切り線
if bfs_path and astar_path:  # 両方ある場合
    print(f"{'経路長':>10} {len(bfs_path):>8} {len(astar_path):>8}")  # 経路長
    print(f"{'探索マス':>10} {bfs_explored:>8} {astar_explored:>8}")  # 探索数
    reduction = (1 - astar_explored / bfs_explored) * 100  # 削減率を計算する
    print(f"\nA*はBFSより探索マスが {reduction:.1f}% 少ない")  # 削減率を表示する
    print("A*はヒューリスティックでゴール方向を優先するため効率的")  # 説明
```

### 発展課題2の解答例

```python
from collections import deque  # 両端キューを読み込む

def bfs_shortest_path(maze, start, goal):
    """BFSで2点間の最短経路を求める"""

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    visited = []  # 訪問済み
    for r in range(rows):  # 初期化
        visited.append([False] * cols)  # Falseで埋める
    parent = []  # 経路復元用
    for r in range(rows):  # 初期化
        parent.append([None] * cols)  # Noneで埋める

    queue = deque()  # キュー
    queue.append(start)  # スタートを追加
    visited[start[0]][start[1]] = True  # 訪問済み

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向

    while queue:  # ループ
        x, y = queue.popleft()  # 取り出す
        if (x, y) == goal:  # ゴール到達
            path = []  # 経路リスト
            pos = goal  # ゴールから
            while pos is not None:  # たどる
                path.append(pos)  # 追加
                pos = parent[pos[0]][pos[1]]  # 親へ
            path.reverse()  # 反転
            return path  # 返す
        for dx, dy in directions:  # 4方向
            nx, ny = x + dx, y + dy  # 隣接マス
            if 0 <= nx < rows and 0 <= ny < cols:  # 範囲内
                if maze[nx][ny] != 1 and not visited[nx][ny]:  # 壁でない
                    visited[nx][ny] = True  # 訪問済み
                    parent[nx][ny] = (x, y)  # 親を記録
                    queue.append((nx, ny))  # 追加

    return None  # 未到達


def solve_item_maze(maze, start, goal, items):
    """アイテムを全て収集してゴールに到達する"""

    remaining = list(items)  # 残りアイテムのリスト
    current_pos = start  # 現在位置
    total_path = [start]  # 総経路リスト
    total_steps = 0  # 総ステップ数

    collected = 0  # 収集数
    while remaining:  # アイテムが残っている間
        # --- 最寄りのアイテムを見つける ---
        best_item = None  # 最良アイテム
        best_path = None  # 最良経路
        best_dist = float("inf")  # 最短距離

        for item in remaining:  # 各アイテムを試す
            path = bfs_shortest_path(maze, current_pos, item)  # 経路を求める
            if path and len(path) < best_dist:  # より短い経路なら
                best_item = item  # アイテムを更新する
                best_path = path  # 経路を更新する
                best_dist = len(path)  # 距離を更新する

        if best_path is None:  # 到達不能
            print(f"アイテム {remaining} に到達できません")  # メッセージ
            return None  # Noneを返す

        # --- アイテムに向かう ---
        collected += 1  # 収集数を増やす
        print(f"アイテム{collected}: {current_pos} → {best_item}（{len(best_path) - 1}歩）")  # 表示
        total_path.extend(best_path[1:])  # 経路を追加する（始点は重複するので除く）
        total_steps += len(best_path) - 1  # ステップを加算する
        current_pos = best_item  # 現在位置を更新する
        remaining.remove(best_item)  # アイテムを除去する

    # --- ゴールに向かう ---
    goal_path = bfs_shortest_path(maze, current_pos, goal)  # ゴールへの経路
    if goal_path:  # 経路がある場合
        print(f"ゴール:     {current_pos} → {goal}（{len(goal_path) - 1}歩）")  # 表示
        total_path.extend(goal_path[1:])  # 経路を追加する
        total_steps += len(goal_path) - 1  # ステップを加算する
    else:  # 経路がない場合
        print("ゴールに到達できません")  # メッセージ
        return None  # Noneを返す

    print(f"\n合計: {total_steps}歩")  # 合計ステップを表示する
    return total_path  # 総経路を返す


# --- 迷路とアイテムを定義する ---
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
start = (0, 0)  # スタート
goal = (9, 9)  # ゴール
items = [(2, 5), (6, 4), (8, 7)]  # アイテム位置

print("===== アイテム収集迷路 =====")  # タイトル
print(f"スタート: {start}")  # スタート
print(f"ゴール: {goal}")  # ゴール
print(f"アイテム: {items}")  # アイテム
print()  # 空行

# --- 解く ---
full_path = solve_item_maze(maze, start, goal, items)  # 解く

# --- 表示する ---
if full_path:  # 経路がある場合
    print()  # 空行

    # アイテム位置を含めた表示用のマップ
    path_set = set(full_path)  # 経路集合
    item_set = set(items)  # アイテム集合

    rows = len(maze)  # 行数
    cols = len(maze[0])  # 列数
    for r in range(rows):  # 各行
        line = ""  # 行文字列
        for c in range(cols):  # 各列
            if (r, c) == start:  # スタート
                line += "\U0001f6b6"  # 歩く人
            elif (r, c) == goal:  # ゴール
                line += "\U0001f3c1"  # チェッカーフラグ
            elif (r, c) in item_set:  # アイテム位置
                line += "\U0001f48e"  # 宝石
            elif (r, c) in path_set:  # 経路上
                line += "\U0001f43e"  # 足跡
            elif maze[r][c] == 1:  # 壁
                line += "\U0001f7eb"  # 茶色
            else:  # 通路
                line += "\U0001f7e9"  # 緑色
        print(line)  # 出力する
```

---

## 6. まとめ

### Big O 記法の重要なポイント

```
O(1)  < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)
 ↑        ↑         ↑        ↑            ↑         ↑
最速   二分探索    全走査   良いソート   単純ソート  組合せ
```

### BFS vs DFS の比較

| 特性 | BFS | DFS |
|------|-----|-----|
| データ構造 | キュー（FIFO） | スタック（LIFO）/ 再帰 |
| 探索順序 | 近い順（幅優先） | 深い順（深さ優先） |
| 最短経路 | 保証する | 保証しない |
| メモリ使用 | 多い（幅に比例） | 少ない（深さに比例） |
| 用途 | 最短経路、レベル順探索 | 全探索、バックトラッキング |

### この講義で学んだアルゴリズムの全体像

```
ソートアルゴリズム:
  O(n^2): 挿入ソート、バブルソート、選択ソート
  O(n log n): シェルソート（概算）、Python sorted()（Timsort）
  O(n+k): 分布数えソート、基数ソート

探索アルゴリズム:
  線形探索: O(n)
  二分探索: O(log n)
  BFS: O(V + E)  ※V:頂点数、E:辺数
  DFS: O(V + E)
```

**ポイント:**
- アルゴリズムの選択はデータの特性と目的に依存する
- 計算量を理解することで、プログラムの性能を予測できる
- BFS は最短経路が必要な場面で、DFS は全探索や深い探索が必要な場面で使う
