# 数当てゲームを「1回の質問でどれだけ候補を減らせるか」という目で見直す
# 作戦A: 1から順に「1ですか」「2ですか」…と聞く（逐次探索）
# 作戦B: いつも残っている範囲のまん中を聞く（二分探索）


def count_linear(secret, low, high):
    """1から順に聞いたときの質問回数"""
    count = 0
    for guess in range(low, high + 1):
        count = count + 1
        if guess == secret:
            return count
    return count


def count_binary(secret, low, high):
    """まん中を聞いたときの質問回数"""
    count = 0
    while low <= high:
        count = count + 1
        middle = (low + high) // 2
        if middle == secret:
            return count
        elif middle < secret:
            low = middle + 1
        else:
            high = middle - 1
    return count


low = 1
high = 100

linear_counts = []
binary_counts = []
for secret in range(low, high + 1):
    linear_counts.append(count_linear(secret, low, high))
    binary_counts.append(count_binary(secret, low, high))

print("1から100までの100個の数すべてを、2つの作戦で当ててみる")
print("-" * 56)
print("作戦                  最悪の回数    平均の回数")
print(f"A: 1から順に聞く    {max(linear_counts):>10}回 {sum(linear_counts)/len(linear_counts):>11.2f}回")
print(f"B: まん中を聞く     {max(binary_counts):>10}回 {sum(binary_counts)/len(binary_counts):>11.2f}回")
print("-" * 56)
print()

# 1回の質問で候補がどれだけ減るかを見る
print("1回の質問で「残る候補の数」がどう変わるか（秘密の数が73のとき）")
print("-" * 56)
print("質問  作戦A: 1から順に聞く      作戦B: まん中を聞く")

low_a = 1
high_a = 100
low_b = 1
high_b = 100
secret = 73

for step in range(1, 8):
    # 作戦A: step 番目の数を聞く
    remain_a = high_a - low_a + 1
    if low_a <= secret <= high_a:
        low_a = low_a + 1              # 外れたので候補が1つ減るだけ
    after_a = high_a - low_a + 1

    # 作戦B: まん中を聞く
    remain_b = high_b - low_b + 1
    if low_b <= high_b:
        middle = (low_b + high_b) // 2
        if middle < secret:
            low_b = middle + 1
        elif middle > secret:
            high_b = middle - 1
        else:
            low_b = middle
            high_b = middle
    after_b = high_b - low_b + 1

    print(f"{step:>3}回目  {remain_a:>4}個 → {after_a:>4}個"
          f"            {remain_b:>4}個 → {after_b:>4}個")

print("-" * 56)
print()
print("作戦Aは1回につき1個しか減らない。作戦Bは1回で半分に減る。")
print("「1回の質問でいちばん多く候補を減らす」選び方が、まん中を聞く作戦になっている。")
