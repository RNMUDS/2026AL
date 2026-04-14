# 第14回: 実践的な課題（2）

> アルゴリズム論及び演習I ｜ 2026年度

---

## 説明: コードレビューとは

コードレビューとは、**他の人が書いたコードを読んで改善点を見つける作業**のこと。プロのソフトウェア開発では、ほぼ全てのコードがレビューを経てから本番環境に反映される。

### レビューの4つの観点

1. **正しさ（Correctness）**: コードは正しく動作するか？ 境界値やエラーケースは？
2. **可読性（Readability）**: 変数名は分かりやすいか？ コメントは適切か？ 関数は短いか？
3. **効率性（Efficiency）**: 無駄なループはないか？ 適切なデータ構造を使っているか？
4. **拡張性（Extensibility）**: マジックナンバーはないか？ 関数は1つの役割に集中しているか？

---

## 例題1: バグのあるコードを見つける

正しさの観点から、バグのあるコードを読んで問題点を特定する。

```python
# ===================================================
# 例題1: バグのあるコードを見つける
# 以下のコードにはバグがある。問題点を特定して修正する
# ===================================================

# --- バグのあるコード ---
def find_max_buggy(numbers):
    """リストの最大値を返す関数（バグあり）"""
    maximum = numbers[0]        # 先頭の要素を初期値にする（空リストでエラー！）
    for i in range(len(numbers)):   # 全要素をループする
        if numbers[i] > maximum:    # 現在の最大値より大きい場合
            maximum = numbers[i]    # 最大値を更新する
    return maximum              # 最大値を返す


def find_average_buggy(numbers):
    """リストの平均値を返す関数（バグあり）"""
    total = 0                   # 合計を初期化する
    for num in numbers:         # 各要素をループする
        total += num            # 合計に加算する
    average = total / len(numbers)  # 平均を計算する（空リストでゼロ除算！）
    return average              # 平均を返す


# --- 修正版 ---
def find_max_fixed(numbers):
    """リストの最大値を返す関数（修正版）"""
    if not numbers:             # 空リストの場合をチェックする
        print("警告: 空のリストです")  # 警告メッセージを出力する
        return None             # Noneを返す
    maximum = numbers[0]        # 先頭の要素を初期値にする
    for i in range(1, len(numbers)):  # 2番目の要素からループする
        if numbers[i] > maximum:      # 現在の最大値より大きい場合
            maximum = numbers[i]      # 最大値を更新する
    return maximum              # 最大値を返す


def find_average_fixed(numbers):
    """リストの平均値を返す関数（修正版）"""
    if not numbers:             # 空リストの場合をチェックする
        print("警告: 空のリストです")  # 警告メッセージを出力する
        return None             # Noneを返す
    total = 0                   # 合計を初期化する
    for num in numbers:         # 各要素をループする
        total += num            # 合計に加算する
    average = total / len(numbers)  # 平均を計算する
    return average              # 平均を返す


# --- テスト ---
print("=== バグの発見と修正 ===")       # タイトルを出力する
test_cases = [                          # テストケースを定義する
    [3, 1, 4, 1, 5, 9, 2, 6],          # 通常のケース
    [42],                               # 1要素のケース
    [-3, -1, -4, -1, -5],              # 負の数のケース
    [],                                 # 空リストのケース
]

for data in test_cases:                 # 各テストケースを実行する
    print(f"\n入力: {data}")            # 入力データを出力する
    result_max = find_max_fixed(data)   # 最大値を求める
    result_avg = find_average_fixed(data)  # 平均値を求める
    print(f"  最大値: {result_max}")    # 最大値を出力する
    print(f"  平均値: {result_avg}")    # 平均値を出力する
```

**実行結果**:
```
=== バグの発見と修正 ===

入力: [3, 1, 4, 1, 5, 9, 2, 6]
  最大値: 9
  平均値: 3.875

入力: [42]
  最大値: 42
  平均値: 42.0

入力: [-3, -1, -4, -1, -5]
  最大値: -1
  平均値: -2.8

入力: []
警告: 空のリストです
警告: 空のリストです
  最大値: None
  平均値: None
```

---

## 例題2: 可読性の改善

変数名やコメントを改善して、コードを読みやすくする。

```python
# ===================================================
# 例題2: 可読性の改善
# 読みにくいコードを読みやすく書き直す
# ===================================================

# --- 悪い例: 変数名が不明瞭 ---
def f(d, s, g):
    """意味不明な関数"""
    from collections import deque   # dequeをインポートする
    q = deque([s])                  # キューを作る
    v = {s}                         # 訪問済みを作る
    p = {s: None}                   # 親マップを作る
    while q:                        # キューが空でない間
        c = q.popleft()             # 先頭を取り出す
        if c == g:                  # ゴールに到着した場合
            r = []                  # 経路を初期化する
            while c is not None:    # 親がなくなるまで
                r.append(c)         # 追加する
                c = p[c]            # 親に移動する
            return r[::-1]          # 逆順にして返す
        x, y = c                    # 位置を取り出す
        for a, b in [(-1,0),(1,0),(0,-1),(0,1)]:    # 4方向を試す
            n = (x+a, y+b)          # 次の位置を計算する
            if (0<=n[0]<len(d) and 0<=n[1]<len(d[0])
                and d[n[0]][n[1]]==0 and n not in v):
                v.add(n)            # 訪問済みに追加する
                q.append(n)         # キューに追加する
                p[n] = c            # 親を記録する
    return None                     # ゴール不到達の場合


# --- 良い例: 変数名・コメントが分かりやすい ---
from collections import deque  # BFS用のキューをインポートする

def find_shortest_path(maze, start, goal):
    """BFSで迷路の最短経路を求める関数"""
    rows = len(maze)            # 迷路の行数を取得する
    cols = len(maze[0])         # 迷路の列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右の移動方向

    queue = deque([start])      # キューにスタートを入れる
    visited = {start}           # 訪問済みにスタートを登録する
    parent = {start: None}      # 経路復元用の親マップを作る

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # キューの先頭を取り出す

        if current == goal:     # ゴールに到着した場合
            path = []           # 経路リストを作る
            node = current      # ゴールからたどる
            while node is not None:     # 親がなくなるまで
                path.append(node)       # ノードを追加する
                node = parent[node]     # 親に移動する
            return path[::-1]   # 逆順にして返す

        row, col = current      # 現在位置の行と列を取り出す
        for delta_row, delta_col in directions:     # 4方向を順番に試す
            next_row = row + delta_row              # 次の行を計算する
            next_col = col + delta_col              # 次の列を計算する
            next_pos = (next_row, next_col)         # 次の位置をタプルにする

            is_inside = (0 <= next_row < rows       # 範囲内か判定する
                         and 0 <= next_col < cols)
            if is_inside and maze[next_row][next_col] == 0 and next_pos not in visited:
                visited.add(next_pos)       # 訪問済みに追加する
                queue.append(next_pos)      # キューに追加する
                parent[next_pos] = current  # 親を記録する

    return None  # ゴールに到達できなかった場合


# --- 比較結果を表示 ---
print("=== 可読性の改善 ===")           # タイトルを出力する
print()
print("【悪い例の問題点】")             # セクションタイトルを出力する
print("  - 関数名 f は意味不明")        # 問題点1を出力する
print("  - 引数名 d, s, g は1文字")    # 問題点2を出力する
print("  - 変数名 q, v, p, c, r は暗号的")  # 問題点3を出力する
print("  - docstringが「意味不明な関数」")   # 問題点4を出力する
print()
print("【良い例の改善点】")             # セクションタイトルを出力する
print("  - 関数名 find_shortest_path で目的が明確")  # 改善点1を出力する
print("  - 引数名 maze, start, goal で意味が分かる")  # 改善点2を出力する
print("  - 変数名が英語の意味ある単語")              # 改善点3を出力する
print("  - 各行にコメントがある")                     # 改善点4を出力する

# --- 動作確認 ---
maze = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 0],
]
path = find_shortest_path(maze, (0, 0), (3, 3))  # 良い例で探索する
print(f"\n動作確認: {path}")            # 経路を出力する
```

---

## 例題3: 効率性の改善

データ構造の選択で実行速度が大きく変わることを実証する。

```python
# ===================================================
# 例題3: 効率性の改善
# リスト vs セットの検索速度を比較する
# ===================================================

import time  # 処理時間の計測に使う

def has_duplicate_slow(data):
    """重複チェック（リスト版 = 遅い）"""
    seen = []                   # リストで記録する（検索がO(n)で遅い）
    for item in data:           # 各要素をループする
        if item in seen:        # リスト内に存在するか検索する（O(n)）
            return True         # 重複が見つかった場合Trueを返す
        seen.append(item)       # リストに追加する
    return False                # 重複なしの場合Falseを返す


def has_duplicate_fast(data):
    """重複チェック（セット版 = 速い）"""
    seen = set()                # セットで記録する（検索がO(1)で速い）
    for item in data:           # 各要素をループする
        if item in seen:        # セット内に存在するか検索する（O(1)）
            return True         # 重複が見つかった場合Trueを返す
        seen.add(item)          # セットに追加する
    return False                # 重複なしの場合Falseを返す


# --- 速度を比較する ---
print("=== 効率性の比較: リスト vs セット ===")  # タイトルを出力する
print()

sizes = [1000, 5000, 10000, 50000]  # テストするデータサイズのリスト

for size in sizes:                  # 各サイズでテストする
    test_data = list(range(size))   # 重複なしのデータを作る（最悪ケース）

    start_time = time.perf_counter()        # リスト版の計測を開始する
    has_duplicate_slow(test_data)            # リスト版を実行する
    slow_time = time.perf_counter() - start_time  # リスト版の時間を計算する

    start_time = time.perf_counter()        # セット版の計測を開始する
    has_duplicate_fast(test_data)            # セット版を実行する
    fast_time = time.perf_counter() - start_time  # セット版の時間を計算する

    speedup = slow_time / fast_time if fast_time > 0 else 0  # 速度比を計算する
    print(f"  データ数: {size:>6,}")             # データ数を出力する
    print(f"    リスト版: {slow_time:.4f}秒")    # リスト版の時間を出力する
    print(f"    セット版: {fast_time:.6f}秒")    # セット版の時間を出力する
    print(f"    速度差: {speedup:.0f}倍")        # 速度比を出力する
    print()
```

**実行結果の例**:
```
=== 効率性の比較: リスト vs セット ===

  データ数:  1,000
    リスト版: 0.0123秒
    セット版: 0.000089秒
    速度差: 138倍

  データ数:  5,000
    リスト版: 0.3012秒
    セット版: 0.000411秒
    速度差: 733倍
  ...
```

---

## 例題4: エラーハンドリングの追加

try/exceptを使ってプログラムがクラッシュしないようにする。

```python
# ===================================================
# 例題4: エラーハンドリング
# try/exceptで安全にエラーを処理する
# ===================================================

def safe_divide(numerator, denominator):
    """安全に割り算をする関数"""
    try:                                    # エラーが起きるかもしれないコード
        result = numerator / denominator    # 割り算を実行する
        return result                       # 結果を返す
    except ZeroDivisionError:               # ゼロ除算エラーの場合
        print("  エラー: 0で割ることはできません")  # エラーメッセージを出力する
        return None                         # Noneを返す
    except TypeError:                       # 型エラーの場合
        print("  エラー: 数値でない値が渡されました")  # エラーメッセージを出力する
        return None                         # Noneを返す


def safe_list_access(data, index):
    """安全にリストの要素を取得する関数"""
    try:                                    # エラーが起きるかもしれないコード
        value = data[index]                 # インデックスで要素を取得する
        return value                        # 値を返す
    except IndexError:                      # インデックス範囲外の場合
        print(f"  エラー: インデックス{index}は範囲外です（リスト長: {len(data)}）")
        return None                         # Noneを返す
    except TypeError:                       # 型エラーの場合
        print(f"  エラー: インデックスは整数でなければなりません")
        return None                         # Noneを返す


def validate_maze_input(maze, start, goal):
    """迷路の入力データを検証する関数"""
    errors = []                     # エラーリストを初期化する

    if not maze:                    # 迷路が空の場合
        errors.append("迷路が空です")   # エラーを追加する
        return errors               # チェック終了して返す

    rows = len(maze)                # 行数を取得する
    cols = len(maze[0])             # 列数を取得する

    sr, sc = start                  # スタート位置を取り出す
    if not (0 <= sr < rows and 0 <= sc < cols):     # 範囲外の場合
        errors.append(f"スタート{start}が範囲外です")  # エラーを追加する
    elif maze[sr][sc] != 0:         # 壁の場合
        errors.append(f"スタート{start}が壁です")      # エラーを追加する

    gr, gc = goal                   # ゴール位置を取り出す
    if not (0 <= gr < rows and 0 <= gc < cols):     # 範囲外の場合
        errors.append(f"ゴール{goal}が範囲外です")     # エラーを追加する
    elif maze[gr][gc] != 0:         # 壁の場合
        errors.append(f"ゴール{goal}が壁です")         # エラーを追加する

    return errors                   # エラーリストを返す


# --- テスト ---
print("=== エラーハンドリング ===")     # タイトルを出力する

print("\n【割り算テスト】")              # セクションタイトルを出力する
print(f"  10 / 3 = {safe_divide(10, 3)}")      # 正常ケースを出力する
print(f"  10 / 0 = {safe_divide(10, 0)}")      # ゼロ除算ケースを出力する
print(f"  10 / 'a' = {safe_divide(10, 'a')}")  # 型エラーケースを出力する

print("\n【リストアクセステスト】")      # セクションタイトルを出力する
data = [10, 20, 30]                     # テストデータを定義する
print(f"  data[1] = {safe_list_access(data, 1)}")    # 正常ケースを出力する
print(f"  data[5] = {safe_list_access(data, 5)}")    # 範囲外ケースを出力する

print("\n【迷路入力検証テスト】")        # セクションタイトルを出力する
maze = [[0, 0, 1], [0, 1, 0], [0, 0, 0]]   # テスト迷路を定義する
errors = validate_maze_input(maze, (0, 0), (2, 2))  # 正常入力を検証する
print(f"  正常入力: エラー{len(errors)}件")          # 結果を出力する
errors = validate_maze_input(maze, (5, 5), (2, 2))  # 範囲外入力を検証する
print(f"  範囲外スタート: {errors}")                 # エラー内容を出力する
errors = validate_maze_input(maze, (0, 2), (2, 2))  # 壁スタートを検証する
print(f"  壁スタート: {errors}")                     # エラー内容を出力する
errors = validate_maze_input([], (0, 0), (0, 0))    # 空迷路を検証する
print(f"  空迷路: {errors}")                         # エラー内容を出力する
```

**実行結果**:
```
=== エラーハンドリング ===

【割り算テスト】
  10 / 3 = 3.3333333333333335
  エラー: 0で割ることはできません
  10 / 0 = None
  エラー: 数値でない値が渡されました
  10 / 'a' = None

【リストアクセステスト】
  data[1] = 20
  エラー: インデックス5は範囲外です（リスト長: 3）
  data[5] = None

【迷路入力検証テスト】
  正常入力: エラー0件
  範囲外スタート: ['スタート(5, 5)が範囲外です']
  壁スタート: ['スタート(0, 2)が壁です']
  空迷路: ['迷路が空です']
```

---

## 例題5: 既存コードに機能を追加する

第13回の迷路BFSに「探索アニメーション表示」機能を追加する。

```python
# ===================================================
# 例題5: 既存コードへの機能追加
# BFSに探索過程のステップ表示機能を追加する
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def bfs_with_trace(maze, start, goal):
    """探索過程を表示するBFS関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する
    direction_names = ["上", "下", "左", "右"]  # 方向名を定義する

    queue = deque([start])      # キューにスタートを入れる
    visited = {start}           # 訪問済みを初期化する
    parent = {start: None}      # 親マップを初期化する
    step_count = 0              # ステップ数を初期化する

    print(f"探索開始: スタート={start}, ゴール={goal}")  # 開始メッセージを出力する
    print()

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # キューの先頭を取り出す
        step_count += 1             # ステップ数を増やす

        if current == goal:         # ゴールに到着した場合
            print(f"ステップ{step_count}: {current} → ゴール到着！")  # 到着メッセージ
            path = []               # 経路リストを作る
            node = current          # ゴールからたどる
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], step_count  # 経路とステップ数を返す

        # --- 探索過程を表示する ---
        neighbors_info = []         # 隣接情報リストを初期化する
        row, col = current          # 現在位置を取り出す

        for i, (dr, dc) in enumerate(directions):  # 4方向を試す
            nr = row + dr           # 次の行を計算する
            nc = col + dc           # 次の列を計算する
            next_pos = (nr, nc)     # 次の位置をタプルにする

            if not (0 <= nr < rows and 0 <= nc < cols):  # 範囲外の場合
                neighbors_info.append(f"{direction_names[i]}:範囲外")
            elif maze[nr][nc] == 1:     # 壁の場合
                neighbors_info.append(f"{direction_names[i]}:壁")
            elif next_pos in visited:   # 訪問済みの場合
                neighbors_info.append(f"{direction_names[i]}:訪問済")
            else:                       # 移動可能な場合
                neighbors_info.append(f"{direction_names[i]}:→{next_pos}")
                visited.add(next_pos)       # 訪問済みに追加する
                queue.append(next_pos)      # キューに追加する
                parent[next_pos] = current  # 親を記録する

        info_str = ", ".join(neighbors_info)    # 情報を文字列に結合する
        print(f"ステップ{step_count}: {current} [{info_str}]")  # 探索情報を出力する

    print("ゴールに到達できませんでした")  # 失敗メッセージを出力する
    return None, step_count  # Noneとステップ数を返す


# --- テスト ---
maze = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 0],
]
print("=== 探索過程の可視化 ===")   # タイトルを出力する
path, steps = bfs_with_trace(maze, (0, 0), (3, 3))  # 探索を実行する
if path:                            # 経路がある場合
    print(f"\n最短経路: {path}")     # 経路を出力する
    print(f"探索ステップ数: {steps}")  # ステップ数を出力する
```

---

## 標準課題

### 標準課題1（超やさしい）: バグを見つけて説明する

以下のコードにはバグが2つある。各バグを見つけて、何が問題か日本語で説明しなさい（修正コードは不要）。

```python
# ===================================================
# 課題1: バグを見つけて説明する
# このコードの2つのバグを日本語で説明しなさい
# ===================================================

def count_occurrences(data, target):
    """リスト内のtargetの出現回数を返す関数（バグあり）"""
    count = 1                       # カウンタを初期化する
    for i in range(len(data)):      # 全要素をループする
        if data[i] == target:       # targetと一致する場合
            count += 1              # カウンタを増やす
    return count                    # カウンタを返す

# テスト
print(count_occurrences([1, 2, 3, 2, 2], 2))  # 期待値: 3
print(count_occurrences([1, 2, 3], 5))         # 期待値: 0
```

---

### 標準課題2（超やさしい）: 変数名を修正する

以下のコードの変数名を全て英語の意味ある名前に変更しなさい。動作は変えないこと。

```python
# ===================================================
# 課題2: 変数名の修正
# 全ての1文字変数名を意味ある英語名に変更する
# ===================================================

def f(a):
    """ソートされたリストを返す関数（変数名を修正すること）"""
    b = a[:]                    # コピーを作る
    n = len(b)                  # 要素数を取得する
    for i in range(1, n):       # 2番目の要素から開始する
        k = b[i]                # 今回挿入する値
        j = i - 1               # 比較位置
        while j >= 0 and b[j] > k:  # 左隣が大きい間
            b[j + 1] = b[j]    # 右にずらす
            j -= 1              # 比較位置を左に移動する
        b[j + 1] = k            # 正しい位置に挿入する
    return b                    # ソート済みリストを返す
```

---

### 標準課題3（やさしい）: コメントを追加する

以下のコードに、各行の処理内容を日本語コメントで追加しなさい。

```python
# ===================================================
# 課題3: コメントの追加
# 各行に日本語コメントを追加しなさい
# ===================================================

from collections import deque

def bfs_count(maze, start):
    rows = len(maze)
    cols = len(maze[0])
    queue = deque([start])
    visited = {start}
    count = 0
    while queue:
        current = queue.popleft()
        count += 1
        row, col = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] == 0 and next_pos not in visited):
                visited.add(next_pos)
                queue.append(next_pos)
    return count
```

---

### 標準課題4（やさしい）: 関数を分割する

以下の長い関数を、3つ以上の小さな関数に分割しなさい。各関数は1つの役割に集中させること。

```python
# ===================================================
# 課題4: 関数の分割
# 1つの大きな関数を複数の小さな関数に分ける
# ===================================================

def do_everything(numbers):
    """全部やる関数（分割すること）"""
    # ソート
    sorted_nums = numbers[:]
    for i in range(1, len(sorted_nums)):
        key = sorted_nums[i]
        j = i - 1
        while j >= 0 and sorted_nums[j] > key:
            sorted_nums[j+1] = sorted_nums[j]
            j -= 1
        sorted_nums[j+1] = key
    # 統計
    total = 0
    for num in sorted_nums:
        total += num
    average = total / len(sorted_nums)
    minimum = sorted_nums[0]
    maximum = sorted_nums[-1]
    # 表示
    print(f"ソート結果: {sorted_nums}")
    print(f"合計: {total}")
    print(f"平均: {average}")
    print(f"最小: {minimum}")
    print(f"最大: {maximum}")
```

---

### 標準課題5（やややさしい）: アルゴリズムの最適化

以下の線形探索を二分探索に書き換え、速度を比較しなさい。

```python
# ===================================================
# 課題5: 線形探索→二分探索への最適化
# 同じ結果を返すが速い二分探索版を作る
# ===================================================

def linear_search(sorted_data, target):
    """線形探索（遅い版）"""
    for i in range(len(sorted_data)):
        if sorted_data[i] == target:
            return i
    return -1

# この関数を二分探索版に書き換えなさい
# def binary_search(sorted_data, target):
#     ...
```

---

### 標準課題6（やややさしい）: 速度を計測して比較する

課題5の線形探索と二分探索の実行時間を、データサイズ1000、10000、100000、1000000で比較し、結果を表形式で出力しなさい。

```python
# ===================================================
# 課題6: 速度計測と比較
# 線形探索と二分探索の実行時間を表で出力する
# ===================================================

import time

# 速度比較を実行し、結果を表形式で出力しなさい
# ヘッダー: データ数 | 線形探索 | 二分探索 | 速度比
```

---

### 標準課題7（やや普通）: try/exceptを追加する

以下のBFS関数に、不正な入力（空迷路、範囲外スタート、壁スタート）を安全に処理するエラーハンドリングを追加しなさい。

```python
# ===================================================
# 課題7: エラーハンドリングの追加
# BFS関数に入力検証とtry/exceptを追加する
# ===================================================

from collections import deque

def safe_bfs(maze, start, goal):
    """安全なBFS関数（エラーハンドリング付き）"""
    # ここに入力検証とtry/exceptを追加しなさい
    pass
```

---

### 標準課題8（やや普通）: 不正入力のテストを作る

課題7のsafe_bfs関数に対して、以下の8種類のテストケースを作成し、全て正しく処理されることを確認しなさい。

```python
# ===================================================
# 課題8: テストケースの作成
# 以下の8パターンをテストしなさい
# 1. 正常な迷路     2. 空の迷路
# 3. 範囲外スタート  4. 範囲外ゴール
# 5. 壁スタート     6. 壁ゴール
# 7. 到達不能ゴール  8. スタート=ゴール
# ===================================================
```

---

### 標準課題9（普通）: 既存BFSに機能追加

例題5を参考に、第13回のアイテム収集BFSに以下の機能を追加しなさい。
- 探索した状態数を表示する
- アイテムを取得した瞬間にメッセージを出力する
- ゴール到達時に全経路と統計を表示する

```python
# ===================================================
# 課題9: アイテム収集BFSの機能追加
# 探索過程のログ出力機能を追加する
# ===================================================

from collections import deque

def solve_maze_verbose(maze, start, goal, items):
    """ログ出力付きアイテム収集BFS関数"""
    # ここに実装しなさい
    pass
```

---

### 標準課題10（普通）: 完全なコードレビュー実施

以下のコードに対して、4つの観点（正しさ・可読性・効率性・拡張性）で問題点を全て指摘し、全ての問題を修正した改善版コードを作成しなさい。

```python
# ===================================================
# 課題10: 以下のコードをレビューし改善版を作成する
# ===================================================

def s(m, s, g, it):
    from collections import deque
    q=deque([(s,frozenset())])
    v=set()
    v.add((s,frozenset()))
    p={(s,frozenset()):None}
    while q:
        c,co=q.popleft()
        if c==g and len(co)==len(it):
            r=[]
            st=(c,co)
            while st!=None:
                r.append(st)
                st=p[st]
            r.reverse()
            return r
        x,y=c
        for a,b in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx=x+a
            ny=y+b
            np=(nx,ny)
            if 0<=nx<len(m) and 0<=ny<len(m[0]) and m[nx][ny]==0:
                nc=co
                if np in it:
                    nc=co|{np}
                ns=(np,nc)
                if ns not in v:
                    v.add(ns)
                    q.append(ns)
                    p[ns]=(c,co)
    return None
```

---

## 発展課題

### 発展課題1: ペアレビュー演習

隣の席の人と自分の第13回課題のコードを交換し、以下のチェックリストでレビューを行いなさい。レビュー結果を文字列として出力するプログラムを作ること。

```
【レビューチェックリスト】
1. 正しさ: コードがエラーなく実行できるか
2. 可読性: 変数名が英語で意味があるか
3. 効率性: 適切なデータ構造を使っているか
4. 拡張性: マジックナンバーがないか
```

---

### 発展課題2: 改善のプレゼンテーション

自分のコードの「改善前」と「改善後」を並べて表示するプログラムを作り、何をどう改善したかを説明する出力を作りなさい。

---

## 解答例

### 課題1 解答例

```python
# ===================================================
# 課題1 解答例: バグの説明
# ===================================================

# バグ1: count = 1 で初期化している
# → 0 で初期化すべき。1で始めると結果が常に1多くなる
# 例: [1,2,3,2,2] で target=2 のとき、正解は3だが4が返る

# バグ2: target が存在しない場合でも1が返る
# → count=1 で始まるため、出現回数0のはずが1になる
# 例: [1,2,3] で target=5 のとき、正解は0だが1が返る

# 修正版
def count_occurrences_fixed(data, target):
    """リスト内のtargetの出現回数を返す関数（修正版）"""
    count = 0                       # カウンタを0で初期化する（修正点1）
    for i in range(len(data)):      # 全要素をループする
        if data[i] == target:       # targetと一致する場合
            count += 1              # カウンタを増やす
    return count                    # カウンタを返す


# テスト
print("=== 課題1: バグの修正 ===")  # タイトルを出力する
print(f"[1,2,3,2,2]でtarget=2: {count_occurrences_fixed([1,2,3,2,2], 2)}")  # 期待値3
print(f"[1,2,3]でtarget=5: {count_occurrences_fixed([1,2,3], 5)}")          # 期待値0
```

---

### 課題2 解答例

```python
# ===================================================
# 課題2 解答例: 変数名の修正
# ===================================================

def insertion_sort(numbers):
    """挿入ソートでソートされたリストを返す関数"""
    sorted_list = numbers[:]        # 元リストのコピーを作る
    length = len(sorted_list)       # 要素数を取得する
    for current_index in range(1, length):  # 2番目の要素から開始する
        key_value = sorted_list[current_index]  # 今回挿入する値を保存する
        compare_index = current_index - 1       # 比較位置を設定する
        while compare_index >= 0 and sorted_list[compare_index] > key_value:  # 左隣が大きい間
            sorted_list[compare_index + 1] = sorted_list[compare_index]  # 右にずらす
            compare_index -= 1      # 比較位置を左に移動する
        sorted_list[compare_index + 1] = key_value  # 正しい位置に挿入する
    return sorted_list              # ソート済みリストを返す


# テスト
print("=== 課題2: 変数名の修正 ===")    # タイトルを出力する
test = [5, 2, 8, 1, 9, 3]               # テストデータを定義する
result = insertion_sort(test)            # ソートを実行する
print(f"入力: {test}")                   # 入力を出力する
print(f"出力: {result}")                 # 結果を出力する
```

---

### 課題3 解答例

```python
# ===================================================
# 課題3 解答例: コメントの追加
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def bfs_count(maze, start):
    """スタートから到達可能なセル数を数える関数"""
    rows = len(maze)                # 迷路の行数を取得する
    cols = len(maze[0])             # 迷路の列数を取得する
    queue = deque([start])          # キューにスタート位置を入れる
    visited = {start}               # 訪問済みにスタートを登録する
    count = 0                       # 到達可能セル数を初期化する
    while queue:                    # キューが空になるまで繰り返す
        current = queue.popleft()   # キューの先頭を取り出す
        count += 1                  # 到達可能セル数を1増やす
        row, col = current          # 現在位置の行と列を取り出す
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:  # 上下左右の4方向を試す
            nr, nc = row + dr, col + dc     # 次の位置を計算する
            next_pos = (nr, nc)             # 次の位置をタプルにする
            if (0 <= nr < rows and 0 <= nc < cols   # 範囲内かつ
                    and maze[nr][nc] == 0            # 通路かつ
                    and next_pos not in visited):    # 未訪問の場合
                visited.add(next_pos)       # 訪問済みに追加する
                queue.append(next_pos)      # キューに追加する
    return count                    # 到達可能セル数を返す


# テスト
maze = [[0,0,1,0],[0,1,0,0],[0,0,0,0],[0,1,0,0]]  # テスト迷路を定義する
print(f"=== 課題3: 到達可能セル数 ===")             # タイトルを出力する
print(f"到達可能セル数: {bfs_count(maze, (0, 0))}")  # 結果を出力する
```

---

### 課題4 解答例

```python
# ===================================================
# 課題4 解答例: 関数の分割
# ===================================================

def sort_numbers(numbers):
    """挿入ソートで数値リストをソートする関数"""
    sorted_nums = numbers[:]        # 元リストのコピーを作る
    for i in range(1, len(sorted_nums)):    # 2番目から開始する
        key = sorted_nums[i]        # 今回挿入する値を保存する
        j = i - 1                   # 比較位置を設定する
        while j >= 0 and sorted_nums[j] > key:  # 左隣が大きい間
            sorted_nums[j + 1] = sorted_nums[j]  # 右にずらす
            j -= 1                  # 比較位置を左に移動する
        sorted_nums[j + 1] = key    # 正しい位置に挿入する
    return sorted_nums              # ソート済みリストを返す


def calculate_statistics(numbers):
    """リストの統計情報を計算する関数"""
    total = 0                       # 合計を初期化する
    for num in numbers:             # 各要素をループする
        total += num                # 合計に加算する
    average = total / len(numbers)  # 平均を計算する
    minimum = numbers[0]            # 最小値を取得する（ソート済み前提）
    maximum = numbers[-1]           # 最大値を取得する（ソート済み前提）
    stats = {                       # 統計情報を辞書にまとめる
        "total": total,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
    }
    return stats                    # 統計情報を返す


def display_results(sorted_nums, stats):
    """結果を表示する関数"""
    print(f"ソート結果: {sorted_nums}")     # ソート結果を出力する
    print(f"合計: {stats['total']}")        # 合計を出力する
    print(f"平均: {stats['average']}")      # 平均を出力する
    print(f"最小: {stats['minimum']}")      # 最小値を出力する
    print(f"最大: {stats['maximum']}")      # 最大値を出力する


# メイン処理
print("=== 課題4: 関数の分割 ===")  # タイトルを出力する
numbers = [38, 27, 43, 3, 9, 82, 10]   # テストデータを定義する
sorted_nums = sort_numbers(numbers)     # ソートを実行する
stats = calculate_statistics(sorted_nums)   # 統計を計算する
display_results(sorted_nums, stats)     # 結果を表示する
```

---

### 課題5 解答例

```python
# ===================================================
# 課題5 解答例: 二分探索への最適化
# ===================================================

def linear_search(sorted_data, target):
    """線形探索（遅い版）"""
    for i in range(len(sorted_data)):   # 先頭から順に探す
        if sorted_data[i] == target:    # 一致した場合
            return i                    # インデックスを返す
    return -1                           # 見つからなかった場合


def binary_search(sorted_data, target):
    """二分探索（速い版）"""
    low = 0                         # 探索範囲の下限を設定する
    high = len(sorted_data) - 1     # 探索範囲の上限を設定する
    while low <= high:              # 範囲が有効な間繰り返す
        mid = (low + high) // 2     # 中央のインデックスを計算する
        if sorted_data[mid] == target:      # 中央が目標値の場合
            return mid                      # インデックスを返す
        elif sorted_data[mid] < target:     # 中央が目標より小さい場合
            low = mid + 1                   # 下限を中央の右に移動する
        else:                               # 中央が目標より大きい場合
            high = mid - 1                  # 上限を中央の左に移動する
    return -1                       # 見つからなかった場合


# テスト
print("=== 課題5: 二分探索 ===")    # タイトルを出力する
data = list(range(0, 100, 3))      # ソート済みデータを作る
target = 42                         # 探索対象を設定する
print(f"データ: {data[:10]}... (計{len(data)}個)")  # データの一部を出力する
print(f"線形探索: インデックス {linear_search(data, target)}")  # 線形探索の結果
print(f"二分探索: インデックス {binary_search(data, target)}")  # 二分探索の結果
```

---

### 課題6 解答例

```python
# ===================================================
# 課題6 解答例: 速度計測と比較
# ===================================================

import time  # 処理時間の計測に使う

def linear_search(sorted_data, target):
    """線形探索"""
    for i in range(len(sorted_data)):
        if sorted_data[i] == target:
            return i
    return -1

def binary_search(sorted_data, target):
    """二分探索"""
    low = 0
    high = len(sorted_data) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_data[mid] == target:
            return mid
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

print("=== 課題6: 速度比較 ===")    # タイトルを出力する
print()
print(f"{'データ数':>10} | {'線形探索':>12} | {'二分探索':>12} | {'速度比':>8}")  # ヘッダ
print("-" * 55)                     # 区切り線を出力する

sizes = [1000, 10000, 100000, 1000000]  # テストするデータサイズ

for size in sizes:                  # 各サイズでテストする
    data = list(range(size))        # ソート済みデータを作る
    target = size - 1               # 最後の要素を探す（最悪ケース）

    start_time = time.perf_counter()        # 線形探索の計測を開始する
    linear_search(data, target)             # 線形探索を実行する
    linear_time = time.perf_counter() - start_time  # 時間を計算する

    start_time = time.perf_counter()        # 二分探索の計測を開始する
    binary_search(data, target)             # 二分探索を実行する
    binary_time = time.perf_counter() - start_time  # 時間を計算する

    ratio = linear_time / binary_time if binary_time > 0 else 0  # 速度比を計算する
    print(f"{size:>10,} | {linear_time:>10.6f}秒 | {binary_time:>10.6f}秒 | {ratio:>6.0f}倍")
```

---

### 課題7 解答例

```python
# ===================================================
# 課題7 解答例: エラーハンドリング付きBFS
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def safe_bfs(maze, start, goal):
    """安全なBFS関数（エラーハンドリング付き）"""

    # --- 入力検証 ---
    if not maze or not maze[0]:         # 迷路が空の場合
        print("エラー: 迷路が空です")   # エラーメッセージを出力する
        return None

    rows = len(maze)                    # 行数を取得する
    cols = len(maze[0])                 # 列数を取得する

    try:
        sr, sc = start                  # スタート位置を取り出す
        gr, gc = goal                   # ゴール位置を取り出す
    except (TypeError, ValueError):     # タプルでない場合
        print("エラー: start/goalはタプル(行,列)で指定してください")
        return None

    if not (0 <= sr < rows and 0 <= sc < cols):     # スタートが範囲外の場合
        print(f"エラー: スタート{start}が範囲外です")
        return None
    if not (0 <= gr < rows and 0 <= gc < cols):     # ゴールが範囲外の場合
        print(f"エラー: ゴール{goal}が範囲外です")
        return None
    if maze[sr][sc] != 0:               # スタートが壁の場合
        print(f"エラー: スタート{start}が壁です")
        return None
    if maze[gr][gc] != 0:               # ゴールが壁の場合
        print(f"エラー: ゴール{goal}が壁です")
        return None

    # --- BFS探索 ---
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])              # キューを初期化する
    visited = {start}                   # 訪問済みを初期化する
    parent = {start: None}              # 親マップを初期化する

    while queue:                        # キューが空になるまで繰り返す
        current = queue.popleft()       # 先頭を取り出す
        if current == goal:             # ゴールに到着した場合
            path = []                   # 経路リストを作る
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]           # 逆順にして返す

        row, col = current
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] == 0 and next_pos not in visited):
                visited.add(next_pos)
                queue.append(next_pos)
                parent[next_pos] = current

    print("ゴールに到達できません")     # 到達不能の場合
    return None


# テスト
print("=== 課題7: 安全なBFS ===")   # タイトルを出力する
maze = [[0,0,1],[0,1,0],[0,0,0]]    # テスト迷路を定義する
print(f"正常: {safe_bfs(maze, (0,0), (2,2))}")          # 正常ケース
print(f"空迷路: {safe_bfs([], (0,0), (0,0))}")          # 空迷路ケース
print(f"範囲外: {safe_bfs(maze, (5,5), (2,2))}")        # 範囲外ケース
print(f"壁: {safe_bfs(maze, (0,2), (2,2))}")            # 壁ケース
```

---

### 課題8 解答例

```python
# ===================================================
# 課題8 解答例: テストケース8パターン
# ===================================================

from collections import deque  # BFS用のキューをインポートする

# safe_bfs関数は課題7の解答例と同じものを使う

def run_all_tests():
    """8パターンのテストを実行する関数"""
    maze_normal = [[0,0,1],[0,1,0],[0,0,0]]     # 正常な迷路を定義する
    maze_blocked = [[0,1,0],[1,1,1],[0,1,0]]     # 到達不能な迷路を定義する

    tests = [                       # テストケースを定義する
        ("1. 正常な迷路",     maze_normal,  (0,0), (2,2), True),
        ("2. 空の迷路",       [],           (0,0), (0,0), False),
        ("3. 範囲外スタート", maze_normal,  (5,5), (2,2), False),
        ("4. 範囲外ゴール",   maze_normal,  (0,0), (9,9), False),
        ("5. 壁スタート",     maze_normal,  (0,2), (2,2), False),
        ("6. 壁ゴール",       maze_normal,  (0,0), (1,1), False),
        ("7. 到達不能ゴール", maze_blocked, (0,0), (2,2), False),
        ("8. スタート=ゴール",maze_normal,  (0,0), (0,0), True),
    ]

    print("=== 課題8: テスト結果 ===")  # タイトルを出力する
    passed = 0                          # 合格数を初期化する

    for name, maze, start, goal, expect_path in tests:  # 各テストを実行する
        result = safe_bfs(maze, start, goal)            # BFSを実行する
        has_path = result is not None                   # 経路の有無を判定する
        is_ok = has_path == expect_path                 # 期待値と比較する
        status = "OK" if is_ok else "NG"                # 結果ラベルを決める
        if is_ok:                                       # 合格の場合
            passed += 1                                 # 合格数を増やす
        print(f"  {name}: {status}")                    # 結果を出力する

    print(f"\n合格: {passed}/{len(tests)}")  # 合格率を出力する


run_all_tests()  # テストを実行する
```

---

### 課題9 解答例

```python
# ===================================================
# 課題9 解答例: ログ出力付きアイテム収集BFS
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def solve_maze_verbose(maze, start, goal, items):
    """ログ出力付きアイテム収集BFS関数"""
    rows = len(maze)                # 行数を取得する
    cols = len(maze[0])             # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_items = frozenset(items)    # 全アイテムの集合を作る

    initial = (start, frozenset())  # 初期状態を作る
    queue = deque([initial])        # キューを初期化する
    visited = {initial}             # 訪問済みを初期化する
    parent = {initial: None}        # 親マップを初期化する
    explored = 0                    # 探索数を初期化する

    print(f"探索開始: アイテム{len(items)}個を収集してゴールを目指す")  # 開始メッセージ

    while queue:                    # キューが空になるまで繰り返す
        current_pos, collected = queue.popleft()  # 先頭を取り出す
        explored += 1               # 探索数を増やす

        if current_pos == goal and collected == all_items:  # 全条件達成
            print(f"\nゴール到達！ 探索状態数: {explored}")  # 到達メッセージ
            path = []               # 経路リストを作る
            state = (current_pos, collected)
            while state is not None:
                path.append(state)
                state = parent[state]
            result_path = path[::-1]    # 逆順にする

            print(f"経路の長さ: {len(result_path)-1}歩")    # 歩数を出力する
            print(f"訪問済み状態数: {len(visited)}")        # 訪問数を出力する
            print()
            for i, (pos, coll) in enumerate(result_path):   # 各ステップを出力する
                print(f"  ステップ{i:2d}: 位置{pos} アイテム{len(coll)}/{len(items)}個")
            return result_path      # 経路を返す

        row, col = current_pos
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0):
                new_collected = collected
                if next_pos in items and next_pos not in collected:  # 新しいアイテムの場合
                    new_collected = collected | {next_pos}
                    print(f"  [探索{explored}] 位置{next_pos}でアイテム発見！ ({len(new_collected)}/{len(items)}個)")

                new_state = (next_pos, new_collected)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
                    parent[new_state] = (current_pos, collected)

    print(f"ゴールに到達できません（探索状態数: {explored}）")  # 失敗メッセージ
    return None


# テスト
maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]
items = [(0, 4), (2, 0), (4, 2)]   # アイテム3個を定義する
print("=== 課題9: ログ付きBFS ===")  # タイトルを出力する
solve_maze_verbose(maze, (0, 0), (4, 4), items)  # ログ付きBFSを実行する
```

---

### 課題10 解答例

```python
# ===================================================
# 課題10 解答例: 完全なコードレビューと改善
# ===================================================

# 【問題点の一覧】
# 正しさ:
#   - None比較に != を使用 → is not を使うべき
#   - 空リスト・空迷路のチェックなし
# 可読性:
#   - 関数名 s は意味不明 → solve_item_maze に変更
#   - 引数名 m, s, g, it は1文字 → maze, start, goal, items に変更
#   - 変数名 q, v, p, c, co, r, st, nx, ny, np, nc, ns は暗号的
#   - コメントが1つもない
#   - docstringがない
# 効率性:
#   - 大きな問題はないが、items を set に変換すれば in 検索が速くなる
# 拡張性:
#   - import が関数の中 → ファイル先頭に移動すべき
#   - マジックナンバー 0 → 定数 PASSAGE に変更
#   - 方向ベクトルがハードコーディング → 定数に抽出

from collections import deque  # BFS用のキューをインポートする

PASSAGE = 0     # 通路を表す定数
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向の移動ベクトル


def solve_item_maze(maze, start, goal, items):
    """全アイテムを集めてゴールする最短経路をBFSで求める関数"""

    # --- 入力検証 ---
    if not maze or not maze[0]:         # 迷路が空の場合
        print("エラー: 迷路が空です")
        return None

    rows = len(maze)                    # 行数を取得する
    cols = len(maze[0])                 # 列数を取得する
    item_set = set(items)               # アイテムをsetに変換して検索を高速化する
    all_items = frozenset(items)        # 全アイテムの集合を作る

    # --- BFS初期化 ---
    initial_state = (start, frozenset())    # 初期状態を作る
    queue = deque([initial_state])          # キューを初期化する
    visited = {initial_state}               # 訪問済みを初期化する
    parent = {initial_state: None}          # 親マップを初期化する

    # --- BFSメインループ ---
    while queue:                            # キューが空になるまで繰り返す
        current_pos, collected_items = queue.popleft()  # 先頭を取り出す

        # --- ゴール判定 ---
        if current_pos == goal and collected_items == all_items:  # 全条件達成
            path = []                       # 経路リストを作る
            state = (current_pos, collected_items)
            while state is not None:        # is not を使う（修正点）
                path.append(state)
                state = parent[state]
            return path[::-1]               # 逆順にして返す

        # --- 4方向を探索 ---
        row, col = current_pos              # 現在位置を取り出す
        for delta_row, delta_col in DIRECTIONS:  # 定数を使う（修正点）
            next_row = row + delta_row      # 次の行を計算する
            next_col = col + delta_col      # 次の列を計算する
            next_pos = (next_row, next_col)  # 次の位置をタプルにする

            is_valid = (0 <= next_row < rows        # 範囲内かつ
                        and 0 <= next_col < cols    # 範囲内かつ
                        and maze[next_row][next_col] == PASSAGE)  # 通路の場合

            if is_valid:
                next_collected = collected_items     # 収集状態をコピーする
                if next_pos in item_set:            # アイテムがある場合
                    next_collected = collected_items | {next_pos}  # 追加する

                next_state = (next_pos, next_collected)
                if next_state not in visited:        # 未訪問の場合
                    visited.add(next_state)
                    queue.append(next_state)
                    parent[next_state] = (current_pos, collected_items)

    return None  # ゴール不到達の場合


# テスト
maze = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 0],
]
items = [(0, 3), (2, 0)]               # アイテム2個を定義する
result = solve_item_maze(maze, (0, 0), (3, 3), items)  # 改善版を実行する

print("=== 課題10: 改善版テスト ===")   # タイトルを出力する
if result is not None:                  # 経路が見つかった場合
    print(f"経路が見つかりました（{len(result)-1}歩）")
    for i, (pos, coll) in enumerate(result):    # 各ステップを出力する
        print(f"  ステップ{i}: 位置{pos} アイテム{len(coll)}個")
else:
    print("経路が見つかりませんでした")

# エラーケースのテスト
print("\n【エラーケースのテスト】")
solve_item_maze([], (0,0), (0,0), [])   # 空迷路のテスト
```
