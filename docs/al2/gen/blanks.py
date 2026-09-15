# -*- coding: utf-8 -*-
"""例題の「穴埋め」の定義。

各例題は「参考」（コメントなしの完成コード）と「実践」（要の行を ____ にした穴埋め、丁寧なコメント付き）の
2つで載せる。学生は実践のコードを埋めてから実行する（実行結果の画像と同じになれば正解）。

  B(find, answer, hint, wrong, nth=0)
    find   : 例題ファイルの中の1行（の一部）。この文字列をさがす
    answer : find の中で ____ にする部分（穴の答え）
    hint   : 穴のとなりに出すヒント
    wrong  : 候補として並べる「まちがい」2つ（answer と混ぜて表示する）
    nth    : find が複数回あるとき、何番目（0始まり）を穴にするか

src/ のファイルはそのまま（答え入り）で置き、ページに載せるときだけ穴をあける。
実行結果の画像は src/ のファイルを実行して作る。
"""


def B(find, answer, hint, wrong, nth=0):
    assert answer in find, (find, answer)
    return dict(find=find, answer=answer, hint=hint, wrong=wrong, nth=nth)


BLANKS = {
# ---------------- 第1回 ----------------
"AL2-01-ex2.py": [
    B("if best_time is None or minutes < best_time:", "minutes < best_time",
      "いま計算した合計時間が、これまでの最短より短いときだけ更新する",
      ["minutes > best_time", "minutes == best_time"]),
    B('total = total + minutes_between(place, "学校")', 'minutes_between(place, "学校")',
      "最後の場所から学校へ戻る時間を足す",
      ['minutes_between("学校", route[0])', "0"]),
],
# ---------------- 第2回 ----------------
"AL2-02-ex2.py": [
    B("current = memo.popleft()", "memo.popleft()",
      "幅優先探索: メモのいちばん古い行を読む",
      ["memo.pop()", "memo[-1]"]),
    B("current = memo.pop()", "memo.pop()",
      "深さ優先探索: メモのいちばん新しい行を読む",
      ["memo.popleft()", "memo[0]"]),
    B("if next_cell in came_from:", "next_cell in came_from",
      "すでに来たことがある場所は飛ばす",
      ["next_cell == goal", "next_cell in memo"]),
],
"AL2-03-ex2.py": [
    B("matrix[j][i] = 1", "matrix[j][i] = 1",
      "路線は両方向に通れるので、行と列を入れかえた場所にも1を書く",
      ["matrix[i][j] = 1", "matrix[j][i] = 0"]),
    B("list_cells = len(lines) * 2", "len(lines) * 2",
      "隣接リストのマスの数。1本の路線は両方の駅に書かれる",
      ["len(lines)", "n * n"]),
],
"AL2-04-ex2.py": [
    B("total = total + minutes", "total + minutes",
      "区間の時間を合計に足す",
      ["total + 1", "minutes"]),
    B("if route_minutes(route) < route_minutes(best_route):", "route_minutes(route) < route_minutes(best_route)",
      "合計時間が短いほうを最良にする（幅優先探索は駅の数しか見ていない）",
      ["len(route) < len(best_route)", "route_minutes(route) > route_minutes(best_route)"]),
],
"AL2-05-ex2.py": [
    B("if current is None or distance[station] < distance[current]:", "distance[station] < distance[current]",
      "まだ確定していない駅の中で、いちばん時間が小さい駅を選ぶ",
      ["distance[station] > distance[current]", "station < current"]),
    B("new_distance = distance[current] + minutes", "distance[current] + minutes",
      "確定した駅までの時間に、その路線の時間を足す",
      ["minutes", "distance[name] + minutes"]),
    B("if new_distance < distance[name]:", "new_distance < distance[name]",
      "いまの表の値より短いときだけ書き直す",
      ["new_distance > distance[name]", "new_distance == distance[name]"]),
],
"AL2-06-ex2.py": [
    B("minutes, current = heapq.heappop(queue)", "heapq.heappop(queue)",
      "いちばん時間が小さい組を取り出す",
      ["queue.pop()", "queue.popleft()"]),
    B("if current in settled:", "current in settled",
      "同じ駅が2回出てきたら、あとの方は読み飛ばす",
      ["current == start", "current not in settled"]),
    B("heapq.heappush(queue, (new_distance, name))", "(new_distance, name)",
      "heapq に入れる組は（時間, 駅名）の順。時間で並ぶようにする",
      ["(name, new_distance)", "new_distance"]),
],
"AL2-07-ex2.py": [
    B("order.append((current, total))", "order.append((current, total))",
      "確定した順番に、マスと合計秒数を記録する",
      ["order.append(current)", "order.insert(0, current)"]),
    B("heapq.heappush(pq, (new_total, (nr, nc)))", "(new_total, (nr, nc))",
      "（合計秒数, マス）の組を入れる。秒数で並ぶようにする",
      ["((nr, nc), new_total)", "new_total"]),
],
"AL2-08-ex2.py": [
    B("all_orders = list(permutations([1, 2, 3, 4]))", "permutations([1, 2, 3, 4])",
      "1〜4番の都市の並べ方をすべて作る（学校は0番で固定）",
      ["permutations([0, 1, 2, 3, 4])", "[1, 2, 3, 4]"]),
    B("total = total + distance[here][0]", "distance[here][0]",
      "最後の都市から学校（0番）へ戻る距離を足す",
      ["distance[here][1]", "0"]),
],
"AL2-09-ex2.py": [
    B("if j in visited:", "j in visited",
      "すでに行った都市は候補にしない",
      ["j == here", "j not in visited"]),
    B("if nearest is None or distance[here][j] < distance[here][nearest]:", "distance[here][j] < distance[here][nearest]",
      "いまいる場所から、まだ行っていない都市のうちいちばん近いものを選ぶ",
      ["distance[here][j] > distance[here][nearest]", "distance[j][j] < distance[nearest][nearest]"]),
    B("ratio = greedy_length / best_length", "greedy_length / best_length",
      "貪欲法の答えが、最適解の何倍か",
      ["best_length / greedy_length", "greedy_length - best_length"]),
],
"AL2-10-ex2.py": [
    B("if visited & (1 << next_city):", "visited & (1 << next_city)",
      "next_city のけたが1なら、すでに回った都市",
      ["visited | (1 << next_city)", "visited == next_city"]),
    B("new_visited = visited | (1 << next_city)", "visited | (1 << next_city)",
      "next_city のけたを1にした、新しい「回った集合」",
      ["visited & (1 << next_city)", "visited + 1"]),
    B("if new_length < best[new_visited][next_city]:", "new_length < best[new_visited][next_city]",
      "表の値より短いときだけ書き直す",
      ["new_length > best[new_visited][next_city]", "new_length < INF"]),
],
"AL2-11-ex2.py": [
    B("if count <= 12:", "count <= 12",
      "全探索は12都市までにする（それ以上は長すぎる）",
      ["count >= 12", "count < 6"]),
    B("answer = min(answer, best[full][here] + distance[here][0])", "best[full][here] + distance[here][0]",
      "全部回って here にいる状態から、0番へ戻る距離を足す",
      ["best[full][here]", "distance[here][0]"]),
],
"AL2-12-ex2.py": [
    B("if used + minutes <= limit:", "used + minutes <= limit",
      "貪欲法: 残り時間に入るクエストだけ受ける",
      ["minutes <= limit", "used <= limit"]),
    B("if t >= minutes:", "t >= minutes",
      "残り時間 t にこのクエストが入るときだけ「受ける」を考える",
      ["t <= minutes", "t > 0"]),
    B("if best[i - 1][t - minutes] + score > best[i][t]:", "best[i - 1][t - minutes] + score > best[i][t]",
      "このクエストを「受ける」ほうが得点が高いなら、表を書き直す",
      ["best[i - 1][t] > best[i][t]", "score > best[i][t]"]),
],
# ---------------- 第13回 ----------------
"AL2-13-ex2.py": [
    B("if nearest is None or distance[here][j] < distance[here][nearest]:", "distance[here][j] < distance[here][nearest]",
      "いまいる場所からいちばん近い配達先を選ぶ",
      ["distance[here][j] > distance[here][nearest]", "j < nearest"]),
    B("return tuple(visited[1:])", "tuple(visited[1:])",
      "営業所（0番）を除いた、回る順番を返す",
      ["tuple(visited)", "visited[0]"]),
],
"AL2-14-ex2.py": [
    B("nearest = None", "nearest = None",
      "バグ修正: 最初は「まだ候補なし」にして、最初の未訪問の家で必ず更新されるようにする",
      ["nearest = 0", "nearest = here"]),
    B("if nearest is None or distance[here][j] < distance[here][nearest]:", "nearest is None or distance[here][j] < distance[here][nearest]",
      "候補がまだ無いか、より近いときに更新する",
      ["distance[here][j] < distance[here][nearest]", "nearest is None"]),
],
"AL2-15-ex2.py": [
    B("value = function()", "function()",
      "表の各方法を順に呼び出して答えを受け取る",
      ["function", "methods()"]),
    B("if best_value is None or value < best_value:", "best_value is None or value < best_value",
      "5つの答えのうち、いちばん短いものを求める",
      ["value > best_value", "best_value is None"]),
],
}

# ================ 例題1（実践）の穴 ================
BLANKS.update({
"AL2-01-ex1.py": [
    B("middle = (low + high) // 2", "(low + high) // 2",
      "low と high の中央の位置。整数になる割り算を使う",
      ["(low + high) / 2", "low + high // 2"]),
    B("low = middle + 1", "low = middle + 1",
      "中央より大きい側に答えがあるので、調べる範囲の下限を中央の1つ上にする",
      ["high = middle - 1", "low = middle"]),
],
"AL2-02-ex1.py": [
    B("current = stack.pop()", "stack.pop()",
      "深さ優先探索: メモのいちばん新しい行を読んで消す",
      ["stack.pop(0)", "stack[0]"]),
    B("stack.append((nr, nc))", "stack.append((nr, nc))",
      "見つけたとなりのマスをメモの最後に書き足す",
      ["stack.insert(0, (nr, nc))", "stack.pop()"]),
],
"AL2-03-ex1.py": [
    B("edge_count = edge_count + len(railway[station])", "edge_count + len(railway[station])",
      "その駅につながっている路線の本数を足す",
      ["edge_count + 1", "len(railway)"]),
    B("edge_count = edge_count // 2", "edge_count // 2",
      "1本の路線は両方の駅から数えられるので、半分にする",
      ["edge_count * 2", "edge_count"]),
],
"AL2-04-ex1.py": [
    B("if name == next_station:", "name == next_station",
      "いまの駅のとなりの一覧から、次に行く駅を探す",
      ["name == here", "minutes == 0"]),
    B("total = total + minutes", "total + minutes",
      "見つかった路線の時間を合計に足す",
      ["total + 1", "minutes"]),
],
"AL2-05-ex1.py": [
    B("if current is None or distance[station] < distance[current]:", "distance[station] < distance[current]",
      "まだ確定していない駅の中で、いちばん時間が小さい駅を選ぶ",
      ["distance[station] > distance[current]", "station < current"]),
    B("new_distance = distance[current] + minutes", "distance[current] + minutes",
      "確定した駅までの時間に、その路線の時間を足す",
      ["minutes", "distance[name] + minutes"]),
    B("if new_distance < distance[name]:", "new_distance < distance[name]",
      "いまの表の値より短いときだけ書き直す",
      ["new_distance > distance[name]", "new_distance == distance[name]"]),
],
"AL2-06-ex1.py": [
    B("heapq.heappush(numbers, value)", "heapq.heappush(numbers, value)",
      "heapq に1つ入れる（入れたあとも「先頭がいちばん小さい」が保たれる）",
      ["numbers.append(value)", "heapq.heappop(numbers)"]),
    B("smallest = heapq.heappop(numbers)", "heapq.heappop(numbers)",
      "いちばん小さいものを取り出す",
      ["numbers.pop()", "numbers[0]"]),
    B('heapq.heappush(tasks, (9, "川崎"))', '(9, "川崎")',
      "（時間, 駅名）の順の組にすると、時間の小さい順に並ぶ",
      ['("川崎", 9)', "9"]),
],
"AL2-07-ex1.py": [
    B("current = queue.popleft()", "queue.popleft()",
      "幅優先探索: メモのいちばん古い行を読む",
      ["queue.pop()", "queue[-1]"]),
    B("total, current = heapq.heappop(pq)", "heapq.heappop(pq)",
      "ダイクストラ法: 合計コストがいちばん小さいマスを取り出す",
      ["pq.pop()", "pq.popleft()"]),
    B("new_total = total + cost_map[nxt[0]][nxt[1]]", "total + cost_map[nxt[0]][nxt[1]]",
      "取り出したマスまでの合計に、となりのマスのコストを足す",
      ["total + 1", "cost_map[nxt[0]][nxt[1]]"]),
],
"AL2-08-ex1.py": [
    B("d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)", "math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)",
      "2点のあいだの直線距離（三平方の定理: 横の差の2乗 + 縦の差の2乗 の平方根）",
      ["(x1 - x2) + (y1 - y2)", "math.sqrt(x1 * x2 + y1 * y2)"]),
    B("row.append(round(d, 1))", "round(d, 1)",
      "小数第1位までに丸めて表に入れる",
      ["int(d)", "d * 10"]),
],
"AL2-09-ex1.py": [
    B("if nearest is None or distance[here][j] < distance[here][nearest]:", "distance[here][j] < distance[here][nearest]",
      "いまいる場所から、まだ行っていない都市のうちいちばん近いものを選ぶ",
      ["distance[here][j] > distance[here][nearest]", "j < nearest"]),
    B("total = total + distance[here][start]", "distance[here][start]",
      "最後の都市から出発点へ戻る距離を足す",
      ["distance[start][start]", "0"]),
    B("if best_length is None or total < best_length:", "best_length is None or total < best_length",
      "全探索: 最初の1つ目か、これまでより短いときに更新する",
      ["total < best_length", "total > best_length"]),
],
"AL2-10-ex1.py": [
    B("bits = bits | (1 << i)", "bits | (1 << i)",
      "i番の都市のけたを1にして「回った」ことにする（| は「または」）",
      ["bits & (1 << i)", "bits + i"]),
    B("if bits & (1 << i):", "bits & (1 << i)",
      "i番のけたが1かどうかを調べる（& は「かつ」）",
      ["bits | (1 << i)", "bits == i"], nth=1),
],
"AL2-11-ex1.py": [
    B("return greedy_from(0)", "greedy_from(0)",
      "ふつうの貪欲法は0番（学校）から出発する",
      ["greedy_from(n)", "greedy_all_starts()"]),
    B("if visited & (1 << nxt):", "visited & (1 << nxt)",
      "nxt のけたが1なら、すでに回った都市なので飛ばす",
      ["visited | (1 << nxt)", "visited == nxt"]),
    B("if new_length < best[visited | (1 << nxt)][nxt]:", "new_length < best[visited | (1 << nxt)][nxt]",
      "表の値より短いときだけ書き直す",
      ["new_length > best[visited][nxt]", "new_length < INF"]),
],
"AL2-12-ex1.py": [
    B("middle = (low + high) // 2", "(low + high) // 2",
      "作戦B: 残っている範囲の中央を聞く",
      ["(low + high) / 2", "low + 1"]),
    B("low_a = low_a + 1", "low_a + 1",
      "作戦A: 外れたら候補が1つ減るだけ",
      ["low_a * 2", "high_a - 1"]),
    B("high_b = middle - 1", "high_b = middle - 1",
      "中央より小さい側に答えがあるので、上限を中央の1つ下にする",
      ["low_b = middle + 1", "high_b = middle"]),
],
"AL2-13-ex1.py": [
    B("if r < 0 or r >= rows or c < 0 or c >= cols:", "r < 0 or r >= rows or c < 0 or c >= cols",
      "迷路の外に出たかどうかを調べる",
      ["r > rows or c > cols", "r == 0 and c == 0"]),
    B("if total + cost_map[nr][nc] < distance[(nr, nc)]:", "total + cost_map[nr][nc] < distance[(nr, nc)]",
      "となりのマスへ行く合計が、表の値より短いときだけ書き直す",
      ["total < distance[(nr, nc)]", "cost_map[nr][nc] < distance[(nr, nc)]"]),
    B("heapq.heappush(queue, (distance[(nr, nc)], (nr, nc)))", "(distance[(nr, nc)], (nr, nc))",
      "（合計秒数, マス）の組を入れる。秒数で並ぶようにする",
      ["((nr, nc), distance[(nr, nc)])", "distance[(nr, nc)]"]),
],
"AL2-14-ex1.py": [
    B('return None, "迷路の外に出てしまいました"', 'return None, "迷路の外に出てしまいました"',
      "外に出たら、道の代わりに None と理由を返して止める",
      ['return route, "OK"', "continue"]),
    B("if route[-1] != goal:", "route[-1] != goal",
      "最後のマスがゴールでなければ受けつけない",
      ["route[0] != start", "len(route) == 0"]),
],
"AL2-15-ex1.py": [
    B("current = queue.popleft()", "queue.popleft()",
      "幅優先探索: メモのいちばん古い行を読む",
      ["queue.pop()", "queue[-1]"]),
    B("current = stack.pop()", "stack.pop()",
      "深さ優先探索: メモのいちばん新しい行を読む",
      ["stack.pop(0)", "stack[0]"]),
    B("minutes, current = heapq.heappop(queue)", "heapq.heappop(queue)",
      "ダイクストラ法: 時間がいちばん小さい組を取り出す",
      ["queue.pop()", "queue.popleft()"]),
],
})
