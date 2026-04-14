# 第4回: 二分探索

## 説明

### 辞書引きのたとえ

国語辞典で「**もも**」という単語を調べるとき、あなたはどうしますか？

1. **1ページ目から順に探す？** -- そんなことはしませんよね
2. **真ん中あたりを開く** →「さ行」だった → 「も」はもっと後ろ → **後半を開く** → ...

この「**半分に絞り込む**」作業を繰り返すのが **二分探索（Binary Search）** です。

### 二分探索の条件

**重要:** 二分探索は **ソート済み（整列済み）のデータ** にしか使えません。

```
使える: [1, 3, 5, 7, 9, 11, 13]  ← ソート済み
使えない: [3, 7, 1, 9, 4]          ← バラバラ
```

### アルゴリズムの手順

```
1. left = 0（先頭）、right = n-1（末尾）に設定
2. mid = (left + right) // 2 で中央を計算
3. data[mid] と target を比較:
   - 一致    → 発見! midを返す
   - 小さい  → target は右半分にある → left = mid + 1
   - 大きい  → target は左半分にある → right = mid - 1
4. left > right になったら「見つからない」
```

### 計算量 O(log n) とは

二分探索は毎回データを **半分** に絞り込みます。

```
データ数(n)   最大比較回数(log2 n)
       10             4回
      100             7回
    1,000            10回
  100,000            17回
1,000,000            20回  ← 100万件でもたった20回!
```

つまり **「100万件のデータから、たった20回の比較で見つけられる」** ということです。

逐次探索の O(n) と比較すると:
```
n = 1,000,000 の場合:
  逐次探索: 最悪 1,000,000回
  二分探索: 最悪        20回  ← 50,000倍速い!
```

---

## 例題と課題

### 例題1: ソート済みリストの基本

```python
# ============================================================
# 例題1: ソート済みリストの確認と基本操作
# ============================================================

# --- ソート済みリストを作る ---
numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]  # 未ソートのリスト
print(f"元のリスト: {numbers}")  # 元のリストを表示する

sorted_numbers = sorted(numbers)  # sorted()でソート済みコピーを作る
print(f"ソート後:   {sorted_numbers}")  # ソートされたリストを表示する

# --- ソート済みか判定する関数 ---
def is_sorted(data):  # リストがソート済みかチェックする関数
    """リストが昇順にソートされているか判定する"""
    for i in range(len(data) - 1):  # 隣り合う要素を順に比較する
        if data[i] > data[i + 1]:  # 前の要素が後の要素より大きければ
            return False  # ソートされていないのでFalseを返す
    return True  # 最後まで問題なければTrueを返す

# --- テスト ---
print(f"\n元のリストはソート済み？: {is_sorted(numbers)}")  # Falseになるはず
print(f"ソート後はソート済み？:   {is_sorted(sorted_numbers)}")  # Trueになるはず

# --- ソート済みリストでの値の検索 ---
target = 5  # 探したい値
print(f"\n{target} はリストに含まれる？: {target in sorted_numbers}")  # in演算子で確認
print(f"{target} の位置(インデックス): {sorted_numbers.index(target)}")  # index()で位置取得
```

---

#### 標準課題1（超やさしい）

リスト `[8, 3, 1, 6, 4, 9, 2, 7, 5, 10]` を受け取り、そのリストがソート済みかどうかを判定して結果を表示するプログラムを作成してください。ソート済みでない場合は、ソートしたリストも表示してください。

---

#### 標準課題2（超やさしい）

ソート済みリスト `[2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]` の中から、ユーザーが入力した値を `in` 演算子で検索し、見つかった場合はインデックスを、見つからない場合は「見つかりませんでした」と表示するプログラムを作成してください。3つの値（23, 50, 100）で動作確認してください。

---

### 例題2: 二分探索のステップ表示

```python
# ============================================================
# 例題2: 二分探索の各ステップを詳細に表示する
# ============================================================

def binary_search_trace(data, target):  # トレース付き二分探索関数
    """二分探索を実行し、各ステップの状態を表示する"""
    left = 0  # 探索範囲の左端を先頭にする
    right = len(data) - 1  # 探索範囲の右端を末尾にする
    step = 0  # ステップ数を数えるカウンター

    print(f"探索対象: {data}")  # 探索するリストを表示する
    print(f"target: {target}")  # 探したい値を表示する
    print("-" * 50)  # 区切り線を表示する

    while left <= right:  # 探索範囲がある間繰り返す
        step += 1  # ステップ数を1増やす
        mid = (left + right) // 2  # 中央のインデックスを計算する

        print(f"ステップ{step}: left={left}, right={right}, mid={mid}, data[{mid}]={data[mid]}")  # 状態表示

        if data[mid] == target:  # 中央の値がtargetと一致したら
            print(f"  → 発見! インデックス{mid}")  # 見つかったことを表示する
            return mid  # 見つかったインデックスを返す
        elif data[mid] < target:  # 中央の値がtargetより小さければ
            print(f"  → {data[mid]} < {target} なので右半分へ")  # 右に進むことを表示する
            left = mid + 1  # 左端を中央の右に移動する
        else:  # 中央の値がtargetより大きければ
            print(f"  → {data[mid]} > {target} なので左半分へ")  # 左に進むことを表示する
            right = mid - 1  # 右端を中央の左に移動する

    print(f"  → 見つかりませんでした（{step}回比較）")  # 見つからなかった場合の表示
    return -1  # -1を返して「見つからない」を示す

# --- 実行 ---
data = [1, 3, 5, 7, 9, 11, 13]  # ソート済みリスト
binary_search_trace(data, 11)  # target=11 で探索する
print()  # 空行を入れる
binary_search_trace(data, 6)  # target=6（存在しない値）で探索する
```

---

#### 標準課題3（やさしい）

ソート済みリスト `[2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]` に対して二分探索を行う関数 `binary_search(data, target)` を実装してください。見つかった場合はインデックスを、見つからなかった場合は `-1` を返してください。target=23, target=2, target=100, target=50 の4つでテストしてください。

---

#### 標準課題4（やさしい）

例題2の `binary_search_trace` 関数を使って、リスト `[1, 3, 5, 7, 9, 11, 13]` で target=1, target=13, target=7, target=4 を探索し、それぞれ何ステップで結果が出たかを表形式でまとめて表示するプログラムを作成してください。

---

### 例題3: 比較回数のカウント

```python
# ============================================================
# 例題3: 逐次探索と二分探索の比較回数を数える
# ============================================================

def linear_search_count(data, target):  # 逐次探索（比較回数カウント付き）
    """逐次探索を実行し、比較回数を返す"""
    count = 0  # 比較回数カウンター
    for i in range(len(data)):  # 先頭から順に調べる
        count += 1  # 比較を1回行ったのでカウント
        if data[i] == target:  # 値が一致したら
            return (i, count)  # (インデックス, 比較回数)を返す
    return (-1, count)  # 見つからなかった場合

def binary_search_count(data, target):  # 二分探索（比較回数カウント付き）
    """二分探索を実行し、比較回数を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    count = 0  # 比較回数カウンター

    while left <= right:  # 探索範囲がある間繰り返す
        count += 1  # 比較を1回行ったのでカウント
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 中央の値がtargetと一致したら
            return (mid, count)  # (インデックス, 比較回数)を返す
        elif data[mid] < target:  # 中央の値がtargetより小さければ
            left = mid + 1  # 左端を右に移動する
        else:  # 中央の値がtargetより大きければ
            right = mid - 1  # 右端を左に移動する
    return (-1, count)  # 見つからなかった場合

# --- 20個のソート済みデータで比較 ---
data = list(range(1, 21))  # [1, 2, 3, ..., 20]のリストを作る
print(f"データ: {data}")  # データの内容を表示する
print(f"データ数: {len(data)}個")  # データの数を表示する
print("-" * 55)  # 区切り線を表示する
print(f"{'target':>6}  {'逐次':>8}  {'二分':>8}  {'差':>6}")  # ヘッダー行
print("-" * 55)  # 区切り線を表示する

for target in [1, 5, 10, 15, 20, 25]:  # テストするtargetのリスト
    idx_l, cnt_l = linear_search_count(data, target)  # 逐次探索の結果を取得する
    idx_b, cnt_b = binary_search_count(data, target)  # 二分探索の結果を取得する
    diff = cnt_l - cnt_b  # 比較回数の差を計算する
    print(f"{target:>6}  {cnt_l:>5}回  {cnt_b:>5}回  {diff:>+5}回")  # 結果を表示する
```

---

#### 標準課題5（やややさしい）

100個のソート済みデータ `list(range(1, 101))` に対して、target=1, 25, 50, 75, 100, 999 のそれぞれについて逐次探索と二分探索の比較回数を計算し、結果を表形式で表示するプログラムを作成してください。

---

#### 標準課題6（やややさしい）

1000個のソート済みデータで、逐次探索と二分探索の**平均比較回数**を比較するプログラムを作成してください。リスト内のすべての値（1〜1000）を探索し、それぞれの比較回数の平均を求めてください。「二分探索は逐次探索の約何倍効率的か」を計算して表示してください。

---

### 例題4: bisect モジュールの活用

```python
# ============================================================
# 例題4: Pythonの bisect モジュールで二分探索する
# ============================================================

import bisect  # Python標準の二分探索モジュールをインポートする

# --- bisect_left: 挿入位置（左端）を求める ---
data = [2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]  # ソート済みリスト
print(f"データ: {data}")  # データの内容を表示する
print()  # 空行

# --- 存在する値を探す ---
target = 23  # 探したい値
pos = bisect.bisect_left(data, target)  # target以上の最初の位置を求める
print(f"bisect_left(data, {target}) = {pos}")  # 挿入位置を表示する
if pos < len(data) and data[pos] == target:  # その位置の値がtargetと一致するか確認
    print(f"  → data[{pos}] = {target} → 存在する!")  # 存在する場合

# --- 存在しない値を探す ---
target = 50  # 探したい値（存在しない）
pos = bisect.bisect_left(data, target)  # target以上の最初の位置を求める
print(f"\nbisect_left(data, {target}) = {pos}")  # 挿入位置を表示する
if pos < len(data) and data[pos] == target:  # 一致確認
    print(f"  → 存在する!")  # 存在する場合
else:  # 一致しなければ
    print(f"  → 存在しない（挿入するなら位置{pos}）")  # 存在しない場合

# --- bisect_right との違い（重複あり） ---
data_dup = [1, 3, 5, 5, 5, 7, 9]  # 重複を含むソート済みリスト
target = 5  # 重複している値を探す
left_pos = bisect.bisect_left(data_dup, target)  # 最初の5の位置
right_pos = bisect.bisect_right(data_dup, target)  # 最後の5の次の位置
print(f"\nデータ（重複あり）: {data_dup}")  # データを表示する
print(f"bisect_left(data, {target})  = {left_pos}（最初の5の位置）")  # 左端を表示する
print(f"bisect_right(data, {target}) = {right_pos}（最後の5の次の位置）")  # 右端を表示する
print(f"5の個数: {right_pos - left_pos}個")  # 個数を計算して表示する
```

---

#### 標準課題7（やや普通）

`bisect_left` を使って、ソート済みリスト `[2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]` から値を検索する関数 `bisect_search(data, target)` を作成してください。見つかった場合はインデックスを、見つからなかった場合は `-1` を返してください。target=23, 50, 2, 100 でテストしてください。

---

#### 標準課題8（やや普通）

ソート済みリスト `[1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5]` に対して、`bisect_left` と `bisect_right` を使い、指定した値の出現回数を数える関数 `count_value(data, target)` を作成してください。target=1, 2, 3, 4, 5, 6 のそれぞれについて出現回数を表示してください。

---

### 例題5: ベンチマーク（性能比較）

```python
# ============================================================
# 例題5: 逐次探索 vs 二分探索のベンチマーク
# ============================================================

import time  # 時間計測用モジュールをインポートする
import random  # ランダム値生成用モジュールをインポートする

def linear_search(data, target):  # 逐次探索の関数
    """逐次探索: 先頭から順に探す"""
    for i in range(len(data)):  # 先頭から末尾まで繰り返す
        if data[i] == target:  # 値が一致したら
            return i  # インデックスを返す
    return -1  # 見つからなければ-1を返す

def binary_search(data, target):  # 二分探索の関数
    """二分探索: 半分ずつ絞り込む"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    while left <= right:  # 探索範囲がある間繰り返す
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return -1  # 見つからなければ-1を返す

# --- ベンチマーク実行 ---
n = 100000  # データ数を10万に設定する
data = list(range(n))  # 0から99999までのソート済みリストを作る
num_queries = 500  # 探索回数を500回にする
targets = [random.randint(0, n - 1) for _ in range(num_queries)]  # ランダムなtargetを生成する

# --- 二分探索の計測 ---
start = time.perf_counter()  # 計測開始
for t in targets:  # 各targetについて探索する
    binary_search(data, t)  # 二分探索を実行する
time_binary = time.perf_counter() - start  # 経過時間を計算する

# --- 逐次探索の計測 ---
start = time.perf_counter()  # 計測開始
for t in targets:  # 各targetについて探索する
    linear_search(data, t)  # 逐次探索を実行する
time_linear = time.perf_counter() - start  # 経過時間を計算する

# --- 結果表示 ---
print(f"データ数: {n:,}件, 探索回数: {num_queries}回")  # テスト条件を表示する
print(f"二分探索: {time_binary:.4f}秒")  # 二分探索の時間を表示する
print(f"逐次探索: {time_linear:.4f}秒")  # 逐次探索の時間を表示する
if time_binary > 0:  # ゼロ除算を防ぐ
    print(f"二分探索は約 {time_linear / time_binary:,.0f}倍 速い!")  # 速度比を表示する
```

---

#### 標準課題9（普通）

データ数を `[1000, 5000, 10000, 50000, 100000]` と変化させて、逐次探索と二分探索の実行時間を計測し、matplotlib を使って棒グラフに描画するプログラムを作成してください。各データサイズで500回の探索を行い、X軸にデータサイズ、Y軸に実行時間（秒）を表示してください。

---

#### 標準課題10（普通）

データ数を `[100, 1000, 10000, 100000, 1000000]` と変化させて、二分探索の平均比較回数を計測し、理論値 `log2(n)` と比較するプログラムを作成してください。実測値と理論値の差を表形式で表示し、O(log n) が実際に成り立っていることを確認してください。

---

## 発展課題

### 発展課題1: ひらがな単語当てゲーム

67個のひらがな単語辞書を使って、二分探索で単語を当てるゲームを作ってください。

**仕様:**
1. 以下のひらがな辞書（ソート済み）を用意する
2. ランダムに1つの正解単語を選ぶ
3. プレイヤーが単語を入力し、「もっと前（辞書順で前）」「もっと後ろ（辞書順で後ろ）」のヒントを出す
4. 正解するまでの回数を表示する
5. 二分探索で最適に絞り込んだ場合の理論最小回数（log2(67) = 約7回）を表示して比較する
6. 自動プレイモード（コンピュータが二分探索で解く）も実装する

**ひらがな辞書:**
```python
hiragana_dict = [
    "あいす", "あさがお", "いちご", "いるか", "うさぎ",
    "うちわ", "えんぴつ", "おにぎり", "かえる", "かさ",
    "きつね", "きのこ", "くじら", "くつ", "けいたい",
    "こあら", "さくら", "さんま", "しまうま", "すいか",
    "すずめ", "せみ", "そら", "たこ", "たぬき",
    "ちきゅう", "つばめ", "てんとう", "とけい", "なす",
    "にじ", "ぬいぐるみ", "ねこ", "のり", "はな",
    "ひこうき", "ふうせん", "へび", "ほし", "まくら",
    "みかん", "むしめがね", "めがね", "もも", "やかん",
    "ゆき", "よる", "らくだ", "りんご", "るすばん",
    "れいぞうこ", "ろうそく", "わに", "あひる", "いす",
    "うめ", "えび", "おと", "かぜ", "きく",
    "くも", "けむし", "こい", "さかな", "しか",
    "すし", "せかい",
]
hiragana_dict.sort()
```

---

### 発展課題2: 大規模ベンチマーク（100万件）

100万件のソート済みデータで、逐次探索と二分探索の速度差を体感してください。

**手順:**
1. 100万件のソート済み整数リストを生成する
2. 1000個のランダムなターゲットを用意する
3. 逐次探索と二分探索それぞれで全ターゲットを探索し、時間を計測する
4. 速度差と理論上の比較回数の差を表示する

**出力例:**
```
データ数: 1,000,000件  探索回数: 1,000回
================================================
Binary Search :  0.002秒  (found=639, not=361)
Linear Search : 15.303秒  (found=639, not=361)
================================================
二分探索は逐次探索の約 7,651倍 速い!
```

---

## 解答例

### 標準課題1 解答

```python
# ============================================================
# 標準課題1 解答: リストがソート済みか判定する
# ============================================================

data = [8, 3, 1, 6, 4, 9, 2, 7, 5, 10]  # 判定するリスト
print(f"リスト: {data}")  # リストの内容を表示する

is_sorted = True  # ソート済みフラグをTrueで初期化する
for i in range(len(data) - 1):  # 隣り合う要素を順に比較する
    if data[i] > data[i + 1]:  # 前の要素が後の要素より大きければ
        is_sorted = False  # ソートされていないのでFalseにする
        break  # ループを抜ける

if is_sorted:  # フラグがTrueなら
    print("このリストはソート済みです")  # ソート済みと表示する
else:  # Falseなら
    print("このリストはソート済みではありません")  # 未ソートと表示する
    sorted_data = sorted(data)  # ソートしたリストを作る
    print(f"ソート後: {sorted_data}")  # ソート後のリストを表示する
```

---

### 標準課題2 解答

```python
# ============================================================
# 標準課題2 解答: ソート済みリストから値を検索する
# ============================================================

data = [2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]  # ソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

targets = [23, 50, 100]  # 検索する値のリスト
for target in targets:  # 各targetについて検索する
    if target in data:  # in演算子で存在確認する
        index = data.index(target)  # 存在する場合はインデックスを取得する
        print(f"target={target}: インデックス{index}で発見")  # 結果を表示する
    else:  # 存在しない場合
        print(f"target={target}: 見つかりませんでした")  # 見つからないと表示する
```

---

### 標準課題3 解答

```python
# ============================================================
# 標準課題3 解答: 二分探索の実装
# ============================================================

def binary_search(data, target):  # 二分探索関数の定義
    """二分探索でtargetを探す。見つかればインデックス、なければ-1を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする

    while left <= right:  # 探索範囲がある間繰り返す
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 中央値が小さければ
            left = mid + 1  # 右半分へ移動する
        else:  # 中央値が大きければ
            right = mid - 1  # 左半分へ移動する
    return -1  # 見つからなかった

# --- テスト ---
data = [2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]  # ソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

for target in [23, 2, 100, 50]:  # テストする値のリスト
    result = binary_search(data, target)  # 二分探索を実行する
    if result != -1:  # 見つかった場合
        print(f"target={target:>3}: インデックス{result}で発見")  # 結果を表示する
    else:  # 見つからなかった場合
        print(f"target={target:>3}: 見つかりませんでした(-1)")  # 見つからないと表示する
```

---

### 標準課題4 解答

```python
# ============================================================
# 標準課題4 解答: 探索ステップ数の比較表
# ============================================================

def binary_search_steps(data, target):  # ステップ数を返す二分探索
    """二分探索を実行し、ステップ数を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    step = 0  # ステップ数カウンター

    while left <= right:  # 探索範囲がある間繰り返す
        step += 1  # ステップ数を増やす
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return (mid, step)  # (インデックス, ステップ数)を返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return (-1, step)  # 見つからなかった場合

# --- テスト ---
data = [1, 3, 5, 7, 9, 11, 13]  # ソート済みリスト
targets = [1, 13, 7, 4]  # テストする値のリスト

print(f"データ: {data}")  # データを表示する
print("-" * 45)  # 区切り線
print(f"{'target':>6}  {'結果':>10}  {'ステップ数':>10}")  # ヘッダー行
print("-" * 45)  # 区切り線

for target in targets:  # 各targetについてテストする
    idx, steps = binary_search_steps(data, target)  # 二分探索を実行する
    if idx != -1:  # 見つかった場合
        result_str = f"idx={idx}"  # 結果文字列を作る
    else:  # 見つからなかった場合
        result_str = "未発見"  # 結果文字列を作る
    print(f"{target:>6}  {result_str:>10}  {steps:>7}回")  # 結果を表示する
```

---

### 標準課題5 解答

```python
# ============================================================
# 標準課題5 解答: 100個のデータで比較回数を比較する
# ============================================================

def linear_search_count(data, target):  # 逐次探索（比較回数付き）
    """逐次探索を実行し、(インデックス, 比較回数)を返す"""
    count = 0  # 比較回数カウンター
    for i in range(len(data)):  # 先頭から順に調べる
        count += 1  # 比較を1回カウント
        if data[i] == target:  # 一致したら
            return (i, count)  # 結果を返す
    return (-1, count)  # 見つからなかった場合

def binary_search_count(data, target):  # 二分探索（比較回数付き）
    """二分探索を実行し、(インデックス, 比較回数)を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    count = 0  # 比較回数カウンター
    while left <= right:  # 探索範囲がある間繰り返す
        count += 1  # 比較を1回カウント
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return (mid, count)  # 結果を返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return (-1, count)  # 見つからなかった場合

# --- 100個のデータで比較 ---
data = list(range(1, 101))  # [1, 2, ..., 100]のリストを作る
print(f"データ数: {len(data)}個")  # データ数を表示する
print("-" * 55)  # 区切り線
print(f"{'target':>6}  {'逐次':>8}  {'二分':>8}  {'差':>8}")  # ヘッダー行
print("-" * 55)  # 区切り線

for target in [1, 25, 50, 75, 100, 999]:  # テストする値のリスト
    _, cnt_l = linear_search_count(data, target)  # 逐次探索の比較回数を取得する
    _, cnt_b = binary_search_count(data, target)  # 二分探索の比較回数を取得する
    diff = cnt_l - cnt_b  # 差を計算する
    print(f"{target:>6}  {cnt_l:>5}回  {cnt_b:>5}回  {diff:>+5}回")  # 結果を表示する
```

---

### 標準課題6 解答

```python
# ============================================================
# 標準課題6 解答: 平均比較回数の比較
# ============================================================

def linear_search_count(data, target):  # 逐次探索（比較回数付き）
    """逐次探索を実行し、(インデックス, 比較回数)を返す"""
    count = 0  # 比較回数カウンター
    for i in range(len(data)):  # 先頭から順に調べる
        count += 1  # 比較を1回カウント
        if data[i] == target:  # 一致したら
            return (i, count)  # 結果を返す
    return (-1, count)  # 見つからなかった場合

def binary_search_count(data, target):  # 二分探索（比較回数付き）
    """二分探索を実行し、(インデックス, 比較回数)を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    count = 0  # 比較回数カウンター
    while left <= right:  # 探索範囲がある間繰り返す
        count += 1  # 比較を1回カウント
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return (mid, count)  # 結果を返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return (-1, count)  # 見つからなかった場合

# --- 1000個のデータで平均比較回数を計算 ---
data = list(range(1, 1001))  # [1, 2, ..., 1000]のリストを作る
total_linear = 0  # 逐次探索の合計比較回数
total_binary = 0  # 二分探索の合計比較回数

for target in data:  # すべての値を探索する
    _, cnt_l = linear_search_count(data, target)  # 逐次探索の比較回数を取得する
    _, cnt_b = binary_search_count(data, target)  # 二分探索の比較回数を取得する
    total_linear += cnt_l  # 逐次探索の合計に加算する
    total_binary += cnt_b  # 二分探索の合計に加算する

avg_linear = total_linear / len(data)  # 逐次探索の平均を計算する
avg_binary = total_binary / len(data)  # 二分探索の平均を計算する

print(f"データ数: {len(data)}個")  # データ数を表示する
print(f"逐次探索の平均比較回数: {avg_linear:.1f}回")  # 逐次探索の平均を表示する
print(f"二分探索の平均比較回数: {avg_binary:.1f}回")  # 二分探索の平均を表示する
print(f"二分探索は逐次探索の約 {avg_linear / avg_binary:.1f}倍 効率的!")  # 効率比を表示する
```

---

### 標準課題7 解答

```python
# ============================================================
# 標準課題7 解答: bisect_leftで検索する関数
# ============================================================

import bisect  # bisectモジュールをインポートする

def bisect_search(data, target):  # bisectを使った検索関数
    """bisect_leftを使って値を検索する。見つかればインデックス、なければ-1"""
    pos = bisect.bisect_left(data, target)  # targetの挿入位置を求める
    if pos < len(data) and data[pos] == target:  # 挿入位置の値がtargetと一致するか
        return pos  # 一致すればインデックスを返す
    return -1  # 一致しなければ-1を返す

# --- テスト ---
data = [2, 5, 8, 12, 16, 23, 38, 42, 56, 72, 91, 100]  # ソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

for target in [23, 50, 2, 100]:  # テストする値のリスト
    result = bisect_search(data, target)  # bisect_searchを実行する
    if result != -1:  # 見つかった場合
        print(f"target={target:>3}: インデックス{result}で発見")  # 結果を表示する
    else:  # 見つからなかった場合
        print(f"target={target:>3}: 見つかりませんでした(-1)")  # 見つからないと表示する
```

---

### 標準課題8 解答

```python
# ============================================================
# 標準課題8 解答: bisectで出現回数を数える
# ============================================================

import bisect  # bisectモジュールをインポートする

def count_value(data, target):  # 出現回数を数える関数
    """ソート済みリストでtargetの出現回数を返す"""
    left_pos = bisect.bisect_left(data, target)  # targetの左端位置を求める
    right_pos = bisect.bisect_right(data, target)  # targetの右端+1の位置を求める
    return right_pos - left_pos  # 差が出現回数になる

# --- テスト ---
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5]  # 重複を含むソート済みリスト
print(f"データ: {data}")  # データを表示する
print("-" * 40)  # 区切り線

for target in [1, 2, 3, 4, 5, 6]:  # テストする値のリスト
    count = count_value(data, target)  # 出現回数を計算する
    print(f"target={target}: {count}個")  # 結果を表示する
```

---

### 標準課題9 解答

```python
# ============================================================
# 標準課題9 解答: matplotlibでベンチマーク結果をグラフ化
# ============================================================

import time  # 時間計測用モジュール
import random  # ランダム値生成用モジュール
import matplotlib.pyplot as plt  # グラフ描画用モジュール
import numpy as np  # 数値計算用モジュール

def linear_search(data, target):  # 逐次探索の関数
    """逐次探索"""
    for i in range(len(data)):  # 先頭から順に調べる
        if data[i] == target:  # 一致したら
            return i  # インデックスを返す
    return -1  # 見つからなければ-1

def binary_search(data, target):  # 二分探索の関数
    """二分探索"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    while left <= right:  # 探索範囲がある間
        mid = (left + right) // 2  # 中央を計算する
        if data[mid] == target:  # 一致したら
            return mid  # 返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右へ
        else:  # 大きければ
            right = mid - 1  # 左へ
    return -1  # 見つからない

# --- ベンチマーク実行 ---
sizes = [1000, 5000, 10000, 50000, 100000]  # テストするデータサイズ
num_queries = 500  # 各サイズでの探索回数
times_linear = []  # 逐次探索の結果リスト
times_binary = []  # 二分探索の結果リスト

for size in sizes:  # 各サイズについてテストする
    data = list(range(size))  # ソート済みリストを作る
    targets = [random.randint(0, size - 1) for _ in range(num_queries)]  # ランダムtarget

    start = time.perf_counter()  # 二分探索の計測開始
    for t in targets:  # 各targetを探索する
        binary_search(data, t)  # 二分探索を実行する
    times_binary.append(time.perf_counter() - start)  # 経過時間を記録する

    start = time.perf_counter()  # 逐次探索の計測開始
    for t in targets:  # 各targetを探索する
        linear_search(data, t)  # 逐次探索を実行する
    times_linear.append(time.perf_counter() - start)  # 経過時間を記録する

    print(f"N={size:>7,}: Linear={times_linear[-1]:.4f}s, Binary={times_binary[-1]:.4f}s")  # 途中経過表示

# --- グラフ描画 ---
fig, ax = plt.subplots(figsize=(10, 6))  # グラフのサイズを設定する
x = np.arange(len(sizes))  # X軸の位置を作る
width = 0.35  # 棒の幅を設定する

ax.bar(x - width / 2, times_linear, width, label="Linear Search", color="#e74c3c")  # 逐次探索の棒
ax.bar(x + width / 2, times_binary, width, label="Binary Search", color="#3498db")  # 二分探索の棒
ax.set_xlabel("Data Size")  # X軸ラベルを設定する
ax.set_ylabel("Time (seconds)")  # Y軸ラベルを設定する
ax.set_title("Linear Search vs Binary Search Benchmark")  # タイトルを設定する
ax.set_xticks(x)  # X軸の目盛り位置を設定する
ax.set_xticklabels([f"{s // 1000}k" for s in sizes])  # X軸のラベルを設定する
ax.legend()  # 凡例を表示する
ax.grid(axis="y", alpha=0.3)  # Y軸方向の薄いグリッドを表示する

plt.tight_layout()  # レイアウトを自動調整する
plt.savefig("search_benchmark.png", dpi=150)  # ファイルに保存する
plt.show()  # グラフを表示する
print("グラフを search_benchmark.png に保存しました")  # 完了メッセージ
```

---

### 標準課題10 解答

```python
# ============================================================
# 標準課題10 解答: O(log n) が成り立つことを確認する
# ============================================================

import math  # 数学関数用モジュール

def binary_search_count(data, target):  # 二分探索（比較回数付き）
    """二分探索を実行し、比較回数を返す"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    count = 0  # 比較回数カウンター
    while left <= right:  # 探索範囲がある間繰り返す
        count += 1  # 比較回数を増やす
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return count  # 比較回数を返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return count  # 見つからなかった場合も比較回数を返す

# --- 各データサイズで平均比較回数を計測 ---
sizes = [100, 1000, 10000, 100000, 1000000]  # テストするデータサイズ
print(f"{'データ数':>10}  {'平均比較回数':>10}  {'log2(n)':>8}  {'差':>6}")  # ヘッダー行
print("-" * 50)  # 区切り線

for n in sizes:  # 各サイズについてテストする
    data = list(range(n))  # ソート済みリストを作る
    total_count = 0  # 合計比較回数
    sample_size = min(n, 1000)  # サンプル数（最大1000）
    step = max(1, n // sample_size)  # サンプリング間隔を計算する

    for target in range(0, n, step):  # 等間隔でサンプリングする
        total_count += binary_search_count(data, target)  # 比較回数を加算する

    actual_samples = len(range(0, n, step))  # 実際のサンプル数を計算する
    avg_count = total_count / actual_samples  # 平均比較回数を計算する
    theory = math.log2(n)  # 理論値log2(n)を計算する
    diff = avg_count - theory  # 実測値と理論値の差を計算する

    print(f"{n:>10,}  {avg_count:>10.2f}  {theory:>8.2f}  {diff:>+6.2f}")  # 結果を表示する

print()  # 空行
print("平均比較回数はlog2(n)に近い値になり、O(log n)が成り立つことが確認できます")  # まとめ
```

---

### 発展課題1 解答

```python
# ============================================================
# 発展課題1 解答: ひらがな単語当てゲーム
# ============================================================

import random  # ランダム選択用モジュール
import math  # 数学関数用モジュール

# --- ひらがな辞書 ---
hiragana_dict = [
    "あいす", "あさがお", "いちご", "いるか", "うさぎ",
    "うちわ", "えんぴつ", "おにぎり", "かえる", "かさ",
    "きつね", "きのこ", "くじら", "くつ", "けいたい",
    "こあら", "さくら", "さんま", "しまうま", "すいか",
    "すずめ", "せみ", "そら", "たこ", "たぬき",
    "ちきゅう", "つばめ", "てんとう", "とけい", "なす",
    "にじ", "ぬいぐるみ", "ねこ", "のり", "はな",
    "ひこうき", "ふうせん", "へび", "ほし", "まくら",
    "みかん", "むしめがね", "めがね", "もも", "やかん",
    "ゆき", "よる", "らくだ", "りんご", "るすばん",
    "れいぞうこ", "ろうそく", "わに", "あひる", "いす",
    "うめ", "えび", "おと", "かぜ", "きく",
    "くも", "けむし", "こい", "さかな", "しか",
    "すし", "せかい",
]
hiragana_dict.sort()  # 辞書順にソートする

def play_game():  # 対話プレイモード
    """プレイヤーが単語を入力して当てるゲーム"""
    answer = random.choice(hiragana_dict)  # 正解をランダムに選ぶ
    guess_count = 0  # 推測回数カウンター
    optimal = math.ceil(math.log2(len(hiragana_dict)))  # 理論最小回数を計算する

    print("ひらがな単語当てゲーム!")  # タイトルを表示する
    print(f"辞書のサイズ: {len(hiragana_dict)}語")  # 辞書サイズを表示する
    print(f"二分探索の理論最小: {optimal}回")  # 理論最小回数を表示する
    print("-" * 40)  # 区切り線

    while True:  # 正解するまで繰り返す
        guess = input(f"推測{guess_count + 1}回目 > ")  # プレイヤーの入力を受け取る
        guess_count += 1  # 推測回数を増やす

        if guess == answer:  # 正解の場合
            print(f"正解! 答えは「{answer}」でした!")  # 正解メッセージを表示する
            print(f"あなたの回数: {guess_count}回 (理論最小: {optimal}回)")  # 回数比較
            break  # ゲーム終了
        elif guess < answer:  # 辞書順で前の場合
            print(f"  → 「{guess}」より【あと】です")  # ヒントを表示する
        else:  # 辞書順で後の場合
            print(f"  → 「{guess}」より【まえ】です")  # ヒントを表示する

def auto_play():  # 自動プレイモード（二分探索）
    """コンピュータが二分探索で単語を当てるデモ"""
    answer = random.choice(hiragana_dict)  # 正解をランダムに選ぶ
    print(f"\n自動プレイ（正解: {answer}）")  # 正解を表示する
    print("-" * 40)  # 区切り線

    left = 0  # 探索範囲の左端
    right = len(hiragana_dict) - 1  # 探索範囲の右端
    guess_count = 0  # 推測回数カウンター

    while left <= right:  # 探索範囲がある間繰り返す
        guess_count += 1  # 推測回数を増やす
        mid = (left + right) // 2  # 中央のインデックスを計算する
        guess = hiragana_dict[mid]  # 中央の単語を取得する

        print(f"  推測{guess_count}: 「{guess}」(範囲=[{left}..{right}])", end="")  # 推測を表示

        if guess == answer:  # 正解の場合
            print(" → 正解!")  # 正解メッセージ
            print(f"  {guess_count}回で発見!")  # 回数を表示する
            return  # 関数を終了する
        elif guess < answer:  # 辞書順で前の場合
            print(" → もっと【あと】")  # ヒントを表示する
            left = mid + 1  # 左端を移動する
        else:  # 辞書順で後の場合
            print(" → もっと【まえ】")  # ヒントを表示する
            right = mid - 1  # 右端を移動する

# --- 実行 ---
# play_game()  # 対話モードで遊ぶ場合はコメントを外す
auto_play()  # 自動プレイを3回実行する
auto_play()  # 2回目の自動プレイ
auto_play()  # 3回目の自動プレイ
```

---

### 発展課題2 解答

```python
# ============================================================
# 発展課題2 解答: 100万件ベンチマーク
# ============================================================

import random  # ランダム値生成用モジュール
import time  # 時間計測用モジュール

def linear_search(data, target):  # 逐次探索の関数
    """逐次探索"""
    for i in range(len(data)):  # 先頭から順に調べる
        if data[i] == target:  # 一致したら
            return i  # インデックスを返す
    return -1  # 見つからなければ-1

def binary_search(data, target):  # 二分探索の関数
    """二分探索"""
    left = 0  # 左端を先頭にする
    right = len(data) - 1  # 右端を末尾にする
    while left <= right:  # 探索範囲がある間繰り返す
        mid = (left + right) // 2  # 中央のインデックスを計算する
        if data[mid] == target:  # 一致したら
            return mid  # インデックスを返す
        elif data[mid] < target:  # 小さければ
            left = mid + 1  # 右半分へ
        else:  # 大きければ
            right = mid - 1  # 左半分へ
    return -1  # 見つからなければ-1

# --- データ準備 ---
n = 1_000_000  # 100万件
print(f"データ生成中... (N={n:,})")  # データ生成中のメッセージ
sorted_data = sorted(random.randint(0, 999_999) for _ in range(n))  # ソート済みリスト生成
num_queries = 1_000  # 探索回数
targets = [random.randint(0, 999_999) for _ in range(num_queries)]  # ランダムtarget

# --- 二分探索の計測 ---
found_b = 0  # 二分探索で見つかった数
start = time.perf_counter()  # 計測開始
for t in targets:  # 各targetを探索する
    if binary_search(sorted_data, t) != -1:  # 見つかったら
        found_b += 1  # カウントする
time_binary = time.perf_counter() - start  # 経過時間

# --- 逐次探索の計測 ---
found_l = 0  # 逐次探索で見つかった数
print("逐次探索実行中（時間がかかります）...")  # 待ちメッセージ
start = time.perf_counter()  # 計測開始
for t in targets:  # 各targetを探索する
    if linear_search(sorted_data, t) != -1:  # 見つかったら
        found_l += 1  # カウントする
time_linear = time.perf_counter() - start  # 経過時間

# --- 結果表示 ---
print(f"\nデータ数: {n:,}件  探索回数: {num_queries:,}回")  # テスト条件
print("=" * 55)  # 区切り線
print(f"Binary Search : {time_binary:>8.3f}秒  (found={found_b}, not={num_queries - found_b})")  # 二分探索結果
print(f"Linear Search : {time_linear:>8.3f}秒  (found={found_l}, not={num_queries - found_l})")  # 逐次探索結果
print("=" * 55)  # 区切り線
if time_binary > 0:  # ゼロ除算を防ぐ
    print(f"\n二分探索は逐次探索の約 {time_linear / time_binary:,.0f}倍 速い!")  # 速度比を表示する
print(f"\n考察:")  # 考察セクション
print(f"- 逐次探索 O(n)  : 最大{n * num_queries:,}回の比較")  # 逐次探索の理論値
print(f"- 二分探索 O(log n): 約{n.bit_length() * num_queries:,}回の比較")  # 二分探索の理論値
```
