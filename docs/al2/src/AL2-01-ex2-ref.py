travel_time = {
    ("学校", "郵便局"): 8,
    ("学校", "図書館"): 12,
    ("学校", "カフェ"): 5,
    ("郵便局", "図書館"): 6,
    ("郵便局", "カフェ"): 9,
    ("図書館", "カフェ"): 7,
}

def minutes_between(a, b):
    """2地点 a と b のあいだの移動時間（分）を返す

    表には ("学校", "郵便局") のように片方向しか書いていないので、
    (a, b) と (b, a) の両方をためす。
    """

    if (a, b) in travel_time:

        return travel_time[(a, b)]
    return travel_time[(b, a)]

def total_minutes(route):
    """学校 → route の順に回る → 学校 に戻るまでの合計時間（分）を返す

    route = 回る順番を並べたリスト。例 ["郵便局", "図書館", "カフェ"]
    """
    total = 0
    place = "学校"

    for next_place in route:

        total = total + minutes_between(place, next_place)
        place = next_place
    total = total + minutes_between(place, "学校")
    return total

all_routes = [
    ["郵便局", "図書館", "カフェ"],
    ["郵便局", "カフェ", "図書館"],
    ["図書館", "郵便局", "カフェ"],
    ["図書館", "カフェ", "郵便局"],
    ["カフェ", "郵便局", "図書館"],
    ["カフェ", "図書館", "郵便局"],
]

print("学校 → 3か所 → 学校 の合計時間をすべて調べる")
print("-" * 52)

best_route = None
best_time = None

for route in all_routes:
    minutes = total_minutes(route)

    print("学校 →", " → ".join(route), "→ 学校 :", minutes, "分")

    if best_time is None or minutes < best_time:
        best_time = minutes
        best_route = route

print("-" * 52)
print("試した順番の数:", len(all_routes), "通り")
print("いちばん短い順番: 学校 →", " → ".join(best_route), "→ 学校")
print("そのときの合計時間:", best_time, "分")
