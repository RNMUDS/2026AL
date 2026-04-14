# 第15回: まとめ

> アルゴリズム論及び演習I ｜ 2026年度

---

## 説明: アルゴリズム総整理

この回では、全14回の学習内容を振り返り、学んだアルゴリズムの**特徴・計算量・適用場面**を体系的に整理する。後期（アルゴリズム論及び演習II）への橋渡しも行う。

### この授業で学んだアルゴリズム

| アルゴリズム | 計算量（平均） | 用途 | 学んだ回 |
|---|---|---|---|
| 逐次探索 | O(n) | 未整列データからの検索 | 第3回 |
| 二分探索 | O(log n) | ソート済みデータからの検索 | 第4回 |
| ハッシュ探索 | O(1) | キーから値を即座に取得 | 第6-7回 |
| 挿入ソート | O(n^2) | 小規模・ほぼ整列データのソート | 第8-9回 |
| バブルソート | O(n^2) | 教育目的・小規模データのソート | 第9回 |
| カウントソート | O(n+k) | 限定範囲の整数ソート | 第10-11回 |
| BFS（幅優先探索） | O(V+E) | 最短経路・迷路探索 | 第12回 |
| DFS（深さ優先探索） | O(V+E) | 全探索・連結判定 | 第12回 |

---

## 例題1: コードからアルゴリズムを特定する

コードを読んで、どのアルゴリズムかを判定する。

```python
# ===================================================
# 例題1: アルゴリズムの特定
# コードの特徴からアルゴリズム名を当てる
# ===================================================

def identify_algorithm():
    """コードの特徴からアルゴリズムを特定する関数"""

    # --- コードA ---
    print("【コードA】")                # セクションタイトルを出力する
    code_a = """
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    """
    print(code_a)                       # コードを表示する
    print("  特徴: 範囲を半分に絞り込む")  # 特徴を出力する
    print("  答え: 二分探索（Binary Search）")  # 答えを出力する
    print(f"  計算量: O(log n)")         # 計算量を出力する
    print()

    # --- コードB ---
    print("【コードB】")                # セクションタイトルを出力する
    code_b = """
    queue = deque([start])
    visited = {start}
    while queue:
        current = queue.popleft()
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    """
    print(code_b)                       # コードを表示する
    print("  特徴: キュー（deque）で先入れ先出し、近い順に探索")  # 特徴を出力する
    print("  答え: BFS（幅優先探索）")   # 答えを出力する
    print(f"  計算量: O(V+E)")           # 計算量を出力する
    print()

    # --- コードC ---
    print("【コードC】")                # セクションタイトルを出力する
    code_c = """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    """
    print(code_c)                       # コードを表示する
    print("  特徴: 1つずつ正しい位置に挿入していく")  # 特徴を出力する
    print("  答え: 挿入ソート（Insertion Sort）")  # 答えを出力する
    print(f"  計算量: O(n^2)、ほぼ整列時はO(n)")  # 計算量を出力する
    print()

    # --- 判定のキーワード一覧 ---
    print("=== アルゴリズム特定のキーワード ===")  # タイトルを出力する
    keywords = [                        # キーワードリストを定義する
        ("low, high, mid",              "二分探索"),
        ("deque, popleft, queue",       "BFS"),
        ("stack, pop (LIFO)",           "DFS"),
        ("key = arr[i], j = i-1",       "挿入ソート"),
        ("arr[j], arr[j+1] の交換",     "バブルソート"),
        ("count配列, 範囲k",            "カウントソート"),
        ("dict, hash, キー検索",        "ハッシュ探索"),
        ("for i in range(len(data))",   "逐次探索"),
    ]
    for keyword, algo_name in keywords:     # 各キーワードを出力する
        print(f"  {keyword:　<30} → {algo_name}")


identify_algorithm()  # アルゴリズム特定を実行する
```

---

## 例題2: 計算量を求める

コードを読んで、時間計算量をO記法で求める。

```python
# ===================================================
# 例題2: 計算量の分析
# コードのループ構造から計算量を求める
# ===================================================

import time  # 処理時間の計測に使う

def analyze_complexity():
    """計算量を分析して実測と比較する関数"""

    # --- パターン1: O(1) 定数時間 ---
    print("【パターン1: O(1)】")        # タイトルを出力する
    print("  data = [10, 20, 30]")      # コード例を出力する
    print("  value = data[0]  # インデックスアクセスは常に一定時間")
    print("  → ループなし = O(1)")      # 計算量を出力する
    print()

    # --- パターン2: O(n) 線形時間 ---
    print("【パターン2: O(n)】")        # タイトルを出力する
    print("  for i in range(n):  # nに比例するループ1つ")
    print("      total += data[i]")
    print("  → 1重ループ = O(n)")       # 計算量を出力する
    print()

    # --- パターン3: O(n^2) 二乗時間 ---
    print("【パターン3: O(n^2)】")      # タイトルを出力する
    print("  for i in range(n):  # 外側ループ: n回")
    print("      for j in range(n):  # 内側ループ: n回")
    print("          ...  # n * n = n^2回実行")
    print("  → 2重ループ = O(n^2)")     # 計算量を出力する
    print()

    # --- パターン4: O(log n) 対数時間 ---
    print("【パターン4: O(log n)】")    # タイトルを出力する
    print("  while n > 1:  # nを毎回半分にする")
    print("      n = n // 2")
    print("  → 半分にする回数 = O(log n)")  # 計算量を出力する
    print()

    # --- 実測で確認する ---
    print("=== 実測による確認 ===")     # タイトルを出力する
    sizes = [1000, 2000, 4000, 8000]    # テストサイズを定義する

    print(f"\n{'n':>6} | {'O(n)実測':>12} | {'O(n^2)実測':>12} | {'比率(n^2/n)':>12}")
    print("-" * 55)                     # 区切り線を出力する

    for n in sizes:                     # 各サイズでテストする
        data = list(range(n))           # テストデータを作る

        # O(n) の処理
        start_time = time.perf_counter()    # 計測開始する
        total = 0                           # 合計を初期化する
        for val in data:                    # 各要素をループする
            total += val                    # 合計に加算する
        time_n = time.perf_counter() - start_time  # O(n)の時間を計算する

        # O(n^2) の処理
        start_time = time.perf_counter()    # 計測開始する
        count = 0                           # カウンタを初期化する
        for i in range(n):                  # 外側ループ
            for j in range(n):              # 内側ループ
                count += 1                  # カウンタを増やす
        time_n2 = time.perf_counter() - start_time  # O(n^2)の時間を計算する

        ratio = time_n2 / time_n if time_n > 0 else 0  # 比率を計算する
        print(f"{n:>6} | {time_n:>10.6f}秒 | {time_n2:>10.4f}秒 | {ratio:>10.0f}倍")

    print("\n※ nが2倍になると、O(n)は約2倍、O(n^2)は約4倍になることを確認しよう")


analyze_complexity()  # 計算量分析を実行する
```

**実行結果の例**:
```
【パターン1: O(1)】
  ...

=== 実測による確認 ===

     n |     O(n)実測 |   O(n^2)実測 |  比率(n^2/n)
-------------------------------------------------------
  1000 |   0.000045秒 |     0.0312秒 |        693倍
  2000 |   0.000089秒 |     0.1248秒 |       1402倍
  4000 |   0.000178秒 |     0.4996秒 |       2807倍
  8000 |   0.000356秒 |     1.9984秒 |       5614倍
```

---

## 例題3: 場面に最適なアルゴリズムを選ぶ

問題の特徴を分析し、最適なアルゴリズムを選択する。

```python
# ===================================================
# 例題3: アルゴリズムの選択
# 問題の特徴に基づいて最適なアルゴリズムを選ぶ
# ===================================================

def select_algorithm():
    """場面ごとに最適なアルゴリズムを選択する関数"""

    scenarios = [                   # シナリオリストを定義する
        {
            "question": "1000人のソート済み名簿から名前を探す",
            "analysis": "データがソート済み → 二分探索が使える",
            "answer": "二分探索 O(log n) → 最大10回の比較で見つかる",
            "why_not": "逐次探索O(n)は平均500回 → 50倍遅い",
        },
        {
            "question": "ユーザーIDから情報を即座に取得する",
            "analysis": "キー→値の取得 → ハッシュテーブルの典型",
            "answer": "ハッシュ探索(辞書) O(1)",
            "why_not": "二分探索O(log n)も速いが、ハッシュのO(1)が最速",
        },
        {
            "question": "10万人の点数(0-100)をソートする",
            "analysis": "整数 + 範囲限定(k=101) + 大量データ",
            "answer": "カウントソート O(n+k) = O(100101)",
            "why_not": "挿入ソートO(n^2) = O(10^10)は遅すぎる",
        },
        {
            "question": "迷路でスタートからゴールへの最短経路を求める",
            "analysis": "グラフの最短経路問題",
            "answer": "BFS O(V+E) → 最短経路を保証する",
            "why_not": "DFSは経路を見つけるが最短とは限らない",
        },
    ]

    print("=== アルゴリズム選択ガイド ===")  # タイトルを出力する
    for i, scenario in enumerate(scenarios, 1):     # 各シナリオを処理する
        print(f"\n--- シナリオ{i} ---")              # シナリオ番号を出力する
        print(f"  問題: {scenario['question']}")     # 問題を出力する
        print(f"  分析: {scenario['analysis']}")     # 分析を出力する
        print(f"  最適: {scenario['answer']}")       # 最適解を出力する
        print(f"  他が不適切な理由: {scenario['why_not']}")  # 理由を出力する

    # --- 選択フローチャート ---
    print("\n=== 選択フローチャート ===")  # タイトルを出力する
    print("  探索問題？")                  # フロー開始
    print("  ├─ ソート済み？ → 二分探索")
    print("  ├─ キー→値？ → ハッシュ探索")
    print("  ├─ グラフ最短経路？ → BFS")
    print("  └─ その他 → 逐次探索")
    print()
    print("  ソート問題？")
    print("  ├─ 値の範囲が限定？ → カウントソート")
    print("  ├─ ほぼ整列？ → 挿入ソート")
    print("  └─ 小規模？ → 挿入ソート")


select_algorithm()  # アルゴリズム選択を実行する
```

---

## 例題4: 同じ問題を2つのアルゴリズムで解く

同じ問題を異なるアルゴリズムで解き、性能を比較する。

```python
# ===================================================
# 例題4: 2つのアプローチの比較
# 「リスト内の重複要素を見つける」問題を2通りで解く
# ===================================================

import time  # 処理時間の計測に使う

def find_duplicates_bruteforce(data):
    """重複要素を見つける（総当たり版 O(n^2)）"""
    duplicates = []             # 重複リストを初期化する
    length = len(data)          # データの長さを取得する
    for i in range(length):     # 外側ループ: 各要素を基準にする
        for j in range(i + 1, length):  # 内側ループ: 基準より後ろと比較
            if data[i] == data[j] and data[i] not in duplicates:  # 重複発見
                duplicates.append(data[i])  # 重複リストに追加する
    return duplicates            # 重複リストを返す


def find_duplicates_hashset(data):
    """重複要素を見つける（ハッシュセット版 O(n)）"""
    seen = set()                # 見た要素を記録するセットを作る
    duplicates = set()          # 重複要素を記録するセットを作る
    for item in data:           # 各要素をループする
        if item in seen:        # 既に見た要素の場合
            duplicates.add(item)    # 重複セットに追加する
        else:                   # 初めて見る要素の場合
            seen.add(item)      # 見た要素に追加する
    return list(duplicates)     # 重複リストに変換して返す


# --- 正しさの確認 ---
print("=== 2つのアプローチ比較 ===")    # タイトルを出力する
test_data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]  # テストデータを定義する
print(f"データ: {test_data}")            # テストデータを出力する
print(f"総当たり版: {find_duplicates_bruteforce(test_data)}")  # 総当たりの結果
print(f"ハッシュ版: {find_duplicates_hashset(test_data)}")    # ハッシュの結果

# --- 速度の比較 ---
print(f"\n--- 速度比較 ---")             # セクションタイトルを出力する
print(f"{'n':>8} | {'総当たりO(n^2)':>14} | {'ハッシュO(n)':>14} | {'速度比':>8}")
print("-" * 55)                          # 区切り線を出力する

import random  # ランダムデータ生成に使う

for n in [500, 1000, 2000, 5000]:       # 各サイズでテストする
    data = [random.randint(1, n // 2) for _ in range(n)]  # 重複を含むデータを生成する

    start_time = time.perf_counter()            # 総当たり版の計測を開始する
    find_duplicates_bruteforce(data)             # 総当たり版を実行する
    brute_time = time.perf_counter() - start_time  # 時間を計算する

    start_time = time.perf_counter()            # ハッシュ版の計測を開始する
    find_duplicates_hashset(data)                # ハッシュ版を実行する
    hash_time = time.perf_counter() - start_time   # 時間を計算する

    ratio = brute_time / hash_time if hash_time > 0 else 0  # 速度比を計算する
    print(f"{n:>8} | {brute_time:>12.6f}秒 | {hash_time:>12.6f}秒 | {ratio:>6.0f}倍")
```

---

## 例題5: 実世界の問題にアルゴリズムを適用する

実世界の問題をアルゴリズムで解く設計を行う。

```python
# ===================================================
# 例題5: 実世界の問題への適用
# 「図書館の蔵書検索システム」を設計・実装する
# ===================================================

def build_library_system():
    """図書館の蔵書検索システムを構築する関数"""

    # --- 蔵書データ（辞書のリスト） ---
    books = [                       # 蔵書データを定義する
        {"id": 1, "title": "Python入門",     "author": "田中太郎", "year": 2024},
        {"id": 2, "title": "アルゴリズム基礎", "author": "鈴木花子", "year": 2023},
        {"id": 3, "title": "データ構造入門",  "author": "田中太郎", "year": 2025},
        {"id": 4, "title": "AI概論",          "author": "佐藤次郎", "year": 2024},
        {"id": 5, "title": "Web開発入門",     "author": "鈴木花子", "year": 2025},
        {"id": 6, "title": "機械学習実践",    "author": "佐藤次郎", "year": 2023},
        {"id": 7, "title": "Python応用",      "author": "田中太郎", "year": 2025},
        {"id": 8, "title": "ネットワーク基礎", "author": "高橋三郎", "year": 2024},
    ]

    # --- ハッシュテーブルでIDから即座に検索（O(1)） ---
    id_index = {}                   # ID検索用のインデックスを作る
    for book in books:              # 各書籍をインデックスに登録する
        id_index[book["id"]] = book     # IDをキーに登録する

    # --- 著者名で検索（ハッシュテーブル） ---
    author_index = {}               # 著者検索用のインデックスを作る
    for book in books:              # 各書籍を著者別に登録する
        author = book["author"]     # 著者名を取り出す
        if author not in author_index:  # 著者がまだ登録されていない場合
            author_index[author] = []   # 空のリストを作る
        author_index[author].append(book)  # 書籍を追加する

    # --- 出版年でソート（挿入ソート） ---
    sorted_books = books[:]         # コピーを作る
    for i in range(1, len(sorted_books)):   # 2番目から開始する
        key = sorted_books[i]       # 今回挿入する書籍を保存する
        j = i - 1                   # 比較位置を設定する
        while j >= 0 and sorted_books[j]["year"] > key["year"]:  # 年が大きい間
            sorted_books[j + 1] = sorted_books[j]  # 右にずらす
            j -= 1                  # 比較位置を左に移動する
        sorted_books[j + 1] = key   # 正しい位置に挿入する

    # --- システムのデモ ---
    print("=== 図書館蔵書検索システム ===")  # タイトルを出力する

    # ID検索（ハッシュ探索 O(1)）
    print("\n【1. ID検索（ハッシュ探索）】")  # セクションタイトル
    target_id = 3                   # 検索するIDを設定する
    if target_id in id_index:       # IDが存在する場合
        book = id_index[target_id]  # 書籍を取得する
        print(f"  ID={target_id}: {book['title']} ({book['author']}, {book['year']})")

    # 著者検索（ハッシュ探索 O(1)）
    print("\n【2. 著者検索（ハッシュ探索）】")
    target_author = "田中太郎"      # 検索する著者を設定する
    if target_author in author_index:   # 著者が存在する場合
        print(f"  {target_author}の著書:")     # 著者名を出力する
        for book in author_index[target_author]:   # 各著書を出力する
            print(f"    - {book['title']} ({book['year']})")

    # ソート済み一覧（挿入ソート結果）
    print("\n【3. 出版年順一覧（挿入ソート）】")
    for book in sorted_books:       # ソート済みリストを出力する
        print(f"  {book['year']} | {book['title']} | {book['author']}")

    # 使ったアルゴリズムのまとめ
    print("\n【使ったアルゴリズム】")    # まとめを出力する
    print("  1. ハッシュ探索 → ID検索 O(1), 著者検索 O(1)")
    print("  2. 挿入ソート → 出版年順の整列 O(n^2)")
    print("  ※ 蔵書が増えたら二分探索やカウントソートも検討")


build_library_system()  # 蔵書検索システムを実行する
```

---

## 標準課題

### 標準課題1（超やさしい）: コードからアルゴリズム名を答える

以下の3つのコードを読み、各コードが何のアルゴリズムかを答えなさい。

```python
# ===================================================
# 課題1: アルゴリズム名を答える
# 各コードのアルゴリズム名と計算量を答えなさい
# ===================================================

# コード1
def algo_1(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

# コード2
def algo_2(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# コード3
def algo_3(data, target):
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# 各コードについて以下を答えなさい:
# アルゴリズム名:
# 計算量:
# 判断の根拠:
```

---

### 標準課題2（超やさしい）: 説明文からアルゴリズム名を答える

以下の5つの説明文が表すアルゴリズムを答えなさい。

```python
# ===================================================
# 課題2: 説明からアルゴリズムを特定する
# ===================================================

descriptions = [
    "探索範囲を毎回半分に絞り込む。ソート済みデータが前提。",
    "キューを使い、近い場所から順に探索する。最短経路を保証する。",
    "各要素の出現回数を数えて、その情報からソート結果を生成する。比較しない。",
    "キーからハッシュ値を計算し、配列の特定位置に格納する。検索はO(1)。",
    "1つずつ正しい位置に挿入していく。ほぼ整列済みのデータに強い。",
]

# 各説明について答えなさい:
# 1.
# 2.
# 3.
# 4.
# 5.
```

---

### 標準課題3（やさしい）: ループ構造から計算量を求める

以下の4つのコードの時間計算量をO記法で答えなさい。

```python
# ===================================================
# 課題3: 計算量を求める
# ===================================================

# コード1
def func_a(n):
    total = 0
    for i in range(n):
        total += i
    return total

# コード2
def func_b(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i + j
    return total

# コード3
def func_c(n):
    count = 0
    value = n
    while value > 1:
        value = value // 2
        count += 1
    return count

# コード4
def func_d(data):
    result = {}
    for item in data:
        if item not in result:
            result[item] = 0
        result[item] += 1
    return result

# 各コードの計算量を答えなさい:
# func_a: O(?)
# func_b: O(?)
# func_c: O(?)
# func_d: O(?)
```

---

### 標準課題4（やさしい）: 実測で計算量を確認する

課題3のfunc_aとfunc_bを実際に実行し、nを1000、2000、4000、8000と変化させたときの実行時間を測定して表にまとめなさい。nが2倍になったとき時間が何倍になるか確認すること。

```python
# ===================================================
# 課題4: 実測で計算量を確認する
# func_aとfunc_bの実行時間をn=1000,2000,4000,8000で測定する
# ===================================================

import time

# ヘッダー: n | func_a時間 | func_b時間 | func_a比率 | func_b比率
# ここに実装しなさい
```

---

### 標準課題5（やややさしい）: 最適なアルゴリズムを選ぶ

以下のシナリオで最適なアルゴリズムを選び、理由を説明しなさい。

```python
# ===================================================
# 課題5: アルゴリズムの選択
# ===================================================

scenarios = [
    "シナリオ1: 50人の学生の点数(0-100)をソートしたい",
    "シナリオ2: 辞書（10万語）から単語の意味を検索したい",
    "シナリオ3: 迷路のスタートからゴールへの最短経路を求めたい",
]

# 各シナリオについて以下を答えなさい:
# 最適なアルゴリズム:
# 理由:
# 他が不適切な理由:
```

---

### 標準課題6（やややさしい）: 不適切なアルゴリズム選択を指摘する

以下のコードでは不適切なアルゴリズムが使われている。何が問題か指摘し、適切なアルゴリズムに書き換えなさい。

```python
# ===================================================
# 課題6: 不適切なアルゴリズムの指摘と修正
# ===================================================

# 問題: ソート済みの10万件のデータから値を検索する
# → 逐次探索を使っている（不適切！）
def search_in_sorted(sorted_data, target):
    """ソート済みデータから検索する（非効率版）"""
    for i in range(len(sorted_data)):
        if sorted_data[i] == target:
            return i
    return -1

# これを適切なアルゴリズムに書き換えなさい
```

---

### 標準課題7（やや普通）: 同じ問題を2通りで解く

「リストの中で最も頻繁に出現する要素を見つける」問題を、(1)ソートしてから数える方法と、(2)辞書で数える方法の2通りで解きなさい。

```python
# ===================================================
# 課題7: 2通りのアプローチで解く
# ===================================================

# 方法1: ソートしてから数える
def most_frequent_sort(data):
    """最頻出要素をソートで求める関数"""
    # ここに実装しなさい
    pass

# 方法2: 辞書で数える
def most_frequent_dict(data):
    """最頻出要素を辞書で求める関数"""
    # ここに実装しなさい
    pass
```

---

### 標準課題8（やや普通）: 2つのアプローチを速度比較する

課題7の2つの方法の実行時間を、データサイズ1000、5000、10000、50000で測定して比較しなさい。どちらが速いか、なぜ速いかを説明すること。

```python
# ===================================================
# 課題8: 速度比較と考察
# 2つのアプローチの速度を測定し、理由を説明する
# ===================================================

import time
import random

# 速度比較を実行し、結果を表形式で出力しなさい
# さらに、なぜ一方が速いかを説明するコメントを書きなさい
```

---

### 標準課題9（普通）: 実問題の解決策を設計する

「オンラインショップの商品管理システム」を設計しなさい。以下の機能を実装すること。
- 商品IDで即座に検索できる
- 価格順に並べ替えられる
- 在庫切れ商品を除外できる

```python
# ===================================================
# 課題9: 商品管理システムの設計と実装
# ===================================================

# 使うアルゴリズムを選択し、各機能を実装しなさい
# 各機能でどのアルゴリズムを使ったか、なぜそれを選んだかを
# コメントで説明すること
```

---

### 標準課題10（普通）: アルゴリズム選択の総合問題

以下の複合的な問題を解きなさい。迷路とアイテム収集を組み合わせ、さらに収集したアイテムの価値を最大化する戦略も考慮すること。全体の計算量を分析し、各ステップでどのアルゴリズム・データ構造を使ったか説明すること。

```python
# ===================================================
# 課題10: 複合問題 - 価値最大化アイテム収集
# ===================================================

# 迷路の中にアイテムがあり、各アイテムには「価値」がある。
# 制限歩数以内で集められるアイテムの価値の合計を最大化したい。
#
# 入力:
#   - 迷路（2次元リスト）
#   - スタート位置
#   - アイテム情報: {位置: 価値} の辞書
#   - 制限歩数
#
# 出力:
#   - 最適な経路と集めたアイテムの合計価値
#
# ヒント:
#   1. BFSで各アイテム間の最短距離を求める
#   2. 制限歩数以内の組み合わせを探索する
#   3. 使ったアルゴリズムと計算量を説明する
```

---

## 発展課題

### 発展課題1: AL2プレビュー実装

後期で学ぶクイックソートを、AL1の知識（分割・再帰の概念）を使って実装しなさい。挿入ソートと速度を比較すること。

```python
# ===================================================
# 発展課題1: クイックソートのプレビュー実装
# ===================================================

# ヒント:
# 1. ピボット（基準値）を選ぶ
# 2. ピボットより小さいグループと大きいグループに分ける
# 3. 各グループを再帰的にソートする
# 4. 結合する
```

---

### 発展課題2: オリジナルアルゴリズムの設計

授業で学んだアルゴリズムを組み合わせて、オリジナルの問題解決プログラムを設計・実装しなさい。使ったアルゴリズムの一覧、各アルゴリズムを選んだ理由、全体の計算量を説明すること。

---

## 解答例

### 課題1 解答例

```python
# ===================================================
# 課題1 解答例: アルゴリズム名の特定
# ===================================================

print("=== 課題1: アルゴリズム名 ===")  # タイトルを出力する

# コード1の解答
print("\n【コード1】")                   # セクションタイトルを出力する
print("  アルゴリズム名: 逐次探索（Linear Search）")  # 名前を出力する
print("  計算量: O(n)")                  # 計算量を出力する
print("  根拠: 先頭から順番に1つずつ比較している")  # 根拠を出力する

# コード2の解答
print("\n【コード2】")                   # セクションタイトルを出力する
print("  アルゴリズム名: バブルソート（Bubble Sort）")  # 名前を出力する
print("  計算量: O(n^2)")               # 計算量を出力する
print("  根拠: 2重ループで隣り合う要素を比較・交換している")  # 根拠を出力する

# コード3の解答
print("\n【コード3】")                   # セクションタイトルを出力する
print("  アルゴリズム名: 二分探索（Binary Search）")  # 名前を出力する
print("  計算量: O(log n)")             # 計算量を出力する
print("  根拠: low/high/midで範囲を半分に絞っている")  # 根拠を出力する
```

---

### 課題2 解答例

```python
# ===================================================
# 課題2 解答例: 説明からアルゴリズムを特定
# ===================================================

print("=== 課題2: 説明から特定 ===")    # タイトルを出力する

answers = [                             # 答えリストを定義する
    ("探索範囲を半分に絞り込む",         "二分探索（Binary Search）"),
    ("キューで近い順に探索",             "BFS（幅優先探索）"),
    ("出現回数を数えてソート",           "カウントソート（Counting Sort）"),
    ("ハッシュ値で特定位置に格納",       "ハッシュ探索（Hash Search）"),
    ("1つずつ正しい位置に挿入",          "挿入ソート（Insertion Sort）"),
]

for i, (desc, name) in enumerate(answers, 1):  # 各答えを出力する
    print(f"  {i}. {desc} → {name}")    # 説明と答えを出力する
```

---

### 課題3 解答例

```python
# ===================================================
# 課題3 解答例: 計算量の分析
# ===================================================

print("=== 課題3: 計算量 ===")  # タイトルを出力する

print("\nfunc_a: O(n)")          # func_aの計算量を出力する
print("  理由: 1重ループでnに比例")  # 理由を出力する

print("\nfunc_b: O(n^2)")        # func_bの計算量を出力する
print("  理由: 2重ループでn*nに比例")  # 理由を出力する

print("\nfunc_c: O(log n)")      # func_cの計算量を出力する
print("  理由: 毎回半分にするので、log2(n)回で終了")  # 理由を出力する

print("\nfunc_d: O(n)")          # func_dの計算量を出力する
print("  理由: 1重ループ + 辞書操作O(1) = O(n)")  # 理由を出力する
```

---

### 課題4 解答例

```python
# ===================================================
# 課題4 解答例: 実測で計算量を確認
# ===================================================

import time  # 処理時間の計測に使う

def func_a(n):
    """O(n)の処理"""
    total = 0                   # 合計を初期化する
    for i in range(n):          # n回ループする
        total += i              # 合計に加算する
    return total                # 合計を返す

def func_b(n):
    """O(n^2)の処理"""
    total = 0                   # 合計を初期化する
    for i in range(n):          # 外側ループ: n回
        for j in range(n):      # 内側ループ: n回
            total += i + j      # 合計に加算する
    return total                # 合計を返す

print("=== 課題4: 実測結果 ===")    # タイトルを出力する
print()
print(f"{'n':>6} | {'func_a':>10} | {'func_b':>10} | {'a倍率':>6} | {'b倍率':>6}")
print("-" * 55)                     # 区切り線を出力する

prev_a = None               # 前回のfunc_a時間を初期化する
prev_b = None               # 前回のfunc_b時間を初期化する

for n in [1000, 2000, 4000, 8000]:  # 各サイズでテストする
    start_time = time.perf_counter()    # func_aの計測を開始する
    func_a(n)                           # func_aを実行する
    time_a = time.perf_counter() - start_time  # 時間を計算する

    start_time = time.perf_counter()    # func_bの計測を開始する
    func_b(n)                           # func_bを実行する
    time_b = time.perf_counter() - start_time  # 時間を計算する

    ratio_a = time_a / prev_a if prev_a else 0  # func_aの倍率を計算する
    ratio_b = time_b / prev_b if prev_b else 0  # func_bの倍率を計算する

    a_str = f"{ratio_a:.1f}x" if prev_a else "-"    # 倍率文字列を作る
    b_str = f"{ratio_b:.1f}x" if prev_b else "-"    # 倍率文字列を作る

    print(f"{n:>6} | {time_a:>8.6f}秒 | {time_b:>8.4f}秒 | {a_str:>6} | {b_str:>6}")

    prev_a = time_a             # 前回の時間を更新する
    prev_b = time_b             # 前回の時間を更新する

print("\n※ O(n)はnが2倍で約2倍、O(n^2)はnが2倍で約4倍になる")
```

---

### 課題5 解答例

```python
# ===================================================
# 課題5 解答例: アルゴリズムの選択
# ===================================================

print("=== 課題5: アルゴリズム選択 ===")  # タイトルを出力する

print("\n【シナリオ1: 50人の点数(0-100)をソート】")  # シナリオ1
print("  最適: カウントソート O(n+k)")    # 最適解を出力する
print("  理由: 整数 + 範囲限定(k=101) + 安定ソート")  # 理由を出力する
print("  他が不適切: 挿入ソートO(n^2)も50人なら実用的だが")
print("            カウントソートの方が確実に速い")

print("\n【シナリオ2: 辞書10万語から検索】")  # シナリオ2
print("  最適: ハッシュ探索(辞書) O(1)")  # 最適解を出力する
print("  理由: キー→値の取得はハッシュテーブルが最速")
print("  他が不適切: 逐次探索O(n)は10万回の比較が必要")

print("\n【シナリオ3: 迷路の最短経路】")   # シナリオ3
print("  最適: BFS O(V+E)")               # 最適解を出力する
print("  理由: 近い場所から探索するので最短経路を保証")
print("  他が不適切: DFSは最短を保証しない")
```

---

### 課題6 解答例

```python
# ===================================================
# 課題6 解答例: 不適切なアルゴリズムの修正
# ===================================================

import time  # 処理時間の計測に使う

# 問題点: ソート済みデータに逐次探索を使っている
# → ソート済みなら二分探索を使うべき（O(n) → O(log n)）

def search_linear(sorted_data, target):
    """逐次探索（不適切版）"""
    for i in range(len(sorted_data)):   # 先頭から順に探す
        if sorted_data[i] == target:    # 一致した場合
            return i                    # インデックスを返す
    return -1                           # 見つからなかった場合


def search_binary(sorted_data, target):
    """二分探索（適切版）"""
    low = 0                         # 下限を設定する
    high = len(sorted_data) - 1     # 上限を設定する
    while low <= high:              # 範囲が有効な間繰り返す
        mid = (low + high) // 2     # 中央を計算する
        if sorted_data[mid] == target:      # 一致した場合
            return mid                      # インデックスを返す
        elif sorted_data[mid] < target:     # 中央が小さい場合
            low = mid + 1                   # 下限を更新する
        else:                               # 中央が大きい場合
            high = mid - 1                  # 上限を更新する
    return -1                       # 見つからなかった場合


# 速度比較
data = list(range(100000))          # 10万件のソート済みデータを作る
target = 99999                      # 最後の要素を探す（最悪ケース）

start_time = time.perf_counter()            # 逐次探索の計測を開始する
search_linear(data, target)                 # 逐次探索を実行する
linear_time = time.perf_counter() - start_time

start_time = time.perf_counter()            # 二分探索の計測を開始する
search_binary(data, target)                 # 二分探索を実行する
binary_time = time.perf_counter() - start_time

print("=== 課題6: アルゴリズム修正 ===")  # タイトルを出力する
print(f"  逐次探索: {linear_time:.6f}秒")  # 逐次探索の時間を出力する
print(f"  二分探索: {binary_time:.6f}秒")  # 二分探索の時間を出力する
ratio = linear_time / binary_time if binary_time > 0 else 0
print(f"  速度差: {ratio:.0f}倍")           # 速度比を出力する
print(f"\n  指摘: ソート済みデータに逐次探索O(n)は無駄。二分探索O(log n)を使うべき。")
```

---

### 課題7 解答例

```python
# ===================================================
# 課題7 解答例: 2通りのアプローチ
# ===================================================

def most_frequent_sort(data):
    """最頻出要素をソートで求める関数"""
    if not data:                    # 空リストの場合
        return None                 # Noneを返す

    # 挿入ソートでソートする
    sorted_data = data[:]           # コピーを作る
    for i in range(1, len(sorted_data)):    # 2番目から開始する
        key = sorted_data[i]        # 今回挿入する値を保存する
        j = i - 1                   # 比較位置を設定する
        while j >= 0 and sorted_data[j] > key:  # 左隣が大きい間
            sorted_data[j + 1] = sorted_data[j]  # 右にずらす
            j -= 1                  # 比較位置を左に移動する
        sorted_data[j + 1] = key    # 正しい位置に挿入する

    # ソート済みデータで連続する同じ値を数える
    best_value = sorted_data[0]     # 最頻出候補を初期化する
    best_count = 1                  # 最頻出の回数を初期化する
    current_count = 1               # 現在の連続回数を初期化する

    for i in range(1, len(sorted_data)):    # 2番目から順に調べる
        if sorted_data[i] == sorted_data[i - 1]:   # 前と同じ値の場合
            current_count += 1      # 連続回数を増やす
        else:                       # 違う値の場合
            current_count = 1       # 連続回数をリセットする

        if current_count > best_count:  # 過去最多を超えた場合
            best_count = current_count  # 最多回数を更新する
            best_value = sorted_data[i]  # 最頻出値を更新する

    return best_value               # 最頻出要素を返す


def most_frequent_dict(data):
    """最頻出要素を辞書で求める関数"""
    if not data:                    # 空リストの場合
        return None                 # Noneを返す

    counts = {}                     # 出現回数を記録する辞書を作る
    for item in data:               # 各要素をループする
        if item not in counts:      # 初めて見る要素の場合
            counts[item] = 0        # カウンタを0で初期化する
        counts[item] += 1           # カウンタを増やす

    best_value = None               # 最頻出候補を初期化する
    best_count = 0                  # 最頻出の回数を初期化する
    for value, count in counts.items():  # 辞書の全ペアを確認する
        if count > best_count:      # 過去最多を超えた場合
            best_count = count      # 最多回数を更新する
            best_value = value      # 最頻出値を更新する

    return best_value               # 最頻出要素を返す


# テスト
test_data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]  # テストデータを定義する
print("=== 課題7: 2通りのアプローチ ===")  # タイトルを出力する
print(f"データ: {test_data}")               # データを出力する
print(f"ソート版: {most_frequent_sort(test_data)}")  # ソート版の結果
print(f"辞書版:  {most_frequent_dict(test_data)}")  # 辞書版の結果
```

---

### 課題8 解答例

```python
# ===================================================
# 課題8 解答例: 速度比較と考察
# ===================================================

import time    # 処理時間の計測に使う
import random  # ランダムデータ生成に使う

# most_frequent_sort と most_frequent_dict は課題7の解答と同じ

print("=== 課題8: 速度比較 ===")    # タイトルを出力する
print()
print(f"{'n':>8} | {'ソート版':>12} | {'辞書版':>12} | {'速度比':>8}")
print("-" * 50)                     # 区切り線を出力する

for n in [1000, 5000, 10000, 50000]:    # 各サイズでテストする
    data = [random.randint(1, n // 5) for _ in range(n)]  # ランダムデータを生成する

    start_time = time.perf_counter()        # ソート版の計測を開始する
    most_frequent_sort(data)                # ソート版を実行する
    sort_time = time.perf_counter() - start_time  # 時間を計算する

    start_time = time.perf_counter()        # 辞書版の計測を開始する
    most_frequent_dict(data)                # 辞書版を実行する
    dict_time = time.perf_counter() - start_time  # 時間を計算する

    ratio = sort_time / dict_time if dict_time > 0 else 0  # 速度比を計算する
    print(f"{n:>8} | {sort_time:>10.6f}秒 | {dict_time:>10.6f}秒 | {ratio:>6.0f}倍")

print("\n【考察】")                  # 考察セクションを出力する
print("  ソート版: O(n^2)（挿入ソート）+ O(n)（走査）= O(n^2)")
print("  辞書版:  O(n)（辞書構築）+ O(n)（最大値検索）= O(n)")
print("  → 辞書版が速い理由: ソートのO(n^2)が不要だから")
print("  → nが大きくなるほど差が広がる")
```

---

### 課題9 解答例

```python
# ===================================================
# 課題9 解答例: 商品管理システム
# ===================================================

def build_shop_system():
    """商品管理システムを構築する関数"""

    # --- 商品データ ---
    products = [                    # 商品データを定義する
        {"id": 101, "name": "ノートPC",    "price": 89000, "stock": 5},
        {"id": 102, "name": "マウス",       "price": 2500,  "stock": 20},
        {"id": 103, "name": "キーボード",   "price": 6800,  "stock": 0},
        {"id": 104, "name": "モニター",     "price": 35000, "stock": 8},
        {"id": 105, "name": "USBメモリ",    "price": 1200,  "stock": 50},
        {"id": 106, "name": "ヘッドホン",   "price": 12000, "stock": 0},
        {"id": 107, "name": "Webカメラ",    "price": 4500,  "stock": 15},
    ]

    # --- 機能1: IDで即座に検索（ハッシュ探索 O(1)） ---
    id_index = {}                   # ID検索用のインデックスを作る
    for product in products:        # 各商品をインデックスに登録する
        id_index[product["id"]] = product  # IDをキーに登録する

    # --- 機能2: 価格順にソート（挿入ソート O(n^2)） ---
    sorted_by_price = products[:]   # コピーを作る
    for i in range(1, len(sorted_by_price)):    # 2番目から開始する
        key = sorted_by_price[i]    # 今回挿入する商品を保存する
        j = i - 1                   # 比較位置を設定する
        while j >= 0 and sorted_by_price[j]["price"] > key["price"]:
            sorted_by_price[j + 1] = sorted_by_price[j]  # 右にずらす
            j -= 1                  # 比較位置を左に移動する
        sorted_by_price[j + 1] = key    # 正しい位置に挿入する

    # --- 機能3: 在庫切れ除外（逐次探索 O(n)） ---
    in_stock = []                   # 在庫あり商品リストを初期化する
    for product in products:        # 各商品を確認する
        if product["stock"] > 0:    # 在庫がある場合
            in_stock.append(product)    # リストに追加する

    # --- デモ ---
    print("=== 商品管理システム ===")    # タイトルを出力する

    print("\n【機能1: ID検索（ハッシュ探索 O(1)）】")
    target_id = 104                 # 検索するIDを設定する
    if target_id in id_index:       # IDが存在する場合
        p = id_index[target_id]     # 商品を取得する
        print(f"  ID={target_id}: {p['name']} ¥{p['price']:,} (在庫{p['stock']})")

    print("\n【機能2: 価格順一覧（挿入ソート O(n^2)）】")
    for p in sorted_by_price:       # 価格順に出力する
        print(f"  ¥{p['price']:>6,} | {p['name']}")

    print("\n【機能3: 在庫あり商品（逐次探索 O(n)）】")
    for p in in_stock:              # 在庫あり商品を出力する
        print(f"  {p['name']} (在庫{p['stock']}個)")

    print(f"\n  全商品: {len(products)}件")      # 全商品数を出力する
    print(f"  在庫あり: {len(in_stock)}件")      # 在庫あり数を出力する
    print(f"  在庫切れ: {len(products) - len(in_stock)}件")  # 在庫切れ数を出力する

    print("\n【使ったアルゴリズム】")
    print("  1. ハッシュ探索 → ID検索 O(1): 大量商品でも即座に検索")
    print("  2. 挿入ソート → 価格順 O(n^2): 商品数が少ないので十分")
    print("  3. 逐次探索 → 在庫フィルタ O(n): 全商品を1回走査")


build_shop_system()  # 商品管理システムを実行する
```

---

### 課題10 解答例

```python
# ===================================================
# 課題10 解答例: 価値最大化アイテム収集
# ===================================================

from collections import deque  # BFS用のキューをインポートする

def bfs_distance(maze, source):
    """sourceから全セルへの最短距離を求める関数"""
    rows = len(maze)            # 行数を取得する
    cols = len(maze[0])         # 列数を取得する
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4方向を定義する

    distances = {}              # 距離を記録する辞書を作る
    distances[source] = 0       # ソースの距離は0
    queue = deque([source])     # キューにソースを入れる

    while queue:                # キューが空になるまで繰り返す
        current = queue.popleft()   # 先頭を取り出す
        row, col = current          # 位置を取り出す
        for dr, dc in directions:   # 4方向を試す
            nr, nc = row + dr, col + dc
            next_pos = (nr, nc)
            if (0 <= nr < rows and 0 <= nc < cols   # 範囲内で
                    and maze[nr][nc] == 0            # 通路で
                    and next_pos not in distances):  # 未計算の場合
                distances[next_pos] = distances[current] + 1  # 距離を記録する
                queue.append(next_pos)  # キューに追加する

    return distances            # 距離マップを返す


def maximize_value(maze, start, item_values, max_steps):
    """制限歩数内で価値を最大化する関数"""

    # --- ステップ1: BFSで全地点間の最短距離を計算する ---
    # 使用アルゴリズム: BFS O(V+E) をスタートと各アイテムから実行
    points = [start] + list(item_values.keys())  # 全地点リストを作る
    dist_map = {}               # 地点間の距離マップを作る

    for point in points:        # 各地点からBFSを実行する
        dist_map[point] = bfs_distance(maze, point)  # 距離マップに登録する

    # --- ステップ2: 全組み合わせを探索して最大価値を求める ---
    # 使用: 状態付きBFS (位置, 集めたアイテムのfrozenset, 残り歩数)
    items_list = list(item_values.keys())  # アイテム位置のリストを作る
    best_value = 0              # 最大価値を初期化する
    best_path = [start]         # 最適経路を初期化する
    best_collected = frozenset()    # 最適収集セットを初期化する

    # BFSで全パターンを探索する
    # 状態 = (現在位置, 集めたアイテム, 残り歩数)
    state_queue = deque()       # 状態キューを初期化する
    state_queue.append((start, frozenset(), max_steps, [start]))  # 初期状態を追加する
    explored = 0                # 探索数を初期化する

    while state_queue:          # キューが空になるまで繰り返す
        current, collected, remaining, path = state_queue.popleft()
        explored += 1           # 探索数を増やす

        # 現在の価値を計算する
        current_value = 0       # 現在の合計価値を初期化する
        for item_pos in collected:  # 集めたアイテムの価値を合算する
            current_value += item_values[item_pos]

        if current_value > best_value:  # 過去最高を超えた場合
            best_value = current_value  # 最大価値を更新する
            best_path = path[:]         # 最適経路を更新する
            best_collected = collected  # 最適収集セットを更新する

        # まだ取っていないアイテムへの移動を試す
        for item_pos in items_list:     # 各アイテムを確認する
            if item_pos not in collected:    # まだ取っていない場合
                if item_pos in dist_map[current]:   # 到達可能な場合
                    distance = dist_map[current][item_pos]  # 距離を取得する
                    if distance <= remaining:        # 残り歩数で足りる場合
                        new_collected = collected | {item_pos}  # アイテムを追加する
                        new_remaining = remaining - distance     # 残り歩数を減らす
                        new_path = path + [item_pos]            # 経路を追加する
                        state_queue.append((item_pos, new_collected,
                                            new_remaining, new_path))

    return best_value, best_path, best_collected, explored


# --- テスト ---
maze = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)                  # スタート位置を設定する
item_values = {                 # アイテムの位置と価値を定義する
    (0, 4): 10,                 # 右上のアイテム（価値10）
    (2, 0): 5,                  # 左中のアイテム（価値5）
    (4, 4): 15,                 # 右下のアイテム（価値15）
    (4, 0): 3,                  # 左下のアイテム（価値3）
}
max_steps = 12                  # 制限歩数を設定する

print("=== 課題10: 価値最大化アイテム収集 ===")  # タイトルを出力する
print(f"制限歩数: {max_steps}")  # 制限歩数を出力する
print(f"アイテム数: {len(item_values)}個")  # アイテム数を出力する
print(f"アイテム一覧:")          # アイテム一覧を出力する
for pos, value in item_values.items():
    print(f"  位置{pos}: 価値{value}")

value, path, collected, explored = maximize_value(maze, start, item_values, max_steps)

print(f"\n【結果】")             # 結果セクションを出力する
print(f"  最大価値: {value}")    # 最大価値を出力する
print(f"  経路: {path}")         # 最適経路を出力する
print(f"  取得アイテム: {collected}")  # 取得セットを出力する
print(f"  探索状態数: {explored}")    # 探索数を出力する

print(f"\n【使ったアルゴリズムと計算量】")  # 分析を出力する
print("  1. BFS O(V+E): 各地点間の最短距離を計算")
print("  2. 状態付きBFS: 全収集パターンを探索")
print("  3. ハッシュ(dict): 距離・価値の即座取得 O(1)")
print("  4. frozenset: アイテム収集状態の管理")
print(f"  全体計算量: O(地点数 * V * E + 2^アイテム数 * アイテム数)")
```
