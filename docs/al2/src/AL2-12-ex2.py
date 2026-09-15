# ナップサック問題: 決められた時間の中で、得点がいちばん高くなる組み合わせを選ぶ
# ゲームの「制限時間内にどのイベントをこなすか」という場面にあたる。

# (名前, かかる分数, もらえる得点)
quests = [
    ("村人を助ける", 6, 10),
    ("宝箱をあける", 5, 8),
    ("鉱石を掘る", 5, 8),
    ("釣りをする", 9, 12),
]

limit = 10          # 使える時間（分）
n = len(quests)


def pad(text, width):
    """全角文字を2文字ぶんとして数え、右側に空白を足して表示の幅をそろえる"""
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


print(f"使える時間: {limit}分")
print("-" * 46)
print(pad("できること", 24) + pad("かかる分", 10) + pad("得点", 8) + " 1分あたり")
for name, minutes, score in quests:
    print(pad(name, 24) + pad(f"{minutes}分", 10) + pad(f"{score}点", 8)
          + f"{score / minutes:>10.2f}")
print("-" * 46)
print()

# --- 方法1: 貪欲法（1分あたりの得点が高いものから選ぶ） ---
# 「1分あたりの得点」を計算して、大きい順に番号を並べる
# key= には「並べかえの基準にする値を返す関数」を渡す。reverse=True で大きい順になる
order = sorted(range(n), key=lambda i: quests[i][2] / quests[i][1], reverse=True)
used = 0
greedy_score = 0
greedy_names = []
for i in order:
    name, minutes, score = quests[i]
    if used + minutes <= limit:
        used = used + minutes
        greedy_score = greedy_score + score
        greedy_names.append(name)

print("方法1: 貪欲法（1分あたりの得点が高い順に、入るだけ入れる）")
print("  選んだもの:", "、".join(greedy_names))
print(f"  使った時間: {used}分 ／ 合計得点: {greedy_score}点")
print()

# --- 方法2: 動的計画法（表を作って最適解を求める） ---
# best[i][t] = 「前から i 個まで見て、使える時間が t 分のときの最高得点」
best = []
for i in range(n + 1):
    best.append([0] * (limit + 1))

for i in range(1, n + 1):
    name, minutes, score = quests[i - 1]
    for t in range(limit + 1):
        # i番目を選ばない場合
        best[i][t] = best[i - 1][t]
        # i番目を選ぶ場合（時間が足りるときだけ）
        if t >= minutes:
            if best[i - 1][t - minutes] + score > best[i][t]:
                best[i][t] = best[i - 1][t - minutes] + score

print("動的計画法の表（たて = 何個目まで見たか、よこ = 使える時間）")
print("-" * 62)
print("      " + "".join(f"{t:>4}" for t in range(limit + 1)))
for i in range(n + 1):
    label = "なし" if i == 0 else f"{i}個目"
    print(pad(label, 6) + "".join(f"{best[i][t]:>4}" for t in range(limit + 1)))
print("-" * 62)
print()

# どれを選んだかを逆にたどって調べる
chosen = []
t = limit
for i in range(n, 0, -1):
    if best[i][t] != best[i - 1][t]:
        name, minutes, score = quests[i - 1]
        chosen.append(name)
        t = t - minutes
chosen.reverse()

print("方法2: 動的計画法（すべての組み合わせを表で調べる）")
print("  選んだもの:", "、".join(chosen))
print(f"  合計得点: {best[n][limit]}点")
print()
print("差:", best[n][limit] - greedy_score, "点")
print("貪欲法は「1分あたりの得点」だけを見るので、")
print("時間がぴったり収まる組み合わせを見のがしてしまう。")
