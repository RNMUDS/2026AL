# 第2回: データの内部処理と構造の理解

## 説明

### この授業で学ぶこと

Pythonには「データをまとめて扱う」ための仕組みがいくつかあります。
この授業では、代表的な4つのデータ構造を学び、それぞれの得意・不得意を理解します。

1. **リスト (`list`)** -- 順番のあるデータの集まり
2. **辞書 (`dict`)** -- 名前で引けるデータの集まり
3. **タプル (`tuple`)** -- 変更できないリスト
4. **セット (`set`)** -- 重複のないデータの集まり

---

### 1. リスト (`list`) -- 買い物リストのイメージ

日常の例: 買い物リストには順番があり、同じものが入ってもOK。
後から追加・削除・並べ替えができます。

```python
# --- リスト: 買い物リストの例 ---

# リストは角括弧 [] で作る
shopping_list = ["りんご", "牛乳", "パン", "卵"]

# 中身を表示する
print("買い物リスト:", shopping_list)

# 要素を追加する（末尾に追加される）
shopping_list.append("バター")
print("バターを追加:", shopping_list)

# インデックス（番号）でアクセスする（0から始まる！）
print("最初の品物:", shopping_list[0])   # "りんご"
print("3番目の品物:", shopping_list[2])   # "パン"

# 要素の数を調べる
print("品物の数:", len(shopping_list))    # 5

# リストは重複OK
shopping_list.append("りんご")
print("りんご追加（重複OK）:", shopping_list)
```

**出力:**
```
買い物リスト: ['りんご', '牛乳', 'パン', '卵']
バターを追加: ['りんご', '牛乳', 'パン', '卵', 'バター']
最初の品物: りんご
3番目の品物: パン
品物の数: 5
りんご追加（重複OK）: ['りんご', '牛乳', 'パン', '卵', 'バター', 'りんご']
```

---

### 2. 辞書 (`dict`) -- 電話帳のイメージ

日常の例: 電話帳では「名前」で検索して「電話番号」を引きます。
辞書はキー（名前）と値（番号）のペアでデータを管理します。

```python
# --- 辞書: 電話帳の例 ---

# 辞書は波括弧 {} で作る
# {キー: 値, キー: 値, ...} の形式
phone_book = {
    "田中": "090-1111-2222",
    "鈴木": "080-3333-4444",
    "佐藤": "070-5555-6666",
}

# 中身を表示する
print("電話帳:", phone_book)

# キーで値を取得する（電話帳を引く）
print("田中さんの番号:", phone_book["田中"])

# 新しい人を追加する
phone_book["山田"] = "090-7777-8888"
print("山田さん追加:", phone_book)

# キーが存在するかチェックする
print("田中さんは登録済み？:", "田中" in phone_book)  # True
print("高橋さんは登録済み？:", "高橋" in phone_book)  # False

# 全員の名前を表示する
print("登録者一覧:", list(phone_book.keys()))
```

**出力:**
```
電話帳: {'田中': '090-1111-2222', '鈴木': '080-3333-4444', '佐藤': '070-5555-6666'}
田中さんの番号: 090-1111-2222
山田さん追加: {'田中': '090-1111-2222', '鈴木': '080-3333-4444', '佐藤': '070-5555-6666', '山田': '090-7777-8888'}
田中さんは登録済み？: True
高橋さんは登録済み？: False
登録者一覧: ['田中', '鈴木', '佐藤', '山田']
```

---

### 3. タプル (`tuple`) -- 座標のイメージ

日常の例: 地図の座標 (35.6, 139.7) は「変えてはいけない」データです。
タプルは作った後に変更できないリストです。

```python
# --- タプル: 座標の例 ---

# タプルは丸括弧 () で作る
tokyo_location = (35.6762, 139.6503)

# 中身を表示する
print("東京の座標:", tokyo_location)

# インデックスでアクセスできる（リストと同じ）
print("緯度:", tokyo_location[0])
print("経度:", tokyo_location[1])

# タプルは変更できない（エラーになる！）
# tokyo_location[0] = 0  # ← これを実行するとTypeError

# 複数の値を一度に変数に入れる（アンパック）
latitude, longitude = tokyo_location
print(f"緯度: {latitude}, 経度: {longitude}")

# 関数から複数の値を返すときに便利
def get_min_max(numbers):
    """リストの最小値と最大値をタプルで返す関数"""
    return (min(numbers), max(numbers))

# 戻り値をアンパックで受け取る
data = [3, 1, 4, 1, 5, 9, 2, 6]
minimum, maximum = get_min_max(data)
print(f"最小値: {minimum}, 最大値: {maximum}")
```

**出力:**
```
東京の座標: (35.6762, 139.6503)
緯度: 35.6762
経度: 139.6503
緯度: 35.6762, 経度: 139.6503
最小値: 1, 最大値: 9
```

---

### 4. セット (`set`) -- 部員名簿のイメージ

日常の例: 部活の名簿には同じ人が2回入ることはありません。
セットは重複を自動で排除するデータ構造です。

```python
# --- セット: 部員名簿の例 ---

# セットは波括弧 {} で作る（辞書と似ているが、キー:値 の形ではない）
members = {"田中", "鈴木", "佐藤", "田中"}  # 田中が2回！

# 中身を表示する（重複が自動で消える）
print("部員:", members)  # 田中は1回だけ

# 要素を追加する
members.add("山田")
print("山田追加:", members)

# すでにある要素を追加しても変わらない
members.add("鈴木")
print("鈴木追加（変化なし）:", members)

# 要素が含まれるかチェックする（超高速！）
print("田中は部員？:", "田中" in members)     # True
print("高橋は部員？:", "高橋" in members)     # False

# 集合演算ができる
tennis_club = {"田中", "佐藤", "高橋"}
soccer_club = {"鈴木", "佐藤", "山田"}

# 両方に入っている人（共通部分 = 交差）
both = tennis_club & soccer_club
print("テニス部かつサッカー部:", both)

# どちらかに入っている人（合体 = 和集合）
either = tennis_club | soccer_club
print("どちらかに所属:", either)
```

**出力:**
```
部員: {'鈴木', '佐藤', '田中'}
山田追加: {'鈴木', '佐藤', '田中', '山田'}
鈴木追加（変化なし）: {'鈴木', '佐藤', '田中', '山田'}
田中は部員？: True
高橋は部員？: False
テニス部かつサッカー部: {'佐藤'}
どちらかに所属: {'鈴木', '田中', '高橋', '佐藤', '山田'}
```

---

### 速度の違い -- どれを使うべき？

データ構造によって、同じ操作でも速度が大きく違います。

| 操作 | list | dict | set | tuple |
|---|---|---|---|---|
| 要素の検索 (`in`) | 遅い (先頭から順に探す) | **速い** (キーで即座に引く) | **速い** (ハッシュで即座に判定) | 遅い (リストと同じ) |
| 要素の追加 | 速い (末尾に追加) | **速い** (キーで即座に追加) | **速い** (ハッシュで即座に追加) | 不可 |
| 順番の保持 | あり | あり (Python 3.7+) | なし | あり |
| 重複 | 許可 | キーは不可 | 不可 | 許可 |
| 変更 | 可能 | 可能 | 可能 | **不可** |

**使い分けの目安:**
- 順番が大事でデータを後から変えたい → **`list`**
- 名前（キー）でデータを引きたい → **`dict`**
- 重複を排除したい、含まれるか高速に調べたい → **`set`**
- 変更してはいけないデータ → **`tuple`**

```python
# --- 速度の違いを体感する ---
import time

# 大きなリストとセットを作る（0〜999999の数）
big_list = list(range(1_000_000))    # リスト版
big_set = set(range(1_000_000))      # セット版

# 「999999が含まれるか？」を調べる時間を計測する

# リスト版（先頭から順に探すので遅い）
start_time = time.time()
result_list = 999_999 in big_list
end_time = time.time()
list_time = end_time - start_time
print(f"リストで検索: {list_time:.6f}秒")

# セット版（ハッシュで即座に見つけるので速い）
start_time = time.time()
result_set = 999_999 in big_set
end_time = time.time()
set_time = end_time - start_time
print(f"セットで検索: {set_time:.6f}秒")

# 速度の比較
if list_time > 0 and set_time > 0:
    print(f"セットはリストの約{list_time / set_time:.0f}倍速い！")
```

---

## 例題と課題

### 例題1: リストの基本操作

リストの作成、追加、アクセス、スライスの基本を学びます。

```python
# ===================================
# 例題1: リストの基本操作
# ===================================

# --- リストの作成と要素の追加 ---
print("=== リストの基本 ===")

# 空のリストを作る
fruits = []
# 現在の状態を表示する
print(f"空のリスト: {fruits}")

# 要素を1つずつ追加する（append）
fruits.append("りんご")
print(f"りんご追加: {fruits}")

fruits.append("バナナ")
print(f"バナナ追加: {fruits}")

fruits.append("みかん")
print(f"みかん追加: {fruits}")

# --- インデックスでアクセスする ---
print()
print("=== インデックスアクセス ===")
# インデックスは0から始まる
print(f"  fruits[0] = {fruits[0]}")  # 先頭の要素
print(f"  fruits[1] = {fruits[1]}")  # 2番目の要素
print(f"  fruits[2] = {fruits[2]}")  # 3番目の要素
# マイナスのインデックスは末尾から
print(f"  fruits[-1] = {fruits[-1]}")  # 最後の要素

# --- リストの長さ ---
print()
print(f"  要素数: {len(fruits)}")

# --- スライスで部分リストを取得する ---
print()
print("=== スライス ===")
numbers = [10, 20, 30, 40, 50, 60, 70]
print(f"  元のリスト: {numbers}")
# [開始:終了] で部分リストを取得（終了は含まない）
print(f"  numbers[1:4] = {numbers[1:4]}")  # [20, 30, 40]
# 先頭から3つ
print(f"  numbers[:3]  = {numbers[:3]}")   # [10, 20, 30]
# 後ろから2つ
print(f"  numbers[-2:] = {numbers[-2:]}")  # [60, 70]

# --- forループでリストの全要素を処理する ---
print()
print("=== forループで全要素を表示 ===")
for i, fruit in enumerate(fruits):
    # enumerate()でインデックスと要素を同時に取得する
    print(f"  [{i}] {fruit}")
```

**実行結果:**
```
=== リストの基本 ===
空のリスト: []
りんご追加: ['りんご']
バナナ追加: ['りんご', 'バナナ']
みかん追加: ['りんご', 'バナナ', 'みかん']

=== インデックスアクセス ===
  fruits[0] = りんご
  fruits[1] = バナナ
  fruits[2] = みかん
  fruits[-1] = みかん

  要素数: 3

=== スライス ===
  元のリスト: [10, 20, 30, 40, 50, 60, 70]
  numbers[1:4] = [20, 30, 40]
  numbers[:3]  = [10, 20, 30]
  numbers[-2:] = [60, 70]

=== forループで全要素を表示 ===
  [0] りんご
  [1] バナナ
  [2] みかん
```

---

### 標準課題1（超やさしい）: 点数リストの合計と平均

**課題:** 5人分のテスト点数をリストに入れて、合計と平均を計算するプログラムを作りなさい。

**要件:**
- 点数リスト `scores = [85, 72, 90, 68, 95]` を使う
- `for` ループで合計を計算する（`sum()` は使わない）
- 平均 = 合計 / 人数 で計算する
- 途中の計算過程（毎回の合計加算）を表示する
- 最終結果（合計と平均）を表示する

**期待される出力例:**
```
=== テスト点数の集計 ===
  85を足す → 合計: 85
  72を足す → 合計: 157
  90を足す → 合計: 247
  68を足す → 合計: 315
  95を足す → 合計: 410
合計: 410
平均: 82.0
```

---

### 標準課題2（超やさしい）: リストの最大値を探す

**課題:** リストの中から最大値を探して、そのインデックスとともに表示するプログラムを作りなさい。

**要件:**
- 数値リスト `numbers = [34, 67, 23, 89, 12, 56, 78]` を使う
- `max()` を使わずに `for` ループで最大値を探す
- 各要素との比較過程を表示する
- 最大値とそのインデックスを表示する

**期待される出力例:**
```
=== 最大値を探す ===
  numbers[0] = 34 → 暫定最大値: 34
  numbers[1] = 67 → 更新！ 暫定最大値: 67
  numbers[2] = 23 → 変更なし
  numbers[3] = 89 → 更新！ 暫定最大値: 89
  numbers[4] = 12 → 変更なし
  numbers[5] = 56 → 変更なし
  numbers[6] = 78 → 変更なし
最大値: 89（インデックス: 3）
```

---

### 例題2: 辞書の基本操作

辞書の作成、値の取得、追加、ループ処理を学びます。

```python
# ===================================
# 例題2: 辞書の基本操作
# ===================================

# --- 辞書の作成と値の取得 ---
print("=== 辞書の基本 ===")

# 商品と価格の辞書を作る
prices = {
    "りんご": 150,
    "バナナ": 100,
    "みかん": 80,
}
# 辞書の中身を表示する
print(f"  商品一覧: {prices}")

# キーで値を取得する
print(f"  りんごの価格: {prices['りんご']}円")
print(f"  バナナの価格: {prices['バナナ']}円")

# --- 辞書への追加と更新 ---
print()
print("=== 追加と更新 ===")

# 新しいキーと値を追加する
prices["ぶどう"] = 300
print(f"  ぶどう追加: {prices}")

# 既存のキーの値を更新する
prices["りんご"] = 180
print(f"  りんご値上げ: {prices}")

# --- 辞書のループ処理 ---
print()
print("=== 全商品を表示 ===")

# items()でキーと値のペアを取得する
for name, price in prices.items():
    # 各商品の名前と価格を表示する
    print(f"  {name}: {price}円")

# --- 辞書で集計する（文字の出現回数） ---
print()
print("=== 文字の出現回数を数える ===")

# 対象の文字列
text = "banana"
print(f"  対象: '{text}'")

# 空の辞書を作る
char_count = {}

# 1文字ずつ処理する
for char in text:
    # すでに辞書にあるかチェックする
    if char in char_count:
        # あれば+1
        char_count[char] = char_count[char] + 1
    else:
        # なければ1で初期化
        char_count[char] = 1
    # 途中経過を表示する
    print(f"    '{char}' を処理 → {char_count}")

# 最終結果を表示する
print(f"  結果: {char_count}")
```

**実行結果:**
```
=== 辞書の基本 ===
  商品一覧: {'りんご': 150, 'バナナ': 100, 'みかん': 80}
  りんごの価格: 150円
  バナナの価格: 100円

=== 追加と更新 ===
  ぶどう追加: {'りんご': 150, 'バナナ': 100, 'みかん': 80, 'ぶどう': 300}
  りんご値上げ: {'りんご': 180, 'バナナ': 100, 'みかん': 80, 'ぶどう': 300}

=== 全商品を表示 ===
  りんご: 180円
  バナナ: 100円
  みかん: 80円
  ぶどう: 300円

=== 文字の出現回数を数える ===
  対象: 'banana'
    'b' を処理 → {'b': 1}
    'a' を処理 → {'b': 1, 'a': 1}
    'n' を処理 → {'b': 1, 'a': 1, 'n': 1}
    'a' を処理 → {'b': 1, 'a': 2, 'n': 1}
    'n' を処理 → {'b': 1, 'a': 2, 'n': 2}
    'a' を処理 → {'b': 1, 'a': 3, 'n': 2}
  結果: {'b': 1, 'a': 3, 'n': 2}
```

---

### 標準課題3（やさしい）: 英和辞書プログラム

**課題:** 英単語を入力すると日本語訳を返す「英和辞書」プログラムを作りなさい。

**要件:**
- 少なくとも5つの英単語と日本語訳を辞書に登録する
- ユーザーが英単語を入力すると日本語訳を表示する
- 辞書にない単語の場合は「登録されていません」と表示する
- 「quit」と入力したら終了する
- `while` ループで繰り返し検索できるようにする

**期待される出力例:**
```
=== 英和辞書 ===
英単語を入力（quitで終了）: apple
  apple → りんご
英単語を入力（quitで終了）: dog
  dog → 犬
英単語を入力（quitで終了）: car
  登録されていません: car
英単語を入力（quitで終了）: quit
終了します。
```

---

### 標準課題4（やさしい）: 成績集計（辞書で管理）

**課題:** 3人の学生の名前と点数を辞書で管理し、平均点と最高得点者を表示するプログラムを作りなさい。

**要件:**
- 辞書の形式: `{"田中": 85, "鈴木": 92, "佐藤": 78}`
- 全員の名前と点数を表示する
- 全員の平均点を計算して表示する
- 最高得点者の名前と点数を表示する（`max()` は使わず、ループで探す）

**期待される出力例:**
```
=== 成績一覧 ===
  田中: 85点
  鈴木: 92点
  佐藤: 78点
平均点: 85.0点
最高得点者: 鈴木（92点）
```

---

### 例題3: セットの操作

セットの重複排除と集合演算を学びます。

```python
# ===================================
# 例題3: セットの操作
# ===================================

# --- 重複の排除 ---
print("=== セットで重複を排除 ===")

# 重複のあるリスト
numbers_with_duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"  元のリスト: {numbers_with_duplicates}")
print(f"  要素数: {len(numbers_with_duplicates)}")

# セットに変換して重複を排除する
unique_numbers = set(numbers_with_duplicates)
print(f"  セットに変換: {unique_numbers}")
print(f"  要素数: {len(unique_numbers)}")

# ソートしたリストに戻す
sorted_unique = sorted(unique_numbers)
print(f"  ソートしたリスト: {sorted_unique}")

# --- 集合演算 ---
print()
print("=== 集合演算 ===")

# 2つのクラスの受講者
class_a = {"田中", "鈴木", "佐藤", "山田", "高橋"}
class_b = {"鈴木", "佐藤", "伊藤", "渡辺", "高橋"}
print(f"  クラスA: {class_a}")
print(f"  クラスB: {class_b}")

# 交差（両方のクラスに所属）
both_classes = class_a & class_b
print(f"  両方に所属: {both_classes}")

# 和集合（どちらかに所属）
any_class = class_a | class_b
print(f"  いずれかに所属: {any_class}")

# 差集合（Aにだけ所属）
only_a = class_a - class_b
print(f"  Aだけに所属: {only_a}")

# 対称差（片方だけに所属）
exclusive = class_a ^ class_b
print(f"  片方だけに所属: {exclusive}")

# --- in 演算子による高速検索 ---
print()
print("=== メンバーシップテスト ===")
# セットのin演算子は非常に高速
name_to_check = "鈴木"
result = name_to_check in class_a
print(f"  '{name_to_check}' はクラスAに所属？ {result}")
```

**実行結果:**
```
=== セットで重複を排除 ===
  元のリスト: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
  要素数: 11
  セットに変換: {1, 2, 3, 4, 5, 6, 9}
  要素数: 7
  ソートしたリスト: [1, 2, 3, 4, 5, 6, 9]

=== 集合演算 ===
  クラスA: {'高橋', '山田', '田中', '鈴木', '佐藤'}
  クラスB: {'高橋', '伊藤', '渡辺', '鈴木', '佐藤'}
  両方に所属: {'高橋', '鈴木', '佐藤'}
  いずれかに所属: {'高橋', '山田', '田中', '伊藤', '渡辺', '鈴木', '佐藤'}
  Aだけに所属: {'山田', '田中'}
  片方だけに所属: {'山田', '田中', '伊藤', '渡辺'}

=== メンバーシップテスト ===
  '鈴木' はクラスAに所属？ True
```

---

### 標準課題5（やややさしい）: リストの重複を排除する

**課題:** リストから重複を排除し、元の順序を保ったまま新しいリストを作るプログラムを作りなさい。

**要件:**
- 入力リスト: `[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]`
- セットを使って「すでに見た要素か」を判定する
- 元のリストの出現順序を保つ（`set()` で変換するだけでは順序が保証されない）
- 途中の判定過程を表示する

**期待される出力例:**
```
=== 重複排除（順序保持） ===
  3 → 初出現、追加
  1 → 初出現、追加
  4 → 初出現、追加
  1 → 既出、スキップ
  5 → 初出現、追加
  9 → 初出現、追加
  2 → 初出現、追加
  6 → 初出現、追加
  5 → 既出、スキップ
  3 → 既出、スキップ
  5 → 既出、スキップ
結果: [3, 1, 4, 5, 9, 2, 6]
```

---

### 標準課題6（やややさしい）: 2つのリストの共通要素

**課題:** 2つのリストに共通する要素をセットを使って求めるプログラムを作りなさい。

**要件:**
- リストA: `[1, 3, 5, 7, 9, 11, 13]`
- リストB: `[2, 3, 5, 7, 11, 15]`
- セットの `&` 演算子を使って共通要素を求める
- 共通要素をソートして表示する
- Aだけにある要素、Bだけにある要素も表示する

**期待される出力例:**
```
リストA: [1, 3, 5, 7, 9, 11, 13]
リストB: [2, 3, 5, 7, 11, 15]
共通要素: [3, 5, 7, 11]
Aだけの要素: [1, 9, 13]
Bだけの要素: [2, 15]
```

---

### 例題4: リストのソートと検索

リストのソートとデータ検索の基本パターンを学びます。

```python
# ===================================
# 例題4: リストのソートと検索
# ===================================

# --- ソートの基本 ---
print("=== ソートの基本 ===")

# 数値リスト
scores = [78, 92, 65, 88, 71, 95, 83]
print(f"  元のリスト: {scores}")

# sorted()で新しいソート済みリストを作る（元のリストは変わらない）
ascending = sorted(scores)
print(f"  昇順ソート: {ascending}")

# reverse=Trueで降順
descending = sorted(scores, reverse=True)
print(f"  降順ソート: {descending}")

# 元のリストは変わっていないことを確認する
print(f"  元のリスト: {scores}")

# --- タプルのリストをソートする ---
print()
print("=== タプルのリストをソート ===")

# (名前, 点数) のタプルリスト
students = [
    ("田中", 78),
    ("鈴木", 92),
    ("佐藤", 65),
    ("山田", 88),
    ("高橋", 71),
]
print("  元のリスト:")
for name, score in students:
    print(f"    {name}: {score}点")

# 点数でソートする
# key=lambda x: x[1] は「タプルの2番目の要素で並べる」という意味
by_score = sorted(students, key=lambda x: x[1], reverse=True)
print()
print("  点数順（降順）:")
for rank, (name, score) in enumerate(by_score, start=1):
    # enumerate()で順位を振る
    print(f"    {rank}位: {name} - {score}点")

# --- リスト内の検索 ---
print()
print("=== リスト内の検索 ===")

# 特定の条件に合う要素を探す
print("  80点以上の学生:")
for name, score in students:
    # 80点以上かチェックする
    if score >= 80:
        print(f"    {name}: {score}点")
```

**実行結果:**
```
=== ソートの基本 ===
  元のリスト: [78, 92, 65, 88, 71, 95, 83]
  昇順ソート: [65, 71, 78, 83, 88, 92, 95]
  降順ソート: [95, 92, 88, 83, 78, 71, 65]
  元のリスト: [78, 92, 65, 88, 71, 95, 83]

=== タプルのリストをソート ===
  元のリスト:
    田中: 78点
    鈴木: 92点
    佐藤: 65点
    山田: 88点
    高橋: 71点

  点数順（降順）:
    1位: 鈴木 - 92点
    2位: 山田 - 88点
    3位: 田中 - 78点
    4位: 高橋 - 71点
    5位: 佐藤 - 65点

=== リスト内の検索 ===
  80点以上の学生:
    鈴木: 92点
    山田: 88点
```

---

### 標準課題7（やや普通）: 単語の出現頻度ランキング

**課題:** 文章中の各単語の出現回数を辞書で数え、出現回数の多い順にランキング表示するプログラムを作りなさい。

**要件:**
- 対象テキスト: `"the cat sat on the mat the cat ate the rat on the mat"`
- `split()` で単語に分割する
- 辞書で各単語の出現回数を数える
- `sorted()` と `key=lambda` で出現回数の多い順にソートする
- 途中の辞書の変化も表示する

**期待される出力例:**
```
=== 単語の出現頻度 ===
テキスト: the cat sat on the mat the cat ate the rat on the mat
単語数: 14

出現頻度ランキング:
  1位: the - 5回
  2位: cat - 2回
  3位: on - 2回
  4位: mat - 2回
  5位: sat - 1回
  ...
```

---

### 標準課題8（やや普通）: 名前リストのソートと検索

**課題:** 名前と年齢のリストをソートし、特定の条件で検索するプログラムを作りなさい。

**要件:**
- データは以下のタプルリストを使う:
  ```python
  people = [("田中", 25), ("鈴木", 32), ("佐藤", 19), ("山田", 28), ("高橋", 22)]
  ```
- 年齢の昇順でソートして表示する
- 名前の五十音順でソートして表示する（ヒント: `key=lambda x: x[0]`）
- 25歳以上の人だけを抽出して表示する
- 最年長と最年少の人を表示する

**期待される出力例:**
```
=== 年齢順 ===
  佐藤: 19歳
  高橋: 22歳
  田中: 25歳
  山田: 28歳
  鈴木: 32歳

=== 25歳以上 ===
  田中: 25歳
  鈴木: 32歳
  山田: 28歳

最年長: 鈴木（32歳）
最年少: 佐藤（19歳）
```

---

### 例題5: ファイル入出力（CSV）

CSVファイルへの書き込みと読み込みの基本を学びます。

```python
# ===================================
# 例題5: ファイル入出力（CSV）
# ===================================

# --- CSVファイルに書き込む ---
print("=== CSVファイルに書き込む ===")

# 書き込むデータ（タプルのリスト）
students = [
    ("田中", 85),
    ("鈴木", 92),
    ("佐藤", 78),
    ("山田", 88),
]

# ファイル名
filename = "students.csv"

# ファイルを書き込みモードで開く
with open(filename, "w", encoding="utf-8") as f:
    # ヘッダー行を書き込む
    f.write("名前,点数\n")
    print("  ヘッダー書き込み: 名前,点数")

    # データを1行ずつ書き込む
    for name, score in students:
        # カンマ区切りの行を作る
        line = f"{name},{score}\n"
        # ファイルに書き込む
        f.write(line)
        # 途中経過を表示する
        print(f"  書き込み: {name},{score}")

print(f"  ファイル保存完了: {filename}")

# --- CSVファイルから読み込む ---
print()
print("=== CSVファイルから読み込む ===")

# 読み込んだデータを格納するリスト
loaded_students = []

# ファイルを読み込みモードで開く
with open(filename, "r", encoding="utf-8") as f:
    # 全行をリストとして取得する
    lines = f.readlines()

    # 各行を処理する
    for i, line in enumerate(lines):
        # 行末の改行を除去する
        stripped = line.strip()

        # 1行目はヘッダーなのでスキップする
        if i == 0:
            print(f"  ヘッダー: {stripped}")
            continue

        # カンマで分割する
        parts = stripped.split(",")
        # 名前と点数を取り出す
        name = parts[0]
        score = int(parts[1])
        # タプルとしてリストに追加する
        loaded_students.append((name, score))
        # 途中経過を表示する
        print(f"  読み込み: {name} - {score}点")

# 読み込み結果を表示する
print(f"  読み込み完了: {len(loaded_students)}件")
print(f"  データ: {loaded_students}")
```

**実行結果:**
```
=== CSVファイルに書き込む ===
  ヘッダー書き込み: 名前,点数
  書き込み: 田中,85
  書き込み: 鈴木,92
  書き込み: 佐藤,78
  書き込み: 山田,88
  ファイル保存完了: students.csv

=== CSVファイルから読み込む ===
  ヘッダー: 名前,点数
  読み込み: 田中 - 85点
  読み込み: 鈴木 - 92点
  読み込み: 佐藤 - 78点
  読み込み: 山田 - 88点
  読み込み完了: 4件
  データ: [('田中', 85), ('鈴木', 92), ('佐藤', 78), ('山田', 88)]
```

---

### 標準課題9（普通）: 買い物リストのCSV保存と読込

**課題:** 買い物リスト（商品名と個数）をCSVファイルに保存し、読み込んで表示するプログラムを作りなさい。

**要件:**
- 買い物データ: `[("りんご", 3), ("牛乳", 1), ("パン", 2), ("卵", 1), ("バター", 1)]`
- `shopping.csv` に保存する（ヘッダー行あり: `商品名,個数`）
- 保存したファイルを読み込んで一覧表示する
- 読み込み時にファイルが存在しない場合は `try/except FileNotFoundError` で対処する
- 途中の書き込み・読み込み過程を表示する

**期待される出力例:**
```
=== 保存 ===
  りんご,3 を書き込み
  牛乳,1 を書き込み
  パン,2 を書き込み
  卵,1 を書き込み
  バター,1 を書き込み
保存完了: shopping.csv

=== 読み込み ===
  りんご: 3個
  牛乳: 1個
  パン: 2個
  卵: 1個
  バター: 1個
合計: 5品目、8個
```

---

### 標準課題10（普通）: 成績管理システム（CSV完全版）

**課題:** 複数の学生の名前・科目・点数をCSVファイルで管理するプログラムを作りなさい。

**要件:**
- データ形式: `名前,科目,点数`（例: `田中,数学,85`）
- 以下の機能を実装する:
  1. CSVファイルにデータを書き込む
  2. CSVファイルからデータを読み込む
  3. 学生ごとの平均点を計算して表示する
  4. 科目ごとの平均点を計算して表示する
- 辞書を使って学生別・科目別に集計する
- テストデータ:
  ```
  田中,数学,85
  田中,英語,72
  鈴木,数学,92
  鈴木,英語,88
  佐藤,数学,78
  佐藤,英語,95
  ```

**期待される出力例:**
```
=== 成績データ読み込み ===
  田中 - 数学: 85点
  田中 - 英語: 72点
  鈴木 - 数学: 92点
  鈴木 - 英語: 88点
  佐藤 - 数学: 78点
  佐藤 - 英語: 95点

=== 学生別 平均点 ===
  田中: 78.5点
  鈴木: 90.0点
  佐藤: 86.5点

=== 科目別 平均点 ===
  数学: 85.0点
  英語: 85.0点
```

---

## 発展課題

### 発展課題1: アナグラム判定（3つのアプローチ）

**課題:** 2つの文字列がアナグラム（文字の並べ替えで一致）かを3つの方法で判定するプログラムを作りなさい。

**要件:**
1. `is_anagram_sort(word1, word2)` -- ソートして比較する方法
2. `is_anagram_dict(word1, word2)` -- 辞書で文字を数える方法
3. `is_anagram_counter(word1, word2)` -- `collections.Counter` を使う方法
- 大文字小文字を区別しない（`.lower()` で統一）
- スペースを無視する（`.replace(" ", "")` で除去）
- 以下のテストケースで確認:
  - `"listen"` vs `"silent"` → True
  - `"hello"` vs `"world"` → False
  - `"Astronomer"` vs `"Moon starer"` → True
  - `"aabb"` vs `"abab"` → True
  - `"abc"` vs `"abcd"` → False

---

### 発展課題2: 数当てゲームのランキング（CSV保存付き）

**課題:** 第1回の数当てゲームにCSVランキング機能を追加しなさい。

**要件:**
- ゲーム終了後にプレイヤー名と試行回数を `ranking.csv` に保存する
- ゲーム開始時にCSVからランキングを読み込む
- ファイルが存在しない場合は空のランキングから始める
- 試行回数の少ない順にソートしてトップ5を表示する
- 難易度選択機能も付ける
- ゲームを繰り返し遊べるリトライ機能を付ける

---

## 解答例

### 標準課題1 解答

```python
# ===================================
# 標準課題1 解答: 点数リストの合計と平均
# ===================================

# --- テスト点数のリスト ---
scores = [85, 72, 90, 68, 95]
# リストの内容を表示する
print("=== テスト点数の集計 ===")

# --- 合計を計算する ---
# 合計を記録する変数を0で初期化する
total = 0

# forループで各点数を処理する
for score in scores:
    # 合計にscoreを足す
    total = total + score
    # 途中経過を表示する
    print(f"  {score}を足す → 合計: {total}")

# --- 平均を計算する ---
# 人数はリストの長さ
count = len(scores)
# 平均 = 合計 / 人数
average = total / count

# --- 結果を表示する ---
print(f"合計: {total}")
print(f"平均: {average}")
```

---

### 標準課題2 解答

```python
# ===================================
# 標準課題2 解答: リストの最大値を探す
# ===================================

# --- 数値リスト ---
numbers = [34, 67, 23, 89, 12, 56, 78]
# リストの内容を表示する
print("=== 最大値を探す ===")

# --- 最大値を探す ---
# 最初の要素を暫定最大値にする
max_value = numbers[0]
# 最大値のインデックスを記録する
max_index = 0

# forループで各要素を比較する
for i, num in enumerate(numbers):
    if i == 0:
        # 最初の要素は暫定最大値として設定済み
        print(f"  numbers[{i}] = {num} → 暫定最大値: {max_value}")
    elif num > max_value:
        # 現在の要素が暫定最大値より大きい場合、更新する
        max_value = num
        max_index = i
        print(f"  numbers[{i}] = {num} → 更新！ 暫定最大値: {max_value}")
    else:
        # 暫定最大値以下の場合は変更なし
        print(f"  numbers[{i}] = {num} → 変更なし")

# --- 結果を表示する ---
print(f"最大値: {max_value}（インデックス: {max_index}）")
```

---

### 標準課題3 解答

```python
# ===================================
# 標準課題3 解答: 英和辞書プログラム
# ===================================

# --- 英和辞書を辞書で定義する ---
dictionary = {
    "apple": "りんご",
    "dog": "犬",
    "cat": "猫",
    "book": "本",
    "water": "水",
}

# --- タイトルを表示する ---
print("=== 英和辞書 ===")

# --- 検索ループ ---
# quitが入力されるまで繰り返す
while True:
    # ユーザーに英単語を入力してもらう
    word = input("英単語を入力（quitで終了）: ")

    # quitが入力されたら終了する
    if word == "quit":
        print("終了します。")
        # ループを抜ける
        break

    # 辞書にキーが存在するかチェックする
    if word in dictionary:
        # 辞書にある場合は日本語訳を表示する
        print(f"  {word} → {dictionary[word]}")
    else:
        # 辞書にない場合はメッセージを表示する
        print(f"  登録されていません: {word}")
```

---

### 標準課題4 解答

```python
# ===================================
# 標準課題4 解答: 成績集計（辞書で管理）
# ===================================

# --- 成績データを辞書で定義する ---
grades = {"田中": 85, "鈴木": 92, "佐藤": 78}

# --- 全員の成績を表示する ---
print("=== 成績一覧 ===")
for name, score in grades.items():
    # 各学生の名前と点数を表示する
    print(f"  {name}: {score}点")

# --- 平均点を計算する ---
# 合計を0で初期化する
total = 0
# 全点数を足す
for score in grades.values():
    total = total + score

# 人数はキーの数
count = len(grades)
# 平均を計算する
average = total / count
# 結果を表示する
print(f"平均点: {average}点")

# --- 最高得点者を探す ---
# 最高点と名前を初期化する
best_name = ""
best_score = 0

# 全員をループで比較する
for name, score in grades.items():
    # 現在の最高点より高い場合は更新する
    if score > best_score:
        best_score = score
        best_name = name

# 結果を表示する
print(f"最高得点者: {best_name}（{best_score}点）")
```

---

### 標準課題5 解答

```python
# ===================================
# 標準課題5 解答: リストの重複を排除する
# ===================================

# --- 元のリスト ---
original = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print("=== 重複排除（順序保持） ===")

# --- すでに見た要素を記録するセット ---
seen = set()

# --- 結果を格納する新しいリスト ---
result = []

# --- 各要素を1つずつ処理する ---
for num in original:
    # すでに見たことがあるかチェックする
    if num in seen:
        # すでに見た要素 → スキップ
        print(f"  {num} → 既出、スキップ")
    else:
        # 初めて見た要素 → 結果に追加し、seenにも追加する
        result.append(num)
        seen.add(num)
        print(f"  {num} → 初出現、追加")

# --- 結果を表示する ---
print(f"結果: {result}")
```

---

### 標準課題6 解答

```python
# ===================================
# 標準課題6 解答: 2つのリストの共通要素
# ===================================

# --- 2つのリスト ---
list_a = [1, 3, 5, 7, 9, 11, 13]
list_b = [2, 3, 5, 7, 11, 15]
# リストの内容を表示する
print(f"リストA: {list_a}")
print(f"リストB: {list_b}")

# --- セットに変換する ---
set_a = set(list_a)
set_b = set(list_b)

# --- 共通要素を求める（交差） ---
common = set_a & set_b
# ソートしてリストに変換する
common_sorted = sorted(common)
print(f"共通要素: {common_sorted}")

# --- Aだけにある要素を求める（差集合） ---
only_a = set_a - set_b
only_a_sorted = sorted(only_a)
print(f"Aだけの要素: {only_a_sorted}")

# --- Bだけにある要素を求める（差集合） ---
only_b = set_b - set_a
only_b_sorted = sorted(only_b)
print(f"Bだけの要素: {only_b_sorted}")
```

---

### 標準課題7 解答

```python
# ===================================
# 標準課題7 解答: 単語の出現頻度ランキング
# ===================================

# --- 対象テキスト ---
text = "the cat sat on the mat the cat ate the rat on the mat"
print("=== 単語の出現頻度 ===")
print(f"テキスト: {text}")

# --- 単語に分割する ---
# split()はスペースで文字列を分割する
words = text.split()
print(f"単語数: {len(words)}")

# --- 各単語の出現回数を辞書で数える ---
word_count = {}

for word in words:
    # すでに辞書にあるかチェックする
    if word in word_count:
        # あれば+1する
        word_count[word] = word_count[word] + 1
    else:
        # なければ1で初期化する
        word_count[word] = 1

# --- 出現回数の多い順にソートする ---
# items()でキーと値のペアを取得し、値（出現回数）でソートする
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

# --- ランキング表示 ---
print()
print("出現頻度ランキング:")
for rank, (word, count) in enumerate(sorted_words, start=1):
    # 順位と単語と出現回数を表示する
    print(f"  {rank}位: {word} - {count}回")
```

---

### 標準課題8 解答

```python
# ===================================
# 標準課題8 解答: 名前リストのソートと検索
# ===================================

# --- データ定義 ---
people = [("田中", 25), ("鈴木", 32), ("佐藤", 19), ("山田", 28), ("高橋", 22)]

# --- 年齢の昇順でソート ---
print("=== 年齢順 ===")
# key=lambda x: x[1] でタプルの2番目（年齢）でソートする
by_age = sorted(people, key=lambda x: x[1])
for name, age in by_age:
    # 各人の名前と年齢を表示する
    print(f"  {name}: {age}歳")

# --- 25歳以上を抽出 ---
print()
print("=== 25歳以上 ===")
for name, age in people:
    # 25歳以上かチェックする
    if age >= 25:
        print(f"  {name}: {age}歳")

# --- 最年長と最年少を探す ---
# 最初の要素で初期化する
oldest_name, oldest_age = people[0]
youngest_name, youngest_age = people[0]

# 全員をループで比較する
for name, age in people:
    # 最年長の更新チェック
    if age > oldest_age:
        oldest_name = name
        oldest_age = age
    # 最年少の更新チェック
    if age < youngest_age:
        youngest_name = name
        youngest_age = age

# 結果を表示する
print()
print(f"最年長: {oldest_name}（{oldest_age}歳）")
print(f"最年少: {youngest_name}（{youngest_age}歳）")
```

---

### 標準課題9 解答

```python
# ===================================
# 標準課題9 解答: 買い物リストのCSV保存と読込
# ===================================

# --- 買い物データ ---
shopping_data = [
    ("りんご", 3),
    ("牛乳", 1),
    ("パン", 2),
    ("卵", 1),
    ("バター", 1),
]

# --- ファイル名 ---
filename = "shopping.csv"

# ========================================
# 保存処理
# ========================================
print("=== 保存 ===")

# ファイルを書き込みモードで開く
with open(filename, "w", encoding="utf-8") as f:
    # ヘッダー行を書き込む
    f.write("商品名,個数\n")

    # 各商品を1行ずつ書き込む
    for item, quantity in shopping_data:
        # カンマ区切りの行を作る
        line = f"{item},{quantity}\n"
        # ファイルに書き込む
        f.write(line)
        # 途中経過を表示する
        print(f"  {item},{quantity} を書き込み")

print(f"保存完了: {filename}")

# ========================================
# 読み込み処理
# ========================================
print()
print("=== 読み込み ===")

# 読み込んだデータを格納するリスト
loaded_data = []

try:
    # ファイルを読み込みモードで開く
    with open(filename, "r", encoding="utf-8") as f:
        # 全行を読み込む
        lines = f.readlines()

        for i, line in enumerate(lines):
            # ヘッダー行はスキップする
            if i == 0:
                continue

            # 行末の改行を除去してカンマで分割する
            parts = line.strip().split(",")
            # 商品名と個数を取り出す
            item = parts[0]
            quantity = int(parts[1])
            # リストに追加する
            loaded_data.append((item, quantity))
            # 読み込み結果を表示する
            print(f"  {item}: {quantity}個")

except FileNotFoundError:
    # ファイルが存在しない場合
    print("  ファイルが見つかりません。")

# --- 合計を計算する ---
total_items = len(loaded_data)
total_quantity = 0
for item, quantity in loaded_data:
    total_quantity = total_quantity + quantity

# 合計を表示する
print(f"合計: {total_items}品目、{total_quantity}個")
```

---

### 標準課題10 解答

```python
# ===================================
# 標準課題10 解答: 成績管理システム（CSV完全版）
# ===================================

# --- ファイル名 ---
filename = "grades.csv"

# ========================================
# 1. CSVファイルにデータを書き込む
# ========================================

# テストデータ
test_data = [
    ("田中", "数学", 85),
    ("田中", "英語", 72),
    ("鈴木", "数学", 92),
    ("鈴木", "英語", 88),
    ("佐藤", "数学", 78),
    ("佐藤", "英語", 95),
]

# ファイルに書き込む
with open(filename, "w", encoding="utf-8") as f:
    # ヘッダーを書き込む
    f.write("名前,科目,点数\n")
    # データを1行ずつ書き込む
    for name, subject, score in test_data:
        f.write(f"{name},{subject},{score}\n")

print(f"データ書き込み完了: {filename}")

# ========================================
# 2. CSVファイルからデータを読み込む
# ========================================
print()
print("=== 成績データ読み込み ===")

# 読み込んだデータを格納するリスト
records = []

with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

    for i, line in enumerate(lines):
        # ヘッダー行はスキップする
        if i == 0:
            continue

        # カンマで分割する
        parts = line.strip().split(",")
        name = parts[0]
        subject = parts[1]
        score = int(parts[2])
        # リストに追加する
        records.append((name, subject, score))
        # 読み込み結果を表示する
        print(f"  {name} - {subject}: {score}点")

# ========================================
# 3. 学生ごとの平均点を計算する
# ========================================
print()
print("=== 学生別 平均点 ===")

# 学生ごとの点数を辞書で集計する
# キー: 学生名, 値: 点数のリスト
student_scores = {}

for name, subject, score in records:
    # すでに辞書にあるかチェックする
    if name in student_scores:
        # あれば点数リストに追加する
        student_scores[name].append(score)
    else:
        # なければ新しいリストで初期化する
        student_scores[name] = [score]

# 各学生の平均点を計算して表示する
for name, scores in student_scores.items():
    # 合計を計算する
    total = 0
    for s in scores:
        total = total + s
    # 平均を計算する
    average = total / len(scores)
    # 結果を表示する
    print(f"  {name}: {average}点")

# ========================================
# 4. 科目ごとの平均点を計算する
# ========================================
print()
print("=== 科目別 平均点 ===")

# 科目ごとの点数を辞書で集計する
subject_scores = {}

for name, subject, score in records:
    if subject in subject_scores:
        subject_scores[subject].append(score)
    else:
        subject_scores[subject] = [score]

# 各科目の平均点を計算して表示する
for subject, scores in subject_scores.items():
    total = 0
    for s in scores:
        total = total + s
    average = total / len(scores)
    print(f"  {subject}: {average}点")
```

---

### 発展課題1 解答

```python
# ===================================
# 発展課題1 解答: アナグラム判定（3つのアプローチ）
# ===================================

# Counterを使うためにインポートする
from collections import Counter


# ========================================
# 共通の前処理関数
# ========================================

def clean_word(word):
    """文字列を前処理する関数（小文字化 + スペース除去）"""
    # 小文字に変換する
    lower_word = word.lower()
    # スペースを除去する
    cleaned = lower_word.replace(" ", "")
    # 途中経過を表示する
    print(f"    前処理: '{word}' → '{cleaned}'")
    return cleaned


# ========================================
# アプローチ1: ソートして比較
# ========================================

def is_anagram_sort(word1, word2):
    """ソートして比較するアナグラム判定"""
    # 前処理する
    clean1 = clean_word(word1)
    clean2 = clean_word(word2)
    # 文字をアルファベット順に並べ替える
    sorted1 = sorted(clean1)
    sorted2 = sorted(clean2)
    # ソート結果が同じならアナグラム
    return sorted1 == sorted2


# ========================================
# アプローチ2: 辞書で文字を数える
# ========================================

def count_chars(word):
    """各文字の出現回数を辞書で返す関数"""
    # 空の辞書を作る
    char_count = {}
    # 1文字ずつ処理する
    for char in word:
        if char in char_count:
            # すでにあれば+1
            char_count[char] = char_count[char] + 1
        else:
            # なければ1で初期化
            char_count[char] = 1
    return char_count


def is_anagram_dict(word1, word2):
    """辞書で文字数を比較するアナグラム判定"""
    # 前処理する
    clean1 = clean_word(word1)
    clean2 = clean_word(word2)
    # 各文字の出現回数を辞書で数える
    count1 = count_chars(clean1)
    count2 = count_chars(clean2)
    # 辞書が同じならアナグラム
    return count1 == count2


# ========================================
# アプローチ3: Counterを使う
# ========================================

def is_anagram_counter(word1, word2):
    """Counterで文字数を比較するアナグラム判定"""
    # 前処理する
    clean1 = clean_word(word1)
    clean2 = clean_word(word2)
    # Counterで各文字の出現回数を自動で数える
    counter1 = Counter(clean1)
    counter2 = Counter(clean2)
    # Counterオブジェクト同士を比較する
    return counter1 == counter2


# ========================================
# テスト実行
# ========================================

# テストケースをリストで定義する
test_cases = [
    ("listen", "silent", True),
    ("hello", "world", False),
    ("Astronomer", "Moon starer", True),
    ("aabb", "abab", True),
    ("abc", "abcd", False),
]

# 全テストケースを実行する
for word1, word2, expected in test_cases:
    print(f"\n--- テスト: '{word1}' vs '{word2}' (期待: {expected}) ---")
    # 3つの方法でそれぞれ判定する
    result_sort = is_anagram_sort(word1, word2)
    result_dict = is_anagram_dict(word1, word2)
    result_counter = is_anagram_counter(word1, word2)

    # 結果を表示する
    print(f"  ソート法:  {result_sort}")
    print(f"  辞書法:   {result_dict}")
    print(f"  Counter法: {result_counter}")

    # 全ての方法が期待結果と一致するかチェックする
    all_correct = (
        result_sort == expected
        and result_dict == expected
        and result_counter == expected
    )
    status = "OK" if all_correct else "NG"
    print(f"  判定: {status}")
```

---

### 発展課題2 解答

```python
# ===================================
# 発展課題2 解答: 数当てゲームのランキング（CSV保存付き）
# ===================================

import random


# ========================================
# ファイル入出力
# ========================================

def load_ranking(filename="ranking.csv"):
    """CSVファイルからランキングを読み込む関数"""
    # 空のリストを準備する
    ranking = []

    try:
        # ファイルを読み込みモードで開く
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                # ヘッダー行はスキップする
                if i == 0:
                    continue

                # カンマで分割する
                parts = line.strip().split(",")
                if len(parts) == 2:
                    name = parts[0]
                    score = int(parts[1])
                    ranking.append((name, score))

        print(f"ランキング読み込み完了（{len(ranking)}件）")

    except FileNotFoundError:
        # ファイルがない場合
        print("ランキングファイルが見つかりません。新規作成します。")

    return ranking


def save_ranking(ranking, filename="ranking.csv"):
    """ランキングをCSVファイルに保存する関数"""
    # 試行回数の少ない順にソートする
    sorted_ranking = sorted(ranking, key=lambda x: x[1])

    # ファイルに書き込む
    with open(filename, "w", encoding="utf-8") as f:
        # ヘッダーを書き込む
        f.write("名前,回数\n")
        # データを書き込む
        for name, score in sorted_ranking:
            f.write(f"{name},{score}\n")

    print(f"ランキング保存完了（{len(ranking)}件）→ {filename}")


# ========================================
# ランキング表示
# ========================================

def display_ranking(ranking):
    """ランキングを表示する関数"""
    if len(ranking) == 0:
        print("  まだランキングはありません。")
        return

    # ソートする
    sorted_ranking = sorted(ranking, key=lambda x: x[1])

    print("=== ランキング TOP 5 ===")
    for i, (name, score) in enumerate(sorted_ranking[:5], start=1):
        print(f"  {i}位: {name} - {score}回")


# ========================================
# 難易度選択
# ========================================

def choose_level():
    """難易度を選択する関数"""
    levels = {
        "1": ("かんたん", 1, 10, 5),
        "2": ("ふつう", 1, 50, 7),
        "3": ("むずかしい", 1, 100, 10),
    }

    print("★ 難易度を選んでください ★")
    for key, (label, lo, hi, tries) in levels.items():
        print(f"  {key}: {label}（{lo}〜{hi}, 最大{tries}回）")

    while True:
        choice = input("番号を入力 → ")
        if choice in levels:
            return levels[choice]
        print("1〜3の番号で選んでください。")


# ========================================
# ゲーム本体
# ========================================

def play_game():
    """数当てゲームを1回プレイして試行回数を返す関数"""
    # 難易度を選択する
    label, lo, hi, max_tries = choose_level()

    # 正解をランダムに決める
    answer = random.randint(lo, hi)

    # 入力履歴
    history = []

    print(f"\n『{label}』モード開始！ 答えは {lo}〜{hi} のどれかです。")

    # メインループ
    for remaining in range(max_tries, 0, -1):
        # 安全な入力処理
        while True:
            try:
                guess = int(input(f"予想を入力（残り{remaining}回）→ "))
                if lo <= guess <= hi:
                    break
                print(f"  {lo}〜{hi}の範囲で入力してください。")
            except ValueError:
                print("  数字を入力してください。")

        # 履歴に追加する
        history.append(guess)

        # 比較する
        if guess == answer:
            print(f"正解！ {len(history)}回目で当たりました！")
            print(f"入力履歴: {history}")
            return len(history)
        elif guess < answer:
            print("もっと大きい数です。")
        else:
            print("もっと小さい数です。")
    else:
        print(f"\nゲームオーバー！ 正解は {answer} でした。")
        print(f"入力履歴: {history}")
        return max_tries + 1


# ========================================
# メイン処理
# ========================================

print("=" * 40)
print("  数当てゲーム（ランキング + CSV保存版）")
print("=" * 40)
print()

# ランキングを読み込む
ranking = load_ranking("ranking.csv")
print()
display_ranking(ranking)
print()

# ゲームループ
while True:
    # ゲームをプレイする
    score = play_game()

    # プレイヤー名を入力する
    print()
    player_name = input("名前を入力してください: ")

    # ランキングに追加する（不変操作）
    new_entry = (player_name, score)
    ranking = ranking + [new_entry]
    print(f"  '{player_name}' さん（{score}回）をランキングに追加しました！")

    # ランキングを表示する
    print()
    display_ranking(ranking)

    # CSVに保存する
    print()
    save_ranking(ranking, "ranking.csv")

    # リトライ確認
    print()
    again = input("もう一度遊びますか？ (y/n) → ").strip().lower()
    if again != "y":
        print("遊んでくれてありがとう！")
        break
    print()
```
