# 第3回: 探索アルゴリズム（逐次探索）

## 説明

### この授業で学ぶこと

- 「探索（Search）」とは何かを理解する
- 逐次探索（線形探索）のアルゴリズムを実装できる
- 計算量 O(n) の意味を直感的に理解する
- 比較回数を数えてアルゴリズムの効率を評価できる

---

### 1. 探索とは何か？

私たちは日常生活で常に「探索」をしています。

| 場面 | やっていること |
|------|---------------|
| 本棚から本を探す | 1冊ずつ背表紙を見て、目的の本か確認する |
| 電話帳で名前を探す | ページをめくりながら名前を探す |
| 出席簿で名前を探す | 上から順に名前を確認する |
| LINEで友達を探す | 友達リストを上からスクロールする |

これらはすべて **「データの集まりの中から、目的のデータを見つける」** という操作です。
コンピュータサイエンスでは、これを **探索（Search）** と呼びます。

### 2. 逐次探索（線形探索）とは

**逐次探索（Sequential Search）** は最もシンプルな探索アルゴリズムです。

**やり方**: データの先頭から順に、1つずつ目的の値と比較していく。

```
データ: [3, 7, 1, 9, 4]
目標値: 9

ステップ1: data[0]=3 → 9と違う → 次へ
ステップ2: data[1]=7 → 9と違う → 次へ
ステップ3: data[2]=1 → 9と違う → 次へ
ステップ4: data[3]=9 → 一致！ → インデックス3を返す
```

### 3. 計算量 O(n) とは

逐次探索の計算量は **O(n)** です。これは：

- データが **10個** なら、最悪 **10回** の比較
- データが **100個** なら、最悪 **100回** の比較
- データが **1,000,000個** なら、最悪 **1,000,000回** の比較

つまり、**データ量が2倍になると、探索時間も2倍になる** ということです。

```
データ数(n)   最悪比較回数   平均比較回数
       10           10            5
      100          100           50
    1,000        1,000          500
1,000,000    1,000,000      500,000
```

---

## 例題と課題

### 例題1: リストの中から値を探す

逐次探索の最も基本的な形です。リストの先頭から順に比較していきます。

```python
# ===================================
# 例題1: 基本的な逐次探索
# ===================================

# --- 探索対象のリスト ---
data = [3, 7, 1, 9, 4]
# 探したい値
target = 9

# --- リストとターゲットを表示する ---
print("=== 逐次探索の基本 ===")
print(f"  データ: {data}")
print(f"  探す値: {target}")
print()

# --- 先頭から順に比較していく ---
found = False  # 見つかったかどうかのフラグ

for i in range(len(data)):
    # 現在の要素を表示する
    print(f"  ステップ{i + 1}: data[{i}] = {data[i]}", end="")

    # ターゲットと比較する
    if data[i] == target:
        # 見つかった場合
        print(f" → {target}と一致！ 発見！")
        found = True
        # 見つかった位置を記録する
        found_index = i
        # ループを抜ける
        break
    else:
        # 一致しない場合
        print(f" → {target}と不一致 → 次へ")

# --- 結果を表示する ---
print()
if found:
    print(f"結果: インデックス {found_index} で発見")
else:
    print(f"結果: {target} は見つかりませんでした")
```

**実行結果:**
```
=== 逐次探索の基本 ===
  データ: [3, 7, 1, 9, 4]
  探す値: 9

  ステップ1: data[0] = 3 → 9と不一致 → 次へ
  ステップ2: data[1] = 7 → 9と不一致 → 次へ
  ステップ3: data[2] = 1 → 9と不一致 → 次へ
  ステップ4: data[3] = 9 → 9と一致！ 発見！

結果: インデックス 3 で発見
```

---

### 標準課題1（超やさしい）: リストから値を探す（見つかる場合）

**課題:** リスト `[15, 3, 27, 8, 42, 11, 36]` から `target = 42` を逐次探索で探すプログラムを作りなさい。

**要件:**
- 先頭から順に1つずつ比較する
- 各ステップで「何番目の要素を比較しているか」を表示する
- 見つかったら「インデックスXで発見」と表示して終了する
- 比較回数も表示する

**期待される出力例:**
```
データ: [15, 3, 27, 8, 42, 11, 36]
探す値: 42
  比較1: data[0] = 15 → 不一致
  比較2: data[1] = 3 → 不一致
  比較3: data[2] = 27 → 不一致
  比較4: data[3] = 8 → 不一致
  比較5: data[4] = 42 → 一致！
結果: インデックス4で発見（比較5回）
```

---

### 標準課題2（超やさしい）: リストから値を探す（見つからない場合）

**課題:** リスト `[15, 3, 27, 8, 42, 11, 36]` から `target = 99` を逐次探索で探すプログラムを作りなさい。

**要件:**
- 先頭から順に1つずつ比較する
- 各ステップの比較状況を表示する
- 最後まで見つからなかったら「見つかりませんでした」と表示する
- 比較回数も表示する（全要素を比較したことを確認する）

**期待される出力例:**
```
データ: [15, 3, 27, 8, 42, 11, 36]
探す値: 99
  比較1: data[0] = 15 → 不一致
  比較2: data[1] = 3 → 不一致
  ...
  比較7: data[6] = 36 → 不一致
結果: 見つかりませんでした（比較7回）
```

---

### 例題2: 関数にまとめた逐次探索

逐次探索を関数として定義し、インデックスと比較回数を返すようにします。

```python
# ===================================
# 例題2: 関数にまとめた逐次探索
# ===================================

def linear_search(data, target):
    """
    逐次探索を行う関数
    - data: 探索対象のリスト
    - target: 探したい値
    - 戻り値: (インデックス, 比較回数) のタプル
              見つからない場合は (-1, 比較回数)
    """
    # 比較回数を記録するカウンター
    comparison_count = 0

    # リストの先頭から順に比較する
    for i in range(len(data)):
        # 比較回数を1増やす
        comparison_count = comparison_count + 1

        # 現在の要素とターゲットを比較する
        if data[i] == target:
            # 見つかった場合: インデックスと比較回数を返す
            return (i, comparison_count)

    # 全て調べたが見つからなかった場合
    return (-1, comparison_count)


# --- テスト ---
test_data = [15, 3, 27, 8, 42, 11, 36, 19, 5, 22]
print(f"データ: {test_data}")
print(f"データ数: {len(test_data)}個")
print("=" * 50)

# いくつかの値を探索してみる
test_targets = [42, 15, 22, 100]

for target in test_targets:
    # 逐次探索を実行する
    index, count = linear_search(test_data, target)

    # 結果を表示する
    if index != -1:
        # 見つかった場合
        print(f"  target={target:>3} → インデックス{index}で発見 (比較{count}回)")
    else:
        # 見つからなかった場合
        print(f"  target={target:>3} → 見つからず (比較{count}回)")
```

**実行結果:**
```
データ: [15, 3, 27, 8, 42, 11, 36, 19, 5, 22]
データ数: 10個
==================================================
  target= 42 → インデックス4で発見 (比較5回)
  target= 15 → インデックス0で発見 (比較1回)
  target= 22 → インデックス9で発見 (比較10回)
  target=100 → 見つからず (比較10回)
```

---

### 標準課題3（やさしい）: 逐次探索関数の実装（位置を返す）

**課題:** 逐次探索関数 `linear_search(data, target)` を自分で実装しなさい。

**要件:**
- 引数: `data`（リスト）、`target`（探す値）
- 戻り値: 見つかった場合は `インデックス`、見つからない場合は `-1`
- `for` ループと `if` 文を使う
- 以下のテストデータで動作確認すること:
  ```python
  fruits = ["apple", "banana", "cherry", "durian", "elderberry"]
  ```
  - `"cherry"` を探す → `2`
  - `"apple"` を探す → `0`（先頭）
  - `"elderberry"` を探す → `4`（末尾）
  - `"mango"` を探す → `-1`（存在しない）

**期待される出力例:**
```
データ: ['apple', 'banana', 'cherry', 'durian', 'elderberry']
  "cherry" → インデックス: 2
  "apple" → インデックス: 0
  "elderberry" → インデックス: 4
  "mango" → インデックス: -1
```

---

### 標準課題4（やさしい）: 探索結果のエラーハンドリング

**課題:** 逐次探索で見つからなかった場合に、適切なメッセージを表示するプログラムを作りなさい。

**要件:**
- `linear_search` 関数を使う（戻り値が `-1` なら見つからなかった）
- 見つかった場合: `"'{target}' はインデックス{index}にあります"` と表示
- 見つからなかった場合: `"'{target}' はリストに存在しません"` と表示
- ユーザーが探す値を `input()` で入力できるようにする
- `"quit"` と入力したら終了する

**期待される出力例:**
```
=== 単語検索 ===
データ: ['apple', 'banana', 'cherry', 'durian', 'elderberry']
探す単語を入力（quitで終了）: cherry
  'cherry' はインデックス2にあります
探す単語を入力（quitで終了）: mango
  'mango' はリストに存在しません
探す単語を入力（quitで終了）: quit
終了します。
```

---

### 例題3: 文字列の中から文字を探す

逐次探索は数値リストだけでなく、文字列の中の文字探索にも使えます。

```python
# ===================================
# 例題3: 文字列の中から文字を探す
# ===================================

def search_char_in_string(text, target_char):
    """
    文字列の中から特定の文字を探す関数
    - text: 探索対象の文字列
    - target_char: 探したい文字
    - 戻り値: (見つかった位置のリスト, 比較回数)
    """
    # 見つかった位置を記録するリスト
    positions = []
    # 比較回数カウンター
    comparison_count = 0

    # 文字列の先頭から1文字ずつ比較する
    for i in range(len(text)):
        # 比較回数を増やす
        comparison_count = comparison_count + 1

        # 現在の文字とターゲットを比較する
        if text[i] == target_char:
            # 一致した場合: 位置を記録する
            positions.append(i)
            # 途中経過を表示する
            print(f"  位置{i}: '{text[i]}' → 一致！")
        else:
            # 一致しない場合
            print(f"  位置{i}: '{text[i]}' → 不一致")

    return (positions, comparison_count)


# --- テスト ---
text = "banana"
target_char = "a"

print(f"=== 文字列 '{text}' から '{target_char}' を探す ===")
print()

# 探索を実行する
positions, count = search_char_in_string(text, target_char)

# 結果を表示する
print()
if len(positions) > 0:
    print(f"結果: '{target_char}' は位置 {positions} に見つかりました")
else:
    print(f"結果: '{target_char}' は見つかりませんでした")
print(f"比較回数: {count}回")
```

**実行結果:**
```
=== 文字列 'banana' から 'a' を探す ===

  位置0: 'b' → 不一致
  位置1: 'a' → 一致！
  位置2: 'n' → 不一致
  位置3: 'a' → 一致！
  位置4: 'n' → 不一致
  位置5: 'a' → 一致！

結果: 'a' は位置 [1, 3, 5] に見つかりました
比較回数: 6回
```

---

### 標準課題5（やややさしい）: 文字列の中で特定の文字を数える

**課題:** 文字列の中に特定の文字が何回出現するかを逐次探索で数えるプログラムを作りなさい。

**要件:**
- 対象文字列: `"programming"`
- 探す文字: `"g"`
- 先頭から1文字ずつ比較して、一致するたびにカウントを増やす
- 各文字との比較過程を表示する
- 最終的に出現回数を表示する

**期待される出力例:**
```
文字列: "programming"
探す文字: "g"
  位置0: 'p' → 不一致
  位置1: 'r' → 不一致
  位置2: 'o' → 不一致
  位置3: 'g' → 一致！（1回目）
  位置4: 'r' → 不一致
  ...
  位置10: 'g' → 一致！（2回目）
結果: 'g' は2回出現（比較11回）
```

---

### 標準課題6（やややさしい）: 文字列から単語を探す

**課題:** 文章の中から特定の単語を逐次探索で探すプログラムを作りなさい。

**要件:**
- 対象テキスト: `"the cat sat on the mat"`
- `split()` で単語リストに分割する
- 探す単語: `"on"`
- 単語リストを先頭から順に比較する
- 見つかった位置（何番目の単語か）と比較回数を表示する

**期待される出力例:**
```
テキスト: "the cat sat on the mat"
単語リスト: ['the', 'cat', 'sat', 'on', 'the', 'mat']
探す単語: "on"
  比較1: 'the' → 不一致
  比較2: 'cat' → 不一致
  比較3: 'sat' → 不一致
  比較4: 'on' → 一致！
結果: 4番目の単語で発見（比較4回）
```

---

### 例題4: 比較回数を記録する逐次探索

比較回数を詳細に記録して、アルゴリズムの効率を分析する方法を学びます。

```python
# ===================================
# 例題4: 比較回数を記録する逐次探索
# ===================================

def linear_search_with_stats(data, target):
    """
    比較回数の統計情報を返す逐次探索
    - data: 探索対象のリスト
    - target: 探したい値
    - 戻り値: (インデックス, 比較回数) のタプル
    """
    # 比較回数カウンター
    comparison_count = 0

    for i, value in enumerate(data):
        # 比較を行うたびにカウントを増やす
        comparison_count = comparison_count + 1

        # 値を比較する
        if value == target:
            # 見つかった場合
            return (i, comparison_count)

    # 見つからなかった場合
    return (-1, comparison_count)


# --- 複数のターゲットで比較回数を分析する ---
data = [15, 3, 27, 8, 42, 11, 36, 19, 5, 22]
print(f"データ: {data}")
print(f"データ数: {len(data)}個")
print("=" * 60)

# 全要素を1つずつ探索して、比較回数を記録する
print()
print("=== 各要素の探索に必要な比較回数 ===")

total_comparisons = 0  # 合計比較回数

for target in data:
    # 逐次探索を実行する
    index, count = linear_search_with_stats(data, target)
    # 合計に加算する
    total_comparisons = total_comparisons + count
    # 結果を表示する
    print(f"  target={target:>2} → インデックス{index}, 比較{count:>2}回")

# --- 統計情報を表示する ---
n = len(data)
average = total_comparisons / n

print()
print("=== 統計情報 ===")
print(f"  データ数: {n}")
print(f"  合計比較回数: {total_comparisons}")
print(f"  平均比較回数: {average}")
print(f"  理論上の平均 (n+1)/2: {(n + 1) / 2}")
print(f"  最良ケース（先頭）: 1回")
print(f"  最悪ケース（末尾）: {n}回")
```

**実行結果:**
```
データ: [15, 3, 27, 8, 42, 11, 36, 19, 5, 22]
データ数: 10個
============================================================

=== 各要素の探索に必要な比較回数 ===
  target=15 → インデックス0, 比較 1回
  target= 3 → インデックス1, 比較 2回
  target=27 → インデックス2, 比較 3回
  target= 8 → インデックス3, 比較 4回
  target=42 → インデックス4, 比較 5回
  target=11 → インデックス5, 比較 6回
  target=36 → インデックス6, 比較 7回
  target=19 → インデックス7, 比較 8回
  target= 5 → インデックス8, 比較 9回
  target=22 → インデックス9, 比較10回

=== 統計情報 ===
  データ数: 10
  合計比較回数: 55
  平均比較回数: 5.5
  理論上の平均 (n+1)/2: 5.5
  最良ケース（先頭）: 1回
  最悪ケース（末尾）: 10回
```

---

### 標準課題7（やや普通）: 最良・最悪・平均ケースの確認

**課題:** リストの先頭・中間・末尾・存在しない値をそれぞれ探索し、比較回数を比較するプログラムを作りなさい。

**要件:**
- データ: `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]`
- 以下の4つのケースを探索する:
  1. `target = 10`（先頭 = 最良ケース）
  2. `target = 50`（中間）
  3. `target = 100`（末尾 = 最悪ケース）
  4. `target = 999`（存在しない = 最悪ケース）
- 各ケースの比較回数を表示する
- 最良・最悪・平均比較回数をまとめて表示する

**期待される出力例:**
```
データ: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

ケース1（先頭）: target=10 → 発見, 比較1回
ケース2（中間）: target=50 → 発見, 比較5回
ケース3（末尾）: target=100 → 発見, 比較10回
ケース4（不在）: target=999 → 未発見, 比較10回

最良: 1回, 最悪: 10回, 平均: 6.5回
```

---

### 標準課題8（やや普通）: 複数のターゲットを連続探索

**課題:** 複数のターゲットを連続して逐次探索し、比較回数の合計と平均を表示するプログラムを作りなさい。

**要件:**
- データ: `["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]`
- ターゲットリスト: `["grape", "mango", "apple", "lemon", "cherry", "peach"]`
- 各ターゲットの探索結果と比較回数を表示する
- 合計比較回数と平均比較回数を計算する
- 見つかった数と見つからなかった数を集計する

**期待される出力例:**
```
データ: ['apple', 'banana', ...]（10個）
ターゲット: 6個

  "grape" → インデックス6, 比較7回
  "mango" → 未発見, 比較10回
  "apple" → インデックス0, 比較1回
  "lemon" → インデックス9, 比較10回
  "cherry" → インデックス2, 比較3回
  "peach" → 未発見, 比較10回

合計比較回数: 41回
平均比較回数: 6.8回
発見: 4個, 未発見: 2個
```

---

### 例題5: 大規模データでの探索時間測定

データサイズを変えて探索時間を測定し、O(n) の性質を体感します。

```python
# ===================================
# 例題5: 大規模データでの探索時間測定
# ===================================

import random
import time


def linear_search_simple(data, target):
    """
    逐次探索（シンプル版 -- 表示なし）
    - data: 探索対象のリスト
    - target: 探したい値
    - 戻り値: インデックス（見つからなければ -1）
    """
    for i in range(len(data)):
        # 値を比較する
        if data[i] == target:
            # 見つかった場合
            return i
    # 見つからなかった場合
    return -1


# --- データサイズを変えて実験する ---
sizes = [1000, 10000, 100000]

print("=== 逐次探索のスケール実験 ===")
print(f"{'データサイズ':>12}  {'探索時間':>10}  {'倍率':>6}")
print("-" * 40)

previous_time = None  # 前回の時間（倍率計算用）

for size in sizes:
    # --- ランダムなデータを生成する ---
    data = [random.randint(0, size * 10) for _ in range(size)]

    # --- 探索ターゲット（存在しない値で最悪ケース） ---
    target = -1  # リストに絶対ない値

    # --- 100回探索して時間を計測する ---
    start_time = time.time()

    for _ in range(100):
        # 逐次探索を実行する
        linear_search_simple(data, target)

    end_time = time.time()
    elapsed = end_time - start_time

    # --- 倍率を計算する ---
    if previous_time is not None and previous_time > 0:
        ratio = elapsed / previous_time
        ratio_str = f"{ratio:.1f}倍"
    else:
        ratio_str = "-"

    # --- 結果を表示する ---
    print(f"{size:>12,}  {elapsed:>8.3f}秒  {ratio_str:>6}")

    previous_time = elapsed

# --- 考察を表示する ---
print()
print("考察:")
print("  - データが10倍になると、探索時間もおよそ10倍になる")
print("  - これが計算量 O(n) の意味: データ量に比例して時間が増加する")
```

**実行結果（例）:**
```
=== 逐次探索のスケール実験 ===
  データサイズ      探索時間    倍率
----------------------------------------
       1,000     0.005秒       -
      10,000     0.048秒  9.6倍
     100,000     0.485秒  10.1倍

考察:
  - データが10倍になると、探索時間もおよそ10倍になる
  - これが計算量 O(n) の意味: データ量に比例して時間が増加する
```

---

### 標準課題9（普通）: データサイズ別の探索時間測定

**課題:** データサイズを 10,000 / 100,000 / 1,000,000 に変えて逐次探索の実行時間を測定するプログラムを作りなさい。

**要件:**
- 各サイズで `random.randint()` を使ってランダムなリストを生成する
- 各サイズで 1000回 のランダム探索を行い、合計時間を測定する（`time.time()` を使う）
- 探索ターゲットはランダムに生成する
- 結果を表形式で表示する
- データが10倍になったときの時間の倍率を計算する
- 発見数と未発見数も集計する

**期待される出力例:**
```
=== 逐次探索 スケール実験 ===
データサイズ     探索時間     発見数    未発見数
    10,000     0.XXX秒      XXX       XXX
   100,000     X.XXX秒      XXX       XXX   (前回のX.X倍)
 1,000,000     XX.XXX秒     XXX       XXX   (前回のX.X倍)
```

---

### 標準課題10（普通）: 逐次探索 vs in演算子 の速度比較

**課題:** 自作の逐次探索関数とPythonの `in` 演算子の速度を比較するプログラムを作りなさい。

**要件:**
- データサイズ 100,000 のランダムリストを生成する
- 同じ1000個のターゲットに対して:
  1. 自作の `linear_search()` で探索する
  2. Python の `in` 演算子で探索する
- それぞれの合計時間を測定して比較する
- `in` 演算子の方が速い理由を考察する（Pythonの `in` はC言語で実装されているため）

**期待される出力例:**
```
=== 速度比較: 自作 vs in演算子 ===
データサイズ: 100,000

自作 linear_search: X.XXX秒
Python in演算子:    X.XXX秒
速度差: in演算子は自作のX.X倍速い

考察: Pythonのin演算子はC言語で実装されているため高速
```

---

## 発展課題

### 発展課題1: 単語探索ゲーム

**課題:** ランダムな5文字の文字列を1000個生成し、ユーザーが入力した文字列を逐次探索で探すゲームを作りなさい。

**要件:**
- `random` と `string` モジュールを使って5文字のランダム文字列を1000個生成する
- 生成した文字列の先頭10個を表示する
- ユーザーが文字列を入力すると逐次探索で探す
- 見つかった場合: インデックスと比較回数を表示
- 見つからなかった場合: 比較回数を表示
- ランダムに1つ選んで自動探索するデモモードも付ける
- 10回の自動探索で平均比較回数を計算する

---

### 発展課題2: 複数キーによる探索

**課題:** 学生データ（名前、学年、点数）のリストから、複数の条件で探索するプログラムを作りなさい。

**要件:**
- 学生データはタプルのリスト: `(名前, 学年, 点数)`
- 以下の探索機能を実装する:
  1. 名前で探索（完全一致）
  2. 学年で探索（条件一致: 全員を返す）
  3. 点数の範囲で探索（例: 80点以上90点以下）
- 各探索で比較回数を表示する
- 探索結果を一覧表示する

---

## 解答例

### 標準課題1 解答

```python
# ===================================
# 標準課題1 解答: リストから値を探す（見つかる場合）
# ===================================

# --- 探索対象のリスト ---
data = [15, 3, 27, 8, 42, 11, 36]
# 探したい値
target = 42

# --- データとターゲットを表示する ---
print(f"データ: {data}")
print(f"探す値: {target}")

# --- 比較回数カウンター ---
comparison_count = 0

# --- 逐次探索を実行する ---
for i in range(len(data)):
    # 比較回数を増やす
    comparison_count = comparison_count + 1

    # 現在の要素とターゲットを比較する
    if data[i] == target:
        # 一致した場合
        print(f"  比較{comparison_count}: data[{i}] = {data[i]} → 一致！")
        # 結果を表示して終了する
        print(f"結果: インデックス{i}で発見（比較{comparison_count}回）")
        # ループを抜ける
        break
    else:
        # 不一致の場合
        print(f"  比較{comparison_count}: data[{i}] = {data[i]} → 不一致")
```

---

### 標準課題2 解答

```python
# ===================================
# 標準課題2 解答: リストから値を探す（見つからない場合）
# ===================================

# --- 探索対象のリスト ---
data = [15, 3, 27, 8, 42, 11, 36]
# 探したい値（存在しない値）
target = 99

# --- データとターゲットを表示する ---
print(f"データ: {data}")
print(f"探す値: {target}")

# --- 比較回数カウンター ---
comparison_count = 0
# --- 見つかったかのフラグ ---
found = False

# --- 逐次探索を実行する ---
for i in range(len(data)):
    # 比較回数を増やす
    comparison_count = comparison_count + 1

    # 現在の要素とターゲットを比較する
    if data[i] == target:
        # 一致した場合
        print(f"  比較{comparison_count}: data[{i}] = {data[i]} → 一致！")
        found = True
        print(f"結果: インデックス{i}で発見（比較{comparison_count}回）")
        break
    else:
        # 不一致の場合
        print(f"  比較{comparison_count}: data[{i}] = {data[i]} → 不一致")

# --- 見つからなかった場合の処理 ---
if not found:
    print(f"結果: 見つかりませんでした（比較{comparison_count}回）")
```

---

### 標準課題3 解答

```python
# ===================================
# 標準課題3 解答: 逐次探索関数の実装
# ===================================

def linear_search(data, target):
    """
    逐次探索を行う関数
    - data: 探索対象のリスト
    - target: 探したい値
    - 戻り値: 見つかった場合はインデックス、見つからない場合は -1
    """
    # リストの先頭から順に比較する
    for i in range(len(data)):
        # 現在の要素とターゲットを比較する
        if data[i] == target:
            # 見つかった場合: インデックスを返す
            return i

    # 全て調べたが見つからなかった場合
    return -1


# --- テストデータ ---
fruits = ["apple", "banana", "cherry", "durian", "elderberry"]
print(f"データ: {fruits}")

# --- テストケース ---
test_targets = ["cherry", "apple", "elderberry", "mango"]

for target in test_targets:
    # 逐次探索を実行する
    index = linear_search(fruits, target)
    # 結果を表示する
    print(f'  "{target}" → インデックス: {index}')
```

---

### 標準課題4 解答

```python
# ===================================
# 標準課題4 解答: 探索結果のエラーハンドリング
# ===================================

def linear_search(data, target):
    """逐次探索を行う関数"""
    # リストの先頭から順に比較する
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


# --- テストデータ ---
fruits = ["apple", "banana", "cherry", "durian", "elderberry"]

# --- タイトル表示 ---
print("=== 単語検索 ===")
print(f"データ: {fruits}")

# --- 検索ループ ---
while True:
    # ユーザーに検索語を入力してもらう
    word = input("探す単語を入力（quitで終了）: ")

    # quitが入力されたら終了する
    if word == "quit":
        print("終了します。")
        break

    # 逐次探索を実行する
    index = linear_search(fruits, word)

    # 結果に応じてメッセージを表示する
    if index != -1:
        # 見つかった場合
        print(f"  '{word}' はインデックス{index}にあります")
    else:
        # 見つからなかった場合
        print(f"  '{word}' はリストに存在しません")
```

---

### 標準課題5 解答

```python
# ===================================
# 標準課題5 解答: 文字列の中で特定の文字を数える
# ===================================

# --- 対象の文字列と探す文字 ---
text = "programming"
target_char = "g"

# --- 表示 ---
print(f'文字列: "{text}"')
print(f'探す文字: "{target_char}"')

# --- カウンターを初期化する ---
match_count = 0  # 一致した回数
comparison_count = 0  # 比較回数

# --- 先頭から1文字ずつ比較する ---
for i in range(len(text)):
    # 比較回数を増やす
    comparison_count = comparison_count + 1

    # 現在の文字とターゲットを比較する
    if text[i] == target_char:
        # 一致した場合
        match_count = match_count + 1
        print(f"  位置{i}: '{text[i]}' → 一致！（{match_count}回目）")
    else:
        # 不一致の場合
        print(f"  位置{i}: '{text[i]}' → 不一致")

# --- 結果を表示する ---
print(f"結果: '{target_char}' は{match_count}回出現（比較{comparison_count}回）")
```

---

### 標準課題6 解答

```python
# ===================================
# 標準課題6 解答: 文字列から単語を探す
# ===================================

# --- 対象のテキスト ---
text = "the cat sat on the mat"
# 探す単語
target_word = "on"

# --- テキストを表示する ---
print(f'テキスト: "{text}"')

# --- 単語リストに分割する ---
words = text.split()
print(f"単語リスト: {words}")
print(f'探す単語: "{target_word}"')

# --- 比較回数カウンター ---
comparison_count = 0
# --- 見つかったかのフラグ ---
found = False

# --- 単語リストを先頭から順に比較する ---
for i in range(len(words)):
    # 比較回数を増やす
    comparison_count = comparison_count + 1

    # 現在の単語とターゲットを比較する
    if words[i] == target_word:
        # 一致した場合
        print(f"  比較{comparison_count}: '{words[i]}' → 一致！")
        found = True
        # 結果を表示する
        print(f"結果: {comparison_count}番目の単語で発見（比較{comparison_count}回）")
        break
    else:
        # 不一致の場合
        print(f"  比較{comparison_count}: '{words[i]}' → 不一致")

# --- 見つからなかった場合 ---
if not found:
    print(f"結果: '{target_word}' は見つかりませんでした（比較{comparison_count}回）")
```

---

### 標準課題7 解答

```python
# ===================================
# 標準課題7 解答: 最良・最悪・平均ケースの確認
# ===================================

def linear_search(data, target):
    """逐次探索（比較回数付き）"""
    comparison_count = 0
    for i in range(len(data)):
        comparison_count = comparison_count + 1
        if data[i] == target:
            return (i, comparison_count)
    return (-1, comparison_count)


# --- データ ---
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(f"データ: {data}")
print()

# --- 4つのケースを探索する ---
cases = [
    ("先頭", 10),
    ("中間", 50),
    ("末尾", 100),
    ("不在", 999),
]

# 比較回数を記録するリスト
counts = []

for label, target in cases:
    # 逐次探索を実行する
    index, count = linear_search(data, target)
    # 比較回数を記録する
    counts.append(count)

    # 結果を表示する
    if index != -1:
        status = "発見"
    else:
        status = "未発見"
    print(f"ケース（{label}）: target={target} → {status}, 比較{count}回")

# --- 統計情報を表示する ---
# 最良ケース（最小比較回数）
best = counts[0]  # 先頭のケース
# 最悪ケース（最大比較回数）
worst = counts[2]  # 末尾のケース
# 平均
total = 0
for c in counts:
    total = total + c
average = total / len(counts)

print()
print(f"最良: {best}回, 最悪: {worst}回, 平均: {average}回")
```

---

### 標準課題8 解答

```python
# ===================================
# 標準課題8 解答: 複数のターゲットを連続探索
# ===================================

def linear_search(data, target):
    """逐次探索（比較回数付き）"""
    comparison_count = 0
    for i in range(len(data)):
        comparison_count = comparison_count + 1
        if data[i] == target:
            return (i, comparison_count)
    return (-1, comparison_count)


# --- データ ---
data = ["apple", "banana", "cherry", "durian", "elderberry",
        "fig", "grape", "honeydew", "kiwi", "lemon"]
# --- ターゲットリスト ---
targets = ["grape", "mango", "apple", "lemon", "cherry", "peach"]

# --- 表示 ---
print(f"データ: {data}（{len(data)}個）")
print(f"ターゲット: {len(targets)}個")
print()

# --- 各ターゲットを探索する ---
total_comparisons = 0  # 合計比較回数
found_count = 0  # 見つかった数
not_found_count = 0  # 見つからなかった数

for target in targets:
    # 逐次探索を実行する
    index, count = linear_search(data, target)
    # 合計に加算する
    total_comparisons = total_comparisons + count

    # 結果を表示する
    if index != -1:
        found_count = found_count + 1
        print(f'  "{target}" → インデックス{index}, 比較{count}回')
    else:
        not_found_count = not_found_count + 1
        print(f'  "{target}" → 未発見, 比較{count}回')

# --- 統計情報を表示する ---
average = total_comparisons / len(targets)
print()
print(f"合計比較回数: {total_comparisons}回")
print(f"平均比較回数: {average:.1f}回")
print(f"発見: {found_count}個, 未発見: {not_found_count}個")
```

---

### 標準課題9 解答

```python
# ===================================
# 標準課題9 解答: データサイズ別の探索時間測定
# ===================================

import random
import time


def linear_search_simple(data, target):
    """逐次探索（高速版 -- 表示なし）"""
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


# --- 実験設定 ---
sizes = [10_000, 100_000, 1_000_000]
num_queries = 1000  # 各サイズで1000回探索する

# --- 表ヘッダーを表示する ---
print("=== 逐次探索 スケール実験 ===")
print(f"{'データサイズ':>12}  {'探索時間':>10}  {'発見数':>6}  {'未発見数':>6}")
print("-" * 55)

previous_time = None  # 前回の時間

for size in sizes:
    # --- ランダムなデータを生成する ---
    data = [random.randint(0, size - 1) for _ in range(size)]

    # --- ランダムなターゲットを生成する ---
    targets = [random.randint(0, size - 1) for _ in range(num_queries)]

    # --- 探索を実行して時間を計測する ---
    found_count = 0
    not_found_count = 0

    start_time = time.time()

    for target in targets:
        result = linear_search_simple(data, target)
        if result != -1:
            found_count = found_count + 1
        else:
            not_found_count = not_found_count + 1

    end_time = time.time()
    elapsed = end_time - start_time

    # --- 倍率を計算する ---
    if previous_time is not None and previous_time > 0:
        ratio = elapsed / previous_time
        ratio_str = f"(前回の{ratio:.1f}倍)"
    else:
        ratio_str = ""

    # --- 結果を表示する ---
    print(f"{size:>12,}  {elapsed:>8.3f}秒  {found_count:>6}  {not_found_count:>6}  {ratio_str}")

    previous_time = elapsed

# --- 考察 ---
print()
print("考察:")
print("  - データが10倍になると、探索時間もおよそ10倍になる")
print("  - これが計算量 O(n) の意味: データ量に比例して時間が増加する")
print("  - 逐次探索は小さなデータには十分だが、大きなデータには遅い")
```

---

### 標準課題10 解答

```python
# ===================================
# 標準課題10 解答: 逐次探索 vs in演算子 の速度比較
# ===================================

import random
import time


def linear_search_simple(data, target):
    """自作の逐次探索（表示なし）"""
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


# --- 設定 ---
data_size = 100_000
num_queries = 1000

# --- データを生成する ---
data = [random.randint(0, data_size - 1) for _ in range(data_size)]

# --- 同じターゲットリストを用意する ---
targets = [random.randint(0, data_size - 1) for _ in range(num_queries)]

print("=== 速度比較: 自作 vs in演算子 ===")
print(f"データサイズ: {data_size:,}")
print(f"探索回数: {num_queries}")
print()

# --- 自作のlinear_searchで探索する ---
start_time = time.time()
for target in targets:
    linear_search_simple(data, target)
end_time = time.time()
custom_time = end_time - start_time
print(f"自作 linear_search: {custom_time:.3f}秒")

# --- Python の in 演算子で探索する ---
start_time = time.time()
for target in targets:
    target in data  # Pythonのin演算子を使う
end_time = time.time()
builtin_time = end_time - start_time
print(f"Python in演算子:    {builtin_time:.3f}秒")

# --- 速度比較 ---
if builtin_time > 0:
    speedup = custom_time / builtin_time
    print(f"速度差: in演算子は自作の{speedup:.1f}倍速い")
else:
    print("速度差: in演算子が速すぎて計測不能")

# --- 考察 ---
print()
print("考察:")
print("  - Pythonのin演算子はC言語で実装されているため高速")
print("  - 自作のPythonループはインタプリタのオーバーヘッドがある")
print("  - アルゴリズムは同じO(n)だが、実装言語で定数倍の差が出る")
```

---

### 発展課題1 解答

```python
# ===================================
# 発展課題1 解答: 単語探索ゲーム
# ===================================

import random
import string


def generate_random_strings(n, length=5):
    """ランダムな文字列をn個生成する関数"""
    # 使用する文字: 英大文字 + 英小文字 + 数字
    characters = string.ascii_letters + string.digits
    # 結果を格納するリスト
    result = []

    for _ in range(n):
        # length文字のランダム文字列を1つ作る
        word = ""
        for _ in range(length):
            # ランダムに1文字選ぶ
            char = random.choice(characters)
            word = word + char
        # リストに追加する
        result.append(word)

    return result


def linear_search(data, target):
    """逐次探索（比較回数付き）"""
    comparison_count = 0
    for i in range(len(data)):
        comparison_count = comparison_count + 1
        if data[i] == target:
            return (i, comparison_count)
    return (-1, comparison_count)


# --- 1000個の文字列を生成する ---
keywords = generate_random_strings(1000)

print("=== 単語探索ゲーム ===")
print(f"  {len(keywords)}個のランダム文字列を生成しました")
print()

# --- 先頭10個を表示する ---
print("生成した文字列（先頭10個）:")
for i in range(10):
    print(f"  [{i}] {keywords[i]}")
print(f"  ... 全{len(keywords)}個")
print()

# --- デモモード: ランダムに10個選んで自動探索する ---
print("=== デモモード: ランダム自動探索 ===")
total_comparisons = 0

for trial in range(10):
    # リストからランダムに1つ選ぶ
    random_target = random.choice(keywords)
    # 逐次探索を実行する
    index, count = linear_search(keywords, random_target)
    # 合計に加算する
    total_comparisons = total_comparisons + count
    # 結果を表示する
    print(f"  試行{trial + 1:2d}: target='{random_target}' → "
          f"インデックス{index:>4d}, 比較{count:>4d}回")

# 平均比較回数を計算する
average = total_comparisons / 10
print()
print(f"平均比較回数: {average:.1f}回")
print(f"理論上の平均 (n/2): {len(keywords) / 2:.1f}回")

# --- 存在しない文字列を探索する ---
print()
print("=== 存在しない文字列の探索 ===")
missing_target = "ZZZZZ"
index, count = linear_search(keywords, missing_target)
if index == -1:
    print(f"  target='{missing_target}' → 見つからず（比較{count}回）")
else:
    print(f"  target='{missing_target}' → インデックス{index}で発見（比較{count}回）")

# --- ユーザー入力モード ---
print()
print("=== ユーザー入力モード ===")
while True:
    user_input = input("探す文字列を入力（quitで終了）: ")
    if user_input == "quit":
        print("終了します。")
        break

    index, count = linear_search(keywords, user_input)
    if index != -1:
        print(f"  '{user_input}' → インデックス{index}で発見（比較{count}回）")
    else:
        print(f"  '{user_input}' → 見つかりませんでした（比較{count}回）")
```

---

### 発展課題2 解答

```python
# ===================================
# 発展課題2 解答: 複数キーによる探索
# ===================================

# --- 学生データ ---
students = [
    ("田中", 1, 85),
    ("鈴木", 2, 92),
    ("佐藤", 1, 78),
    ("山田", 3, 65),
    ("高橋", 2, 88),
    ("伊藤", 1, 95),
    ("渡辺", 3, 72),
    ("中村", 2, 80),
    ("小林", 1, 67),
    ("加藤", 3, 91),
]


def search_by_name(students, target_name):
    """名前で探索する関数（完全一致）"""
    comparison_count = 0
    # 先頭から順に比較する
    for name, grade, score in students:
        comparison_count = comparison_count + 1
        if name == target_name:
            # 見つかった場合
            return ((name, grade, score), comparison_count)
    # 見つからなかった場合
    return (None, comparison_count)


def search_by_grade(students, target_grade):
    """学年で探索する関数（条件一致: 全員を返す）"""
    comparison_count = 0
    results = []
    # 全員を調べる（途中で止めない）
    for name, grade, score in students:
        comparison_count = comparison_count + 1
        if grade == target_grade:
            # 条件に一致した場合: 結果リストに追加する
            results.append((name, grade, score))
    return (results, comparison_count)


def search_by_score_range(students, min_score, max_score):
    """点数の範囲で探索する関数"""
    comparison_count = 0
    results = []
    # 全員を調べる
    for name, grade, score in students:
        comparison_count = comparison_count + 1
        # 点数が範囲内かチェックする
        if min_score <= score <= max_score:
            results.append((name, grade, score))
    return (results, comparison_count)


# --- データを表示する ---
print("=== 学生データ ===")
for name, grade, score in students:
    print(f"  {name} - {grade}年 - {score}点")
print()

# --- 名前で探索する ---
print("=== 名前で探索: '鈴木' ===")
result, count = search_by_name(students, "鈴木")
if result is not None:
    name, grade, score = result
    print(f"  発見: {name} - {grade}年 - {score}点（比較{count}回）")
else:
    print(f"  見つかりませんでした（比較{count}回）")

# --- 名前で探索（存在しない） ---
print()
print("=== 名前で探索: '木村' ===")
result, count = search_by_name(students, "木村")
if result is not None:
    name, grade, score = result
    print(f"  発見: {name} - {grade}年 - {score}点（比較{count}回）")
else:
    print(f"  見つかりませんでした（比較{count}回）")

# --- 学年で探索する ---
print()
print("=== 学年で探索: 1年生 ===")
results, count = search_by_grade(students, 1)
print(f"  {len(results)}人見つかりました（比較{count}回）:")
for name, grade, score in results:
    print(f"    {name} - {grade}年 - {score}点")

# --- 点数の範囲で探索する ---
print()
print("=== 点数で探索: 80〜90点 ===")
results, count = search_by_score_range(students, 80, 90)
print(f"  {len(results)}人見つかりました（比較{count}回）:")
for name, grade, score in results:
    print(f"    {name} - {grade}年 - {score}点")

# --- 点数の範囲で探索する ---
print()
print("=== 点数で探索: 90点以上 ===")
results, count = search_by_score_range(students, 90, 100)
print(f"  {len(results)}人見つかりました（比較{count}回）:")
for name, grade, score in results:
    print(f"    {name} - {grade}年 - {score}点")
```
