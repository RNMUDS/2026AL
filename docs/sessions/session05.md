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

### ジャンプ探索と指数探索 — 何が違う？どう使い分ける？

二分探索を学んだあとに登場する **ジャンプ探索** と **指数探索** は、どちらも「ソート済みデータを高速に探す」という目的では似ています。しかし **「どうやって探索範囲を狭めるか」** と **「データ数 n を最初に知っているか」** という2点で大きく違います。

#### 共通点

- 両方とも **ソート済み** であることが前提
- どちらも **2段階** の探索（まず大ざっぱに範囲を絞り、次にその範囲を詳しく調べる）
- 純粋な逐次探索 O(n) よりは速い

#### 違い① — 範囲の絞り方

| | ジャンプ探索 | 指数探索 |
|---|---|---|
| 第1段階のジャンプ幅 | **固定** `√n` ずつ | **倍々**（1, 2, 4, 8, 16, …） |
| 第2段階の探索方法 | ブロック内を **逐次探索** | 絞り込んだ範囲で **二分探索** |
| 計算量 | O(√n) | O(log n) |
| データ数 n の事前知識 | **必要**（√n を計算するため） | **不要**（端を知らなくても進める） |

#### 違い② — 探索の手順をフローで見る

**ジャンプ探索の流れ**（例: n=100, target=42, ジャンプ幅=√100=10）

```
ステップ1: √n=10 ずつ「飛び石」のように進む
  [0] [1] ... [9] [10] [11] ... [19] [20] ... [29] [30] ... [39] [40] ... [49] ...
   ↑               ↑                ↑                ↑                ↑
   0 を見る         10 を見る         20 を見る         30 を見る         40 を見る
   (0 < 42 OK)      (10 < 42 OK)      (20 < 42 OK)      (30 < 42 OK)      (40 < 42 OK)
                                                                          ↓
                                                                          次は50で42を超える!

ステップ2: 一つ前のブロック [40, 49] に target がいるはず → ブロック内を1つずつ確認
  data[40]=40 → ✗
  data[41]=41 → ✗
  data[42]=42 → ✓ 見つかった!
```

ポイント: **「行き過ぎたら一つ前のブロックに戻って、そこを逐次探索」** が本質。`√n` ジャンプ + `√n` 逐次 = 合計 O(√n)。

**指数探索の流れ**（例: target=42、データ数は不明 or 巨大）

```
ステップ1: bound を 2倍ずつ広げていく
  bound=1   : data[1]=1   < 42  → さらに広げる
  bound=2   : data[2]=2   < 42  → さらに広げる
  bound=4   : data[4]=4   < 42  → さらに広げる
  bound=8   : data[8]=8   < 42  → さらに広げる
  bound=16  : data[16]=16 < 42  → さらに広げる
  bound=32  : data[32]=32 < 42  → さらに広げる
  bound=64  : data[64]=64 ≥ 42  → ストップ! target は [32, 64] の間にいる

ステップ2: 範囲 [32, 64] に対して「二分探索」を実行
  ← ここで前回学んだ二分探索がそのまま使える!
  mid=48 → data[48]=48 > 42 → 右半分を捨てる → 範囲 [32, 47]
  mid=39 → data[39]=39 < 42 → 左半分を捨てる → 範囲 [40, 47]
  mid=43 → data[43]=43 > 42 → 右半分を捨てる → 範囲 [40, 42]
  mid=41 → data[41]=41 < 42 → 左半分を捨てる → 範囲 [42, 42]
  mid=42 → data[42]=42 = 42 → ✓ 見つかった!
```

ポイント: **「範囲を倍々に広げて当たり地点を超えたら、そこから二分探索」**。

#### 違い③ — どこで二分探索を呼んでいる？

ここが最初に混乱しやすいところです。**指数探索は中身で二分探索を呼び出します**。

```
指数探索(data, target):
    bound = 1
    while bound < n and data[bound] < target:   # ← ここはステップ1（指数的に広げる）
        bound = bound * 2

    # ↓ ここでステップ2として「二分探索」を呼ぶ!
    return binary_search(data, target, 範囲=[bound//2, min(bound, n-1)])
```

つまり指数探索とは **「二分探索を実行する前に、適切な探索区間 [L, R] を素早く見つけるための前処理」** です。
二分探索は「`left` と `right` がわかっていないと始められない」のですが、データ数 n がわからない状況では `right` を決められません。指数探索は **`right` を見つけるための仕組み** とも言えます。

#### 違い④ — データ数 n が「わかる」か「わからない」かで選ぶ

最大の判断基準はここです。

**ジャンプ探索を選ぶ場面**

- データ数 n が **事前にわかっている**（普通の Python リストなど `len(data)` がすぐ得られる）
- ランダムアクセス（任意の位置 `data[i]` への参照）は可能だが、できれば「インデックス計算は単純に」したい
- 教育的な題材として「逐次探索より速く、二分探索より単純」な中間例を見たい

**指数探索を選ぶ場面**

- データ数 n が **未知**、または非常に大きい（例: ストリーミングデータ、巨大ファイル、無限数列、API ページネーション）
- 探したい値が **配列の先頭付近にあると予想される**。倍々に広げるので、target が先頭近くなら数回で済む（二分探索は毎回 n/2 から始まるので、先頭付近の値でも `log n` 回必要）
- 「終端がどこかわからないが、ソートされてはいる」ようなデータに対して二分探索を適用したい

| 状況 | おすすめ |
|---|---|
| 普通の Python リストで `len()` が使える | **二分探索 / bisect**（最も高速 O(log n)） |
| 同上だがアルゴリズム比較として | ジャンプ探索 |
| データ数不明・巨大・先頭付近を高速に探したい | **指数探索** |

#### まとめの一言

- **ジャンプ探索** = 「√n 幅で飛び石、当たりブロックを逐次探索」。n が既知のときの中間的選択肢。
- **指数探索** = 「倍々に広げて範囲を見つけ、その範囲を二分探索」。n が未知 / 巨大なときの強力な選択肢。
- 計算量は **指数探索 O(log n) > ジャンプ探索 O(√n)** で指数探索が速いが、ジャンプ探索は実装が簡単という良さがある。

---

## 例題

### 例題1: bisect_left と bisect_right の違い

```python
import bisect

def show_bisect(data, target):
    """bisect_left と bisect_right の位置を表示する"""
    left_pos = bisect.bisect_left(data, target)
    right_pos = bisect.bisect_right(data, target)
    print(f"  bisect_left(data, {target})  = {left_pos}")
    print(f"  bisect_right(data, {target}) = {right_pos}")
    return (left_pos, right_pos)

# --- 重複なしのデータで動作確認 ---
data = [1, 3, 5, 7, 9, 11, 13]
show_bisect(data, 5)   # 存在する値
show_bisect(data, 8)   # 存在しない値（8を挿入する位置）

# --- 重複ありのデータで動作確認 ---
data_dup = [1, 3, 5, 5, 5, 7, 9]
left_pos, right_pos = show_bisect(data_dup, 5)
print(f"  5の個数: {right_pos - left_pos}個")
print(f"  スライス: {data_dup[left_pos:right_pos]}")
```

**やってみよう（1分）**: `data_dup` で `bisect_left(data_dup, 4)` と `bisect_right(data_dup, 4)` を試してみよう。存在しない値のとき left と right は同じになる？

---

### 例題2: insort でソート済みリストを維持する

```python
import bisect

sorted_list = []
values = [7, 3, 11, 1, 9, 5, 13, 2, 8]

for value in values:
    insert_pos = bisect.bisect_left(sorted_list, value)
    bisect.insort(sorted_list, value)
    print(f"  insort({value:>2}) → 位置{insert_pos}に挿入 → {sorted_list}")

print(f"\n最終結果: {sorted_list}")
```

**やってみよう（1分）**: `values` の末尾に `5` を追加して `[7, 3, 11, 1, 9, 5, 13, 2, 8, 5]` にして実行してみよう。

---

### 例題3: ジャンプ探索

```python
import math

def jump_search(data, target):
    """ジャンプ探索: sqrt(n)ずつジャンプ → ブロック内を逐次探索"""
    n = len(data)
    jump_size = int(math.sqrt(n))
    print(f"  データ数: {n}, ジャンプ幅: {jump_size}")

    # ステップ1: ジャンプしてブロックを特定する
    prev = 0
    curr = 0
    while curr < n and data[curr] < target:
        prev = curr
        curr += jump_size
        print(f"  ジャンプ: 位置{curr}をチェック")

    # ステップ2: ブロック内を逐次探索する
    block_end = min(curr, n - 1)
    print(f"  ブロック内探索: 位置{prev}〜{block_end}")
    for i in range(prev, block_end + 1):
        if data[i] == target:
            return i
    return -1

data = list(range(0, 100))
result = jump_search(data, 42)
print(f"  結果: インデックス{result}")
```

**やってみよう（1分）**: `jump_search(data, 99)` を試してみよう。ジャンプとブロック内探索の出力を観察しよう。

---

### 例題4: 指数探索

```python
def exponential_search(data, target):
    """指数探索: 指数的に範囲を広げてから二分探索"""
    n = len(data)
    if n == 0:
        return -1
    if data[0] == target:
        return 0

    # ステップ1: 指数的にインデックスを広げる
    bound = 1
    while bound < n and data[bound] < target:
        print(f"    bound={bound}, data[{bound}]={data[bound]}")
        bound *= 2

    # ステップ2: 絞り込んだ範囲で二分探索
    left = bound // 2
    right = min(bound, n - 1)
    print(f"  二分探索: [{left}..{right}]")

    while left <= right:
        mid = (left + right) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

data = list(range(0, 200))
result = exponential_search(data, 42)
print(f"  結果: インデックス{result}")
```

**やってみよう（1分）**: `exponential_search(data, 2)` を試してみよう。先頭付近の値を探すとき、bound はどこまで広がる？

---

### 例題5: 複数の探索アルゴリズムの性能比較

```python
import time, random, bisect

def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

def binary_search(data, target):
    left = 0
    right = len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def bisect_search(data, target):
    idx = bisect.bisect_left(data, target)
    if idx < len(data) and data[idx] == target:
        return idx
    return -1

# --- ベンチマーク ---
n = 100000
data = list(range(n))
targets = [random.randint(0, n - 1) for _ in range(500)]

algorithms = [
    ("Linear Search", linear_search),
    ("Binary Search", binary_search),
    ("Bisect Search", bisect_search),
]

results = []
for name, func in algorithms:
    start = time.perf_counter()
    for t in targets:
        func(data, t)
    elapsed = time.perf_counter() - start
    results.append((name, elapsed))

results.sort(key=lambda x: x[1])
for rank, (name, elapsed) in enumerate(results, 1):
    print(f"  {rank}位: {name:<18} {elapsed:.4f}秒")
```

**やってみよう（1分）**: `n = 100000` を `n = 1000000`（100万件）に変えて実行してみよう。順位は変わる？

---

## 標準課題

### 標準課題1: bisect_left と bisect_right の出力を予測する

以下の各ケースで `bisect_left` と `bisect_right` の返り値を **実行せずに** 予測しなさい。

```
data = [1, 3, 5, 5, 5, 7, 9, 11]
```

| target      | bisect_left | bisect_right | 個数 |
|-------------|-------------|--------------|------|
| 5           |             |              |      |
| 6（不在）   |             |              |      |
| 1（先頭）   |             |              |      |
| 15（範囲外）|             |              |      |

---

### 標準課題2: bisect＋insortコードのトレース

以下のコードを **実行せずに**、ループの各ステップで `sorted_list` と `pos` がどう変化するかを追い、最終出力を予測しなさい。予測を書いた後に、`AL05-3.py` として保存・実行して確かめなさい。

```python
from bisect import bisect_left, insort

values = [7, 3, 11, 1, 9, 3]
sorted_list = []

for v in values:
    pos = bisect_left(sorted_list, v)
    print(f"v={v}: pos={pos}, ", end="")
    insort(sorted_list, v)
    print(f"list={sorted_list}")

print(f"最終: {sorted_list}")
print(f"3の個数: {bisect_left(sorted_list, 4) - bisect_left(sorted_list, 3)}")
```

提出項目:
- Q1: 各ステップの `pos` と `sorted_list` の変化のトレース
- Q2: 最終出力の予測（最終リストと3の個数）
- Q3: 実行結果（予測と合っていたか）

---

## 発展課題

### 発展課題: ジャンプ探索と二分探索の比較

ジャンプ探索と二分探索の性能を実際に比較するプログラムを作成しなさい。データサイズ n=100, 10000, 1000000 の場合の比較回数を計測し、結果を出力すること。

提出要件（2点セット）:
1. **コード**: `AL05-4.py` として作成し、コード全体をNotionノートに貼り付ける
2. **音声説明**: 以下の内容を 1〜2分の音声で録音し、Notionノートに添付する
   - ジャンプ探索と二分探索をそれぞれどう実装したか
   - データサイズごとの比較回数の結果と、O(sqrt(n)) vs O(log n) の違い
   - どのような場面でジャンプ探索が有利になりうるか

---

## 解答例

### 標準課題1 解答

`data = [1, 3, 5, 5, 5, 7, 9, 11]`（要素数8）:

| target      | bisect_left | bisect_right | 個数 | 解説 |
|-------------|-------------|--------------|------|------|
| 5           | 2           | 5            | 3    | 位置 [2][3][4] に 5 が3個 |
| 6（不在）   | 5           | 5            | 0    | 5 と 7 の間。存在しない値は left=right |
| 1（先頭）   | 0           | 1            | 1    | 先頭に 1 が1個 |
| 15（範囲外）| 8           | 8            | 0    | 範囲外 → 挿入位置はリスト長 8 |

**ポイント:** `個数 = bisect_right - bisect_left`。存在しない値は `left = right` で個数 0、範囲外は配列長と同じインデックスを返す。

---

### 標準課題2 解答

トレース表:

| v  | pos | insort 後の sorted_list |
|----|-----|-------------------------|
| 7  | 0   | [7]                     |
| 3  | 0   | [3, 7]                  |
| 11 | 2   | [3, 7, 11]              |
| 1  | 0   | [1, 3, 7, 11]           |
| 9  | 3   | [1, 3, 7, 9, 11]        |
| 3  | 1   | [1, 3, 3, 7, 9, 11]     |

最終出力:

```
v=7: pos=0, list=[7]
v=3: pos=0, list=[3, 7]
v=11: pos=2, list=[3, 7, 11]
v=1: pos=0, list=[1, 3, 7, 11]
v=9: pos=3, list=[1, 3, 7, 9, 11]
v=3: pos=1, list=[1, 3, 3, 7, 9, 11]
最終: [1, 3, 3, 7, 9, 11]
3の個数: 2
```

`3の個数: bisect_left(sorted_list, 4) - bisect_left(sorted_list, 3) = 3 - 1 = 2`

---

### 発展課題 解答例

```python
# ===== 発展課題: ジャンプ探索と二分探索の比較 =====

import math
import random

# --- ジャンプ探索（比較回数を計測） ---
def jump_search(data, target):
    """ジャンプ探索: (見つかったか, 比較回数) を返す"""
    n = len(data)
    step = int(math.sqrt(n))
    count = 0

    prev = 0
    while prev < n and data[min(prev + step, n) - 1] < target:
        count += 1
        prev += step
        if prev >= n:
            return False, count

    for i in range(prev, min(prev + step, n)):
        count += 1
        if data[i] == target:
            return True, count

    return False, count

# --- 二分探索（比較回数を計測） ---
def binary_search(data, target):
    """二分探索: (見つかったか, 比較回数) を返す"""
    low = 0
    high = len(data) - 1
    count = 0

    while low <= high:
        mid = (low + high) // 2
        count += 1
        if data[mid] == target:
            return True, count
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return False, count

# --- 実験 ---
sizes = [100, 10000, 1000000]
trials = 100

print(f"{'データサイズ':>12} | {'ジャンプ探索':>12} | {'二分探索':>10} | {'理論値 sqrt(n)':>14} | {'理論値 log2(n)':>14}")
print("-" * 75)

for n in sizes:
    data = list(range(n))
    total_jump = 0
    total_binary = 0

    for _ in range(trials):
        target = random.randint(0, n - 1)
        _, jcount = jump_search(data, target)
        _, bcount = binary_search(data, target)
        total_jump += jcount
        total_binary += bcount

    avg_jump = total_jump / trials
    avg_binary = total_binary / trials
    theory_jump = math.sqrt(n)
    theory_binary = math.log2(n)

    print(f"{n:>12,} | {avg_jump:>12.1f} | {avg_binary:>10.1f} | {theory_jump:>14.1f} | {theory_binary:>14.1f}")
```

評価ポイント:
- ジャンプ探索は sqrt(n) 幅でブロックを飛ばし、該当ブロック内で逐次探索する2段階の方法
- 二分探索 O(log n) はジャンプ探索 O(sqrt(n)) より常に比較回数が少ない（n が大きいほど差が開く）
- データサイズが大きくなると差が顕著になる（例: n=1,000,000 で sqrt(n)=1000 vs log2(n)=20）
- ジャンプ探索は実装が単純で、「前方にしか進めない」データ構造で有利になる場合がある
