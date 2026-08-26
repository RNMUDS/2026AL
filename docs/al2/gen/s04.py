# -*- coding: utf-8 -*-
"""第4回: 重み付きグラフとは の本文を組み立てる。"""
import math
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

POS = {"新宿": (170, 96), "渋谷": (170, 246), "品川": (390, 246),
       "池袋": (390, 66), "上野": (560, 66), "東京": (560, 196)}
EDGES = [("新宿", "渋谷", 7), ("新宿", "池袋", 9), ("新宿", "品川", 30),
         ("渋谷", "品川", 9), ("池袋", "上野", 12), ("上野", "東京", 6),
         ("東京", "品川", 11)]

COST_MAP = [
    [1, 1, 1, 9, 1],
    [9, 9, 1, 9, 1],
    [1, 1, 1, 9, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]
ROUTE_A = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
ROUTE_B = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
ROUTE_C = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0),
           (4, 1), (4, 2), (4, 3), (4, 4)]


def draw_graph(highlight=None, hcolor=GREEN, show_weight=True):
    """路線図を描く。highlight は強調する経路（駅名の並び）。"""
    out = []
    hedges = set()
    if highlight:
        for i in range(len(highlight) - 1):
            hedges.add(frozenset((highlight[i], highlight[i + 1])))
    for a, b, w in EDGES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        on = frozenset((a, b)) in hedges
        out.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="{hcolor if on else "#555"}" stroke-width="{5 if on else 2}"/>')
    if show_weight:
        for a, b, w in EDGES:
            (x1, y1), (x2, y2) = POS[a], POS[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            on = frozenset((a, b)) in hedges
            out.append(f'        <rect x="{mx-17}" y="{my-11}" width="34" height="22" rx="6" '
                       f'fill="#0A0A0A" stroke="{hcolor if on else GRAY}"/>')
            out.append(f'        <text x="{mx}" y="{my+5}" text-anchor="middle" '
                       f'fill="{hcolor if on else "#bbb"}" font-size="11" font-weight="{700 if on else 400}">{w}分</text>')
    for name, (x, y) in POS.items():
        on = highlight and name in highlight
        out.append(f'        <circle cx="{x}" cy="{y}" r="26" fill="{"#1a2e0a" if on else "#1A1A1A"}" '
                   f'stroke="{hcolor if on else "#555"}" stroke-width="2"/>')
        out.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" '
                   f'font-size="12" font-weight="700">{name}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 直通より乗りかえのほうが早い
# ────────────────────────────────────────────────────────────
def fig_weighted_graph():
    dur = 15
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '辺に「かかる時間」を書き込んだグラフ（重み付きグラフ）</text>']
    s += draw_graph()
    phases = [
        (0.02, 0.34, ["新宿", "品川"], AMBER, "直通: 路線1本 ／ 合計 30分", "辺の数はいちばん少ない"),
        (0.36, 0.66, ["新宿", "渋谷", "品川"], GREEN, "乗りかえ1回: 路線2本 ／ 合計 16分", "辺の数は多いが、合計時間はいちばん短い"),
        (0.68, 0.98, ["新宿", "池袋", "上野", "東京", "品川"], RED, "遠回り: 路線4本 ／ 合計 38分", "辺の数も合計時間も多い"),
    ]
    for a, b, route, color, label, note in phases:
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s += ["  " + line for line in draw_graph(route, color)]
        s.append(f'          <text x="350" y="300" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{label}</text>')
        s.append(f'          <text x="350" y="322" text-anchor="middle" fill="{GRAY}" font-size="11">{note}</text>')
        s.append('        </g>')
    return fig(700, 336, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 重みなしと重みありの書き方の違い
# ────────────────────────────────────────────────────────────
def fig_notation():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '隣接リストに重みを書き足す</text>']
    boxes = [
        (24, "重みなし（第3回）", GRAY, [
            '"新宿": ["渋谷", "池袋", "品川"]',
            '',
            'となりの駅の名前だけを並べる',
            '「どこへ行けるか」しか分からない',
        ]),
        (364, "重みあり（第4回）", GREEN, [
            '"新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)]',
            '',
            '（駅の名前, かかる時間）の組で並べる',
            '「どこへ行けるか」＋「いくらかかるか」が分かる',
        ]),
    ]
    for x0, title, color, lines in boxes:
        s.append(f'        <rect x="{x0}" y="46" width="312" height="150" rx="12" fill="#141414" stroke="{color}" stroke-width="1.6"/>')
        s.append(f'        <text x="{x0+156}" y="72" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        for i, ln in enumerate(lines):
            if not ln:
                continue
            mono = ' font-family="JetBrains Mono, monospace"' if ln.startswith('"') else ""
            size = 10 if ln.startswith('"') else 11
            fill = "#cdd6f4" if ln.startswith('"') else "#bbb"
            s.append(f'        <text x="{x0+156}" y="{100+i*24}" text-anchor="middle" fill="{fill}" font-size="{size}"{mono}>{ln}</text>')
    s.append(f'        <text x="350" y="222" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '重みを書き足すだけで、「乗りかえの少なさ」ではなく「かかる時間の短さ」を考えられるようになる</text>')
    return fig(700, 238, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 床コスト付き迷路の3つの行き方
# ────────────────────────────────────────────────────────────
def fig_cost_maze():
    cell = 46
    dur = 15
    x0, y0 = 246, 62
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '床コスト付き迷路: 歩数が多くても合計時間は短いことがある</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'マスの数字は、そのマスを通り抜けるのにかかる秒数</text>']
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * cell, y0 + r * cell
            v = COST_MAP[r][c]
            deep = v >= 9
            s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="6" '
                     f'fill="{"#2b1a00" if deep else "#141414"}" stroke="{"#5a3d00" if deep else "#333"}"/>')
            s.append(f'        <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+6}" text-anchor="middle" '
                     f'fill="{AMBER if deep else "#bbb"}" font-size="15" font-weight="{700 if deep else 400}">{v}</text>')
    s.append(f'        <text x="{x0+8}" y="{y0+14}" fill="{GREEN}" font-size="11" font-weight="700">S</text>')
    s.append(f'        <text x="{x0+4*cell+30}" y="{y0+4*cell+38}" fill="{GREEN}" font-size="11" font-weight="700">G</text>')

    phases = [
        (0.02, 0.32, ROUTE_A, AMBER, "行き方A: 8歩 ／ 合計 16秒"),
        (0.34, 0.64, ROUTE_B, AMBER, "行き方B: 8歩 ／ 合計 16秒"),
        (0.66, 0.98, ROUTE_C, GREEN, "行き方C: 12歩 ／ 合計 12秒（いちばん短い）"),
    ]
    for a, b, route, color, label in phases:
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        pts = " ".join(f"{x0+c*cell+(cell-3)/2},{y0+r*cell+(cell-3)/2}" for r, c in route)
        s.append(f'          <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="5" '
                 f'stroke-linejoin="round" stroke-linecap="round" opacity="0.85"/>')
        s.append(f'          <text x="350" y="{y0+5*cell+28}" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{label}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{y0+5*cell+54}" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '9のマス（ぬかるみ）を1つ通るだけで、1のマスを8回通るより時間がかかる</text>')
    return fig(700, y0 + 5 * cell + 70, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 全探索の通り数の爆発
# ────────────────────────────────────────────────────────────
def fig_explosion():
    rows = [("3×3", 12, "すぐ終わる"), ("4×4", 184, "すぐ終わる"),
            ("5×5", 8512, "0.03秒"), ("6×6", 1262816, "約7秒"),
            ("7×7", 575780564, "約1時間")]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路が1マス大きくなるだけで、行き方の数は数百倍に増える</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり</text>']
    for i, (size, count, note) in enumerate(rows):
        y = 66 + i * 44
        big = count > 10 ** 6
        color = RED if big else GREEN
        w = math.log10(count) / 9 * 400
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{size}</text>')
        s.append(f'        <rect x="86" y="{y+4}" width="{w:.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{86+w+10:.0f}" y="{y+21}" fill="{color}" font-size="12" font-weight="700">{count:,}通り</text>')
        s.append(f'        <text x="676" y="{y+21}" text-anchor="end" fill="{GRAY}" font-size="11">{note}</text>')
    s.append(f'        <text x="350" y="{66+5*44+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '全探索では現実的な時間で終わらない。第5回から学ぶダイクストラ法が必要になる</text>')
    return fig(700, 66 + 5 * 44 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "重みとは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2の14分の差"),
    ("#sec-examples", "tag-example", "観察記録", "例題4の通り数の増え方"),
    ("#sec-standard", "tag-standard", "標準課題1", "重みを変えると？"),
    ("#sec-standard", "tag-standard", "標準課題2", "自分で重み付きグラフを作る"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第3回のグラフでは、辺は「つながっている／つながっていない」のどちらかでした。
      しかし実際の地図や路線図では、つながり方に<strong>強さの違い</strong>があります。
      1駅ぶんでも、急行で3分の区間もあれば、各駅停車で30分かかる区間もあります。
      辺ごとに数値を書き込んだグラフを<strong>重み付きグラフ</strong>と呼び、書き込む数値を<strong>重み</strong>と呼びます。
    </p>

    <div class="analogy">
      乗換案内アプリで経路を調べると、「乗りかえ0回・所要45分」と「乗りかえ2回・所要28分」のように、
      性質の違う候補が並びます。乗りかえの回数がいちばん少ない行き方と、所要時間がいちばん短い行き方は、別のものです。
      第1回から第3回までの幅優先探索が求めていたのは、前者の「乗りかえの回数がいちばん少ない行き方」でした。
    </div>

{fig_weighted_graph()}

    <div class="concept-box">
      <h4>重みになるもの</h4>
      <table>
        <tr><th>あつかうもの</th><th>重みになるもの</th><th>小さいほど良いか</th></tr>
        <tr><td>路線図</td><td>乗車時間（分）</td><td>小さいほど良い</td></tr>
        <tr><td>道路地図</td><td>距離（km）、通行料金（円）</td><td>小さいほど良い</td></tr>
        <tr><td>床コスト付き迷路</td><td>そのマスを通り抜ける時間（秒）</td><td>小さいほど良い</td></tr>
        <tr><td>通信ネットワーク</td><td>通信の遅れ（ミリ秒）</td><td>小さいほど良い</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        後期の授業であつかう重みは、すべて<strong>0以上の数値</strong>です。
        マイナスの重みが混ざると、第5回から学ぶダイクストラ法は正しく動きません。理由は第5回で確かめます。
      </p>
    </div>

{fig_notation()}

    <div class="concept-box">
      <h4>用語の整理: 「最短」には2つの意味がある</h4>
      <table>
        <tr><th>言い方</th><th>意味</th><th>求める方法</th></tr>
        <tr><td>辺の数が最も少ない経路</td><td>乗りかえや歩数がいちばん少ない行き方</td><td>幅優先探索（第1〜3回）</td></tr>
        <tr><td>重みの合計が最も小さい経路</td><td>かかる時間や料金がいちばん小さい行き方</td><td>ダイクストラ法（第5回から）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        重みがすべて同じ値なら、2つの答えは一致します。
        重みがばらばらのときは、例題2で確かめるように<strong>答えがずれます</strong>。
      </p>
    </div>"""

ex1_body = f"""      <p>6つの駅からなる路線図に、区間ごとの乗車時間を重みとして書き込みます。
      重み付きの隣接リストでは、となりの駅を <code>("駅の名前", 時間)</code> という<strong>2つ組</strong>で並べます。</p>

{code('AL2-04-ex1.py')}

{run('a04_ex1_result.png', '新宿から品川へは3通りの行き方があり、乗りかえ0回の直通が<strong>30分</strong>、'
     '渋谷で1回乗りかえる行き方が<strong>16分</strong>、大回りの行き方が<strong>38分</strong>でした。'
     '乗りかえが少ない順に並べると 30分 → 16分 → 38分 で、乗りかえの回数と所要時間はまったく対応していません。'
     '<code>route_minutes</code> 関数は、隣り合う2駅の重みを順に足していくことで合計時間を求めています。')}"""

ex2_body = f"""      <p>幅優先探索で新宿から品川への経路を求め、すべての行き方の中でいちばん時間が短い経路と比べます。</p>

{code('AL2-04-ex2.py')}

{run('a04_ex2_result.png', '幅優先探索が選んだのは<strong>直通の30分</strong>の経路でした。'
     '一方、合計時間がいちばん短いのは<strong>渋谷で乗りかえる16分</strong>の経路で、その差は14分もあります。'
     '幅優先探索は「路線の本数」を最小にするアルゴリズムなので、本数が1本の直通を選びます。'
     '重みの合計を最小にしたい場合、幅優先探索は使えません。')}

{notion('例題2の実行結果から、幅優先探索が選んだ経路と合計時間、いちばん短い経路と合計時間、その差を書く。'
        'あわせて、幅優先探索が16分の経路を選べない理由を、幅優先探索の進め方と結びつけて説明する。')}"""

ex3_body = f"""      <p>迷路のマスごとに「通り抜けるのにかかる秒数」を決めた迷路を作り、3通りの行き方の合計時間を比べます。
      1 は舗装された道（1秒）、9 はぬかるみ（9秒）です。</p>

{code('AL2-04-ex3.py')}

{fig_cost_maze()}

{run('a04_ex3_result.png', '行き方Aと行き方Bはどちらも<strong>8歩・16秒</strong>、行き方Cは<strong>12歩・12秒</strong>でした。'
     '歩数がいちばん多い行き方Cが、合計時間ではいちばん短くなっています。'
     '行き方Aと行き方Bは、途中で 9 のマス（ぬかるみ）を1回通っているためです。'
     'ぬかるみを1マス通るだけで9秒かかるので、舗装路を4マスよけいに歩いたほうが早く着きます。')}"""

ex4_body = f"""      <p>「すべての行き方を書き出して、いちばん安いものを選ぶ」という全探索が、
      迷路の大きさによってどれくらい時間がかかるようになるかを測ります。</p>

{code('AL2-04-ex4.py')}

{fig_explosion()}

{run('a04_ex4_result.png', '3マス四方は12通り、4マス四方は184通り、5マス四方は8,512通り、6マス四方は1,262,816通りでした。'
     'たった1マス大きくなるだけで、行き方の数は<strong>およそ150倍</strong>に増えています。'
     '6マス四方で約7秒かかったので、7マス四方（5億7千万通り）では1時間近くかかる計算になります。'
     'カーナビが数万の交差点をあつかうことを考えると、全探索はまったく使えません。')}

{notion('例題4の表から、迷路の大きさごとの「行き方の数」と「かかった時間」を書き写す。'
        'あわせて、5マス四方から6マス四方に大きくしたとき、行き方の数が何倍になったかを計算して書く。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題4は実行に10秒ほどかかります。止まっているように見えても、終わるまで待ってください。</p>

{setup_guide('04', ['AL2-04-ex1.py', 'AL2-04-ex2.py', 'AL2-04-ex3.py', 'AL2-04-ex4.py'])}

{keywords([
    ('重み', 'おもみ / weight', '辺ごとに書き込む数値。乗車時間・距離・料金など「その辺を通るのにかかるもの」を表す。'),
    ('重み付きグラフ', 'weighted graph', 'すべての辺に重みが付いているグラフ。重みのないグラフは、すべての重みが1のグラフと考えることもできる。'),
    ('コスト', 'cost', '重みの言いかえ。「その道を通るために支払うもの」という意味で使う。合計コストが小さいほど良い。'),
    ('タプル', 'tuple', '<code>("渋谷", 7)</code> のように、丸かっこでいくつかの値をまとめたもの。リストと違って、あとから中身を書き換えられない。'),
    ('全探索', 'ぜんたんさく / brute force', '考えられる候補をすべて書き出して1つずつ調べる方法。必ず正しい答えが出るが、候補が増えると終わらなくなる。'),
])}

{example(1, '重み付きグラフを隣接リストで表す', ex1_body)}

{example(2, '幅優先探索では最短時間を求められない', ex2_body)}

{example(3, '床にコストがある迷路', ex3_body)}

{example(4, '全探索が使えなくなる大きさ', ex4_body)}"""

std1_body = """      <p>例題2のファイル <code>AL2-04-ex2.py</code> を開き、新宿と品川を直接つなぐ区間の重みを変えます。
      直通が急行に変わり、30分から12分に短くなったという設定です。</p>

<pre><span class="code-label">Python ── 書き換える2か所</span>
    <span class="str">"新宿"</span>: [(<span class="str">"渋谷"</span>, <span class="num">7</span>), (<span class="str">"池袋"</span>, <span class="num">9</span>), (<span class="str">"品川"</span>, <span class="num">12</span>)],   <span class="cmt"># ← 30 を 12 に</span>
    <span class="str">"品川"</span>: [(<span class="str">"新宿"</span>, <span class="num">12</span>), (<span class="str">"渋谷"</span>, <span class="num">9</span>), (<span class="str">"東京"</span>, <span class="num">11</span>)],   <span class="cmt"># ← 30 を 12 に</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、3通りの行き方それぞれの合計時間と、いちばん短い行き方を予測してNotionに書く</li>
          <li>2か所を書き換えて保存し、実行する</li>
          <li>幅優先探索が選んだ経路と、いちばん短い経路を記録する</li>
          <li>書き換える前（30分）と比べて、何が変わったかを書く</li>
        </ol>
      </div>

      <table>
        <tr><th>行き方</th><th>30分のとき</th><th>予測（12分のとき）</th><th>実際</th></tr>
        <tr><td>新宿 → 品川</td><td>30分</td><td></td><td></td></tr>
        <tr><td>新宿 → 渋谷 → 品川</td><td>16分</td><td></td><td></td></tr>
        <tr><td>新宿 → 池袋 → 上野 → 東京 → 品川</td><td>38分</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 重みを12分にしたとき、幅優先探索が選ぶ経路と、いちばん短い経路は一致しますか。
      一致する場合、それは「幅優先探索が重みを考えられるようになった」ことを意味しますか。理由とともに説明してください。</p>
"""

std2_body = """      <p>身近な場面を1つ選び、自分で重み付きグラフを作ります。頂点は4個以上、辺は5本以上にしてください。</p>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>テーマを1つ決める（例: 自宅から大学までの経路、キャンパス内の建物、よく行く店の位置関係）</li>
          <li>頂点（場所）と辺（つながり）と重み（かかる時間や距離）を紙に描く</li>
          <li>例題1のコードをコピーして <code>AL2-04-std2.py</code> という名前で保存し、<code>railway</code> の中身を自分のグラフに書き換える</li>
          <li>出発点と目的地を決め、行き方を3通り以上書き出して、それぞれの合計コストを <code>route_minutes</code> で計算する</li>
          <li>いちばんコストが小さい行き方を答える</li>
        </ol>
      </div>

      <p><strong>Notionに書くこと:</strong></p>
      <ul class="point-list">
        <li>選んだテーマと、頂点・辺・重みが何を表しているか</li>
        <li>作ったグラフの図（手描きの写真でもよい）</li>
        <li>書き換えたコードと実行結果</li>
        <li>3通り以上の行き方とそれぞれの合計コスト、いちばん小さいもの</li>
      </ul>

      <p style="margin-top:1rem"><strong>問い:</strong> 自分が選んだテーマで、重みを「時間」ではなく「料金」に変えたとしたら、
      いちばん良い行き方は変わりそうですか。変わる／変わらないの理由を説明してください。</p>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。</p>

{standard(1, '重みを変えると、いちばん短い行き方はどうなるか', std1_body)}
{notion('3通りの行き方についての予測と実際の表、幅優先探索が選んだ経路、いちばん短い経路、および「一致は偶然か」の説明。')}

{standard(2, '自分で重み付きグラフを作る', std2_body)}
{notion('テーマ、グラフの図、書き換えたコード、実行結果、3通り以上の行き方とコスト、いちばん小さい行き方、および重みを料金に変えた場合の考察。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第4回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 幅優先探索の経路と時間、最短の経路と時間、差、選べない理由</li>
        <li><strong>例題4</strong>: 大きさごとの行き方の数と時間、5マス四方から6マス四方への倍率</li>
        <li><strong>標準課題1</strong>: 予測と実際の表、一致するかどうかの考察</li>
        <li><strong>標準課題2</strong>: 自作の重み付きグラフと計算結果、料金に変えた場合の考察</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: 直通を12分にしたときの結果", """        <table>
          <tr><th>行き方</th><th>30分のとき</th><th>12分のとき</th></tr>
          <tr><td>新宿 → 品川</td><td>30分</td><td><strong style="color:#76B900">12分（いちばん短い）</strong></td></tr>
          <tr><td>新宿 → 渋谷 → 品川</td><td><strong style="color:#76B900">16分（いちばん短い）</strong></td><td>16分</td></tr>
          <tr><td>新宿 → 池袋 → 上野 → 東京 → 品川</td><td>38分</td><td>38分</td></tr>
        </table>
        <p style="margin-top:0.8rem">幅優先探索が選ぶ経路は<strong>直通（新宿 → 品川）</strong>で、書き換える前と変わりません。
        いちばん短い経路も<strong>直通の12分</strong>になるので、2つの答えは一致します。</p>
        <p style="margin-top:0.6rem"><strong>一致は偶然です。</strong>
        幅優先探索がしていることは、書き換える前とまったく同じ「路線の本数がいちばん少ない経路をさがす」ことだけです。
        重みが30分から12分に変わったことを、幅優先探索は一切見ていません。
        たまたま「本数がいちばん少ない経路」と「時間がいちばん短い経路」が同じになっただけです。</p>
        <p style="margin-top:0.6rem">確かめる方法があります。直通をもう一度30分に戻すと、幅優先探索の答えは直通のまま変わりませんが、
        いちばん短い経路は渋谷まわりに変わります。
        <strong>重みを変えても答えが変わらないアルゴリズムは、重みを考えていない</strong>ということです。
        重みを正しくあつかうには、第5回から学ぶダイクストラ法が必要になります。</p>"""),
    ("標準課題2: 自作の重み付きグラフの例", """        <p>作り方の一例として、大学の最寄り駅から教室までの経路を重み付きグラフにした場合を示します。
        自分のテーマで作れていれば、内容が違っていてかまいません。</p>
<pre><span class="code-label">Python ── AL2-04-std2.py の例</span>
campus = {
    <span class="str">"駅"</span>: [(<span class="str">"正門"</span>, <span class="num">8</span>), (<span class="str">"裏門"</span>, <span class="num">12</span>)],
    <span class="str">"正門"</span>: [(<span class="str">"駅"</span>, <span class="num">8</span>), (<span class="str">"1号館"</span>, <span class="num">3</span>), (<span class="str">"食堂"</span>, <span class="num">5</span>)],
    <span class="str">"裏門"</span>: [(<span class="str">"駅"</span>, <span class="num">12</span>), (<span class="str">"3号館"</span>, <span class="num">2</span>)],
    <span class="str">"1号館"</span>: [(<span class="str">"正門"</span>, <span class="num">3</span>), (<span class="str">"教室"</span>, <span class="num">4</span>)],
    <span class="str">"食堂"</span>: [(<span class="str">"正門"</span>, <span class="num">5</span>), (<span class="str">"教室"</span>, <span class="num">6</span>)],
    <span class="str">"3号館"</span>: [(<span class="str">"裏門"</span>, <span class="num">2</span>), (<span class="str">"教室"</span>, <span class="num">3</span>)],
    <span class="str">"教室"</span>: [(<span class="str">"1号館"</span>, <span class="num">4</span>), (<span class="str">"食堂"</span>, <span class="num">6</span>), (<span class="str">"3号館"</span>, <span class="num">3</span>)],
}</pre>
        <table style="margin-top:0.8rem">
          <tr><th>行き方</th><th>合計時間</th></tr>
          <tr><td>駅 → 正門 → 1号館 → 教室</td><td>8 + 3 + 4 = 15分</td></tr>
          <tr><td>駅 → 正門 → 食堂 → 教室</td><td>8 + 5 + 6 = 19分</td></tr>
          <tr><td>駅 → 裏門 → 3号館 → 教室</td><td>12 + 2 + 3 = <strong style="color:#76B900">17分</strong></td></tr>
        </table>
        <p style="margin-top:0.8rem">この例では「駅 → 正門 → 1号館 → 教室」の15分がいちばん短くなります。</p>
        <p style="margin-top:0.6rem"><strong>重みを料金に変えた場合の考え方:</strong>
        キャンパス内の移動はどの道も無料なので、料金を重みにするとすべての辺が0になり、
        「どの行き方も同じ」という答えになります。重みの選び方によって、問題そのものが変わってしまうということです。</p>
        <p style="margin-top:0.6rem">路線図をテーマに選んだ場合は、時間と料金で答えが変わることがよくあります。
        新幹線を使えば時間は短くなりますが料金は高くなるため、
        「時間を重みにしたときの最短経路」と「料金を重みにしたときの最短経路」は別のものになります。
        <strong>何を重みにするかを決めることは、何を大切にするかを決めること</strong>だと言えます。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "重み付きグラフとは", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("04", NAV, body)
