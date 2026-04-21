import random

# コンピュータが1〜50の中からランダムに答えを決める
answer = random.randint(1, 50)

# 試行回数を記録する変数
count = 0

# 正解するまで繰り返す
while True:
    guess = int(input("1〜50の数を予想してください: "))
    count = count + 1

    if guess == answer:
        print(f"正解！ 答えは {answer} でした！")
        print(f"{count}回で当たりました")
        break
    elif guess > answer:
        print("もっと小さい数です")
    else:
        print("もっと大きい数です")