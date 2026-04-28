import time

# 大きなリストとセットを作る（0〜999999999の数）
big_list = list(range(1_000_000_000))
big_set = set(range(1_000_000_000))

# リスト版（先頭から順に探すので遅い）
start_time = time.time()
result_list = 999_999_999 in big_list
list_time = time.time() - start_time
print(f"リストで検索: {list_time:.6f}秒")

# セット版（ハッシュで即座に見つけるので速い）
start_time = time.time()
result_set = 999_999_999 in big_set
set_time = time.time() - start_time
print(f"セットで検索: {set_time:.6f}秒")