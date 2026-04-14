# 第10回: 度数分布法（1）--- 分布数えソート

## 学習目標

- **分布数えソート**（Counting Sort）の考え方を理解する --- 比較を使わないソート！
- 度数配列・累積度数配列の作り方と使い方を習得する
- `matplotlib` でヒストグラム（度数分布図）を描画できる

---

## 1. 説明

### 1.1 これまでのソートとの違い

これまで学んだソートアルゴリズム（挿入ソート、バブルソートなど）は、
**要素同士を比較**して順序を決めていました。

```
比較ベースのソート: 「AとBはどちらが大きい？」を繰り返す
→ 最速でも O(n log n) が限界
```

分布数えソート（Counting Sort）は**比較を一切使いません**。
代わりに、**各値が何回出現するかを数える**ことでソートします。

```
分布数えソート: 「値0は何個？値1は何個？...」と数えて並べ直す
→ O(n + k) で動作（k は値の範囲）
```

### 1.2 分布数えソートの3ステップ

**ステップ1: 度数を数える（Count）**

各値が配列に何回出現するかを数えます。

```
入力: [4, 2, 2, 8, 3, 3, 1]
値の範囲: 0 ~ 8

度数配列 count:
index:  0  1  2  3  4  5  6  7  8
count: [0, 1, 2, 2, 1, 0, 0, 0, 1]
        ↑  ↑  ↑  ↑  ↑           ↑
        0個 1個 2個 2個 1個        1個
```

**ステップ2: 累積度数を計算する（Cumulative Count）**

度数配列を左から足し合わせて、各値の「出力位置」を決めます。

```
度数配列:   [0, 1, 2, 2, 1, 0, 0, 0, 1]
累積配列:   [0, 1, 3, 5, 6, 6, 6, 6, 7]
             ↑  ↑  ↑  ↑  ↑           ↑
             0個 1個 3個 5個 6個        7個（全要素数）

意味: 「値3以下の要素は5個ある」→ 値3は出力の4番目と5番目に入る
```

**ステップ3: 要素を正しい位置に配置する（Place）**

元の配列を**末尾から**走査し、累積度数を使って出力配列に配置します。

```
入力:     [4, 2, 2, 8, 3, 3, 1]
累積配列: [0, 1, 3, 5, 6, 6, 6, 6, 7]

末尾から処理:
  arr[6]=1 → cumulative[1]=1 → output[0]=1, cumulative[1]=0
  arr[5]=3 → cumulative[3]=5 → output[4]=3, cumulative[3]=4
  arr[4]=3 → cumulative[3]=4 → output[3]=3, cumulative[3]=3
  arr[3]=8 → cumulative[8]=7 → output[6]=8, cumulative[8]=6
  arr[2]=2 → cumulative[2]=3 → output[2]=2, cumulative[2]=2
  arr[1]=2 → cumulative[2]=2 → output[1]=2, cumulative[2]=1
  arr[0]=4 → cumulative[4]=6 → output[5]=4, cumulative[4]=5

出力: [1, 2, 2, 3, 3, 4, 8]
```

### 1.3 なぜ末尾から処理するのか？

末尾から処理すると、**同じ値の要素の元の順序が保たれます**（安定ソート）。
これは次回（第11回）で詳しく学びます。

### 1.4 計算量

| 操作 | 計算量 |
|------|--------|
| 度数を数える | O(n) |
| 累積度数を計算 | O(k) |
| 要素を配置 | O(n) |
| **合計** | **O(n + k)** |

- n: 要素数
- k: 値の範囲（最大値 - 最小値 + 1）
- k が小さければ（例: テストの点数 0~100）、非常に高速

---

## 2. 例題

### 例題1: リスト内の各値の出現回数を数える

```python
def count_occurrences(data):
    """リスト内の各値の出現回数を数えて度数配列を返す"""

    max_val = max(data)  # データの最大値を取得する
    count = [0] * (max_val + 1)  # 度数配列を0で初期化する

    for value in data:  # データを1つずつ走査する
        count[value] += 1  # 該当する値のカウントを1増やす

    return count  # 完成した度数配列を返す


# --- 実行 ---
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]  # テストデータを用意する
frequency = count_occurrences(data)  # 度数を数える

print(f"入力データ: {data}")  # 入力を表示する
print(f"度数配列:   {frequency}")  # 度数配列を表示する

for i, cnt in enumerate(frequency):  # 度数を1つずつ表示する
    if cnt > 0:  # 出現回数が0でないものだけ表示する
        print(f"  値 {i}: {cnt} 回")  # 値と回数を表示する
```

### 例題2: 度数配列から累積度数配列を作る

```python
def build_cumulative(count):
    """度数配列から累積度数配列を作成する"""

    cumulative = count[:]  # 度数配列をコピーする
    for i in range(1, len(cumulative)):  # 2番目の要素から順に処理する
        cumulative[i] = cumulative[i] + cumulative[i - 1]  # 前の要素を足し合わせる

    return cumulative  # 累積度数配列を返す


# --- 実行 ---
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]  # テストデータを用意する
max_val = max(data)  # 最大値を取得する
count = [0] * (max_val + 1)  # 度数配列を初期化する

for value in data:  # 度数を数える
    count[value] += 1  # カウントを増やす

cumulative = build_cumulative(count)  # 累積度数を計算する

print(f"度数配列:   {count}")  # 度数配列を表示する
print(f"累積度数:   {cumulative}")  # 累積度数配列を表示する

for i in range(len(cumulative)):  # 累積度数の意味を表示する
    if count[i] > 0:  # 出現する値だけ表示する
        print(f"  値 {i} 以下の要素数: {cumulative[i]}")  # 意味を説明する
```

### 例題3: 基本的な分布数えソート

```python
def counting_sort_basic(data):
    """分布数えソートの基本実装"""

    if len(data) <= 1:  # 要素が1個以下ならそのまま返す
        return data[:]  # コピーを返す

    max_val = max(data)  # 最大値を求める

    # --- ステップ1: 度数を数える ---
    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 各要素について処理する
        count[value] += 1  # 出現回数を加算する

    # --- ステップ2: 累積度数を計算する ---
    for i in range(1, len(count)):  # 先頭から順に足し合わせる
        count[i] += count[i - 1]  # 累積和を計算する

    # --- ステップ3: 出力配列に配置する ---
    output = [0] * len(data)  # 出力配列を初期化する
    for i in range(len(data) - 1, -1, -1):  # 末尾から走査する（安定ソート）
        value = data[i]  # 現在の値を取得する
        position = count[value] - 1  # 配置位置を決定する（0始まり）
        output[position] = value  # 出力配列に配置する
        count[value] -= 1  # 次の同じ値は1つ前に配置する

    return output  # ソート済み配列を返す


# --- 実行 ---
data = [4, 2, 2, 8, 3, 3, 1]  # テストデータを用意する
result = counting_sort_basic(data)  # 分布数えソートを実行する

print(f"入力: {data}")  # ソート前を表示する
print(f"出力: {result}")  # ソート後を表示する

assert result == sorted(data), "ソート結果が不正です"  # 正しさを検証する
print("検証OK: sorted() と同じ結果")  # 検証結果を表示する
```

### 例題4: テストの点数（0-100）を分布数えソートで並べ替える

```python
import random  # 乱数モジュールを読み込む

def sort_test_scores(scores):
    """テストの点数（0-100）を分布数えソートでソートする"""

    max_score = 100  # 点数の最大値を定義する

    # --- ステップ1: 度数を数える ---
    count = [0] * (max_score + 1)  # 0点から100点までの配列を用意する
    for score in scores:  # 各点数を走査する
        count[score] += 1  # 該当する点数のカウントを増やす

    # --- ステップ2: 累積度数を計算する ---
    for i in range(1, len(count)):  # 先頭から累積和を作る
        count[i] += count[i - 1]  # 前の値を足す

    # --- ステップ3: 出力配列に配置する ---
    output = [0] * len(scores)  # 出力配列を用意する
    for i in range(len(scores) - 1, -1, -1):  # 末尾から処理する
        score = scores[i]  # 現在の点数を取得する
        position = count[score] - 1  # 配置位置を計算する
        output[position] = score  # 配置する
        count[score] -= 1  # カウントを減らす

    return output  # ソート済みの点数を返す


# --- 実行 ---
random.seed(42)  # 再現性のためシードを固定する
num_students = 100  # 生徒数を設定する
scores = [random.randint(0, 100) for _ in range(num_students)]  # ランダムに点数を生成する

sorted_scores = sort_test_scores(scores)  # ソートを実行する

print(f"生徒数: {num_students}")  # 生徒数を表示する
print(f"ソート前（先頭10人）: {scores[:10]}")  # ソート前を表示する
print(f"ソート後（先頭10人）: {sorted_scores[:10]}")  # ソート後（低い順）を表示する
print(f"ソート後（末尾10人）: {sorted_scores[-10:]}")  # ソート後（高い順）を表示する

total = sum(sorted_scores)  # 合計点を計算する
average = total / num_students  # 平均点を計算する
print(f"平均点: {average:.1f}")  # 平均点を表示する
print(f"最低点: {sorted_scores[0]}")  # 最低点を表示する
print(f"最高点: {sorted_scores[-1]}")  # 最高点を表示する
```

### 例題5: 分布数えソートと挿入ソートの速度比較

```python
import time  # 時間計測モジュールを読み込む
import random  # 乱数モジュールを読み込む

def counting_sort(data, max_val):
    """分布数えソート（整数専用）"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[value] += 1  # カウントを増やす
    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る
    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        output[count[data[i]] - 1] = data[i]  # 正しい位置に置く
        count[data[i]] -= 1  # カウントを減らす
    return output  # ソート結果を返す


def insertion_sort(data):
    """挿入ソート"""

    arr = data[:]  # 配列をコピーする
    for i in range(1, len(arr)):  # 2番目の要素から処理する
        key = arr[i]  # 挿入する値を保存する
        j = i - 1  # 比較位置を設定する
        while j >= 0 and arr[j] > key:  # 左側の大きい値をずらす
            arr[j + 1] = arr[j]  # 1つ右にずらす
            j -= 1  # 比較位置を左に移動する
        arr[j + 1] = key  # 正しい位置に挿入する
    return arr  # ソート結果を返す


# --- 速度比較 ---
random.seed(42)  # シードを固定する
sizes = [1000, 5000, 10000]  # テストするデータサイズ
max_val = 100  # 値の範囲（0-100）

print(f"値の範囲: 0 ~ {max_val}")  # 条件を表示する
print(f"{'サイズ':>8} {'分布数えソート':>14} {'挿入ソート':>12} {'速度比':>8}")  # ヘッダー
print("-" * 50)  # 区切り線を表示する

for size in sizes:  # 各サイズで計測する
    data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する

    start = time.time()  # 計測開始
    counting_sort(data, max_val)  # 分布数えソートを実行する
    counting_time = time.time() - start  # 経過時間を記録する

    start = time.time()  # 計測開始
    insertion_sort(data)  # 挿入ソートを実行する
    insertion_time = time.time() - start  # 経過時間を記録する

    ratio = insertion_time / counting_time if counting_time > 0 else 0  # 速度比を計算する
    print(f"{size:>8} {counting_time:>13.4f}s {insertion_time:>11.4f}s {ratio:>7.1f}x")  # 結果を表示する
```

---

## 3. 標準課題

### 標準課題1（超やさしい）: リスト内の文字の出現回数を数える

文字のリスト `["a", "b", "a", "c", "b", "a", "d", "c"]` の各文字の出現回数を数えて表示してください。

**要件:**
- 辞書（dict）を使って各文字の出現回数を記録する
- 出現回数が多い順に表示する

### 標準課題2（超やさしい）: 度数分布表を作成する

1~6の目が出るサイコロを100回振ったデータ `[random.randint(1, 6) for _ in range(100)]` に対して度数分布表を作成し、棒グラフ風にテキスト表示してください。

**要件:**
- 度数配列を作成する
- 各目の出現回数を `*` で棒グラフ風に表示する
- 合計が100であることを確認する

### 標準課題3（やさしい）: 累積度数から順位を計算する

10人分のテスト点数 `[72, 85, 60, 91, 85, 72, 45, 91, 60, 78]` に対して度数配列と累積度数配列を作り、各点数の順位を求めてください。

**要件:**
- 度数配列と累積度数配列を作成する
- 累積度数を使って「その点数以下の人数」を表示する
- 高得点順の順位（1位が最高点）を計算して表示する

### 標準課題4（やさしい）: 累積度数で偏差値の区間人数を求める

50人分のテスト点数（0-100）をランダム生成し、累積度数を使って各10点区間（0-9, 10-19, ..., 90-100）の人数を計算してください。

**要件:**
- 累積度数配列を作成する
- `累積度数[上限] - 累積度数[下限-1]` で区間人数を計算する
- 各区間の人数をテキスト表形式で表示する

### 標準課題5（やややさしい）: 小さな配列を分布数えソートで並べ替える

配列 `[3, 6, 4, 1, 3, 4, 1, 4]` を分布数えソートでソートし、各ステップ（度数→累積度数→配置）の途中経過を表示してください。

**要件:**
- 度数配列の作成過程を表示する
- 累積度数配列の作成過程を表示する
- 末尾からの配置過程を1要素ずつ表示する
- 最終結果が `sorted()` と一致することを検証する

### 標準課題6（やややさしい）: 分布数えソートのステップをトレースする

配列 `[5, 3, 8, 1, 3, 7, 2, 5, 1, 8]` に対して、分布数えソートの全ステップをトレースし、末尾から配置するときの累積度数配列の変化を表形式で表示してください。

**要件:**
- 配置のたびに累積度数配列の状態を表示する
- 出力配列の変化も同時に表示する
- 処理順序（末尾から）を明記する

### 標準課題7（やや普通）: 100人分のテスト点数をソートして統計を出す

100人分のテスト点数（0-100）をランダム生成し、分布数えソートでソート後、平均点・中央値・最頻値・最高点・最低点を計算してください。

**要件:**
- `random.seed(42)` で再現性を確保する
- ソート前後を表示する（先頭10人・末尾10人）
- 度数配列から最頻値（最も多い点数）を求める
- 中央値を正しく計算する（偶数個の場合は中央2つの平均）

### 標準課題8（やや普通）: テスト点数の度数分布をヒストグラムで可視化する

課題7のデータを `matplotlib` でヒストグラムとして描画し、平均点の縦線と各区間の人数ラベルを追加してください。

**要件:**
- 10点刻みで集計する（0-9, 10-19, ..., 90-100）
- 各バーの上に人数を表示する
- 平均点を赤い破線で表示する
- グラフにタイトル・軸ラベル・凡例を付ける

### 標準課題9（普通）: 分布数えソートと挿入ソートのベンチマーク

データサイズ 1000, 5000, 10000, 50000 で、分布数えソートと挿入ソートの速度を比較し、`matplotlib` でグラフ化してください。

**要件:**
- 値の範囲は 0-100
- 各サイズで3回計測して平均を取る
- 棒グラフで比較する
- 速度比（挿入ソートの時間 / 分布数えソートの時間）も表示する

### 標準課題10（普通）: 分布数えソートの計算量 O(n+k) を実験で分析する

分布数えソートの計算量が O(n+k) であることを実験で示してください。

**要件:**
- 実験1: n を変化させて k を固定（k=100、n=1000,5000,10000,50000,100000）
- 実験2: k を変化させて n を固定（n=10000、k=10,100,1000,10000,100000）
- 各条件で実行時間を計測する
- 2つのグラフを描画して O(n+k) の理論通りか考察する

---

## 4. 発展課題

### 発展課題1: 文字列を長さ順に分布数えソートする

文字列のリストを「文字列の長さ」をキーにして分布数えソートで並べ替えてください。

**要件:**
- 入力: `["apple", "hi", "cat", "elephant", "go", "python", "a", "dog", "wonderful"]`
- 文字列の長さを整数キーとして分布数えソートを適用する
- 同じ長さの文字列は元の順序を保つ（安定ソート）
- ソート結果を表示する

### 発展課題2: matplotlib でカラフルなヒストグラムを作成する

200人分のテスト点数を生成し、`matplotlib` で以下の機能を持つヒストグラムを描画してください。

**要件:**
- 10点刻みの区間ごとに異なる色を使う（0-59: 赤系、60-79: 黄系、80-100: 青系）
- 平均点・中央値の縦線を追加する（それぞれ色を変える）
- 各バーの上に人数を表示する
- 合格ライン（60点）を破線で表示する

---

## 5. 解答例

### 課題1の解答例

```python
def count_characters(char_list):
    """文字リストの各文字の出現回数を数える"""

    frequency = {}  # 空の辞書を用意する
    for char in char_list:  # リストの各文字を走査する
        if char in frequency:  # すでに辞書にある場合
            frequency[char] += 1  # カウントを1増やす
        else:  # 初めて出現した場合
            frequency[char] = 1  # カウントを1に設定する

    return frequency  # 度数辞書を返す


# --- 実行 ---
data = ["a", "b", "a", "c", "b", "a", "d", "c"]  # テストデータ
result = count_characters(data)  # 出現回数を数える

print(f"入力: {data}")  # 入力を表示する
print(f"出現回数: {result}")  # 辞書を表示する

# --- 出現回数が多い順に表示する ---
sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)  # 回数で降順ソート
for char, cnt in sorted_items:  # 1つずつ表示する
    print(f"  '{char}': {cnt} 回")  # 文字と回数を表示する
```

### 課題2の解答例

```python
import random  # 乱数モジュールを読み込む

def dice_frequency_table(rolls):
    """サイコロの出目の度数分布表を作成する"""

    count = [0] * 7  # インデックス0-6（0は使わない）を用意する
    for value in rolls:  # 各出目を走査する
        count[value] += 1  # 該当する目のカウントを増やす

    return count  # 度数配列を返す


# --- 実行 ---
random.seed(42)  # シードを固定する
num_rolls = 100  # 試行回数を設定する
rolls = [random.randint(1, 6) for _ in range(num_rolls)]  # サイコロを振る

count = dice_frequency_table(rolls)  # 度数を集計する

print(f"サイコロを {num_rolls} 回振った結果:")  # タイトルを表示する
print("-" * 30)  # 区切り線を表示する

total = 0  # 合計を初期化する
for face in range(1, 7):  # 1から6まで処理する
    bar = "*" * count[face]  # 棒グラフ文字列を作る
    print(f"  目 {face}: {bar} ({count[face]}回)")  # 出目と回数を表示する
    total += count[face]  # 合計に加算する

print("-" * 30)  # 区切り線を表示する
print(f"  合計: {total} 回")  # 合計を表示する
assert total == num_rolls, "合計が一致しません"  # 合計を検証する
print("検証OK: 合計は100回")  # 検証結果を表示する
```

### 課題3の解答例

```python
def calculate_rank(scores):
    """テスト点数から度数・累積度数・順位を計算する"""

    max_score = max(scores)  # 最高点を取得する

    # --- 度数配列を作成する ---
    count = [0] * (max_score + 1)  # 度数配列を初期化する
    for score in scores:  # 各点数を走査する
        count[score] += 1  # カウントを増やす

    # --- 累積度数配列を作成する ---
    cumulative = count[:]  # 度数配列をコピーする
    for i in range(1, len(cumulative)):  # 先頭から順に足す
        cumulative[i] += cumulative[i - 1]  # 累積和を計算する

    # --- 各点数の順位を計算する ---
    num_students = len(scores)  # 全生徒数を取得する
    print(f"生徒数: {num_students}")  # 生徒数を表示する
    print(f"点数データ: {scores}")  # データを表示する
    print()  # 空行を出力する

    print(f"{'点数':>4} {'度数':>4} {'累積度数':>6} {'以下人数':>6} {'順位':>4}")  # ヘッダー
    print("-" * 30)  # 区切り線を表示する

    shown = set()  # 表示済みの点数を記録する
    for score in sorted(set(scores), reverse=True):  # 高い順に表示する
        below_count = cumulative[score]  # その点数以下の人数を取得する
        rank = num_students - below_count + 1  # 順位を計算する
        print(f"{score:>4} {count[score]:>4} {cumulative[score]:>6} {below_count:>6} {rank:>4}")  # 表示する


# --- 実行 ---
scores = [72, 85, 60, 91, 85, 72, 45, 91, 60, 78]  # テストデータ
calculate_rank(scores)  # 順位を計算する
```

### 課題4の解答例

```python
import random  # 乱数モジュールを読み込む

def interval_counts(scores, interval_size):
    """累積度数を使って各区間の人数を計算する"""

    max_score = 100  # 最高点を定義する

    # --- 度数配列を作成する ---
    count = [0] * (max_score + 1)  # 度数配列を初期化する
    for score in scores:  # 各点数を走査する
        count[score] += 1  # カウントを増やす

    # --- 累積度数配列を作成する ---
    cumulative = [0] * (max_score + 1)  # 累積度数配列を初期化する
    cumulative[0] = count[0]  # 最初の値を設定する
    for i in range(1, len(cumulative)):  # 先頭から順に計算する
        cumulative[i] = cumulative[i - 1] + count[i]  # 累積和を作る

    # --- 各区間の人数を計算する ---
    print(f"{'区間':>8} {'人数':>4}")  # ヘッダーを表示する
    print("-" * 16)  # 区切り線を表示する

    total = 0  # 合計を初期化する
    lower = 0  # 区間の下限を設定する
    while lower <= max_score:  # 全区間を処理する
        upper = min(lower + interval_size - 1, max_score)  # 区間の上限を計算する
        if lower == 0:  # 最初の区間の場合
            num_people = cumulative[upper]  # 累積度数をそのまま使う
        else:  # それ以外の区間の場合
            num_people = cumulative[upper] - cumulative[lower - 1]  # 差を計算する
        print(f"{lower:>3}-{upper:>3}点 {num_people:>4}人")  # 区間と人数を表示する
        total += num_people  # 合計に加算する
        lower += interval_size  # 次の区間へ進む

    print("-" * 16)  # 区切り線を表示する
    print(f"{'合計':>8} {total:>4}人")  # 合計を表示する


# --- 実行 ---
random.seed(42)  # シードを固定する
scores = [random.randint(0, 100) for _ in range(50)]  # 50人分の点数を生成する
interval_counts(scores, 10)  # 10点刻みで集計する
```

### 課題5の解答例

```python
def counting_sort_with_trace(data):
    """分布数えソートの各ステップを表示する"""

    print(f"入力配列: {data}")  # 入力を表示する
    max_val = max(data)  # 最大値を求める

    # --- ステップ1: 度数を数える ---
    print("\n【ステップ1: 度数を数える】")  # ステップ名を表示する
    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for i, value in enumerate(data):  # 各要素を走査する
        count[value] += 1  # カウントを増やす
        print(f"  data[{i}]={value} → count={count}")  # 途中経過を表示する

    # --- ステップ2: 累積度数を計算する ---
    print("\n【ステップ2: 累積度数を計算する】")  # ステップ名を表示する
    for i in range(1, len(count)):  # 先頭から順に足す
        old_val = count[i]  # 変更前の値を保存する
        count[i] += count[i - 1]  # 累積和を計算する
        print(f"  count[{i}] = {old_val} + {count[i - 1] - old_val} = {count[i]}")  # 計算過程を表示する
    print(f"  累積度数: {count}")  # 完成した累積度数を表示する

    # --- ステップ3: 末尾から配置する ---
    print("\n【ステップ3: 末尾から配置する】")  # ステップ名を表示する
    output = [None] * len(data)  # 出力配列を初期化する
    for i in range(len(data) - 1, -1, -1):  # 末尾から処理する
        value = data[i]  # 現在の値を取得する
        position = count[value] - 1  # 配置位置を決定する
        output[position] = value  # 出力配列に配置する
        count[value] -= 1  # カウントを減らす
        print(f"  data[{i}]={value} → 位置{position} → output={output}")  # 配置過程を表示する

    print(f"\n出力配列: {output}")  # 最終結果を表示する

    assert output == sorted(data), "ソート結果が不正です"  # 検証する
    print("検証OK: sorted() と一致")  # 検証結果を表示する
    return output  # 結果を返す


# --- 実行 ---
counting_sort_with_trace([3, 6, 4, 1, 3, 4, 1, 4])  # テストデータでソートする
```

### 課題6の解答例

```python
def counting_sort_trace_table(data):
    """分布数えソートの配置ステップを表形式でトレースする"""

    print(f"入力配列: {data}")  # 入力を表示する
    max_val = max(data)  # 最大値を求める

    # --- 度数配列を作成する ---
    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[value] += 1  # カウントを増やす
    print(f"度数配列: {count}")  # 度数配列を表示する

    # --- 累積度数を計算する ---
    cumulative = count[:]  # コピーする
    for i in range(1, len(cumulative)):  # 累積和を作る
        cumulative[i] += cumulative[i - 1]  # 前の値を足す
    print(f"累積度数: {cumulative}")  # 累積度数を表示する

    # --- 配置ステップを表形式で表示する ---
    print("\n【配置ステップ（末尾から処理）】")  # タイトルを表示する
    header_indices = "  ".join([f"c[{i}]" for i in range(max_val + 1)])  # ヘッダーを作る
    print(f"{'処理':>12} {'値':>3} {'位置':>4}  累積度数: {header_indices}  出力配列")  # ヘッダー表示
    print("-" * 80)  # 区切り線を表示する

    output = [None] * len(data)  # 出力配列を初期化する
    for i in range(len(data) - 1, -1, -1):  # 末尾から処理する
        value = data[i]  # 現在の値を取得する
        position = cumulative[value] - 1  # 配置位置を決定する
        output[position] = value  # 配置する
        cumulative[value] -= 1  # カウントを減らす

        cum_str = "  ".join([f"{c:>3}" for c in cumulative])  # 累積度数を文字列にする
        out_str = str(output)  # 出力配列を文字列にする
        print(f"  data[{i}]  {value:>3} {position:>4}  累積度数: {cum_str}  {out_str}")  # 1行表示する

    print(f"\n最終結果: {output}")  # 最終結果を表示する
    return output  # 結果を返す


# --- 実行 ---
counting_sort_trace_table([5, 3, 8, 1, 3, 7, 2, 5, 1, 8])  # テストデータでトレースする
```

### 課題7の解答例

```python
import random  # 乱数モジュールを読み込む

def sort_and_statistics(scores):
    """分布数えソートでソートし統計情報を計算する"""

    max_score = 100  # 最高点を定義する
    num_students = len(scores)  # 生徒数を取得する

    # --- 分布数えソート ---
    count = [0] * (max_score + 1)  # 度数配列を初期化する
    for score in scores:  # 度数を数える
        count[score] += 1  # カウントを増やす

    count_copy = count[:]  # 統計用に度数配列をコピーする

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [0] * num_students  # 出力配列を用意する
    for i in range(num_students - 1, -1, -1):  # 末尾から配置する
        score = scores[i]  # 点数を取得する
        position = count[score] - 1  # 位置を決定する
        output[position] = score  # 配置する
        count[score] -= 1  # カウントを減らす

    # --- 統計情報を計算する ---
    total = sum(output)  # 合計を計算する
    average = total / num_students  # 平均を計算する
    lowest = output[0]  # 最低点を取得する
    highest = output[-1]  # 最高点を取得する

    # --- 中央値を計算する ---
    mid = num_students // 2  # 中央のインデックスを計算する
    if num_students % 2 == 0:  # 偶数人の場合
        median = (output[mid - 1] + output[mid]) / 2  # 中央2つの平均
    else:  # 奇数人の場合
        median = output[mid]  # 中央の値

    # --- 最頻値を計算する ---
    max_count = max(count_copy)  # 最大の度数を取得する
    mode = [i for i, c in enumerate(count_copy) if c == max_count]  # 最頻値を求める

    # --- 結果を表示する ---
    print(f"生徒数: {num_students}")  # 生徒数を表示する
    print(f"\nソート前（先頭10人）: {scores[:10]}")  # ソート前を表示する
    print(f"ソート前（末尾10人）: {scores[-10:]}")  # ソート前を表示する
    print(f"\nソート後（先頭10人）: {output[:10]}")  # 低い順を表示する
    print(f"ソート後（末尾10人）: {output[-10:]}")  # 高い順を表示する
    print(f"\n--- 統計情報 ---")  # タイトルを表示する
    print(f"平均点: {average:.1f}")  # 平均点を表示する
    print(f"中央値: {median:.1f}")  # 中央値を表示する
    print(f"最頻値: {mode}（{max_count}回出現）")  # 最頻値を表示する
    print(f"最高点: {highest}")  # 最高点を表示する
    print(f"最低点: {lowest}")  # 最低点を表示する

    return output  # ソート結果を返す


# --- 実行 ---
random.seed(42)  # シードを固定する
scores = [random.randint(0, 100) for _ in range(100)]  # 100人分の点数を生成する
sort_and_statistics(scores)  # ソートと統計を実行する
```

### 課題8の解答例

```python
import random  # 乱数モジュールを読み込む
import matplotlib.pyplot as plt  # グラフ描画モジュールを読み込む

def draw_score_histogram(scores):
    """テスト点数のヒストグラムを描画する"""

    # --- 10点刻みで度数を集計する ---
    bins = list(range(0, 101, 10))  # 区間の境界を作る
    bin_labels = []  # 区間ラベルのリスト
    bin_counts = []  # 区間の度数リスト

    for i in range(len(bins) - 1):  # 各区間を処理する
        lower = bins[i]  # 下限を取得する
        upper = bins[i + 1]  # 上限を取得する

        if i == len(bins) - 2:  # 最後の区間（90-100）の場合
            cnt = sum(1 for s in scores if lower <= s <= upper)  # 上限含む
            label = f"{lower}-{upper}"  # ラベルを作る
        else:  # 他の区間の場合
            cnt = sum(1 for s in scores if lower <= s < upper)  # 上限含まない
            label = f"{lower}-{upper - 1}"  # ラベルを作る

        bin_labels.append(label)  # ラベルを追加する
        bin_counts.append(cnt)  # 度数を追加する

    # --- 平均点を計算する ---
    average = sum(scores) / len(scores)  # 平均点を計算する

    # --- グラフを描画する ---
    fig, ax = plt.subplots(figsize=(12, 6))  # 図を作成する

    bar_colors = ["#3498db"] * len(bin_labels)  # バーの色を設定する
    bars = ax.bar(bin_labels, bin_counts, color=bar_colors, edgecolor="white", linewidth=1.2)  # バーを描画する

    for bar, cnt in zip(bars, bin_counts):  # 各バーの上に数値を表示する
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # バーの中央X座標
            bar.get_height() + 0.3,  # バーの上に少し余白
            str(cnt),  # 表示する数値
            ha="center",  # 水平中央揃え
            va="bottom",  # 下揃え
            fontsize=11,  # フォントサイズ
            fontweight="bold",  # 太字
        )

    # --- 平均点の縦線を追加する ---
    ax.axvline(
        x=average / 10 - 0.5,  # バーの位置に合わせる
        color="red",  # 赤色
        linestyle="--",  # 破線
        linewidth=2,  # 線の太さ
        label=f"平均点: {average:.1f}",  # 凡例テキスト
    )

    ax.set_xlabel("点数の範囲", fontsize=13)  # X軸ラベルを設定する
    ax.set_ylabel("人数", fontsize=13)  # Y軸ラベルを設定する
    ax.set_title("テスト点数の度数分布（100人）", fontsize=15)  # タイトルを設定する
    ax.legend(fontsize=12)  # 凡例を表示する
    ax.set_ylim(0, max(bin_counts) + 3)  # Y軸の範囲を設定する
    plt.tight_layout()  # レイアウトを調整する
    plt.show()  # グラフを表示する


# --- 実行 ---
random.seed(42)  # シードを固定する
scores = [random.randint(0, 100) for _ in range(100)]  # 100人分の点数を生成する
draw_score_histogram(scores)  # ヒストグラムを描画する
```

### 課題9の解答例

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む
import matplotlib.pyplot as plt  # グラフ描画モジュールを読み込む

def counting_sort_bench(data, max_val):
    """ベンチマーク用の分布数えソート"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[value] += 1  # カウントを増やす
    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る
    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        output[count[data[i]] - 1] = data[i]  # 配置する
        count[data[i]] -= 1  # カウントを減らす
    return output  # ソート結果を返す


def insertion_sort_bench(data):
    """ベンチマーク用の挿入ソート"""

    arr = data[:]  # コピーする
    for i in range(1, len(arr)):  # 2番目から処理する
        key = arr[i]  # 挿入する値を保存する
        j = i - 1  # 比較位置を設定する
        while j >= 0 and arr[j] > key:  # 左の大きい値をずらす
            arr[j + 1] = arr[j]  # 右にずらす
            j -= 1  # 左に進む
        arr[j + 1] = key  # 挿入する
    return arr  # ソート結果を返す


def measure_time(sort_func, data, trials=3):
    """ソート関数の平均実行時間を計測する"""

    times = []  # 計測結果のリスト
    for _ in range(trials):  # 指定回数繰り返す
        arr_copy = data[:]  # データをコピーする
        start = time.time()  # 計測開始
        sort_func(arr_copy)  # ソートを実行する
        elapsed = time.time() - start  # 経過時間を計算する
        times.append(elapsed)  # 結果を記録する
    return sum(times) / len(times)  # 平均を返す


# --- ベンチマーク実行 ---
random.seed(42)  # シードを固定する
sizes = [1000, 5000, 10000, 50000]  # テストするデータサイズ
max_val = 100  # 値の範囲

counting_times = []  # 分布数えソートの時間を記録するリスト
insertion_times = []  # 挿入ソートの時間を記録するリスト

print(f"値の範囲: 0 ~ {max_val}、各サイズ3回計測の平均")  # 条件を表示する
print(f"{'サイズ':>8} {'分布数えソート':>14} {'挿入ソート':>12} {'速度比':>8}")  # ヘッダー
print("-" * 50)  # 区切り線

for size in sizes:  # 各サイズで計測する
    data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する

    ct = measure_time(lambda d: counting_sort_bench(d, max_val), data)  # 分布数えソートを計測する
    counting_times.append(ct)  # 結果を記録する

    it = measure_time(insertion_sort_bench, data)  # 挿入ソートを計測する
    insertion_times.append(it)  # 結果を記録する

    ratio = it / ct if ct > 0 else 0  # 速度比を計算する
    print(f"{size:>8} {ct:>13.4f}s {it:>11.4f}s {ratio:>7.1f}x")  # 結果を表示する

# --- グラフを描画する ---
fig, ax = plt.subplots(figsize=(10, 6))  # 図を作成する
x_pos = range(len(sizes))  # X座標を設定する
bar_width = 0.35  # バーの幅を設定する

bars1 = ax.bar([x - bar_width / 2 for x in x_pos], counting_times, bar_width,
               label="分布数えソート", color="#3498db")  # 分布数えソートのバー
bars2 = ax.bar([x + bar_width / 2 for x in x_pos], insertion_times, bar_width,
               label="挿入ソート", color="#e74c3c")  # 挿入ソートのバー

for bar, t in zip(bars1, counting_times):  # 分布数えソートの数値表示
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{t:.4f}s", ha="center", va="bottom", fontsize=9)  # バーの上に表示する
for bar, t in zip(bars2, insertion_times):  # 挿入ソートの数値表示
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{t:.4f}s", ha="center", va="bottom", fontsize=9)  # バーの上に表示する

ax.set_xlabel("データサイズ", fontsize=13)  # X軸ラベル
ax.set_ylabel("平均実行時間（秒）", fontsize=13)  # Y軸ラベル
ax.set_title("分布数えソート vs 挿入ソート", fontsize=14)  # タイトル
ax.set_xticks(list(x_pos))  # X軸目盛り位置
ax.set_xticklabels([f"{s:,}" for s in sizes])  # X軸ラベル
ax.legend(fontsize=12)  # 凡例を表示する
ax.grid(axis="y", alpha=0.3)  # Y軸グリッドを表示する
plt.tight_layout()  # レイアウトを調整する
plt.show()  # グラフを表示する
```

### 課題10の解答例

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む
import matplotlib.pyplot as plt  # グラフ描画モジュールを読み込む

def counting_sort_nk(data, max_val):
    """分布数えソート（計算量分析用）"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[value] += 1  # カウントを増やす
    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る
    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        output[count[data[i]] - 1] = data[i]  # 配置する
        count[data[i]] -= 1  # カウントを減らす
    return output  # ソート結果を返す


def measure_avg(sort_func, data, max_val, trials=3):
    """平均実行時間を計測する"""

    times = []  # 結果リスト
    for _ in range(trials):  # 指定回数繰り返す
        arr_copy = data[:]  # コピーする
        start = time.time()  # 計測開始
        sort_func(arr_copy, max_val)  # ソートを実行する
        times.append(time.time() - start)  # 時間を記録する
    return sum(times) / len(times)  # 平均を返す


# ===== 実験1: n を変化、k を固定 =====
print("【実験1】n を変化させる（k = 100 固定）")  # タイトルを表示する
print("=" * 40)  # 区切り線

k_fixed = 100  # k を固定する
n_values = [1000, 5000, 10000, 50000, 100000]  # n のリスト
times_exp1 = []  # 計測結果リスト

for n in n_values:  # 各 n で計測する
    data = [random.randint(0, k_fixed) for _ in range(n)]  # データを生成する
    t = measure_avg(counting_sort_nk, data, k_fixed)  # 時間を計測する
    times_exp1.append(t)  # 結果を記録する
    print(f"  n={n:>7}, k={k_fixed}: {t:.6f} 秒")  # 結果を表示する

# ===== 実験2: k を変化、n を固定 =====
print("\n【実験2】k を変化させる（n = 10000 固定）")  # タイトルを表示する
print("=" * 40)  # 区切り線

n_fixed = 10000  # n を固定する
k_values = [10, 100, 1000, 10000, 100000]  # k のリスト
times_exp2 = []  # 計測結果リスト

for k in k_values:  # 各 k で計測する
    data = [random.randint(0, k) for _ in range(n_fixed)]  # データを生成する
    t = measure_avg(counting_sort_nk, data, k)  # 時間を計測する
    times_exp2.append(t)  # 結果を記録する
    print(f"  n={n_fixed}, k={k:>6}: {t:.6f} 秒")  # 結果を表示する

# ===== グラフを描画する =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))  # 2つのグラフを作成する

# --- 実験1のグラフ ---
ax1.plot(n_values, times_exp1, "o-", color="#3498db", linewidth=2, markersize=8)  # 折れ線を描画する
ax1.set_xlabel("n（要素数）", fontsize=12)  # X軸ラベル
ax1.set_ylabel("実行時間（秒）", fontsize=12)  # Y軸ラベル
ax1.set_title(f"実験1: n を変化（k={k_fixed} 固定）", fontsize=13)  # タイトル
ax1.grid(alpha=0.3)  # グリッドを表示する

# --- 実験2のグラフ ---
ax2.plot(k_values, times_exp2, "s-", color="#e74c3c", linewidth=2, markersize=8)  # 折れ線を描画する
ax2.set_xlabel("k（値の範囲）", fontsize=12)  # X軸ラベル
ax2.set_ylabel("実行時間（秒）", fontsize=12)  # Y軸ラベル
ax2.set_title(f"実験2: k を変化（n={n_fixed} 固定）", fontsize=13)  # タイトル
ax2.set_xscale("log")  # X軸を対数スケールにする
ax2.grid(alpha=0.3)  # グリッドを表示する

plt.tight_layout()  # レイアウトを調整する
plt.show()  # グラフを表示する

# --- 考察 ---
print("\n【考察】")  # 考察を表示する
print("実験1: n が増加すると実行時間もほぼ線形に増加 → O(n) の影響")  # 結論1
print("実験2: k が増加すると実行時間が増加 → O(k) の影響")  # 結論2
print("よって、分布数えソートの計算量は O(n + k) であることが実験的に確認できた")  # 総合結論
```

### 発展課題1の解答例

```python
def counting_sort_strings_by_length(strings):
    """文字列を長さ順に分布数えソートする"""

    if len(strings) <= 1:  # 要素が1個以下ならそのまま返す
        return strings[:]  # コピーを返す

    lengths = [len(s) for s in strings]  # 各文字列の長さを計算する
    max_length = max(lengths)  # 最大の長さを取得する

    # --- ステップ1: 度数を数える ---
    count = [0] * (max_length + 1)  # 度数配列を初期化する
    for length in lengths:  # 各長さを走査する
        count[length] += 1  # カウントを増やす

    # --- ステップ2: 累積度数を計算する ---
    for i in range(1, len(count)):  # 先頭から足し合わせる
        count[i] += count[i - 1]  # 累積和を作る

    # --- ステップ3: 末尾から配置する（安定ソート） ---
    output = [None] * len(strings)  # 出力配列を用意する
    for i in range(len(strings) - 1, -1, -1):  # 末尾から処理する
        length = len(strings[i])  # 現在の文字列の長さを取得する
        position = count[length] - 1  # 配置位置を決定する
        output[position] = strings[i]  # 配置する
        count[length] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- 実行 ---
words = ["apple", "hi", "cat", "elephant", "go", "python", "a", "dog", "wonderful"]  # テストデータ
sorted_words = counting_sort_strings_by_length(words)  # ソートを実行する

print("入力:")  # 入力を表示する
for word in words:  # 各単語を表示する
    print(f"  '{word}' (長さ {len(word)})")  # 単語と長さを表示する

print("\nソート結果（長さ順）:")  # ソート結果を表示する
for word in sorted_words:  # 各単語を表示する
    print(f"  '{word}' (長さ {len(word)})")  # 単語と長さを表示する

# --- 安定性の確認 ---
print("\n安定性の確認:")  # 安定性を確認する
length_3 = [w for w in sorted_words if len(w) == 3]  # 長さ3の単語を抽出する
print(f"  長さ3の単語: {length_3}")  # 表示する
print(f"  元の順序 ['cat', 'dog'] が保たれているか: {length_3 == ['cat', 'dog']}")  # 確認する
```

### 発展課題2の解答例

```python
import random  # 乱数モジュールを読み込む
import matplotlib.pyplot as plt  # グラフ描画モジュールを読み込む

def draw_colorful_histogram(scores):
    """カラフルなヒストグラムを描画する"""

    # --- 10点刻みで度数を集計する ---
    bin_labels = []  # 区間ラベルリスト
    bin_counts = []  # 度数リスト
    bin_colors = []  # 色リスト

    for start in range(0, 100, 10):  # 各区間を処理する
        if start == 90:  # 最後の区間（90-100）
            end = 100  # 上限を100にする
            cnt = sum(1 for s in scores if start <= s <= end)  # 上限含む
            label = f"{start}-{end}"  # ラベルを作る
        else:  # 他の区間
            end = start + 9  # 上限を計算する
            cnt = sum(1 for s in scores if start <= s <= end)  # 度数を数える
            label = f"{start}-{end}"  # ラベルを作る

        bin_labels.append(label)  # ラベルを追加する
        bin_counts.append(cnt)  # 度数を追加する

        if start < 60:  # 不合格ゾーン（0-59）
            bin_colors.append("#e74c3c")  # 赤系を設定する
        elif start < 80:  # 普通ゾーン（60-79）
            bin_colors.append("#f39c12")  # 黄系を設定する
        else:  # 高得点ゾーン（80-100）
            bin_colors.append("#3498db")  # 青系を設定する

    # --- 統計値を計算する ---
    average = sum(scores) / len(scores)  # 平均点を計算する
    sorted_scores = sorted(scores)  # ソートする
    mid = len(scores) // 2  # 中央インデックスを計算する
    if len(scores) % 2 == 0:  # 偶数の場合
        median = (sorted_scores[mid - 1] + sorted_scores[mid]) / 2  # 中央2つの平均
    else:  # 奇数の場合
        median = sorted_scores[mid]  # 中央の値

    # --- グラフを描画する ---
    fig, ax = plt.subplots(figsize=(14, 7))  # 図を作成する

    bars = ax.bar(bin_labels, bin_counts, color=bin_colors, edgecolor="white", linewidth=1.5)  # バーを描画する

    for bar, cnt in zip(bars, bin_counts):  # 各バーの上に数値を表示する
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(cnt), ha="center", va="bottom", fontsize=11, fontweight="bold")  # 数値を表示する

    # --- 平均点の縦線 ---
    ax.axvline(x=average / 10 - 0.5, color="darkred", linestyle="--",
               linewidth=2, label=f"平均点: {average:.1f}")  # 平均線を描画する

    # --- 中央値の縦線 ---
    ax.axvline(x=median / 10 - 0.5, color="darkblue", linestyle="-.",
               linewidth=2, label=f"中央値: {median:.1f}")  # 中央値線を描画する

    # --- 合格ライン（60点） ---
    ax.axvline(x=5.5, color="green", linestyle=":",
               linewidth=2, label="合格ライン: 60点")  # 合格ラインを描画する

    ax.set_xlabel("点数の範囲", fontsize=13)  # X軸ラベルを設定する
    ax.set_ylabel("人数", fontsize=13)  # Y軸ラベルを設定する
    ax.set_title(f"テスト点数の度数分布（{len(scores)}人）", fontsize=15)  # タイトルを設定する
    ax.legend(fontsize=11, loc="upper left")  # 凡例を表示する
    ax.set_ylim(0, max(bin_counts) + 5)  # Y軸の範囲を設定する
    plt.tight_layout()  # レイアウトを調整する
    plt.show()  # グラフを表示する


# --- 実行 ---
random.seed(42)  # シードを固定する
scores = [random.randint(0, 100) for _ in range(200)]  # 200人分の点数を生成する
draw_colorful_histogram(scores)  # ヒストグラムを描画する
```

---

## 6. まとめ

| 比較ベースのソート | 分布数えソート |
|---|---|
| 要素同士を比較する | 比較しない、出現回数を数える |
| 最速でも O(n log n) | O(n + k) で動作 |
| どんなデータにも使える | 値が整数で範囲が限られる場合に有効 |
| 例: 挿入ソート、バブルソート | 例: Counting Sort |

**ポイント:**
- 分布数えソートは「数える」だけなので、比較ソートの O(n log n) の壁を突破できる
- ただし値の範囲 k が大きすぎると、メモリと時間が無駄になる
- テストの点数（0~100）や年齢（0~150）など、範囲が小さいデータに最適
- 末尾から配置することで**安定ソート**になる（次回詳しく解説）
