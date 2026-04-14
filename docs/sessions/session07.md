# 第7回: ハッシュ法（2）--- ハッシュテーブルと衝突解決

## 学習目標

- ハッシュテーブルの構造（配列 + ハッシュ関数）を理解する
- 衝突（collision）が起きる原因と対処法を説明できる
- 線形探索法（linear probing）を実装できる
- Python の `dict` がハッシュテーブルであることを理解する

---

## 1. 説明

### 1.1 ハッシュテーブルとは

ハッシュテーブルは **配列（スロット）** と **ハッシュ関数** の組み合わせです。

```
キー "apple" → ハッシュ関数 → インデックス 0 → テーブル[0] に格納
キー "banana" → ハッシュ関数 → インデックス 9 → テーブル[9] に格納
```

- キーからハッシュ関数でインデックスを計算し、そのインデックスにデータを格納する
- 検索・格納が平均 O(1) で行える高速なデータ構造

### 1.2 衝突（Collision）とは

異なるキーが **同じインデックス** に格納されようとすること。

- テーブルサイズは有限（例: 10 スロット）
- 格納するキーは無限に存在しうる
- **鳩の巣原理**: 11 個のデータを 10 個のスロットに入れたら、必ずどこかが重複する

### 1.3 線形探索法（Linear Probing）

衝突が起きたら **次のスロット** を試す。それも埋まっていたら **さらに次** へ。

```
目的のスロットが埋まっている
  → 1つ右にずらす
    → それも埋まっている
      → さらに1つ右にずらす
        → 空いている！ ここに格納
```

### 1.4 チェイン法（Chaining）

各スロットにリストを持たせ、衝突したデータをリストに追加する方法。

```
テーブル[3] → [("apple", 100), ("pleap", 999)]
テーブル[9] → [("banana", 80)]
```

- 線形探索法: 空きスロットを探す → テーブルが埋まると性能低下
- チェイン法: リストに追加 → テーブルサイズを超えてもデータを格納できる

### 1.5 Python の dict

Python の `dict` は内部的にハッシュテーブルを使っている。`hash()` 組み込み関数でハッシュ値を確認できる。

---

## 2. 例題

### 例題1: 配列をテーブルとして使う

```python
# ===== 配列をハッシュテーブルとして使う基本 =====

table_size = 10  # テーブルのサイズを設定する
table = [None] * table_size  # 全スロットをNoneで初期化する

print("=== 空のハッシュテーブル ===")  # テーブル表示の見出し
for i in range(table_size):  # 全スロットを順番に表示する
    print(f"  [{i}] {table[i]}")  # インデックスと中身を表示する

# --- ハッシュ関数を定義する ---
def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 文字コードの合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    index = total % size  # テーブルサイズで割った余りを計算する
    return index  # インデックスを返す

# --- キーのインデックスを計算して格納する ---
key = "apple"  # 格納するキーを設定する
value = 100  # 格納する値を設定する
index = hash_function(key, table_size)  # ハッシュ関数でインデックスを計算する
print(f"\n'{key}' のハッシュ値: {index}")  # 計算されたインデックスを表示する

table[index] = (key, value)  # テーブルにタプルとして格納する
print(f"テーブル[{index}] に ('{key}', {value}) を格納しました")  # 格納完了メッセージ

# --- 格納後のテーブルを表示する ---
print("\n=== 格納後のテーブル ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    marker = " <-- apple" if i == index else ""  # appleの位置にマークをつける
    print(f"  [{i}] {table[i]}{marker}")  # インデックスと中身を表示する
```

### 例題2: ハッシュテーブルへのデータ挿入

```python
# ===== ハッシュテーブルにデータを挿入する =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 文字コードの合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

def insert_item(table, key, value):
    """ハッシュテーブルにデータを格納する関数"""
    size = len(table)  # テーブルのサイズを取得する
    index = hash_function(key, size)  # ハッシュ関数でインデックスを計算する
    print(f"  '{key}' → インデックス {index}", end="")  # 計算結果を表示する

    if table[index] is None:  # スロットが空の場合
        table[index] = (key, value)  # そのままデータを格納する
        print(f" → 格納完了")  # 格納成功メッセージ
    else:  # スロットが既に埋まっている場合
        print(f" → 既にデータあり: {table[index]}")  # 既存データを表示する

# --- テーブルを作成してデータを挿入する ---
table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

print("=== ハッシュテーブルにデータを挿入 ===")  # 見出しを表示する
insert_item(table, "apple", 100)  # appleを格納する
insert_item(table, "banana", 80)  # bananaを格納する
insert_item(table, "cherry", 150)  # cherryを格納する
insert_item(table, "date", 200)  # dateを格納する

# --- テーブルの状態を表示する ---
print("\n=== テーブルの状態 ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    if table[i] is not None:  # データがあるスロットの場合
        print(f"  [{i}] {table[i]}")  # キーと値を表示する
    else:  # 空のスロットの場合
        print(f"  [{i}] (空)")  # 空であることを表示する
```

### 例題3: 衝突の発生を確認する

```python
# ===== 衝突（collision）の発生を確認する =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 文字コードの合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

# --- 衝突するキーの組み合わせを確認する ---
table_size = 10  # テーブルサイズを設定する
keys = ["apple", "pleap", "banana", "ananab", "cherry"]  # テスト用のキー一覧

print("=== 各キーのハッシュ値 ===")  # 見出しを表示する
for key in keys:  # 各キーについて処理する
    index = hash_function(key, table_size)  # ハッシュ値を計算する
    print(f"  '{key}' → インデックス {index}")  # 結果を表示する

# --- 衝突を検出する ---
print("\n=== 衝突の検出 ===")  # 見出しを表示する
table = [None] * table_size  # 空のテーブルを作成する
collision_count = 0  # 衝突回数を初期化する

for key in keys:  # 各キーについて処理する
    index = hash_function(key, table_size)  # インデックスを計算する
    if table[index] is not None:  # スロットが既に使われている場合
        existing_key = table[index][0]  # 既存のキーを取得する
        print(f"  衝突! '{key}'(→{index}) と '{existing_key}'(→{index}) が同じ位置")  # 衝突を報告する
        collision_count = collision_count + 1  # 衝突回数を加算する
    else:  # スロットが空の場合
        table[index] = (key, key.upper())  # データを格納する
        print(f"  '{key}' → [{index}] に格納")  # 格納成功メッセージ

print(f"\n衝突回数: {collision_count}")  # 衝突の合計回数を表示する
```

### 例題4: 線形探索法で検索する

```python
# ===== 線形探索法（linear probing）による格納と検索 =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 文字コードの合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

def insert_with_probing(table, key, value):
    """線形探索法でデータを格納する関数"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # 初期インデックスを計算する
    original_index = index  # 元のインデックスを記録する
    probe_count = 0  # 探索回数を初期化する

    while table[index] is not None:  # スロットが空でない間ループする
        if table[index][0] == key:  # 同じキーが既にある場合
            break  # ループを抜けて上書きする
        probe_count = probe_count + 1  # 探索回数を加算する
        index = (index + 1) % size  # 次のスロットに移動する
        if index == original_index:  # 一周してしまった場合
            print(f"  エラー: テーブルが満杯です")  # エラーメッセージを表示する
            return -1  # エラーを返す

    table[index] = (key, value)  # データを格納する
    print(f"  insert '{key}': 初期={original_index}, 探索{probe_count}回 → [{index}]")  # 結果を表示する
    return index  # 格納位置を返す

def search_with_probing(table, key):
    """線形探索法でデータを検索する関数"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # 初期インデックスを計算する
    start_index = index  # 開始位置を記録する
    probe_count = 0  # 探索回数を初期化する

    while table[index] is not None:  # スロットが空でない間ループする
        probe_count = probe_count + 1  # 探索回数を加算する
        stored_key = table[index][0]  # 格納されているキーを取得する
        stored_value = table[index][1]  # 格納されている値を取得する
        if stored_key == key:  # キーが一致した場合
            print(f"  search '{key}': [{index}]で発見, 値={stored_value}, 探索{probe_count}回")  # 結果を表示する
            return stored_value  # 値を返す
        index = (index + 1) % size  # 次のスロットに移動する
        if index == start_index:  # 一周してしまった場合
            break  # ループを抜ける

    print(f"  search '{key}': 見つかりません, 探索{probe_count}回")  # 見つからない場合のメッセージ
    return None  # Noneを返す

# --- テスト: データを格納して検索する ---
table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

print("=== データの格納 ===")  # 見出しを表示する
insert_with_probing(table, "apple", 100)  # appleを格納する
insert_with_probing(table, "banana", 80)  # bananaを格納する
insert_with_probing(table, "pleap", 999)  # pleapを格納する（appleと衝突）

print("\n=== データの検索 ===")  # 見出しを表示する
search_with_probing(table, "apple")  # appleを検索する
search_with_probing(table, "pleap")  # pleapを検索する（衝突位置にある）
search_with_probing(table, "grape")  # grapeを検索する（存在しない）
```

### 例題5: HashTable クラスの作成

```python
# ===== HashTableクラス（insert/search/delete 対応） =====

class HashTable:
    """線形探索法を使ったハッシュテーブルクラス"""

    def __init__(self, size=10):
        """コンストラクタ: テーブルを初期化する"""
        self.size = size  # テーブルサイズを保存する
        self.table = [None] * size  # 全スロットをNoneで初期化する
        self.count = 0  # 格納されたデータ数を初期化する

    def _hash(self, key):
        """ハッシュ関数: 各文字のord値の合計 mod サイズ"""
        total = 0  # 合計値を初期化する
        for char in key:  # 各文字を処理する
            total = total + ord(char)  # ord値を加算する
        return total % self.size  # テーブルサイズで割った余りを返す

    def insert(self, key, value):
        """線形探索法でデータを格納するメソッド"""
        index = self._hash(key)  # ハッシュ関数でインデックスを計算する
        original = index  # 元のインデックスを記録する
        collisions = 0  # 衝突回数を初期化する

        while self.table[index] is not None:  # スロットが埋まっている間ループする
            if self.table[index][0] == key:  # 同じキーがある場合は上書きする
                break  # ループを抜ける
            collisions = collisions + 1  # 衝突回数を加算する
            index = (index + 1) % self.size  # 次のスロットに移動する
            if index == original:  # 一周した場合
                print(f"  エラー: テーブルが満杯です")  # エラーを表示する
                return -1  # エラーを返す

        self.table[index] = (key, value)  # データを格納する
        self.count = self.count + 1  # データ数を加算する
        print(f"  insert('{key}', {value}): [{index}] (衝突{collisions}回)")  # 結果を表示する
        return index  # 格納位置を返す

    def search(self, key):
        """線形探索法でデータを検索するメソッド"""
        index = self._hash(key)  # ハッシュ関数でインデックスを計算する
        start = index  # 開始位置を記録する
        probes = 0  # 探索回数を初期化する

        while self.table[index] is not None:  # スロットが空でない間ループする
            probes = probes + 1  # 探索回数を加算する
            if self.table[index][0] == key:  # キーが一致した場合
                print(f"  search('{key}'): [{index}]で発見, 値={self.table[index][1]}, 探索{probes}回")  # 結果を表示する
                return self.table[index][1]  # 値を返す
            index = (index + 1) % self.size  # 次のスロットに移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける

        print(f"  search('{key}'): 見つかりません, 探索{probes}回")  # 見つからない場合のメッセージ
        return None  # Noneを返す

    def delete(self, key):
        """線形探索法でデータを削除するメソッド"""
        index = self._hash(key)  # ハッシュ関数でインデックスを計算する
        start = index  # 開始位置を記録する

        while self.table[index] is not None:  # スロットが空でない間ループする
            if self.table[index][0] == key:  # キーが一致した場合
                deleted_value = self.table[index][1]  # 削除する値を保存する
                self.table[index] = None  # スロットをNoneにして削除する
                self.count = self.count - 1  # データ数を減らす
                print(f"  delete('{key}'): [{index}]から削除, 値={deleted_value}")  # 削除結果を表示する
                return deleted_value  # 削除した値を返す
            index = (index + 1) % self.size  # 次のスロットに移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける

        print(f"  delete('{key}'): 見つかりません")  # 見つからない場合のメッセージ
        return None  # Noneを返す

    def display(self):
        """テーブルの全スロットを表示するメソッド"""
        print(f"\n=== HashTable (サイズ={self.size}, データ数={self.count}) ===")  # ヘッダーを表示する
        for i in range(self.size):  # 全スロットを順番に表示する
            if self.table[i] is not None:  # データがある場合
                key = self.table[i][0]  # キーを取得する
                value = self.table[i][1]  # 値を取得する
                print(f"  [{i}] '{key}': {value}")  # キーと値を表示する
            else:  # 空の場合
                print(f"  [{i}] (空)")  # 空であることを表示する

# --- テスト実行 ---
print("=== HashTable クラスのテスト ===")  # 見出しを表示する
ht = HashTable(10)  # サイズ10のテーブルを作成する

ht.insert("apple", 100)  # appleを格納する
ht.insert("banana", 80)  # bananaを格納する
ht.insert("pleap", 999)  # pleapを格納する
ht.insert("cherry", 150)  # cherryを格納する

ht.display()  # テーブルの状態を表示する

print("\n=== 検索テスト ===")  # 検索テストの見出し
ht.search("apple")  # appleを検索する
ht.search("pleap")  # pleapを検索する
ht.search("grape")  # grapeを検索する（存在しない）

print("\n=== 削除テスト ===")  # 削除テストの見出し
ht.delete("banana")  # bananaを削除する
ht.delete("grape")  # grapeを削除する（存在しない）

ht.display()  # 削除後のテーブルを表示する
```

---

## 3. 標準課題

### 課題1: 空のハッシュテーブルを作成して表示する（超やさしい）

サイズ8の空のハッシュテーブル（配列）を作成し、全スロットの内容を表示してください。

### 課題2: ハッシュ関数でインデックスを計算して値を格納・取得する（超やさしい）

サイズ10のテーブルに `"cat"`, `"dog"`, `"bird"` をハッシュ関数でインデックスを計算して格納し、キーを指定して値を取得してください。

### 課題3: 複数のデータをハッシュテーブルに挿入する（やさしい）

以下の果物と値段をハッシュテーブルに挿入し、テーブルの状態を表示してください。
- `"apple": 120`, `"banana": 80`, `"cherry": 200`, `"date": 150`

### 課題4: 挿入後のテーブル状態を詳細に表示する（やさしい）

課題3のデータに加えて `"elderberry": 300`, `"fig": 90` も挿入し、各スロットの使用状況（使用中/空き）と負荷率（データ数/テーブルサイズ）を表示してください。

### 課題5: 衝突が発生するキーの組み合わせを見つける（やややさしい）

テーブルサイズ10で、ハッシュ関数（ord合計 mod サイズ）を使ったとき、同じインデックスになるキーのペアを3組見つけて表示してください。

### 課題6: 線形探索法でデータを格納する（やややさしい）

衝突が発生するデータを用意し、線形探索法で全データを格納してください。各格納時に「衝突あり/なし」と探索回数を表示してください。

### 課題7: 線形探索法でデータを検索し、探索ステップを表示する（やや普通）

課題6のテーブルに対して、存在するキーと存在しないキーの検索を行い、各ステップで確認したスロットの内容を表示してください。

### 課題8: 検索時の探索回数を集計して平均を求める（やや普通）

10個のデータを格納したハッシュテーブルで、全データの検索に必要な探索回数をそれぞれ計測し、平均探索回数を計算してください。

### 課題9: HashTable クラスに insert/search/delete を実装する（普通）

線形探索法を使った `HashTable` クラスを作成してください。`insert`, `search`, `delete`, `display` メソッドを実装し、以下のテストを通してください。

```python
ht = HashTable(10)
ht.insert("apple", 100)
ht.insert("banana", 80)
ht.insert("pleap", 999)
ht.search("apple")     # → 100
ht.search("pleap")     # → 999
ht.delete("apple")
ht.search("apple")     # → None
ht.display()
```

### 課題10: HashTable クラスに負荷率監視とリハッシュ機能を追加する（普通）

課題9の `HashTable` クラスに、負荷率が0.7を超えたらテーブルサイズを2倍にしてリハッシュ（全データを再配置）する機能を追加してください。リハッシュ前後のテーブル状態を表示してください。

---

## 4. 発展課題

### 発展課題1: チェイン法（連鎖法）の実装

各スロットにリストを持たせるチェイン法でハッシュテーブルを実装してください。線形探索法と同じデータを格納して、衝突時の動作の違いを比較してください。

### 発展課題2: Python の dict との性能比較

自作ハッシュテーブルと Python 組み込みの `dict` について、10000件のランダムデータで格納・検索の速度を比較し、結果を表形式で表示してください。

---

## 5. 解答例

### 課題1の解答例

```python
# ===== 課題1: 空のハッシュテーブルを作成して表示する =====

table_size = 8  # テーブルサイズを8に設定する
table = [None] * table_size  # 全スロットをNoneで初期化する

print("=== 空のハッシュテーブル (サイズ=8) ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    print(f"  [{i}] {table[i]}")  # インデックスと中身を表示する

print(f"\nスロット数: {table_size}")  # スロット数を表示する
print(f"使用中: 0")  # 使用中のスロット数を表示する
print(f"空き: {table_size}")  # 空きスロット数を表示する
```

### 課題2の解答例

```python
# ===== 課題2: ハッシュ関数でインデックスを計算して格納・取得する =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

# --- データを格納する ---
items = [("cat", 3), ("dog", 5), ("bird", 7)]  # 格納するデータのリスト
print("=== データの格納 ===")  # 見出しを表示する
for key, value in items:  # 各データについて処理する
    index = hash_function(key, table_size)  # インデックスを計算する
    table[index] = (key, value)  # テーブルに格納する
    print(f"  '{key}' → インデックス {index} に値 {value} を格納")  # 結果を表示する

# --- データを取得する ---
print("\n=== データの取得 ===")  # 見出しを表示する
search_keys = ["cat", "dog", "bird"]  # 検索するキーのリスト
for key in search_keys:  # 各キーについて処理する
    index = hash_function(key, table_size)  # インデックスを計算する
    if table[index] is not None:  # スロットにデータがある場合
        stored_key = table[index][0]  # 格納されたキーを取得する
        stored_value = table[index][1]  # 格納された値を取得する
        print(f"  '{key}' → テーブル[{index}] = {stored_value}")  # 取得結果を表示する
    else:  # スロットが空の場合
        print(f"  '{key}' → 見つかりません")  # 見つからないことを表示する
```

### 課題3の解答例

```python
# ===== 課題3: 複数のデータをハッシュテーブルに挿入する =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

# --- 果物データを挿入する ---
fruits = [  # 果物と値段のリストを定義する
    ("apple", 120),
    ("banana", 80),
    ("cherry", 200),
    ("date", 150)
]

print("=== 果物データの挿入 ===")  # 見出しを表示する
for key, value in fruits:  # 各果物について処理する
    index = hash_function(key, table_size)  # インデックスを計算する
    table[index] = (key, value)  # テーブルに格納する
    print(f"  '{key}' (¥{value}) → [{index}] に格納")  # 結果を表示する

# --- テーブルの状態を表示する ---
print("\n=== テーブルの状態 ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    if table[i] is not None:  # データがある場合
        print(f"  [{i}] '{table[i][0]}': ¥{table[i][1]}")  # キーと値を表示する
    else:  # 空の場合
        print(f"  [{i}] (空)")  # 空であることを表示する
```

### 課題4の解答例

```python
# ===== 課題4: 詳細なテーブル状態と負荷率の表示 =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

# --- 全データを挿入する ---
items = [  # 格納するデータのリストを定義する
    ("apple", 120), ("banana", 80), ("cherry", 200),
    ("date", 150), ("elderberry", 300), ("fig", 90)
]

print("=== データの挿入 ===")  # 見出しを表示する
for key, value in items:  # 各データについて処理する
    index = hash_function(key, table_size)  # インデックスを計算する
    table[index] = (key, value)  # テーブルに格納する
    print(f"  '{key}' → [{index}]")  # 格納位置を表示する

# --- 詳細な状態を表示する ---
print("\n=== テーブルの詳細状態 ===")  # 見出しを表示する
used_count = 0  # 使用中のスロット数を初期化する
for i in range(table_size):  # 全スロットを順番に表示する
    if table[i] is not None:  # データがある場合
        status = "使用中"  # ステータスを使用中にする
        used_count = used_count + 1  # 使用中カウントを加算する
        print(f"  [{i}] {status} | '{table[i][0]}': {table[i][1]}")  # 詳細を表示する
    else:  # 空の場合
        status = "空き  "  # ステータスを空きにする
        print(f"  [{i}] {status} |")  # 空きであることを表示する

# --- 負荷率を計算して表示する ---
load_factor = used_count / table_size  # 負荷率を計算する
empty_count = table_size - used_count  # 空きスロット数を計算する
print(f"\n--- 統計 ---")  # 統計の見出し
print(f"  テーブルサイズ: {table_size}")  # テーブルサイズを表示する
print(f"  使用中: {used_count}")  # 使用中スロット数を表示する
print(f"  空き: {empty_count}")  # 空きスロット数を表示する
print(f"  負荷率: {load_factor:.1%}")  # 負荷率をパーセントで表示する
```

### 課題5の解答例

```python
# ===== 課題5: 衝突するキーのペアを見つける =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

table_size = 10  # テーブルサイズを設定する

# --- 多数のキーのハッシュ値を計算する ---
candidates = [  # テスト用のキーリストを定義する
    "apple", "pleap", "banana", "ananab", "cherry",
    "fig", "gif", "date", "kiwi", "lemon",
    "mango", "grape", "peach", "plum", "pear"
]

print("=== 各キーのハッシュ値 ===")  # 見出しを表示する
hash_groups = {}  # ハッシュ値ごとにキーをグループ化する辞書
for key in candidates:  # 各キーについて処理する
    index = hash_function(key, table_size)  # ハッシュ値を計算する
    print(f"  '{key}' → {index}")  # 結果を表示する
    if index not in hash_groups:  # このハッシュ値が初めての場合
        hash_groups[index] = []  # 空のリストを作成する
    hash_groups[index].append(key)  # キーをグループに追加する

# --- 衝突するペアを表示する ---
print("\n=== 衝突するキーのペア ===")  # 見出しを表示する
pair_count = 0  # 発見したペア数を初期化する
for index in hash_groups:  # 各ハッシュ値について処理する
    group = hash_groups[index]  # そのハッシュ値のキーリストを取得する
    if len(group) >= 2:  # 2つ以上のキーがある場合（衝突）
        for i in range(len(group)):  # ペアの最初のキーを選ぶ
            for j in range(i + 1, len(group)):  # ペアの2番目のキーを選ぶ
                pair_count = pair_count + 1  # ペア数を加算する
                print(f"  ペア{pair_count}: '{group[i]}' と '{group[j]}' → 両方インデックス {index}")  # ペアを表示する
                if pair_count >= 3:  # 3ペア見つけたら終了する
                    break
            if pair_count >= 3:  # 3ペア見つけたら外側ループも抜ける
                break
    if pair_count >= 3:  # 3ペア見つけたら全体ループも抜ける
        break

print(f"\n合計: {pair_count}ペア発見")  # 合計ペア数を表示する
```

### 課題6の解答例

```python
# ===== 課題6: 線形探索法でデータを格納する =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

def insert_linear_probing(table, key, value):
    """線形探索法でデータを格納する関数"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # 初期インデックスを計算する
    original = index  # 元のインデックスを記録する
    probe_count = 0  # 探索回数を初期化する
    had_collision = False  # 衝突フラグを初期化する

    while table[index] is not None:  # スロットが空でない間ループする
        had_collision = True  # 衝突が発生したことを記録する
        probe_count = probe_count + 1  # 探索回数を加算する
        print(f"    [{index}]は使用中 → 次へ")  # 衝突状況を表示する
        index = (index + 1) % size  # 次のスロットに移動する

    table[index] = (key, value)  # 空きスロットにデータを格納する

    if had_collision:  # 衝突があった場合
        print(f"  '{key}': 衝突あり, 初期={original}, 探索{probe_count}回 → [{index}]に格納")  # 衝突情報を表示する
    else:  # 衝突がなかった場合
        print(f"  '{key}': 衝突なし → [{index}]に格納")  # 格納成功メッセージ

    return had_collision  # 衝突の有無を返す

# --- テスト実行 ---
table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

keys = ["apple", "pleap", "leapp", "banana", "cherry", "fig", "gif"]  # 衝突しやすいキーを含むリスト
total_collisions = 0  # 衝突の合計回数を初期化する

print("=== 線形探索法でデータを格納 ===")  # 見出しを表示する
for key in keys:  # 各キーについて処理する
    had_collision = insert_linear_probing(table, key, key.upper())  # 格納を実行する
    if had_collision:  # 衝突があった場合
        total_collisions = total_collisions + 1  # 衝突回数を加算する

# --- テーブル状態を表示する ---
print(f"\n=== テーブルの状態 ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    if table[i] is not None:  # データがある場合
        print(f"  [{i}] '{table[i][0]}': {table[i][1]}")  # データを表示する
    else:  # 空の場合
        print(f"  [{i}] (空)")  # 空であることを表示する

print(f"\n衝突が発生した挿入: {total_collisions} / {len(keys)}")  # 衝突統計を表示する
```

### 課題7の解答例

```python
# ===== 課題7: 線形探索法による検索ステップの表示 =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

def insert_lp(table, key, value):
    """線形探索法で格納する（表示なし版）"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # インデックスを計算する
    while table[index] is not None:  # スロットが空でない間ループする
        if table[index][0] == key:  # 同じキーの場合
            break  # 上書きする
        index = (index + 1) % size  # 次のスロットに移動する
    table[index] = (key, value)  # データを格納する

def search_with_steps(table, key):
    """線形探索法で検索し、各ステップを表示する関数"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # 初期インデックスを計算する
    start = index  # 開始位置を記録する
    step = 0  # ステップ数を初期化する

    print(f"  '{key}' を検索（初期インデックス={index}）")  # 検索開始を表示する

    while table[index] is not None:  # スロットが空でない間ループする
        step = step + 1  # ステップ数を加算する
        stored_key = table[index][0]  # 格納キーを取得する
        stored_value = table[index][1]  # 格納値を取得する
        if stored_key == key:  # キーが一致した場合
            print(f"    ステップ{step}: [{index}] '{stored_key}'={stored_value} → 発見!")  # 発見を表示する
            return stored_value  # 値を返す
        else:  # キーが一致しない場合
            print(f"    ステップ{step}: [{index}] '{stored_key}'={stored_value} → 不一致")  # 不一致を表示する
        index = (index + 1) % size  # 次のスロットに移動する
        if index == start:  # 一周した場合
            break  # ループを抜ける

    if table[index] is None:  # 空スロットに到達した場合
        step = step + 1  # ステップ数を加算する
        print(f"    ステップ{step}: [{index}] 空スロット → 見つかりません")  # 結果を表示する
    else:  # 一周した場合
        print(f"    一周して見つかりません")  # 結果を表示する

    return None  # Noneを返す

# --- テーブルにデータを準備する ---
table_size = 10  # テーブルサイズを設定する
table = [None] * table_size  # 空のテーブルを作成する

data = ["apple", "pleap", "banana", "cherry", "fig"]  # 格納するデータ
for key in data:  # 各キーを格納する
    insert_lp(table, key, key.upper())  # テーブルに挿入する

# --- テーブルを表示する ---
print("=== 現在のテーブル ===")  # 見出しを表示する
for i in range(table_size):  # 全スロットを順番に表示する
    if table[i] is not None:  # データがある場合
        print(f"  [{i}] '{table[i][0]}'")  # キーを表示する
    else:  # 空の場合
        print(f"  [{i}] (空)")  # 空であることを表示する

# --- 検索テスト ---
print("\n=== 検索テスト ===")  # 見出しを表示する
search_with_steps(table, "apple")  # 存在するキーを検索する
print()  # 空行を表示する
search_with_steps(table, "pleap")  # 衝突位置にあるキーを検索する
print()  # 空行を表示する
search_with_steps(table, "grape")  # 存在しないキーを検索する
```

### 課題8の解答例

```python
# ===== 課題8: 平均探索回数の計算 =====

def hash_function(key, size):
    """キーからインデックスを計算するハッシュ関数"""
    total = 0  # 合計値を初期化する
    for char in key:  # キーの各文字を処理する
        total = total + ord(char)  # 文字コードを合計に加算する
    return total % size  # テーブルサイズで割った余りを返す

def insert_lp(table, key, value):
    """線形探索法で格納する（表示なし版）"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # インデックスを計算する
    while table[index] is not None:  # スロットが空でない間ループする
        if table[index][0] == key:  # 同じキーの場合
            break  # 上書きする
        index = (index + 1) % size  # 次のスロットに移動する
    table[index] = (key, value)  # データを格納する

def count_probes(table, key):
    """キーの検索に必要な探索回数を返す関数"""
    size = len(table)  # テーブルサイズを取得する
    index = hash_function(key, size)  # 初期インデックスを計算する
    start = index  # 開始位置を記録する
    probes = 0  # 探索回数を初期化する

    while table[index] is not None:  # スロットが空でない間ループする
        probes = probes + 1  # 探索回数を加算する
        if table[index][0] == key:  # キーが一致した場合
            return probes  # 探索回数を返す
        index = (index + 1) % size  # 次のスロットに移動する
        if index == start:  # 一周した場合
            break  # ループを抜ける

    return probes  # 探索回数を返す（見つからなかった場合も）

# --- テーブルにデータを格納する ---
table_size = 15  # テーブルサイズを設定する（データより少し大きめ）
table = [None] * table_size  # 空のテーブルを作成する

keys = ["apple", "banana", "cherry", "date", "elderberry",  # 格納するキーのリスト
        "fig", "grape", "honeydew", "kiwi", "lemon"]

for key in keys:  # 各キーを格納する
    insert_lp(table, key, key.upper())  # テーブルに挿入する

# --- 各キーの探索回数を計測する ---
print("=== 各キーの探索回数 ===")  # 見出しを表示する
total_probes = 0  # 探索回数の合計を初期化する

for key in keys:  # 各キーについて処理する
    probes = count_probes(table, key)  # 探索回数を計測する
    total_probes = total_probes + probes  # 合計に加算する
    print(f"  '{key}': {probes}回")  # 結果を表示する

# --- 平均探索回数を計算する ---
average_probes = total_probes / len(keys)  # 平均探索回数を計算する
print(f"\n--- 統計 ---")  # 統計の見出し
print(f"  データ数: {len(keys)}")  # データ数を表示する
print(f"  テーブルサイズ: {table_size}")  # テーブルサイズを表示する
print(f"  負荷率: {len(keys)/table_size:.1%}")  # 負荷率を表示する
print(f"  探索回数の合計: {total_probes}")  # 合計探索回数を表示する
print(f"  平均探索回数: {average_probes:.2f}")  # 平均探索回数を表示する
```

### 課題9の解答例

```python
# ===== 課題9: HashTableクラスの実装 =====

class HashTable:
    """線形探索法を使ったハッシュテーブルクラス"""

    def __init__(self, size=10):
        """コンストラクタ: テーブルを初期化する"""
        self.size = size  # テーブルサイズを保存する
        self.table = [None] * size  # 全スロットをNoneで初期化する
        self.count = 0  # データ数を初期化する

    def _hash(self, key):
        """ハッシュ関数: ord値の合計 mod サイズ"""
        total = 0  # 合計値を初期化する
        for char in key:  # 各文字を処理する
            total = total + ord(char)  # ord値を加算する
        return total % self.size  # 余りを返す

    def insert(self, key, value):
        """線形探索法でデータを格納するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        original = index  # 元のインデックスを記録する
        collisions = 0  # 衝突回数を初期化する

        while self.table[index] is not None:  # スロットが埋まっている間ループ
            if self.table[index][0] == key:  # 同じキーなら上書きする
                self.table[index] = (key, value)  # 値を更新する
                print(f"  insert('{key}', {value}): [{index}] 上書き")  # 結果を表示する
                return index  # 格納位置を返す
            collisions = collisions + 1  # 衝突回数を加算する
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == original:  # 一周した場合
                print(f"  エラー: テーブルが満杯です")  # エラーを表示する
                return -1  # エラーを返す

        self.table[index] = (key, value)  # データを格納する
        self.count = self.count + 1  # データ数を加算する
        print(f"  insert('{key}', {value}): [{index}] (衝突{collisions}回)")  # 結果を表示する
        return index  # 格納位置を返す

    def search(self, key):
        """線形探索法でデータを検索するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        start = index  # 開始位置を記録する
        probes = 0  # 探索回数を初期化する

        while self.table[index] is not None:  # スロットが空でない間ループ
            probes = probes + 1  # 探索回数を加算する
            if self.table[index][0] == key:  # キーが一致した場合
                result = self.table[index][1]  # 値を取得する
                print(f"  search('{key}'): [{index}]で発見, 値={result}, 探索{probes}回")  # 結果を表示する
                return result  # 値を返す
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける

        print(f"  search('{key}'): 見つかりません, 探索{probes}回")  # 見つからない場合を表示する
        return None  # Noneを返す

    def delete(self, key):
        """線形探索法でデータを削除するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        start = index  # 開始位置を記録する

        while self.table[index] is not None:  # スロットが空でない間ループ
            if self.table[index][0] == key:  # キーが一致した場合
                deleted_value = self.table[index][1]  # 削除する値を保存する
                self.table[index] = None  # スロットを空にする
                self.count = self.count - 1  # データ数を減らす
                print(f"  delete('{key}'): [{index}]から削除, 値={deleted_value}")  # 結果を表示する
                return deleted_value  # 削除した値を返す
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける

        print(f"  delete('{key}'): 見つかりません")  # 見つからない場合を表示する
        return None  # Noneを返す

    def display(self):
        """テーブルの全スロットを表示するメソッド"""
        print(f"\n=== HashTable (サイズ={self.size}, データ数={self.count}) ===")  # ヘッダーを表示する
        for i in range(self.size):  # 全スロットを順番に表示する
            if self.table[i] is not None:  # データがある場合
                print(f"  [{i}] '{self.table[i][0]}': {self.table[i][1]}")  # データを表示する
            else:  # 空の場合
                print(f"  [{i}] (空)")  # 空であることを表示する

# --- テスト実行 ---
print("=== HashTable テスト ===")  # 見出しを表示する
ht = HashTable(10)  # サイズ10のテーブルを作成する

ht.insert("apple", 100)  # appleを格納する
ht.insert("banana", 80)  # bananaを格納する
ht.insert("pleap", 999)  # pleapを格納する

print("\n--- 検索 ---")  # 検索の見出し
ht.search("apple")  # appleを検索する（→ 100）
ht.search("pleap")  # pleapを検索する（→ 999）

print("\n--- 削除と再検索 ---")  # 削除の見出し
ht.delete("apple")  # appleを削除する
ht.search("apple")  # 削除後にappleを検索する（→ None）

ht.display()  # テーブルの状態を表示する
```

### 課題10の解答例

```python
# ===== 課題10: 負荷率監視とリハッシュ機能付きHashTable =====

class HashTable:
    """リハッシュ機能付きハッシュテーブルクラス"""

    def __init__(self, size=10):
        """コンストラクタ: テーブルを初期化する"""
        self.size = size  # テーブルサイズを保存する
        self.table = [None] * size  # 全スロットをNoneで初期化する
        self.count = 0  # データ数を初期化する
        self.load_threshold = 0.7  # リハッシュ閾値を設定する

    def _hash(self, key):
        """ハッシュ関数: ord値の合計 mod サイズ"""
        total = 0  # 合計値を初期化する
        for char in key:  # 各文字を処理する
            total = total + ord(char)  # ord値を加算する
        return total % self.size  # 余りを返す

    def _load_factor(self):
        """現在の負荷率を計算するメソッド"""
        return self.count / self.size  # データ数/テーブルサイズを返す

    def _rehash(self):
        """テーブルサイズを2倍にしてリハッシュするメソッド"""
        old_size = self.size  # 古いサイズを記録する
        old_table = self.table  # 古いテーブルを保存する

        self.size = old_size * 2  # テーブルサイズを2倍にする
        self.table = [None] * self.size  # 新しい空のテーブルを作成する
        self.count = 0  # データ数をリセットする

        print(f"\n  *** リハッシュ実行: サイズ {old_size} → {self.size} ***")  # リハッシュ通知

        for slot in old_table:  # 古いテーブルの全スロットを処理する
            if slot is not None:  # データがある場合
                key = slot[0]  # キーを取得する
                value = slot[1]  # 値を取得する
                index = self._hash(key)  # 新しいインデックスを計算する
                while self.table[index] is not None:  # 空きスロットを探す
                    index = (index + 1) % self.size  # 次のスロットに移動する
                self.table[index] = (key, value)  # 新しい位置に格納する
                self.count = self.count + 1  # データ数を加算する
                print(f"    '{key}' → [{index}]")  # 再配置結果を表示する

    def insert(self, key, value):
        """データを格納する（負荷率チェック付き）"""
        # --- 負荷率チェック ---
        current_load = self._load_factor()  # 現在の負荷率を計算する
        if current_load > self.load_threshold:  # 閾値を超えた場合
            print(f"  負荷率 {current_load:.1%} > {self.load_threshold:.0%} → リハッシュが必要")  # 警告を表示する
            self._rehash()  # リハッシュを実行する

        index = self._hash(key)  # インデックスを計算する
        original = index  # 元のインデックスを記録する

        while self.table[index] is not None:  # スロットが埋まっている間ループ
            if self.table[index][0] == key:  # 同じキーなら上書きする
                self.table[index] = (key, value)  # 値を更新する
                return index  # 格納位置を返す
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == original:  # 一周した場合
                return -1  # エラーを返す

        self.table[index] = (key, value)  # データを格納する
        self.count = self.count + 1  # データ数を加算する
        print(f"  insert('{key}'): [{index}] (負荷率={self._load_factor():.1%})")  # 結果を表示する
        return index  # 格納位置を返す

    def search(self, key):
        """線形探索法でデータを検索するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        start = index  # 開始位置を記録する

        while self.table[index] is not None:  # スロットが空でない間ループ
            if self.table[index][0] == key:  # キーが一致した場合
                print(f"  search('{key}'): 発見, 値={self.table[index][1]}")  # 結果を表示する
                return self.table[index][1]  # 値を返す
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける

        print(f"  search('{key}'): 見つかりません")  # 見つからない場合を表示する
        return None  # Noneを返す

    def display(self):
        """テーブルの全スロットを表示するメソッド"""
        print(f"\n=== HashTable (サイズ={self.size}, データ数={self.count}, "
              f"負荷率={self._load_factor():.1%}) ===")  # ヘッダーを表示する
        for i in range(self.size):  # 全スロットを順番に表示する
            if self.table[i] is not None:  # データがある場合
                print(f"  [{i}] '{self.table[i][0]}': {self.table[i][1]}")  # データを表示する
            else:  # 空の場合
                print(f"  [{i}] (空)")  # 空であることを表示する

# --- テスト: リハッシュが発動するまでデータを追加 ---
print("=== リハッシュ機能付き HashTable テスト ===")  # 見出しを表示する
ht = HashTable(10)  # サイズ10のテーブルを作成する

fruits = ["apple", "banana", "cherry", "date", "elderberry",  # テスト用データ
          "fig", "grape", "honeydew", "kiwi", "lemon"]

for fruit in fruits:  # 各果物を格納する
    ht.insert(fruit, fruit.upper())  # テーブルに挿入する

ht.display()  # 最終テーブル状態を表示する

print("\n--- 検索テスト ---")  # 検索テストの見出し
ht.search("apple")  # appleを検索する
ht.search("lemon")  # lemonを検索する
```

### 発展課題1の解答例

```python
# ===== 発展課題1: チェイン法（連鎖法）の実装 =====

class ChainHashTable:
    """チェイン法を使ったハッシュテーブルクラス"""

    def __init__(self, size=10):
        """コンストラクタ: 各スロットに空のリストを持たせる"""
        self.size = size  # テーブルサイズを保存する
        self.table = []  # テーブル用のリストを作成する
        for i in range(size):  # 全スロットを初期化する
            self.table.append([])  # 各スロットに空のリストを追加する
        self.count = 0  # データ数を初期化する

    def _hash(self, key):
        """ハッシュ関数: ord値の合計 mod サイズ"""
        total = 0  # 合計値を初期化する
        for char in key:  # 各文字を処理する
            total = total + ord(char)  # ord値を加算する
        return total % self.size  # 余りを返す

    def insert(self, key, value):
        """チェイン法でデータを格納するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        chain = self.table[index]  # そのスロットのチェイン（リスト）を取得する

        for i in range(len(chain)):  # チェイン内のデータを確認する
            if chain[i][0] == key:  # 同じキーがある場合
                chain[i] = (key, value)  # 値を上書きする
                print(f"  insert('{key}'): [{index}] 上書き (チェイン長={len(chain)})")  # 結果を表示する
                return  # 処理を終了する

        chain.append((key, value))  # チェインにデータを追加する
        self.count = self.count + 1  # データ数を加算する
        print(f"  insert('{key}'): [{index}] に追加 (チェイン長={len(chain)})")  # 結果を表示する

    def search(self, key):
        """チェイン法でデータを検索するメソッド"""
        index = self._hash(key)  # インデックスを計算する
        chain = self.table[index]  # そのスロットのチェインを取得する
        probes = 0  # 探索回数を初期化する

        for item in chain:  # チェイン内のデータを順番に確認する
            probes = probes + 1  # 探索回数を加算する
            if item[0] == key:  # キーが一致した場合
                print(f"  search('{key}'): [{index}]で発見, 値={item[1]}, 探索{probes}回")  # 結果を表示する
                return item[1]  # 値を返す

        print(f"  search('{key}'): 見つかりません, 探索{probes}回")  # 見つからない場合を表示する
        return None  # Noneを返す

    def display(self):
        """テーブルの全スロットを表示するメソッド"""
        print(f"\n=== ChainHashTable (サイズ={self.size}, データ数={self.count}) ===")  # ヘッダーを表示する
        for i in range(self.size):  # 全スロットを順番に表示する
            chain = self.table[i]  # チェインを取得する
            if len(chain) > 0:  # チェインにデータがある場合
                items_str = ""  # 表示用文字列を初期化する
                for item in chain:  # チェイン内の全データを文字列にする
                    items_str = items_str + f"('{item[0]}',{item[1]}) "  # データを追加する
                print(f"  [{i}] {items_str}")  # チェインの内容を表示する
            else:  # チェインが空の場合
                print(f"  [{i}] (空)")  # 空であることを表示する

# --- 比較テスト ---
print("=== チェイン法 vs 線形探索法 ===\n")  # 見出しを表示する

keys = ["apple", "pleap", "leapp", "banana", "cherry"]  # テスト用データ

print("--- チェイン法 ---")  # チェイン法の見出し
cht = ChainHashTable(10)  # チェイン法テーブルを作成する
for key in keys:  # 各キーを格納する
    cht.insert(key, key.upper())  # テーブルに挿入する
cht.display()  # テーブルを表示する

print("\n--- チェイン法の検索 ---")  # 検索の見出し
cht.search("apple")  # appleを検索する
cht.search("pleap")  # pleapを検索する
cht.search("grape")  # grapeを検索する

print("\n--- 比較 ---")  # 比較の見出し
print("  チェイン法: 同じインデックスのデータはリストに追加される")  # チェイン法の特徴
print("  線形探索法: 衝突時に次の空きスロットを探す")  # 線形探索法の特徴
print("  チェイン法はテーブルサイズ以上のデータも格納可能")  # 利点を表示する
```

### 発展課題2の解答例

```python
# ===== 発展課題2: 自作HashTable vs Python dict の性能比較 =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール
import string  # 文字列操作用モジュール

class HashTable:
    """性能テスト用のハッシュテーブル（表示なし版）"""

    def __init__(self, size=10000):
        """コンストラクタ"""
        self.size = size  # テーブルサイズを保存する
        self.table = [None] * size  # テーブルを初期化する
        self.count = 0  # データ数を初期化する

    def _hash(self, key):
        """ハッシュ関数"""
        total = 0  # 合計値を初期化する
        for char in key:  # 各文字を処理する
            total = total + ord(char)  # ord値を加算する
        return total % self.size  # 余りを返す

    def insert(self, key, value):
        """線形探索法で格納する"""
        index = self._hash(key)  # インデックスを計算する
        original = index  # 元のインデックスを記録する
        while self.table[index] is not None:  # 空きスロットを探す
            if self.table[index][0] == key:  # 同じキーの場合
                break  # 上書きする
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == original:  # 一周した場合
                return  # 満杯なので中断する
        self.table[index] = (key, value)  # データを格納する
        self.count = self.count + 1  # データ数を加算する

    def search(self, key):
        """線形探索法で検索する"""
        index = self._hash(key)  # インデックスを計算する
        start = index  # 開始位置を記録する
        while self.table[index] is not None:  # 空でない間ループする
            if self.table[index][0] == key:  # キーが一致した場合
                return self.table[index][1]  # 値を返す
            index = (index + 1) % self.size  # 次のスロットへ移動する
            if index == start:  # 一周した場合
                break  # ループを抜ける
        return None  # 見つからなかった場合

def generate_random_words(count, length=8):
    """ランダムな文字列をcount個生成する関数"""
    words = []  # 結果リストを初期化する
    for i in range(count):  # count回繰り返す
        word = ""  # 空の文字列を初期化する
        for j in range(length):  # length文字分繰り返す
            word = word + random.choice(string.ascii_lowercase)  # ランダムな小文字を追加する
        words.append(word)  # リストに追加する
    return words  # 文字列リストを返す

# --- テストデータを生成する ---
data_size = 10000  # データ数を設定する
words = generate_random_words(data_size)  # ランダム文字列を生成する
search_targets = random.sample(words, 100)  # 検索対象を100個選ぶ

# --- 自作HashTableの格納テスト ---
print("=== 格納速度の比較 ===")  # 見出しを表示する

start_time = time.time()  # 計測を開始する
ht = HashTable(data_size * 2)  # 自作テーブルを作成する（負荷率を低く保つ）
for i in range(len(words)):  # 全単語を格納する
    ht.insert(words[i], i)  # テーブルに挿入する
ht_insert_time = time.time() - start_time  # 経過時間を計算する

start_time = time.time()  # 計測を開始する
py_dict = {}  # Python dictを作成する
for i in range(len(words)):  # 全単語を格納する
    py_dict[words[i]] = i  # dictに挿入する
dict_insert_time = time.time() - start_time  # 経過時間を計算する

print(f"  自作HashTable: {ht_insert_time:.6f} 秒")  # 自作テーブルの時間を表示する
print(f"  Python dict:   {dict_insert_time:.6f} 秒")  # dictの時間を表示する

# --- 検索速度の比較 ---
print("\n=== 検索速度の比較 ({0}件中100件検索) ===".format(data_size))  # 見出しを表示する

start_time = time.time()  # 計測を開始する
for target in search_targets:  # 各ターゲットを検索する
    ht.search(target)  # 自作テーブルで検索する
ht_search_time = time.time() - start_time  # 経過時間を計算する

start_time = time.time()  # 計測を開始する
for target in search_targets:  # 各ターゲットを検索する
    result = py_dict.get(target)  # dictで検索する
dict_search_time = time.time() - start_time  # 経過時間を計算する

print(f"  自作HashTable: {ht_search_time:.6f} 秒")  # 自作テーブルの時間を表示する
print(f"  Python dict:   {dict_search_time:.6f} 秒")  # dictの時間を表示する

# --- 比較まとめ ---
print("\n=== 結果まとめ ===")  # 見出しを表示する
print(f"  {'操作':<10} {'自作HashTable':<18} {'Python dict':<18} {'速度比'}")  # ヘッダーを表示する
print(f"  {'-'*56}")  # 区切り線を表示する

insert_ratio = ht_insert_time / dict_insert_time if dict_insert_time > 0 else 0  # 格納の速度比を計算する
search_ratio = ht_search_time / dict_search_time if dict_search_time > 0 else 0  # 検索の速度比を計算する
print(f"  {'格納':<10} {ht_insert_time:<18.6f} {dict_insert_time:<18.6f} {insert_ratio:.1f}x")  # 格納結果を表示する
print(f"  {'検索':<10} {ht_search_time:<18.6f} {dict_search_time:<18.6f} {search_ratio:.1f}x")  # 検索結果を表示する

print("\n  Python dict はC言語で最適化されたハッシュテーブルを使用しているため高速")  # 考察を表示する
```

---

## 6. まとめ

| 項目 | 内容 |
|------|------|
| ハッシュテーブル | 配列 + ハッシュ関数の組み合わせ |
| 衝突（collision） | 異なるキーが同じインデックスになること |
| 線形探索法 | 衝突時に次のスロットを試す方法 |
| チェイン法 | 衝突時にリストに追加する方法 |
| 負荷率 | データ数 / テーブルサイズ（低いほど衝突が少ない） |
| Python の dict | 内部的にハッシュテーブルを使っている |
| 検索速度 | ハッシュテーブル O(1) vs 線形探索 O(n) |
