# 第11回: 度数分布法（2）--- 安定ソートとファイル入出力

## 学習目標

- **CSVファイルの読み書き**を Python で行える
- **安定ソート**（Stable Sort）の概念を理解し、なぜ重要かを説明できる
- 大規模データ（10,000~100,000件）に対して分布数えソートを適用できる
- **基数ソート**（Radix Sort）の基本的な考え方を理解する

---

## 1. 説明

### 1.1 CSVファイルとは

CSV（Comma-Separated Values）は、データをカンマで区切ったテキストファイルです。
Excel やデータベースのデータをやり取りするのによく使われます。

```
名前,数学,英語,国語
田中太郎,85,72,90
佐藤花子,92,88,76
鈴木一郎,78,95,83
```

### 1.2 Python での CSV 読み書き

Python には `csv` モジュールが標準で用意されています。

```python
import csv

# --- 書き込み ---
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["名前", "点数"])    # ヘッダー行
    writer.writerow(["田中", 85])        # データ行
    writer.writerow(["佐藤", 92])

# --- 読み込み ---
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)       # 1行目（ヘッダー）を読み飛ばす
    for row in reader:
        name = row[0]           # 文字列
        score = int(row[1])     # 数値に変換
        print(f"{name}: {score}点")
```

### 1.3 安定ソート（Stable Sort）とは

**安定ソート**とは、同じ値の要素が**元の配列での順序を保つ**ソートのことです。

```
入力: [(佐藤, 80), (田中, 90), (鈴木, 80), (山田, 90)]

安定ソート（点数で並べ替え）:
  [(佐藤, 80), (鈴木, 80), (田中, 90), (山田, 90)]
   ↑ 佐藤が鈴木より前（元の順序を保持）
   ↑ 田中が山田より前（元の順序を保持）

不安定ソート（点数で並べ替え）:
  [(鈴木, 80), (佐藤, 80), (山田, 90), (田中, 90)]
   ↑ 鈴木が佐藤より前になった（元の順序が崩れた）
```

### 1.4 安定ソートが重要な場面

**複数のキーでソートしたい場合**に安定ソートが必要です。

例: 成績データを「数学の点数→名前の五十音順」で並べたい場合

1. まず名前の五十音順でソート
2. 次に数学の点数で安定ソート

→ 同じ点数の人は五十音順が保たれる！

### 1.5 各ソートアルゴリズムの安定性

| アルゴリズム | 安定？ | 理由 |
|---|---|---|
| 挿入ソート | 安定 | 「より大きい」場合のみ交換 |
| バブルソート | 安定 | 「より大きい」場合のみ交換 |
| 分布数えソート | 安定 | 末尾から配置すれば安定 |
| 選択ソート | **不安定** | 離れた要素を交換する |
| Python sorted() | 安定 | Timsort は安定ソート |

### 1.6 基数ソート（Radix Sort）入門

基数ソートは、数値を**桁ごとに分布数えソート**するアルゴリズムです。

```
入力: [170, 45, 75, 90, 802, 24, 2, 66]

1桁目（1の位）でソート: [170, 90, 802, 2, 24, 45, 75, 66]
2桁目（10の位）でソート: [802, 2, 24, 45, 66, 170, 75, 90]
3桁目（100の位）でソート: [2, 24, 45, 66, 75, 90, 170, 802]
```

- 各桁のソートには**安定ソート**を使う必要がある（だから分布数えソートを使う）
- 計算量: O(d * (n + k))（d: 最大桁数、n: 要素数、k: 基数（通常10））

---

## 2. 例題

### 例題1: CSVファイルにデータを書き込んで読み込む

```python
import csv  # CSVモジュールを読み込む

def write_scores_csv(filename, data):
    """成績データをCSVファイルに書き出す"""

    with open(filename, "w", newline="", encoding="utf-8") as f:  # ファイルを開く
        writer = csv.writer(f)  # CSVライターを作成する
        writer.writerow(["name", "math", "english"])  # ヘッダー行を書き出す
        for row in data:  # 各データを走査する
            writer.writerow(row)  # データ行を書き出す

    print(f"CSVファイルを保存しました: {filename}")  # 完了メッセージを表示する


def read_scores_csv(filename):
    """CSVファイルから成績データを読み込む"""

    records = []  # データ格納用リスト
    with open(filename, "r", encoding="utf-8") as f:  # ファイルを開く
        reader = csv.reader(f)  # CSVリーダーを作成する
        header = next(reader)  # ヘッダー行を読み飛ばす
        print(f"ヘッダー: {header}")  # ヘッダーを表示する

        for row in reader:  # 各データ行を読む
            name = row[0]  # 名前を取得する
            math_score = int(row[1])  # 数学の点数を整数に変換する
            english_score = int(row[2])  # 英語の点数を整数に変換する
            records.append([name, math_score, english_score])  # リストに追加する

    print(f"読み込み完了: {len(records)} 件")  # 件数を表示する
    return records  # データを返す


# --- 実行 ---
sample_data = [  # テストデータを用意する
    ["Tanaka", 85, 72],  # 田中のデータ
    ["Sato", 92, 88],  # 佐藤のデータ
    ["Suzuki", 78, 95],  # 鈴木のデータ
    ["Yamada", 65, 80],  # 山田のデータ
]

write_scores_csv("scores.csv", sample_data)  # CSVに書き出す
loaded = read_scores_csv("scores.csv")  # CSVから読み込む

for record in loaded:  # 読み込んだデータを表示する
    print(f"  {record[0]}: 数学={record[1]}, 英語={record[2]}")  # 各レコードを表示する
```

### 例題2: CSVファイルにソート結果を書き出す

```python
import csv  # CSVモジュールを読み込む
import random  # 乱数モジュールを読み込む

def counting_sort_records(records, key_index, max_val):
    """レコードのリストを指定キーで分布数えソートする"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for record in records:  # 度数を数える
        count[record[key_index]] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(records)  # 出力配列を用意する
    for i in range(len(records) - 1, -1, -1):  # 末尾から配置する
        key = records[i][key_index]  # ソートキーを取得する
        position = count[key] - 1  # 配置位置を計算する
        output[position] = records[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


def write_sorted_csv(filename, records, header):
    """ソート済みデータをCSVに書き出す"""

    with open(filename, "w", newline="", encoding="utf-8") as f:  # ファイルを開く
        writer = csv.writer(f)  # ライターを作成する
        writer.writerow(header)  # ヘッダーを書き出す
        for record in records:  # 各レコードを処理する
            writer.writerow(record)  # データ行を書き出す

    print(f"ソート結果を保存しました: {filename} ({len(records)} 件)")  # 完了メッセージ


# --- 実行 ---
random.seed(42)  # シードを固定する
names = ["Tanaka", "Sato", "Suzuki", "Yamada", "Ito",
         "Watanabe", "Nakamura", "Kobayashi", "Kato", "Yoshida"]  # 名前リスト
records = []  # レコードリスト
for i, name in enumerate(names):  # 各名前でレコードを生成する
    math_score = random.randint(0, 100)  # 数学の点数をランダム生成する
    english_score = random.randint(0, 100)  # 英語の点数をランダム生成する
    records.append([name, math_score, english_score])  # レコードに追加する

print("ソート前:")  # タイトルを表示する
for r in records:  # 各レコードを表示する
    print(f"  {r[0]}: 数学={r[1]}, 英語={r[2]}")  # データを表示する

sorted_records = counting_sort_records(records, 1, 100)  # 数学の点数でソートする

print("\nソート後（数学の点数順）:")  # タイトルを表示する
for r in sorted_records:  # 各レコードを表示する
    print(f"  {r[0]}: 数学={r[1]}, 英語={r[2]}")  # データを表示する

write_sorted_csv("sorted_scores.csv", sorted_records, ["name", "math", "english"])  # CSVに書き出す
```

### 例題3: 安定ソートの動作を確認する

```python
def counting_sort_stable(data, key_func, max_val):
    """安定な分布数えソート（キー関数版）"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for item in data:  # 度数を数える
        count[key_func(item)] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する（安定のポイント）
        key = key_func(data[i])  # キーを取得する
        position = count[key] - 1  # 配置位置を計算する
        output[position] = data[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- テストデータ ---
students = [  # (名前, 点数) のリスト
    ("Sato", 80),  # 佐藤
    ("Tanaka", 90),  # 田中
    ("Suzuki", 80),  # 鈴木
    ("Yamada", 90),  # 山田
    ("Ito", 80),  # 伊藤
    ("Watanabe", 90),  # 渡辺
]

print("--- 元のデータ ---")  # タイトルを表示する
for i, (name, score) in enumerate(students):  # 各データを表示する
    print(f"  [{i}] {name}: {score}点")  # インデックスと内容を表示する

# --- 安定ソートを実行する ---
result = counting_sort_stable(  # ソートを実行する
    students,  # データ
    key_func=lambda s: s[1],  # 点数をキーにする
    max_val=100,  # 最大値
)

print("\n--- 安定ソート後 ---")  # タイトルを表示する
for i, (name, score) in enumerate(result):  # 各データを表示する
    print(f"  [{i}] {name}: {score}点")  # インデックスと内容を表示する

# --- 安定性を確認する ---
score_80 = [name for name, score in result if score == 80]  # 80点の人を抽出する
print(f"\n80点の順序: {score_80}")  # 順序を表示する
print(f"元の順序 ['Sato', 'Suzuki', 'Ito'] が保持: {score_80 == ['Sato', 'Suzuki', 'Ito']}")  # 確認する
```

### 例題4: 大規模データ（10万件）を分布数えソートする

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む

def counting_sort_large(data, max_val):
    """大規模データ用の分布数えソート"""

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


# --- 大規模データで速度計測 ---
random.seed(42)  # シードを固定する
sizes = [10000, 50000, 100000]  # データサイズのリスト
max_val = 999  # 値の範囲

print(f"値の範囲: 0 ~ {max_val}")  # 条件を表示する
print(f"{'サイズ':>8} {'分布数えソート':>14} {'sorted()':>10}")  # ヘッダー
print("-" * 36)  # 区切り線

for size in sizes:  # 各サイズで計測する
    data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する

    start = time.time()  # 計測開始
    counting_sort_large(data, max_val)  # 分布数えソートを実行する
    counting_time = time.time() - start  # 経過時間を計算する

    start = time.time()  # 計測開始
    sorted(data)  # Python組み込みソートを実行する
    builtin_time = time.time() - start  # 経過時間を計算する

    print(f"{size:>8} {counting_time:>13.4f}s {builtin_time:>9.4f}s")  # 結果を表示する
```

### 例題5: 基数ソートの基本実装

```python
def counting_sort_by_digit(data, digit_pos):
    """指定した桁で分布数えソートする（基数ソートの内部関数）"""

    base = 10  # 10進数を使う

    count = [0] * base  # 度数配列（0-9）を初期化する
    for value in data:  # 各要素を処理する
        digit = (value // digit_pos) % base  # 指定桁の数字を取り出す
        count[digit] += 1  # カウントを増やす

    for i in range(1, base):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する（安定ソート必須）
        digit = (data[i] // digit_pos) % base  # 指定桁の数字を取り出す
        position = count[digit] - 1  # 配置位置を計算する
        output[position] = data[i]  # 配置する
        count[digit] -= 1  # カウントを減らす

    return output  # ソート結果を返す


def radix_sort(data):
    """基数ソート: 各桁で分布数えソートを繰り返す"""

    if len(data) <= 1:  # 要素が1以下なら
        return data[:]  # そのまま返す

    max_val = max(data)  # 最大値を求める
    result = data[:]  # 作業用コピーを作る
    digit_pos = 1  # 1の位からスタートする

    while digit_pos <= max_val:  # 全ての桁を処理するまで繰り返す
        print(f"  {digit_pos}の位でソート: {result[:10]}...")  # 途中経過を表示する
        result = counting_sort_by_digit(result, digit_pos)  # 現在の桁でソートする
        digit_pos *= 10  # 次の桁に進む

    return result  # ソート結果を返す


# --- 実行 ---
test_data = [170, 45, 75, 90, 802, 24, 2, 66]  # テストデータ
print(f"入力: {test_data}")  # 入力を表示する

sorted_result = radix_sort(test_data)  # 基数ソートを実行する
print(f"結果: {sorted_result}")  # 結果を表示する

assert sorted_result == sorted(test_data), "基数ソートの結果が不正です"  # 検証する
print("検証OK: sorted() と一致")  # 検証結果を表示する
```

---

## 3. 標準課題

### 標準課題1（超やさしい）: テキストファイルの各行を読み込んでリストにする

テキストファイル `numbers.txt` を作成して5個の整数を書き込み、それを読み込んでリストにしてください。

**要件:**
- ファイルに1行1個ずつ整数を書き込む
- ファイルを読み込んで整数のリストを作る
- リストの内容と合計を表示する

### 標準課題2（超やさしい）: CSVファイルに5人分の成績を書き出して読み込む

5人分の `[名前, 国語, 数学]` のデータをCSVに書き出し、読み込んで表形式で表示してください。

**要件:**
- `csv.writer` でヘッダー付きCSVを作成する
- `csv.reader` で読み込む
- 各生徒の合計点も計算して表示する

### 標準課題3（やさしい）: CSVから読み込んだデータをソートしてCSVに書き出す

20人分のランダム成績データをCSVに書き出し、読み込んで数学の点数で分布数えソートし、結果を別のCSVに保存してください。

**要件:**
- 名前はアルファベットでランダム生成する（例: "Student01"）
- 数学の点数（0-100）でソートする
- ソート前のCSVとソート後のCSVの両方を作成する

### 標準課題4（やさしい）: ソート結果をフォーマットしてテキストファイルに出力する

50人分の成績データを分布数えソートし、順位付きのフォーマットされたレポートをテキストファイルに書き出してください。

**要件:**
- 各行に「順位. 名前: 数学 XX点, 英語 XX点, 合計 XX点」と表示する
- ファイルの先頭に統計情報（平均点・最高点・最低点）を記載する
- テキストファイルとCSVの両方に出力する

### 標準課題5（やややさしい）: 安定ソートの動作を確認する

(名前, 点数) のペア10組に対して分布数えソート（安定）を実行し、同じ点数の要素の順序が保たれることを検証してください。

**要件:**
- 同じ点数の人を意図的に複数含める
- ソート後に、同じ点数グループ内の順序が元と同じかチェックする
- 「安定」「不安定」の判定結果を表示する

### 標準課題6（やややさしい）: 安定ソートと不安定ソートを比較する

同じデータに対して分布数えソート（安定）と選択ソート（不安定）を適用し、結果の違いを表示してください。

**要件:**
- 選択ソートを自分で実装する
- 同じ点数の要素の順序がどう変わるか比較する
- 安定性の違いを明確に表示する

### 標準課題7（やや普通）: 1万件のデータを分布数えソートして実行時間を計測する

10,000件の整数データ（値の範囲 0-999）を分布数えソートし、`sorted()` と実行時間を比較してください。

**要件:**
- 3回計測して平均を取る
- ソート結果が `sorted()` と一致することを検証する
- 実行時間の比較を表示する

### 標準課題8（やや普通）: 10万件のデータで分布数えソートの性能をグラフ化する

10,000件・50,000件・100,000件のデータで分布数えソートと `sorted()` の実行時間を計測し、`matplotlib` で棒グラフを描画してください。

**要件:**
- 値の範囲は 0-999
- 各サイズで3回計測して平均を取る
- 棒グラフでバーの上に数値を表示する

### 標準課題9（普通）: 基数ソートを1桁ずつ手動でトレースする

配列 `[329, 457, 657, 839, 436, 720, 355]` に対して基数ソートを実装し、各桁でのソート結果を表示してください。

**要件:**
- 1の位 → 10の位 → 100の位 の順でソートする
- 各桁ソート前後の配列を表示する
- 各要素から桁を取り出す計算過程も表示する

### 標準課題10（普通）: 完全な基数ソートを実装して性能を比較する

基数ソートを完全に実装し、分布数えソートおよび `sorted()` と性能を比較してください。

**要件:**
- 基数ソート内部で安定な分布数えソートを使う
- 10,000件のデータ（値の範囲 0-99999）で正しさを検証する
- 3つのアルゴリズムの実行時間を比較する
- 値の範囲が広い場合（0-99999）での分布数えソートのメモリ問題を考察する

---

## 4. 発展課題

### 発展課題1: 学生レコードを複数キーでソートする

学生レコード `(名前, クラス, 数学, 英語)` のリストを「クラス昇順 → 数学降順」でソートしてください。

**要件:**
- 安定ソートを2回適用する（第2キー → 第1キー の順）
- まず数学の点数で降順ソート（100-点数 をキーにする）
- 次にクラスで昇順ソート（安定ソートなので数学順が保たれる）
- 結果をCSVに書き出す

### 発展課題2: 複数キーソートを一括で行う

学生レコードを「数学の点数降順 → 英語の点数降順 → 名前昇順」の3つのキーで一括ソートしてください。

**要件:**
- 安定ソートを3回、逆順（名前 → 英語 → 数学）で適用する
- 各ステップのソート結果を表示する
- 最終結果をフォーマットして表示する

---

## 5. 解答例

### 課題1の解答例

```python
def write_numbers_file(filename, numbers):
    """整数リストをテキストファイルに書き出す"""

    with open(filename, "w", encoding="utf-8") as f:  # ファイルを開く
        for num in numbers:  # 各整数を処理する
            f.write(str(num) + "\n")  # 整数を文字列にして1行書き出す

    print(f"ファイルを保存しました: {filename}")  # 完了メッセージ


def read_numbers_file(filename):
    """テキストファイルから整数リストを読み込む"""

    numbers = []  # 格納用リストを用意する
    with open(filename, "r", encoding="utf-8") as f:  # ファイルを開く
        for line in f:  # 各行を読む
            stripped = line.strip()  # 改行を除去する
            if stripped:  # 空行でなければ
                numbers.append(int(stripped))  # 整数に変換して追加する

    return numbers  # 整数リストを返す


# --- 実行 ---
data = [42, 17, 88, 5, 63]  # テストデータを用意する
write_numbers_file("numbers.txt", data)  # ファイルに書き出す

loaded = read_numbers_file("numbers.txt")  # ファイルから読み込む
print(f"読み込んだリスト: {loaded}")  # リストを表示する
print(f"合計: {sum(loaded)}")  # 合計を表示する
```

### 課題2の解答例

```python
import csv  # CSVモジュールを読み込む

def write_student_csv(filename, students):
    """生徒の成績をCSVに書き出す"""

    with open(filename, "w", newline="", encoding="utf-8") as f:  # ファイルを開く
        writer = csv.writer(f)  # ライターを作成する
        writer.writerow(["name", "japanese", "math"])  # ヘッダーを書き出す
        for student in students:  # 各生徒を処理する
            writer.writerow(student)  # データ行を書き出す

    print(f"CSVを保存しました: {filename}")  # 完了メッセージ


def read_student_csv(filename):
    """CSVから生徒の成績を読み込む"""

    records = []  # 格納用リスト
    with open(filename, "r", encoding="utf-8") as f:  # ファイルを開く
        reader = csv.reader(f)  # リーダーを作成する
        header = next(reader)  # ヘッダーを読み飛ばす

        for row in reader:  # 各行を処理する
            name = row[0]  # 名前を取得する
            japanese = int(row[1])  # 国語の点数を整数にする
            math = int(row[2])  # 数学の点数を整数にする
            records.append([name, japanese, math])  # リストに追加する

    return records  # データを返す


# --- 実行 ---
students = [  # 5人分のデータ
    ["Tanaka", 85, 72],  # 田中
    ["Sato", 92, 88],  # 佐藤
    ["Suzuki", 78, 95],  # 鈴木
    ["Yamada", 65, 80],  # 山田
    ["Ito", 90, 67],  # 伊藤
]

write_student_csv("students.csv", students)  # CSVに書き出す
loaded = read_student_csv("students.csv")  # CSVから読み込む

print(f"\n{'名前':>10} {'国語':>4} {'数学':>4} {'合計':>4}")  # ヘッダーを表示する
print("-" * 28)  # 区切り線
for name, jp, math in loaded:  # 各生徒を表示する
    total = jp + math  # 合計を計算する
    print(f"{name:>10} {jp:>4} {math:>4} {total:>4}")  # 表示する
```

### 課題3の解答例

```python
import csv  # CSVモジュールを読み込む
import random  # 乱数モジュールを読み込む

def generate_students(num):
    """ランダムな生徒データを生成する"""

    records = []  # 格納用リスト
    for i in range(num):  # 指定人数分ループする
        name = f"Student{i + 1:02d}"  # 名前を生成する
        math_score = random.randint(0, 100)  # 数学の点数をランダム生成する
        records.append([name, math_score])  # リストに追加する
    return records  # データを返す


def counting_sort_by_key(records, key_index, max_val):
    """レコードを指定キーで分布数えソートする"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for record in records:  # 度数を数える
        count[record[key_index]] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(records)  # 出力配列を用意する
    for i in range(len(records) - 1, -1, -1):  # 末尾から配置する
        key = records[i][key_index]  # キーを取得する
        position = count[key] - 1  # 位置を計算する
        output[position] = records[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- 実行 ---
random.seed(42)  # シードを固定する
students = generate_students(20)  # 20人分のデータを生成する

# --- ソート前をCSVに保存する ---
with open("before_sort.csv", "w", newline="", encoding="utf-8") as f:  # ファイルを開く
    writer = csv.writer(f)  # ライターを作成する
    writer.writerow(["name", "math"])  # ヘッダーを書く
    for s in students:  # 各データを書き出す
        writer.writerow(s)  # 行を書く
print("ソート前CSVを保存しました: before_sort.csv")  # メッセージ

# --- 分布数えソートする ---
sorted_students = counting_sort_by_key(students, 1, 100)  # 数学の点数でソートする

# --- ソート後をCSVに保存する ---
with open("after_sort.csv", "w", newline="", encoding="utf-8") as f:  # ファイルを開く
    writer = csv.writer(f)  # ライターを作成する
    writer.writerow(["name", "math"])  # ヘッダーを書く
    for s in sorted_students:  # 各データを書き出す
        writer.writerow(s)  # 行を書く
print("ソート後CSVを保存しました: after_sort.csv")  # メッセージ

print("\n上位5人:")  # タイトル
for s in sorted_students[-5:]:  # 上位5人を表示する
    print(f"  {s[0]}: {s[1]}点")  # 名前と点数を表示する
```

### 課題4の解答例

```python
import csv  # CSVモジュールを読み込む
import random  # 乱数モジュールを読み込む

def counting_sort_records_desc(records, key_index, max_val):
    """降順で分布数えソートする（max_val - key で昇順ソート）"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for record in records:  # 度数を数える
        inverted_key = max_val - record[key_index]  # キーを反転する（降順用）
        count[inverted_key] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(records)  # 出力配列を用意する
    for i in range(len(records) - 1, -1, -1):  # 末尾から配置する
        inverted_key = max_val - records[i][key_index]  # キーを反転する
        position = count[inverted_key] - 1  # 位置を計算する
        output[position] = records[i]  # 配置する
        count[inverted_key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- 実行 ---
random.seed(42)  # シードを固定する
records = []  # レコードリスト
for i in range(50):  # 50人分生成する
    name = f"Student{i + 1:02d}"  # 名前を生成する
    math_score = random.randint(0, 100)  # 数学をランダム生成する
    english_score = random.randint(0, 100)  # 英語をランダム生成する
    records.append([name, math_score, english_score])  # リストに追加する

# --- 数学の点数で降順ソートする ---
sorted_records = counting_sort_records_desc(records, 1, 100)  # ソートする

# --- 統計情報を計算する ---
math_scores = [r[1] for r in sorted_records]  # 数学の点数を抽出する
average = sum(math_scores) / len(math_scores)  # 平均を計算する
highest = max(math_scores)  # 最高点を取得する
lowest = min(math_scores)  # 最低点を取得する

# --- テキストファイルに出力する ---
with open("report.txt", "w", encoding="utf-8") as f:  # ファイルを開く
    f.write("===== 成績レポート =====\n")  # タイトルを書く
    f.write(f"人数: {len(sorted_records)}\n")  # 人数を書く
    f.write(f"平均点（数学）: {average:.1f}\n")  # 平均を書く
    f.write(f"最高点（数学）: {highest}\n")  # 最高点を書く
    f.write(f"最低点（数学）: {lowest}\n")  # 最低点を書く
    f.write("\n")  # 空行を書く

    for rank, record in enumerate(sorted_records, 1):  # 順位付きで処理する
        name = record[0]  # 名前を取得する
        math = record[1]  # 数学を取得する
        english = record[2]  # 英語を取得する
        total = math + english  # 合計を計算する
        f.write(f"{rank:>3}. {name}: 数学 {math:>3}点, 英語 {english:>3}点, 合計 {total:>3}点\n")  # 書く

print("テキストレポートを保存しました: report.txt")  # メッセージ

# --- CSVにも出力する ---
with open("report.csv", "w", newline="", encoding="utf-8") as f:  # CSVファイルを開く
    writer = csv.writer(f)  # ライターを作成する
    writer.writerow(["rank", "name", "math", "english", "total"])  # ヘッダーを書く
    for rank, record in enumerate(sorted_records, 1):  # 順位付きで処理する
        total = record[1] + record[2]  # 合計を計算する
        writer.writerow([rank, record[0], record[1], record[2], total])  # 行を書く

print("CSVレポートを保存しました: report.csv")  # メッセージ
```

### 課題5の解答例

```python
def counting_sort_stable_check(data, key_func, max_val):
    """安定ソートを実行して安定性を検証する"""

    # --- 分布数えソート（安定版） ---
    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for item in data:  # 度数を数える
        count[key_func(item)] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        key = key_func(data[i])  # キーを取得する
        position = count[key] - 1  # 位置を計算する
        output[position] = data[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- テストデータ ---
students = [  # 同じ点数を含むデータ
    ("Sato_A", 75), ("Tanaka_B", 90), ("Suzuki_C", 75),
    ("Yamada_D", 85), ("Ito_E", 90), ("Watanabe_F", 75),
    ("Nakamura_G", 85), ("Kobayashi_H", 90), ("Kato_I", 85),
    ("Yoshida_J", 75),
]

print("--- 元のデータ ---")  # タイトル
for i, (name, score) in enumerate(students):  # 各データを表示する
    print(f"  [{i}] {name}: {score}点")  # 表示する

result = counting_sort_stable_check(students, lambda s: s[1], 100)  # ソートする

print("\n--- ソート後 ---")  # タイトル
for i, (name, score) in enumerate(result):  # 各データを表示する
    print(f"  [{i}] {name}: {score}点")  # 表示する

# --- 安定性を検証する ---
print("\n--- 安定性の検証 ---")  # タイトル
all_stable = True  # 全体の安定性フラグ
for target_score in [75, 85, 90]:  # 各点数グループで確認する
    original_order = [n for n, s in students if s == target_score]  # 元の順序を取得する
    sorted_order = [n for n, s in result if s == target_score]  # ソート後の順序を取得する
    is_stable = original_order == sorted_order  # 順序が一致するか確認する
    status = "安定" if is_stable else "不安定"  # 判定する
    print(f"  {target_score}点: 元={original_order}")  # 元の順序を表示する
    print(f"         ソート後={sorted_order} → {status}")  # ソート後の順序を表示する
    if not is_stable:  # 不安定な場合
        all_stable = False  # フラグを更新する

print(f"\n最終判定: {'安定ソートです' if all_stable else '不安定ソートです'}")  # 判定結果
```

### 課題6の解答例

```python
def selection_sort_by_score(data):
    """選択ソート（不安定）で点数順にソートする"""

    arr = data[:]  # コピーを作る
    n = len(arr)  # 要素数を取得する
    for i in range(n):  # 先頭から処理する
        min_idx = i  # 最小値のインデックスを仮設定する
        for j in range(i + 1, n):  # 残りの要素を走査する
            if arr[j][1] < arr[min_idx][1]:  # より小さい点数が見つかったら
                min_idx = j  # インデックスを更新する
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # 交換する（ここで順序が崩れる）
    return arr  # ソート結果を返す


def counting_sort_by_score(data, max_val):
    """分布数えソート（安定）で点数順にソートする"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for item in data:  # 度数を数える
        count[item[1]] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        key = data[i][1]  # 点数を取得する
        position = count[key] - 1  # 位置を計算する
        output[position] = data[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # ソート結果を返す


# --- テストデータ ---
students = [  # 同じ点数を含むデータ
    ("Sato", 80), ("Tanaka", 90), ("Suzuki", 80),
    ("Yamada", 90), ("Ito", 80), ("Watanabe", 90),
]

print("--- 元のデータ ---")  # タイトル
for i, (name, score) in enumerate(students):  # 表示する
    print(f"  [{i}] {name}: {score}点")  # 表示する

# --- 安定ソート（分布数えソート） ---
stable_result = counting_sort_by_score(students, 100)  # ソートする
print("\n--- 分布数えソート（安定） ---")  # タイトル
for i, (name, score) in enumerate(stable_result):  # 表示する
    print(f"  [{i}] {name}: {score}点")  # 表示する

# --- 不安定ソート（選択ソート） ---
unstable_result = selection_sort_by_score(students)  # ソートする
print("\n--- 選択ソート（不安定） ---")  # タイトル
for i, (name, score) in enumerate(unstable_result):  # 表示する
    print(f"  [{i}] {name}: {score}点")  # 表示する

# --- 安定性の比較 ---
print("\n--- 比較 ---")  # タイトル
for target in [80, 90]:  # 各点数で比較する
    stable_names = [n for n, s in stable_result if s == target]  # 安定ソートの順序
    unstable_names = [n for n, s in unstable_result if s == target]  # 不安定ソートの順序
    original_names = [n for n, s in students if s == target]  # 元の順序
    print(f"  {target}点 元の順序:       {original_names}")  # 表示する
    print(f"  {target}点 安定ソート後:   {stable_names} → {'保持' if stable_names == original_names else '崩れた'}")  # 表示する
    print(f"  {target}点 不安定ソート後: {unstable_names} → {'保持' if unstable_names == original_names else '崩れた'}")  # 表示する
```

### 課題7の解答例

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む

def counting_sort_int(data, max_val):
    """整数用の分布数えソート"""

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


# --- 計測 ---
random.seed(42)  # シードを固定する
size = 10000  # データサイズ
max_val = 999  # 値の範囲
data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する
trials = 3  # 計測回数

print(f"データサイズ: {size:,}、値の範囲: 0~{max_val}、計測回数: {trials}")  # 条件を表示する

# --- 分布数えソートの計測 ---
counting_times = []  # 計測結果リスト
for t in range(trials):  # 指定回数繰り返す
    arr_copy = data[:]  # コピーする
    start = time.time()  # 開始
    result_counting = counting_sort_int(arr_copy, max_val)  # ソートする
    elapsed = time.time() - start  # 経過時間
    counting_times.append(elapsed)  # 記録する
    print(f"  分布数えソート 試行{t + 1}: {elapsed:.6f}秒")  # 表示する

# --- sorted() の計測 ---
builtin_times = []  # 計測結果リスト
for t in range(trials):  # 指定回数繰り返す
    arr_copy = data[:]  # コピーする
    start = time.time()  # 開始
    result_builtin = sorted(arr_copy)  # ソートする
    elapsed = time.time() - start  # 経過時間
    builtin_times.append(elapsed)  # 記録する
    print(f"  sorted()       試行{t + 1}: {elapsed:.6f}秒")  # 表示する

# --- 結果を表示する ---
avg_counting = sum(counting_times) / trials  # 平均を計算する
avg_builtin = sum(builtin_times) / trials  # 平均を計算する
print(f"\n平均: 分布数えソート={avg_counting:.6f}秒, sorted()={avg_builtin:.6f}秒")  # 表示する

# --- 正しさを検証する ---
assert result_counting == result_builtin, "ソート結果が一致しません"  # 検証する
print("検証OK: 両方のソート結果が一致")  # メッセージ
```

### 課題8の解答例

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
    return output  # 結果を返す


def measure_avg_time(sort_func, data, trials=3):
    """平均実行時間を計測する"""

    times = []  # 結果リスト
    for _ in range(trials):  # 指定回数計測する
        arr = data[:]  # コピーする
        start = time.time()  # 開始
        sort_func(arr)  # ソートする
        times.append(time.time() - start)  # 記録する
    return sum(times) / len(times)  # 平均を返す


# --- ベンチマーク ---
random.seed(42)  # シードを固定する
sizes = [10000, 50000, 100000]  # データサイズ
max_val = 999  # 値の範囲

counting_times = []  # 分布数えソートの結果
builtin_times = []  # sorted() の結果

for size in sizes:  # 各サイズで計測する
    data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する
    ct = measure_avg_time(lambda d: counting_sort_bench(d, max_val), data)  # 分布数えソート
    bt = measure_avg_time(sorted, data)  # sorted()
    counting_times.append(ct)  # 記録する
    builtin_times.append(bt)  # 記録する
    print(f"サイズ {size:>7,}: 分布数え={ct:.4f}s, sorted()={bt:.4f}s")  # 表示する

# --- グラフを描画する ---
fig, ax = plt.subplots(figsize=(10, 6))  # 図を作成する
x_pos = range(len(sizes))  # X座標を設定する
bar_width = 0.35  # バーの幅

bars1 = ax.bar([x - bar_width / 2 for x in x_pos], counting_times, bar_width,
               label="分布数えソート", color="#3498db")  # バーを描画する
bars2 = ax.bar([x + bar_width / 2 for x in x_pos], builtin_times, bar_width,
               label="sorted()", color="#e74c3c")  # バーを描画する

for bar, t in zip(bars1, counting_times):  # 数値を表示する
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{t:.4f}s", ha="center", va="bottom", fontsize=9)  # バーの上に表示する
for bar, t in zip(bars2, builtin_times):  # 数値を表示する
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{t:.4f}s", ha="center", va="bottom", fontsize=9)  # バーの上に表示する

ax.set_xlabel("データサイズ", fontsize=13)  # X軸ラベル
ax.set_ylabel("平均実行時間（秒）", fontsize=13)  # Y軸ラベル
ax.set_title("分布数えソート vs sorted()（値の範囲: 0~999）", fontsize=14)  # タイトル
ax.set_xticks(list(x_pos))  # 目盛り位置
ax.set_xticklabels([f"{s:,}" for s in sizes])  # 目盛りラベル
ax.legend(fontsize=12)  # 凡例
ax.grid(axis="y", alpha=0.3)  # グリッド
plt.tight_layout()  # レイアウト調整
plt.show()  # 表示する
```

### 課題9の解答例

```python
def counting_sort_digit_trace(data, digit_pos):
    """桁ソートをトレース付きで実行する"""

    base = 10  # 10進数
    print(f"\n  --- {digit_pos}の位でソート ---")  # タイトル

    # --- 各要素の桁を表示する ---
    for value in data:  # 各要素を処理する
        digit = (value // digit_pos) % base  # 指定桁の数字を取り出す
        print(f"    {value} → {digit_pos}の位 = {digit}")  # 計算過程を表示する

    # --- 分布数えソート ---
    count = [0] * base  # 度数配列を初期化する
    for value in data:  # 度数を数える
        digit = (value // digit_pos) % base  # 桁を取り出す
        count[digit] += 1  # カウントを増やす
    print(f"  度数配列: {count}")  # 度数配列を表示する

    for i in range(1, base):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        digit = (data[i] // digit_pos) % base  # 桁を取り出す
        position = count[digit] - 1  # 位置を計算する
        output[position] = data[i]  # 配置する
        count[digit] -= 1  # カウントを減らす

    print(f"  ソート後: {output}")  # 結果を表示する
    return output  # ソート結果を返す


def radix_sort_trace(data):
    """基数ソートをトレース付きで実行する"""

    if len(data) <= 1:  # 要素が1以下なら
        return data[:]  # そのまま返す

    max_val = max(data)  # 最大値を求める
    result = data[:]  # コピーを作る
    digit_pos = 1  # 1の位からスタート

    print(f"入力: {data}")  # 入力を表示する
    print(f"最大値: {max_val}")  # 最大値を表示する

    while digit_pos <= max_val:  # 全桁を処理する
        result = counting_sort_digit_trace(result, digit_pos)  # 桁ソートを実行する
        digit_pos *= 10  # 次の桁へ

    return result  # 最終結果を返す


# --- 実行 ---
test = [329, 457, 657, 839, 436, 720, 355]  # テストデータ
sorted_result = radix_sort_trace(test)  # 基数ソートを実行する

print(f"\n最終結果: {sorted_result}")  # 最終結果を表示する
assert sorted_result == sorted(test), "結果が不正です"  # 検証する
print("検証OK: sorted() と一致")  # メッセージ
```

### 課題10の解答例

```python
import random  # 乱数モジュールを読み込む
import time  # 時間計測モジュールを読み込む

def counting_sort_by_digit_impl(data, digit_pos):
    """基数ソート内部の桁ソート"""

    base = 10  # 10進数
    count = [0] * base  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[(value // digit_pos) % base] += 1  # カウントを増やす

    for i in range(1, base):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        digit = (data[i] // digit_pos) % base  # 桁を取り出す
        output[count[digit] - 1] = data[i]  # 配置する
        count[digit] -= 1  # カウントを減らす

    return output  # ソート結果を返す


def radix_sort_impl(data):
    """基数ソートの完全実装"""

    if len(data) <= 1:  # 要素が1以下なら
        return data[:]  # そのまま返す

    max_val = max(data)  # 最大値を求める
    result = data[:]  # コピーを作る
    digit_pos = 1  # 1の位から開始する

    while digit_pos <= max_val:  # 全桁を処理する
        result = counting_sort_by_digit_impl(result, digit_pos)  # 桁ソートする
        digit_pos *= 10  # 次の桁へ

    return result  # 最終結果を返す


def counting_sort_direct(data, max_val):
    """直接の分布数えソート"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for value in data:  # 度数を数える
        count[value] += 1  # カウントを増やす
    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る
    output = [0] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        output[count[data[i]] - 1] = data[i]  # 配置する
        count[data[i]] -= 1  # カウントを減らす
    return output  # 結果を返す


# --- 正しさの検証 ---
random.seed(42)  # シードを固定する
size = 10000  # データサイズ
max_val = 99999  # 値の範囲
data = [random.randint(0, max_val) for _ in range(size)]  # データを生成する

result_radix = radix_sort_impl(data)  # 基数ソートを実行する
result_builtin = sorted(data)  # sorted() を実行する
assert result_radix == result_builtin, "基数ソートの結果が不正"  # 検証する
print(f"基数ソートの正しさ検証OK（{size}件、値の範囲 0~{max_val}）")  # メッセージ

# --- 性能比較 ---
print(f"\n{'アルゴリズム':>16} {'時間':>10}")  # ヘッダー
print("-" * 30)  # 区切り線

# 基数ソート
start = time.time()  # 開始
radix_sort_impl(data[:])  # 実行する
radix_time = time.time() - start  # 時間を計算する
print(f"{'基数ソート':>16} {radix_time:>9.4f}s")  # 表示する

# 分布数えソート
start = time.time()  # 開始
counting_sort_direct(data[:], max_val)  # 実行する
counting_time = time.time() - start  # 時間を計算する
print(f"{'分布数えソート':>16} {counting_time:>9.4f}s")  # 表示する

# sorted()
start = time.time()  # 開始
sorted(data[:])  # 実行する
builtin_time = time.time() - start  # 時間を計算する
print(f"{'sorted()':>16} {builtin_time:>9.4f}s")  # 表示する

# --- 考察 ---
print("\n【考察】")  # 考察タイトル
print(f"値の範囲が {max_val} の場合:")  # 条件を表示する
print(f"  分布数えソートは {max_val + 1} 個の配列を必要とする → メモリ使用量が大きい")  # 問題点
print(f"  基数ソートは 10 個の配列 x {len(str(max_val))} 桁 → メモリ効率が良い")  # 利点
print(f"  sorted() は比較ベースだが、高度に最適化されている")  # 参考
```

### 発展課題1の解答例

```python
import csv  # CSVモジュールを読み込む

def counting_sort_multi_key(data, key_func, max_val):
    """安定な分布数えソート（汎用キー関数版）"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for item in data:  # 度数を数える
        count[key_func(item)] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        key = key_func(data[i])  # キーを取得する
        position = count[key] - 1  # 位置を計算する
        output[position] = data[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # 結果を返す


# --- テストデータ ---
students = [  # (名前, クラス, 数学, 英語)
    ("Tanaka", 2, 85, 72),
    ("Sato", 1, 92, 88),
    ("Suzuki", 2, 78, 95),
    ("Yamada", 1, 85, 80),
    ("Ito", 3, 92, 67),
    ("Watanabe", 1, 78, 70),
    ("Nakamura", 3, 85, 90),
    ("Kobayashi", 2, 92, 85),
    ("Kato", 3, 78, 75),
    ("Yoshida", 1, 92, 60),
]

print("--- 元のデータ ---")  # タイトル
for s in students:  # 表示する
    print(f"  {s[0]:>12} クラス{s[1]} 数学{s[2]:>3} 英語{s[3]:>3}")  # 表示する

# --- ステップ1: 数学の点数で降順ソート（100 - score をキーにする） ---
step1 = counting_sort_multi_key(students, lambda s: 100 - s[2], 100)  # 降順ソート
print("\n--- ステップ1: 数学降順 ---")  # タイトル
for s in step1:  # 表示する
    print(f"  {s[0]:>12} クラス{s[1]} 数学{s[2]:>3} 英語{s[3]:>3}")  # 表示する

# --- ステップ2: クラスで昇順ソート（安定なので数学順は保たれる） ---
step2 = counting_sort_multi_key(step1, lambda s: s[1], 10)  # クラス昇順ソート
print("\n--- ステップ2: クラス昇順 → 数学降順（最終結果） ---")  # タイトル
for s in step2:  # 表示する
    print(f"  {s[0]:>12} クラス{s[1]} 数学{s[2]:>3} 英語{s[3]:>3}")  # 表示する

# --- CSVに書き出す ---
with open("multi_key_sorted.csv", "w", newline="", encoding="utf-8") as f:  # ファイルを開く
    writer = csv.writer(f)  # ライターを作成する
    writer.writerow(["name", "class", "math", "english"])  # ヘッダーを書く
    for s in step2:  # 各レコードを書き出す
        writer.writerow(s)  # 行を書く
print("\nCSVに保存しました: multi_key_sorted.csv")  # メッセージ
```

### 発展課題2の解答例

```python
def counting_sort_general(data, key_func, max_val):
    """汎用安定分布数えソート"""

    count = [0] * (max_val + 1)  # 度数配列を初期化する
    for item in data:  # 度数を数える
        count[key_func(item)] += 1  # カウントを増やす

    for i in range(1, len(count)):  # 累積度数を計算する
        count[i] += count[i - 1]  # 累積和を作る

    output = [None] * len(data)  # 出力配列を用意する
    for i in range(len(data) - 1, -1, -1):  # 末尾から配置する
        key = key_func(data[i])  # キーを取得する
        output[count[key] - 1] = data[i]  # 配置する
        count[key] -= 1  # カウントを減らす

    return output  # 結果を返す


# --- テストデータ ---
students = [  # (名前, 数学, 英語)
    ("Tanaka", 85, 72),
    ("Sato", 92, 88),
    ("Suzuki", 78, 95),
    ("Yamada", 85, 80),
    ("Ito", 92, 67),
    ("Watanabe", 78, 70),
    ("Nakamura", 85, 90),
    ("Kobayashi", 92, 85),
    ("Kato", 78, 75),
    ("Yoshida", 85, 60),
]

print("--- 元のデータ ---")  # タイトル
for s in students:  # 表示する
    print(f"  {s[0]:>12} 数学{s[1]:>3} 英語{s[2]:>3}")  # 表示する

# --- 3つのキーでソート（逆順に適用する） ---

# ステップ1: 名前昇順（名前の長さでソート、同じ長さはアルファベット順を保つ）
# 簡易的に名前の最初の文字のASCIIコードをキーにする
step1 = counting_sort_general(students, lambda s: ord(s[0][0]), 130)  # 名前でソートする
print("\n--- ステップ1: 名前昇順 ---")  # タイトル
for s in step1:  # 表示する
    print(f"  {s[0]:>12} 数学{s[1]:>3} 英語{s[2]:>3}")  # 表示する

# ステップ2: 英語降順（安定ソートなので名前順が保たれる）
step2 = counting_sort_general(step1, lambda s: 100 - s[2], 100)  # 英語降順
print("\n--- ステップ2: 英語降順 ---")  # タイトル
for s in step2:  # 表示する
    print(f"  {s[0]:>12} 数学{s[1]:>3} 英語{s[2]:>3}")  # 表示する

# ステップ3: 数学降順（安定ソートなので英語順・名前順が保たれる）
step3 = counting_sort_general(step2, lambda s: 100 - s[1], 100)  # 数学降順
print("\n--- ステップ3: 数学降順 → 英語降順 → 名前昇順（最終結果） ---")  # タイトル
for rank, s in enumerate(step3, 1):  # 順位付きで表示する
    print(f"  {rank:>2}位 {s[0]:>12} 数学{s[1]:>3} 英語{s[2]:>3}")  # 表示する
```

---

## 6. まとめ

| 項目 | 内容 |
|------|------|
| **CSVファイル** | `csv.reader` / `csv.writer` で読み書き |
| **安定ソート** | 同じ値の要素の元の順序を保つ |
| **安定が必要な場面** | 複数キーでソートする場合 |
| **基数ソート** | 各桁で安定な分布数えソートを繰り返す |
| **基数ソートの計算量** | O(d * (n + k)) --- d:桁数, n:要素数, k:基数 |

**ポイント:**
- 安定ソートは「同じ値のときの順序」を保証する重要な性質
- 分布数えソートは末尾から配置すれば安定、先頭からだと不安定
- 基数ソートは分布数えソートの安定性を利用した強力なアルゴリズム
- 実データでは CSV が最も一般的なデータ交換形式の一つ
