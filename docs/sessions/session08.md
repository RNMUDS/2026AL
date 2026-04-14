# 第8回: 挿入ソート（直接挿入法）

## 学習目標

- ソート（並び替え）がなぜ重要かを理解する
- 挿入ソートの仕組みを「トランプの手札を並べる」比喩で理解する
- 挿入ソートを比較回数カウント付きで実装できる
- Pygame を使ったソートの可視化ができる
- データサイズによる実行時間の変化を測定できる

---

## 1. 説明

### 1.1 なぜソートが重要なのか

- **検索の高速化**: ソート済みデータなら二分探索 O(log n) が使える
- **データ分析**: 中央値、最大値、最小値が簡単に見つかる
- **重複の検出**: ソート済みなら隣同士を比較するだけ
- **表示の整理**: 名前順、日付順、成績順など

### 1.2 挿入ソートの考え方

トランプのカードを手に持って、1枚ずつ正しい位置に差し込む動作と同じです。

```
1. 最初のカードは「整列済み」（1枚だけなので）
2. 2枚目のカードを手に取る
3. 手札の中で正しい位置を見つける
4. その位置にカードを差し込む
5. 3枚目以降も同様に繰り返す
```

### 1.3 アルゴリズムの手順

```
配列: [64, 34, 25, 12, 22]

ステップ1: 34 を取り出す → 34 < 64 なので 64 の前に挿入
  → [34, 64, 25, 12, 22]

ステップ2: 25 を取り出す → 25 < 64, 25 < 34 なので先頭に挿入
  → [25, 34, 64, 12, 22]

ステップ3: 12 を取り出す → 12 < 64, 12 < 34, 12 < 25 なので先頭に挿入
  → [12, 25, 34, 64, 22]

ステップ4: 22 を取り出す → 22 < 64, 22 < 34, 22 < 25, 22 > 12 なので 12 の後に挿入
  → [12, 22, 25, 34, 64]
```

### 1.4 計算量

| ケース | 比較回数 | 特徴 |
|--------|----------|------|
| 最良（ソート済み） | O(n) | 各要素で1回の比較のみ |
| 平均 | O(n^2) | 約 n(n-1)/4 回 |
| 最悪（逆順） | O(n^2) | n(n-1)/2 回 |

---

## 2. 例題

### 例題1: 2つの変数を交換する

```python
# ===== 2つの変数の値を交換する基本操作 =====

# --- 方法1: 一時変数を使う ---
value_a = 30  # 変数aに30を代入する
value_b = 10  # 変数bに10を代入する
print(f"交換前: a={value_a}, b={value_b}")  # 交換前の値を表示する

temp = value_a  # 一時変数にaの値を退避する
value_a = value_b  # aにbの値を代入する
value_b = temp  # bに退避した値を代入する
print(f"交換後: a={value_a}, b={value_b}")  # 交換後の値を表示する

# --- 方法2: Pythonのタプル交換 ---
value_x = 50  # 変数xに50を代入する
value_y = 20  # 変数yに20を代入する
print(f"\n交換前: x={value_x}, y={value_y}")  # 交換前の値を表示する

value_x, value_y = value_y, value_x  # Pythonの多重代入で交換する
print(f"交換後: x={value_x}, y={value_y}")  # 交換後の値を表示する

# --- 配列内の2要素を交換する ---
data = [30, 10, 20]  # テスト用の配列を作成する
print(f"\n配列の交換前: {data}")  # 交換前の配列を表示する

if data[0] > data[1]:  # data[0]がdata[1]より大きい場合
    print(f"  data[0]={data[0]} > data[1]={data[1]} → 交換する")  # 比較結果を表示する
    temp = data[0]  # 一時変数にdata[0]を退避する
    data[0] = data[1]  # data[0]にdata[1]の値を代入する
    data[1] = temp  # data[1]に退避した値を代入する
    print(f"  交換後: {data}")  # 交換後の配列を表示する
else:  # data[0]がdata[1]以下の場合
    print(f"  data[0]={data[0]} <= data[1]={data[1]} → 交換不要")  # 交換不要メッセージ
```

### 例題2: 挿入位置を見つけて要素を挿入する

```python
# ===== ソート済み配列に値を正しい位置に挿入する =====

sorted_part = [12, 25, 34, 64]  # ソート済みの配列を用意する
new_value = 22  # 挿入したい値を設定する
print(f"ソート済み部分: {sorted_part}")  # ソート済み部分を表示する
print(f"挿入する値: {new_value}")  # 挿入する値を表示する

# --- 挿入位置を探す（右端から左に向かって比較）---
position = len(sorted_part)  # 挿入位置を末尾に初期化する
print(f"\n--- 挿入位置を探す ---")  # 見出しを表示する

for i in range(len(sorted_part) - 1, -1, -1):  # 右端から左に向かってループする
    print(f"  比較: {new_value} と sorted_part[{i}]={sorted_part[i]}", end="")  # 比較内容を表示する
    if sorted_part[i] > new_value:  # 現在の要素が挿入値より大きい場合
        position = i  # 挿入位置を更新する
        print(f" → {sorted_part[i]} > {new_value}, 位置を{i}に更新")  # 位置更新を表示する
    else:  # 現在の要素が挿入値以下の場合
        print(f" → {sorted_part[i]} <= {new_value}, ここで停止")  # 停止メッセージ
        break  # ループを終了する

print(f"\n挿入位置: {position}")  # 最終的な挿入位置を表示する

# --- 要素をずらして挿入する ---
sorted_part.append(0)  # 末尾にダミー要素を追加して配列を拡張する
print(f"\n--- 要素を右にずらす ---")  # 見出しを表示する

for i in range(len(sorted_part) - 1, position, -1):  # 末尾から挿入位置まで
    sorted_part[i] = sorted_part[i - 1]  # 要素を1つ右にずらす
    print(f"  sorted_part[{i}] = sorted_part[{i-1}] ({sorted_part[i]})")  # ずらし操作を表示する

sorted_part[position] = new_value  # 挿入位置に新しい値を代入する
print(f"\n結果: {sorted_part}")  # 挿入後の配列を表示する
```

### 例題3: 挿入ソートの1パス（1要素の挿入）

```python
# ===== 挿入ソート: 1要素を正しい位置に挿入する1パス =====

data = [25, 34, 64, 12, 22]  # 先頭3つがソート済みの配列
target_index = 3  # 挿入する要素のインデックスを設定する
print(f"配列: {data}")  # 配列の状態を表示する
print(f"ソート済み部分: {data[:target_index]}")  # ソート済み部分を表示する
print(f"挿入する値: data[{target_index}] = {data[target_index]}")  # 挿入する値を表示する

# --- keyを取り出す ---
key = data[target_index]  # 挿入する値をkeyに保存する
j = target_index - 1  # 比較を開始するインデックスを設定する
shift_count = 0  # ずらし回数を初期化する

print(f"\n--- 挿入位置を探しながら要素をずらす ---")  # 見出しを表示する

# --- keyより大きい要素を右にずらす ---
while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
    print(f"  data[{j}]={data[j]} > key={key} → data[{j+1}]にずらす")  # ずらし操作を表示する
    data[j + 1] = data[j]  # 要素を右に1つずらす
    shift_count = shift_count + 1  # ずらし回数を加算する
    j = j - 1  # 1つ左に移動する

# --- keyを正しい位置に挿入する ---
data[j + 1] = key  # keyを空いた位置に挿入する
print(f"\n  key={key} を data[{j+1}] に挿入（ずらし{shift_count}回）")  # 挿入結果を表示する
print(f"結果: {data}")  # 挿入後の配列を表示する
```

### 例題4: 完全な挿入ソート（比較回数カウント付き）

```python
# ===== 完全な挿入ソート（各ステップ表示+比較回数カウント） =====

def insertion_sort(data):
    """挿入ソートを実行する関数（比較回数と移動回数を計測する）"""
    n = len(data)  # 配列の長さを取得する
    comparison_count = 0  # 比較回数を初期化する
    shift_count = 0  # 移動回数を初期化する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print(f"配列の長さ: {n}")  # 長さを表示する
    print("=" * 60)  # 区切り線を表示する

    for i in range(1, n):  # 2番目の要素から最後まで処理する
        key = data[i]  # 挿入するカードを取り出す
        j = i - 1  # 整列済み部分の右端のインデックスを設定する

        print(f"\nステップ {i}: key={key}")  # ステップ番号と挿入値を表示する
        print(f"  整列済み: {data[:i]}")  # 整列済み部分を表示する
        print(f"  未整列:   {data[i:]}")  # 未整列部分を表示する

        while j >= 0:  # 左端に到達するまでループする
            comparison_count = comparison_count + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                shift_count = shift_count + 1  # 移動回数を加算する
                print(f"    data[{j}]={data[j]} > {key} → 右にずらす")  # ずらし操作を表示する
                j = j - 1  # 1つ左に移動する
            else:  # key以下の要素に当たった場合
                print(f"    data[{j}]={data[j]} <= {key} → ここに挿入")  # 停止位置を表示する
                break  # ループを終了する

        data[j + 1] = key  # keyを正しい位置に挿入する
        print(f"  → data[{j+1}] に {key} を挿入")  # 挿入位置を表示する
        print(f"  現在の配列: {data}")  # 現在の配列状態を表示する

    print("\n" + "=" * 60)  # 区切り線を表示する
    print(f"ソート完了: {data}")  # 最終結果を表示する
    print(f"比較回数: {comparison_count}, 移動回数: {shift_count}")  # 統計を表示する
    return data, comparison_count, shift_count  # 結果を返す

# --- テスト実行 ---
test_data = [64, 34, 25, 12, 22]  # テスト用配列を定義する
insertion_sort(test_data[:])  # コピーを渡してソートする
```

### 例題5: テキストベースのソート可視化

```python
# ===== テキストで挿入ソートの過程を棒グラフ風に可視化する =====

def visualize_sort(data):
    """挿入ソートを棒グラフ風テキストで可視化する関数"""
    n = len(data)  # 配列の長さを取得する
    max_value = max(data)  # 最大値を取得する（棒の長さ計算用）

    def draw_bars(data, current_idx, sorted_up_to, step_label):
        """棒グラフ風にデータを描画する内部関数"""
        print(f"\n  {step_label}")  # ステップのラベルを表示する
        for i in range(n):  # 各要素について棒を描画する
            bar_length = int(data[i] / max_value * 30)  # 棒の長さを計算する
            if i == current_idx:  # 現在挿入中の要素の場合
                marker = ">>"  # 挿入中のマーカーを設定する
                bar_char = "@"  # 目立つ文字を使う
            elif i <= sorted_up_to:  # 整列済み部分の場合
                marker = "OK"  # 整列済みマーカーを設定する
                bar_char = "#"  # 通常の棒文字を使う
            else:  # 未整列部分の場合
                marker = "  "  # 空白マーカーを設定する
                bar_char = "-"  # 未整列用の棒文字を使う
            bar = bar_char * bar_length  # 棒の文字列を作成する
            print(f"    [{marker}] data[{i:>2}]={data[i]:>3} |{bar}")  # 棒を表示する

    print("=== 挿入ソート 可視化 ===")  # 見出しを表示する
    print(f"元の配列: {data}")  # 元の配列を表示する

    draw_bars(data, -1, 0, "初期状態")  # 初期状態を描画する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
            data[j + 1] = data[j]  # 要素を右にずらす
            j = j - 1  # 1つ左に移動する

        data[j + 1] = key  # keyを正しい位置に挿入する
        draw_bars(data, j + 1, i, f"ステップ{i}: key={key} を data[{j+1}] に挿入")  # ステップを描画する

    print(f"\nソート完了: {data}")  # 最終結果を表示する

# --- テスト実行 ---
test_data = [64, 34, 25, 12, 22, 50, 15]  # テスト用配列を定義する
visualize_sort(test_data[:])  # コピーを渡して可視化する
```

---

## 3. 標準課題

### 課題1: 2つの変数の値を交換する（超やさしい）

変数 `value_a = 100` と `value_b = 200` の値を一時変数を使って交換し、交換前と交換後の値を表示してください。

### 課題2: 配列内の2要素を交換する（超やさしい）

配列 `[50, 30, 40, 10, 20]` について、`data[0]` と `data[3]` を交換し、交換前後の配列を表示してください。

### 課題3: ソート済み配列に対して要素をずらす操作を行う（やさしい）

ソート済み配列 `[10, 20, 30, 50]` に値 `25` を挿入するため、各要素を右にずらす操作を1ステップずつ表示してください。

### 課題4: ソート済み配列の正しい位置に値を挿入する（やさしい）

ソート済み配列 `[10, 20, 30, 40, 50]` に対して、値 `35` を正しい位置に挿入してください。挿入位置の探索過程と要素のずらし操作を表示してください。

### 課題5: 配列の先頭N要素を挿入ソートで整列する（やややさしい）

配列 `[64, 34, 25, 12, 22, 11, 90]` の先頭4要素 `[64, 34, 25, 12]` だけを挿入ソートで整列し、各ステップの配列の状態を表示してください。

### 課題6: 配列の先頭N要素を段階的に増やして整列する（やややさしい）

配列 `[64, 34, 25, 12, 22, 11, 90]` に対して、先頭2要素、3要素、4要素...と段階的に挿入ソートを適用し、各段階の配列状態を表示してください。

### 課題7: 比較回数と移動回数をカウントする挿入ソートを実装する（やや普通）

挿入ソート関数を実装し、比較回数と移動回数をカウントしてください。テストデータ `[64, 34, 25, 12, 22]`, `[5, 4, 3, 2, 1]`, `[1, 2, 3, 4, 5]` で動作確認してください。

### 課題8: 各ステップのトレース出力付き挿入ソートを実装する（やや普通）

挿入ソートの各ステップで「挿入する値」「ソート済み部分」「挿入位置」「移動した要素」を表示してください。テストデータ `[38, 27, 43, 3, 9, 82, 10]` で動作確認してください。

### 課題9: テキストベースの挿入ソート可視化プログラムを作成する（普通）

配列の各要素を棒グラフ風に表示し、挿入ソートの各ステップで整列済み部分と未整列部分を区別して表示するプログラムを作成してください。

### 課題10: 挿入ソートの実行時間をデータサイズ別に計測する（普通）

データサイズ 100, 500, 1000, 2000, 5000 でランダム配列を生成し、挿入ソートの実行時間と比較回数を計測してください。結果を表形式で表示し、O(n^2) であることを実験的に確認してください。

---

## 4. 発展課題

### 発展課題1: Pygame による挿入ソートアニメーション

Pygame を使って棒グラフで挿入ソートの過程を可視化してください。整列済み部分を緑、現在挿入中の要素を赤、未整列部分を青で色分けしてください。

### 発展課題2: トランプカードの手札ソートゲーム

ランダムに配られた5枚のカード（1-13の数値）を手動で並び替えるゲームを作成してください。プレイヤーの操作と挿入ソートの動きを比較して表示してください。

---

## 5. 解答例

### 課題1の解答例

```python
# ===== 課題1: 2つの変数の値を交換する =====

value_a = 100  # 変数aに100を代入する
value_b = 200  # 変数bに200を代入する

print("=== 変数の交換 ===")  # 見出しを表示する
print(f"交換前: a={value_a}, b={value_b}")  # 交換前の値を表示する

temp = value_a  # 一時変数にaの値を退避する
value_a = value_b  # aにbの値を代入する
value_b = temp  # bに退避した値を代入する

print(f"交換後: a={value_a}, b={value_b}")  # 交換後の値を表示する
print(f"\n確認: a={value_a}(元のb), b={value_b}(元のa)")  # 確認メッセージを表示する
```

### 課題2の解答例

```python
# ===== 課題2: 配列内の2要素を交換する =====

data = [50, 30, 40, 10, 20]  # テスト用配列を定義する
print(f"交換前: {data}")  # 交換前の配列を表示する
print(f"  data[0]={data[0]}, data[3]={data[3]}")  # 交換対象を表示する

# --- data[0]とdata[3]を交換する ---
temp = data[0]  # 一時変数にdata[0]を退避する
data[0] = data[3]  # data[0]にdata[3]の値を代入する
data[3] = temp  # data[3]に退避した値を代入する

print(f"交換後: {data}")  # 交換後の配列を表示する
print(f"  data[0]={data[0]}, data[3]={data[3]}")  # 交換結果を確認する
```

### 課題3の解答例

```python
# ===== 課題3: 要素をずらす操作 =====

sorted_arr = [10, 20, 30, 50]  # ソート済み配列を定義する
new_value = 25  # 挿入する値を設定する

print(f"配列: {sorted_arr}")  # 配列を表示する
print(f"挿入する値: {new_value}")  # 挿入する値を表示する

# --- 挿入位置を見つける ---
insert_pos = len(sorted_arr)  # 挿入位置を末尾に初期化する
for i in range(len(sorted_arr)):  # 配列を先頭から走査する
    if sorted_arr[i] > new_value:  # 挿入値より大きい要素を見つけた場合
        insert_pos = i  # その位置を挿入位置にする
        print(f"\n挿入位置: {insert_pos} (sorted_arr[{i}]={sorted_arr[i]} > {new_value})")  # 挿入位置を表示する
        break  # ループを終了する

# --- 末尾にダミーを追加して右にずらす ---
sorted_arr.append(0)  # 配列を1要素分拡張する
print(f"\n--- 要素を右にずらす ---")  # 見出しを表示する

for i in range(len(sorted_arr) - 1, insert_pos, -1):  # 末尾から挿入位置まで
    sorted_arr[i] = sorted_arr[i - 1]  # 要素を1つ右にずらす
    print(f"  sorted_arr[{i}] = sorted_arr[{i-1}] = {sorted_arr[i]}")  # ずらし操作を表示する
    print(f"  配列の状態: {sorted_arr}")  # 配列の状態を表示する

# --- 挿入する ---
sorted_arr[insert_pos] = new_value  # 挿入位置に新しい値を代入する
print(f"\nsorted_arr[{insert_pos}] = {new_value}")  # 挿入操作を表示する
print(f"結果: {sorted_arr}")  # 最終結果を表示する
```

### 課題4の解答例

```python
# ===== 課題4: ソート済み配列に値を挿入する =====

sorted_arr = [10, 20, 30, 40, 50]  # ソート済み配列を定義する
new_value = 35  # 挿入する値を設定する

print(f"ソート済み配列: {sorted_arr}")  # 配列を表示する
print(f"挿入する値: {new_value}")  # 挿入する値を表示する

# --- 挿入位置を右端から探す ---
print(f"\n--- 挿入位置を探す（右から左へ）---")  # 見出しを表示する
j = len(sorted_arr) - 1  # 右端のインデックスを設定する
sorted_arr.append(0)  # 末尾にダミー要素を追加する

while j >= 0:  # 左端に到達するまでループする
    print(f"  比較: sorted_arr[{j}]={sorted_arr[j]} と {new_value}", end="")  # 比較内容を表示する
    if sorted_arr[j] > new_value:  # 現在の要素が挿入値より大きい場合
        sorted_arr[j + 1] = sorted_arr[j]  # 要素を右にずらす
        print(f" → {sorted_arr[j]} > {new_value}, 右にずらす")  # ずらし操作を表示する
        j = j - 1  # 1つ左に移動する
    else:  # 現在の要素が挿入値以下の場合
        print(f" → {sorted_arr[j]} <= {new_value}, ここで停止")  # 停止メッセージ
        break  # ループを終了する

sorted_arr[j + 1] = new_value  # 挿入位置に値を代入する
print(f"\n{new_value} を sorted_arr[{j+1}] に挿入")  # 挿入位置を表示する
print(f"結果: {sorted_arr}")  # 最終結果を表示する
```

### 課題5の解答例

```python
# ===== 課題5: 先頭N要素を挿入ソートで整列する =====

data = [64, 34, 25, 12, 22, 11, 90]  # テスト用配列を定義する
sort_count = 4  # 先頭4要素を整列する

print(f"元の配列: {data}")  # 元の配列を表示する
print(f"先頭{sort_count}要素を整列します")  # 整列範囲を表示する
print("=" * 50)  # 区切り線を表示する

for i in range(1, sort_count):  # 2番目からsort_count番目まで処理する
    key = data[i]  # 挿入するカードを取り出す
    j = i - 1  # 比較開始位置を設定する

    print(f"\nステップ {i}: key={key}")  # ステップ情報を表示する
    print(f"  整列済み部分: {data[:i]}")  # 整列済み部分を表示する

    while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
        print(f"  data[{j}]={data[j]} > {key} → 右にずらす")  # ずらし操作を表示する
        data[j + 1] = data[j]  # 要素を右にずらす
        j = j - 1  # 1つ左に移動する

    data[j + 1] = key  # keyを正しい位置に挿入する
    print(f"  → data[{j+1}]に{key}を挿入")  # 挿入結果を表示する
    print(f"  現在の配列: {data}")  # 現在の配列を表示する

print(f"\n結果: {data}")  # 最終結果を表示する
print(f"先頭{sort_count}要素: {data[:sort_count]} ← 整列済み")  # 整列済み部分を表示する
```

### 課題6の解答例

```python
# ===== 課題6: 段階的に挿入ソートを適用する =====

data = [64, 34, 25, 12, 22, 11, 90]  # テスト用配列を定義する
n = len(data)  # 配列の長さを取得する

print(f"元の配列: {data}")  # 元の配列を表示する
print("=" * 60)  # 区切り線を表示する

for step in range(2, n + 1):  # 先頭2要素から全要素まで段階的に処理する
    # --- step番目の要素を整列済み部分に挿入する ---
    i = step - 1  # 挿入する要素のインデックスを計算する
    key = data[i]  # 挿入する値を取り出す
    j = i - 1  # 比較開始位置を設定する

    while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
        data[j + 1] = data[j]  # 要素を右にずらす
        j = j - 1  # 1つ左に移動する

    data[j + 1] = key  # keyを正しい位置に挿入する

    # --- 現在の状態を表示する ---
    sorted_section = data[:step]  # 整列済み部分を取得する
    unsorted_section = data[step:]  # 未整列部分を取得する
    print(f"先頭{step}要素を整列: {sorted_section} | {unsorted_section}")  # 状態を表示する

print(f"\n最終結果: {data}")  # 最終結果を表示する
```

### 課題7の解答例

```python
# ===== 課題7: 比較回数と移動回数カウント付き挿入ソート =====

def insertion_sort(data):
    """挿入ソートを実行して統計情報を返す関数"""
    n = len(data)  # 配列の長さを取得する
    comparison_count = 0  # 比較回数を初期化する
    shift_count = 0  # 移動回数を初期化する

    for i in range(1, n):  # 2番目の要素から最後まで処理する
        key = data[i]  # 挿入するカードを取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0:  # 左端に到達するまでループする
            comparison_count = comparison_count + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                shift_count = shift_count + 1  # 移動回数を加算する
                j = j - 1  # 1つ左に移動する
            else:  # key以下の要素に当たった場合
                break  # ループを終了する

        data[j + 1] = key  # keyを正しい位置に挿入する

    return data, comparison_count, shift_count  # 結果を返す

# --- テスト実行 ---
test_cases = [  # テストケースのリストを定義する
    ("通常", [64, 34, 25, 12, 22]),
    ("最悪（逆順）", [5, 4, 3, 2, 1]),
    ("最良（ソート済み）", [1, 2, 3, 4, 5])
]

print("=== 挿入ソート: 比較回数・移動回数 ===\n")  # 見出しを表示する
for name, test in test_cases:  # 各テストケースを実行する
    original = test[:]  # 元の配列をコピーする
    result, comps, shifts = insertion_sort(test[:])  # ソートを実行する
    print(f"--- {name} ---")  # テストケース名を表示する
    print(f"  元の配列: {original}")  # 元の配列を表示する
    print(f"  ソート後:  {result}")  # ソート結果を表示する
    print(f"  比較回数:  {comps}")  # 比較回数を表示する
    print(f"  移動回数:  {shifts}")  # 移動回数を表示する
    print()  # 空行を表示する
```

### 課題8の解答例

```python
# ===== 課題8: トレース出力付き挿入ソート =====

def insertion_sort_trace(data):
    """各ステップの詳細をトレース出力する挿入ソート"""
    n = len(data)  # 配列の長さを取得する

    print(f"元の配列: {data}")  # 元の配列を表示する
    print("=" * 60)  # 区切り線を表示する

    for i in range(1, n):  # 2番目の要素から最後まで処理する
        key = data[i]  # 挿入するカードを取り出す
        j = i - 1  # 比較開始位置を設定する
        moved = []  # 移動した要素のリストを初期化する

        print(f"\nステップ {i}:")  # ステップ番号を表示する
        print(f"  挿入する値: {key}")  # 挿入する値を表示する
        print(f"  ソート済み部分: {data[:i]}")  # ソート済み部分を表示する

        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
            moved.append(data[j])  # 移動した要素を記録する
            data[j + 1] = data[j]  # 要素を右にずらす
            j = j - 1  # 1つ左に移動する

        data[j + 1] = key  # keyを正しい位置に挿入する

        insert_pos = j + 1  # 挿入位置を計算する
        if len(moved) > 0:  # 移動した要素がある場合
            print(f"  移動した要素: {moved}")  # 移動した要素を表示する
        else:  # 移動した要素がない場合
            print(f"  移動した要素: なし（そのままの位置）")  # 移動なしを表示する
        print(f"  挿入位置: data[{insert_pos}]")  # 挿入位置を表示する
        print(f"  結果: {data}")  # 結果を表示する

    print("\n" + "=" * 60)  # 区切り線を表示する
    print(f"ソート完了: {data}")  # 最終結果を表示する

# --- テスト実行 ---
test_data = [38, 27, 43, 3, 9, 82, 10]  # テスト用配列を定義する
insertion_sort_trace(test_data[:])  # コピーを渡してソートする
```

### 課題9の解答例

```python
# ===== 課題9: テキストベースの挿入ソート可視化 =====

def visualize_insertion_sort(data):
    """棒グラフ風テキストで挿入ソートを可視化する関数"""
    n = len(data)  # 配列の長さを取得する
    max_val = max(data)  # 最大値を取得する

    def draw_bars(current_idx, sorted_up_to):
        """棒グラフ風に配列を描画する内部関数"""
        for i in range(n):  # 各要素について棒を描画する
            bar_length = int(data[i] / max_val * 30)  # 棒の長さを計算する
            if i == current_idx:  # 現在挿入中の要素
                marker = ">>"  # 挿入中マーカーを設定する
                bar = "@" * bar_length  # 目立つ棒文字を使う
            elif i <= sorted_up_to:  # 整列済み部分
                marker = "OK"  # 整列済みマーカーを設定する
                bar = "#" * bar_length  # 通常の棒文字を使う
            else:  # 未整列部分
                marker = "  "  # 空白マーカーを設定する
                bar = "-" * bar_length  # 未整列用棒文字を使う
            print(f"    [{marker}] {data[i]:>3} |{bar}")  # 棒を表示する

    print("=== 挿入ソート可視化 ===")  # 見出しを表示する
    print(f"元の配列: {data}\n")  # 元の配列を表示する

    print("  [初期状態]")  # 初期状態のラベルを表示する
    draw_bars(-1, 0)  # 初期状態を描画する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間ループする
            data[j + 1] = data[j]  # 要素を右にずらす
            j = j - 1  # 1つ左に移動する

        data[j + 1] = key  # keyを正しい位置に挿入する

        print(f"\n  [ステップ{i}: key={key} → data[{j+1}]]")  # ステップ情報を表示する
        draw_bars(j + 1, i)  # ステップの状態を描画する

    print(f"\nソート完了: {data}")  # 最終結果を表示する

# --- テスト実行 ---
test_data = [64, 34, 25, 12, 22, 50, 15, 40]  # テスト用配列を定義する
visualize_insertion_sort(test_data[:])  # コピーを渡して可視化する
```

### 課題10の解答例

```python
# ===== 課題10: データサイズ別の実行時間計測 =====

import time  # 時間計測用モジュール
import random  # ランダムデータ生成用モジュール

def insertion_sort_timed(data):
    """挿入ソート（比較回数カウント付き、表示なし版）"""
    n = len(data)  # 配列の長さを取得する
    comparison_count = 0  # 比較回数を初期化する

    for i in range(1, n):  # 2番目の要素から処理する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        while j >= 0:  # 左端まで探す
            comparison_count = comparison_count + 1  # 比較回数を加算する
            if data[j] > key:  # 左隣がkeyより大きい場合
                data[j + 1] = data[j]  # 要素を右にずらす
                j = j - 1  # 1つ左に移動する
            else:  # key以下に当たった場合
                break  # ループを終了する

        data[j + 1] = key  # keyを正しい位置に挿入する

    return data, comparison_count  # ソート結果と比較回数を返す

# --- 複数のデータサイズで計測する ---
sizes = [100, 500, 1000, 2000, 5000]  # テストするデータサイズのリスト

print("=== 挿入ソート: 実行時間計測 ===\n")  # 見出しを表示する
print(f"{'データ数':<10} {'実行時間(秒)':<16} {'比較回数':<16} {'比較/n^2'}")  # ヘッダーを表示する
print("-" * 58)  # 区切り線を表示する

results = []  # 結果を保存するリスト

for size in sizes:  # 各データサイズでテストする
    data = []  # テストデータを初期化する
    for i in range(size):  # size個のランダム整数を生成する
        data.append(random.randint(0, 10000))  # ランダム整数を追加する

    start = time.time()  # 計測を開始する
    sorted_data, comparisons = insertion_sort_timed(data)  # ソートを実行する
    elapsed = time.time() - start  # 経過時間を計算する

    n_squared = size * size  # n^2を計算する
    ratio = comparisons / n_squared  # 比較回数/n^2を計算する
    results.append((size, elapsed, comparisons))  # 結果を保存する

    print(f"{size:<10} {elapsed:<16.4f} {comparisons:<16} {ratio:.4f}")  # 結果を表示する

# --- O(n^2)の確認 ---
print("\n=== O(n^2)の確認 ===")  # 見出しを表示する
if len(results) >= 2:  # 結果が2つ以上ある場合
    n1 = results[0][0]  # 最初のデータサイズ
    t1 = results[0][1]  # 最初の実行時間
    n2 = results[-1][0]  # 最後のデータサイズ
    t2 = results[-1][1]  # 最後の実行時間

    size_ratio = n2 / n1  # サイズの比率を計算する
    time_ratio = t2 / t1 if t1 > 0 else 0  # 実行時間の比率を計算する
    expected_ratio = (n2 / n1) ** 2  # 理論上の比率を計算する

    print(f"  データ数: {n1} → {n2} ({size_ratio:.0f}倍)")  # サイズ比を表示する
    print(f"  実行時間: {t1:.4f}秒 → {t2:.4f}秒 ({time_ratio:.1f}倍)")  # 時間比を表示する
    print(f"  理論値 (n^2): {expected_ratio:.0f}倍")  # 理論比を表示する
    print(f"  → 実測比と理論比が近ければ O(n^2) が確認できた")  # 結論を表示する
```

### 発展課題1の解答例

```python
# ===== 発展課題1: Pygame による挿入ソートアニメーション =====
# 実行するには pygame が必要: pip install pygame

import pygame  # ゲーム/描画ライブラリ
import random  # ランダムデータ生成用
import sys  # システム操作用

# --- 色の定義（RGB） ---
WHITE = (255, 255, 255)  # 背景色（白）
BLACK = (0, 0, 0)  # テキスト色（黒）
BLUE = (70, 130, 180)  # 未整列の棒の色（青）
RED = (220, 50, 50)  # 現在挿入中の色（赤）
GREEN = (50, 180, 50)  # 整列済みの色（緑）
DARK_BLUE = (30, 60, 90)  # ヘッダー背景色

# --- 画面設定 ---
SCREEN_WIDTH = 900  # 画面幅を設定する
SCREEN_HEIGHT = 600  # 画面高さを設定する
HEADER_HEIGHT = 80  # ヘッダーの高さを設定する

def generate_data(count, max_value=100):
    """ランダムデータを生成する関数"""
    data = []  # 結果リストを初期化する
    for i in range(count):  # count回繰り返す
        value = random.randint(5, max_value)  # 5からmax_valueのランダム整数
        data.append(value)  # リストに追加する
    return data  # データリストを返す

def draw_bars(screen, data, current_index, sorted_up_to, font):
    """棒グラフとしてデータを描画する関数"""
    screen.fill(WHITE)  # 画面を白で塗りつぶす

    pygame.draw.rect(screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))  # ヘッダーを描画する
    title_text = font.render("Insertion Sort Visualization", True, WHITE)  # タイトルテキストを作成する
    screen.blit(title_text, (20, 10))  # タイトルを表示する

    if current_index >= 0:  # ソート中の場合
        step_text = font.render(  # ステップ情報のテキストを作成する
            f"Inserting: data[{current_index}] = {data[current_index]}",
            True, WHITE
        )
        screen.blit(step_text, (20, 45))  # ステップ情報を表示する

    n = len(data)  # データの個数を取得する
    bar_width = max(1, (SCREEN_WIDTH - 40) // n)  # 棒の幅を計算する
    max_value = max(data) if data else 1  # 最大値を取得する
    bar_area_top = HEADER_HEIGHT + 10  # 棒エリアの上端を設定する
    bar_area_bottom = SCREEN_HEIGHT - 30  # 棒エリアの下端を設定する
    available_height = bar_area_bottom - bar_area_top  # 描画可能な高さを計算する

    for i in range(n):  # 各データについて棒を描画する
        bar_height = int((data[i] / max_value) * available_height)  # 棒の高さを計算する

        if i == current_index:  # 現在挿入中の場合
            color = RED  # 赤色に設定する
        elif i <= sorted_up_to:  # 整列済み部分の場合
            color = GREEN  # 緑色に設定する
        else:  # 未整列部分の場合
            color = BLUE  # 青色に設定する

        x = 20 + i * bar_width  # 棒のx座標を計算する
        y = bar_area_bottom - bar_height  # 棒のy座標を計算する
        pygame.draw.rect(screen, color, (x, y, bar_width - 2, bar_height))  # 棒を描画する

    pygame.display.update()  # 画面を更新する

def main():
    """メイン関数: Pygameの初期化と挿入ソートアニメーション"""
    pygame.init()  # pygameを初期化する
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 画面を作成する
    pygame.display.set_caption("Insertion Sort")  # ウィンドウタイトルを設定する
    font = pygame.font.SysFont("Arial", 20)  # フォントを設定する

    data = generate_data(50)  # 50個のランダムデータを生成する
    n = len(data)  # データ数を取得する
    delay = 30  # アニメーション速度を設定する（ミリ秒）

    draw_bars(screen, data, -1, 0, font)  # 初期状態を表示する
    pygame.time.wait(1000)  # 1秒待つ

    for i in range(1, n):  # 挿入ソートを実行する
        key = data[i]  # 挿入する値を取り出す
        j = i - 1  # 比較開始位置を設定する

        draw_bars(screen, data, i, i - 1, font)  # 挿入する要素を赤で表示する
        pygame.time.wait(delay)  # 少し待つ

        for event in pygame.event.get():  # イベントを処理する
            if event.type == pygame.QUIT:  # 閉じるボタンの場合
                pygame.quit()  # pygameを終了する
                sys.exit()  # プログラムを終了する

        while j >= 0 and data[j] > key:  # 左隣がkeyより大きい間
            data[j + 1] = data[j]  # 要素を右にずらす
            j = j - 1  # 1つ左に移動する
            draw_bars(screen, data, j + 1, i, font)  # 状態を更新して表示する
            pygame.time.wait(delay)  # 少し待つ

        data[j + 1] = key  # keyを挿入する
        draw_bars(screen, data, -1, i, font)  # 挿入後の状態を表示する
        pygame.time.wait(delay)  # 少し待つ

    draw_bars(screen, data, -1, n - 1, font)  # 完了状態を表示する

    waiting = True  # 終了待ちフラグを設定する
    while waiting:  # ユーザーが閉じるまで待つ
        for event in pygame.event.get():  # イベントを処理する
            if event.type == pygame.QUIT:  # 閉じるボタンの場合
                waiting = False  # 待機を終了する
            if event.type == pygame.KEYDOWN:  # キー入力の場合
                if event.key == pygame.K_ESCAPE:  # ESCキーの場合
                    waiting = False  # 待機を終了する

    pygame.quit()  # pygameを終了する

if __name__ == "__main__":  # 直接実行された場合
    main()  # メイン関数を実行する
```

### 発展課題2の解答例

```python
# ===== 発展課題2: トランプカードの手札ソートゲーム =====

import random  # ランダムデータ生成用モジュール

def display_hand(cards, label="手札"):
    """手札をカード風に表示する関数"""
    card_strs = []  # カード表示用リストを初期化する
    for card in cards:  # 各カードについて処理する
        card_strs.append(f"[{card:>2}]")  # カード文字列を追加する
    print(f"  {label}: {''.join(card_strs)}")  # 手札を表示する

def insertion_sort_cards(cards):
    """挿入ソートでカードを並べる過程を表示する関数"""
    n = len(cards)  # カード数を取得する
    steps = 0  # ステップ数を初期化する

    print("\n=== 挿入ソートでの並べ替え ===")  # 見出しを表示する
    display_hand(cards, "初期状態")  # 初期状態を表示する

    for i in range(1, n):  # 2枚目のカードから処理する
        key = cards[i]  # 挿入するカードを取り出す
        j = i - 1  # 比較開始位置を設定する
        steps = steps + 1  # ステップ数を加算する

        while j >= 0 and cards[j] > key:  # 左隣がkeyより大きい間ループする
            cards[j + 1] = cards[j]  # カードを右にずらす
            j = j - 1  # 1つ左に移動する

        cards[j + 1] = key  # カードを正しい位置に挿入する
        display_hand(cards, f"ステップ{steps}")  # 現在の状態を表示する

    return steps  # ステップ数を返す

def play_game():
    """カードソートゲームのメイン関数"""
    all_cards = list(range(1, 14))  # 1から13のカードを作成する
    hand = random.sample(all_cards, 5)  # 5枚をランダムに選ぶ

    print("=== トランプ手札ソートゲーム ===\n")  # 見出しを表示する
    print("5枚のカードが配られました。")  # 説明メッセージを表示する
    display_hand(hand, "配られたカード")  # 配られたカードを表示する

    # --- プレイヤーの手動ソート ---
    player_hand = hand[:]  # プレイヤー用のコピーを作成する
    player_moves = 0  # プレイヤーの操作回数を初期化する

    print("\n--- あなたの番 ---")  # プレイヤーのターンを表示する
    print("カードの位置番号(0-4)を2つ入力して交換します。")  # 操作説明を表示する
    print("'done'と入力すると終了します。\n")  # 終了方法を表示する

    while True:  # プレイヤーの入力を繰り返す
        display_hand(player_hand, "現在の手札")  # 現在の手札を表示する
        user_input = input("  交換する位置 (例: 0 3) または 'done': ")  # 入力を受け付ける

        if user_input.strip().lower() == "done":  # doneが入力された場合
            break  # ループを終了する

        parts = user_input.strip().split()  # 入力をスペースで分割する
        if len(parts) != 2:  # 入力が2つでない場合
            print("  2つの数字を入力してください")  # エラーメッセージを表示する
            continue  # ループの先頭に戻る

        try:  # 入力値の処理を試みる
            pos1 = int(parts[0])  # 1つ目の位置を整数に変換する
            pos2 = int(parts[1])  # 2つ目の位置を整数に変換する
        except ValueError:  # 整数変換に失敗した場合
            print("  数字を入力してください")  # エラーメッセージを表示する
            continue  # ループの先頭に戻る

        if pos1 < 0 or pos1 > 4 or pos2 < 0 or pos2 > 4:  # 範囲外の場合
            print("  0-4の範囲で入力してください")  # エラーメッセージを表示する
            continue  # ループの先頭に戻る

        temp = player_hand[pos1]  # 一時変数に退避する
        player_hand[pos1] = player_hand[pos2]  # 交換する
        player_hand[pos2] = temp  # 交換を完了する
        player_moves = player_moves + 1  # 操作回数を加算する
        print(f"  → 位置{pos1}と位置{pos2}を交換しました (操作{player_moves}回目)")  # 交換結果を表示する

    # --- 挿入ソートの結果と比較 ---
    algo_hand = hand[:]  # アルゴリズム用のコピーを作成する
    algo_steps = insertion_sort_cards(algo_hand)  # 挿入ソートを実行する

    print("\n=== 結果比較 ===")  # 比較の見出しを表示する
    display_hand(player_hand, "あなたの結果")  # プレイヤーの結果を表示する
    display_hand(algo_hand, "挿入ソート  ")  # アルゴリズムの結果を表示する
    print(f"\n  あなたの操作回数: {player_moves}回")  # プレイヤーの操作回数を表示する
    print(f"  挿入ソートのステップ: {algo_steps}回")  # アルゴリズムのステップ数を表示する

    is_sorted = True  # ソート済みフラグを初期化する
    for i in range(len(player_hand) - 1):  # 隣り合う要素を比較する
        if player_hand[i] > player_hand[i + 1]:  # 順序が正しくない場合
            is_sorted = False  # フラグをFalseにする
            break  # ループを終了する

    if is_sorted:  # 正しくソートされている場合
        print("\n  正しくソートできました!")  # 成功メッセージを表示する
    else:  # ソートされていない場合
        print("\n  まだソートが完了していません。")  # 未完了メッセージを表示する

# --- ゲーム実行 ---
play_game()  # ゲームを開始する
```

---

## 6. まとめ

| 項目 | 内容 |
|------|------|
| 挿入ソート | トランプの手札を並べる要領でソート |
| アルゴリズム | 整列済み部分に1つずつ正しい位置に挿入 |
| 時間計算量 | 平均・最悪: O(n^2)、最良（ソート済み）: O(n) |
| 比較回数 | 最悪: n(n-1)/2 回、最良: n-1 回 |
| 特徴 | 小規模データやほぼ整列済みデータに効率的 |
