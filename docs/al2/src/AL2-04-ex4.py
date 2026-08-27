# すべての行き方を書き出して最小コストを求める方法（全探索）は、
# 迷路が少し大きくなるだけで使えなくなることを確かめる
import time

def count_all_routes(size):
    """size × size の迷路で、同じマスを2度通らない行き方をすべて数え、
    いちばん安い合計コストも求める。すべてのマスのコストは1とする。"""
    goal = (size - 1, size - 1)
    visited = set()
    result = {"count": 0, "best": None}

    def walk(r, c, total):
        """ここから先の行き方を、同じ場所を2度通らないようにすべてたどる"""
        if (r, c) == goal:
            result["count"] = result["count"] + 1
            if result["best"] is None or total < result["best"]:
                result["best"] = total
            return
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                continue
            if (nr, nc) in visited:
                continue
            visited.add((nr, nc))
            walk(nr, nc, total + 1)
            visited.discard((nr, nc))    # 調べ終わったら「通っていない」状態に戻す

    visited.add((0, 0))
    walk(0, 0, 0)
    return result["count"], result["best"]


print("全探索で「すべての行き方」を数えたときの通り数と時間")
print("-" * 56)
print("迷路の大きさ             行き方の数   かかった時間")

for size in [3, 4, 5, 6]:
    started = time.time()
    count, best = count_all_routes(size)
    elapsed = time.time() - started
    print(f"{size}マス×{size}マス   {count:>16,}通り   {elapsed:>10.3f}秒")

print("-" * 56)
print()
print("7マス×7マスの行き方は 575,780,564 通りある。")
print("6マス×6マスのおよそ456倍なので、同じパソコンでは1時間近くかかる計算になる。")
print("迷路が1マス大きくなるだけで、全探索は現実的な時間で終わらなくなる。")
