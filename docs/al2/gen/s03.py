# -*- coding: utf-8 -*-
"""第3回: グラフとデータ構造の再確認 の本文を組み立てる。"""
from collections import deque
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
                    AMBER, GRAY, GREEN, answers, code, example, fig, keywords,
                    notion, reveal, run, section, setup_guide, standard,
                    write)

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
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("03")

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

ans = answers([
    ("確かめ用の数値", """        <table>
          <tr><th>駅の数</th><th>隣接行列</th><th>隣接リスト</th></tr>
          <tr><td>6</td><td>36マス</td><td>36マス</td></tr>
          <tr><td>50</td><td>2,500マス</td><td>300マス</td></tr>
          <tr><td>500</td><td>250,000マス</td><td>3,000マス</td></tr>
          <tr><td>5,000</td><td>25,000,000マス</td><td>30,000マス</td></tr>
        </table>
        <p style="margin-top:0.6rem">駅の数が10倍になると、隣接行列は<strong>100倍</strong>、隣接リストは<strong>10倍</strong>になります。</p>
        <p style="margin-top:0.8rem"><strong>問い2（新宿—品川を足したとき）</strong>:
        新宿0、渋谷1、池袋1、東京1、<strong style="color:#76B900">品川1（2から1へ）</strong>、上野2（変わらず）。
        新宿から品川は「新宿 → 渋谷 → 品川」から「新宿 → 品川」に変わります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "グラフとは", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("03", SLIDES),
    rubric_section("03"),
    ans,
])

write("03", NAV, body)
