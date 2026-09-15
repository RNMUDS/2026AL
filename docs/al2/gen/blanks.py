# -*- coding: utf-8 -*-
"""例題の「穴埋め」の定義。

例題1は完成したコードを読んで実行する。例題2は、アルゴリズムの要になる行を
____ にして載せ、学生が埋めてから実行する（実行結果の画像と同じになれば正解）。

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
