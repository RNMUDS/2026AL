# 第9回: 挿入ソートの応用

## 学習目標

- **二分挿入ソート**（Binary Insertion Sort）の仕組みを理解し、`bisect` モジュールを使って実装できる
- **バブルソート**（Bubble Sort）のアルゴリズムを理解し、最適化版を実装できる
- 3つのデータパターン（ランダム・ほぼ整列済み・逆順）で各アルゴリズムの性能を比較できる

---

## 1. 説明

### 1.1 通常の挿入ソート（復習）

前回学んだ挿入ソートでは、ソート済み部分から**挿入位置を線形探索**（1つずつ比較）で見つけていました。

```
配列: [2, 5, 8, | 3, 7, 1]
                  ↑ この3を挿入したい
ソート済み部分: [2, 5, 8]
→ 8と比較: 3 < 8 → 右にずらす
→ 5と比較: 3 < 5 → 右にずらす
→ 2と比較: 3 > 2 → ここに挿入！
結果: [2, 3, 5, 8, | 7, 1]
```

ソート済み部分が長くなると、比較回数が増えます（最悪 O(n) 回）。

### 1.2 二分挿入ソート（Binary Insertion Sort）

**アイデア**: ソート済み部分はすでに整列しているので、**二分探索**（Binary Search）で挿入位置を効率的に見つけられます。

```
配列: [2, 5, 8, | 3, 7, 1]
                  ↑ この3を挿入したい
ソート済み部分: [2, 5, 8]
→ 二分探索: 中央は5 → 3 < 5 → 左半分[2]を見る
→ 二分探索: 中央は2 → 3 > 2 → 位置1に挿入！
結果: [2, 3, 5, 8, | 7, 1]
```

- 比較回数: O(n) → **O(log n)** に改善
- ただし、要素をずらす操作は依然 O(n) なので、全体の計算量は O(n^2) のまま

### 1.3 Python の `bisect` モジュール

Python には二分探索を行う標準ライブラリ `bisect` があります。

| 関数 | 説明 |
|------|------|
| `bisect.bisect_left(a, x, lo, hi)` | ソート済みリスト `a` の `lo` から `hi` の範囲で、`x` を挿入すべき**左端**の位置を返す |
| `bisect.bisect_right(a, x, lo, hi)` | 同上、ただし**右端**の位置を返す |
| `bisect.insort_left(a, x)` | `x` をソート済みリスト `a` に挿入する |

### 1.4 バブルソート（Bubble Sort）

バブルソートは「隣り合う要素を比較して交換」を繰り返すアルゴリズムです。

```
[5, 3, 8, 1, 2]  ← 初期状態

パス1: 末尾から先頭へ比較・交換
  → 最小値「1」が先頭に浮かび上がった！（泡のように）

パス2: 2番目の位置から繰り返す...
```

**最適化**: あるパスで1回も交換が起きなければ、すでにソート済みなので終了できます。

### 1.5 シェルソート（Shell Sort）

挿入ソートの改良版で、離れた要素同士を先に比較・交換し、間隔を徐々に縮めていく方法です。間隔が1になったとき通常の挿入ソートになりますが、その時点でほぼ整列済みなので高速に動作します。

---

## 2. 例題

### 例題1: bisect で挿入位置を見つける

```python
# ===== bisectモジュールで挿入位置を見つける =====

import bisect  # 二分探索モジュールをインポートする

# --- ソート済みリストを用意する ---
sorted_list = [10, 20, 30, 40, 50]  # ソート済みリストを定義する
print(f"ソート済みリスト: {sorted_list}")  # リストを表示する

# --- bisect_leftで挿入位置を求める ---
target = 25  # 挿入したい値を設定する
position = bisect.bisect_left(sorted_list, target)  # 挿入位置（左端）を求める
print(f"\n{target} の挿入位置（bisect_left）: {position}")  # 結果を表示する
print(f"  → sorted_list[{position}]={sorted_list[position]} の前に挿入する")  # 説明を表示する

# --- 同じ値がある場合のbisect_leftとbisect_rightの違い ---
list_with_dup = [10, 20, 30, 30, 30, 40, 50]  # 重複を含むリストを定義する
print(f"\n重複ありリスト: {list_with_dup}")  # リストを表示する

left_pos = bisect.bisect_left(list_with_dup, 30)  # 左端の位置を求める
right_pos = bisect.bisect_right(list_with_dup, 30)  # 右端の位置を求める
print(f"  30 の挿入位置（bisect_left）:  {left_pos}")  # 左端の位置を表示する
print(f"  30 の挿入位置（bisect_right）: {right_pos}")  # 右端の位置を表示する
print(f"  → 30 は位置 {left_pos} から {right_pos-1} に存在する")  # 範囲を表示する

# --- 範囲を指定して探索する ---
data = [10, 20, 30, 30, 40, 50]  # テスト用リストを定義する
pos_in_range = bisect.bisect_left(data, 25, lo=1, hi=4)  # 範囲指定で探索する
print(f"\n範囲指定（lo=1, hi=4）での 25 の挿入位置: {pos_in_range}")  # 結果を表示する

# --- insort_leftで実際に挿入する ---
demo_list = [10, 20, 30, 40, 50]  # デモ用リストを定義する
print(f"\n挿入前: {demo_list}")  # 挿入前を表示する
bisect.insort_left(demo_list, 25)  # 25を挿入する
print(f"insort_left(25) 後: {demo_list}")  # 挿入後を表示する
```

### 例題2: 二分挿入ソートの実装

```python
# ===== 二分挿入ソート（bisect使用） =====

import bisect  # 二分探索モジュールをインポートする

def binary_insertion_sort(data):
    """二分探索を使った挿入ソート（各ステップを表示する）"""
    n = len(data)  # 配列の長さを取得する
    comparison_count = 0  # 比較回数を初期化する（bisect内部の比較を概算）

    print(f"元の配列: {data}")  # 元の配列を表示する
    print("=" * 60)  # 区切り線を表示する

    for i in range(1, n):  # 2番目の要素から最後まで処理する
        key = data[i]  # 挿入する値を取り出す
        sorted_part = data[:i]  # ソート済み部分を取得する（表示用）

        # --- bisect_leftで挿入位置を求める ---
        position = bisect.bisect_left(data, key, 0, i)  # 挿入位置を二分探索で求める

        # --- 比較回数をlog2(i)で概算する ---
        import math  # mathモジュールをインポートする
        comparison_count = comparison_count + int(math.log2(i)) + 1  # 概算比較回数を加算する

        print(f"\nステップ {i}:")  # ステップ番号を表示する
        print(f"  挿入する値: {key}")  # 挿入する値を表示する
        print(f"  ソート済み部分: {sorted_part}")  # ソート済み部分を表示する
        print(f"  二分探索の結果 → 挿入位置: {position}")  # 挿入位置を表示する

        # --- 要素をずらして挿入する ---
        if position < i:  # ずらす必要がある場合
            print(f"  移動する要素: {data[position:i]}")  # 移動する要素を表示する
        temp = data[i]  # 挿入する値を一時保存する
        for j in range(i, position, -1):  # iからpositionまで右にずらす
            data[j] = data[j - 1]  # 要素を1つ右にずらす
        data[position] = temp  # 挿入位置にkeyを挿入する
        print(f"  結果: {data}")  # 結果を表示する

    print(f"\n{'=' * 60}")  # 区切り線を表示する
    print(f"ソート完了: {data}")  # 最終結果を表示する
    print(f"概算比較回数: {comparison_count}")  # 比較回数を表示する
    return data  # ソート済み配列を返す

# --- テスト実行 ---
test_data = [38, 27, 43, 3, 9, 82, 10]  # テスト用配列を定義する
binary_insertion_sort(test_data[:])  # コピーを渡してソートする
```

### 例題3: バブルソートの基本

```python
# ===== バブルソートの動作を表示する =====

def bubble_sort(data):
    """バブルソートを実行して各パスの動作を表示する関数"""
    n = len(data)  # 配列の長さを取得する
    comparison_count = 0  # 比較回数を初期化する
    swap_count = 0  # 交換回数を初期化する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print("=" * 60)  # 区切り線を表示する

    for i in range(n):  # パスをn回繰り返す
        print(f"\n--- パス {i + 1} ---")  # パス番号を表示する
        swapped = False  # 交換フラグを初期化する

        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparison_count = comparison_count + 1  # 比較回数を加算する
            left = data[j - 1]  # 左の要素を取得する
            right = data[j]  # 右の要素を取得する

            if data[j - 1] > data[j]:  # 左が右より大きい場合
                temp = data[j - 1]  # 一時変数に退避する
                data[j - 1] = data[j]  # 左に右の値を代入する
                data[j] = temp  # 右に退避した値を代入する
                swap_count = swap_count + 1  # 交換回数を加算する
                swapped = True  # 交換フラグを立てる
                print(f"  arr[{j-1}]={left} > arr[{j}]={right} → 交換 → {data}")  # 交換を表示する
            else:  # 左が右以下の場合
                print(f"  arr[{j-1}]={left} <= arr[{j}]={right} → そのまま")  # 交換なしを表示する

        print(f"  パス{i+1}の結果: {data}")  # パスの結果を表示する

        if not swapped:  # 交換がなかった場合
            print(f"\n  交換なし → ソート完了!")  # 完了メッセージを表示する
            break  # ループを終了する

    print(f"\n最終結果: {data}")  # 最終結果を表示する
    print(f"比較回数: {comparison_count}, 交換回数: {swap_count}")  # 統計を表示する
    return data, comparison_count, swap_count  # 結果を返す

# --- テスト実行 ---
test_data = [5, 3, 8, 1, 2]  # テスト用配列を定義する
bubble_sort(test_data[:])  # コピーを渡してソートする
```

### 例題4: 挿入ソートとバブルソートの比較

```python
# ===== 挿入ソートとバブルソートの性能比較 =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def insertion_sort_count(data):
    """挿入ソート（比較回数カウント付き、表示なし）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0:  # 左端まで探す
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                j = j - 1  # 1つ左に移動する
            else:  # key以下に当たった場合
                break  # ループを終了する

        data[j + 1] = key  # keyを挿入する

    return comparisons  # 比較回数を返す

def bubble_sort_count(data):
    """バブルソート最適化版（比較回数カウント付き、表示なし）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する

    for i in range(n):  # パスをn回繰り返す
        swapped = False  # 交換フラグを初期化する

        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # 交換フラグを立てる

        if not swapped:  # 交換がなかった場合
            break  # ループを終了する

    return comparisons  # 比較回数を返す

# --- 比較テスト ---
data_size = 2000  # データサイズを設定する
test_data = []  # テストデータを初期化する
for i in range(data_size):  # data_size個のランダム整数を生成する
    test_data.append(random.randint(0, 10000))  # ランダム整数を追加する

print(f"=== 挿入ソート vs バブルソート (データ数={data_size}) ===\n")  # 見出しを表示する

# --- 挿入ソート ---
data_copy1 = test_data[:]  # テストデータのコピーを作成する
start = time.time()  # 計測を開始する
ins_comps = insertion_sort_count(data_copy1)  # 挿入ソートを実行する
ins_time = time.time() - start  # 経過時間を計算する

# --- バブルソート ---
data_copy2 = test_data[:]  # テストデータのコピーを作成する
start = time.time()  # 計測を開始する
bub_comps = bubble_sort_count(data_copy2)  # バブルソートを実行する
bub_time = time.time() - start  # 経過時間を計算する

# --- 結果を表示する ---
print(f"{'アルゴリズム':<20} {'比較回数':<16} {'実行時間(秒)'}")  # ヘッダーを表示する
print(f"{'-'*52}")  # 区切り線を表示する
print(f"{'挿入ソート':<20} {ins_comps:<16} {ins_time:.4f}")  # 挿入ソートの結果を表示する
print(f"{'バブルソート':<20} {bub_comps:<16} {bub_time:.4f}")  # バブルソートの結果を表示する

if ins_time > 0 and bub_time > 0:  # 両方の時間が正の場合
    ratio = bub_time / ins_time  # 速度比を計算する
    print(f"\nバブルソートは挿入ソートの約 {ratio:.1f} 倍の時間がかかった")  # 比較結果を表示する
```

### 例題5: データパターン別の性能分析

```python
# ===== 3つのデータパターンでソートアルゴリズムの性能を分析する =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def insertion_sort_bench(data):
    """挿入ソート（ベンチマーク用、表示なし）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する
        while j >= 0:  # 左端まで探す
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                j = j - 1  # 1つ左に移動する
            else:  # key以下に当たった場合
                break  # ループを終了する
        data[j + 1] = key  # keyを挿入する
    return comparisons  # 比較回数を返す

def bubble_sort_bench(data):
    """バブルソート最適化版（ベンチマーク用、表示なし）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(n):  # パスをn回繰り返す
        swapped = False  # 交換フラグを初期化する
        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # 交換フラグを立てる
        if not swapped:  # 交換がなかった場合
            break  # ループを終了する
    return comparisons  # 比較回数を返す

def generate_random(size):
    """ランダムデータを生成する関数"""
    data = []  # 結果リストを初期化する
    for i in range(size):  # size個のランダム整数を生成する
        data.append(random.randint(0, 10000))  # ランダム整数を追加する
    return data  # データを返す

def generate_nearly_sorted(size):
    """ほぼ整列済みデータを生成する関数"""
    data = list(range(size))  # 0からsize-1の整列済みリストを作成する
    swap_count = size // 10  # 全体の10%を入れ替える
    for i in range(swap_count):  # swap_count回繰り返す
        idx1 = random.randint(0, size - 1)  # ランダムな位置を選ぶ
        idx2 = random.randint(0, size - 1)  # ランダムな位置を選ぶ
        data[idx1], data[idx2] = data[idx2], data[idx1]  # 2つの要素を入れ替える
    return data  # データを返す

def generate_reversed(size):
    """逆順データを生成する関数"""
    data = list(range(size, 0, -1))  # sizeから1の逆順リストを作成する
    return data  # データを返す

def measure(sort_func, data):
    """ソート関数の実行時間と比較回数を計測する関数"""
    data_copy = data[:]  # データのコピーを作成する
    start = time.time()  # 計測を開始する
    comparisons = sort_func(data_copy)  # ソートを実行する
    elapsed = time.time() - start  # 経過時間を計算する
    return elapsed, comparisons  # 時間と比較回数を返す

# --- テスト実行 ---
size = 2000  # データサイズを設定する
print(f"=== データパターン別 性能比較 (N={size}) ===\n")  # 見出しを表示する

patterns = [  # データパターンのリストを定義する
    ("ランダム", generate_random(size)),
    ("ほぼ整列済み", generate_nearly_sorted(size)),
    ("逆順", generate_reversed(size))
]

algorithms = [  # アルゴリズムのリストを定義する
    ("挿入ソート", insertion_sort_bench),
    ("バブルソート(最適化)", bubble_sort_bench)
]

# --- 結果テーブルのヘッダー ---
print(f"{'パターン':<14} {'アルゴリズム':<22} {'時間(秒)':<12} {'比較回数'}")  # ヘッダーを表示する
print("-" * 64)  # 区切り線を表示する

for pattern_name, pattern_data in patterns:  # 各パターンについて処理する
    for algo_name, algo_func in algorithms:  # 各アルゴリズムについて処理する
        elapsed, comparisons = measure(algo_func, pattern_data)  # 計測する
        print(f"{pattern_name:<14} {algo_name:<22} {elapsed:<12.4f} {comparisons}")  # 結果を表示する
    print()  # パターン間に空行を入れる

# --- 考察 ---
print("=== 考察 ===")  # 考察の見出しを表示する
print("1. ほぼ整列済みデータでは挿入ソートが最も高速")  # 考察1を表示する
print("2. 逆順データは挿入ソート・バブルソートの最悪ケース")  # 考察2を表示する
print("3. バブルソートはほぼ整列済みデータで早期終了の恩恵を受ける")  # 考察3を表示する
print("4. データの初期状態がアルゴリズムの性能に大きく影響する")  # 考察4を表示する
```

---

## 3. 標準課題

### 課題1: bisect_left で挿入位置を求める（超やさしい）

ソート済みリスト `[5, 10, 15, 20, 25, 30]` に対して、値 `12`, `20`, `35` の挿入位置を `bisect.bisect_left` で求めて表示してください。

### 課題2: bisect を使った挿入位置と線形探索を比較する（超やさしい）

ソート済みリスト `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]` に値 `55` を挿入する位置を、線形探索と `bisect.bisect_left` の両方で求め、結果が一致することを確認してください。それぞれの探索ステップ数も表示してください。

### 課題3: 二分挿入ソートを実装する（やさしい）

`bisect.bisect_left` を使った二分挿入ソートを実装し、テストデータ `[38, 27, 43, 3, 9, 82, 10]` を整列してください。各ステップで挿入する値と挿入位置を表示してください。

### 課題4: 二分挿入ソートで比較回数を概算する（やさしい）

課題3の二分挿入ソートに比較回数の概算（各ステップで log2(ソート済み部分の長さ)+1）を追加してください。通常の挿入ソートの比較回数と比較してください。

### 課題5: バブルソートを実装する（やややさしい）

基本的なバブルソートを実装し、テストデータ `[64, 34, 25, 12, 22, 11, 90]` を整列してください。各パスでの交換回数を表示してください。

### 課題6: バブルソートに早期終了の最適化を追加する（やややさしい）

課題5のバブルソートに「交換がなければ早期終了」の最適化を追加してください。ソート済みデータ `[1, 2, 3, 4, 5, 6, 7]` で基本版と最適化版のパス数・比較回数を比較してください。

### 課題7: 挿入ソートとバブルソートの比較回数を計測する（やや普通）

データサイズ 1000 のランダムデータに対して、挿入ソートとバブルソート（最適化版）の比較回数と実行時間を計測し、結果を表形式で表示してください。

### 課題8: 3つのデータパターンで性能を比較する（やや普通）

ランダム、ほぼ整列済み（10%入れ替え）、逆順の3パターンのデータ（各1000要素）を生成し、挿入ソートとバブルソートの実行時間と比較回数を表形式で比較してください。

### 課題9: データパターン別のソート過程を可視化する（普通）

ランダム、ほぼ整列済み、逆順の3パターンのデータ（各20要素）に対して挿入ソートを適用し、各パターンでのステップ数と移動回数をテキストで可視化して比較してください。

### 課題10: 4つのアルゴリズムの総合ベンチマークを実施する（普通）

挿入ソート、二分挿入ソート、バブルソート（最適化版）、Python 組み込み `sorted()` の4つを、3パターンのデータ（各3000要素）で比較してください。結果を表形式で表示し、考察を出力してください。

---

## 4. 発展課題

### 発展課題1: シェルソートの実装

シェルソートを実装し、挿入ソートとバブルソートと比較してください。間隔列は `[n//2, n//4, ..., 1]` を使用してください。

### 発展課題2: matplotlib でソート性能の比較グラフを作成する

4つのアルゴリズム x 3つのデータパターンの比較結果を matplotlib の棒グラフで表示してください。

---

## 5. 解答例

### 課題1の解答例

```python
# ===== 課題1: bisect_leftで挿入位置を求める =====

import bisect  # 二分探索モジュールをインポートする

sorted_list = [5, 10, 15, 20, 25, 30]  # ソート済みリストを定義する
print(f"ソート済みリスト: {sorted_list}")  # リストを表示する

targets = [12, 20, 35]  # 検索する値のリストを定義する

print("\n=== 各値の挿入位置 ===")  # 見出しを表示する
for target in targets:  # 各値について処理する
    pos = bisect.bisect_left(sorted_list, target)  # 挿入位置を求める
    print(f"  値 {target} → 挿入位置: {pos}", end="")  # 結果を表示する
    if pos < len(sorted_list):  # 配列範囲内の場合
        print(f" (sorted_list[{pos}]={sorted_list[pos]} の前)")  # 説明を表示する
    else:  # 末尾の場合
        print(f" (末尾に追加)")  # 末尾追加を表示する
```

### 課題2の解答例

```python
# ===== 課題2: bisectと線形探索の比較 =====

import bisect  # 二分探索モジュールをインポートする

sorted_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # ソート済みリストを定義する
target = 55  # 挿入する値を設定する

print(f"リスト: {sorted_list}")  # リストを表示する
print(f"挿入する値: {target}")  # 挿入値を表示する

# --- 線形探索で挿入位置を求める ---
print("\n--- 線形探索 ---")  # 見出しを表示する
linear_steps = 0  # 探索ステップ数を初期化する
linear_pos = len(sorted_list)  # 挿入位置を末尾に初期化する

for i in range(len(sorted_list)):  # リストを先頭から走査する
    linear_steps = linear_steps + 1  # ステップ数を加算する
    print(f"  ステップ{linear_steps}: sorted_list[{i}]={sorted_list[i]} と比較")  # 比較を表示する
    if sorted_list[i] > target:  # 現在の値が挿入値より大きい場合
        linear_pos = i  # 挿入位置を設定する
        print(f"    → {sorted_list[i]} > {target} → 挿入位置 = {i}")  # 結果を表示する
        break  # ループを終了する

print(f"  線形探索の結果: 位置 {linear_pos} ({linear_steps} ステップ)")  # 結果を表示する

# --- bisectで挿入位置を求める ---
print("\n--- bisect_left ---")  # 見出しを表示する
bisect_pos = bisect.bisect_left(sorted_list, target)  # 挿入位置を求める
import math  # mathモジュールをインポートする
bisect_steps = int(math.log2(len(sorted_list))) + 1  # 二分探索のステップ数を概算する
print(f"  bisect_leftの結果: 位置 {bisect_pos} (約 {bisect_steps} ステップ)")  # 結果を表示する

# --- 比較 ---
print(f"\n=== 結果比較 ===")  # 比較の見出しを表示する
print(f"  線形探索: 位置 {linear_pos}, {linear_steps} ステップ")  # 線形探索の結果
print(f"  bisect:   位置 {bisect_pos}, 約 {bisect_steps} ステップ")  # bisectの結果
if linear_pos == bisect_pos:  # 結果が一致する場合
    print(f"  → 結果一致! bisectは約 {linear_steps - bisect_steps} ステップ少ない")  # 一致メッセージ
```

### 課題3の解答例

```python
# ===== 課題3: 二分挿入ソートの実装 =====

import bisect  # 二分探索モジュールをインポートする

def binary_insertion_sort(data):
    """bisect_leftを使った二分挿入ソート"""
    n = len(data)  # 配列の長さを取得する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print("=" * 50)  # 区切り線を表示する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        position = bisect.bisect_left(data, key, 0, i)  # 挿入位置を二分探索で求める

        print(f"\nステップ {i}: key={key}, 挿入位置={position}")  # ステップ情報を表示する
        print(f"  ソート済み部分: {data[:i]}")  # ソート済み部分を表示する

        # --- 要素をずらして挿入する ---
        for j in range(i, position, -1):  # iからpositionまで右にずらす
            data[j] = data[j - 1]  # 要素を1つ右にずらす
        data[position] = key  # 挿入位置にkeyを挿入する

        print(f"  結果: {data}")  # 結果を表示する

    print(f"\nソート完了: {data}")  # 最終結果を表示する
    return data  # ソート済み配列を返す

# --- テスト実行 ---
test_data = [38, 27, 43, 3, 9, 82, 10]  # テスト用配列を定義する
binary_insertion_sort(test_data[:])  # コピーを渡してソートする
```

### 課題4の解答例

```python
# ===== 課題4: 二分挿入ソートと通常挿入ソートの比較回数比較 =====

import bisect  # 二分探索モジュールをインポートする
import math  # 数学関数モジュールをインポートする

def binary_insertion_sort_count(data):
    """二分挿入ソート（比較回数概算付き）"""
    n = len(data)  # 配列の長さを取得する
    total_comparisons = 0  # 比較回数の合計を初期化する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        position = bisect.bisect_left(data, key, 0, i)  # 挿入位置を求める
        step_comparisons = int(math.log2(i)) + 1  # このステップの比較回数を概算する
        total_comparisons = total_comparisons + step_comparisons  # 合計に加算する

        for j in range(i, position, -1):  # 要素をずらす
            data[j] = data[j - 1]  # 1つ右にずらす
        data[position] = key  # keyを挿入する

    return data, total_comparisons  # 結果を返す

def insertion_sort_count(data):
    """通常挿入ソート（比較回数カウント付き）"""
    n = len(data)  # 配列の長さを取得する
    total_comparisons = 0  # 比較回数の合計を初期化する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0:  # 左端まで探す
            total_comparisons = total_comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                j = j - 1  # 1つ左に移動する
            else:  # key以下の場合
                break  # ループを終了する

        data[j + 1] = key  # keyを挿入する

    return data, total_comparisons  # 結果を返す

# --- テスト ---
test_data = [38, 27, 43, 3, 9, 82, 10]  # テスト用配列を定義する
print(f"テストデータ: {test_data}\n")  # テストデータを表示する

result1, comps1 = insertion_sort_count(test_data[:])  # 通常挿入ソートを実行する
result2, comps2 = binary_insertion_sort_count(test_data[:])  # 二分挿入ソートを実行する

print(f"通常挿入ソート:   比較回数 = {comps1}")  # 通常版の比較回数を表示する
print(f"二分挿入ソート:   比較回数 ≒ {comps2} (概算)")  # 二分版の比較回数を表示する
print(f"ソート結果: {result1}")  # ソート結果を表示する

if comps1 > 0:  # 比較回数が正の場合
    reduction = (1 - comps2 / comps1) * 100  # 削減率を計算する
    print(f"\n二分探索により比較回数が約 {reduction:.0f}% 削減された")  # 削減率を表示する
```

### 課題5の解答例

```python
# ===== 課題5: バブルソートの実装 =====

def bubble_sort(data):
    """バブルソート（各パスの交換回数を表示する）"""
    n = len(data)  # 配列の長さを取得する
    total_swaps = 0  # 交換回数の合計を初期化する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print("=" * 50)  # 区切り線を表示する

    for i in range(n):  # パスをn回繰り返す
        pass_swaps = 0  # このパスの交換回数を初期化する

        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                temp = data[j - 1]  # 一時変数に退避する
                data[j - 1] = data[j]  # 交換する
                data[j] = temp  # 交換を完了する
                pass_swaps = pass_swaps + 1  # パスの交換回数を加算する

        total_swaps = total_swaps + pass_swaps  # 合計に加算する
        print(f"  パス{i+1}: 交換{pass_swaps}回 → {data}")  # パスの結果を表示する

    print(f"\nソート完了: {data}")  # 最終結果を表示する
    print(f"交換回数の合計: {total_swaps}")  # 交換回数の合計を表示する
    return data  # ソート済み配列を返す

# --- テスト実行 ---
test_data = [64, 34, 25, 12, 22, 11, 90]  # テスト用配列を定義する
bubble_sort(test_data[:])  # コピーを渡してソートする
```

### 課題6の解答例

```python
# ===== 課題6: バブルソートの早期終了最適化 =====

def bubble_sort_basic(data):
    """基本版バブルソート（全パスを実行する）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    pass_count = 0  # パス回数を初期化する

    for i in range(n):  # パスをn回繰り返す
        pass_count = pass_count + 1  # パス回数を加算する
        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する

    return data, comparisons, pass_count  # 結果を返す

def bubble_sort_optimized(data):
    """最適化版バブルソート（交換なしで早期終了する）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    pass_count = 0  # パス回数を初期化する

    for i in range(n):  # パスをn回繰り返す
        pass_count = pass_count + 1  # パス回数を加算する
        swapped = False  # 交換フラグを初期化する

        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # 交換フラグを立てる

        if not swapped:  # 交換がなかった場合
            break  # ループを終了する

    return data, comparisons, pass_count  # 結果を返す

# --- ランダムデータでテスト ---
test_random = [64, 34, 25, 12, 22, 11, 90]  # ランダムデータ
print("=== ランダムデータ ===")  # 見出しを表示する
r1, c1, p1 = bubble_sort_basic(test_random[:])  # 基本版を実行する
r2, c2, p2 = bubble_sort_optimized(test_random[:])  # 最適化版を実行する
print(f"  基本版:   比較{c1}回, パス{p1}回")  # 基本版の結果を表示する
print(f"  最適化版: 比較{c2}回, パス{p2}回")  # 最適化版の結果を表示する

# --- ソート済みデータでテスト ---
test_sorted = [1, 2, 3, 4, 5, 6, 7]  # ソート済みデータ
print("\n=== ソート済みデータ ===")  # 見出しを表示する
r3, c3, p3 = bubble_sort_basic(test_sorted[:])  # 基本版を実行する
r4, c4, p4 = bubble_sort_optimized(test_sorted[:])  # 最適化版を実行する
print(f"  基本版:   比較{c3}回, パス{p3}回")  # 基本版の結果を表示する
print(f"  最適化版: 比較{c4}回, パス{p4}回")  # 最適化版の結果を表示する
print(f"\n  → 最適化版はソート済みデータを{p4}パスで検出（基本版は{p3}パス）")  # 比較結果を表示する
```

### 課題7の解答例

```python
# ===== 課題7: 挿入ソートとバブルソートのベンチマーク =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def insertion_sort_bench(data):
    """挿入ソート（ベンチマーク用）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する
        while j >= 0:  # 左端まで探す
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                j = j - 1  # 1つ左に移動する
            else:  # key以下の場合
                break  # ループを終了する
        data[j + 1] = key  # keyを挿入する
    return comparisons  # 比較回数を返す

def bubble_sort_bench(data):
    """バブルソート最適化版（ベンチマーク用）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(n):  # パスをn回繰り返す
        swapped = False  # 交換フラグを初期化する
        for j in range(n - 1, i, -1):  # 末尾からi+1番目まで比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が右より大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # 交換フラグを立てる
        if not swapped:  # 交換がなかった場合
            break  # ループを終了する
    return comparisons  # 比較回数を返す

# --- テストデータを生成する ---
data_size = 1000  # データサイズを設定する
test_data = []  # テストデータを初期化する
for i in range(data_size):  # data_size個のランダム整数を生成する
    test_data.append(random.randint(0, 10000))  # ランダム整数を追加する

print(f"=== ベンチマーク (N={data_size}) ===\n")  # 見出しを表示する

# --- 挿入ソート ---
start = time.time()  # 計測開始
ins_comps = insertion_sort_bench(test_data[:])  # 挿入ソートを実行する
ins_time = time.time() - start  # 経過時間を計算する

# --- バブルソート ---
start = time.time()  # 計測開始
bub_comps = bubble_sort_bench(test_data[:])  # バブルソートを実行する
bub_time = time.time() - start  # 経過時間を計算する

# --- 結果を表示する ---
print(f"{'アルゴリズム':<20} {'比較回数':<16} {'実行時間(秒)'}")  # ヘッダーを表示する
print("-" * 52)  # 区切り線を表示する
print(f"{'挿入ソート':<20} {ins_comps:<16} {ins_time:.4f}")  # 挿入ソートの結果
print(f"{'バブルソート(最適化)':<20} {bub_comps:<16} {bub_time:.4f}")  # バブルソートの結果
```

### 課題8の解答例

```python
# ===== 課題8: 3パターンでの性能比較 =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def insertion_sort_bench(data):
    """挿入ソート（ベンチマーク用）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(1, n):  # 2番目から処理する
        key = data[i]  # 挿入する値
        j = i - 1  # 比較開始位置
        while j >= 0:  # 左端まで探す
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 右にずらす
                j = j - 1  # 左に移動する
            else:  # key以下の場合
                break  # 終了する
        data[j + 1] = key  # keyを挿入する
    return comparisons  # 比較回数を返す

def bubble_sort_bench(data):
    """バブルソート最適化版（ベンチマーク用）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(n):  # パスを繰り返す
        swapped = False  # 交換フラグ
        for j in range(n - 1, i, -1):  # 比較する
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j - 1] > data[j]:  # 左が大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # フラグを立てる
        if not swapped:  # 交換なしの場合
            break  # 終了する
    return comparisons  # 比較回数を返す

# --- データ生成関数 ---
size = 1000  # データサイズを設定する

def make_random():
    """ランダムデータを生成する"""
    data = []  # リストを初期化する
    for i in range(size):  # size個生成する
        data.append(random.randint(0, 10000))  # ランダム整数を追加する
    return data  # データを返す

def make_nearly_sorted():
    """ほぼ整列済みデータを生成する"""
    data = list(range(size))  # 整列済みリストを作成する
    for i in range(size // 10):  # 10%を入れ替える
        a = random.randint(0, size - 1)  # ランダムな位置
        b = random.randint(0, size - 1)  # ランダムな位置
        data[a], data[b] = data[b], data[a]  # 入れ替える
    return data  # データを返す

def make_reversed():
    """逆順データを生成する"""
    return list(range(size, 0, -1))  # 逆順リストを返す

# --- 計測と表示 ---
print(f"=== 3パターンの性能比較 (N={size}) ===\n")  # 見出しを表示する
print(f"{'パターン':<14} {'アルゴリズム':<20} {'比較回数':<14} {'時間(秒)'}")  # ヘッダー
print("-" * 60)  # 区切り線を表示する

patterns = [("ランダム", make_random()), ("ほぼ整列済み", make_nearly_sorted()), ("逆順", make_reversed())]  # パターンリスト

for name, data in patterns:  # 各パターンについて処理する
    # 挿入ソート
    start = time.time()  # 計測開始
    ins_c = insertion_sort_bench(data[:])  # 挿入ソートを実行する
    ins_t = time.time() - start  # 時間を計算する
    print(f"{name:<14} {'挿入ソート':<20} {ins_c:<14} {ins_t:.4f}")  # 結果を表示する

    # バブルソート
    start = time.time()  # 計測開始
    bub_c = bubble_sort_bench(data[:])  # バブルソートを実行する
    bub_t = time.time() - start  # 時間を計算する
    print(f"{'':<14} {'バブルソート(最適化)':<20} {bub_c:<14} {bub_t:.4f}")  # 結果を表示する
    print()  # 空行を表示する
```

### 課題9の解答例

```python
# ===== 課題9: データパターン別のソート過程可視化 =====

import random  # ランダムデータ生成用モジュール

def insertion_sort_visual(data, label):
    """挿入ソートの過程をテキストで可視化する関数"""
    n = len(data)  # 配列の長さを取得する
    total_shifts = 0  # 移動回数の合計を初期化する

    print(f"\n=== {label} ===")  # ラベルを表示する
    print(f"初期: {data}")  # 初期状態を表示する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する
        step_shifts = 0  # このステップの移動回数を初期化する

        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
            data[j + 1] = data[j]  # 要素を右にずらす
            step_shifts = step_shifts + 1  # 移動回数を加算する
            j = j - 1  # 1つ左に移動する

        data[j + 1] = key  # keyを正しい位置に挿入する
        total_shifts = total_shifts + step_shifts  # 合計に加算する

        # --- 棒グラフ風表示 ---
        bar = ""  # 棒の文字列を初期化する
        for k in range(n):  # 各要素について処理する
            if k <= i:  # ソート済み部分の場合
                bar = bar + f"[{data[k]:>2}]"  # ソート済みの値を表示する
            else:  # 未整列部分の場合
                bar = bar + f" {data[k]:>2} "  # 未整列の値を表示する
        print(f"  S{i:>2}: {bar} (移動{step_shifts}回)")  # ステップ情報を表示する

    print(f"完了: {data}")  # 最終結果を表示する
    print(f"移動回数の合計: {total_shifts}")  # 移動回数の合計を表示する
    return total_shifts  # 移動回数を返す

# --- 3パターンのデータを生成する ---
size = 20  # データサイズを設定する

random_data = []  # ランダムデータを初期化する
for i in range(size):  # size個生成する
    random_data.append(random.randint(1, 99))  # ランダム整数を追加する

nearly_sorted = list(range(1, size + 1))  # ほぼ整列済みデータを作成する
for i in range(size // 10):  # 10%を入れ替える
    a = random.randint(0, size - 1)  # ランダムな位置
    b = random.randint(0, size - 1)  # ランダムな位置
    nearly_sorted[a], nearly_sorted[b] = nearly_sorted[b], nearly_sorted[a]  # 入れ替える

reversed_data = list(range(size, 0, -1))  # 逆順データを作成する

# --- 各パターンでソートする ---
shifts1 = insertion_sort_visual(random_data[:], "ランダムデータ")  # ランダムデータをソートする
shifts2 = insertion_sort_visual(nearly_sorted[:], "ほぼ整列済みデータ")  # ほぼ整列済みをソートする
shifts3 = insertion_sort_visual(reversed_data[:], "逆順データ")  # 逆順データをソートする

# --- 比較 ---
print(f"\n=== 移動回数の比較 ===")  # 比較の見出しを表示する
print(f"  ランダム:       {shifts1}回")  # ランダムの結果を表示する
print(f"  ほぼ整列済み:   {shifts2}回")  # ほぼ整列済みの結果を表示する
print(f"  逆順:           {shifts3}回")  # 逆順の結果を表示する
```

### 課題10の解答例

```python
# ===== 課題10: 4アルゴリズムの総合ベンチマーク =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール
import bisect  # 二分探索モジュールをインポートする

def insertion_sort(data):
    """通常の挿入ソート"""
    n = len(data)  # 配列の長さを取得する
    for i in range(1, n):  # 2番目から処理する
        key = data[i]  # 挿入する値
        j = i - 1  # 比較開始位置
        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間
            data[j + 1] = data[j]  # 右にずらす
            j = j - 1  # 左に移動する
        data[j + 1] = key  # keyを挿入する
    return data  # ソート済み配列を返す

def binary_insertion_sort(data):
    """二分挿入ソート（bisect使用）"""
    n = len(data)  # 配列の長さを取得する
    for i in range(1, n):  # 2番目から処理する
        key = data[i]  # 挿入する値
        position = bisect.bisect_left(data, key, 0, i)  # 挿入位置を求める
        for j in range(i, position, -1):  # 要素をずらす
            data[j] = data[j - 1]  # 1つ右にずらす
        data[position] = key  # keyを挿入する
    return data  # ソート済み配列を返す

def bubble_sort_optimized(data):
    """バブルソート最適化版"""
    n = len(data)  # 配列の長さを取得する
    for i in range(n):  # パスを繰り返す
        swapped = False  # 交換フラグ
        for j in range(n - 1, i, -1):  # 比較する
            if data[j - 1] > data[j]:  # 左が大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # フラグを立てる
        if not swapped:  # 交換なしの場合
            break  # 終了する
    return data  # ソート済み配列を返す

def python_sorted(data):
    """Python組み込みsorted()"""
    return sorted(data)  # sorted()でソートして返す

def measure_time(func, data):
    """ソート関数の実行時間を計測する関数"""
    data_copy = data[:]  # データのコピーを作成する
    start = time.time()  # 計測を開始する
    func(data_copy)  # ソートを実行する
    elapsed = time.time() - start  # 経過時間を計算する
    return elapsed  # 時間を返す

# --- データ生成 ---
size = 3000  # データサイズを設定する

def make_random():
    """ランダムデータ"""
    data = []  # リストを初期化する
    for i in range(size):  # size個生成する
        data.append(random.randint(0, 10000))  # ランダム整数を追加する
    return data  # データを返す

def make_nearly_sorted():
    """ほぼ整列済みデータ"""
    data = list(range(size))  # 整列済みリストを作成する
    for i in range(size // 10):  # 10%を入れ替える
        a = random.randint(0, size - 1)  # ランダムな位置
        b = random.randint(0, size - 1)  # ランダムな位置
        data[a], data[b] = data[b], data[a]  # 入れ替える
    return data  # データを返す

def make_reversed():
    """逆順データ"""
    return list(range(size, 0, -1))  # 逆順リストを返す

# --- ベンチマーク実行 ---
algorithms = [  # アルゴリズムのリストを定義する
    ("挿入ソート", insertion_sort),
    ("二分挿入ソート", binary_insertion_sort),
    ("バブルソート(最適化)", bubble_sort_optimized),
    ("Python sorted()", python_sorted)
]

patterns = [  # データパターンのリストを定義する
    ("ランダム", make_random()),
    ("ほぼ整列済み", make_nearly_sorted()),
    ("逆順", make_reversed())
]

print(f"=== 総合ベンチマーク (N={size}) ===\n")  # 見出しを表示する

# --- 結果を格納する ---
results = {}  # 結果の辞書を初期化する
for algo_name, algo_func in algorithms:  # 各アルゴリズムの辞書を初期化する
    results[algo_name] = {}  # 空の辞書を作成する

# --- 計測 ---
for pattern_name, pattern_data in patterns:  # 各パターンについて処理する
    print(f"--- {pattern_name}データ ---")  # パターン名を表示する
    for algo_name, algo_func in algorithms:  # 各アルゴリズムについて処理する
        elapsed = measure_time(algo_func, pattern_data)  # 実行時間を計測する
        results[algo_name][pattern_name] = elapsed  # 結果を保存する
        print(f"  {algo_name:<22}: {elapsed:.4f} 秒")  # 結果を表示する
    print()  # 空行を表示する

# --- 結果を表形式で表示する ---
print("=" * 72)  # 区切り線を表示する
print(f"{'アルゴリズム':<22} | {'ランダム':>10} | {'ほぼ整列済み':>10} | {'逆順':>10}")  # ヘッダーを表示する
print("-" * 72)  # 区切り線を表示する

for algo_name, algo_func in algorithms:  # 各アルゴリズムについて結果を表示する
    r = results[algo_name]  # そのアルゴリズムの結果を取得する
    print(f"{algo_name:<22} | {r['ランダム']:>10.4f} | {r['ほぼ整列済み']:>10.4f} | {r['逆順']:>10.4f}")  # 表示する

# --- 考察 ---
print(f"\n=== 考察 ===")  # 考察の見出しを表示する
print("1. Python組み込みsorted()はTimsort(O(n log n))を使用しており圧倒的に速い")  # 考察1
print("2. 二分挿入ソートは比較回数が少ないため通常の挿入ソートより若干速い")  # 考察2
print("3. バブルソート(最適化版)はほぼ整列済みデータで大幅に高速化される")  # 考察3
print("4. 逆順データは挿入ソート・バブルソートの最悪ケース(O(n^2))")  # 考察4
print("5. データの初期状態がアルゴリズムの性能に大きく影響する")  # 考察5
```

### 発展課題1の解答例

```python
# ===== 発展課題1: シェルソートの実装 =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def shell_sort(data):
    """シェルソート（間隔列: n//2, n//4, ..., 1）"""
    n = len(data)  # 配列の長さを取得する
    gap = n // 2  # 初期間隔をn//2に設定する
    comparisons = 0  # 比較回数を初期化する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print(f"配列の長さ: {n}")  # 長さを表示する

    while gap > 0:  # 間隔が0より大きい間繰り返す
        print(f"\n--- 間隔 = {gap} ---")  # 間隔を表示する

        for i in range(gap, n):  # gap番目から最後まで処理する
            key = data[i]  # 挿入する値を取り出す
            j = i  # 比較位置を設定する

            while j >= gap:  # gap以上離れた要素と比較する
                comparisons = comparisons + 1  # 比較回数を加算する
                if data[j - gap] > key:  # gap離れた要素がkeyより大きい場合
                    data[j] = data[j - gap]  # 要素をgap分右にずらす
                    j = j - gap  # gap分左に移動する
                else:  # key以下の場合
                    break  # ループを終了する

            data[j] = key  # keyを正しい位置に挿入する

        print(f"  結果: {data}")  # 結果を表示する
        gap = gap // 2  # 間隔を半分にする

    print(f"\nソート完了: {data}")  # 最終結果を表示する
    print(f"比較回数: {comparisons}")  # 比較回数を表示する
    return data, comparisons  # 結果を返す

def insertion_sort_bench(data):
    """挿入ソート（ベンチマーク用）"""
    n = len(data)  # 配列の長さを取得する
    comparisons = 0  # 比較回数を初期化する
    for i in range(1, n):  # 2番目から処理する
        key = data[i]  # 挿入する値
        j = i - 1  # 比較開始位置
        while j >= 0:  # 左端まで探す
            comparisons = comparisons + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 右にずらす
                j = j - 1  # 左に移動する
            else:  # key以下の場合
                break  # 終了する
        data[j + 1] = key  # keyを挿入する
    return comparisons  # 比較回数を返す

def shell_sort_bench(data):
    """シェルソート（ベンチマーク用、表示なし）"""
    n = len(data)  # 配列の長さを取得する
    gap = n // 2  # 初期間隔を設定する
    comparisons = 0  # 比較回数を初期化する
    while gap > 0:  # 間隔が0より大きい間
        for i in range(gap, n):  # gap番目から処理する
            key = data[i]  # 挿入する値
            j = i  # 比較位置
            while j >= gap:  # gap以上離れた要素と比較する
                comparisons = comparisons + 1  # 比較回数を加算する
                if data[j - gap] > key:  # gap離れた要素が大きい場合
                    data[j] = data[j - gap]  # ずらす
                    j = j - gap  # 移動する
                else:  # key以下の場合
                    break  # 終了する
            data[j] = key  # keyを挿入する
        gap = gap // 2  # 間隔を半分にする
    return comparisons  # 比較回数を返す

# --- 小さいデータでトレース表示 ---
print("=== シェルソート（トレース表示） ===")  # 見出しを表示する
shell_sort([38, 27, 43, 3, 9, 82, 10, 15])  # トレース表示付きでソートする

# --- 性能比較 ---
print("\n\n=== 性能比較 ===\n")  # 見出しを表示する
test_size = 3000  # テストサイズを設定する
test_data = []  # テストデータを初期化する
for i in range(test_size):  # size個のランダム整数を生成する
    test_data.append(random.randint(0, 10000))  # ランダム整数を追加する

# 挿入ソート
start = time.time()  # 計測開始
ins_c = insertion_sort_bench(test_data[:])  # 実行する
ins_t = time.time() - start  # 時間を計算する

# シェルソート
start = time.time()  # 計測開始
shell_c = shell_sort_bench(test_data[:])  # 実行する
shell_t = time.time() - start  # 時間を計算する

print(f"データサイズ: {test_size}")  # データサイズを表示する
print(f"{'アルゴリズム':<16} {'比較回数':<16} {'実行時間(秒)'}")  # ヘッダーを表示する
print("-" * 48)  # 区切り線を表示する
print(f"{'挿入ソート':<16} {ins_c:<16} {ins_t:.4f}")  # 挿入ソートの結果
print(f"{'シェルソート':<16} {shell_c:<16} {shell_t:.4f}")  # シェルソートの結果

if ins_t > 0 and shell_t > 0:  # 両方の時間が正の場合
    speedup = ins_t / shell_t  # 速度比を計算する
    print(f"\nシェルソートは挿入ソートの約 {speedup:.1f} 倍高速")  # 比較結果を表示する
```

### 発展課題2の解答例

```python
# ===== 発展課題2: matplotlibで比較グラフを作成する =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール
import bisect  # 二分探索モジュール
import matplotlib.pyplot as plt  # グラフ描画ライブラリ

def insertion_sort(data):
    """通常の挿入ソート"""
    for i in range(1, len(data)):  # 2番目から処理する
        key = data[i]  # 挿入する値
        j = i - 1  # 比較開始位置
        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間
            data[j + 1] = data[j]  # 右にずらす
            j = j - 1  # 左に移動する
        data[j + 1] = key  # keyを挿入する
    return data  # ソート済み配列を返す

def binary_insertion_sort(data):
    """二分挿入ソート"""
    for i in range(1, len(data)):  # 2番目から処理する
        key = data[i]  # 挿入する値
        pos = bisect.bisect_left(data, key, 0, i)  # 挿入位置を求める
        for j in range(i, pos, -1):  # 要素をずらす
            data[j] = data[j - 1]  # 1つ右にずらす
        data[pos] = key  # keyを挿入する
    return data  # ソート済み配列を返す

def bubble_sort_opt(data):
    """バブルソート最適化版"""
    n = len(data)  # 配列の長さを取得する
    for i in range(n):  # パスを繰り返す
        swapped = False  # 交換フラグ
        for j in range(n - 1, i, -1):  # 比較する
            if data[j - 1] > data[j]:  # 左が大きい場合
                data[j - 1], data[j] = data[j], data[j - 1]  # 交換する
                swapped = True  # フラグを立てる
        if not swapped:  # 交換なしの場合
            break  # 終了する
    return data  # ソート済み配列を返す

def measure(func, data):
    """実行時間を計測する関数"""
    copy = data[:]  # コピーを作成する
    start = time.time()  # 計測開始
    func(copy)  # ソートを実行する
    return time.time() - start  # 経過時間を返す

# --- データ生成 ---
size = 3000  # データサイズを設定する

random_data = [random.randint(0, 10000) for _ in range(size)]  # ランダムデータ
nearly_sorted = list(range(size))  # ほぼ整列済みデータ
for i in range(size // 10):  # 10%を入れ替える
    a = random.randint(0, size - 1)  # 位置a
    b = random.randint(0, size - 1)  # 位置b
    nearly_sorted[a], nearly_sorted[b] = nearly_sorted[b], nearly_sorted[a]  # 入れ替え
reversed_data = list(range(size, 0, -1))  # 逆順データ

# --- 計測 ---
algos = [  # アルゴリズムリスト
    ("挿入ソート", insertion_sort),
    ("二分挿入ソート", binary_insertion_sort),
    ("バブルソート(最適化)", bubble_sort_opt),
    ("Python sorted()", sorted)
]

patterns = [("ランダム", random_data), ("ほぼ整列済み", nearly_sorted), ("逆順", reversed_data)]  # パターンリスト

results = {}  # 結果辞書を初期化する
for name, func in algos:  # 各アルゴリズムの辞書を作成する
    results[name] = {}  # 空辞書を設定する

print(f"=== 計測中 (N={size}) ===")  # 見出しを表示する
for pname, pdata in patterns:  # 各パターンについて計測する
    print(f"\n{pname}:")  # パターン名を表示する
    for aname, afunc in algos:  # 各アルゴリズムについて計測する
        t = measure(afunc, pdata)  # 実行時間を計測する
        results[aname][pname] = t  # 結果を保存する
        print(f"  {aname}: {t:.4f}秒")  # 結果を表示する

# --- グラフ描画 ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # 3つのサブプロットを作成する
pattern_names = ["ランダム", "ほぼ整列済み", "逆順"]  # パターン名のリスト
colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6"]  # 棒グラフの色リスト

for idx in range(3):  # 各パターンについてグラフを描画する
    pname = pattern_names[idx]  # パターン名を取得する
    ax = axes[idx]  # サブプロットを取得する
    algo_names = [name for name, _ in algos]  # アルゴリズム名のリスト
    times = [results[name][pname] for name in algo_names]  # 実行時間のリスト

    bars = ax.bar(algo_names, times, color=colors)  # 棒グラフを描画する
    ax.set_title(f"{pname}データ", fontsize=14)  # タイトルを設定する
    ax.set_ylabel("実行時間(秒)")  # y軸ラベルを設定する
    ax.tick_params(axis="x", rotation=30)  # x軸ラベルを回転する

    for bar, t in zip(bars, times):  # 各棒の上に数値を表示する
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),  # 位置を設定する
                f"{t:.4f}", ha="center", va="bottom", fontsize=9)  # 数値を表示する

plt.suptitle(f"ソートアルゴリズム性能比較 ({size}要素)", fontsize=16)  # 全体タイトルを設定する
plt.tight_layout()  # レイアウトを調整する
plt.show()  # グラフを表示する
```

---

## 6. まとめ

| アルゴリズム | 最良 | 平均 | 最悪 | 安定性 | 特徴 |
|---|---|---|---|---|---|
| 挿入ソート | O(n) | O(n^2) | O(n^2) | 安定 | ほぼ整列済みに強い |
| 二分挿入ソート | O(n log n) 比較 | O(n^2) | O(n^2) | 安定 | 比較回数を削減 |
| バブルソート | O(n) | O(n^2) | O(n^2) | 安定 | 実装が単純 |
| シェルソート | O(n log n) | O(n^1.5) | O(n^2) | 不安定 | 間隔を縮めて挿入ソート |
| Python sorted() | O(n) | O(n log n) | O(n log n) | 安定 | Timsort、実用最速 |

**ポイント:**
- 二分探索で「探す」部分は速くなるが、「ずらす」部分は変わらない
- バブルソートの最適化は、整列済みデータの検出に効果的
- 実用ではPython組み込みの `sorted()` を使うべきだが、アルゴリズムの理解が重要
