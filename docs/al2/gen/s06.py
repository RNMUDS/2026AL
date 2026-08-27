# -*- coding: utf-8 -*-
"""第6回: ダイクストラ法（2）実装入門 の本文を組み立てる。"""
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

COST_MAP = [
    [1, 1, 1, 9, 9, 9, 1, 1, 1, 1],
    [9, 9, 1, 9, 1, 1, 1, 9, 9, 1],
    [1, 1, 1, 9, 1, 9, 9, 9, 1, 1],
    [1, 9, 9, 9, 1, 1, 1, 9, 1, 9],
    [1, 1, 1, 1, 1, 9, 1, 9, 1, 1],
    [9, 9, 9, 9, 1, 9, 1, 1, 1, 9],
    [1, 1, 1, 9, 1, 9, 9, 9, 1, 1],
    [1, 9, 1, 9, 1, 1, 1, 9, 9, 1],
    [1, 9, 1, 1, 1, 9, 1, 1, 1, 1],
    [1, 1, 1, 9, 1, 1, 1, 9, 9, 1],
]


def dijkstra_route():
    import heapq
    rows = cols = 10
    start, goal = (0, 0), (9, 9)
    INF = float("inf")
    dist = {(r, c): INF for r in range(rows) for c in range(cols)}
    prev = {(r, c): None for r in range(rows) for c in range(cols)}
    dist[start] = 0
    pq = [(0, start)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        if u == goal:
            break
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and d + COST_MAP[nr][nc] < dist[(nr, nc)]:
                dist[(nr, nc)] = d + COST_MAP[nr][nc]
                prev[(nr, nc)] = u
                heapq.heappush(pq, (dist[(nr, nc)], (nr, nc)))
    p, n = [], goal
    while n is not None:
        p.append(n)
        n = prev[n]
    return list(reversed(p)), dist[goal]


# ────────────────────────────────────────────────────────────
# 図1: heapq が守っているきまり
# ────────────────────────────────────────────────────────────
def fig_heap_rule():
    heap = [1, 3, 2, 8, 9, 5]
    pos = {0: (430, 92), 1: (330, 168), 2: (530, 168),
           3: (280, 244), 4: (380, 244), 5: (480, 244)}
    pairs = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'heapq が守っているたった1つのきまり: 親は必ず子より小さい</text>']
    # 左: リストとしての中身
    s.append(f'        <text x="118" y="86" text-anchor="middle" fill="{GRAY}" font-size="12">リストとしての中身</text>')
    for i, v in enumerate(heap):
        y = 104 + i * 34
        s.append(f'        <rect x="40" y="{y}" width="46" height="28" rx="6" fill="#141414" stroke="#444"/>')
        s.append(f'        <text x="63" y="{y+19}" text-anchor="middle" fill="#ccc" font-size="13">{v}</text>')
        s.append(f'        <text x="100" y="{y+19}" fill="#666" font-size="10">← {i}番目</text>')
    s.append(f'        <text x="118" y="{104+6*34+16}" text-anchor="middle" fill="{GRAY}" font-size="10">'
             '並びはバラバラに見える</text>')
    # 右: 木としての形
    s.append(f'        <text x="430" y="52" text-anchor="middle" fill="{GRAY}" font-size="12">同じ中身を木の形に描いたもの</text>')
    for a, b in pairs:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        s.append(f'        <line x1="{x1}" y1="{y1+20}" x2="{x2}" y2="{y2-20}" stroke="#555" stroke-width="2"/>')
    for i, v in enumerate(heap):
        x, y = pos[i]
        s.append(f'        <circle cx="{x}" cy="{y}" r="21" fill="#1A1A1A" stroke="{GREEN if i == 0 else "#555"}" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="14" font-weight="700">{v}</text>')
        s.append(f'        <text x="{x}" y="{y-27}" text-anchor="middle" fill="#666" font-size="9">{i}番目</text>')
    # 親子の関係を順に光らせる
    for k, (a, b) in enumerate(pairs):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        p0, p1 = k / len(pairs), (k + 1) / len(pairs)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{p0:.3f};{p0+0.01:.3f};{p1-0.02:.3f};{p1:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <line x1="{x1}" y1="{y1+20}" x2="{x2}" y2="{y2-20}" stroke="{AMBER}" stroke-width="4"/>')
        s.append(f'          <circle cx="{x1}" cy="{y1}" r="21" fill="none" stroke="{AMBER}" stroke-width="3"/>')
        s.append(f'          <circle cx="{x2}" cy="{y2}" r="21" fill="none" stroke="{AMBER}" stroke-width="3"/>')
        s.append(f'          <text x="430" y="298" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">'
                 f'親 {heap[a]} ＜ 子 {heap[b]}　きまりを守っている</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="326" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'きまりのおかげで、いちばん小さい数は必ず0番目にある。だから先頭を見るだけで最小が分かる</text>')
    return fig(700, 342, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 最小をさがす作業の違い
# ────────────────────────────────────────────────────────────
def fig_find_min():
    values = [24, 7, 31, 12, 45, 9, 38, 16, 52, 3, 27, 19]
    n = len(values)
    dur = 10
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '「いちばん小さいもの」をさがす作業のちがい</text>']
    # 左: 全部見る
    s.append(f'        <text x="175" y="56" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">第5回のやり方: 全部見る</text>')
    for i, v in enumerate(values):
        x = 34 + (i % 4) * 72
        y = 76 + (i // 4) * 40
        s.append(f'        <rect x="{x}" y="{y}" width="60" height="30" rx="6" fill="#141414" stroke="#444"/>')
        s.append(f'        <text x="{x+30}" y="{y+20}" text-anchor="middle" fill="#ccc" font-size="12">{v}</text>')
        a = 0.7 * i / n
        s.append(f'        <rect x="{x}" y="{y}" width="60" height="30" rx="6" fill="none" stroke="{AMBER}" stroke-width="2.5" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.005:.3f};{a+0.05:.3f};{a+0.055:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="175" y="212" text-anchor="middle" fill="{AMBER}" font-size="12">'
             f'{n}個あれば{n}回調べる（頂点がn個なら n 回）</text>')
    s.append('        <line x1="350" y1="46" x2="350" y2="232" stroke="#333" stroke-width="1"/>')
    # 右: heapq
    s.append(f'        <text x="525" y="56" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">第6回のやり方: heapq に任せる</text>')
    s.append(f'        <rect x="430" y="76" width="60" height="30" rx="6" fill="#1a2e0a" stroke="{GREEN}" stroke-width="2.5"/>')
    s.append(f'        <text x="460" y="96" text-anchor="middle" fill="#93D500" font-size="12" font-weight="700">3</text>')
    s.append(f'        <text x="500" y="96" fill="{GREEN}" font-size="11">← 先頭を見るだけ</text>')
    for i, v in enumerate([7, 9, 12, 16, 19, 24, 27, 31]):
        x = 400 + (i % 4) * 66
        y = 126 + (i // 4) * 36
        s.append(f'        <rect x="{x}" y="{y}" width="54" height="26" rx="5" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x+27}" y="{y+18}" text-anchor="middle" fill="#666" font-size="11">{v}</text>')
    s.append(f'        <text x="525" y="212" text-anchor="middle" fill="{GREEN}" font-size="12">'
             '取り出したあとの並べ直しも、n個なら20回程度で終わる</text>')
    s.append(f'        <text x="350" y="252" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '頂点が100万個あるとき、全部見る方法は100万回。heapq なら20回程度</text>')
    return fig(700, 268, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 速度の比較
# ────────────────────────────────────────────────────────────
def fig_speed():
    rows = [("20×20", 400, 0.004, 0.000, 23), ("40×40", 1600, 0.070, 0.001, 86),
            ("80×80", 6400, 1.116, 0.003, 328), ("120×120", 14400, 6.140, 0.009, 656)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ答えを出すのにかかる時間の比較</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは、全部見る方法にかかった時間の割合（数値は測ったときの一例）</text>']
    for i, (size, v, tl, th, ratio) in enumerate(rows):
        y = 66 + i * 76
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{size}</text>')
        s.append(f'        <text x="24" y="{y+38}" fill="{GRAY}" font-size="10">頂点{v:,}個</text>')
        wl = max(tl / 6.14 * 430, 2)
        wh = max(th / 6.14 * 430, 2)
        s.append(f'        <text x="120" y="{y+18}" fill="{AMBER}" font-size="10">全部見る</text>')
        s.append(f'        <rect x="186" y="{y+4}" width="{wl:.0f}" height="18" rx="4" fill="{AMBER}" opacity="0.85"/>')
        s.append(f'        <text x="{186+wl+8:.0f}" y="{y+18}" fill="{AMBER}" font-size="11" font-weight="700">{tl:.3f}秒</text>')
        s.append(f'        <text x="120" y="{y+42}" fill="{GREEN}" font-size="10">heapq</text>')
        s.append(f'        <rect x="186" y="{y+28}" width="{wh:.0f}" height="18" rx="4" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{186+wh+8:.0f}" y="{y+42}" fill="{GREEN}" font-size="11" font-weight="700">{th:.3f}秒</text>')
        s.append(f'        <text x="676" y="{y+30}" text-anchor="end" fill="#ccc" font-size="12" font-weight="700">{ratio}倍速い</text>')
    s.append(f'        <text x="350" y="{66+4*76+14}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '頂点が増えるほど差が開く。カーナビが数万の交差点をあつかえるのは heapq のおかげ</text>')
    return fig(700, 66 + 4 * 76 + 32, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 10マス四方の迷路で見つけた経路
# ────────────────────────────────────────────────────────────
def fig_big_maze():
    route, total = dijkstra_route()
    simple = [(0, c) for c in range(10)] + [(r, 9) for r in range(1, 10)]
    simple_cost = sum(COST_MAP[r][c] for r, c in simple[1:])
    cell = 30
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '10マス四方の床コスト付き迷路で見つけた2つの経路</text>']
    for panel, (rt, title, x0, color, cost, steps) in enumerate([
            (simple, f"歩数の少ない経路: 18歩 ／ {simple_cost}秒", 24, AMBER, simple_cost, 18),
            (route, f"ダイクストラ法の経路: {len(route)-1}歩 ／ {total}秒", 376, GREEN, total, len(route) - 1)]):
        s.append(f'        <text x="{x0+150}" y="52" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 62
        mark = set(rt)
        for r in range(10):
            for c in range(10):
                x, y = x0 + c * cell, y0 + r * cell
                v = COST_MAP[r][c]
                deep = v >= 9
                on = (r, c) in mark
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="4" '
                         f'fill="{"#1a2e0a" if on else ("#2b1a00" if deep else "#141414")}" '
                         f'stroke="{color if on else ("#5a3d00" if deep else "#2e2e2e")}"/>')
                s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+4}" text-anchor="middle" '
                         f'fill="{color if on else (AMBER if deep else "#555")}" font-size="10">{v}</text>')
        pts = " ".join(f"{x0+c*cell+(cell-2)/2},{y0+r*cell+(cell-2)/2}" for r, c in rt)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3" '
                 f'stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900">'
                 f'<animate attributeName="stroke-dashoffset" values="900;0;0" keyTimes="0;0.7;1" dur="9s" repeatCount="indefinite"/></polyline>')
    s.append(f'        <text x="350" y="{62+10*cell+28}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             f'4歩よけいに歩くかわりに、9のマスを1つも通らずに済み、合計は{simple_cost}秒から{total}秒に減った</text>')
    return fig(700, 62 + 10 * cell + 46, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "heapqとは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2の読み飛ばし"),
    ("#sec-examples", "tag-example", "観察記録", "例題3の速さの差"),
    ("#sec-standard", "tag-standard", "標準課題1", "取り出す順番を予測"),
    ("#sec-standard", "tag-standard", "標準課題2", "辺を1本足すと？"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回で書いたダイクストラ法には、遅くなる原因が1つあります。
      手順1の「まだ決まっていない駅のうち、いちばん小さい駅をさがす」部分で、
      <strong>毎回すべての駅を順に見ている</strong>ためです。
      駅が6個なら大した手間ではありませんが、交差点が10万個ある道路地図では、
      1回さがすたびに10万回の比較が必要になります。
    </p>

    <div class="analogy">
      病院の待合室で、症状の重い順に患者を呼ぶ場面を思い浮かべてください。
      呼ぶたびに全員に「どのくらい痛いですか」と聞いて回るのは大変です。
      受付で番号札に重さを書いて<strong>専用の箱</strong>に入れておき、
      箱から取り出すと必ずいちばん重い人の札が出てくる仕組みがあれば、聞いて回る必要はありません。
      「専用の箱」にあたるものが<strong>優先度付きキュー</strong>で、Pythonでは <code>heapq</code> という道具で使えます。
    </div>

{fig_find_min()}

    <div class="concept-box">
      <h4>heapq の3つの命令</h4>
      <table>
        <tr><th>命令</th><th>すること</th></tr>
        <tr><td><code>heapq.heappush(箱, 値)</code></td><td>箱に値を1つ入れる</td></tr>
        <tr><td><code>heapq.heappop(箱)</code></td><td>箱の中でいちばん小さい値を取り出す（箱からは消える）</td></tr>
        <tr><td><code>箱[0]</code></td><td>取り出さずに、いちばん小さい値を見るだけ</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        箱として使うのは、ふつうのPythonのリストです。特別な型を用意する必要はありません。
        ただし、リストの中身を <code>append()</code> などで直接いじってしまうと、きまりが崩れて正しく動かなくなります。
        必ず <code>heappush</code> と <code>heappop</code> だけを使ってください。
      </p>
    </div>

{fig_heap_rule()}

    <div class="concept-box">
      <h4>すでに確定した駅が、もう一度出てくることがある</h4>
      <p style="font-size:0.95rem">
        heapq を使うダイクストラ法では、同じ駅が箱の中に<strong>何度も入る</strong>ことがあります。
        品川は最初に「30分」として入り、あとから「16分」としてもう一度入るためです。
        箱から取り出すときは小さい順なので、先に16分のほうが出てきて確定します。
        あとから出てくる30分の組は、すでに確定した駅についてのものなので<strong>読み飛ばします</strong>。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        読み飛ばす処理を忘れると、確定した駅をもう一度確定させてしまい、正しく動かなくなります。
        例題2の実行結果で、実際に読み飛ばしが起きていることを確かめてください。
      </p>
    </div>"""

ex1_body = f"""      <p>ダイクストラ法に使う前に、<code>heapq</code> がどう動くかだけを確かめます。
      数を入れる例と、<code>(時間, 駅名)</code> の組を入れる例の2つを実行します。</p>

{code('AL2-06-ex1.py')}

{run('a06_ex1_result.png', '8, 3, 5, 1, 9, 2 の順に入れたのに、取り出す順番は 1, 2, 3, 5, 8, 9 と小さい順になりました。'
     '入れている途中の中身（例: <code>[1, 3, 2, 8, 9, 5]</code>）は小さい順に並んでいませんが、'
     '<strong>先頭だけは必ずいちばん小さい数</strong>になっています。'
     '後半では <code>(16, "品川")</code> のような組を入れており、1番目の要素である時間が小さい順に出てきています。'
     'ダイクストラ法では、この形をそのまま使います。')}"""

ex2_body = f"""      <p>第5回のダイクストラ法を、<code>heapq</code> を使う形に書き直します。
      「まだ決まっていない駅を全部見る」ループがなくなり、<code>heappop</code> の1行に置きかわります。</p>

{code('AL2-06-ex2.py')}

{run('a06_ex2_result.png', '取り出した順番は (0分, 新宿) → (7分, 渋谷) → (9分, 池袋) → (16分, 品川) → (21分, 上野) → (27分, 東京) でした。'
     '第5回の例題1で確定した順番とまったく同じです。'
     'いちばん最後に <strong>(30分, 品川) → すでに確定済みなので読み飛ばす</strong> と表示されています。'
     '品川は最初に30分として箱に入れられ、あとから16分として入れ直されました。'
     '16分のほうが先に取り出されて確定したので、残っていた30分の組は読み飛ばされています。')}

{notion('例題2の実行結果から、「読み飛ばす」と表示された行を書き写す。'
        'あわせて、品川が2回 queue に入れられた理由と、30分の組を読み飛ばしてよい理由を説明する。')}"""

ex3_body = f"""      <p>第5回のやり方（全部見る）と、第6回のやり方（heapq）で、同じグラフの最短距離を求めて時間を比べます。
      グラフはマス目の形で、大きさを 20×20 から 120×120 まで変えていきます。</p>

{code('AL2-06-ex3.py')}

{fig_speed()}

{run('a06_ex3_result.png', '120マス四方（頂点14,400個）では、全部見る方法が<strong>約6秒</strong>、'
     'heapq を使う方法が<strong>0.01秒ほど</strong>で、<strong>数百倍</strong>の差が出ました。'
     '20マス四方のときは20倍ほどだったので、頂点が増えるほど差が広がっています。'
     '2つの方法が出した答えは、どの大きさでも完全に一致しています。'
     '秒数はパソコンの性能で変わるので、自分の結果が画像と一致しなくても問題ありません。大切なのは<strong>差の広がり方</strong>です。')}

{notion('例題3の表から、4つの大きさそれぞれの「全部見る方法の時間」「heapqの方法の時間」「何倍速いか」を書き写す。'
        'あわせて、頂点の数が増えるほど差が広がる理由を説明する。')}"""

ex4_body = f"""      <p>heapq を使ったダイクストラ法で、10マス四方の床コスト付き迷路を解きます。
      1 は舗装された道（1秒）、9 はぬかるみ（9秒）です。</p>

{code('AL2-06-ex4.py')}

{fig_big_maze()}

{run('a06_ex4_result.png', 'ダイクストラ法が見つけた経路は<strong>22歩・22秒</strong>でした。'
     '通り道には 9 のマスが1つも含まれておらず、すべて 1 のマスだけを通っています。'
     '参考として表示した「上の行を右へ進んでから右の列を下りる経路」は18歩ですが、'
     'ぬかるみを何度も通るため<strong>58秒</strong>かかります。'
     '4歩よけいに歩くかわりに、36秒も短くなっているということです。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題3は実行に10秒ほどかかります。まず作業フォルダを用意します。</p>

{setup_guide('06', ['AL2-06-ex1.py', 'AL2-06-ex2.py', 'AL2-06-ex3.py', 'AL2-06-ex4.py'])}

{keywords([
    ('優先度付きキュー', 'ゆうせんどつきキュー / priority queue', '入れたものの中から、いつでも「いちばん小さいもの」を速く取り出せる入れもの。'),
    ('heapq', 'ヒープキュー', 'Pythonで優先度付きキューを使うための道具。<code>import heapq</code> と書いて使う。'),
    ('heappush', 'ヒーププッシュ', '<code>heapq.heappush(箱, 値)</code> で、箱に値を1つ入れる。'),
    ('heappop', 'ヒーポップ', '<code>heapq.heappop(箱)</code> で、箱の中のいちばん小さい値を取り出す。'),
    ('読み飛ばし', 'skip', '箱から取り出した駅がすでに確定しているとき、何もせず次に進むこと。heapq版のダイクストラ法で必要になる。'),
])}

{example(1, 'heapq の使い方を確かめる', ex1_body)}

{example(2, 'heapq を使ったダイクストラ法', ex2_body)}

{example(3, '2つのやり方の速さを比べる', ex3_body)}

{example(4, '大きめの迷路を解く', ex4_body)}"""

std1_body = """      <p>プログラムを実行する<strong>前に</strong>、次のコードが何をどの順番で表示するかを予測してください。</p>

<pre><span class="code-label">Python ── AL2-06-std1.py</span>
<span class="kw">import</span> heapq

box = []
heapq.heappush(box, (<span class="num">14</span>, <span class="str">"東京"</span>))
heapq.heappush(box, (<span class="num">5</span>, <span class="str">"渋谷"</span>))
heapq.heappush(box, (<span class="num">23</span>, <span class="str">"上野"</span>))
heapq.heappush(box, (<span class="num">5</span>, <span class="str">"池袋"</span>))
heapq.heappush(box, (<span class="num">9</span>, <span class="str">"品川"</span>))

<span class="fn">print</span>(<span class="str">"箱の中身:"</span>, box)
<span class="fn">print</span>(<span class="str">"先頭:"</span>, box[<span class="num">0</span>])
<span class="fn">print</span>()

<span class="kw">while</span> <span class="fn">len</span>(box) &gt; <span class="num">0</span>:
    <span class="fn">print</span>(heapq.heappop(box))</pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、取り出される5つの組を順番どおりに予測してNotionに書く</li>
          <li><code>AL2-06-std1.py</code> という名前で保存して実行する</li>
          <li>実際の出力を記録し、予測と比べる</li>
        </ol>
      </div>

      <table>
        <tr><th>取り出す順番</th><th>予測</th><th>実際</th></tr>
        <tr><td>1つ目</td><td></td><td></td></tr>
        <tr><td>2つ目</td><td></td><td></td></tr>
        <tr><td>3つ目</td><td></td><td></td></tr>
        <tr><td>4つ目</td><td></td><td></td></tr>
        <tr><td>5つ目</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 時間が同じ <code>(5, "渋谷")</code> と <code>(5, "池袋")</code> は、
      どちらが先に取り出されましたか。なぜその順番になるのかを説明してください。</p>
"""

std2_body = """      <p>例題2のファイル <code>AL2-06-ex2.py</code> を開き、池袋と品川を直接つなぐ新しい路線（5分）を追加します。</p>

<pre><span class="code-label">Python ── 書き換える2行</span>
    <span class="str">"池袋"</span>: [(<span class="str">"新宿"</span>, <span class="num">9</span>), (<span class="str">"上野"</span>, <span class="num">12</span>), (<span class="str">"品川"</span>, <span class="num">5</span>)],   <span class="cmt"># ← ("品川", 5) を足す</span>
    <span class="str">"品川"</span>: [(<span class="str">"新宿"</span>, <span class="num">30</span>), (<span class="str">"渋谷"</span>, <span class="num">9</span>), (<span class="str">"東京"</span>, <span class="num">11</span>), (<span class="str">"池袋"</span>, <span class="num">5</span>)],   <span class="cmt"># ← ("池袋", 5) を足す</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、新宿から各駅までの最短時間と、東京への道順を予測してNotionに書く</li>
          <li>2行を書き換えて保存し、実行する</li>
          <li>実際の結果を記録し、予測と比べる</li>
          <li>「読み飛ばす」と表示された行が何回出たかを数える</li>
        </ol>
      </div>

      <table>
        <tr><th>駅</th><th>追加する前</th><th>予測</th><th>実際</th></tr>
        <tr><td>渋谷</td><td>7分</td><td></td><td></td></tr>
        <tr><td>池袋</td><td>9分</td><td></td><td></td></tr>
        <tr><td>品川</td><td>16分</td><td></td><td></td></tr>
        <tr><td>上野</td><td>21分</td><td></td><td></td></tr>
        <tr><td>東京</td><td>27分</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 新しい路線を1本足しただけで、時間が短くなった駅と変わらなかった駅があります。
      どの駅がどう変わったかを書き、変わった理由を「新しい路線を通る経路」を示しながら説明してください。</p>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    どちらも<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, 'heapq から取り出される順番を予測する', std1_body)}
{notion('5つの組についての予測と実際の表、および「時間が同じときの順番」の説明。')}

{standard(2, '路線を1本足すと最短時間はどう変わるか', std2_body)}
{notion('5つの駅についての予測と実際の表、東京への道順、読み飛ばしの回数、および変わった理由の説明。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第6回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 「読み飛ばす」行の書き写し、2回入れられた理由、読み飛ばしてよい理由</li>
        <li><strong>例題3</strong>: 4つの大きさの時間と倍率、差が広がる理由</li>
        <li><strong>標準課題1</strong>: 予測と実際の表、時間が同じときの順番の説明</li>
        <li><strong>標準課題2</strong>: 予測と実際の表、道順、読み飛ばし回数、変わった理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: 取り出される順番", """        <table>
          <tr><th>取り出す順番</th><th>実際</th></tr>
          <tr><td>1つ目</td><td>(5, '池袋')</td></tr>
          <tr><td>2つ目</td><td>(5, '渋谷')</td></tr>
          <tr><td>3つ目</td><td>(9, '品川')</td></tr>
          <tr><td>4つ目</td><td>(14, '東京')</td></tr>
          <tr><td>5つ目</td><td>(23, '上野')</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>時間が同じときの順番:</strong>
        <code>(5, "渋谷")</code> と <code>(5, "池袋")</code> は1番目の要素が同じ 5 なので、
        Pythonは<strong>2番目の要素で比べます</strong>。
        文字列どうしの比較では、文字コードの小さいほうが先になります。
        「池」と「渋」を比べると「池」のほうが文字コードが小さいため、<code>(5, "池袋")</code> が先に取り出されます。</p>
        <p style="margin-top:0.6rem">ダイクストラ法では、時間が同じ駅がどちらの順で確定しても、最終的な最短時間は変わりません。
        ただし、同じ時間でたどり着ける経路が複数あるとき、<strong>表示される道順がどちらになるかは変わります</strong>。
        第5回の例題2で東京への道順が「新宿 → 渋谷 → 品川 → 東京」になったのも、
        同じ27分の「新宿 → 池袋 → 上野 → 東京」より先に見つかったからです。</p>
        <p style="margin-top:0.6rem"><strong>注意:</strong> タプルの2番目に、比べられないもの（辞書など）を入れると、
        時間が同じになったときにエラーが出ます。実際のプログラムでは、駅名のかわりに番号を入れることがよくあります。</p>"""),
    ("標準課題2: 池袋と品川を5分でつないだときの結果", """        <table>
          <tr><th>駅</th><th>追加する前</th><th>追加したあと</th><th>変化</th></tr>
          <tr><td>渋谷</td><td>7分</td><td>7分</td><td>変わらない</td></tr>
          <tr><td>池袋</td><td>9分</td><td>9分</td><td>変わらない</td></tr>
          <tr><td>品川</td><td>16分</td><td><strong style="color:#76B900">14分</strong></td><td>2分短くなった</td></tr>
          <tr><td>上野</td><td>21分</td><td>21分</td><td>変わらない</td></tr>
          <tr><td>東京</td><td>27分</td><td><strong style="color:#76B900">25分</strong></td><td>2分短くなった</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>変わった理由:</strong>
        品川への行き方が「新宿 → 渋谷 → 品川」（7+9=16分）から
        「<strong>新宿 → 池袋 → 品川</strong>」（9+5=14分）に変わったためです。
        新しくできた池袋と品川のあいだの5分が、渋谷まわりより速い近道になっています。</p>
        <p style="margin-top:0.6rem">東京へは品川を通るので、品川が2分早くなったぶん、東京も 27分 → 25分 と2分短くなります。
        道順は「新宿 → 池袋 → 品川 → 東京」に変わります。</p>
        <p style="margin-top:0.6rem">渋谷（7分）と池袋（9分）は新宿の直接のとなりなので、新しい路線を通る必要がありません。
        上野へは「新宿 → 池袋 → 上野」の21分のままで、品川を通る経路（14+11+6=31分）より短いため変わりません。</p>
        <p style="margin-top:0.6rem"><strong>読み飛ばしの回数: 2回</strong>（どちらも品川）。
        品川は「30分」「16分」「14分」の3回 queue に入ります。
        いちばん小さい14分が先に取り出されて確定するので、あとから出てくる16分と30分の組が読み飛ばされます。
        東京は25分の1回しか queue に入りません。
        上野を確定させたときに計算される 21+6=27分 は、すでに書いてある25分より大きいので、queue に入れられないためです。
        実行結果の「すでに確定済みなので読み飛ばす」の行を数えて確かめてください。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "優先度付きキュー（heapq）", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("06", NAV, body)
