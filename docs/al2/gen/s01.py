# -*- coding: utf-8 -*-
"""第1回: ガイダンス・前期の復習 の本文を組み立てる。"""
import math
from collections import deque
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
                    answers, code, example, keywords, notion, run, section,
                    setup_guide, standard, write)

GREEN, AMBER, GRAY, RED = "#76B900", "#FFB800", "#888", "#FF5252"


def fig(w, h, inner, dark=True):
    bg = ' style="background:#0A0A0A"' if dark else ""
    return (f'      <div class="diagram-container">\n'
            f'        <svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg"'
            f' font-family="Noto Sans JP, sans-serif"{bg}>\n{inner}\n        </svg>\n'
            f'      </div>')


def reveal(i, n, dur, hold=0.12):
    """i 番目の要素を順番に出す opacity アニメーション（出たあとは消えない）。"""
    a = (1 - hold) * i / n
    return (f'<animate attributeName="opacity" values="0;0;1;1" '
            f'keyTimes="0;{a:.3f};{min(a + 0.03, 0.999):.3f};1" dur="{dur}s" '
            f'repeatCount="indefinite" fill="freeze"/>')


# ────────────────────────────────────────────────────────────
# 図1: 後期のロードマップ
# ────────────────────────────────────────────────────────────
def fig_roadmap():
    boxes = [
        ("第1〜2回", "前期の復習", ["探索を思い出す"]),
        ("第3〜4回", "グラフ", ["地図をデータに", "書き写す"]),
        ("第5〜7回", "ダイクストラ法", ["最短コストの道を", "求める"]),
        ("第8〜10回", "巡回セールスマン", ["全部回って戻る", "最短ルート"]),
        ("第11〜15回", "比較と作品制作", ["使い分けを整理し", "作品を作る"]),
    ]
    s = ['        <text x="350" y="26" text-anchor="middle" fill="#76B900" font-weight="700" font-size="15">'
         '後期に学ぶことの流れ</text>']
    n = len(boxes)
    for i, (weeks, name, lines) in enumerate(boxes):
        x = 20 + i * 134
        s.append(f'        <rect x="{x}" y="58" width="124" height="104" rx="12" fill="#1A1A1A" stroke="#444" stroke-width="1.5"/>')
        s.append(f'        <text x="{x+62}" y="80" text-anchor="middle" fill="{GRAY}" font-size="11">{weeks}</text>')
        s.append(f'        <text x="{x+62}" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
        for j, ln in enumerate(lines):
            s.append(f'        <text x="{x+62}" y="{124+j*16}" text-anchor="middle" fill="{GRAY}" font-size="10">{ln}</text>')
        # 順番に光る枠
        a, b = i / n, (i + 1) / n
        s.append(f'        <rect x="{x-3}" y="55" width="130" height="110" rx="14" fill="none" '
                 f'stroke="{GREEN}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.01:.3f};{b:.3f};1" dur="15s" repeatCount="indefinite"/></rect>')
        if i < n - 1:
            s.append(f'        <line x1="{x+124}" y1="110" x2="{x+132}" y2="110" stroke="#555" stroke-width="2"/>')
    s.append(f'        <text x="350" y="188" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '前期は「探す」。後期は「たくさんある選び方の中から、いちばん良い選び方を見つける」</text>')
    return fig(700, 205, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 「探す」と「いちばん良いものを選ぶ」の違い
# ────────────────────────────────────────────────────────────
def fig_search_vs_optimize():
    s = []
    # 左: 探す
    s.append(f'        <text x="175" y="28" text-anchor="middle" fill="{GRAY}" font-size="13" font-weight="700">前期の問題「探す」</text>')
    s.append('        <text x="175" y="48" text-anchor="middle" fill="#E0E0E0" font-size="11">たくさんのデータの中から目的の1つを見つける</text>')
    values = [14, 8, 23, 5, 31, 42, 19, 7]
    target_index = 5
    for i, v in enumerate(values):
        x = 30 + i * 36
        s.append(f'        <rect x="{x}" y="70" width="30" height="30" rx="6" fill="#141414" stroke="#444"/>')
        s.append(f'        <text x="{x+15}" y="90" text-anchor="middle" fill="#ccc" font-size="12">{v}</text>')
    # 走査マーカー
    xs = [30 + i * 36 + 15 for i in range(len(values))]
    key_times = ";".join(f"{i/ (len(values)+2):.3f}" for i in range(len(values))) + ";1"
    vals = ";".join(str(x) for x in xs) + f";{xs[target_index]}"
    s.append(f'        <polygon points="-6,0 6,0 0,10" fill="{AMBER}">'
             f'<animateTransform attributeName="transform" attributeType="XML" type="translate" '
             f'values="{";".join(f"{x} 54" for x in xs)};{xs[target_index]} 54" '
             f'keyTimes="{key_times}" dur="8s" repeatCount="indefinite" calcMode="discrete"/></polygon>')
    s.append(f'        <rect x="{30+target_index*36-2}" y="68" width="34" height="34" rx="7" fill="none" '
             f'stroke="{GREEN}" stroke-width="3" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.62;0.66;1" dur="8s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="175" y="128" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.62;0.66;1" dur="8s" repeatCount="indefinite"/>'
             '42 を見つけた</text>')
    s.append(f'        <text x="175" y="168" text-anchor="middle" fill="#bbb" font-size="11">答えは「どこにあるか」の1つだけ。</text>')
    s.append(f'        <text x="175" y="188" text-anchor="middle" fill="#bbb" font-size="11">見つかった時点で仕事は終わる。</text>')
    s.append(f'        <text x="175" y="222" text-anchor="middle" fill="{GRAY}" font-size="12" font-weight="700">42 がどこにあるかを答える</text>')
    # 区切り線
    s.append('        <line x1="350" y1="20" x2="350" y2="230" stroke="#333" stroke-width="1"/>')
    # 右: 選ぶ
    s.append(f'        <text x="525" y="28" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">後期の問題「いちばん良いものを選ぶ」</text>')
    s.append('        <text x="525" y="48" text-anchor="middle" fill="#E0E0E0" font-size="11">やり方が何通りもあり、それぞれに「かかる時間」がある</text>')
    routes = [("順番A", 26), ("順番B", 36), ("順番C", 32), ("順番D", 41)]
    best = 0
    for i, (name, cost) in enumerate(routes):
        y = 70 + i * 34
        wbar = int(cost * 4.2)
        s.append(f'        <g opacity="0">{reveal(i, len(routes)+2, 8)}')
        s.append(f'          <text x="378" y="{y+18}" fill="{GRAY}" font-size="11">{name}</text>')
        s.append(f'          <rect x="424" y="{y+4}" width="{wbar}" height="20" rx="5" '
                 f'fill="{"#1a2e0a" if i==best else "#141414"}" stroke="{GREEN if i==best else "#444"}"/>')
        s.append(f'          <text x="{424+wbar+10}" y="{y+19}" fill="#ccc" font-size="11">{cost}分</text>')
        s.append('        </g>')
    s.append(f'        <text x="525" y="222" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700" opacity="0">'
             f'{reveal(len(routes)+1, len(routes)+2, 8)}'
             '順番A が最短（いちばん良い選び方を1つ選ぶ）</text>')
    return fig(700, 240, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 二分探索で範囲が半分になっていく
# ────────────────────────────────────────────────────────────
def fig_binary_steps():
    steps = []
    low, high, secret = 1, 100, 73
    while low <= high:
        mid = (low + high) // 2
        if mid == secret:
            steps.append((low, high, mid, "正解！"))
            break
        elif mid < secret:
            steps.append((low, high, mid, "もっと大きい"))
            low = mid + 1
        else:
            steps.append((low, high, mid, "もっと小さい"))
            high = mid - 1

    X0, X1 = 150, 600

    def px(v):
        return X0 + (v - 1) / 99 * (X1 - X0)

    s = [f'        <text x="360" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '秘密の数 73 をさがす: 質問のたびに範囲が半分になる</text>',
         f'        <text x="{X0}" y="52" text-anchor="middle" fill="{GRAY}" font-size="10">1</text>',
         f'        <text x="{X1}" y="52" text-anchor="middle" fill="{GRAY}" font-size="10">100</text>']
    n = len(steps)
    for i, (lo, hi, mid, res) in enumerate(steps):
        y = 62 + i * 46
        color = GREEN if res == "正解！" else AMBER
        s.append(f'        <g opacity="0">{reveal(i, n, 12)}')
        s.append(f'          <text x="16" y="{y+22}" fill="{GRAY}" font-size="11">質問{i+1}回目</text>')
        s.append(f'          <rect x="{X0}" y="{y+8}" width="{X1-X0}" height="20" rx="5" fill="#141414" stroke="#333"/>')
        s.append(f'          <rect x="{px(lo):.1f}" y="{y+8}" width="{max(px(hi)-px(lo),2):.1f}" height="20" rx="5" '
                 f'fill="#1a2e0a" stroke="{GREEN}" stroke-width="1.5"/>')
        s.append(f'          <line x1="{px(mid):.1f}" y1="{y+2}" x2="{px(mid):.1f}" y2="{y+34}" stroke="{color}" stroke-width="2"/>')
        s.append(f'          <text x="{px(mid):.1f}" y="{y+45}" text-anchor="middle" fill="{color}" font-size="10">{mid}</text>')
        s.append(f'          <text x="{X1+14}" y="{y+23}" fill="{color}" font-size="11">{res}</text>')
        s.append(f'          <text x="96" y="{y+22}" text-anchor="end" fill="#666" font-size="10">{hi-lo+1}個</text>')
        s.append('        </g>')
    s.append(f'        <text x="360" y="{62+n*46+22}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '残りの個数は 100 → 50 → 24 → 12 → 6 → 3 と、質問のたびにおよそ半分になる</text>')
    return fig(720, 62 + n * 46 + 40, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 手数の伸び方の比較（目もりは10倍ずつ）
# ────────────────────────────────────────────────────────────
def fig_growth():
    sizes = [10, 100, 1000, 10000, 100000]
    linear = [10, 100, 1000, 10000, 100000]
    binary = [4, 7, 10, 14, 17]
    xs = [130 + i * 120 for i in range(5)]
    YB, YT = 285, 62

    def py(v):
        return YB - math.log10(v) / 5 * (YB - YT)

    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'データが10倍になったときの手数の増え方</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'よこ＝データの個数、たて＝調べた回数。どちらの目もりも1目もりで10倍</text>']
    for v in [1, 10, 100, 1000, 10000, 100000]:
        y = py(v)
        s.append(f'        <line x1="100" y1="{y:.1f}" x2="670" y2="{y:.1f}" stroke="#2a2a2a" stroke-width="1"/>')
        s.append(f'        <text x="94" y="{y+4:.1f}" text-anchor="end" fill="#666" font-size="10">{v:,}</text>')
    for i, sz in enumerate(sizes):
        s.append(f'        <text x="{xs[i]}" y="{YB+20}" text-anchor="middle" fill="{GRAY}" font-size="10">{sz:,}</text>')
    s.append(f'        <text x="385" y="{YB+40}" text-anchor="middle" fill="{GRAY}" font-size="11">データの個数</text>')

    for name, series, color, dy in [("逐次探索", linear, RED, -10), ("二分探索", binary, GREEN, 18)]:
        pts = " ".join(f"{xs[i]},{py(v):.1f}" for i, v in enumerate(series))
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3" '
                 f'stroke-dasharray="900" stroke-dashoffset="900">'
                 f'<animate attributeName="stroke-dashoffset" values="900;0;0" keyTimes="0;0.6;1" dur="9s" repeatCount="indefinite"/></polyline>')
        for i, v in enumerate(series):
            s.append(f'        <circle cx="{xs[i]}" cy="{py(v):.1f}" r="4" fill="{color}"/>')
            s.append(f'        <text x="{xs[i]}" y="{py(v)+dy:.1f}" text-anchor="middle" fill="{color}" font-size="10">{v:,}</text>')
    s.append(f'        <rect x="118" y="62" width="212" height="46" rx="8" fill="#141414" stroke="#333"/>')
    s.append(f'        <line x1="132" y1="78" x2="158" y2="78" stroke="{RED}" stroke-width="3"/>')
    s.append(f'        <text x="166" y="82" fill="{RED}" font-size="11">逐次探索（まっすぐ増える）</text>')
    s.append(f'        <line x1="132" y1="96" x2="158" y2="96" stroke="{GREEN}" stroke-width="3"/>')
    s.append(f'        <text x="166" y="100" fill="{GREEN}" font-size="11">二分探索（ほとんど増えない）</text>')
    return fig(700, 345, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図5: 幅優先探索が波のように広がる
# ────────────────────────────────────────────────────────────
MAZE = [
    "S.....#",
    ".####.#",
    ".#....#",
    ".#.##..",
    ".#..#.#",
    ".##.#.#",
    "......G",
]


def bfs_dist():
    rows, cols = len(MAZE), len(MAZE[0])
    start = goal = None
    for r in range(rows):
        for c in range(cols):
            if MAZE[r][c] == "S":
                start = (r, c)
            if MAZE[r][c] == "G":
                goal = (r, c)
    dist = {start: 0}
    prev = {start: None}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and MAZE[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                prev[(nr, nc)] = (r, c)
                q.append((nr, nc))
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = prev[node]
    return dist, list(reversed(path)), start, goal


def fig_bfs_wave():
    dist, path, start, goal = bfs_dist()
    maxd = max(dist.values())
    cell, x0, y0 = 38, 217, 62
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '幅優先探索: スタートから波のように1歩ずつ広がる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'マスの中の数字は「スタートから何歩か」。# は壁、. はまだ調べていない通路</text>']
    dur = 15
    for r in range(len(MAZE)):
        for c in range(len(MAZE[0])):
            x, y = x0 + c * cell, y0 + r * cell
            ch = MAZE[r][c]
            if ch == "#":
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" fill="#33302a" stroke="#4a453a"/>')
                s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+5}" text-anchor="middle" fill="#7a7060" font-size="14" font-weight="700">#</text>')
                continue
            d = dist.get((r, c))
            s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" fill="#141414" stroke="#333"/>')
            s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+5}" text-anchor="middle" fill="#4a4a4a" font-size="13">.</text>')
            if d is None:
                continue
            a = (1 - 0.18) * d / (maxd + 1)
            fillc = "#1a2e0a"
            s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
                     f'keyTimes="0;{a:.3f};{min(a+0.02,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
            s.append(f'          <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" fill="{fillc}" stroke="{GREEN}" stroke-width="1.2"/>')
            label = "S" if ch == "S" else ("G" if ch == "G" else str(d))
            col = AMBER if ch in "SG" else "#93D500"
            s.append(f'          <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+5}" text-anchor="middle" fill="{col}" '
                     f'font-size="{13 if ch in "SG" else 12}" font-weight="{700 if ch in "SG" else 400}">{label}</text>')
            s.append('        </g>')
    # 最短経路を最後に太線で描く
    pts = " ".join(f"{x0+c*cell+(cell-2)/2},{y0+r*cell+(cell-2)/2}" for r, c in path)
    s.append(f'        <polyline points="{pts}" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linejoin="round" '
             f'stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
             f'keyTimes="0;0.86;0.90;1" dur="{dur}s" repeatCount="indefinite"/></polyline>')
    s.append(f'        <text x="350" y="{y0+len(MAZE)*cell+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             f'ゴールは12歩。同じ歩数のマスがすべて出そろってから、次の歩数へ進む</text>')
    return fig(700, y0 + len(MAZE) * cell + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図6: 6通りの順番を全部試して最小を選ぶ
# ────────────────────────────────────────────────────────────
def fig_all_routes():
    routes = [
        ("郵便局 → 図書館 → カフェ", 26),
        ("郵便局 → カフェ → 図書館", 36),
        ("図書館 → 郵便局 → カフェ", 32),
        ("図書館 → カフェ → 郵便局", 36),
        ("カフェ → 郵便局 → 図書館", 32),
        ("カフェ → 図書館 → 郵便局", 26),
    ]
    n = len(routes)
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索: 6通りの順番をすべて試して、いちばん短いものを選ぶ</text>']
    for i, (name, cost) in enumerate(routes):
        y = 48 + i * 34
        best = (cost == 26)
        s.append(f'        <g opacity="0">{reveal(i, n + 2, 12)}')
        s.append(f'          <text x="30" y="{y+20}" fill="{GRAY}" font-size="11">{i+1}通り目</text>')
        s.append(f'          <text x="96" y="{y+20}" fill="#E0E0E0" font-size="12">学校 → {name} → 学校</text>')
        s.append(f'          <rect x="430" y="{y+4}" width="{cost*4}" height="20" rx="5" '
                 f'fill="#3a3a3a" stroke="#555"/>')
        s.append(f'          <text x="{430+cost*4+10}" y="{y+19}" fill="#ccc" font-size="11">{cost}分</text>')
        s.append('        </g>')
        if best:
            s.append(f'        <g opacity="0">{reveal(n + 1, n + 2, 12)}')
            s.append(f'          <rect x="430" y="{y+4}" width="{cost*4}" height="20" rx="5" fill="{GREEN}" stroke="{GREEN}"/>')
            s.append(f'          <rect x="22" y="{y}" width="{408+cost*4}" height="28" rx="8" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
            s.append('        </g>')
    s.append(f'        <text x="350" y="{48+n*34+26}" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700" opacity="0">'
             f'{reveal(n + 1, n + 2, 12)}'
             '最短は26分。逆回りの2通りは同じ時間になる</text>')
    return fig(700, 48 + n * 34 + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 本文
# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "後期の全体像 #sec-overview",
    "例題 #sec-examples",
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("01")

overview = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      前期のアルゴリズム論及び演習Iでは、「たくさんのデータの中から目的の1つを<strong>探す</strong>」方法を学びました。
      逐次探索、二分探索、ハッシュ法、そして迷路の幅優先探索です。
      後期のアルゴリズム論及び演習IIでは、一歩進んだ問題をあつかいます。
      <strong>やり方が何通りもあるとき、いちばん良いやり方を見つける</strong>という問題です。
    </p>

    <div class="analogy">
      駅から学校まで行く道は何通りもあります。遠回りでも空いている道、近いけれど坂がきつい道。
      「どの道が最も早く着くか」を決めるのが、後期のテーマである<strong>最適化</strong>です。
      カーナビの経路案内、宅配便の配送ルート、工場の作業順番は、すべて同じ問題として扱えます。
    </div>

{fig_roadmap()}

    <div class="concept-box">
      <h4>最適化（さいてきか / optimization）とは</h4>
      <p style="font-size:0.95rem">
        考えられる選び方をすべて「候補」とみなし、その中から<strong>ある基準でいちばん良いものを1つ選ぶ</strong>ことを最適化と呼びます。
        基準は問題によって変わります。移動時間なら「短いほど良い」、売上なら「大きいほど良い」です。
        後期の授業では、移動時間・移動コストを基準にした問題を中心にあつかいます。
      </p>
    </div>

{fig_search_vs_optimize()}

    <div class="concept-box">
      <h4>後期で身につける3つの道具</h4>
      <table>
        <tr><th>道具</th><th>いつ使うか</th><th>学ぶ回</th></tr>
        <tr><td><strong style="color:#76B900">グラフ</strong></td><td>地図・路線図・人のつながりを、コンピュータが扱える形に書き写すための表現方法</td><td>第3〜4回</td></tr>
        <tr><td><strong style="color:#76B900">ダイクストラ法</strong></td><td>出発点から各地点までの「最も安い行き方」を求める。カーナビの中身にあたる手法</td><td>第5〜7回</td></tr>
        <tr><td><strong style="color:#76B900">巡回セールスマン問題</strong></td><td>全ての地点を1回ずつ回って戻る最短ルートを求める。宅配便の配送計画にあたる問題</td><td>第8〜10回</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>評価方法と、毎回の課題</h4>
      <p style="font-size:0.95rem">定期試験はありません。<strong>毎回の演習課題の提出で100%</strong>の評価となります。</p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        課題は毎回同じ形です。<strong>Googleスライドを1本だけ作り、毎回3枚ずつ足していきます。</strong>
        15回ぶんを足し終えると、45枚の「自分が作ったアルゴリズム解説資料」ができあがります。
      </p>
      <table>
        <tr><th>枚</th><th>入れるもの</th></tr>
        <tr><td>A</td><td>その回のしくみを説明する図（<strong>自分で作ったもの</strong>）</td></tr>
        <tr><td>B</td><td>自分のパソコンで動かした実行画面のスクリーンショットと、読み取れること</td></tr>
        <tr><td>C</td><td>その回の問い2つへの答え（<strong>自分の実行結果の数値を根拠にする</strong>）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        説明する相手は<strong>前期を受けていない友達</strong>です。
        専門用語をそのまま並べても伝わりません。自分の言葉で書いてください。
      </p>
    </div>

    <div class="card" style="border-left:4px solid #76B900">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>Googleスライドを1本つくる（第1回だけ）</h3>
      </div>
      <div class="setup-step">
        <p class="step-title">Step 1: スライドを作る</p>
        <ol>
          <li>ブラウザで <strong>slides.google.com</strong> を開く（大学のGoogleアカウントでログイン）</li>
          <li><strong>空白</strong>を選んで新しいスライドを作る</li>
          <li>左上のファイル名を <strong>「アルゴリズム論II 解説資料 ○○（自分の名前）」</strong>に変える</li>
          <li>1枚目を表紙にして、授業名・自分の学籍番号・名前を書く</li>
        </ol>
      </div>
      <div class="setup-step">
        <p class="step-title">Step 2: 共有の設定をする</p>
        <ol>
          <li>右上の<strong>「共有」</strong>をクリック</li>
          <li>「一般的なアクセス」を <strong>「リンクを知っている全員」</strong>に変える</li>
          <li>権限は <strong>「閲覧者」</strong>のままでよい</li>
          <li><strong>「リンクをコピー」</strong>を押して、URLをどこかに控えておく</li>
        </ol>
        <p style="color:#888;font-size:0.85rem;margin-top:0.5rem">
          共有していないと、提出しても中身が見られず、未提出あつかいになります。必ず設定してください。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">Step 3: 毎回の出し方を覚える</p>
        <ol>
          <li>その回の3枚（A・B・C）をスライドに足す</li>
          <li><strong>ファイル → ダウンロード → PDFドキュメント</strong> でPDFに書き出す</li>
          <li>ManabaにPDFを提出し、<strong>コメント欄に共有URLを貼る</strong></li>
        </ol>
      </div>
      <div class="note-warn">
        <strong>スライドは15回ぶんずっと同じ1本を使います。</strong>毎回新しく作らないでください。
        回ごとに「第○回: テーマ名」の見出しスライドを入れておくと、あとで見返しやすくなります。
      </div>
    </div>

    <div class="note-warn">
      <strong>後期の授業で必要なもの:</strong> Visual Studio Code（VS Code）と Python が動くパソコン。
      前期に用意した環境をそのまま使います。動かなくなっている場合は、第1回の授業中に申し出てください。
    </div>"""

ex1_body = f"""      <p>前期に学んだ二分探索を、数当てゲームの形で思い出します。
      1から100までの中に「秘密の数」が1つあり、コンピュータが<strong>まん中を聞く</strong>作戦で当てにいきます。</p>

{code('AL2-01-ex1.py')}

{fig_binary_steps()}

{run('a01_ex1_result.png', '質問のたびに、探す範囲が 100個 → 50個 → 24個 → 12個 → 6個 → 3個 と、およそ半分ずつ減っています。'
     '1から100までの100個の中から、たった<strong>6回</strong>の質問で73を当てられました。'
     '「まん中を聞いて、外れた半分を捨てる」という作戦が二分探索です。')}"""

ex2_body = f"""      <p>二分探索がどれくらい得なのかを、逐次探索と比べて数で確かめます。
      逐次探索は先頭から1つずつ調べる方法、二分探索はまん中と比べて半分を捨てる方法です。</p>

{code('AL2-01-ex2.py')}

{fig_growth()}

{run('a01_ex2_result.png', 'データの個数が10倍になるたびに、逐次探索の回数も<strong>10倍</strong>に増えています（10 → 100 → 1000 → 10000 → 100000）。'
     '一方の二分探索は 4 → 7 → 10 → 14 → 17 と、<strong>3〜4回ずつしか増えません</strong>。'
     'データが10万個あっても17回で見つかります。同じ答えにたどり着くのに、手数がまったく違うという点が重要です。')}

{notion('データの個数が10倍になったとき、逐次探索の回数と二分探索の回数がそれぞれ何倍になったかを書く。'
        'あわせて、10万個のデータから1つ探すとき、逐次探索と二分探索で何回の差があるかを書く。')}"""

ex3_body = f"""      <p>前期の最後にあつかった幅優先探索を、迷路で思い出します。
      幅優先探索は、スタートから<strong>1歩で行ける場所をすべて調べ、次に2歩で行ける場所をすべて調べる</strong>という順番で進みます。
      波紋が広がるように調べていくため、最初にゴールへ届いたときの歩数が必ず最短になります。</p>

{code('AL2-01-ex3.py')}

{fig_bfs_wave()}

{run('a01_ex3_result.png', 'スタートからゴールまで<strong>12歩</strong>で着く道が見つかりました。'
     '2つ目の迷路図で <code>*</code> が付いているマスが通り道です。左端の列をまっすぐ下り、いちばん下の行を右へ進む道になっています。'
     '幅優先探索は「歩数が少ない順」に調べるので、最初に届いた道がそのまま最短経路になります。')}

    <div class="note-warn">
      <strong>後期につながる注意点:</strong> 幅優先探索が求めるのは<strong>歩数が最も少ない道</strong>です。
      1歩の重さがマスによって違う場合、たとえば砂地は3秒、舗装路は1秒という迷路では、幅優先探索は最短時間の道を求められません。
      重さの違いをあつかう方法が、第5回から学ぶダイクストラ法です。
    </div>"""

ex4_body = f"""      <p>後期のテーマである最適化を、いちばん小さな形で体験します。
      学校を出発して3か所を回り、学校へ戻ります。回る順番は全部で6通りあり、順番によって合計時間が変わります。
      6通りをすべて試して、いちばん短い順番を選びます。</p>

    <div class="analogy">
      配達のアルバイトで、3軒の家に荷物を届けて営業所に戻る場面を思い浮かべてください。
      どの家から回るかで、かかる時間が変わります。時間を最も短くする回り方を見つける問題が、第8回から学ぶ巡回セールスマン問題です。
    </div>

{code('AL2-01-ex4.py')}

{fig_all_routes()}

{run('a01_ex4_result.png', '6通りすべての合計時間が表示され、最短は<strong>26分</strong>でした。'
     '「学校 → 郵便局 → 図書館 → カフェ → 学校」と「学校 → カフェ → 図書館 → 郵便局 → 学校」の2つが同じ26分になっています。'
     '2つは進む向きが逆なだけで、通る道は同じだからです。'
     'すべての候補を書き出して比べる方法を<strong>全探索</strong>と呼びます。')}

    <div class="note-warn">
      <strong>後期につながる注意点:</strong> 回る場所が3か所なら6通りですが、場所が増えると候補の数は急激に増えます。
      4か所で24通り、5か所で120通り、10か所では362880通りです。
      全探索が使えなくなる大きさの問題をどう解くかが、第9回・第10回のテーマになります。
    </div>

{notion('例題4の実行結果から、6通りの合計時間をすべて書き出す。'
        'そのうえで、最短の順番が2つある理由を自分の言葉で説明する。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを、実際に自分のパソコンで実行してください。
    まず作業フォルダを用意します。</p>

{setup_guide('01', ['AL2-01-ex1.py', 'AL2-01-ex2.py', 'AL2-01-ex3.py', 'AL2-01-ex4.py'])}

{keywords([
    ('最適化', 'さいてきか / optimization', '考えられる選び方の中から、ある基準でいちばん良いものを1つ選ぶこと。後期の授業全体のテーマ。'),
    ('全探索', 'ぜんたんさく / brute force', '考えられる候補をすべて書き出して1つずつ調べる方法。必ず正しい答えが出るが、候補が増えると時間がかかる。'),
    ('二分探索', 'にぶんたんさく / binary search', '並んでいるデータのまん中と比べ、外れた半分を捨てることをくり返す探し方。'),
    ('幅優先探索', 'はばゆうせんたんさく / BFS', 'スタートから1歩で行ける場所、2歩で行ける場所、と近い順に調べる探し方。最短の歩数が求まる。'),
    ('計算量', 'けいさんりょう / complexity', 'データが増えたときに手数がどれくらい増えるかを表す目安。O(n) や O(log n) のように書く。'),
])}

{example(1, '数当てゲームをコンピュータに解かせる（二分探索の復習）', ex1_body)}

{example(2, '逐次探索と二分探索の手数を比べる（計算量の復習）', ex2_body)}

{example(3, '迷路を幅優先探索で解く（探索の復習）', ex3_body)}

{example(4, '全部の順番を試して、いちばん短いものを選ぶ（後期の予告）', ex4_body)}"""

ans = answers([
    ("確かめ用の数値", """        <p><strong>問い1（学校—カフェを20分にしたとき）</strong></p>
        <table>
          <tr><th>順番</th><th>20分にする前</th><th>20分にしたあと</th></tr>
          <tr><td>学校 → 郵便局 → 図書館 → カフェ → 学校</td><td>26分</td><td>41分</td></tr>
          <tr><td>学校 → 郵便局 → カフェ → 図書館 → 学校</td><td>36分</td><td><strong style="color:#76B900">36分</strong></td></tr>
          <tr><td>学校 → 図書館 → 郵便局 → カフェ → 学校</td><td>32分</td><td>47分</td></tr>
        </table>
        <p style="margin-top:0.6rem">いちばん短い順番は<strong>36分</strong>に変わります。
        書き換える前に1位だった26分の順番は41分になり、1位ではなくなります。</p>
        <p style="margin-top:0.8rem"><strong>問い2（二分探索の回数）</strong>: 4 → 7 → 10 → 14 → 17 回。
        データが10倍になっても3〜4回しか増えません。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-overview", "1", "後期に学ぶこと", overview),
    section("sec-examples", "2", "例題", examples),
    slides_for("01", SLIDES),
    rubric_section("01"),
    ans,
])

write("01", NAV, body)
