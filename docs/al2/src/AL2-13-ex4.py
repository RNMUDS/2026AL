# 作品づくりに使える部品集
# コピーして自分の作品に組み込むための、小さな道具を4つ集めた。
import time

# ------------------------------------------------------------
# 部品1: プレイヤーからの入力を受け取る
# ------------------------------------------------------------
# 授業ページに実行結果を載せるため、いまは USE_INPUT を False にしてある。
# 自分の作品では True に変えると、キーボードから入力できるようになる。
USE_INPUT = False
sample_answers = ["3", "たなか", "DDRR"]
answer_index = 0


def ask(question, default):
    """質問を表示して答えを受け取る。USE_INPUT が False なら決められた答えを返す。"""
    global answer_index
    if USE_INPUT:
        return input(question)
    if answer_index < len(sample_answers):
        answer = sample_answers[answer_index]
        answer_index = answer_index + 1
    else:
        answer = default
    print(question + answer + "  ← 入力のかわりに用意した答え")
    return answer


print("=" * 52)
print("  部品1: 入力を受け取る")
print("=" * 52)
level = ask("難易度を選んでください（1〜3）: ", "1")
name = ask("名前を入力してください: ", "ゲスト")
print(f"  → 難易度 {level} で、{name} さんとして始めます")
print()


# ------------------------------------------------------------
# 部品2: 数字だけを受け取る（まちがった入力をはじく）
# ------------------------------------------------------------
def ask_number(question, low, high, default):
    """low 以上 high 以下の整数を受け取る。正しくない入力はやり直しになる。"""
    while True:
        answer = ask(question, str(default))
        if not answer.isdigit():
            print("  数字を入力してください")
            if not USE_INPUT:
                return default
            continue
        value = int(answer)
        if value < low or value > high:
            print(f"  {low} から {high} までの数を入力してください")
            if not USE_INPUT:
                return default
            continue
        return value


print("=" * 52)
print("  部品2: 数字だけを受け取る")
print("=" * 52)
count = ask_number("配達先の数を入力してください（3〜8）: ", 3, 8, 5)
print(f"  → 配達先を {count} 件にします")
print()


# ------------------------------------------------------------
# 部品3: 処理にかかった時間を測る
# ------------------------------------------------------------
print("=" * 52)
print("  部品3: 時間を測る")
print("=" * 52)

began = time.time()
total = 0
for i in range(1000000):
    total = total + i
elapsed = time.time() - began

print(f"  1から100万までの合計: {total:,}")
print(f"  かかった時間: {elapsed:.4f}秒")
print()


# ------------------------------------------------------------
# 部品4: スコアを計算して表示する
# ------------------------------------------------------------
def show_score(player_value, best_value, smaller_is_better=True):
    """プレイヤーの結果と最適な結果を比べて、100点満点で表示する"""
    if smaller_is_better:
        score = int(best_value / player_value * 100)
    else:
        score = int(player_value / best_value * 100)
    if score > 100:
        score = 100

    print(f"  あなたの結果: {player_value}")
    print(f"  最適な結果  : {best_value}")
    print(f"  スコア      : {score}点")

    bar_length = score // 4
    print("  [" + "#" * bar_length + "." * (25 - bar_length) + "]")

    if score == 100:
        print("  評価: ★★★ 最適解を見つけた")
    elif score >= 80:
        print("  評価: ★★☆ あと少し")
    else:
        print("  評価: ★☆☆ もう一度考えてみよう")
    return score


print("=" * 52)
print("  部品4: スコアを表示する")
print("=" * 52)
show_score(42, 18)
print()
show_score(19, 18)
print()
print("=" * 52)
print("  4つの部品を組み合わせれば、遊べる作品になる")
print("=" * 52)
