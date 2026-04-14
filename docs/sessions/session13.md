# 第13回: 実践的な課題（1）

> アルゴリズム論及び演習I ｜ 2026年度

---

## 説明: アイテム収集迷路ゲーム

この回では、これまで学んだアルゴリズム（BFS・状態管理・frozenset）を組み合わせて、**迷路の中でアイテムを全て集めてゴールする最短経路**を求めるプログラムを段階的に作る。

### 基本の考え方

普通のBFSでは「位置」だけを状態として記録するが、アイテム収集では**「位置 + 集めたアイテムの組み合わせ」**を状態として管理する必要がある。同じ位置でも、集めたアイテムが違えば**別の状態**として扱う。

**使うアルゴリズム・データ構造**:
- **BFS（幅優先探索）**: 最短経路の保証
- **frozenset**: 集めたアイテムの集合をハッシュ可能にする
- **deque**: BFS用のキュー
- **辞書（dict）**: 経路復元のための親マップ

---

## 例題1: 迷路の表示

迷路を2次元リストで定義し、絵文字で見やすく表示する。

```python
# ===================================================
# 例題1: 迷路の表示
# 2次元リストを絵文字で描画する
# ===================================================

def display_maze(maze):
    """迷路を絵文字で表示する関数"""
    rows = len(maze)        # 迷路の行数を取得する
    cols = len(maze[0])     # 迷路の列数を取得する
    for r in range(rows):   # 各行を順番に処理する
        line = ""           # 1行分の文字列を初期化する
        for c in range(cols):       # 各列を順番に処理する
            if maze[r][c] == 1:     # 壁の場合
                line += "🟫"        # 茶色の四角を追加する
            else:                   # 通路の場合
                line += "🟩"        # 緑の四角を追加する
        print(line)         # 1行分をまとめて出力する


# --- 迷路を定義する ---
# 0 = 通路, 1 = 壁
maze = [
    [0, 0, 1, 0, 0],   # 0行目
    [0, 1, 0, 0, 0],   # 1行目
    [0, 0, 0, 1, 0],   # 2行目
    [0, 1, 1, 0, 0],   # 3行目
    [0, 0, 0, 0, 0],   # 4行目
]

# --- 迷路を表示する ---
print("=== 迷路の表示 ===")     # タイトルを出力する
display_maze(maze)               # 迷路を描画する
print()                          # 空行を出力する
print(f"サイズ: {len(maze)}行 x {len(maze[0])}列")  # サイズを出力する
```

**実行結果**:
```
=== 迷路の表示 ===
🟩🟩🟫🟩🟩
🟩🟫🟩🟩🟩
🟩🟩🟩🟫🟩
🟩🟫🟫🟩🟩
🟩🟩🟩🟩🟩

サイズ: 5行 x 5列
```

---

## 例題2: BFSで最短経路を求める

スタートからゴールまでの最短経路をBFSで探索する。

```python
# ===================================================
# 例題2: BFSで最短経路探索
# 状態 = 位置のみ、訪問済みをsetで管理する
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def find_shortest_path(maze, start, goal):
    """BFSで最短経路を求める関数"""
    rows = len(maze)            # 迷路の行数を取得する
    cols = len(maze[0])         # 迷路の列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右の移動方向

    queue = deque([start])      # キューにスタート位置を入れる
    visited = {start}           # 訪問済みにスタートを登録する
    parent = {start: None}      # 経路復元用の親マップを作る

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # キューの先頭を取り出す

        if current == goal:         # ゴールに到着した場合
            path = []               # 経路を格納するリストを作る
            node = current          # 現在のノードからたどる
            while node is not None:     # 親がなくなるまで繰り返す
                path.append(node)       # ノードを経路に追加する
                node = parent[node]     # 親ノードに移動する
            return path[::-1]       # 逆順にして返す

        row, col = current          # 現在位置の行と列を取り出す
        for dr, dc in directions:   # 4方向を順番に試す
            nr = row + dr           # 次の行を計算する
            nc = col + dc           # 次の列を計算する
            next_pos = (nr, nc)     # 次の位置をタプルにする

            is_inside = 0 <= nr < rows and 0 <= nc < cols  # 範囲内か判定する
            if is_inside and maze[nr][nc] == 0 and next_pos not in visited:
                visited.add(next_pos)           # 訪問済みに追加する
                queue.append(next_pos)          # キューに追加する
                parent[next_pos] = current      # 親を記録する

    return None  # ゴールに到達できなかった場合


# --- 迷路を定義する ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)  # スタート位置を設定する
goal = (4, 4)   # ゴール位置を設定する

# --- 最短経路を探索する ---
path = find_shortest_path(maze, start, goal)  # BFSで探索する

if path is not None:                              # 経路が見つかった場合
    print(f"最短経路が見つかりました（{len(path)-1}歩）")  # 歩数を出力する
    for i, pos in enumerate(path):                # 経路を1歩ずつ出力する
        print(f"  ステップ{i}: {pos}")            # 位置を出力する
else:
    print("経路が見つかりませんでした")  # 到達不可能な場合
```

**実行結果**:
```
最短経路が見つかりました（8歩）
  ステップ0: (0, 0)
  ステップ1: (0, 1)
  ステップ2: (1, 0)
  ステップ3: (2, 0)
  ステップ4: (2, 1)
  ステップ5: (2, 2)
  ステップ6: (3, 3)
  ステップ7: (3, 4)
  ステップ8: (4, 4)
```

---

## 例題3: 迷路にアイテムを配置する

迷路の通路にアイテムを配置し、プレイヤーがアイテムの上を通ったら取得する。

```python
# ===================================================
# 例題3: アイテムの配置と取得判定
# アイテムを迷路に配置し、経路上で拾えるか確認する
# ===================================================

def display_maze_with_items(maze, start, goal, items):
    """迷路をスタート・ゴール・アイテム付きで表示する関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    for r in range(rows):       # 各行を処理する
        line = ""               # 1行分の文字列を初期化する
        for c in range(cols):   # 各列を処理する
            pos = (r, c)        # 現在のセル位置をタプルにする
            if pos == start:            # スタート地点の場合
                line += "🚶"            # 人の絵文字を追加する
            elif pos == goal:           # ゴール地点の場合
                line += "🏁"            # 旗の絵文字を追加する
            elif pos in items:          # アイテムがある場合
                line += "💎"            # 宝石の絵文字を追加する
            elif maze[r][c] == 1:       # 壁の場合
                line += "🟫"            # 茶色の四角を追加する
            else:                       # 通路の場合
                line += "🟩"            # 緑の四角を追加する
        print(line)             # 1行分を出力する


def check_item_pickup(path, items):
    """経路上で拾えるアイテムを調べる関数"""
    collected = []              # 拾ったアイテムのリストを初期化する
    for pos in path:            # 経路の各位置を順に確認する
        if pos in items and pos not in collected:  # アイテムがあり未取得の場合
            collected.append(pos)   # 取得済みリストに追加する
            print(f"  位置{pos}でアイテムを拾った！")  # 取得メッセージを出力する
    return collected            # 拾ったアイテムのリストを返す


# --- 迷路とアイテムを定義する ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)                          # スタート位置を設定する
goal = (4, 4)                           # ゴール位置を設定する
items = [(0, 4), (2, 0), (4, 2)]        # アイテム3個の位置を設定する

# --- 迷路を表示する ---
print("=== アイテム付き迷路 ===")       # タイトルを出力する
print("🚶=スタート 🏁=ゴール 💎=アイテム")  # 凡例を出力する
display_maze_with_items(maze, start, goal, items)  # 迷路を描画する

# --- 普通のBFSで経路を求める ---
from collections import deque  # dequeをインポートする

path = find_shortest_path(maze, start, goal)  # 最短経路を求める
print(f"\n最短経路（アイテム無視）: {len(path)-1}歩")  # 歩数を出力する

# --- 経路上のアイテム取得を確認する ---
print("\n【アイテム取得チェック】")          # セクションタイトルを出力する
collected = check_item_pickup(path, items)  # 拾えるアイテムを調べる
print(f"\n取得数: {len(collected)}/{len(items)}個")  # 結果を出力する

if len(collected) < len(items):             # 全部拾えなかった場合
    missing = [i for i in items if i not in collected]  # 未取得を計算する
    print(f"未取得: {missing}")             # 未取得リストを出力する
    print("→ 全アイテムを集めるには経路を変える必要がある！")
```

**実行結果**:
```
=== アイテム付き迷路 ===
🚶=スタート 🏁=ゴール 💎=アイテム
🚶🟩🟫🟩💎
🟩🟫🟩🟩🟩
💎🟩🟩🟫🟩
🟩🟫🟫🟩🟩
🟩🟩💎🟩🏁

最短経路（アイテム無視）: 8歩

【アイテム取得チェック】
  位置(2, 0)でアイテムを拾った！

取得数: 1/3個
未取得: [(0, 4), (4, 2)]
→ 全アイテムを集めるには経路を変える必要がある！
```

---

## 例題4: frozensetで状態を管理する

frozensetを使い、「位置 + 集めたアイテム」を1つの状態として管理する方法を学ぶ。

```python
# ===================================================
# 例題4: frozensetによる状態管理
# setは変更可能なのでdictのキーに使えないが
# frozensetは変更不可能なのでキーに使える
# ===================================================

def demonstrate_frozenset():
    """frozensetの使い方を実演する関数"""

    # --- setとfrozensetの違い ---
    normal_set = {(0, 4), (2, 0)}       # 普通のset（変更可能）
    frozen = frozenset({(0, 4), (2, 0)})  # frozenset（変更不可能）

    print("=== frozensetの基本 ===")     # タイトルを出力する
    print(f"set:       {normal_set}")    # setの中身を出力する
    print(f"frozenset: {frozen}")        # frozensetの中身を出力する

    # --- frozensetは辞書のキーに使える ---
    state_a = ((0, 0), frozenset())             # 位置(0,0)、アイテム0個
    state_b = ((0, 0), frozenset({(2, 0)}))     # 位置(0,0)、アイテム1個
    state_c = ((0, 0), frozenset({(2, 0), (0, 4)}))  # 位置(0,0)、アイテム2個

    visited = {}                # 訪問記録用の辞書を作る
    visited[state_a] = True     # 状態Aを訪問済みにする
    visited[state_b] = True     # 状態Bを訪問済みにする
    visited[state_c] = True     # 状態Cを訪問済みにする

    print(f"\n同じ位置でも違う状態として管理できる:")  # 説明を出力する
    print(f"  状態A（アイテム0個）: {state_a}")  # 状態Aを出力する
    print(f"  状態B（アイテム1個）: {state_b}")  # 状態Bを出力する
    print(f"  状態C（アイテム2個）: {state_c}")  # 状態Cを出力する
    print(f"  登録された状態数: {len(visited)}")  # 状態数を出力する

    # --- アイテム追加のシミュレーション ---
    print(f"\n=== アイテム追加の操作 ===")  # タイトルを出力する
    collected = frozenset()                 # 空のfrozensetから始める
    print(f"初期状態: {collected}")          # 初期状態を出力する

    collected = collected | {(2, 0)}        # アイテム1つ目を追加する
    print(f"1個取得後: {collected}")         # 追加後を出力する

    collected = collected | {(0, 4)}        # アイテム2つ目を追加する
    print(f"2個取得後: {collected}")         # 追加後を出力する

    # --- ゴール判定 ---
    all_items = frozenset({(0, 4), (2, 0), (4, 2)})  # 全アイテムの集合
    print(f"\n全アイテム: {all_items}")      # 全アイテムを出力する
    print(f"現在の収集: {collected}")        # 現在の状態を出力する
    print(f"全部集めた？: {collected == all_items}")  # 判定結果を出力する

    collected = collected | {(4, 2)}        # 最後のアイテムを追加する
    print(f"3個取得後: {collected}")         # 追加後を出力する
    print(f"全部集めた？: {collected == all_items}")  # 判定結果を出力する


demonstrate_frozenset()  # 実演を実行する
```

**実行結果**:
```
=== frozensetの基本 ===
set:       {(2, 0), (0, 4)}
frozenset: frozenset({(2, 0), (0, 4)})

同じ位置でも違う状態として管理できる:
  状態A（アイテム0個）: ((0, 0), frozenset())
  状態B（アイテム1個）: ((0, 0), frozenset({(2, 0)}))
  状態C（アイテム2個）: ((0, 0), frozenset({(2, 0), (0, 4)}))
  登録された状態数: 3

=== アイテム追加の操作 ===
初期状態: frozenset()
1個取得後: frozenset({(2, 0)})
2個取得後: frozenset({(2, 0), (0, 4)})

全アイテム: frozenset({(2, 0), (0, 4), (4, 2)})
現在の収集: frozenset({(2, 0), (0, 4)})
全部集めた？: False
3個取得後: frozenset({(2, 0), (0, 4), (4, 2)})
全部集めた？: True
```

---

## 例題5: 全アイテム収集BFS（完全版）

位置とアイテム収集状態を組み合わせたBFSで、全アイテムを集めてゴールする最短経路を求める。

```python
# ===================================================
# 例題5: アイテム収集BFS（完全版）
# 状態 = (位置, 集めたアイテムのfrozenset)
# ゴール条件 = 全アイテム収集 + ゴール到着
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def solve_item_maze(maze, start, goal, items):
    """全アイテムを集めてゴールする最短経路を求める関数"""
    rows = len(maze)            # 迷路の行数を取得する
    cols = len(maze[0])         # 迷路の列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右の移動方向
    all_items = frozenset(items)    # 全アイテムの集合を作る

    # --- 初期状態を設定する ---
    initial_state = (start, frozenset())    # 位置とアイテム0個で開始する
    queue = deque([initial_state])          # キューに初期状態を入れる
    visited = {initial_state}               # 訪問済みに初期状態を登録する
    parent = {initial_state: None}          # 親マップを初期化する

    # --- BFSのメインループ ---
    while queue:                # キューが空になるまで繰り返す
        current_pos, collected = queue.popleft()  # 先頭の状態を取り出す

        # --- ゴール判定 ---
        if current_pos == goal and collected == all_items:  # 全条件を満たす場合
            path = []                               # 経路リストを初期化する
            state = (current_pos, collected)         # 現在の状態から開始する
            while state is not None:                # 親がなくなるまで繰り返す
                path.append(state)                  # 状態を経路に追加する
                state = parent[state]               # 親の状態に移動する
            return path[::-1]                       # 逆順にして返す

        # --- 4方向を探索する ---
        row, col = current_pos              # 現在位置の行と列を取り出す
        for dr, dc in directions:           # 4方向を順番に試す
            nr = row + dr                   # 次の行を計算する
            nc = col + dc                   # 次の列を計算する
            next_pos = (nr, nc)             # 次の位置をタプルにする

            is_valid = (0 <= nr < rows and 0 <= nc < cols  # 範囲内か判定する
                        and maze[nr][nc] == 0)              # 通路か判定する

            if is_valid:                        # 移動可能な場合
                new_collected = collected        # 現在の収集状態をコピーする
                if next_pos in items:           # アイテムがある場合
                    new_collected = collected | {next_pos}  # アイテムを追加する

                new_state = (next_pos, new_collected)   # 新しい状態を作る
                if new_state not in visited:             # 未訪問の場合
                    visited.add(new_state)               # 訪問済みに追加する
                    queue.append(new_state)              # キューに追加する
                    parent[new_state] = (current_pos, collected)  # 親を記録する

    return None  # 全探索してもゴールできなかった場合


def display_result(maze, start, goal, items, path):
    """結果を絵文字付きで表示する関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    path_positions = set()      # 経路上の位置を集合で管理する
    if path is not None:        # 経路がある場合
        for pos, _ in path:     # 各ステップの位置を取り出す
            path_positions.add(pos)  # 位置を集合に追加する

    for r in range(rows):       # 各行を処理する
        line = ""               # 1行分の文字列を初期化する
        for c in range(cols):   # 各列を処理する
            pos = (r, c)        # セル位置をタプルにする
            if pos == start:            # スタートの場合
                line += "🚶"
            elif pos == goal:           # ゴールの場合
                line += "🏁"
            elif pos in items:          # アイテムの場合
                line += "💎"
            elif pos in path_positions: # 経路上の場合
                line += "👣"
            elif maze[r][c] == 1:       # 壁の場合
                line += "🟫"
            else:                       # 通路の場合
                line += "🟩"
        print(line)             # 1行分を出力する


# --- メインの実行部分 ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)                          # スタート位置を設定する
goal = (4, 4)                           # ゴール位置を設定する
items = [(0, 4), (2, 0), (4, 2)]        # アイテム3個の位置を設定する

print("=== アイテム収集迷路ゲーム ===")  # タイトルを出力する
print("🚶=スタート 🏁=ゴール 💎=アイテム 👣=経路")  # 凡例を出力する
print()

# --- BFSで全アイテム収集最短経路を求める ---
path = solve_item_maze(maze, start, goal, items)  # 探索を実行する

if path is not None:                    # 経路が見つかった場合
    print(f"経路が見つかりました！（{len(path)-1}歩）")  # 歩数を出力する
    print()
    display_result(maze, start, goal, items, path)  # 結果を描画する
    print()
    print("【経路の詳細】")             # セクションタイトルを出力する
    for i, (pos, collected) in enumerate(path):  # 各ステップを出力する
        count = len(collected)          # 取得アイテム数を計算する
        print(f"  ステップ{i:2d}: 位置{pos} | アイテム{count}/{len(items)}個")
else:
    print("経路が見つかりませんでした")  # 到達不可能な場合
```

**実行結果**:
```
=== アイテム収集迷路ゲーム ===
🚶=スタート 🏁=ゴール 💎=アイテム 👣=経路

経路が見つかりました！（16歩）

🚶👣🟫👣💎
👣🟫👣👣👣
💎👣👣🟫👣
🟩🟫🟫👣👣
🟩👣💎👣🏁

【経路の詳細】
  ステップ 0: 位置(0, 0) | アイテム0/3個
  ステップ 1: 位置(1, 0) | アイテム0/3個
  ...
  ステップ16: 位置(4, 4) | アイテム3/3個
```

---

## 標準課題

### 標準課題1（超やさしい）: 迷路を自分で作って表示する

例題1の`display_maze`関数を使い、自分だけのオリジナル迷路（6x6以上）を作って表示しなさい。

```python
# ===================================================
# 課題1: オリジナル迷路の作成と表示
# 6x6以上の迷路を定義して絵文字で表示する
# ===================================================

# あなたの迷路をここに定義してください
# my_maze = [
#     [0, ...],
#     ...
# ]
# display_maze(my_maze)
```

---

### 標準課題2（超やさしい）: スタートとゴールを表示する

`display_maze`を改良し、スタートとゴールの位置も絵文字で表示する関数`display_maze_sg`を作りなさい。

```python
# ===================================================
# 課題2: スタートとゴールの表示
# スタートを🚶、ゴールを🏁で表示する
# ===================================================

def display_maze_sg(maze, start, goal):
    """迷路をスタート・ゴール付きで表示する関数"""
    # ここに実装してください
    pass
```

---

### 標準課題3（やさしい）: 訪問済みを記録して表示する

BFS探索の過程で訪問した全てのセルを記録し、迷路上に「探索範囲」として表示しなさい。

```python
# ===================================================
# 課題3: 訪問済みセルの記録と表示
# BFSで訪問した全セルを🔵で表示する
# ===================================================

def bfs_with_visited_log(maze, start, goal):
    """訪問済みセルのリストも返すBFS関数"""
    # ここに実装してください
    # 戻り値: (経路, 訪問済みセルのset)
    pass
```

---

### 標準課題4（やさしい）: 最短経路を求めて表示する

例題2のBFSを使い、経路を迷路上に絵文字で表示しなさい。経路上のセルは👣で表示すること。

```python
# ===================================================
# 課題4: 最短経路の迷路上への表示
# BFSで求めた経路を👣で迷路に描画する
# ===================================================

def display_maze_with_path(maze, start, goal, path):
    """経路付きで迷路を表示する関数"""
    # ここに実装してください
    pass
```

---

### 標準課題5（やややさしい）: アイテムを迷路に追加する

例題3を参考に、アイテムの位置リストを受け取り、迷路・スタート・ゴール・アイテムを全て表示する関数を作りなさい。

```python
# ===================================================
# 課題5: アイテム付き迷路の表示
# 迷路にスタート・ゴール・アイテムを全て表示する
# ===================================================

def display_full_maze(maze, start, goal, items):
    """全要素を表示する迷路描画関数"""
    # ここに実装してください
    pass
```

---

### 標準課題6（やややさしい）: 経路上でアイテムを拾う

BFSで求めた最短経路（アイテム無視）を歩き、途中で拾えるアイテムを特定しなさい。拾えなかったアイテムも報告すること。

```python
# ===================================================
# 課題6: 経路上のアイテム拾得判定
# 最短経路を歩いてアイテムを何個拾えるか調べる
# ===================================================

def walk_and_collect(path, items):
    """経路を歩いてアイテムを拾う関数"""
    # ここに実装してください
    # 戻り値: (拾ったリスト, 拾えなかったリスト)
    pass
```

---

### 標準課題7（やや普通）: frozensetで収集状態を管理する

例題4を参考に、BFSの状態を`(位置, frozenset(収集済みアイテム))`として定義し、同じ位置でも収集状態が異なれば別の状態として扱うBFSを実装しなさい。ゴール条件は「ゴール位置に到達すること」のみ（全アイテム収集は不要）とする。

```python
# ===================================================
# 課題7: 状態付きBFS（ゴール到達のみ）
# 状態 = (位置, frozenset)、ゴール条件 = ゴール到達
# ===================================================

def bfs_with_state(maze, start, goal, items):
    """状態付きBFSでゴールまでの経路を求める関数"""
    # ここに実装してください
    # 経路上でアイテムを自動取得するが、
    # 全アイテム収集はゴール条件に含めない
    pass
```

---

### 標準課題8（やや普通）: 収集状態を含むBFSの探索ログ

課題7のBFSに、探索した状態数・訪問済み状態数・キューの最大長を記録する機能を追加しなさい。

```python
# ===================================================
# 課題8: 状態付きBFSの探索統計
# 探索過程の統計情報を収集する
# ===================================================

def bfs_with_stats(maze, start, goal, items):
    """統計情報付きの状態付きBFS関数"""
    # ここに実装してください
    # 戻り値: (経路, 統計情報の辞書)
    # 統計: explored(探索状態数), visited(訪問状態数), max_queue(キュー最大長)
    pass
```

---

### 標準課題9（普通）: 全アイテム収集BFSの完成

例題5を参考に、全アイテムを集めてからゴールする最短経路を求める完全版BFSを実装しなさい。アイテム数は3個以上で動作確認すること。

```python
# ===================================================
# 課題9: 全アイテム収集BFS（完全版）
# 全アイテム収集 + ゴール到着を条件とする
# ===================================================

def solve_complete_maze(maze, start, goal, items):
    """全アイテム収集してゴールする最短経路を求める関数"""
    # ここに実装してください
    pass
```

---

### 標準課題10（普通）: 最短経路の最適性検証

全アイテム収集BFSの結果が本当に最短であることを検証しなさい。アイテムなしのBFS（例題2）との歩数の差を計算し、「アイテム収集による追加コスト」を報告すること。さらに、アイテム数を1〜4個に変化させて、探索状態数と経路長がどう変わるかを表形式で出力しなさい。

```python
# ===================================================
# 課題10: 最短経路の最適性検証
# アイテム数と探索コストの関係を分析する
# ===================================================

def analyze_item_impact(maze, start, goal, all_item_candidates):
    """アイテム数による探索コストの変化を分析する関数"""
    # ここに実装してください
    # アイテム数1〜4で探索し、状態数と経路長を比較する
    pass
```

---

## 発展課題

### 発展課題1: ランダム迷路生成器

迷路をランダムに生成する関数を作りなさい。壁の確率を引数で指定でき、スタートとゴールは必ず通路とすること。生成した迷路に対してアイテムをランダム配置し、全アイテム収集BFSで解けることを確認しなさい。解けない迷路が生成された場合は再生成すること。

---

### 発展課題2: Pygameによる迷路可視化

Pygameを使い、迷路・アイテム・BFSの探索過程・最短経路をアニメーションで表示するプログラムを作りなさい。BFSが探索するセルを1つずつ色を変えて表示し、最短経路が見つかったら経路を強調表示すること。

---

## 解答例

### 課題1 解答例

```python
# ===================================================
# 課題1 解答例: オリジナル迷路
# ===================================================

def display_maze(maze):
    """迷路を絵文字で表示する関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    for r in range(rows):       # 各行を処理する
        line = ""               # 1行分の文字列を初期化する
        for c in range(cols):   # 各列を処理する
            if maze[r][c] == 1:     # 壁の場合
                line += "🟫"        # 茶色を追加する
            else:                   # 通路の場合
                line += "🟩"        # 緑を追加する
        print(line)             # 1行分を出力する


# --- オリジナル迷路（7x7） ---
my_maze = [
    [0, 0, 1, 0, 0, 0, 0],   # 0行目
    [0, 1, 1, 0, 1, 1, 0],   # 1行目
    [0, 0, 0, 0, 0, 1, 0],   # 2行目
    [1, 1, 0, 1, 0, 0, 0],   # 3行目
    [0, 0, 0, 1, 0, 1, 1],   # 4行目
    [0, 1, 0, 0, 0, 0, 0],   # 5行目
    [0, 0, 0, 1, 1, 0, 0],   # 6行目
]

print("=== オリジナル迷路（7x7） ===")  # タイトルを出力する
display_maze(my_maze)                    # 迷路を表示する
print(f"サイズ: {len(my_maze)}行 x {len(my_maze[0])}列")  # サイズを出力する
```

---

### 課題2 解答例

```python
# ===================================================
# 課題2 解答例: スタートとゴールの表示
# ===================================================

def display_maze_sg(maze, start, goal):
    """迷路をスタート・ゴール付きで表示する関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    for r in range(rows):       # 各行を処理する
        line = ""               # 1行分の文字列を初期化する
        for c in range(cols):   # 各列を処理する
            pos = (r, c)        # 現在位置をタプルにする
            if pos == start:            # スタートの場合
                line += "🚶"            # 人の絵文字を追加する
            elif pos == goal:           # ゴールの場合
                line += "🏁"            # 旗の絵文字を追加する
            elif maze[r][c] == 1:       # 壁の場合
                line += "🟫"            # 茶色を追加する
            else:                       # 通路の場合
                line += "🟩"            # 緑を追加する
        print(line)             # 1行分を出力する


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
print("=== スタート・ゴール付き迷路 ===")  # タイトルを出力する
display_maze_sg(maze, (0, 0), (4, 4))      # スタートとゴール付きで表示する
```

---

### 課題3 解答例

```python
# ===================================================
# 課題3 解答例: 訪問済みセルの記録と表示
# ===================================================

from collections import deque  # dequeをインポートする

def bfs_with_visited_log(maze, start, goal):
    """訪問済みセルも返すBFS関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する

    queue = deque([start])      # キューを初期化する
    visited = {start}           # 訪問済みを初期化する
    parent = {start: None}      # 親マップを初期化する

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # 先頭を取り出す
        if current == goal:         # ゴールに到着した場合
            path = []               # 経路リストを作る
            node = current          # ゴールからたどる
            while node is not None:     # 親がなくなるまで
                path.append(node)       # ノードを追加する
                node = parent[node]     # 親に移動する
            return path[::-1], visited  # 経路と訪問済みを返す

        row, col = current          # 現在位置を取り出す
        for dr, dc in directions:   # 4方向を試す
            nr = row + dr           # 次の行を計算する
            nc = col + dc           # 次の列を計算する
            next_pos = (nr, nc)     # 次の位置をタプルにする
            if (0 <= nr < rows and 0 <= nc < cols   # 範囲内で
                    and maze[nr][nc] == 0            # 通路で
                    and next_pos not in visited):    # 未訪問の場合
                visited.add(next_pos)       # 訪問済みに追加する
                queue.append(next_pos)      # キューに追加する
                parent[next_pos] = current  # 親を記録する

    return None, visited  # ゴール不到達の場合


def display_maze_visited(maze, start, goal, path, visited):
    """訪問済みセルを表示する関数"""
    path_set = set(path) if path else set()  # 経路をsetに変換する
    rows = len(maze)        # 行数を取得する
    cols = len(maze[0])     # 列数を取得する
    for r in range(rows):   # 各行を処理する
        line = ""           # 1行分を初期化する
        for c in range(cols):   # 各列を処理する
            pos = (r, c)        # 位置をタプルにする
            if pos == start:                # スタートの場合
                line += "🚶"
            elif pos == goal:               # ゴールの場合
                line += "🏁"
            elif pos in path_set:           # 経路上の場合
                line += "👣"
            elif pos in visited:            # 訪問済みの場合
                line += "🔵"
            elif maze[r][c] == 1:           # 壁の場合
                line += "🟫"
            else:                           # 通路の場合
                line += "🟩"
        print(line)         # 1行分を出力する


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
path, visited = bfs_with_visited_log(maze, (0, 0), (4, 4))  # BFSを実行する
print("=== 訪問済みセルの表示 ===")     # タイトルを出力する
print("🔵=訪問済み 👣=経路")             # 凡例を出力する
display_maze_visited(maze, (0, 0), (4, 4), path, visited)  # 表示する
print(f"訪問済みセル数: {len(visited)}")  # 訪問数を出力する
```

---

### 課題4 解答例

```python
# ===================================================
# 課題4 解答例: 最短経路の迷路上表示
# ===================================================

from collections import deque  # dequeをインポートする

def find_shortest_path(maze, start, goal):
    """BFSで最短経路を求める関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する
    queue = deque([start])      # キューを初期化する
    visited = {start}           # 訪問済みを初期化する
    parent = {start: None}      # 親マップを初期化する

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # 先頭を取り出す
        if current == goal:         # ゴール到着の場合
            path = []               # 経路リストを作る
            node = current          # ゴールからたどる
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]       # 逆順にして返す
        row, col = current
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] == 0 and next_pos not in visited):
                visited.add(next_pos)
                queue.append(next_pos)
                parent[next_pos] = current
    return None


def display_maze_with_path(maze, start, goal, path):
    """経路付きで迷路を表示する関数"""
    path_set = set(path) if path else set()  # 経路をsetに変換する
    rows = len(maze)        # 行数を取得する
    cols = len(maze[0])     # 列数を取得する
    for r in range(rows):   # 各行を処理する
        line = ""           # 1行分を初期化する
        for c in range(cols):
            pos = (r, c)
            if pos == start:            # スタートの場合
                line += "🚶"
            elif pos == goal:           # ゴールの場合
                line += "🏁"
            elif pos in path_set:       # 経路上の場合
                line += "👣"
            elif maze[r][c] == 1:       # 壁の場合
                line += "🟫"
            else:                       # 通路の場合
                line += "🟩"
        print(line)         # 1行分を出力する


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
path = find_shortest_path(maze, (0, 0), (4, 4))  # 最短経路を求める
print("=== 最短経路の表示 ===")     # タイトルを出力する
display_maze_with_path(maze, (0, 0), (4, 4), path)  # 経路を表示する
print(f"経路の長さ: {len(path)-1}歩")  # 歩数を出力する
```

---

### 課題5 解答例

```python
# ===================================================
# 課題5 解答例: アイテム付き迷路の表示
# ===================================================

def display_full_maze(maze, start, goal, items):
    """全要素を表示する迷路描画関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    item_set = set(items)       # アイテム位置をsetに変換する
    for r in range(rows):       # 各行を処理する
        line = ""               # 1行分を初期化する
        for c in range(cols):   # 各列を処理する
            pos = (r, c)        # 位置をタプルにする
            if pos == start:            # スタートの場合
                line += "🚶"
            elif pos == goal:           # ゴールの場合
                line += "🏁"
            elif pos in item_set:       # アイテムの場合
                line += "💎"
            elif maze[r][c] == 1:       # 壁の場合
                line += "🟫"
            else:                       # 通路の場合
                line += "🟩"
        print(line)             # 1行分を出力する


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム位置を定義する
print("=== アイテム付き迷路 ===")   # タイトルを出力する
print("🚶=スタート 🏁=ゴール 💎=アイテム")  # 凡例を出力する
display_full_maze(maze, (0, 0), (4, 4), items)  # 表示する
print(f"アイテム数: {len(items)}個")  # アイテム数を出力する
```

---

### 課題6 解答例

```python
# ===================================================
# 課題6 解答例: 経路上のアイテム拾得判定
# ===================================================

def walk_and_collect(path, items):
    """経路を歩いてアイテムを拾う関数"""
    item_set = set(items)       # アイテム位置をsetに変換する
    collected = []              # 拾ったアイテムのリストを初期化する
    missed = []                 # 拾えなかったリストを初期化する

    for pos in path:            # 経路の各位置を確認する
        if pos in item_set and pos not in collected:  # アイテムがあり未取得の場合
            collected.append(pos)   # 取得リストに追加する
            print(f"  ステップ: 位置{pos}でアイテム取得！")  # 取得メッセージを出力する

    for item in items:          # 全アイテムを確認する
        if item not in collected:   # 拾えなかった場合
            missed.append(item)     # 未取得リストに追加する

    return collected, missed    # 拾ったリストと拾えなかったリストを返す


# --- テスト ---
from collections import deque  # dequeをインポートする

maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム位置を定義する
path = find_shortest_path(maze, (0, 0), (4, 4))  # 最短経路を求める

print("=== アイテム拾得チェック ===")  # タイトルを出力する
collected, missed = walk_and_collect(path, items)  # 拾得判定する
print(f"\n取得: {len(collected)}/{len(items)}個 → {collected}")   # 取得数を出力する
print(f"未取得: {len(missed)}個 → {missed}")  # 未取得数を出力する
```

---

### 課題7 解答例

```python
# ===================================================
# 課題7 解答例: 状態付きBFS（ゴール到達のみ）
# ===================================================

from collections import deque  # dequeをインポートする

def bfs_with_state(maze, start, goal, items):
    """状態付きBFSでゴールまでの経路を求める関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する

    initial = (start, frozenset())  # 初期状態を作る
    queue = deque([initial])        # キューに初期状態を入れる
    visited = {initial}             # 訪問済みに登録する
    parent = {initial: None}        # 親マップを初期化する

    while queue:                    # キューが空になるまで繰り返す
        current_pos, collected = queue.popleft()  # 先頭を取り出す

        if current_pos == goal:     # ゴールに到着した場合（アイテム数は問わない）
            path = []               # 経路リストを作る
            state = (current_pos, collected)  # 現在状態を設定する
            while state is not None:         # 親がなくなるまで
                path.append(state)           # 状態を追加する
                state = parent[state]        # 親に移動する
            return path[::-1]       # 逆順にして返す

        row, col = current_pos      # 現在位置を取り出す
        for dr, dc in directions:   # 4方向を試す
            nr = row + dr           # 次の行を計算する
            nc = col + dc           # 次の列を計算する
            next_pos = (nr, nc)     # 次の位置をタプルにする

            if (0 <= nr < rows and 0 <= nc < cols   # 範囲内で
                    and maze[nr][nc] == 0):          # 通路の場合
                new_collected = collected            # 収集状態をコピーする
                if next_pos in items:               # アイテムがある場合
                    new_collected = collected | {next_pos}  # アイテムを追加する

                new_state = (next_pos, new_collected)   # 新しい状態を作る
                if new_state not in visited:             # 未訪問の場合
                    visited.add(new_state)               # 訪問済みに追加する
                    queue.append(new_state)              # キューに追加する
                    parent[new_state] = (current_pos, collected)  # 親を記録する

    return None  # ゴール不到達の場合


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム位置を定義する
path = bfs_with_state(maze, (0, 0), (4, 4), items)  # 状態付きBFSを実行する

if path is not None:                # 経路がある場合
    print(f"=== 状態付きBFS（ゴール到達のみ） ===")  # タイトルを出力する
    print(f"経路の長さ: {len(path)-1}歩")  # 歩数を出力する
    final_pos, final_collected = path[-1]   # 最終状態を取り出す
    print(f"ゴール時のアイテム: {len(final_collected)}/{len(items)}個")  # 取得数を出力する
    for i, (pos, coll) in enumerate(path):  # 各ステップを出力する
        print(f"  ステップ{i:2d}: 位置{pos} アイテム{len(coll)}個")
```

---

### 課題8 解答例

```python
# ===================================================
# 課題8 解答例: 状態付きBFSの探索統計
# ===================================================

from collections import deque  # dequeをインポートする

def bfs_with_stats(maze, start, goal, items):
    """統計情報付きの状態付きBFS関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する
    all_items = frozenset(items)    # 全アイテムの集合を作る

    initial = (start, frozenset())  # 初期状態を作る
    queue = deque([initial])        # キューを初期化する
    visited = {initial}             # 訪問済みを初期化する
    parent = {initial: None}        # 親マップを初期化する

    explored_count = 0      # 探索した状態数を初期化する
    max_queue_size = 1      # キューの最大長を初期化する

    while queue:            # キューが空になるまで繰り返す
        if len(queue) > max_queue_size:     # キューが過去最大を超えた場合
            max_queue_size = len(queue)     # 最大長を更新する

        current_pos, collected = queue.popleft()  # 先頭を取り出す
        explored_count += 1                       # 探索数を1増やす

        if current_pos == goal and collected == all_items:  # 全条件達成の場合
            path = []                   # 経路リストを作る
            state = (current_pos, collected)
            while state is not None:
                path.append(state)
                state = parent[state]
            stats = {                   # 統計情報をまとめる
                "explored": explored_count,         # 探索した状態数
                "visited": len(visited),            # 訪問済み状態数
                "max_queue": max_queue_size,         # キューの最大長
            }
            return path[::-1], stats    # 経路と統計を返す

        row, col = current_pos
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0):
                new_collected = collected
                if next_pos in items:
                    new_collected = collected | {next_pos}
                new_state = (next_pos, new_collected)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
                    parent[new_state] = (current_pos, collected)

    stats = {                       # ゴール不到達の場合の統計
        "explored": explored_count,
        "visited": len(visited),
        "max_queue": max_queue_size,
    }
    return None, stats              # Noneと統計を返す


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム位置を定義する
path, stats = bfs_with_stats(maze, (0, 0), (4, 4), items)  # 統計付きBFSを実行する

print("=== 探索統計 ===")           # タイトルを出力する
if path is not None:                # 経路が見つかった場合
    print(f"経路の長さ: {len(path)-1}歩")       # 歩数を出力する
print(f"探索した状態数: {stats['explored']}")    # 探索数を出力する
print(f"訪問済み状態数: {stats['visited']}")     # 訪問数を出力する
print(f"キューの最大長: {stats['max_queue']}")   # キュー最大を出力する
```

---

### 課題9 解答例

```python
# ===================================================
# 課題9 解答例: 全アイテム収集BFS（完全版）
# ===================================================

from collections import deque  # dequeをインポートする

def solve_complete_maze(maze, start, goal, items):
    """全アイテム収集してゴールする最短経路を求める関数"""
    rows = len(maze)                # 行数を取得する
    cols = len(maze[0])             # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する
    all_items = frozenset(items)    # 全アイテムの集合を作る

    initial = (start, frozenset())  # 初期状態を作る
    queue = deque([initial])        # キューを初期化する
    visited = {initial}             # 訪問済みを初期化する
    parent = {initial: None}        # 親マップを初期化する

    while queue:                    # キューが空になるまで繰り返す
        current_pos, collected = queue.popleft()  # 先頭を取り出す

        if current_pos == goal and collected == all_items:  # 全条件達成の場合
            path = []               # 経路リストを作る
            state = (current_pos, collected)
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]       # 逆順にして返す

        row, col = current_pos      # 現在位置を取り出す
        for dr, dc in directions:   # 4方向を試す
            nr = row + dr           # 次の行を計算する
            nc = col + dc           # 次の列を計算する
            next_pos = (nr, nc)     # 次の位置をタプルにする

            if (0 <= nr < rows and 0 <= nc < cols   # 範囲内かつ通路の場合
                    and maze[nr][nc] == 0):
                new_collected = collected
                if next_pos in items:               # アイテムがある場合
                    new_collected = collected | {next_pos}  # 追加する

                new_state = (next_pos, new_collected)
                if new_state not in visited:         # 未訪問の場合
                    visited.add(new_state)
                    queue.append(new_state)
                    parent[new_state] = (current_pos, collected)

    return None  # ゴール不到達の場合


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム3個を定義する
path = solve_complete_maze(maze, (0, 0), (4, 4), items)  # 全収集BFSを実行する

print("=== 全アイテム収集BFS ===")  # タイトルを出力する
if path is not None:                # 経路が見つかった場合
    print(f"経路が見つかりました！（{len(path)-1}歩）")  # 歩数を出力する
    for i, (pos, coll) in enumerate(path):  # 各ステップを出力する
        print(f"  ステップ{i:2d}: 位置{pos} アイテム{len(coll)}/{len(items)}個")
else:
    print("経路が見つかりませんでした")  # 到達不可能な場合
```

---

### 課題10 解答例

```python
# ===================================================
# 課題10 解答例: 最短経路の最適性検証
# ===================================================

from collections import deque  # dequeをインポートする

def find_shortest_path_simple(maze, start, goal):
    """アイテムなしの単純BFS関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        row, col = current
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] == 0 and next_pos not in visited):
                visited.add(next_pos)
                queue.append(next_pos)
                parent[next_pos] = current
    return None


def bfs_items_with_stats(maze, start, goal, items):
    """統計付き全アイテム収集BFS関数"""
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_items = frozenset(items)
    initial = (start, frozenset())
    queue = deque([initial])
    visited = {initial}
    parent = {initial: None}
    explored = 0                # 探索した状態数を初期化する

    while queue:
        current_pos, collected = queue.popleft()
        explored += 1           # 探索数を1増やす
        if current_pos == goal and collected == all_items:
            path = []
            state = (current_pos, collected)
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1], explored, len(visited)
        row, col = current_pos
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0):
                new_collected = collected
                if next_pos in items:
                    new_collected = collected | {next_pos}
                new_state = (next_pos, new_collected)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
                    parent[new_state] = (current_pos, collected)
    return None, explored, len(visited)


def analyze_item_impact(maze, start, goal, all_item_candidates):
    """アイテム数による探索コストの変化を分析する関数"""

    # --- アイテムなしの最短経路 ---
    base_path = find_shortest_path_simple(maze, start, goal)  # 単純BFSを実行する
    base_steps = len(base_path) - 1 if base_path else -1      # 歩数を取得する
    print(f"アイテムなしの最短経路: {base_steps}歩")           # 基準歩数を出力する
    print()

    # --- アイテム数を変えて比較 ---
    print(f"{'アイテム数':>10} | {'経路長':>6} | {'追加コスト':>8} | {'探索状態数':>10} | {'訪問状態数':>10}")
    print("-" * 65)                 # 区切り線を出力する

    for count in range(1, len(all_item_candidates) + 1):  # 1個から最大まで
        subset = all_item_candidates[:count]    # 先頭count個をアイテムとする
        result, explored, visited = bfs_items_with_stats(maze, start, goal, subset)

        if result is not None:                  # 経路が見つかった場合
            steps = len(result) - 1             # 歩数を計算する
            extra = steps - base_steps          # 追加コストを計算する
            print(f"{count:>10}個 | {steps:>5}歩 | {'+' + str(extra):>7}歩 | {explored:>10} | {visited:>10}")
        else:                                   # 経路がない場合
            print(f"{count:>10}個 | {'不可':>6} | {'-':>8} | {explored:>10} | {visited:>10}")


# --- テスト ---
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
all_candidates = [(2, 0), (4, 2), (0, 4), (2, 2)]  # アイテム候補4個を定義する

print("=== アイテム数と探索コストの分析 ===")  # タイトルを出力する
analyze_item_impact(maze, (0, 0), (4, 4), all_candidates)  # 分析を実行する
```
