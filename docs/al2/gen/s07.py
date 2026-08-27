# -*- coding: utf-8 -*-
"""第7回: ダイクストラ法（3）迷路への応用 の本文を組み立てる。"""
import heapq
from collections import deque
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

COST5 = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

FLAT = [[1] * 8 for _ in range(8)]
RIVER = [[9 if (c == 3 and r != 4) else 1 for c in range(8)] for r in range(8)]
FOREST = [
    [1, 1, 5, 5, 5, 5, 5, 1],
    [1, 1, 1, 5, 5, 5, 5, 1],
    [5, 1, 1, 1, 5, 5, 5, 1],
    [5, 5, 1, 1, 1, 5, 5, 1],
    [5, 5, 5, 1, 1, 1, 5, 1],
    [5, 5, 5, 5, 1, 1, 1, 1],
    [5, 5, 5, 5, 5, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def solve(cost_map):
    size = len(cost_map)
    start, goal = (0, 0), (size - 1, size - 1)
    INF = float("inf")
    dist = {(r, c): INF for r in range(size) for c in range(size)}
    prev = {(r, c): None for r in range(size) for c in range(size)}
    dist[start] = 0
    pq = [(0, start)]
    done = set()
    order = []
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        order.append((u, d))
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and d + cost_map[nr][nc] < dist[(nr, nc)]:
                dist[(nr, nc)] = d + cost_map[nr][nc]
                prev[(nr, nc)] = u
                heapq.heappush(pq, (dist[(nr, nc)], (nr, nc)))
    p, n = [], goal
    while n is not None:
        p.append(n)
        n = prev[n]
    return list(reversed(p)), dist[goal], dist, order


def bfs_route(cost_map):
    size = len(cost_map)
    start, goal = (0, 0), (size - 1, size - 1)
    came = {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            break
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in came:
                came[(nr, nc)] = u
                q.append((nr, nc))
    p, n = [], goal
    while n is not None:
        p.append(n)
        n = came[n]
    p.reverse()
    return p, sum(cost_map[r][c] for r, c in p[1:])


# ────────────────────────────────────────────────────────────
# 図1: マスのコストは辺の重みになる
# ────────────────────────────────────────────────────────────
def fig_cell_to_edge():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路のマスのコストは、グラフの「辺の重み」として表す</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '「そのマスに入るのにかかる時間」を、そのマスへ向かう辺の重みにする</text>']
    cells = [("A", 1, 60), ("B", 9, 230), ("C", 1, 400), ("D", 1, 570)]
    for name, v, x in cells:
        deep = v >= 9
        s.append(f'        <rect x="{x-36}" y="90" width="72" height="72" rx="10" '
                 f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#444"}" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="126" text-anchor="middle" fill="{AMBER if deep else "#ccc"}" font-size="22" font-weight="700">{v}</text>')
        s.append(f'        <text x="{x}" y="150" text-anchor="middle" fill="{GRAY}" font-size="11">マス{name}</text>')
    for i in range(3):
        x1 = cells[i][2] + 36
        x2 = cells[i + 1][2] - 36
        w = cells[i + 1][1]
        s.append(f'        <line x1="{x1}" y1="126" x2="{x2}" y2="126" stroke="{GREEN}" stroke-width="2"/>')
        s.append(f'        <polygon points="{x2},126 {x2-9},121 {x2-9},131" fill="{GREEN}"/>')
    s.append(f'        <text x="350" y="196" text-anchor="middle" fill="#ccc" font-size="12">'
             'マスAからマスBへ進むときは、マスBのコスト9を払う</text>')
    s.append(f'        <rect x="90" y="216" width="520" height="76" rx="12" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="242" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'コードの上では、迷路をグラフに変換する必要はない</text>')
    s.append(f'        <text x="350" y="264" text-anchor="middle" fill="#ccc" font-size="11">'
             'となりのマスへ進むときに <tspan font-family="JetBrains Mono, monospace" fill="#cdd6f4">total + cost_map[nr][nc]</tspan> と書けば、</text>')
    s.append(f'        <text x="350" y="282" text-anchor="middle" fill="#ccc" font-size="11">'
             'それがそのまま「辺の重みを足す」ことになっている</text>')
    return fig(700, 306, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 幅優先探索とダイクストラ法の広がり方
# ────────────────────────────────────────────────────────────
def fig_spread():
    route, best, dist, order = solve(COST5)
    bfs_p, bfs_cost = bfs_route(COST5)
    # 幅優先探索の歩数
    size = 5
    steps = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        u = q.popleft()
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in steps:
                steps[(nr, nc)] = steps[u] + 1
                q.append((nr, nc))

    cell = 52
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '広がり方のちがい: 歩数の順か、コストの順か</text>']
    panels = [("幅優先探索: 歩数の順に広がる", 34, AMBER, steps, sorted(steps, key=lambda k: steps[k])),
              ("ダイクストラ法: コストの順に広がる", 386, GREEN, dist, [u for u, d in order])]
    for title, x0, color, table, seq in panels:
        s.append(f'        <text x="{x0+130}" y="54" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 66
        for r in range(5):
            for c in range(5):
                x, y = x0 + c * cell, y0 + r * cell
                v = COST5[r][c]
                deep = v >= 9
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" '
                         f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#2e2e2e"}"/>')
                s.append(f'        <text x="{x+8}" y="{y+16}" fill="{AMBER if deep else "#555"}" font-size="10">{v}</text>')
        for k, u in enumerate(seq):
            r, c = u
            x, y = x0 + c * cell, y0 + r * cell
            a = (1 - 0.16) * k / len(seq)
            s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
                     f'keyTimes="0;{a:.3f};{min(a+0.015,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
            s.append(f'          <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" fill="#1a2e0a" stroke="{color}" stroke-width="1.6"/>')
            s.append(f'          <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+8}" text-anchor="middle" fill="{color}" font-size="16" font-weight="700">{table[u]}</text>')
            s.append('        </g>')
        note = "数字はスタートからの歩数" if color == AMBER else "数字はスタートからの合計コスト"
        s.append(f'        <text x="{x0+130}" y="{y0+5*cell+22}" text-anchor="middle" fill="{GRAY}" font-size="11">{note}</text>')
    s.append('        <line x1="350" y1="44" x2="350" y2="356" stroke="#333" stroke-width="1"/>')
    s.append(f'        <text x="350" y="{66+5*cell+48}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'ダイクストラ法は、9のマスをできるだけ後回しにして広がっていく</text>')
    return fig(700, 66 + 5 * cell + 66, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 迷路の大きさと実行時間
# ────────────────────────────────────────────────────────────
def fig_scale():
    rows = [("50×50", 2500, 0.002), ("100×100", 10000, 0.008),
            ("200×200", 40000, 0.038), ("400×400", 160000, 0.182)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'マスの数が4倍になっても、時間は4倍すこしにしかならない</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '秒数は測ったときの一例。パソコンによって変わる</text>']
    for i, (size, cells, t) in enumerate(rows):
        y = 66 + i * 52
        w = t / 0.182 * 400
        s.append(f'        <text x="24" y="{y+22}" fill="#E0E0E0" font-size="12" font-weight="700">{size}</text>')
        s.append(f'        <text x="118" y="{y+22}" fill="{GRAY}" font-size="10">{cells:,}マス</text>')
        s.append(f'        <rect x="200" y="{y+6}" width="{max(w,3):.0f}" height="22" rx="5" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{200+max(w,3)+10:.0f}" y="{y+23}" fill="{GREEN}" font-size="12" font-weight="700">{t:.3f}秒</text>')
    y = 66 + 4 * 52 + 10
    s.append(f'        <rect x="24" y="{y}" width="652" height="60" rx="10" fill="#2b1a00" stroke="{RED}"/>')
    s.append(f'        <text x="350" y="{y+24}" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             '第4回の全探索: 6マス×6マス（36マス）で 約7秒</text>')
    s.append(f'        <text x="350" y="{y+45}" text-anchor="middle" fill="#ccc" font-size="11">'
             'ダイクストラ法なら160,000マスが1秒もかからない。あつかえる大きさがまるで違う</text>')
    return fig(700, y + 78, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 地形が変わると通る道が変わる
# ────────────────────────────────────────────────────────────
def fig_terrains():
    maps = [(FLAT, "地形A 平地だけ"), (RIVER, "地形B 川がある"), (FOREST, "地形C 森がある")]
    cell = 24
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ大きさの地図でも、地形が変わると通る道が変わる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '1 = 平地1秒　／　5 = 森5秒　／　9 = 川9秒</text>']
    for i, (cmap, title) in enumerate(maps):
        route, best, dist, order = solve(cmap)
        x0 = 24 + i * 228
        s.append(f'        <text x="{x0+96}" y="72" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">{title}</text>')
        y0 = 84
        mark = set(route)
        for r in range(8):
            for c in range(8):
                x, y = x0 + c * cell, y0 + r * cell
                v = cmap[r][c]
                on = (r, c) in mark
                if v >= 9:
                    fill, stroke, tc = "#2b1a00", "#5a3d00", AMBER
                elif v >= 5:
                    fill, stroke, tc = "#1e1a10", "#3d3520", "#8a7a50"
                else:
                    fill, stroke, tc = "#141414", "#2a2a2a", "#555"
                if on:
                    fill, stroke, tc = "#1a2e0a", GREEN, "#93D500"
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" fill="{fill}" stroke="{stroke}"/>')
                s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+4}" text-anchor="middle" fill="{tc}" font-size="10">{v}</text>')
        pts = " ".join(f"{x0+c*cell+(cell-2)/2},{y0+r*cell+(cell-2)/2}" for r, c in route)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="2.5" '
                 f'stroke-linejoin="round" stroke-dasharray="600" stroke-dashoffset="600">'
                 f'<animate attributeName="stroke-dashoffset" values="600;0;0" keyTimes="0;0.7;1" dur="9s" repeatCount="indefinite"/></polyline>')
        s.append(f'        <text x="{x0+96}" y="{y0+8*cell+20}" text-anchor="middle" fill="#ccc" font-size="11">'
                 f'{len(route)-1}歩 ／ 合計 {best}秒</text>')
    s.append(f'        <text x="350" y="{84+8*cell+48}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'どの地形でも14歩・14秒。歩数も合計も同じだが、通る道はまったく違う</text>')
    return fig(700, 84 + 8 * cell + 66, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "迷路とグラフ #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題1の2つの経路"),
    ("#sec-examples", "tag-example", "観察記録", "例題3の実行時間"),
    ("#sec-standard", "tag-standard", "標準課題1", "コストを変えると？"),
    ("#sec-standard", "tag-standard", "標準課題2", "使い分けの表"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回・第6回では、駅と路線からなるグラフでダイクストラ法を動かしました。
      第7回では、同じダイクストラ法を<strong>床コスト付きの迷路</strong>に使います。
      第3回で確かめたとおり、迷路は「1マスが頂点、となり合うマスのつながりが辺」のグラフです。
      マスごとのコストは、そのマスへ<strong>入る</strong>ときに払う重みとして扱います。
    </p>

    <div class="analogy">
      災害時の避難経路を思い浮かべてください。地図の上では最短の道でも、
      がれきで通りにくい道と、遠回りでも整備された道があります。
      「距離が短い道」ではなく「早く着く道」を知りたいとき、
      道ごとの通りにくさを数値にしてダイクストラ法にかけると、答えが求まります。
    </div>

{fig_cell_to_edge()}

    <div class="concept-box">
      <h4>迷路をグラフに変換しなくてよい理由</h4>
      <p style="font-size:0.95rem">
        第3回の例題4では、迷路をわざわざ隣接リストに書き直してから解きました。
        じつは書き直さなくても、<strong>となりのマスを調べるところで直接コストを足せば</strong>同じことになります。
      </p>
<pre><span class="code-label">Python ── となりのマスへ進む部分</span>
<span class="kw">for</span> dr, dc <span class="kw">in</span> [(-<span class="num">1</span>, <span class="num">0</span>), (<span class="num">1</span>, <span class="num">0</span>), (<span class="num">0</span>, -<span class="num">1</span>), (<span class="num">0</span>, <span class="num">1</span>)]:
    nr = r + dr
    nc = c + dc
    new_total = total + cost_map[nr][nc]   <span class="cmt"># ← ここが「辺の重みを足す」ことになっている</span></pre>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        <code>cost_map[nr][nc]</code> が、そのマスへ入る辺の重みです。
        隣接リストを作る手間もメモリもいらないので、迷路のように「となりが計算で分かる」問題では、
        書き直さずに直接あつかうほうがふつうです。
      </p>
    </div>

{fig_spread()}

    <div class="concept-box">
      <h4>2つの探索の広がり方のちがい</h4>
      <table>
        <tr><th></th><th>幅優先探索</th><th>ダイクストラ法</th></tr>
        <tr><td>広がる順番</td><td>歩数が少ないマスから</td><td>合計コストが小さいマスから</td></tr>
        <tr><td>使う入れもの</td><td>キュー（<code>deque</code>）</td><td>優先度付きキュー（<code>heapq</code>）</td></tr>
        <tr><td>求まるもの</td><td>歩数がいちばん少ない経路</td><td>合計コストがいちばん小さい経路</td></tr>
        <tr><td>すべてのマスのコストが同じとき</td><td colspan="2" style="text-align:center">答えは一致する</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        すべてのマスのコストが1なら、合計コストは歩数と同じ値になります。
        つまり<strong>幅優先探索は、ダイクストラ法の特別な場合</strong>だと言えます。
      </p>
    </div>"""

ex1_body = f"""      <p>第4回の例題3で使った迷路を、幅優先探索とダイクストラ法の両方で解いて比べます。
      迷路も経路も同じプログラムの中であつかい、結果を並べて表示します。</p>

{code('AL2-07-ex1.py')}

{run('a07_ex1_result.png', '幅優先探索は<strong>8歩・16秒</strong>、ダイクストラ法は<strong>12歩・12秒</strong>という結果でした。'
     '迷路の絵を見ると、幅優先探索の経路は 9 のマス（ぬかるみ）を1つ通っていますが、'
     'ダイクストラ法の経路は 9 のマスを1つも通らず、すべて 1 のマスだけを歩いています。'
     '第4回では3通りの行き方を手で用意して比べましたが、ダイクストラ法は<strong>自動で</strong>いちばん安い経路を見つけています。')}

{notion('例題1の実行結果から、2つの経路の歩数と合計秒数を表にまとめる。'
        'あわせて、2つの迷路の絵を見比べて、経路がどこで分かれているかを言葉で説明する。')}"""

ex2_body = f"""      <p>ダイクストラ法は、ゴールの最小コストだけを求めているわけではありません。
      止めずに最後まで動かすと、<strong>すべてのマスへの最小コスト</strong>が同時に求まります。</p>

{code('AL2-07-ex2.py')}

{run('a07_ex2_result.png', '確定した順番は (0,0)=0秒 → (0,1)=1秒 → (0,2)=2秒 → (1,2)=3秒 … と、'
     '<strong>コストが小さいマスから順</strong>になっています。'
     'いちばん最後に確定した (3,3) は20秒で、9のマスに囲まれているためコストが高くなっています。'
     '真ん中の表は、スタートからそれぞれのマスへ行くのにかかる最小の秒数です。'
     '9のマスがある右上の (0,3) は11秒、(0,4) は12秒と、遠回りしてたどり着く形になっています。')}"""

ex3_body = f"""      <p>迷路を大きくしていったとき、ダイクストラ法がどれくらいの時間で解けるかを測ります。
      50マス四方から400マス四方まで、4通りの大きさを試します。</p>

{code('AL2-07-ex3.py')}

{fig_scale()}

{run('a07_ex3_result.png', '400マス四方（160,000マス）でも<strong>0.2秒ほど</strong>で解けています。'
     'マスの数が4倍になるたびに、かかる時間も4倍すこしずつ増えています。'
     '第4回の例題4で、全探索が6マス四方（36マス）に約7秒かかったことと比べてください。'
     '全探索では6マス四方が限界でしたが、ダイクストラ法なら400マス四方が一瞬で終わります。'
     '秒数はパソコンの性能で変わるので、自分の結果が画像と一致しなくても問題ありません。')}

{notion('例題3の表から、4つの大きさそれぞれの「マスの数」「最小コスト」「かかった時間」を書き写す。'
        'あわせて、マスの数が4倍になったとき、かかった時間が何倍になったかを計算して書く。')}"""

ex4_body = f"""      <p>同じ大きさ・同じスタートとゴールで、地形だけを3通りに変えて経路を比べます。
      1 は平地（1秒）、5 は森（5秒）、9 は川（9秒）です。</p>

{code('AL2-07-ex4.py')}

{fig_terrains()}

{run('a07_ex4_result.png', '3つの地形はどれも<strong>14歩・14秒</strong>で、歩数も合計コストも同じです。'
     'しかし通る道はまったく違います。'
     '地形Bでは、まん中の川を避けて4行目の橋まで下りてから右へわたっています。'
     '地形Cでは、ななめに伸びる細い平地を階段状にたどり、森を1マスも通っていません。'
     'ダイクストラ法は地形を見て判断しているわけではなく、'
     '<strong>コストの小さいマスから順に広げる</strong>という手順だけで、高いマスを自然に避けています。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('07', ['AL2-07-ex1.py', 'AL2-07-ex2.py', 'AL2-07-ex3.py', 'AL2-07-ex4.py'])}

{keywords([
    ('床コスト', 'ゆかコスト / terrain cost', 'マスごとに決まっている「そのマスを通り抜けるのにかかる時間や手間」。そのマスへ入る辺の重みとして扱う。'),
    ('コスト等高線', 'コストとうこうせん', 'スタートから同じコストでたどり着けるマスを結んだ線。ダイクストラ法はコスト等高線を外へ広げるように進む。'),
    ('最短経路木', 'さいたんけいろぎ / shortest path tree', 'すべての頂点への最短経路をまとめた形。<code>came_from</code> の記録がそのまま最短経路木になっている。'),
    ('一様コスト', 'いちようコスト', 'すべてのマスのコストが同じであること。一様コストのとき、ダイクストラ法と幅優先探索は同じ答えを出す。'),
])}

{example(1, '床コスト付き迷路を2つの方法で解く', ex1_body)}

{example(2, 'すべてのマスへの最小コストを見る', ex2_body)}

{example(3, '迷路を大きくして実行時間を測る', ex3_body)}

{example(4, '地形を変えると経路はどう変わるか', ex4_body)}"""

std1_body = """      <p>例題1のファイル <code>AL2-07-ex1.py</code> を開き、迷路のいちばん下の行を高いコストに書き換えます。
      下の道路が水びたしになり、通り抜けに9秒かかるようになったという設定です（ゴールのマスだけは 1 のまま）。</p>

<pre><span class="code-label">Python ── 書き換えたあとの cost_map</span>
cost_map = [
    [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">9</span>, <span class="num">1</span>],
    [<span class="num">9</span>, <span class="num">9</span>, <span class="num">1</span>, <span class="num">9</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">9</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">9</span>, <span class="num">9</span>, <span class="num">9</span>, <span class="num">1</span>],
    [<span class="num">9</span>, <span class="num">9</span>, <span class="num">9</span>, <span class="num">9</span>, <span class="num">1</span>],   <span class="cmt"># ← いちばん下の行の左から4つを 1 から 9 に変える</span>
]</pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、幅優先探索とダイクストラ法それぞれの歩数と合計秒数を予測してNotionに書く</li>
          <li>いちばん下の行の左から4つを 1 から 9 に書き換えて保存し、実行する</li>
          <li>実際の結果を記録し、予測と比べる</li>
          <li>2つの経路の絵を見比べて、書き換える前とどう変わったかを書く</li>
        </ol>
      </div>

      <table>
        <tr><th>方法</th><th>書き換える前</th><th>予測</th><th>実際</th></tr>
        <tr><td>幅優先探索</td><td>8歩 ／ 16秒</td><td></td><td></td></tr>
        <tr><td>ダイクストラ法</td><td>12歩 ／ 12秒</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> ダイクストラ法の歩数は12歩から減りましたが、合計秒数は12秒から増えました。
      「歩数が減ったのに合計秒数が増える」ということが起きる理由を説明してください。</p>
"""

std2_body = """      <p>例題1から例題4までの結果をもとに、幅優先探索とダイクストラ法の使い分けを表にまとめます。
      表はNotionに作り、空欄をすべて埋めてください。</p>

      <table>
        <tr><th>比べる点</th><th>幅優先探索</th><th>ダイクストラ法</th></tr>
        <tr><td>使う入れもの</td><td></td><td></td></tr>
        <tr><td>広がる順番</td><td></td><td></td></tr>
        <tr><td>求まる経路</td><td></td><td></td></tr>
        <tr><td>例題1での結果（歩数／秒数）</td><td></td><td></td></tr>
        <tr><td>すべてのマスのコストが1のとき</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem">表を作ったうえで、次の3つの場面には、それぞれどちらが向いているかを<strong>理由つきで</strong>答えてください。</p>
      <ul class="point-list">
        <li><strong>場面A:</strong> パズルゲームで「最も少ない手数で解けるか」を判定する</li>
        <li><strong>場面B:</strong> 自転車のナビで「上り坂を避けて最も早く着く道」を案内する</li>
        <li><strong>場面C:</strong> すべてのマスの移動時間が同じ、まっさらな地図で最短経路を求める</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    標準課題1は<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, '右の列を通りにくくすると経路はどう変わるか', std1_body)}
{notion('2つの方法についての予測と実際の表、経路がどう変わったかの説明、および「歩数と秒数のどちらが変わったか」の理由。')}

{standard(2, '幅優先探索とダイクストラ法の使い分け', std2_body)}
{notion('5行の比較表（空欄をすべて埋める）と、場面A・場面B・場面Cそれぞれに向いている方法とその理由。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第7回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題1</strong>: 2つの経路の歩数と秒数の表、経路が分かれる場所の説明</li>
        <li><strong>例題3</strong>: 4つの大きさの表、時間が何倍になったかの計算</li>
        <li><strong>標準課題1</strong>: 予測と実際の表、経路の変化、歩数と秒数の理由</li>
        <li><strong>標準課題2</strong>: 比較表、場面A・B・Cへの答えと理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: いちばん下の行を9にしたときの結果", """        <table>
          <tr><th>方法</th><th>書き換える前</th><th>書き換えたあと</th></tr>
          <tr><td>幅優先探索</td><td>8歩 ／ 16秒</td><td>8歩 ／ <strong style="color:#FF5252">48秒</strong></td></tr>
          <tr><td>ダイクストラ法</td><td>12歩 ／ 12秒</td><td><strong style="color:#76B900">8歩 ／ 16秒</strong></td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>幅優先探索:</strong> 経路も歩数もまったく変わりません（左の列を下りて、下の行を右へ進む道）。
        しかし通る道の上のマスが 1 から 9 に変わったため、合計秒数だけが16秒から<strong>48秒</strong>に増えています。
        幅優先探索はコストを1つも見ていないので、下の行が通りにくくなったことに気づけません。</p>
        <p style="margin-top:0.6rem"><strong>ダイクストラ法:</strong> 経路が<strong>まったく別の道</strong>に変わります。</p>
<pre><span class="code-label">Terminal ── 書き換えたあとのダイクストラ法の経路</span>
     1*   1*   1*   9*   1*
     9    9    1    9    1*
     1    1    1    9    1*
     1    9    9    9    1*
     9    9    9    9    1*</pre>
        <p style="margin-top:0.8rem">上の行を右へ進み、9のマスを1つだけ通ってから、右の列をまっすぐ下りる道になりました。
        合計は 1+1+9+1+1+1+1+1 = <strong>16秒</strong>です。</p>
        <p style="margin-top:0.6rem"><strong>「歩数が減ったのに合計秒数が増える」理由:</strong>
        ダイクストラ法が選んでいるのは、あくまで<strong>そのときの地形でいちばん安い道</strong>です。
        書き換える前は、遠回り（12歩）をしてでも 1 のマスだけを歩くほうが安く（12秒）済みました。
        書き換えたあとは、その遠回りの道がいちばん下の行を通っていたため、
        同じ道を歩くと 1+1+1+1+1+1+9+9+9+1 のように高くついてしまいます。
        そこで、9のマスを1つだけ通る短い道（8歩・16秒）に乗りかえたということです。</p>
        <p style="margin-top:0.6rem">つまり、<strong>歩数はダイクストラ法が最小にしようとしている値ではありません</strong>。
        結果として歩数が減ることも増えることもあります。
        ダイクストラ法が保証するのは「合計コストが、そのときの地形で最小であること」だけです。
        書き換えたあとの16秒は、幅優先探索の48秒より3分の1の時間であり、確かに最小になっています。</p>"""),
    ("標準課題2: 使い分けの表と答え", """        <table>
          <tr><th>比べる点</th><th>幅優先探索</th><th>ダイクストラ法</th></tr>
          <tr><td>使う入れもの</td><td>キュー（<code>deque</code>）</td><td>優先度付きキュー（<code>heapq</code>）</td></tr>
          <tr><td>広がる順番</td><td>歩数が少ないマスから</td><td>合計コストが小さいマスから</td></tr>
          <tr><td>求まる経路</td><td>歩数がいちばん少ない経路</td><td>合計コストがいちばん小さい経路</td></tr>
          <tr><td>例題1での結果</td><td>8歩 ／ 16秒</td><td>12歩 ／ 12秒</td></tr>
          <tr><td>コストがすべて1のとき</td><td colspan="2" style="text-align:center">同じ答えになる</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>場面A（最も少ない手数で解けるか）: 幅優先探索</strong><br>
        知りたいのは手数の少なさです。1手が1歩に相当し、どの手も同じ重さなので、コストを考える必要がありません。
        幅優先探索のほうが仕組みが簡単で、優先度付きキューを使わないぶん速く動きます。</p>
        <p style="margin-top:0.6rem"><strong>場面B（上り坂を避けて最も早く着く道）: ダイクストラ法</strong><br>
        上り坂と平地では、同じ距離でもかかる時間が違います。
        坂の勾配に応じたコストをマスごとに決めれば、ダイクストラ法が自動で坂を避ける経路を選びます。
        幅優先探索では、距離が短いというだけで急な坂の道を案内してしまいます。</p>
        <p style="margin-top:0.6rem"><strong>場面C（すべての移動時間が同じ地図）: 幅優先探索</strong><br>
        コストがすべて同じなら、2つの方法は同じ答えを出します。
        同じ答えが出るなら、簡単で速いほうを選びます。
        ダイクストラ法でも正しい答えは出ますが、優先度付きキューの出し入れがむだになります。</p>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        重みに差があるかどうかで選びます。差がなければ幅優先探索、差があればダイクストラ法です。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "迷路とグラフ", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("07", NAV, body)
