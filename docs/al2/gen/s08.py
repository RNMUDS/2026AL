# -*- coding: utf-8 -*-
"""第8回: 巡回セールスマン問題（1）概要 の本文を組み立てる。"""
import math
from itertools import permutations
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
                    AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)

CITIES = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9),
          ("カフェ", 6, 12), ("公園", 3, 8), ("駅", 17, 4),
          ("病院", 12, 13), ("書店", 8, 7)]


def dist_table(cities, rounded=False):
    """都市どうしの直線距離の表。rounded=True なら例題1・例題2と同じく小数第1位に丸める。"""
    n = len(cities)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            d = math.sqrt((cities[i][1] - cities[j][1]) ** 2 + (cities[i][2] - cities[j][2]) ** 2)
            row.append(round(d, 1) if rounded else d)
        out.append(row)
    return out


def tour_len(order, table):
    total, here = 0.0, 0
    for c in order:
        total += table[here][c]
        here = c
    return total + table[here][0]


def best_tour(cities):
    table = dist_table(cities)
    best, bo = None, None
    for order in permutations(range(1, len(cities))):
        t = tour_len(order, table)
        if best is None or t < best:
            best, bo = t, order
    return bo, round(best, 1)


def city_dot(x, y, label, sx, sy, ox, oy, color=GREEN, r=14, sub=None):
    cx, cy = ox + x * sx, oy + y * sy
    out = [f'        <circle cx="{cx}" cy="{cy}" r="{r}" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>',
           f'        <text x="{cx}" y="{cy+4}" text-anchor="middle" fill="#E0E0E0" font-size="{r-3}" font-weight="700">{label}</text>']
    if sub:
        out.append(f'        <text x="{cx}" y="{cy-r-6}" text-anchor="middle" fill="{GRAY}" font-size="10">{sub}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 巡回セールスマン問題とは
# ────────────────────────────────────────────────────────────
def fig_tsp_intro():
    cities = CITIES[:5]
    order, best = best_tour(cities)
    sx, sy, ox, oy = 31, 21, 44, 52
    route = [0] + list(order) + [0]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '巡回セールスマン問題: 全ての都市を1回ずつ回って出発点へ戻る最短ルート</text>']
    # 都市どうしの線（薄く）
    for i in range(5):
        for j in range(i + 1, 5):
            x1, y1 = ox + cities[i][1] * sx, oy + cities[i][2] * sy
            x2, y2 = ox + cities[j][1] * sx, oy + cities[j][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2a2a2a" stroke-width="1"/>')
    # ルートを順に引く
    table = dist_table(cities)
    for k in range(len(route) - 1):
        a, b = route[k], route[k + 1]
        x1, y1 = ox + cities[a][1] * sx, oy + cities[a][2] * sy
        x2, y2 = ox + cities[b][1] * sx, oy + cities[b][2] * sy
        p0 = (1 - 0.2) * k / (len(route) - 1)
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                 f'dur="{dur}s" repeatCount="indefinite"/></line>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'        <text x="{mx}" y="{my-6}" text-anchor="middle" fill="{GREEN}" font-size="11" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                 f'dur="{dur}s" repeatCount="indefinite"/>{round(table[a][b],1)}</text>')
    for i, (name, x, y) in enumerate(cities):
        color = AMBER if i == 0 else GREEN
        s += city_dot(x, y, str(i), sx, sy, ox, oy, color, 16, name)
    s.append(f'        <rect x="430" y="60" width="240" height="88" rx="10" fill="#141414" stroke="#333"/>')
    s.append(f'        <text x="550" y="84" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">3つのきまり</text>')
    for i, t in enumerate(["すべての都市を回る", "同じ都市は1回だけ", "最後は出発点へ戻る"]):
        s.append(f'        <text x="550" y="{106+i*18}" text-anchor="middle" fill="#ccc" font-size="11">{t}</text>')
    s.append(f'        <text x="350" y="{oy+13*sy+30}" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             f'最短ルート: 学校 → 郵便局 → 図書館 → カフェ → 公園 → 学校　合計 {best}</text>')
    return fig(700, oy + 13 * sy + 48, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 都市の数と順番の数
# ────────────────────────────────────────────────────────────
def fig_factorial():
    rows = []
    for n in [5, 8, 10, 12, 15, 20]:
        total = 1
        for k in range(1, n):
            total *= k
        rows.append((n, total))
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が1つ増えるだけで、試す順番の数は何倍にもなる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり。右の時間は、12都市が8.7秒だった実測からの見積もり</text>']
    notes = {5: "一瞬", 8: "一瞬", 10: "0.07秒", 12: "8.7秒",
             15: "約5時間", 20: "約800年"}
    for i, (n, total) in enumerate(rows):
        y = 66 + i * 46
        big = total > 10 ** 9
        color = RED if big else GREEN
        w = math.log10(total) / 18 * 380
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{n}都市</text>')
        s.append(f'        <rect x="92" y="{y+4}" width="{max(w,3):.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{92+max(w,3)+10:.0f}" y="{y+21}" fill="{color}" font-size="11" font-weight="700">{total:,}通り</text>')
        s.append(f'        <text x="676" y="{y+21}" text-anchor="end" fill="{GRAY}" font-size="11">{notes[n]}</text>')
    s.append(f'        <text x="350" y="{66+6*46+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             'このように急激に増える問題を、コンピュータの世界では「NP困難」と呼ぶ</text>')
    return fig(700, 66 + 6 * 46 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 全探索が24通りを順に試す
# ────────────────────────────────────────────────────────────
def fig_bruteforce():
    cities = CITIES[:5]
    table = dist_table(cities, rounded=True)
    orders = [(1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (2, 1, 3, 4),
              (3, 2, 1, 4), (4, 3, 2, 1)]
    sx, sy = 12, 10
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索: 24通りの順番を1つずつ試して、いちばん短いものを選ぶ</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '24通りのうち6通りを表示（0 = 学校）</text>']
    for i, order in enumerate(orders):
        px = 20 + (i % 3) * 226
        py = 0 if i < 3 else 180
        length = round(tour_len(order, table), 1)
        best = (length == 34.9)
        color = GREEN if best else "#666"
        s.append(f'        <rect x="{px}" y="{56+py}" width="212" height="164" rx="10" fill="#141414" stroke="{color if best else "#333"}" stroke-width="{2.5 if best else 1}"/>')
        route = [0] + list(order) + [0]
        for k in range(len(route) - 1):
            a, b = route[k], route[k + 1]
            x1 = px + 22 + cities[a][1] * sx
            y1 = 74 + py + cities[a][2] * sy
            x2 = px + 22 + cities[b][1] * sx
            y2 = 74 + py + cities[b][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>')
        for j, (name, x, y) in enumerate(cities):
            cx = px + 22 + x * sx
            cy = 74 + py + y * sy
            s.append(f'        <circle cx="{cx}" cy="{cy}" r="8" fill="#1A1A1A" stroke="{AMBER if j == 0 else color}" stroke-width="1.5"/>')
            s.append(f'        <text x="{cx}" y="{cy+3}" text-anchor="middle" fill="#ccc" font-size="8">{j}</text>')
        s.append(f'        <text x="{px+106}" y="{212+py}" text-anchor="middle" fill="{color if best else "#999"}" '
                 f'font-size="12" font-weight="700">{"".join(str(c) for c in order)} → {length}{"  最短" if best else ""}</text>')
        a0 = (1 - 0.2) * i / len(orders)
        s.append(f'        <rect x="{px-2}" y="{54+py}" width="216" height="168" rx="12" fill="none" stroke="{AMBER}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a0:.3f};{a0+0.01:.3f};{a0+0.11:.3f};{a0+0.12:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="350" y="418" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '全探索は必ず正しい答えを出すが、都市が増えると終わらなくなる</text>')
    return fig(700, 434, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 5都市と8都市の最適ルート
# ────────────────────────────────────────────────────────────
def fig_five_vs_eight():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が増えると、ルートの形そのものが変わる</text>']
    for panel, count in enumerate([5, 8]):
        cities = CITIES[:count]
        order, best = best_tour(cities)
        table = dist_table(cities)
        x0 = 20 + panel * 350
        sx, sy = 15.5, 12.5
        ox, oy = x0 + 22, 74
        s.append(f'        <rect x="{x0}" y="46" width="330" height="252" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="66" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
                 f'{count}都市の最短ルート: 合計 {best}</text>')
        route = [0] + list(order) + [0]
        for k in range(len(route) - 1):
            a, b = route[k], route[k + 1]
            x1, y1 = ox + cities[a][1] * sx, oy + cities[a][2] * sy
            x2, y2 = ox + cities[b][1] * sx, oy + cities[b][2] * sy
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{GREEN}" stroke-width="2.5"/>')
        visit = {0: "S"}
        for k, c in enumerate(order):
            visit[c] = str(k + 1)
        for i, (name, x, y) in enumerate(cities):
            cx, cy = ox + x * sx, oy + y * sy
            color = AMBER if i == 0 else GREEN
            s.append(f'        <circle cx="{cx:.0f}" cy="{cy:.0f}" r="11" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>')
            s.append(f'        <text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" fill="#E0E0E0" font-size="10" font-weight="700">{visit[i]}</text>')
            s.append(f'        <text x="{cx:.0f}" y="{cy-15:.0f}" text-anchor="middle" fill="{GRAY}" font-size="9">{name}</text>')
    s.append(f'        <text x="350" y="320" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '5都市の答えに3都市を足すだけでは、8都市の最短ルートにはならない</text>')
    return fig(700, 336, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "巡回セールスマン問題 #sec-explanation",
    "例題 #sec-examples",
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("08")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回から第7回まででは、<strong>2地点のあいだ</strong>の最短経路を求めました。
      第8回からは問題の形が変わります。求めるのは<strong>すべての地点を1回ずつ回って出発点へ戻る、いちばん短いルート</strong>です。
      巡回セールスマン問題（じゅんかいセールスマンもんだい）と呼ばれ、
      英語の頭文字をとって<strong>TSP</strong>と書かれることもあります。
    </p>

    <div class="analogy">
      宅配便のドライバーが、営業所を出発して10軒の家に荷物を届け、営業所へ戻る場面を思い浮かべてください。
      どの家から回るかで、走る距離もかかる時間も変わります。
      同じ問題は、基板に穴をあける機械のドリルの動かし方、
      工場の部品を取りに行くロボットの動き方など、いろいろな場面に現れます。
    </div>

{fig_tsp_intro()}

    <div class="concept-box">
      <h4>ダイクストラ法との違い</h4>
      <table>
        <tr><th></th><th>ダイクストラ法（第5〜7回）</th><th>巡回セールスマン問題（第8〜10回）</th></tr>
        <tr><td>求めるもの</td><td>出発点から目的地までの最短経路</td><td>すべての都市を1回ずつ回って戻る最短ルート</td></tr>
        <tr><td>通らなくてよい地点</td><td>ある（近道でないなら通らない）</td><td>ない（全部必ず1回通る）</td></tr>
        <tr><td>決めるもの</td><td>どの道を通るか</td><td>どの順番で回るか</td></tr>
        <tr><td>速く解く方法</td><td>ある（ダイクストラ法）</td><td>まだ見つかっていない</td></tr>
      </table>
    </div>

    <div class="concept-box">
      <h4>順番の数え方</h4>
      <p style="font-size:0.95rem">
        都市が5個あり、そのうち1個を出発点とします。残りの4個を回る順番は
        <strong>4 × 3 × 2 × 1 = 24通り</strong>です。
        最初に選べる都市が4通り、次が3通り、その次が2通り、最後は1通りに決まるためです。
        1から順にかけ算した値を<strong>階乗</strong>（かいじょう）と呼び、<code>4!</code> と書きます。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        都市が n 個なら <code>(n-1)!</code> 通りです。
        6都市なら120通り、8都市なら5,040通り、12都市なら約4,000万通りになります。
      </p>
    </div>

{fig_factorial()}

    <div class="note-warn">
      <strong>NP困難（エヌピーこんなん）:</strong>
      巡回セールスマン問題には、都市が増えても現実的な時間で必ず最適解を出せる方法が、
      <strong>いまだに見つかっていません</strong>。
      「速く解く方法は存在しないだろう」と多くの研究者が考えていますが、証明もされていません。
      証明できた人には100万ドルの賞金がかけられている、有名な未解決問題の1つです。
    </div>"""

ex1_body = f"""      <p>巡回セールスマン問題を解く準備として、都市の位置から<strong>距離の表</strong>を作ります。
      2つの都市のあいだの直線距離は、三平方の定理で求められます。</p>

      <div class="concept-box">
        <h4>2点のあいだの距離</h4>
        <p style="font-size:0.95rem">点(x1, y1) と点(x2, y2) のあいだの直線距離は、
        よこの差とたての差から <code>math.sqrt((x1-x2)**2 + (y1-y2)**2)</code> で求まります。
        <code>**2</code> は2乗、<code>math.sqrt</code> は平方根（ルート）を求める命令です。</p>
      </div>

{code('AL2-08-ex1.py')}

{run('a08_ex1_result.png', '5つの都市について、5行5列の距離の表ができました。'
     'ななめの線（0行0列、1行1列、…）はすべて 0.0 です。自分自身との距離は0だからです。'
     'また、0行1列と1行0列がどちらも 8.1 のように、表は<strong>左上から右下の線を軸にして対称</strong>になっています。'
     '行きと帰りで同じ距離だからです。'
     'いちばん下の地図では、5つの都市の位置関係が確かめられます。')}"""

ex2_body = f"""      <p>学校を出発点とし、残りの4つの都市を回る順番をすべて書き出して、いちばん短いルートをさがします。
      並べ方をすべて作るには <code>itertools</code> の <code>permutations</code> を使います。</p>

      <div class="concept-box">
        <h4>permutations（順列）</h4>
        <p style="font-size:0.95rem">
          <code>permutations([1, 2, 3])</code> と書くと、
          <code>(1,2,3) (1,3,2) (2,1,3) (2,3,1) (3,1,2) (3,2,1)</code> の6通りをすべて作ってくれます。
          自分で入れ子のループを書かなくてよいので、全探索のコードがとても短くなります。
        </p>
      </div>

{code('AL2-08-ex2.py')}

{fig_bruteforce()}

{run('a08_ex2_result.png', '24通りすべての合計距離が表示され、最短は<strong>34.9</strong>でした。'
     'ルートは「学校 → 郵便局 → 図書館 → カフェ → 公園 → 学校」です。'
     'いちばん下に表示した逆回りのルートも、同じ34.9になっています。'
     '同じ道を反対向きに走るだけなので、距離が変わらないためです。'
     '24通りの中には、実際には12通りの「別のルート」しかなく、残り12通りはその逆回りだということです。')}

{notion('例題2の実行結果から、最短ルートと合計距離、いちばん長かったルートと合計距離を書く。'
        'あわせて、24通りの中に「同じ形のルート」が2つずつある理由を説明する。')}"""

ex3_body = f"""      <p>都市の数を5個から12個まで増やし、全探索にかかる時間を測ります。
      12都市は約4,000万通りを試すので、実行に10秒ほどかかります。</p>

{code('AL2-08-ex3.py')}

{run('a08_ex3_result.png', '10都市で362,880通り（0.07秒ほど）、11都市で3,628,800通り（0.7秒ほど）、'
     '12都市で39,916,800通り（<strong>約9秒</strong>）でした。'
     '都市が1つ増えるたびに、時間がおよそ<strong>10倍</strong>になっています。'
     '下の表は、実際には試さずに順番の数だけを計算した結果です。'
     '12都市の約4000万通りに8.7秒かかったので、1秒あたり約460万通り調べている計算になります。'
     '同じ速さだとすると、15都市（871億通り）には約5時間、20都市（約12京通り）には約800年かかります。'
     '秒数はパソコンの性能で変わるので、自分の結果が画像と一致しなくても問題ありません。')}

{notion('例題3の上の表から、都市の数ごとの「試した順番の数」と「かかった時間」を書き写す。'
        'あわせて、都市が1つ増えるとかかる時間が何倍になったかを計算して書く。')}"""

ex4_body = f"""      <p>最短ルートの中身を、区間ごとに分けて表示します。
      5都市のときと8都市のときで、ルートの形がどう変わるかを見比べてください。</p>

{code('AL2-08-ex4.py')}

{fig_five_vs_eight()}

{run('a08_ex4_result.png', '5都市の最短ルートは合計<strong>34.9</strong>、8都市の最短ルートは合計<strong>46.8</strong>でした。'
     '5都市のときは「学校 → 郵便局 → 図書館 → カフェ → 公園 → 学校」の順に回っていましたが、'
     '8都市になると「学校 → 公園 → カフェ → 病院 → 図書館 → 駅 → 郵便局 → 書店 → 学校」と、'
     '<strong>まったく逆向きの回り方</strong>に変わっています。'
     '都市を足すと、それまでの順番はそのまま使えなくなるということです。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題3は実行に10秒ほどかかります。まず作業フォルダを用意します。</p>

{setup_guide('08', ['AL2-08-ex1.py', 'AL2-08-ex2.py', 'AL2-08-ex3.py', 'AL2-08-ex4.py'])}

{keywords([
    ('巡回セールスマン問題', 'じゅんかいセールスマンもんだい / TSP', 'すべての都市を1回ずつ回って出発点へ戻る、合計距離がいちばん短いルートを求める問題。'),
    ('階乗', 'かいじょう / factorial', '1からその数までを順にかけた値。<code>4!</code> は 4×3×2×1＝24。都市がn個のときのルート数は <code>(n-1)!</code> 通り。'),
    ('permutations', 'じゅんれつ / 順列', 'Pythonの <code>itertools</code> にある道具。並べ方をすべて作ってくれる。'),
    ('NP困難', 'エヌピーこんなん / NP-hard', '都市が増えると、現実的な時間で必ず最適解を出す方法が知られていない問題のこと。巡回セールスマン問題はその代表例。'),
    ('距離行列', 'きょりぎょうれつ / distance matrix', 'すべての都市の組み合わせについて距離を書き並べた表。第3回の隣接行列と同じ形。'),
])}

{example(1, '都市の位置から距離の表を作る', ex1_body)}

{example(2, '全探索で最短ルートを求める', ex2_body)}

{example(3, '都市を増やすと時間はどうなるか', ex3_body)}

{example(4, '最短ルートの中身を区間ごとに見る', ex4_body)}"""

ans = answers([
    ("確かめ用の数値", """        <p><strong>問い1（長方形の4すみ・手計算）</strong></p>
        <table>
          <tr><th>ルート</th><th>計算</th><th>合計</th></tr>
          <tr><td>0 → 1 → 2 → 3 → 0</td><td>4 + 3 + 4 + 3</td><td><strong style="color:#76B900">14</strong></td></tr>
          <tr><td>0 → 1 → 3 → 2 → 0</td><td>4 + 5 + 4 + 5</td><td>18</td></tr>
          <tr><td>0 → 2 → 1 → 3 → 0</td><td>5 + 3 + 5 + 3</td><td>16</td></tr>
          <tr><td>0 → 2 → 3 → 1 → 0</td><td>5 + 4 + 5 + 4</td><td>18</td></tr>
          <tr><td>0 → 3 → 1 → 2 → 0</td><td>3 + 5 + 3 + 5</td><td>16</td></tr>
          <tr><td>0 → 3 → 2 → 1 → 0</td><td>3 + 4 + 3 + 4</td><td><strong style="color:#76B900">14</strong></td></tr>
        </table>
        <p style="margin-top:0.6rem">最短は14で、長方形の外周を一周する形です。
        ルートが交差しているものほど長くなります。</p>
        <p style="margin-top:0.8rem"><strong>問い2の根拠</strong>: 20軒なら 19! ＝ 約12京通り。
        12都市の約4000万通りに約9秒かかったので、同じ速さでも<strong>約800年</strong>かかります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "巡回セールスマン問題とは", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("08", SLIDES),
    rubric_section("08"),
    ans,
])

write("08", NAV, body)
