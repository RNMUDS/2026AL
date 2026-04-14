# 第6回: ハッシュ法（1）

## 説明

### ハッシュとは何か？

大学のロッカーを想像してください。

- ロッカーには **番号** がついている（0, 1, 2, ..., 99）
- 名前からロッカー番号を計算する **ルール** がある
- 番号がわかれば、**一発で** そのロッカーを開けられる（O(1)）

これがハッシュの基本です。

| 操作 | 線形探索 | ハッシュ |
|------|----------|----------|
| データを探す | 先頭から1つずつ調べる | 番号を計算して直接アクセス |
| 計算量 | O(n) | O(1)（理想的な場合） |
| 例え | 本棚を端から探す | ロッカー番号で直接開ける |

### ハッシュ関数の3つの性質

1. **決定性**: 同じ入力 → 必ず同じ出力
2. **一様分布**: 出力がまんべんなく散らばる
3. **高速**: 計算が速い

### 単純ハッシュと多項式ハッシュ

**単純ハッシュ**: 各文字の ord 値を合計し、テーブルサイズで割った余り
```
hash("apple") = (ord('a') + ord('p') + ord('p') + ord('l') + ord('e')) % テーブルサイズ
```
問題点: 文字の**順番を考慮しない**ので、アナグラム（"apple" と "pleap"）が同じ値になる。

**多項式ハッシュ**: 基数の累乗をかけて位置情報を反映させる
```
h = 0
h = h * 31 + ord(c₀)
h = h * 31 + ord(c₁)
...
```
利点: 文字の順番も考慮するので、アナグラムでも異なる値になる。

---

## 例題と課題

### 例題1: ord() 関数で文字を数値にする

```python
# ============================================================
# 例題1: ord() 関数で文字を数値に変換する
# ============================================================

# --- アルファベットの ord 値 ---
print("=== アルファベット ===")  # セクション見出しを表示する
print(f"'A' → {ord('A')}")  # Aの数値（65）を表示する
print(f"'B' → {ord('B')}")  # Bの数値（66）を表示する
print(f"'Z' → {ord('Z')}")  # Zの数値（90）を表示する
print(f"'a' → {ord('a')}")  # aの数値（97）を表示する
print(f"'z' → {ord('z')}")  # zの数値（122）を表示する

# --- 日本語の ord 値 ---
print("\n=== 日本語 ===")  # セクション見出しを表示する
print(f"'あ' → {ord('あ')}")  # あの数値（12354）を表示する
print(f"'い' → {ord('い')}")  # いの数値（12356）を表示する
print(f"'中' → {ord('中')}")  # 漢字の数値を表示する

# --- 逆変換: chr() ---
print("\n=== chr() で数値から文字に戻す ===")  # セクション見出しを表示する
print(f"chr(65)    = '{chr(65)}'")  # 65をAに戻す
print(f"chr(97)    = '{chr(97)}'")  # 97をaに戻す
print(f"chr(12354) = '{chr(12354)}'")  # 12354をあに戻す

# --- 文字列の各文字を数値に変換する ---
name = "Python"  # 変換したい文字列
print(f"\n=== '{name}' の各文字のord値 ===")  # セクション見出しを表示する
total = 0  # ord値の合計を初期化する
for i, char in enumerate(name):  # 各文字を位置番号付きで処理する
    code = ord(char)  # 文字を数値に変換する
    total += code  # 合計に加算する
    print(f"  位置{i}: '{char}' → {code}  (累計: {total})")  # 各ステップを表示する
print(f"合計: {total}")  # 最終的な合計を表示する
```

---

#### 標準課題1（超やさしい）

文字 `'A'`, `'Z'`, `'a'`, `'z'`, `'0'`, `'9'` の ord 値をそれぞれ表示するプログラムを作成してください。さらに、`chr()` を使って ord 値 `72`, `101`, `108` がどの文字になるか表示してください。

---

#### 標準課題2（超やさしい）

自分の名前（ローマ字）の各文字を `ord()` で数値に変換し、すべての ord 値の合計を計算するプログラムを作成してください。「累計」を各ステップで表示してください。（例: "Tanaka" の各文字の ord 値と合計）

---

### 例題2: 単純ハッシュ関数

```python
# ============================================================
# 例題2: 単純ハッシュ関数の実装
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数の定義
    """各文字のord値を合計し、テーブルサイズで割った余りを返す"""
    total = 0  # ord値の合計を初期化する
    for char in key:  # 文字列の各文字を処理する
        code = ord(char)  # 文字を数値に変換する
        total += code  # 合計に加算する
    hash_value = total % table_size  # テーブルサイズで割った余りを計算する
    return hash_value  # ハッシュ値を返す

# --- テスト ---
table_size = 10  # テーブルサイズを10に設定する
test_words = ["apple", "banana", "cherry", "date", "elderberry"]  # テスト用の単語リスト

print(f"テーブルサイズ: {table_size}")  # テーブルサイズを表示する
print("-" * 40)  # 区切り線を表示する
for word in test_words:  # 各単語についてハッシュ値を計算する
    h = simple_hash(word, table_size)  # ハッシュ関数を呼び出す
    print(f"  simple_hash('{word}', {table_size}) = {h}")  # 結果を表示する

# --- アナグラムの問題点 ---
print(f"\n=== アナグラムの問題 ===")  # セクション見出し
word1 = "apple"  # 元の単語
word2 = "pleap"  # アナグラム（同じ文字の並び替え）
h1 = simple_hash(word1, table_size)  # appleのハッシュ値を計算する
h2 = simple_hash(word2, table_size)  # pleapのハッシュ値を計算する
print(f"  simple_hash('{word1}') = {h1}")  # 結果を表示する
print(f"  simple_hash('{word2}') = {h2}")  # 結果を表示する
print(f"  → 同じ値になる! 文字の順番を区別できない")  # 問題点を説明する
```

---

#### 標準課題3（やさしい）

`simple_hash` 関数を自分で実装し、テーブルサイズ10で "apple", "banana", "cherry", "dog", "elephant" のハッシュ値を計算するプログラムを作成してください。各文字の ord 値の計算過程も print で表示してください。

---

#### 標準課題4（やさしい）

テーブルサイズを 5, 10, 20, 50 と変えて、10個の単語 `["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]` のハッシュ値がどう分布するか観察するプログラムを作成してください。各テーブルサイズで、どのスロットに何個の単語が割り当てられたかを表示してください。

---

### 例題3: 多項式ハッシュ関数

```python
# ============================================================
# 例題3: 多項式ハッシュ関数の実装（ステップ表示付き）
# ============================================================

def polynomial_hash_trace(key):  # トレース付き多項式ハッシュ
    """多項式ハッシュを1ステップずつ表示する"""
    base = 31  # 基数を31に設定する
    mask = 0xFFFFFFFF  # 32ビットマスク（2^32 - 1）

    h = 0  # ハッシュ値を0で初期化する
    print(f"'{key}' の多項式ハッシュ計算（base={base}）")  # タイトルを表示する
    print(f"{'Step':<5} {'文字':<5} {'ord':<6} {'計算式':<30} {'結果':<12}")  # ヘッダー行
    print("-" * 65)  # 区切り線

    for step, char in enumerate(key, 1):  # 各文字をステップ番号付きで処理する
        prev = h  # 計算前のハッシュ値を保存する
        code = ord(char)  # 文字を数値に変換する
        calculated = prev * base + code  # 多項式ハッシュの計算を行う
        h = calculated & mask  # 32ビットで折りたたむ

        formula = f"{prev} * {base} + {code} = {calculated}"  # 計算式の文字列を作る
        print(f"{step:<5} {char:<5} {code:<6} {formula:<30} {h:<12}")  # ステップを表示する

    print("-" * 65)  # 区切り線
    print(f"最終ハッシュ値: {h} (0x{h:08X})")  # 最終結果を表示する
    return h  # ハッシュ値を返す

# --- テスト ---
polynomial_hash_trace("apple")  # appleのトレースを表示する
print()  # 空行
polynomial_hash_trace("pleap")  # pleapのトレースを表示する

# --- 結果比較 ---
print("\n=== アナグラム比較 ===")  # セクション見出し
h1 = polynomial_hash_trace("apple")  # appleのハッシュ値
print()  # 空行
h2 = polynomial_hash_trace("pleap")  # pleapのハッシュ値
print(f"\napple={h1}, pleap={h2}")  # 両方を表示する
print(f"→ 多項式ハッシュでは異なる値になる!")  # 結果を説明する
```

---

#### 標準課題5（やややさしい）

多項式ハッシュ関数 `polynomial_hash(key)` を実装してください（base=31, mask=0xFFFFFFFF）。"apple", "pleap", "Python", "Nakamura" の4つの文字列のハッシュ値を計算し、10進数と16進数の両方で表示してください。

---

#### 標準課題6（やややさしい）

"Nakamura" の多項式ハッシュ計算を1ステップずつトレースするプログラムを作成してください。各ステップで「文字」「ord値」「計算前のh」「計算式」「折りたたみ後のh」を表形式で表示してください。（例題3を参考に自分で実装してください）

---

### 例題4: 自分の名前でハッシュ値を計算する

```python
# ============================================================
# 例題4: 複数の名前でハッシュ値を計算・比較する
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ: 各文字のord値の合計 mod テーブルサイズ"""
    total = 0  # 合計値を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ: h = (h * base + ord(c)) & mask"""
    h = 0  # ハッシュ値を初期化する
    for char in key:  # 各文字を処理する
        h = (h * base + ord(char)) & mask  # 多項式計算を行う
    return h  # ハッシュ値を返す

# --- 日本の名字トップ15でハッシュ値を比較 ---
names = [  # 日本の名字トップ15のリスト
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe",
    "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato",
    "Yoshida", "Yamada", "Sasaki", "Yamaguchi", "Matsumoto",
]
table_size = 10  # テーブルサイズを10に設定する

print(f"日本の名字 top15 のハッシュ値分布（テーブルサイズ={table_size}）")  # タイトル
print(f"{'名前':<14} {'単純ハッシュ':<12} {'多項式(mod10)':<14}")  # ヘッダー行
print("-" * 45)  # 区切り線

for name in names:  # 各名前についてハッシュ値を計算する
    s_hash = simple_hash(name, table_size)  # 単純ハッシュ値
    p_hash = polynomial_hash(name) % table_size  # 多項式ハッシュ値
    print(f"{name:<14} {s_hash:<12} {p_hash:<14}")  # 結果を表示する

# --- アナグラムでの衝突テスト ---
print(f"\n=== アナグラム衝突テスト ===")  # セクション見出し
name1 = "Tanaka"  # 元の名前
name2 = "anaTak"  # アナグラム
s1 = simple_hash(name1, table_size)  # 単純ハッシュ（元）
s2 = simple_hash(name2, table_size)  # 単純ハッシュ（アナグラム）
p1 = polynomial_hash(name1)  # 多項式ハッシュ（元）
p2 = polynomial_hash(name2)  # 多項式ハッシュ（アナグラム）
print(f"'{name1}': 単純={s1}, 多項式={p1}")  # 結果を表示する
print(f"'{name2}': 単純={s2}, 多項式={p2}")  # 結果を表示する
print(f"単純ハッシュ: {'衝突!' if s1 == s2 else '異なる'}")  # 衝突判定
print(f"多項式ハッシュ: {'衝突!' if p1 == p2 else '異なる'}")  # 衝突判定
```

---

#### 標準課題7（やや普通）

10個の異なる英単語を用意し、テーブルサイズ10の単純ハッシュと多項式ハッシュ（mod 10）のハッシュ値をそれぞれ計算して表示するプログラムを作成してください。どちらのハッシュ関数がより均等に分布しているか、スロットごとの単語数を数えて比較してください。

---

#### 標準課題8（やや普通）

"abc", "bca", "cab", "acb", "bac", "cba" の6つの文字列（すべて同じ文字のアナグラム）について、単純ハッシュと多項式ハッシュの値をそれぞれ計算するプログラムを作成してください。単純ハッシュではすべて同じ値になり、多項式ハッシュでは異なる値になることを確認してください。

---

### 例題5: 衝突の検出

```python
# ============================================================
# 例題5: ハッシュ値の衝突を検出する
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

# --- 多数の単語でハッシュ値を計算し、衝突を検出する ---
words = [  # テスト用の単語リスト
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
]
table_size = 10  # テーブルサイズを10に設定する

print(f"テーブルサイズ: {table_size}, 単語数: {len(words)}")  # テスト条件を表示する
print("-" * 50)  # 区切り線

# --- 各スロットに割り当てられた単語を記録する ---
slots = {}  # スロット番号→単語リストの辞書
for word in words:  # 各単語についてハッシュ値を計算する
    h = simple_hash(word, table_size)  # ハッシュ値を計算する
    if h not in slots:  # スロットが初出の場合
        slots[h] = []  # 空リストで初期化する
    slots[h].append(word)  # 単語をスロットに追加する

# --- 結果を表示する ---
collision_count = 0  # 衝突が起きたスロット数
for slot_num in sorted(slots.keys()):  # スロット番号順に表示する
    words_in_slot = slots[slot_num]  # そのスロットの単語リスト
    count = len(words_in_slot)  # 単語数
    marker = " ← 衝突!" if count > 1 else ""  # 衝突マーク
    if count > 1:  # 衝突している場合
        collision_count += 1  # 衝突スロット数を増やす
    print(f"  スロット{slot_num}: {words_in_slot}{marker}")  # 結果を表示する

print(f"\n衝突が起きたスロット: {collision_count}個")  # 衝突数を表示する
print(f"使用中のスロット: {len(slots)}/{table_size}")  # 使用率を表示する
```

---

#### 標準課題9（普通）

20個以上の英単語を用意し、テーブルサイズ 7, 10, 13, 20 のそれぞれで単純ハッシュの衝突数を数えるプログラムを作成してください。テーブルサイズが素数（7, 13）と非素数（10, 20）で衝突の起きやすさに違いがあるか分析してください。

---

#### 標準課題10（普通）

20個の英単語について、テーブルサイズ10の単純ハッシュと多項式ハッシュ（mod 10）の分布を比較するプログラムを作成してください。各スロットの単語数をヒストグラム（テキストの棒グラフ）で表示し、分布の偏りを標準偏差で数値化してください。どちらのハッシュ関数がより均等に分布しているか結論を出してください。

---

## 発展課題

### 発展課題1: ハッシュ分布の可視化

matplotlib を使って、単純ハッシュと多項式ハッシュの分布を棒グラフで比較してください。

**仕様:**
1. 50個以上の英単語を用意する
2. テーブルサイズ20で、単純ハッシュと多項式ハッシュのハッシュ値を計算する
3. 2つのグラフを横に並べて表示する（左: 単純ハッシュ、右: 多項式ハッシュ）
4. 各グラフのX軸はスロット番号、Y軸はそのスロットに割り当てられた単語数
5. 理想的な均等分布の線（平均値）も重ねて描画する

---

### 発展課題2: オリジナルハッシュ関数の設計

単純ハッシュと多項式ハッシュの欠点を改良した、独自のハッシュ関数を設計・実装してください。

**仕様:**
1. 自分のハッシュ関数を設計し、なぜその計算方法を選んだか説明する
2. 単純ハッシュ、多項式ハッシュ、自作ハッシュの3つについて同じ単語リストでハッシュ値を計算する
3. 各ハッシュ関数の衝突数を比較して表示する
4. どのハッシュ関数が最も均等に分布しているか分析する

---

## 解答例

### 標準課題1 解答

```python
# ============================================================
# 標準課題1 解答: ord() と chr() の基本
# ============================================================

# --- 各文字の ord 値を表示する ---
chars = ['A', 'Z', 'a', 'z', '0', '9']  # 調べたい文字のリスト
print("=== 各文字の ord 値 ===")  # セクション見出し
for char in chars:  # 各文字について
    print(f"  '{char}' → {ord(char)}")  # ord値を表示する

# --- chr() で数値から文字に変換する ---
codes = [72, 101, 108]  # 変換したい数値のリスト
print("\n=== chr() で文字に戻す ===")  # セクション見出し
for code in codes:  # 各数値について
    print(f"  chr({code}) = '{chr(code)}'")  # 文字に戻して表示する
```

---

### 標準課題2 解答

```python
# ============================================================
# 標準課題2 解答: 名前の各文字のord値と合計
# ============================================================

name = "Tanaka"  # 自分の名前（ローマ字）
print(f"名前: '{name}'")  # 名前を表示する
print("-" * 35)  # 区切り線

total = 0  # 合計を初期化する
for i, char in enumerate(name):  # 各文字を位置番号付きで処理する
    code = ord(char)  # 文字を数値に変換する
    total += code  # 合計に加算する
    print(f"  位置{i}: '{char}' → ord={code}  (累計: {total})")  # ステップを表示する

print("-" * 35)  # 区切り線
print(f"ord値の合計: {total}")  # 最終合計を表示する
```

---

### 標準課題3 解答

```python
# ============================================================
# 標準課題3 解答: simple_hash関数の実装（計算過程付き）
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """各文字のord値を合計し、テーブルサイズで割った余りを返す"""
    total = 0  # 合計を初期化する
    print(f"  '{key}' の計算:")  # どの文字列を計算しているか表示する

    for i, char in enumerate(key):  # 各文字を位置番号付きで処理する
        code = ord(char)  # 文字を数値に変換する
        total += code  # 合計に加算する
        print(f"    [{i}] '{char}' → ord={code}, 累計={total}")  # 各ステップを表示する

    hash_value = total % table_size  # テーブルサイズで割った余りを計算する
    print(f"    合計{total} % {table_size} = {hash_value}")  # 最終計算を表示する
    return hash_value  # ハッシュ値を返す

# --- テスト ---
table_size = 10  # テーブルサイズ
words = ["apple", "banana", "cherry", "dog", "elephant"]  # テスト用単語

for word in words:  # 各単語についてテストする
    result = simple_hash(word, table_size)  # ハッシュ値を計算する
    print(f"  → simple_hash('{word}', {table_size}) = {result}")  # 結果を表示する
    print()  # 空行で見やすくする
```

---

### 標準課題4 解答

```python
# ============================================================
# 標準課題4 解答: テーブルサイズを変えて分布を観察する
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

words = ["apple", "banana", "cherry", "date", "elderberry",  # テスト用の10単語
         "fig", "grape", "honeydew", "kiwi", "lemon"]

for table_size in [5, 10, 20, 50]:  # 各テーブルサイズでテストする
    print(f"\n=== テーブルサイズ: {table_size} ===")  # テーブルサイズを表示する
    slots = {}  # スロット→単語リストの辞書
    for word in words:  # 各単語のハッシュ値を計算する
        h = simple_hash(word, table_size)  # ハッシュ値を計算する
        if h not in slots:  # スロットが初出の場合
            slots[h] = []  # 空リストで初期化する
        slots[h].append(word)  # 単語を追加する

    for slot_num in sorted(slots.keys()):  # スロット番号順に表示する
        count = len(slots[slot_num])  # 単語数を取得する
        marker = " ← 衝突" if count > 1 else ""  # 衝突マーク
        print(f"  スロット{slot_num:>2}: ({count}個) {slots[slot_num]}{marker}")  # 表示する

    collision_slots = sum(1 for v in slots.values() if len(v) > 1)  # 衝突スロット数
    print(f"  衝突スロット数: {collision_slots}")  # 衝突数を表示する
```

---

### 標準課題5 解答

```python
# ============================================================
# 標準課題5 解答: 多項式ハッシュ関数の実装
# ============================================================

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ: h = (h * base + ord(c)) & mask"""
    h = 0  # ハッシュ値を初期化する
    for char in key:  # 各文字を処理する
        h = (h * base + ord(char)) & mask  # 多項式計算を行う
    return h  # ハッシュ値を返す

# --- テスト ---
words = ["apple", "pleap", "Python", "Nakamura"]  # テスト用の文字列
print("=== 多項式ハッシュ関数のテスト ===")  # セクション見出し
print(f"{'文字列':<12} {'10進数':<15} {'16進数'}")  # ヘッダー行
print("-" * 40)  # 区切り線

for word in words:  # 各文字列のハッシュ値を計算する
    h = polynomial_hash(word)  # ハッシュ値を計算する
    print(f"{word:<12} {h:<15} 0x{h:08X}")  # 10進数と16進数で表示する
```

---

### 標準課題6 解答

```python
# ============================================================
# 標準課題6 解答: "Nakamura"の多項式ハッシュをトレースする
# ============================================================

target_string = "Nakamura"  # トレースする文字列
base = 31  # 基数
mask = 0xFFFFFFFF  # 32ビットマスク

h = 0  # ハッシュ値を初期化する
print(f"'{target_string}' の多項式ハッシュ計算トレース")  # タイトル
print(f"{'Step':<5} {'文字':<5} {'ord':<6} {'計算前h':<12} {'計算式':<28} {'結果':<12} {'16進'}")  # ヘッダー
print("-" * 85)  # 区切り線

for step, char in enumerate(target_string, 1):  # 各文字をステップ番号付きで処理する
    prev = h  # 計算前のハッシュ値を保存する
    code = ord(char)  # 文字を数値に変換する
    calculated = prev * base + code  # 多項式計算
    h = calculated & mask  # 32ビットで折りたたむ

    formula = f"{prev}*{base}+{code}={calculated}"  # 計算式の文字列
    print(f"{step:<5} {char:<5} {code:<6} {prev:<12} {formula:<28} {h:<12} 0x{h:08X}")  # 表示する

print("-" * 85)  # 区切り線
print(f"最終ハッシュ値: {h} (0x{h:08X})")  # 最終結果を表示する
```

---

### 標準課題7 解答

```python
# ============================================================
# 標準課題7 解答: 2つのハッシュ関数の分布を比較する
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ"""
    h = 0  # ハッシュ値を初期化する
    for char in key:  # 各文字を処理する
        h = (h * base + ord(char)) & mask  # 多項式計算
    return h  # 返す

words = ["apple", "banana", "cherry", "date", "elderberry",  # 10個の英単語
         "fig", "grape", "honeydew", "kiwi", "lemon"]
table_size = 10  # テーブルサイズ

# --- ハッシュ値を計算する ---
print(f"{'単語':<12} {'単純':<6} {'多項式':<8}")  # ヘッダー行
print("-" * 30)  # 区切り線
simple_slots = {}  # 単純ハッシュのスロット分布
poly_slots = {}  # 多項式ハッシュのスロット分布

for word in words:  # 各単語についてハッシュ値を計算する
    s = simple_hash(word, table_size)  # 単純ハッシュ値
    p = polynomial_hash(word) % table_size  # 多項式ハッシュ値
    print(f"{word:<12} {s:<6} {p:<8}")  # 結果を表示する
    simple_slots[s] = simple_slots.get(s, 0) + 1  # 単純ハッシュの分布を記録する
    poly_slots[p] = poly_slots.get(p, 0) + 1  # 多項式ハッシュの分布を記録する

# --- 分布を比較する ---
print(f"\n=== スロット分布比較 ===")  # セクション見出し
print(f"{'スロット':<8} {'単純':<8} {'多項式':<8}")  # ヘッダー行
print("-" * 25)  # 区切り線
for i in range(table_size):  # 各スロットについて表示する
    s_count = simple_slots.get(i, 0)  # 単純ハッシュの単語数
    p_count = poly_slots.get(i, 0)  # 多項式ハッシュの単語数
    if s_count > 0 or p_count > 0:  # いずれかに単語がある場合
        print(f"  {i:<8} {s_count:<8} {p_count:<8}")  # 表示する

s_collision = sum(1 for v in simple_slots.values() if v > 1)  # 単純ハッシュの衝突数
p_collision = sum(1 for v in poly_slots.values() if v > 1)  # 多項式ハッシュの衝突数
print(f"\n衝突スロット数: 単純={s_collision}, 多項式={p_collision}")  # 衝突数を比較する
```

---

### 標準課題8 解答

```python
# ============================================================
# 標準課題8 解答: アナグラムのハッシュ値比較
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ"""
    h = 0  # 初期化
    for char in key:  # 各文字
        h = (h * base + ord(char)) & mask  # 計算
    return h  # 返す

anagrams = ["abc", "bca", "cab", "acb", "bac", "cba"]  # abcのすべてのアナグラム
table_size = 10  # テーブルサイズ

print("=== アナグラムのハッシュ値比較 ===")  # タイトル
print(f"{'文字列':<8} {'単純ハッシュ':<12} {'多項式ハッシュ':<16} {'多項式(16進)'}")  # ヘッダー
print("-" * 55)  # 区切り線

simple_values = set()  # 単純ハッシュの値を記録する集合
poly_values = set()  # 多項式ハッシュの値を記録する集合

for word in anagrams:  # 各アナグラムについてハッシュ値を計算する
    s = simple_hash(word, table_size)  # 単純ハッシュ値
    p = polynomial_hash(word)  # 多項式ハッシュ値
    simple_values.add(s)  # 値を集合に追加する
    poly_values.add(p)  # 値を集合に追加する
    print(f"{word:<8} {s:<12} {p:<16} 0x{p:08X}")  # 結果を表示する

print(f"\n単純ハッシュのユニーク値数: {len(simple_values)} (全{len(anagrams)}文字列中)")  # ユニーク数
print(f"多項式ハッシュのユニーク値数: {len(poly_values)} (全{len(anagrams)}文字列中)")  # ユニーク数

if len(simple_values) == 1:  # 単純ハッシュがすべて同じ場合
    print("→ 単純ハッシュ: 全て同じ値（アナグラムを区別できない）")  # 説明
if len(poly_values) == len(anagrams):  # 多項式ハッシュがすべて異なる場合
    print("→ 多項式ハッシュ: 全て異なる値（アナグラムを区別できる!）")  # 説明
```

---

### 標準課題9 解答

```python
# ============================================================
# 標準課題9 解答: テーブルサイズと衝突の関係（素数 vs 非素数）
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

words = [  # 20個以上の英単語
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
    "watermelon", "xigua", "yuzu", "zucchini",
]

table_sizes = [7, 10, 13, 20]  # テストするテーブルサイズ（7,13は素数、10,20は非素数）

print(f"単語数: {len(words)}")  # 単語数を表示する
print("=" * 60)  # 区切り線

for table_size in table_sizes:  # 各テーブルサイズでテストする
    is_prime = "素数" if table_size in [7, 13] else "非素数"  # 素数判定
    slots = {}  # スロット分布
    for word in words:  # 各単語のハッシュ値を計算する
        h = simple_hash(word, table_size)  # ハッシュ値
        if h not in slots:  # スロット初出
            slots[h] = []  # 初期化
        slots[h].append(word)  # 追加

    collision_slots = sum(1 for v in slots.values() if len(v) > 1)  # 衝突スロット数
    max_slot_size = max(len(v) for v in slots.values())  # 最大スロットサイズ
    used_slots = len(slots)  # 使用スロット数

    print(f"\nテーブルサイズ: {table_size} ({is_prime})")  # テーブルサイズを表示する
    print(f"  使用スロット: {used_slots}/{table_size}")  # 使用率を表示する
    print(f"  衝突スロット: {collision_slots}")  # 衝突数を表示する
    print(f"  最大スロットサイズ: {max_slot_size}")  # 最大を表示する

print("\n=== 分析 ===")  # 分析セクション
print("素数サイズの方が、一般的に衝突が少なく均等に分布する傾向があります")  # まとめ
```

---

### 標準課題10 解答

```python
# ============================================================
# 標準課題10 解答: ハッシュ分布の比較（テキストヒストグラム+標準偏差）
# ============================================================

import math  # 標準偏差計算用モジュール

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ"""
    h = 0  # 初期化
    for char in key:  # 各文字
        h = (h * base + ord(char)) & mask  # 計算
    return h  # 返す

def calc_std_dev(counts):  # 標準偏差を計算する関数
    """リストの標準偏差を計算する"""
    n = len(counts)  # 要素数
    mean = sum(counts) / n  # 平均を計算する
    variance = sum((x - mean) ** 2 for x in counts) / n  # 分散を計算する
    return math.sqrt(variance)  # 標準偏差を返す

words = [  # 20個の英単語
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
]
table_size = 10  # テーブルサイズ

# --- 各ハッシュ関数の分布を計算する ---
simple_counts = [0] * table_size  # 単純ハッシュのスロット別カウント
poly_counts = [0] * table_size  # 多項式ハッシュのスロット別カウント

for word in words:  # 各単語についてハッシュ値を計算する
    simple_counts[simple_hash(word, table_size)] += 1  # 単純ハッシュのカウントを増やす
    poly_counts[polynomial_hash(word) % table_size] += 1  # 多項式ハッシュのカウントを増やす

# --- テキストヒストグラムを表示する ---
print(f"テーブルサイズ: {table_size}, 単語数: {len(words)}")  # テスト条件
print(f"理想: 各スロットに {len(words) / table_size:.1f}個")  # 理想分布
print()  # 空行

print("=== 単純ハッシュの分布 ===")  # 単純ハッシュのヒストグラム
for i in range(table_size):  # 各スロット
    bar = "#" * simple_counts[i]  # #で棒グラフを作る
    print(f"  スロット{i}: {bar} ({simple_counts[i]}個)")  # 表示する

print(f"\n=== 多項式ハッシュの分布 ===")  # 多項式ハッシュのヒストグラム
for i in range(table_size):  # 各スロット
    bar = "#" * poly_counts[i]  # #で棒グラフを作る
    print(f"  スロット{i}: {bar} ({poly_counts[i]}個)")  # 表示する

# --- 標準偏差で比較する ---
std_simple = calc_std_dev(simple_counts)  # 単純ハッシュの標準偏差
std_poly = calc_std_dev(poly_counts)  # 多項式ハッシュの標準偏差

print(f"\n=== 分布の偏り（標準偏差） ===")  # 分析セクション
print(f"  単純ハッシュ:   {std_simple:.3f}")  # 標準偏差を表示する
print(f"  多項式ハッシュ: {std_poly:.3f}")  # 標準偏差を表示する
print(f"  （値が小さいほど均等に分布している）")  # 説明

if std_poly < std_simple:  # 多項式の方が均等な場合
    print(f"\n結論: 多項式ハッシュの方がより均等に分布しています")  # 結論
else:  # 単純の方が均等な場合
    print(f"\n結論: 単純ハッシュの方がより均等に分布しています")  # 結論
```

---

### 発展課題1 解答

```python
# ============================================================
# 発展課題1 解答: matplotlibでハッシュ分布を可視化
# ============================================================

import matplotlib.pyplot as plt  # グラフ描画用モジュール
import numpy as np  # 数値計算用モジュール

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash(key, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ"""
    h = 0  # 初期化
    for char in key:  # 各文字
        h = (h * base + ord(char)) & mask  # 計算
    return h  # 返す

# --- 50個以上の英単語を用意する ---
words = [  # 英単語リスト
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
    "watermelon", "xigua", "yuzu", "zucchini", "avocado",
    "blueberry", "coconut", "dragonfruit", "eggplant", "feijoa",
    "guava", "hazelnut", "jackfruit", "kumquat", "lime",
    "mulberry", "nutmeg", "olive", "peach", "plum",
    "raisin", "sage", "thyme", "tomato", "turnip",
    "ube", "violet", "walnut", "yam", "zest",
]
table_size = 20  # テーブルサイズ

# --- ハッシュ値を計算する ---
simple_counts = [0] * table_size  # 単純ハッシュのスロット別カウント
poly_counts = [0] * table_size  # 多項式ハッシュのスロット別カウント

for word in words:  # 各単語についてハッシュ値を計算する
    simple_counts[simple_hash(word, table_size)] += 1  # 単純ハッシュのカウント
    poly_counts[polynomial_hash(word) % table_size] += 1  # 多項式ハッシュのカウント

# --- グラフ描画 ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 2つのグラフを横に並べる
x = np.arange(table_size)  # X軸の位置
ideal = len(words) / table_size  # 理想的な均等分布の値

# --- 左: 単純ハッシュ ---
ax1 = axes[0]  # 左のグラフ
ax1.bar(x, simple_counts, color="#e74c3c", alpha=0.7, label="Simple Hash")  # 棒グラフ
ax1.axhline(y=ideal, color="black", linestyle="--", label=f"Ideal ({ideal:.1f})")  # 理想線
ax1.set_xlabel("Slot Number")  # X軸ラベル
ax1.set_ylabel("Word Count")  # Y軸ラベル
ax1.set_title("Simple Hash Distribution")  # タイトル
ax1.set_xticks(x)  # 目盛り
ax1.legend()  # 凡例
ax1.grid(axis="y", alpha=0.3)  # グリッド

# --- 右: 多項式ハッシュ ---
ax2 = axes[1]  # 右のグラフ
ax2.bar(x, poly_counts, color="#3498db", alpha=0.7, label="Polynomial Hash")  # 棒グラフ
ax2.axhline(y=ideal, color="black", linestyle="--", label=f"Ideal ({ideal:.1f})")  # 理想線
ax2.set_xlabel("Slot Number")  # X軸ラベル
ax2.set_ylabel("Word Count")  # Y軸ラベル
ax2.set_title("Polynomial Hash Distribution")  # タイトル
ax2.set_xticks(x)  # 目盛り
ax2.legend()  # 凡例
ax2.grid(axis="y", alpha=0.3)  # グリッド

plt.tight_layout()  # レイアウト調整
plt.savefig("hash_distribution.png", dpi=150)  # ファイルに保存する
plt.show()  # グラフを表示する
print("グラフを hash_distribution.png に保存しました")  # 完了メッセージ
```

---

### 発展課題2 解答

```python
# ============================================================
# 発展課題2 解答: オリジナルハッシュ関数の設計
# ============================================================

def simple_hash(key, table_size):  # 単純ハッシュ関数
    """単純ハッシュ: ord値の合計 mod テーブルサイズ"""
    total = 0  # 合計を初期化する
    for char in key:  # 各文字を処理する
        total += ord(char)  # ord値を加算する
    return total % table_size  # 余りを返す

def polynomial_hash_mod(key, table_size, base=31, mask=0xFFFFFFFF):  # 多項式ハッシュ関数
    """多項式ハッシュ: h = (h * base + ord(c)) & mask"""
    h = 0  # 初期化
    for char in key:  # 各文字
        h = (h * base + ord(char)) & mask  # 計算
    return h % table_size  # テーブルサイズで余りを取る

def custom_hash(key, table_size):  # オリジナルハッシュ関数
    """
    オリジナル: XOR回転ハッシュ
    設計理由:
    - XOR演算でビットを混ぜることで分布を均等にする
    - 位置情報を加えてアナグラムを区別する
    - ビット回転で上位ビットと下位ビットを混合する
    """
    h = 0  # ハッシュ値を初期化する
    for i, char in enumerate(key):  # 各文字を位置番号付きで処理する
        code = ord(char)  # 文字を数値に変換する
        h = h ^ (code * (i + 1))  # XORと位置の積で混ぜる
        h = ((h << 5) | (h >> 27)) & 0xFFFFFFFF  # 5ビット左回転する
        h = (h + code) & 0xFFFFFFFF  # ord値を加算する
    return h % table_size  # テーブルサイズで余りを取る

# --- テスト用の単語リスト ---
words = [  # 20個の英単語
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
]
table_size = 10  # テーブルサイズ

# --- 3つのハッシュ関数で分布を計算する ---
hash_funcs = [  # テストするハッシュ関数のリスト
    ("単純ハッシュ", lambda w: simple_hash(w, table_size)),  # 単純
    ("多項式ハッシュ", lambda w: polynomial_hash_mod(w, table_size)),  # 多項式
    ("XOR回転ハッシュ", lambda w: custom_hash(w, table_size)),  # オリジナル
]

import math  # 標準偏差計算用

for name, func in hash_funcs:  # 各ハッシュ関数についてテストする
    counts = [0] * table_size  # スロット別カウント
    for word in words:  # 各単語のハッシュ値を計算する
        counts[func(word)] += 1  # カウントを増やす

    collision = sum(1 for c in counts if c > 1)  # 衝突スロット数
    max_count = max(counts)  # 最大スロットサイズ
    mean = sum(counts) / len(counts)  # 平均
    std = math.sqrt(sum((c - mean) ** 2 for c in counts) / len(counts))  # 標準偏差

    print(f"=== {name} ===")  # ハッシュ関数名を表示する
    for i in range(table_size):  # 各スロットを表示する
        bar = "#" * counts[i]  # #で棒グラフ
        print(f"  スロット{i}: {bar} ({counts[i]})")  # 表示する
    print(f"  衝突スロット: {collision}, 最大: {max_count}, 標準偏差: {std:.3f}")  # 統計を表示する
    print()  # 空行

# --- アナグラムテスト ---
print("=== アナグラム区別テスト ===")  # セクション見出し
anagrams = ["abc", "bca", "cab"]  # テスト用アナグラム
for name, func in hash_funcs:  # 各ハッシュ関数でテストする
    values = [func(w) for w in anagrams]  # 各アナグラムのハッシュ値を計算する
    unique = len(set(values))  # ユニーク値の数
    print(f"  {name}: {values} (ユニーク値: {unique}/{len(anagrams)})")  # 結果を表示する
```
