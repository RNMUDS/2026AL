# 数当てゲーム: コンピュータが「秘密の数」を当てる
# 1 から 100 までの中に秘密の数が1つある。
# コンピュータは「まん中を聞く」作戦で当てにいく。

secret = 73      # 秘密の数（あとで自由に変えてよい）
low = 1          # 探す範囲の下限
high = 100       # 探す範囲の上限
count = 0        # 何回目の質問かを数える

print("秘密の数を 1〜100 の中から当てます")
print("-" * 44)

while low <= high:
    count = count + 1
    middle = (low + high) // 2      # 範囲のまん中（// は小数を切り捨てる割り算）

    print("質問", count, "回目: 範囲", low, "〜", high, "／まん中は", middle, end="  ")

    if middle == secret:
        print("→ 正解！")
        break
    elif middle < secret:
        print("→ もっと大きい")
        low = middle + 1            # 下限を上げて、右半分だけを残す
    else:
        print("→ もっと小さい")
        high = middle - 1           # 上限を下げて、左半分だけを残す

print("-" * 44)
print("秘密の数", secret, "を", count, "回の質問で当てました")
