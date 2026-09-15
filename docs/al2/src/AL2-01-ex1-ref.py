secret = 73
low = 1
high = 100
count = 0

print("秘密の数を 1〜100 の中から当てます")

print("-" * 44)

while low <= high:
    count = count + 1

    middle = (low + high) // 2

    print("質問", count, "回目: 範囲", low, "〜", high, "／中央は", middle, end="  ")

    if middle == secret:
        print("→ 正解！")

        break

    elif middle < secret:
        print("→ もっと大きい")

        low = middle + 1

    else:
        print("→ もっと小さい")

        high = middle - 1

print("-" * 44)

print("秘密の数", secret, "を", count, "回の質問で当てました")
