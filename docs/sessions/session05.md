# 第5回: 探索アルゴリズムの応用

## 説明

### なぜ bisect を使うのか？

前回、二分探索を自分で実装しました。しかし、Pythonには **標準ライブラリに二分探索が用意** されています。

```python
import bisect  # Python標準ライブラリ（インストール不要）
```

自作の二分探索との違い:
| 項目 | 自作 binary_search | bisect モジュール |
|------|-------------------|------------------|
| 実装 | 自分で書く | 標準ライブラリ |
| 速度 | Python速度 | **C言語で実装済み（高速）** |
| 機能 | 値の検索のみ | 検索 + **挿入位置** の特定 |
| 重複対応 | 工夫が必要 | `bisect_left` / `bisect_right` で対応 |

### bisect の主な関数

| 関数 | 説明 |
|------|------|
| `bisect_left(a, x)` | `x` を挿入すべき **左端** の位置を返す |
| `bisect_right(a, x)` | `x` を挿入すべき **右端** の位置を返す |
| `bisect(a, x)` | `bisect_right` と同じ |
| `insort_left(a, x)` | `x` をソートを保ったまま **左端** に挿入する |
| `insort_right(a, x)` | `x` をソートを保ったまま **右端** に挿入する |
| `insort(a, x)` | `insort_right` と同じ |

### bisect_left と bisect_right の違い

重複がない場合は同じ結果ですが、**重複がある場合に差が出ます**。

```
データ: [1, 3, 5, 5, 5, 7, 9]
              ↑     ↑
         bisect_left  bisect_right
         (位置2)      (位置5)

bisect_left(data, 5)  → 2  (最初の5の位置)
bisect_right(data, 5) → 5  (最後の5の次の位置)
```

### 探索アルゴリズムの使い分け

| アルゴリズム | 計算量 | 条件 | 使いどころ |
|-------------|--------|------|-----------|
| 逐次探索 | O(n) | なし | 小データ、未ソート |
| 二分探索 | O(log n) | ソート済み | 大データの検索 |
| bisect | O(log n) | ソート済み | Python実用コード |
| ジャンプ探索 | O(sqrt(n)) | ソート済み | ブロック単位の探索 |
| 指数探索 | O(log n) | ソート済み | 無限/巨大リスト |

---

## 例題と課題

### 例題1: bisect_left と bisect_right の違い

```python
# ============================================================
# 例題1: bisect_left と bisect_right の違いを理解する
# ============================================================

import bisect  # bisectモジュールをインポートする

# --- 重複なしのデータ ---
data = [1, 3, 5, 7, 9, 11, 13]  # 重複なしのソート済みリスト
print(f"データ（重複なし）: {data}")  # データを表示する

target = 5  # 探したい値
left_pos = bisect.bisect_left(data, target)  # 左端の挿入位置を求める
right_pos = bisect.bisect_right(data, target)  # 右端の挿入位置を求める
print(f"  bisect_left(data, {target})  = {left_pos}")  # 左端の位置を表示する
print(f"  bisect_right(data, {target}) = {right_pos}")  # 右端の位置を表示する

# --- 存在しない値 ---
target = 8  # 存在しない値
left_pos = bisect.bisect_left(data, target)  # 挿入位置を求める
print(f"\n  bisect_left(data, {target})  = {left_pos}（8を挿入する位置）")  # 結果を表示する

# --- 重複ありのデータ ---
data_dup = [1, 3, 5, 5, 5, 7, 9]  # 重複ありのソート済みリスト
print(f"\nデータ（重複あり）: {data_dup}")  # データを表示する

target = 5  # 重複している値
left_pos = bisect.bisect_left(data_dup, target)  # 最初の5の位置を求める
right_pos = bisect.bisect_right(data_dup, target)  # 最後の5の次の位置を求める
print(f"  bisect_left(data, {target})  = {left_pos}（最初の5の位置）")  # 結果を表示する
print(f"  bisect_right(data, {target}) = {right_pos}（最後の5の次）")  # 結果を表示する
print(f"  5の個数: {right_pos - left_pos}個")  # 個数を計算して表示する
print(f"  5のスライス: data[{left_pos}:{right_pos}] = {data_dup[left_pos:right_pos]}")  # スライスで取得
```

---

#### 標準課題1（超やさしい）

ソート済みリスト `[1, 3, 5, 7, 9, 11, 13]` に対して、値 `6` の挿入位置を `bisect_left` で求め、「6を挿入するなら位置Xです」と表示するプログラムを作成してください。値 `4` と `10` についても同様に表示してください。

---

#### 標準課題2（超やさしい）

ソート済みリスト `[1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5]` に対して、`bisect_left` と `bisect_right` を使い、値 `3` が何個含まれているかを求めるプログラムを作成してください。値 `1`, `4`, `6` についても同様に個数を表示してください。

---

### 例題2: insort でソート済みリストを維持する

```python
# ============================================================
# 例題2: insort でソートを保ったまま要素を挿入する
# ============================================================

import bisect  # bisectモジュールをインポートする

sorted_list = []  # 空のリストから始める
values = [7, 3, 11, 1, 9, 5, 13, 2, 8]  # 挿入する値（バラバラの順番）

print("insort でソートを保ったまま挿入する")  # タイトルを表示する
print("=" * 50)  # 区切り線

for value in values:  # 各値について処理する
    insert_pos = bisect.bisect_left(sorted_list, value)  # 挿入位置を確認する
    bisect.insort(sorted_list, value)  # ソートを保ったまま挿入する
    print(f"  insort({value:>2}) → 位置{insert_pos}に挿入 → {sorted_list}")  # 状態を表示する

print(f"\n最終結果: {sorted_list}")  # 最終結果を表示する
print("ソート済みが維持されている!")  # 確認メッセージ
```

---

#### 標準課題3（やさしい）

空のリストに対して、ランダムに生成した10個の整数（1〜100）を `bisect.insort` で1つずつ挿入し、各ステップでリストの状態を表示するプログラムを作成してください。最終結果がソート済みであることを確認してください。

---

#### 標準課題4（やさしい）

リアルタイムに数値が到着する状況をシミュレーションしてください。20個のランダムな整数（1〜50）を1つずつ `insort` で挿入し、毎回の挿入後に「現在の中央値」を表示するプログラムを作成してください。（中央値: リストの真ん中の値。要素数が偶数の場合は中央2つの平均）

---

### 例題3: ジャンプ探索

```python
# ============================================================
# 例題3: ジャンプ探索の実装
# ============================================================

import math  # 平方根計算用モジュールをインポートする

def jump_search(data, target):  # ジャンプ探索の関数
    """ジャンプ探索: sqrt(n)ずつジャンプしてブロックを特定し、ブロック内を逐次探索"""
    n = len(data)  # データの長さを取得する
    jump_size = int(math.sqrt(n))  # ジャンプ幅をsqrt(n)にする
    print(f"  データ数: {n}, ジャンプ幅: {jump_size}")  # ジャンプ幅を表示する

    # --- ステップ1: ジャンプしてブロックを特定する ---
    prev = 0  # ブロックの開始位置
    curr = 0  # 現在のジャンプ位置

    while curr < n and data[curr] < target:  # targetより小さい間ジャンプする
        prev = curr  # 前の位置を記憶する
        curr += jump_size  # ジャンプ幅分進む
        print(f"  ジャンプ: 位置{curr}をチェック", end="")  # ジャンプ先を表示する
        if curr < n:  # 範囲内なら
            print(f" → data[{curr}]={data[curr]}")  # 値を表示する
        else:  # 範囲外なら
            print(f" → 範囲外")  # 範囲外と表示する

    # --- ステップ2: ブロック内を逐次探索する ---
    print(f"  ブロック内探索: 位置{prev}〜{min(curr, n - 1)}")  # 探索範囲を表示する
    for i in range(prev, min(curr + 1, n)):  # ブロック内を順に調べる
        if data[i] == target:  # 一致したら
            return i  # インデックスを返す
    return -1  # 見つからなかった

# --- テスト ---
data = list(range(0, 100, 3))  # [0, 3, 6, 9, ..., 99]を作る
print(f"データ: {data[:10]}... (全{len(data)}個)")  # 先頭10個を表示する
print()  # 空行

target = 42  # 探したい値
print(f"target={target} を探索:")  # 探索開始メッセージ
result = jump_search(data, target)  # ジャンプ探索を実行する
print(f"  結果: インデックス{result}")  # 結果を表示する
```

---

#### 標準課題5（やややさしい）

ジャンプ探索を実装してください。ソート済みリスト `list(range(1, 101))` に対して target=25, 50, 75, 100, 999 を探索し、それぞれの結果を表示するプログラムを作成してください。ジャンプ幅は `int(math.sqrt(n))` を使ってください。

---

#### 標準課題6（やややさしい）

ジャンプ探索に比較回数カウンターを追加し、同じデータ・同じtargetで逐次探索と二分探索と比較するプログラムを作成してください。100個のソート済みデータで target=1, 25, 50, 75, 100 を探索し、3つのアルゴリズムの比較回数を表形式で表示してください。

---

### 例題4: 指数探索

```python
# ============================================================
# 例題4: 指数探索の実装
# ============================================================

def exponential_search(data, target):  # 指数探索の関数
    """指数探索: 指数的に範囲を広げてからその範囲で二分探索する"""
    n = len(data)  # データの長さを取得する
    if n == 0:  # 空リストの場合
        return -1  # -1を返す

    if data[0] == target:  # 先頭が一致する場合
        return 0  # 0を返す

    # --- ステップ1: 指数的にインデックスを広げる ---
    bound = 1  # 最初の境界値は1
    print(f"  指数探索フェーズ:")  # フェーズ名を表示する
    while bound < n and data[bound] < target:  # targetより小さい間続ける
        print(f"    bound={bound}, data[{bound}]={data[bound]} < {target}")  # 現在の状態を表示する
        bound *= 2  # 境界を2倍にする
    print(f"    bound={bound}（探索範囲確定）")  # 確定した境界を表示する

    # --- ステップ2: 絞り込んだ範囲で二分探索する ---
    left = bound // 2  # 左端は境界の半分
    right = min(bound, n - 1)  # 右端は境界かデータ末尾の小さい方
    print(f"  二分探索フェーズ: [{left}..{right}]")  # 二分探索の範囲を表示する

    while left <= right:  # 探索範囲がある間繰り返す
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return -1  # 見つからなかった

# --- テスト ---
data = list(range(0, 200, 2))  # [0, 2, 4, 6, ..., 198]を作る
print(f"データ: {data[:10]}... (全{len(data)}個)")  # 先頭10個を表示する
print()  # 空行

target = 42  # 探したい値
print(f"target={target} を探索:")  # 探索開始メッセージ
result = exponential_search(data, target)  # 指数探索を実行する
print(f"  結果: インデックス{result}")  # 結果を表示する
```

---

#### 標準課題7（やや普通）

指数探索を実装してください。ソート済みリスト `list(range(1, 1001))` に対して target=1, 100, 500, 999, 2000 を探索し、それぞれの結果を表示するプログラムを作成してください。

---

#### 標準課題8（やや普通）

指数探索の「指数フェーズ」で何回の比較を行い、「二分探索フェーズ」で何回の比較を行ったかを分けてカウントし、合計比較回数を表示するプログラムを作成してください。1000個のデータで target=1, 100, 500, 999 を探索してください。

---

### 例題5: アルゴリズム性能比較

```python
# ============================================================
# 例題5: 複数の探索アルゴリズムの性能比較
# ============================================================

import time  # 時間計測用モジュール
import random  # ランダム値生成用モジュール
import bisect  # bisectモジュール
import math  # 数学関数用モジュール

def linear_search(data, target):  # 逐次探索
    """逐次探索"""
    for i in range(len(data)):  # 先頭から順に調べる
        if data[i] == target:  # 一致したら
            return i  # インデックスを返す
    return -1  # 見つからない

def binary_search(data, target):  # 二分探索
    """二分探索"""
    left = 0  # 左端
    right = len(data) - 1  # 右端
    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央
        if data[mid] == target:  # 一致
            return mid  # 返す
        elif data[mid] < target:  # 小さい
            left = mid + 1  # 右へ
        else:  # 大きい
            right = mid - 1  # 左へ
    return -1  # 見つからない

def bisect_search(data, target):  # bisect探索
    """bisect_leftを使った探索"""
    idx = bisect.bisect_left(data, target)  # 挿入位置を求める
    if idx < len(data) and data[idx] == target:  # 一致確認
        return idx  # 返す
    return -1  # 見つからない

# --- ベンチマーク ---
n = 100000  # データ数10万
data = list(range(n))  # ソート済みリスト
num_queries = 500  # 探索回数
targets = [random.randint(0, n - 1) for _ in range(num_queries)]  # ランダムtarget

algorithms = [  # テストするアルゴリズムのリスト
    ("Linear Search", linear_search),  # 逐次探索
    ("Binary Search", binary_search),  # 二分探索
    ("Bisect Search", bisect_search),  # bisect探索
]

results = []  # 結果を格納するリスト
for name, func in algorithms:  # 各アルゴリズムについてテストする
    start = time.perf_counter()  # 計測開始
    for t in targets:  # 各targetを探索する
        func(data, t)  # 探索を実行する
    elapsed = time.perf_counter() - start  # 経過時間
    results.append((name, elapsed))  # 結果を追加する

results.sort(key=lambda x: x[1])  # 速い順にソートする

print(f"探索アルゴリズム比較 (N={n:,}, クエリ={num_queries}回)")  # タイトル
print("=" * 45)  # 区切り線
for rank, (name, elapsed) in enumerate(results, 1):  # 順位をつけて表示する
    print(f"  {rank}位: {name:<18} {elapsed:.4f}秒")  # 結果を表示する
print("=" * 45)  # 区切り線
```

---

#### 標準課題9（普通）

逐次探索、二分探索、bisect探索、ジャンプ探索、指数探索の5つのアルゴリズムを実装し、データ数10万件・探索1000回でベンチマークを行い、速い順にランキング表示するプログラムを作成してください。

---

#### 標準課題10（普通）

データ数を `[1000, 10000, 100000]` と変化させて、5つの探索アルゴリズムの実行時間を計測し、matplotlib でデータサイズごとの実行時間を棒グラフに描画するプログラムを作成してください。グラフは2枚用意し、1枚目は全アルゴリズム比較、2枚目は逐次探索を除いた4つのアルゴリズムの比較としてください。

---

## 発展課題

### 発展課題1: Guess Race ゲーム

コンピュータが内部に秘密の数（1〜1000）を持ち、4つの探索アルゴリズム（逐次探索、二分探索、ジャンプ探索、指数探索）がそれぞれの戦略で数を当てるレースを作ってください。

**仕様:**
1. ランダムに秘密の数を決める
2. 各アルゴリズムが何回の「質問」（比較）で正解にたどり着くかをシミュレーションする
3. 結果を速い順にランキング表示する
4. 10回のレースを行い、各アルゴリズムの平均推測回数と勝率を表示する

---

### 発展課題2: オリジナル探索アルゴリズムの設計

ジャンプ探索と指数探索を組み合わせた、または改良した独自の探索アルゴリズムを設計・実装してください。

**仕様:**
1. 既存のアルゴリズムの良い点を組み合わせて独自アルゴリズムを実装する
2. 名前をつけて、どういう戦略なのかコメントで説明する
3. データ数10万件で5つの既存アルゴリズム+自作アルゴリズムのベンチマークを行う
4. 結果をランキング形式で表示する

---

## 解答例

### 標準課題1 解答

```python
# ============================================================
# 標準課題1 解答: bisect_leftで挿入位置を求める
# ============================================================

import bisect  # bisectモジュールをインポートする

data = [1, 3, 5, 7, 9, 11, 13]  # ソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

for target in [6, 4, 10]:  # 各targetについて挿入位置を求める
    pos = bisect.bisect_left(data, target)  # 挿入位置を計算する
    print(f"{target}を挿入するなら位置{pos}です")  # 結果を表示する
```

---

### 標準課題2 解答

```python
# ============================================================
# 標準課題2 解答: bisectで重複の個数を数える
# ============================================================

import bisect  # bisectモジュールをインポートする

data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5]  # 重複を含むソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

for target in [3, 1, 4, 6]:  # 各targetについて個数を求める
    left_pos = bisect.bisect_left(data, target)  # 左端の位置を求める
    right_pos = bisect.bisect_right(data, target)  # 右端+1の位置を求める
    count = right_pos - left_pos  # 差が個数になる
    print(f"target={target}: {count}個 (left={left_pos}, right={right_pos})")  # 結果を表示する
```

---

### 標準課題3 解答

```python
# ============================================================
# 標準課題3 解答: insortでランダム値を挿入する
# ============================================================

import bisect  # bisectモジュールをインポートする
import random  # ランダム値生成用モジュール

sorted_list = []  # 空のリストから始める
print("insort でランダム値をソート済みリストに挿入")  # タイトル
print("=" * 50)  # 区切り線

for i in range(10):  # 10個の値を挿入する
    value = random.randint(1, 100)  # 1〜100のランダム値を生成する
    bisect.insort(sorted_list, value)  # ソートを保ったまま挿入する
    print(f"  {i + 1}回目: insort({value:>3}) → {sorted_list}")  # 状態を表示する

# --- ソート済み確認 ---
is_sorted = all(sorted_list[i] <= sorted_list[i + 1] for i in range(len(sorted_list) - 1))  # ソート済みか確認する
print(f"\n最終結果: {sorted_list}")  # 最終結果を表示する
print(f"ソート済み: {is_sorted}")  # ソート済みかどうかを表示する
```

---

### 標準課題4 解答

```python
# ============================================================
# 標準課題4 解答: insortでリアルタイム中央値計算
# ============================================================

import bisect  # bisectモジュールをインポートする
import random  # ランダム値生成用モジュール

sorted_list = []  # 空のリストから始める
print("リアルタイム中央値計算")  # タイトル
print("=" * 60)  # 区切り線
print(f"{'#':>3}  {'挿入値':>6}  {'リスト':<30}  {'中央値':>6}")  # ヘッダー行
print("-" * 60)  # 区切り線

for i in range(20):  # 20個の値を挿入する
    value = random.randint(1, 50)  # 1〜50のランダム値を生成する
    bisect.insort(sorted_list, value)  # ソートを保ったまま挿入する

    # --- 中央値を計算する ---
    n = len(sorted_list)  # 現在の要素数を取得する
    if n % 2 == 1:  # 要素数が奇数の場合
        median = sorted_list[n // 2]  # 真ん中の値が中央値
    else:  # 要素数が偶数の場合
        median = (sorted_list[n // 2 - 1] + sorted_list[n // 2]) / 2  # 中央2つの平均

    # --- リストの表示（長い場合は省略する） ---
    list_str = str(sorted_list) if n <= 10 else f"[{sorted_list[0]}...{sorted_list[-1]}]({n}個)"  # 表示用文字列
    print(f"{i + 1:>3}  {value:>6}  {list_str:<30}  {median:>6.1f}")  # 結果を表示する
```

---

### 標準課題5 解答

```python
# ============================================================
# 標準課題5 解答: ジャンプ探索の実装
# ============================================================

import math  # 平方根計算用モジュール

def jump_search(data, target):  # ジャンプ探索関数
    """ジャンプ探索: sqrt(n)ずつジャンプしてブロックを特定し、ブロック内を逐次探索"""
    n = len(data)  # データの長さを取得する
    jump_size = int(math.sqrt(n))  # ジャンプ幅をsqrt(n)にする

    prev = 0  # ブロックの開始位置
    curr = 0  # 現在のジャンプ位置

    while curr < n and data[curr] < target:  # targetより小さい間ジャンプする
        prev = curr  # 前の位置を記憶する
        curr += jump_size  # ジャンプ幅分進む

    for i in range(prev, min(curr + 1, n)):  # ブロック内を逐次探索する
        if data[i] == target:  # 一致したら
            return i  # インデックスを返す
    return -1  # 見つからなかった

# --- テスト ---
data = list(range(1, 101))  # [1, 2, ..., 100]のリスト
print(f"データ数: {len(data)}個, ジャンプ幅: {int(math.sqrt(len(data)))}") # テスト条件
print("-" * 40)  # 区切り線

for target in [25, 50, 75, 100, 999]:  # テストする値のリスト
    result = jump_search(data, target)  # ジャンプ探索を実行する
    if result != -1:  # 見つかった場合
        print(f"target={target:>4}: インデックス{result}で発見")  # 結果を表示する
    else:  # 見つからなかった場合
        print(f"target={target:>4}: 見つかりませんでした")  # 見つからないと表示する
```

---

### 標準課題6 解答

```python
# ============================================================
# 標準課題6 解答: 3つのアルゴリズムの比較回数を比較する
# ============================================================

import math  # 平方根計算用モジュール

def linear_search_count(data, target):  # 逐次探索（比較回数付き）
    """逐次探索を実行し、比較回数を返す"""
    count = 0  # 比較回数カウンター
    for i in range(len(data)):  # 先頭から順に調べる
        count += 1  # 比較を1回カウント
        if data[i] == target:  # 一致したら
            return (i, count)  # 結果を返す
    return (-1, count)  # 見つからなかった場合

def binary_search_count(data, target):  # 二分探索（比較回数付き）
    """二分探索を実行し、比較回数を返す"""
    left = 0  # 左端
    right = len(data) - 1  # 右端
    count = 0  # 比較回数カウンター
    while left <= right:  # 範囲がある間
        count += 1  # 比較を1回カウント
        mid = (left + right) // 2  # 中央
        if data[mid] == target:  # 一致
            return (mid, count)  # 返す
        elif data[mid] < target:  # 小さい
            left = mid + 1  # 右へ
        else:  # 大きい
            right = mid - 1  # 左へ
    return (-1, count)  # 見つからない

def jump_search_count(data, target):  # ジャンプ探索（比較回数付き）
    """ジャンプ探索を実行し、比較回数を返す"""
    n = len(data)  # データの長さ
    jump_size = int(math.sqrt(n))  # ジャンプ幅
    count = 0  # 比較回数カウンター
    prev = 0  # ブロック開始位置
    curr = 0  # 現在位置

    while curr < n and data[curr] < target:  # ジャンプフェーズ
        count += 1  # 比較を1回カウント
        prev = curr  # 位置を記憶する
        curr += jump_size  # ジャンプする

    for i in range(prev, min(curr + 1, n)):  # ブロック内探索
        count += 1  # 比較を1回カウント
        if data[i] == target:  # 一致したら
            return (i, count)  # 返す
    return (-1, count)  # 見つからない

# --- テスト ---
data = list(range(1, 101))  # [1, 2, ..., 100]
print(f"データ数: {len(data)}個")  # データ数を表示する
print("-" * 55)  # 区切り線
print(f"{'target':>6}  {'逐次':>6}  {'二分':>6}  {'ジャンプ':>8}")  # ヘッダー行
print("-" * 55)  # 区切り線

for target in [1, 25, 50, 75, 100]:  # テストする値のリスト
    _, cnt_l = linear_search_count(data, target)  # 逐次探索の比較回数
    _, cnt_b = binary_search_count(data, target)  # 二分探索の比較回数
    _, cnt_j = jump_search_count(data, target)  # ジャンプ探索の比較回数
    print(f"{target:>6}  {cnt_l:>4}回  {cnt_b:>4}回  {cnt_j:>6}回")  # 結果を表示する
```

---

### 標準課題7 解答

```python
# ============================================================
# 標準課題7 解答: 指数探索の実装
# ============================================================

def exponential_search(data, target):  # 指数探索関数
    """指数探索: 指数的に範囲を広げてから二分探索"""
    n = len(data)  # データの長さを取得する
    if n == 0:  # 空リストの場合
        return -1  # -1を返す
    if data[0] == target:  # 先頭が一致する場合
        return 0  # 0を返す

    bound = 1  # 最初の境界値
    while bound < n and data[bound] < target:  # targetより小さい間
        bound *= 2  # 境界を2倍にする

    left = bound // 2  # 二分探索の左端
    right = min(bound, n - 1)  # 二分探索の右端

    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央を計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右へ
        else:  # 大きければ
            right = mid - 1  # 左へ
    return -1  # 見つからなかった

# --- テスト ---
data = list(range(1, 1001))  # [1, 2, ..., 1000]のリスト
print(f"データ数: {len(data)}個")  # データ数を表示する
print("-" * 40)  # 区切り線

for target in [1, 100, 500, 999, 2000]:  # テストする値のリスト
    result = exponential_search(data, target)  # 指数探索を実行する
    if result != -1:  # 見つかった場合
        print(f"target={target:>4}: インデックス{result}で発見")  # 結果を表示する
    else:  # 見つからなかった場合
        print(f"target={target:>4}: 見つかりませんでした")  # 見つからないと表示する
```

---

### 標準課題8 解答

```python
# ============================================================
# 標準課題8 解答: 指数探索のフェーズ別比較回数
# ============================================================

def exponential_search_detail(data, target):  # フェーズ別カウント付き指数探索
    """指数探索の各フェーズの比較回数を分けて返す"""
    n = len(data)  # データの長さ
    exp_count = 0  # 指数フェーズの比較回数
    bin_count = 0  # 二分探索フェーズの比較回数

    if n == 0:  # 空リストの場合
        return (-1, 0, 0)  # 見つからない

    if data[0] == target:  # 先頭が一致する場合
        return (0, 1, 0)  # 1回の比較で発見

    # --- 指数フェーズ ---
    bound = 1  # 最初の境界値
    while bound < n and data[bound] < target:  # targetより小さい間
        exp_count += 1  # 指数フェーズの比較回数を増やす
        bound *= 2  # 境界を2倍にする
    exp_count += 1  # 最後の比較もカウントする

    # --- 二分探索フェーズ ---
    left = bound // 2  # 左端
    right = min(bound, n - 1)  # 右端

    while left <= right:  # 範囲がある間
        bin_count += 1  # 二分探索の比較回数を増やす
        mid = (left + right) // 2  # 中央
        if data[mid] == target:  # 一致したら
            return (mid, exp_count, bin_count)  # 結果を返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右へ
        else:  # 大きければ
            right = mid - 1  # 左へ
    return (-1, exp_count, bin_count)  # 見つからなかった

# --- テスト ---
data = list(range(1, 1001))  # [1, 2, ..., 1000]
print(f"データ数: {len(data)}個")  # データ数を表示する
print("-" * 60)  # 区切り線
print(f"{'target':>6}  {'指数':>6}  {'二分':>6}  {'合計':>6}  {'結果':>8}")  # ヘッダー
print("-" * 60)  # 区切り線

for target in [1, 100, 500, 999]:  # テストする値のリスト
    idx, exp_c, bin_c = exponential_search_detail(data, target)  # 指数探索を実行する
    total = exp_c + bin_c  # 合計比較回数
    result_str = f"idx={idx}" if idx != -1 else "未発見"  # 結果文字列
    print(f"{target:>6}  {exp_c:>4}回  {bin_c:>4}回  {total:>4}回  {result_str:>8}")  # 表示する
```

---

### 標準課題9 解答

```python
# ============================================================
# 標準課題9 解答: 5つのアルゴリズムのベンチマーク
# ============================================================

import time  # 時間計測用モジュール
import random  # ランダム値生成用モジュール
import bisect  # bisectモジュール
import math  # 数学関数用モジュール

def linear_search(data, target):  # 逐次探索
    """逐次探索"""
    for i in range(len(data)):  # 先頭から順に調べる
        if data[i] == target:  # 一致したら
            return i  # 返す
    return -1  # 見つからない

def binary_search(data, target):  # 二分探索
    """二分探索"""
    left = 0  # 左端
    right = len(data) - 1  # 右端
    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央
        if data[mid] == target:  # 一致
            return mid  # 返す
        elif data[mid] < target:  # 小さい
            left = mid + 1  # 右へ
        else:  # 大きい
            right = mid - 1  # 左へ
    return -1  # 見つからない

def bisect_search(data, target):  # bisect探索
    """bisect探索"""
    idx = bisect.bisect_left(data, target)  # 挿入位置を求める
    if idx < len(data) and data[idx] == target:  # 一致確認
        return idx  # 返す
    return -1  # 見つからない

def jump_search(data, target):  # ジャンプ探索
    """ジャンプ探索"""
    n = len(data)  # データの長さ
    jump_size = int(math.sqrt(n))  # ジャンプ幅
    prev = 0  # ブロック開始
    curr = 0  # 現在位置
    while curr < n and data[curr] < target:  # ジャンプ
        prev = curr  # 記憶
        curr += jump_size  # 進む
    for i in range(prev, min(curr + 1, n)):  # ブロック内探索
        if data[i] == target:  # 一致
            return i  # 返す
    return -1  # 見つからない

def exponential_search(data, target):  # 指数探索
    """指数探索"""
    n = len(data)  # データの長さ
    if n == 0:  # 空
        return -1  # 返す
    if data[0] == target:  # 先頭一致
        return 0  # 返す
    bound = 1  # 境界
    while bound < n and data[bound] < target:  # 指数的に広げる
        bound *= 2  # 2倍
    left = bound // 2  # 左端
    right = min(bound, n - 1)  # 右端
    while left <= right:  # 二分探索
        mid = (left + right) // 2  # 中央
        if data[mid] == target:  # 一致
            return mid  # 返す
        elif data[mid] < target:  # 小さい
            left = mid + 1  # 右へ
        else:  # 大きい
            right = mid - 1  # 左へ
    return -1  # 見つからない

# --- ベンチマーク実行 ---
n = 100000  # データ数10万
data = list(range(n))  # ソート済みリスト
num_queries = 1000  # 探索回数
targets = [random.randint(0, n - 1) for _ in range(num_queries)]  # ランダムtarget

algorithms = [  # アルゴリズムのリスト
    ("Linear Search", linear_search),  # 逐次探索
    ("Binary Search", binary_search),  # 二分探索
    ("Bisect Search", bisect_search),  # bisect探索
    ("Jump Search", jump_search),  # ジャンプ探索
    ("Exponential", exponential_search),  # 指数探索
]

results = []  # 結果リスト
for name, func in algorithms:  # 各アルゴリズムをテストする
    start = time.perf_counter()  # 計測開始
    for t in targets:  # 各targetを探索する
        func(data, t)  # 探索実行
    elapsed = time.perf_counter() - start  # 経過時間
    results.append((name, elapsed))  # 結果を追加する

results.sort(key=lambda x: x[1])  # 速い順にソートする

print(f"探索アルゴリズム対決 (N={n:,}, クエリ={num_queries:,}回)")  # タイトル
print("=" * 50)  # 区切り線
for rank, (name, elapsed) in enumerate(results, 1):  # 順位をつけて表示する
    print(f"  {rank}位: {name:<18} {elapsed:.4f}秒")  # 結果を表示する
print("=" * 50)  # 区切り線
```

---

### 標準課題10 解答

```python
# ============================================================
# 標準課題10 解答: matplotlibで5つのアルゴリズムを比較するグラフ
# ============================================================

import time  # 時間計測用モジュール
import random  # ランダム値生成用モジュール
import bisect  # bisectモジュール
import math  # 数学関数用モジュール
import matplotlib.pyplot as plt  # グラフ描画用モジュール
import numpy as np  # 数値計算用モジュール

def linear_search(data, target):  # 逐次探索
    """逐次探索"""
    for i in range(len(data)):  # 順に調べる
        if data[i] == target:  # 一致
            return i  # 返す
    return -1  # 見つからない

def binary_search(data, target):  # 二分探索
    """二分探索"""
    left, right = 0, len(data) - 1  # 範囲設定
    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央
        if data[mid] == target: return mid  # 一致なら返す
        elif data[mid] < target: left = mid + 1  # 右へ
        else: right = mid - 1  # 左へ
    return -1  # 見つからない

def bisect_search(data, target):  # bisect探索
    """bisect探索"""
    idx = bisect.bisect_left(data, target)  # 挿入位置
    if idx < len(data) and data[idx] == target: return idx  # 一致なら返す
    return -1  # 見つからない

def jump_search(data, target):  # ジャンプ探索
    """ジャンプ探索"""
    n = len(data)  # データの長さ
    jump_size = int(math.sqrt(n))  # ジャンプ幅
    prev, curr = 0, 0  # 開始位置
    while curr < n and data[curr] < target:  # ジャンプ
        prev = curr  # 記憶
        curr += jump_size  # 進む
    for i in range(prev, min(curr + 1, n)):  # ブロック内
        if data[i] == target: return i  # 一致なら返す
    return -1  # 見つからない

def exponential_search(data, target):  # 指数探索
    """指数探索"""
    n = len(data)  # データの長さ
    if n == 0: return -1  # 空なら返す
    if data[0] == target: return 0  # 先頭一致
    bound = 1  # 境界
    while bound < n and data[bound] < target: bound *= 2  # 2倍に広げる
    left, right = bound // 2, min(bound, n - 1)  # 範囲
    while left <= right:  # 二分探索
        mid = (left + right) // 2  # 中央
        if data[mid] == target: return mid  # 一致
        elif data[mid] < target: left = mid + 1  # 右へ
        else: right = mid - 1  # 左へ
    return -1  # 見つからない

# --- ベンチマーク実行 ---
sizes = [1000, 10000, 100000]  # テストするデータサイズ
num_queries = 1000  # 探索回数

algorithms = [  # アルゴリズムリスト
    ("Linear", linear_search, "#e74c3c"),  # 逐次探索（赤）
    ("Binary", binary_search, "#3498db"),  # 二分探索（青）
    ("Bisect", bisect_search, "#2ecc71"),  # bisect（緑）
    ("Jump", jump_search, "#f39c12"),  # ジャンプ（オレンジ）
    ("Exponential", exponential_search, "#9b59b6"),  # 指数（紫）
]

all_times = {name: [] for name, _, _ in algorithms}  # 結果格納用辞書

for size in sizes:  # 各サイズでテストする
    data = list(range(size))  # ソート済みリスト
    targets = [random.randint(0, size - 1) for _ in range(num_queries)]  # ランダムtarget

    for name, func, _ in algorithms:  # 各アルゴリズム
        start = time.perf_counter()  # 計測開始
        for t in targets:  # 各target
            func(data, t)  # 探索実行
        elapsed = time.perf_counter() - start  # 経過時間
        all_times[name].append(elapsed)  # 結果を記録する

# --- グラフ1: 全アルゴリズム ---
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 2つのグラフを用意する
x = np.arange(len(sizes))  # X軸の位置
width = 0.15  # 棒の幅

ax1 = axes[0]  # 左のグラフ
for i, (name, _, color) in enumerate(algorithms):  # 各アルゴリズムの棒を描く
    ax1.bar(x + i * width, all_times[name], width, label=name, color=color)  # 棒グラフ
ax1.set_xlabel("Data Size")  # X軸ラベル
ax1.set_ylabel("Time (seconds)")  # Y軸ラベル
ax1.set_title("All Algorithms Comparison")  # タイトル
ax1.set_xticks(x + width * 2)  # 目盛り位置
ax1.set_xticklabels([f"{s // 1000}k" for s in sizes])  # ラベル
ax1.legend()  # 凡例
ax1.grid(axis="y", alpha=0.3)  # グリッド

# --- グラフ2: 逐次探索を除く ---
ax2 = axes[1]  # 右のグラフ
for i, (name, _, color) in enumerate(algorithms[1:]):  # 逐次探索以外
    ax2.bar(x + i * width, all_times[name], width, label=name, color=color)  # 棒グラフ
ax2.set_xlabel("Data Size")  # X軸ラベル
ax2.set_ylabel("Time (seconds)")  # Y軸ラベル
ax2.set_title("Without Linear Search")  # タイトル
ax2.set_xticks(x + width * 1.5)  # 目盛り位置
ax2.set_xticklabels([f"{s // 1000}k" for s in sizes])  # ラベル
ax2.legend()  # 凡例
ax2.grid(axis="y", alpha=0.3)  # グリッド

plt.tight_layout()  # レイアウト調整
plt.savefig("algorithm_comparison.png", dpi=150)  # ファイルに保存する
plt.show()  # グラフを表示する
print("グラフを algorithm_comparison.png に保存しました")  # 完了メッセージ
```

---

### 発展課題1 解答

```python
# ============================================================
# 発展課題1 解答: Guess Race ゲーム
# ============================================================

import random  # ランダム値生成用モジュール
import math  # 数学関数用モジュール

def linear_guess(secret, max_val):  # 逐次探索による推測
    """逐次探索: 1から順に試す"""
    for guess in range(1, max_val + 1):  # 1から順に試す
        if guess == secret:  # 正解なら
            return guess  # 推測回数（=値そのもの）を返す
    return max_val  # 最悪ケース

def binary_guess(secret, max_val):  # 二分探索による推測
    """二分探索: 半分ずつ絞り込む"""
    left = 1  # 左端
    right = max_val  # 右端
    count = 0  # 推測回数
    while left <= right:  # 範囲がある間
        count += 1  # 推測回数を増やす
        mid = (left + right) // 2  # 中央を計算する
        if mid == secret:  # 正解なら
            return count  # 推測回数を返す
        elif mid < secret:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return count  # 推測回数を返す

def jump_guess(secret, max_val):  # ジャンプ探索による推測
    """ジャンプ探索: sqrt(n)ずつジャンプ"""
    jump_size = int(math.sqrt(max_val))  # ジャンプ幅
    count = 0  # 推測回数
    prev = 1  # 前の位置
    curr = 1  # 現在位置
    while curr <= max_val and curr < secret:  # ジャンプフェーズ
        count += 1  # カウント
        prev = curr  # 位置を記憶
        curr += jump_size  # ジャンプ
    for i in range(prev, min(curr + 1, max_val + 1)):  # ブロック内探索
        count += 1  # カウント
        if i == secret:  # 正解なら
            return count  # 推測回数を返す
    return count  # 返す

def exponential_guess(secret, max_val):  # 指数探索による推測
    """指数探索: 指数的に範囲を広げてから二分探索"""
    count = 0  # 推測回数
    if secret == 1:  # 1なら即発見
        return 1  # 1回で見つかる
    bound = 1  # 境界
    while bound < max_val and bound < secret:  # 指数的に広げる
        count += 1  # カウント
        bound *= 2  # 2倍にする
    left = bound // 2  # 左端
    right = min(bound, max_val)  # 右端
    while left <= right:  # 二分探索
        count += 1  # カウント
        mid = (left + right) // 2  # 中央
        if mid == secret:  # 正解
            return count  # 返す
        elif mid < secret:  # 小さい
            left = mid + 1  # 右へ
        else:  # 大きい
            right = mid - 1  # 左へ
    return count  # 返す

# --- レース実行 ---
max_val = 1000  # 範囲は1〜1000
num_races = 10  # レース回数
wins = {"Linear": 0, "Binary": 0, "Jump": 0, "Exponential": 0}  # 勝利数
totals = {"Linear": 0, "Binary": 0, "Jump": 0, "Exponential": 0}  # 合計推測回数

print(f"Guess Race (範囲: 1〜{max_val}, {num_races}レース)")  # タイトル
print("=" * 60)  # 区切り線

for race in range(1, num_races + 1):  # 各レースを実行する
    secret = random.randint(1, max_val)  # 秘密の数を決める
    results = [  # 各アルゴリズムの結果
        ("Linear", linear_guess(secret, max_val)),  # 逐次
        ("Binary", binary_guess(secret, max_val)),  # 二分
        ("Jump", jump_guess(secret, max_val)),  # ジャンプ
        ("Exponential", exponential_guess(secret, max_val)),  # 指数
    ]
    results.sort(key=lambda x: x[1])  # 速い順にソートする
    wins[results[0][0]] += 1  # 1位のアルゴリズムの勝利数を増やす
    for name, count in results:  # 各アルゴリズムの合計を記録する
        totals[name] += count  # 合計に加算する

    print(f"Race {race:>2} (secret={secret:>4}): ", end="")  # レース番号表示
    for name, count in results:  # 結果を表示する
        print(f"{name}={count}回 ", end="")  # 各アルゴリズムの回数
    print()  # 改行

print("=" * 60)  # 区切り線
print("\n最終結果:")  # 最終結果ヘッダー
print(f"{'アルゴリズム':<15} {'勝利数':>6} {'平均推測回数':>12}")  # ヘッダー行
print("-" * 40)  # 区切り線
for name in ["Binary", "Exponential", "Jump", "Linear"]:  # 各アルゴリズム
    avg = totals[name] / num_races  # 平均推測回数を計算する
    print(f"{name:<15} {wins[name]:>4}勝  {avg:>10.1f}回")  # 結果を表示する
```

---

### 発展課題2 解答

```python
# ============================================================
# 発展課題2 解答: オリジナル探索アルゴリズム
# ============================================================

import time  # 時間計測用モジュール
import random  # ランダム値生成用モジュール
import bisect  # bisectモジュール
import math  # 数学関数用モジュール

# --- 既存アルゴリズム（省略版） ---
def linear_search(data, target):  # 逐次探索
    for i in range(len(data)):  # 順に調べる
        if data[i] == target: return i  # 一致なら返す
    return -1  # 見つからない

def binary_search(data, target):  # 二分探索
    left, right = 0, len(data) - 1  # 範囲
    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央
        if data[mid] == target: return mid  # 一致
        elif data[mid] < target: left = mid + 1  # 右
        else: right = mid - 1  # 左
    return -1  # 見つからない

def bisect_search(data, target):  # bisect探索
    idx = bisect.bisect_left(data, target)  # 挿入位置
    if idx < len(data) and data[idx] == target: return idx  # 一致
    return -1  # 見つからない

def jump_search(data, target):  # ジャンプ探索
    n = len(data)  # 長さ
    jump_size = int(math.sqrt(n))  # ジャンプ幅
    prev, curr = 0, 0  # 位置
    while curr < n and data[curr] < target: prev, curr = curr, curr + jump_size  # ジャンプ
    for i in range(prev, min(curr + 1, n)):  # ブロック内
        if data[i] == target: return i  # 一致
    return -1  # 見つからない

def exponential_search(data, target):  # 指数探索
    n = len(data)  # 長さ
    if n == 0: return -1  # 空
    if data[0] == target: return 0  # 先頭一致
    bound = 1  # 境界
    while bound < n and data[bound] < target: bound *= 2  # 広げる
    left, right = bound // 2, min(bound, n - 1)  # 範囲
    while left <= right:  # 二分探索
        mid = (left + right) // 2  # 中央
        if data[mid] == target: return mid  # 一致
        elif data[mid] < target: left = mid + 1  # 右
        else: right = mid - 1  # 左
    return -1  # 見つからない

# --- オリジナルアルゴリズム: ギャロッピングジャンプ探索 ---
def galloping_jump_search(data, target):  # ギャロッピングジャンプ探索
    """
    オリジナル: ギャロッピングジャンプ探索
    戦略: 最初は小さいジャンプで始め、targetが見つからない間
    ジャンプ幅を2倍に増やしていく（ギャロッピング）。
    ブロックを特定したら、そのブロック内で二分探索する。
    指数探索の「広げ方」とジャンプ探索の「ブロック探索」を組み合わせた手法。
    """
    n = len(data)  # データの長さを取得する
    if n == 0:  # 空リストの場合
        return -1  # -1を返す

    prev = 0  # 前のブロック開始位置
    jump = 1  # 最初のジャンプ幅は1

    # --- ギャロッピングフェーズ: ジャンプ幅を倍増させながらブロックを特定 ---
    curr = 0  # 現在位置
    while curr < n and data[curr] < target:  # targetより小さい間
        prev = curr  # 前の位置を記憶する
        curr = min(curr + jump, n - 1)  # ジャンプする（範囲外防止）
        jump *= 2  # ジャンプ幅を2倍にする
        if curr == n - 1:  # 末尾に到達した場合
            break  # ループを抜ける

    # --- ブロック内を二分探索する ---
    left = prev  # 左端
    right = min(curr, n - 1)  # 右端
    while left <= right:  # 範囲がある間
        mid = (left + right) // 2  # 中央を計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return -1  # 見つからなかった

# --- ベンチマーク ---
n = 100000  # データ数10万
data = list(range(n))  # ソート済みリスト
num_queries = 1000  # 探索回数
targets = [random.randint(0, n - 1) for _ in range(num_queries)]  # ランダムtarget

algorithms = [  # 全アルゴリズムのリスト
    ("Linear", linear_search),  # 逐次探索
    ("Binary", binary_search),  # 二分探索
    ("Bisect", bisect_search),  # bisect探索
    ("Jump", jump_search),  # ジャンプ探索
    ("Exponential", exponential_search),  # 指数探索
    ("GallopJump", galloping_jump_search),  # オリジナル
]

results = []  # 結果リスト
for name, func in algorithms:  # 各アルゴリズムをテストする
    start = time.perf_counter()  # 計測開始
    for t in targets:  # 各target
        func(data, t)  # 探索実行
    elapsed = time.perf_counter() - start  # 経過時間
    results.append((name, elapsed))  # 結果を追加する

results.sort(key=lambda x: x[1])  # 速い順にソートする

print(f"アルゴリズム対決（オリジナル含む）(N={n:,}, クエリ={num_queries:,}回)")  # タイトル
print("=" * 50)  # 区切り線
for rank, (name, elapsed) in enumerate(results, 1):  # 順位をつけて表示する
    marker = " ★" if name == "GallopJump" else ""  # オリジナルにマーク
    print(f"  {rank}位: {name:<18} {elapsed:.4f}秒{marker}")  # 結果を表示する
print("=" * 50)  # 区切り線
```
