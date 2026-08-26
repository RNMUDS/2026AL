# 条件から「どのアルゴリズムを使うべきか」を判定するプログラム
# 後期に学んだ5つのアルゴリズムを、条件で選び分ける。


def pad(text, width):
    length = 0
    for ch in text:
        if ord(ch) > 0x2000:
            length = length + 2
        else:
            length = length + 1
    return text + " " * (width - length)


def choose(kind, weighted, size, need_best):
    """条件から使うべきアルゴリズムを1つ選んで、名前と理由を返す

    kind      : "経路" なら2地点間の最短経路、"巡回" なら全部回って戻る問題
    weighted  : 辺に重み（時間や距離の差）があるなら True
    size      : 頂点や都市の数
    need_best : 必ず最適解が必要なら True
    """
    if kind == "経路":
        if not weighted:
            if need_best:
                return "幅優先探索", "重みがないので、歩数の少ない順に広げれば必ず最短になる"
            return "深さ優先探索", "最短でなくてよいなら、調べるマスが少ない深さ優先探索で足りる"
        return "ダイクストラ法", "重みがあるので、コストの小さい順に確定していく必要がある"

    # kind == "巡回"
    if not need_best:
        return "貪欲法", "最適でなくてよいので、いちばん近い都市へ進むだけで一瞬で終わる"
    if size <= 10:
        return "全探索", f"{size}都市なら順番の数が少なく、全部試しても一瞬で終わる"
    if size <= 20:
        return "bitDP", f"{size}都市では全探索は終わらないが、bitDP なら表が現実的な大きさに収まる"
    return "貪欲法", f"{size}都市では bitDP でも表が大きすぎる。最適解はあきらめて近似解を使うしかない"


cases = [
    ("駅の乗りかえ回数を最小にする", "経路", False, 9000, True),
    ("迷路のゴールに行けるかだけ判定する", "経路", False, 400, False),
    ("カーナビで最も早く着く道を案内する", "経路", True, 100000, True),
    ("床コストのある迷路を最小コストで抜ける", "経路", True, 10000, True),
    ("修学旅行で6か所を回る順番を決める", "巡回", True, 6, True),
    ("工場のドリルが18か所をあける順番を決める", "巡回", True, 18, True),
    ("宅配便が100軒を回る順番を5秒で決める", "巡回", True, 100, False),
    ("配送センターが30軒の最適な順番を1晩かけて求める", "巡回", True, 30, True),
]

print("条件から使うべきアルゴリズムを選ぶ")
print("=" * 76)
for description, kind, weighted, size, need_best in cases:
    name, reason = choose(kind, weighted, size, need_best)
    print(pad(description, 52) + "→ " + name)
    print(" " * 54 + reason)
    print()
print("=" * 76)
print()
print("同じ「巡回」の問題でも、都市の数と「最適解が必要か」で答えが変わる。")
print("アルゴリズムは1つを覚えるのではなく、使い分けられることが大切。")
