import random

answer = random.randint(1, 30)
max_tries = 3

print(f"1〜30の数を当ててください（{max_tries}回以内）")

for i in range(max_tries):
    remaining = max_tries - i
    print(f"（残り{remaining}回）")

    guess = int(input("予想: "))

    if guess == answer:
        print(f"正解！ {i+1}回目で当たりました！")
        break
    elif guess > answer:
        print("もっと小さい数です")
    else:
        print("もっと大きい数です")
else:
    print(f"残念！ 答えは {answer} でした")