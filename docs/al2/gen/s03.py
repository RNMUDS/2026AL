# -*- coding: utf-8 -*-
"""第3回: グラフとデータ構造の再確認 の本文を組み立てる。"""
from collections import deque
from common import (AMBER, GRAY, GREEN, answers, code, example, fig, keywords,
                    notion, reveal, run, section, setup_guide, standard,
                    submission, write)

STATIONS = ["新宿", "渋谷", "池袋", "東京", "品川", "上野"]
LINES = [("新宿", "渋谷"), ("新宿", "池袋"), ("新宿", "東京"),
         ("渋谷", "品川"), ("東京", "品川"), ("東京", "上野"), ("池袋", "上野")]
POS = {"池袋": (260, 62), "新宿": (176, 146), "上野": (470, 62),
       "東京": (408, 152), "渋谷": (206, 252), "品川": (356, 252)}


def node(name, x, y, color=GREEN, r=26, fill="#1A1A1A", text_fill="#E0E0E0"):
    return (f'        <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>\n'
            f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="{text_fill}" font-size="12" font-weight="700">{name}</text>')


def edges_svg(color="#555", width=2):
    out = []
    for a, b in LINES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        out.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: グラフの用語
# ────────────────────────────────────────────────────────────
def fig_graph_terms():
    dur = 15
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'グラフの言葉: 頂点と辺</text>']
    s += edges_svg()
    for name, (x, y) in POS.items():
        s.append(node(name, x, y, color="#555"))
    # ① 頂点を光らせる
    for i, (name, (x, y)) in enumerate(POS.items()):
        s.append(f'        <circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{GREEN}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{0.04+i*0.02:.3f};{0.06+i*0.02:.3f};0.30;0.34;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.04;0.08;0.30;0.34;1" dur="{dur}s" repeatCount="indefinite"/>'
             '① 頂点（ちょうてん）＝ 駅。全部で6個</text>')
    # ② 辺を光らせる
    for i, (a, b) in enumerate(LINES):
        (x1, y1), (x2, y2) = POS[a], POS[b]
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AMBER}" stroke-width="4" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{0.36+i*0.02:.3f};{0.38+i*0.02:.3f};0.62;0.66;1" dur="{dur}s" repeatCount="indefinite"/></line>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.36;0.40;0.62;0.66;1" dur="{dur}s" repeatCount="indefinite"/>'
             '② 辺（へん）＝ 路線。全部で7本</text>')
    # ③ 重みの予告
    weights = {("新宿", "渋谷"): 7, ("新宿", "池袋"): 9, ("新宿", "東京"): 14,
               ("渋谷", "品川"): 15, ("東京", "品川"): 11, ("東京", "上野"): 6, ("池袋", "上野"): 12}
    for (a, b), w in weights.items():
        (x1, y1), (x2, y2) = POS[a], POS[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;0.68;0.72;0.94;0.97;1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'<rect x="{mx-14}" y="{my-11}" width="28" height="22" rx="6" fill="#0A0A0A" stroke="{GRAY}"/>'
                 f'<text x="{mx}" y="{my+5}" text-anchor="middle" fill="#ccc" font-size="12">{w}</text></g>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{GRAY}" font-size="13" font-weight="700" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.68;0.72;0.94;0.97;1" dur="{dur}s" repeatCount="indefinite"/>'
             '③ 重み（おもみ）＝ 辺ごとの数値。第4回であつかう</text>')
    return fig(700, 322, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 隣接リストと隣接行列は同じグラフを表す
# ────────────────────────────────────────────────────────────
def fig_list_vs_matrix():
    n = len(STATIONS)
    adj = {st: [] for st in STATIONS}
    for a, b in LINES:
        adj[a].append(b)
        adj[b].append(a)
    matrix = [[0] * n for _ in range(n)]
    for a, b in LINES:
        i, j = STATIONS.index(a), STATIONS.index(b)
        matrix[i][j] = matrix[j][i] = 1

    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じグラフを2通りの形で書き写す</text>',
         f'        <text x="175" y="52" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">隣接リスト</text>',
         f'        <text x="175" y="70" text-anchor="middle" fill="{GRAY}" font-size="11">駅ごとに、となりの駅を並べる</text>',
         f'        <text x="500" y="52" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">隣接行列</text>',
         f'        <text x="500" y="70" text-anchor="middle" fill="{GRAY}" font-size="11">表を作り、つながっていれば1を書く</text>',
         '        <line x1="345" y1="44" x2="345" y2="290" stroke="#333" stroke-width="1"/>']
    # 左: 隣接リスト
    for i, st in enumerate(STATIONS):
        y = 96 + i * 30
        s.append(f'        <rect x="24" y="{y-16}" width="300" height="26" rx="6" fill="#141414" stroke="#2e2e2e"/>')
        s.append(f'        <text x="36" y="{y+2}" fill="{GREEN}" font-size="12" font-weight="700">{st}</text>')
        s.append(f'        <text x="90" y="{y+2}" fill="#ccc" font-size="12">→ ' + "、".join(adj[st]) + '</text>')
    # 右: 隣接行列
    cell = 30
    mx0, my0 = 396, 100
    for j, st in enumerate(STATIONS):
        s.append(f'        <text x="{mx0+j*cell+cell/2}" y="{my0-9}" text-anchor="middle" fill="{GRAY}" font-size="10">{st}</text>')
    for i, st in enumerate(STATIONS):
        s.append(f'        <text x="{mx0-8}" y="{my0+i*cell+cell/2+4}" text-anchor="end" fill="{GRAY}" font-size="10">{st}</text>')
        for j in range(n):
            v = matrix[i][j]
            s.append(f'        <rect x="{mx0+j*cell}" y="{my0+i*cell}" width="{cell-2}" height="{cell-2}" rx="4" '
                     f'fill="{"#1a2e0a" if v else "#141414"}" stroke="{AMBER if v else "#2e2e2e"}"/>')
            s.append(f'        <text x="{mx0+j*cell+(cell-2)/2}" y="{my0+i*cell+(cell-2)/2+4}" text-anchor="middle" '
                     f'fill="{"#93D500" if v else "#555"}" font-size="12">{v}</text>')
    # 対応する行を同時に光らせる
    for i in range(n):
        a, b = i / n, (i + 1) / n
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        y = 96 + i * 30
        s.append(f'        <rect x="24" y="{y-16}" width="300" height="26" rx="6" fill="none" stroke="{GREEN}" stroke-width="2.5" opacity="0">{anim}</rect>')
        s.append(f'        <rect x="{mx0-2}" y="{my0+i*cell-2}" width="{n*cell+2}" height="{cell+2}" rx="6" fill="none" stroke="{GREEN}" stroke-width="2.5" opacity="0">{anim}</rect>')
    s.append(f'        <text x="350" y="300" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '左の1行と右の1行は、まったく同じつながりを表している</text>')
    return fig(700, 316, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 駅の数が増えたときの必要なマス数
# ────────────────────────────────────────────────────────────
def fig_size_compare():
    rows = [(6, 36, 36), (50, 2500, 300), (500, 250000, 3000), (5000, 25000000, 30000)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '駅の数が増えたとき、表に必要なマスの数はどうなるか</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり（1駅あたり3路線として計算）</text>']
    import math
    for i, (count, mat, lst) in enumerate(rows):
        y = 66 + i * 62
        s.append(f'        <text x="24" y="{y+22}" fill="#E0E0E0" font-size="12" font-weight="700">駅{count:,}個</text>')
        for j, (name, v, color) in enumerate([("隣接行列", mat, AMBER), ("隣接リスト", lst, GREEN)]):
            yy = y + j * 26
            w = math.log10(v) / 8 * 420
            s.append(f'        <text x="106" y="{yy+16}" fill="{GRAY}" font-size="10">{name}</text>')
            s.append(f'        <rect x="168" y="{yy+2}" width="{w:.0f}" height="18" rx="4" fill="{color}" opacity="0.85"/>')
            s.append(f'        <text x="{168+w+10:.0f}" y="{yy+16}" fill="{color}" font-size="11" font-weight="700">{v:,}マス</text>')
    s.append(f'        <text x="350" y="{66+4*62+14}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '駅が5000個になると、隣接行列は隣接リストの約800倍のマスが必要になる</text>')
    return fig(700, 66 + 4 * 62 + 32, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: グラフの上を幅優先探索が広がる
# ────────────────────────────────────────────────────────────
def fig_graph_bfs():
    adj = {st: [] for st in STATIONS}
    for a, b in LINES:
        adj[a].append(b)
        adj[b].append(a)
    start = "新宿"
    rides = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nx in adj[cur]:
            if nx in rides:
                continue
            rides[nx] = rides[cur] + 1
            q.append(nx)
    maxr = max(rides.values())
    dur = 10
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '新宿から出発して、乗る路線の数が少ない駅から順に広がる</text>']
    s += edges_svg()
    for name, (x, y) in POS.items():
        s.append(node(name, x, y, color="#555"))
    for name, (x, y) in POS.items():
        k = rides[name]
        a = (1 - 0.2) * k / (maxr + 1)
        s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
                 f'keyTimes="0;{a:.3f};{min(a+0.03,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(node(name, x, y, color=GREEN, fill="#1a2e0a"))
        s.append(f'          <text x="{x}" y="{y-34}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">{k}本</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '0本（新宿）→ 1本（渋谷・池袋・東京）→ 2本（品川・上野）の順に決まっていく</text>')
    return fig(700, 322, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図5: 迷路をグラフに書き直す
# ────────────────────────────────────────────────────────────
def fig_maze_as_graph():
    maze = ["S.#..", "..#..", "....#", "#.#..", "...#G"]
    cell = 40
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '迷路もグラフ: 1マスが頂点、となり合うマスのつながりが辺</text>']
    x0, y0 = 60, 60
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * cell, y0 + r * cell
            wall = maze[r][c] == "#"
            s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="5" '
                     f'fill="{"#33302a" if wall else "#141414"}" stroke="{"#4a453a" if wall else "#333"}"/>')
            label = maze[r][c] if maze[r][c] in "SG#" else ""
            if label:
                s.append(f'        <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+5}" text-anchor="middle" '
                         f'fill="{"#7a7060" if wall else AMBER}" font-size="14" font-weight="700">{label}</text>')
    s.append(f'        <text x="{x0+2.5*cell}" y="{y0+5*cell+24}" text-anchor="middle" fill="{GRAY}" font-size="12">迷路として見た形</text>')
    # 右: グラフとして見た形
    gx0, gy0 = 380, 60
    gcell = 40
    for r in range(5):
        for c in range(5):
            if maze[r][c] == "#":
                continue
            x, y = gx0 + c * gcell + 18, gy0 + r * gcell + 18
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < 5 and nc < 5 and maze[nr][nc] != "#":
                    s.append(f'        <line x1="{x}" y1="{y}" x2="{gx0+nc*gcell+18}" y2="{gy0+nr*gcell+18}" '
                             f'stroke="{GREEN}" stroke-width="2" opacity="0.7"/>')
    for r in range(5):
        for c in range(5):
            if maze[r][c] == "#":
                continue
            x, y = gx0 + c * gcell + 18, gy0 + r * gcell + 18
            s.append(f'        <circle cx="{x}" cy="{y}" r="13" fill="#1A1A1A" stroke="{GREEN}" stroke-width="1.6"/>')
            s.append(f'        <text x="{x}" y="{y+4}" text-anchor="middle" fill="#bbb" font-size="9">{r},{c}</text>')
    s.append(f'        <text x="{gx0+2.5*gcell}" y="{gy0+5*gcell+24}" text-anchor="middle" fill="{GRAY}" font-size="12">グラフとして見た形</text>')
    s.append(f'        <text x="350" y="{gy0+5*gcell+52}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '壁のマスは頂点にしない。通れるマスどうしだけを辺でつなぐ</text>')
    return fig(700, gy0 + 5 * gcell + 70, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "グラフとは #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2のマス数の比較"),
    ("#sec-examples", "tag-example", "観察記録", "例題4の変換結果"),
    ("#sec-standard", "tag-standard", "標準課題1", "路線を1本足すと？"),
    ("#sec-standard", "tag-standard", "標準課題2", "2つの表現の使い分け"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第1回・第2回であつかった迷路は、じつは<strong>グラフ</strong>という考え方の一例です。
      グラフとは、<strong>「点」と「点どうしのつながり」だけでものごとを表す方法</strong>のことです。
      点のことを<strong>頂点</strong>、つながりのことを<strong>辺</strong>と呼びます。
    </p>

    <div class="analogy">
      路線図を思い浮かべてください。実際の線路は曲がりくねっていますが、路線図では駅を丸で、路線をまっすぐな線で描きます。
      駅の正確な位置や線路の曲がり方は消えていますが、「どの駅とどの駅がつながっているか」は残っています。
      乗りかえを考えるときに必要な情報だけを残した形が、グラフです。
    </div>

{fig_graph_terms()}

    <div class="concept-box">
      <h4>グラフで表せるもの</h4>
      <table>
        <tr><th>あつかうもの</th><th>頂点になるもの</th><th>辺になるもの</th></tr>
        <tr><td>路線図</td><td>駅</td><td>駅と駅をつなぐ路線</td></tr>
        <tr><td>友達関係</td><td>人</td><td>友達であるという関係</td></tr>
        <tr><td>迷路</td><td>通れる1マス</td><td>となり合うマスどうしのつながり</td></tr>
        <tr><td>道路地図</td><td>交差点</td><td>交差点をつなぐ道路</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        見た目はまるで違いますが、どれも「頂点」と「辺」だけで書き直せます。
        書き直してしまえば、<strong>同じ1つのプログラムで4つとも解ける</strong>ようになります。
        例題4では、迷路をグラフに書き直して、例題3とまったく同じ幅優先探索で解きます。
      </p>
    </div>

    <div class="concept-box">
      <h4>グラフをPythonに書き写す2つの方法</h4>
      <p style="font-size:0.95rem">
        紙に描いたグラフを、そのままPythonに渡すことはできません。数や文字の形に書き写す必要があります。
        書き写し方には、よく使われる方法が2つあります。
      </p>
      <ul class="point-list" style="margin-top:0.6rem">
        <li><strong style="color:#76B900">隣接リスト</strong>（りんせつリスト）: 頂点ごとに「となりの頂点」を並べる。辞書とリストで書ける。</li>
        <li><strong style="color:#FFB800">隣接行列</strong>（りんせつぎょうれつ）: たてよこの表を作り、つながっていれば1、つながっていなければ0を書く。</li>
      </ul>
    </div>

{fig_list_vs_matrix()}"""

ex1_body = f"""      <p>6つの駅と7本の路線からなる路線図を、隣接リストの形でPythonに書き写します。
      隣接リストは<strong>辞書</strong>を使い、「駅の名前」を鍵、「となりの駅を並べたリスト」を値にします。</p>

{code('AL2-03-ex1.py')}

{run('a03_ex1_result.png', '6つの駅それぞれについて、となりの駅が一覧で表示されました。'
     '<code>railway["新宿"]</code> と書くだけで、新宿のとなりの駅3つがすぐ取り出せています。'
     '辺（路線）の数を数えるときに <code>// 2</code> で半分にしているのは、'
     '1本の路線が「新宿の側」と「渋谷の側」の両方から数えられてしまうためです。')}"""

ex2_body = f"""      <p>例題1とまったく同じ路線図を、今度は隣接行列の形で書き写します。
      6つの駅があるので、たて6マス・よこ6マスの表を作ります。</p>

{code('AL2-03-ex2.py')}

{fig_size_compare()}

{run('a03_ex2_result.png', '同じ路線図が、6×6＝36マスの表になりました。'
     '表のななめの線（自分自身との交点）はすべて0で、表は左上から右下の線を軸にして<strong>対称</strong>になっています。'
     '「新宿と東京はつながっているか」は <code>matrix[0][3]</code> を見るだけで分かります。'
     '一方で、駅の数が5000個になると、隣接行列は2500万マス、隣接リストは3万マスで、約800倍の差が出ています。')}

{notion('例題2の最後の表から、駅の数が6個・50個・500個・5000個のときの「隣接行列のマス数」と「隣接リストのマス数」を書き写す。'
        'あわせて、駅の数が10倍になったとき、それぞれのマス数が何倍になるかを書く。')}"""

ex3_body = f"""      <p>迷路で使った幅優先探索を、そのままグラフに使います。
      「新宿から各駅まで、何本の路線に乗ればたどり着けるか」を求めます。</p>

{code('AL2-03-ex3.py')}

{fig_graph_bfs()}

{run('a03_ex3_result.png', '新宿から見て、渋谷・池袋・東京は<strong>1本</strong>、品川・上野は<strong>2本</strong>という結果になりました。'
     '実行結果の上半分を見ると、幅優先探索が「新宿 → 渋谷・池袋・東京 → 品川・上野」の順に調べていることが分かります。'
     '1本で行ける駅をすべて調べ終えてから、2本で行ける駅に進んでいます。迷路のときとまったく同じ進み方です。')}"""

ex4_body = f"""      <p>迷路をグラフ（隣接リスト）に書き直してから、例題3と同じ幅優先探索で解きます。
      迷路の1マスを1つの頂点とし、頂点の名前を <code>"(行,列)"</code> という文字列にします。</p>

{code('AL2-03-ex4.py')}

{fig_maze_as_graph()}

{run('a03_ex4_result.png', '5マス×5マスの迷路のうち、壁ではないマスは<strong>19個</strong>ありました。'
     '19個の頂点と、となり合うマスどうしの辺からなるグラフに書き直せています。'
     '書き直したあとは、例題3の路線図とまったく同じコードで最短経路（8歩）が求まりました。'
     '見た目がまったく違う迷路と路線図が、グラフという同じ形に書き直すことで、同じプログラムで解けるようになります。')}

{notion('例題4の実行結果から、迷路の頂点の数と、(0,0) の頂点につながっている頂点を書き写す。'
        'あわせて、迷路をグラフに書き直したことで何が便利になったかを、自分の言葉で説明する。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('03', ['AL2-03-ex1.py', 'AL2-03-ex2.py', 'AL2-03-ex3.py', 'AL2-03-ex4.py'])}

{keywords([
    ('グラフ', 'graph', '「点」と「点どうしのつながり」だけでものごとを表す方法。棒グラフや折れ線グラフとは別のもの。'),
    ('頂点', 'ちょうてん / vertex', 'グラフの「点」。駅・人・迷路の1マスなどが頂点になる。ノード（node）とも呼ぶ。'),
    ('辺', 'へん / edge', 'グラフの「つながり」。路線・友達関係・となり合うマスの関係などが辺になる。'),
    ('隣接リスト', 'りんせつリスト / adjacency list', '頂点ごとに、となりの頂点を並べた表し方。辺の数だけ場所を使うので、辺が少ないグラフに向く。'),
    ('隣接行列', 'りんせつぎょうれつ / adjacency matrix', 'たてよこの表を作り、つながっていれば1を書く表し方。「2点がつながっているか」を1回で調べられる。'),
])}

{example(1, '隣接リストで路線図を表す', ex1_body)}

{example(2, '隣接行列で同じ路線図を表す', ex2_body)}

{example(3, 'グラフの上を幅優先探索する', ex3_body)}

{example(4, '迷路をグラフに書き直して解く', ex4_body)}"""

std1_body = """      <p>例題3のファイル <code>AL2-03-ex3.py</code> を開き、路線図に<strong>新宿と品川を直接つなぐ新しい路線</strong>を1本追加します。
      隣接リストは両方の駅を書き換える必要があります。</p>

<pre><span class="code-label">Python ── 書き換える2行</span>
    <span class="str">"新宿"</span>: [<span class="str">"渋谷"</span>, <span class="str">"池袋"</span>, <span class="str">"東京"</span>, <span class="str">"品川"</span>],   <span class="cmt"># ← "品川" を足す</span>
    <span class="str">"品川"</span>: [<span class="str">"渋谷"</span>, <span class="str">"東京"</span>, <span class="str">"新宿"</span>],           <span class="cmt"># ← "新宿" を足す</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、6つの駅それぞれについて「乗る路線の数」がどうなるかを予測してNotionに書く</li>
          <li>2行を書き換えて保存し、実行する</li>
          <li>実際の結果を記録し、予測と比べる</li>
          <li>新宿から品川への行き方が、書き換える前とどう変わったかを書く</li>
        </ol>
      </div>

      <table>
        <tr><th>駅</th><th>書き換える前</th><th>予測</th><th>実際</th></tr>
        <tr><td>渋谷</td><td>1本</td><td></td><td></td></tr>
        <tr><td>池袋</td><td>1本</td><td></td><td></td></tr>
        <tr><td>東京</td><td>1本</td><td></td><td></td></tr>
        <tr><td>品川</td><td>2本</td><td></td><td></td></tr>
        <tr><td>上野</td><td>2本</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 隣接リストの片方（<code>"新宿"</code> の行）だけを書き換えて、
      もう片方（<code>"品川"</code> の行）を書き換え忘れると、どんな問題が起きるかを説明してください。</p>
"""

std2_body = """      <p>例題1から例題4までの結果をもとに、隣接リストと隣接行列の使い分けを表にまとめます。
      表はNotionに作り、空欄をすべて埋めてください。</p>

      <table>
        <tr><th>比べる点</th><th>隣接リスト</th><th>隣接行列</th></tr>
        <tr><td>書き方</td><td></td><td></td></tr>
        <tr><td>駅が5000個のときのマス数</td><td></td><td></td></tr>
        <tr><td>「2駅が直接つながっているか」の調べやすさ</td><td></td><td></td></tr>
        <tr><td>「ある駅のとなりの駅をすべて並べる」調べやすさ</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem">表を作ったうえで、次の2つの場面には、それぞれどちらの表し方が向いているかを<strong>理由つきで</strong>答えてください。</p>
      <ul class="point-list">
        <li><strong>場面A:</strong> 日本全国の鉄道路線図（駅が約9000個、1駅あたりつながる駅は2〜4個）をあつかう</li>
        <li><strong>場面B:</strong> 30人のクラス全員について、「誰と誰が同じ委員会か」を何度も繰り返し調べる</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    標準課題1は<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, '路線を1本足すと、乗る路線の数はどう変わるか', std1_body)}
{notion('5つの駅についての予測と実際の表、新宿から品川への行き方の変化、および「片方だけ書き換えたときに起きる問題」の説明。')}

{standard(2, '隣接リストと隣接行列の使い分け', std2_body)}
{notion('4行の比較表（空欄をすべて埋める）と、場面A・場面Bそれぞれに向いている表し方とその理由。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第3回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 駅の数ごとのマス数の表、10倍になったときの増え方</li>
        <li><strong>例題4</strong>: 迷路の頂点の数、(0,0) につながる頂点、書き直して便利になったこと</li>
        <li><strong>標準課題1</strong>: 予測と実際の表、行き方の変化、片方だけ書き換えたときの問題</li>
        <li><strong>標準課題2</strong>: 比較表、場面A・場面Bへの答えと理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: 路線を1本足したときの結果", """        <table>
          <tr><th>駅</th><th>書き換える前</th><th>書き換えたあと</th></tr>
          <tr><td>渋谷</td><td>1本</td><td>1本（変わらない）</td></tr>
          <tr><td>池袋</td><td>1本</td><td>1本（変わらない）</td></tr>
          <tr><td>東京</td><td>1本</td><td>1本（変わらない）</td></tr>
          <tr><td>品川</td><td>2本</td><td><strong style="color:#76B900">1本（1本減る）</strong></td></tr>
          <tr><td>上野</td><td>2本</td><td>2本（変わらない）</td></tr>
        </table>
        <p style="margin-top:0.8rem">新宿から品川への行き方は、<strong>「新宿 → 渋谷 → 品川」から「新宿 → 品川」へ変わります。</strong>
        新しい直通の路線ができたので、渋谷で乗りかえる必要がなくなりました。</p>
        <p style="margin-top:0.6rem">上野が2本のまま変わらないのは、新しい路線が上野に関係していないからです。
        上野へは「新宿 → 池袋 → 上野」または「新宿 → 東京 → 上野」の2本が必要で、近道はできていません。</p>
        <p style="margin-top:0.6rem"><strong>片方だけ書き換えたときに起きる問題:</strong>
        <code>"新宿"</code> の行にだけ <code>"品川"</code> を足すと、「新宿から品川へは行けるが、品川から新宿へは行けない」という、
        <strong>一方通行の路線</strong>になってしまいます。
        新宿を出発点にした探索では品川が1本と出ますが、品川を出発点にすると新宿は2本のままです。
        路線のように「行き帰りの両方を通れる」つながりを表すときは、隣接リストの両方の行を必ず書き換えます。
        なお、一方通行を<strong>わざと</strong>表したいときには、片方だけ書く形が正しい書き方になります（有向グラフと呼びます）。</p>"""),
    ("標準課題2: 使い分けの表と答え", """        <table>
          <tr><th>比べる点</th><th>隣接リスト</th><th>隣接行列</th></tr>
          <tr><td>書き方</td><td>頂点ごとに、となりの頂点を並べる（辞書とリスト）</td><td>たてよこの表を作り、つながっていれば1を書く</td></tr>
          <tr><td>駅が5000個のときのマス数</td><td>30,000マス</td><td>25,000,000マス</td></tr>
          <tr><td>2駅が直接つながっているか</td><td>リストの中を順に探すので少し時間がかかる</td><td><strong>表を1回見るだけ</strong>で分かる</td></tr>
          <tr><td>となりの駅をすべて並べる</td><td><strong>リストをそのまま取り出せる</strong></td><td>その行の5000マスを全部調べる必要がある</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>場面A（全国の鉄道路線図）: 隣接リスト</strong><br>
        駅が9000個あるので、隣接行列にすると8100万マスが必要になります。
        しかも1駅あたりつながる駅は2〜4個しかないので、表のほとんどのマスが0で埋まり、場所のむだが非常に大きくなります。
        辺が少ないグラフでは隣接リストを選びます。</p>
        <p style="margin-top:0.6rem"><strong>場面B（30人のクラスの委員会）: 隣接行列</strong><br>
        30人なら表は30×30＝900マスで、まったく大きくありません。
        「AさんとBさんは同じ委員会か」を何度も繰り返し調べるので、表を1回見るだけで答えが出る隣接行列が向いています。
        頂点が少なく、同じ質問を何度もするときは隣接行列を選びます。</p>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        頂点が多くて辺が少ないなら隣接リスト、頂点が少ないか辺がとても多いなら隣接行列、と覚えてください。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "グラフとは", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("03", NAV, body)
