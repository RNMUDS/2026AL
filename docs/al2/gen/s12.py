# -*- coding: utf-8 -*-
"""第12回: 数当てゲーム・パズルの再応用 の本文を組み立てる。"""
import math
from collections import deque
from common import (AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

MAZE = ["S..#....", ".#.#.##.", ".#...#..", ".###.#..",
        ".....#..", "#.##....", "...#.##.", ".#......"]
ITEMS = {"A": (0, 2), "B": (1, 7), "C": (2, 0), "D": (2, 3)}


def bfs_path(origin, target):
    rows = cols = 8
    prev = {origin: None}
    q = deque([origin])
    while q:
        u = q.popleft()
        if u == target:
            break
        r, c = u
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and MAZE[nr][nc] != "#" and (nr, nc) not in prev:
                prev[(nr, nc)] = u
                q.append((nr, nc))
    p, n = [], target
    while n is not None:
        p.append(n)
        n = prev[n]
    return list(reversed(p))


def full_path(order):
    points = [(0, 0)] + [ITEMS[k] for k in order] + [(7, 7)]
    out = []
    for i in range(len(points) - 1):
        seg = bfs_path(points[i], points[i + 1])
        out += seg if i == 0 else seg[1:]
    return out


# ────────────────────────────────────────────────────────────
# 図1: 候補の減り方
# ────────────────────────────────────────────────────────────
def fig_narrowing():
    a = [100, 99, 98, 97, 96, 95, 94]
    b = [100, 50, 24, 12, 6, 3, 1]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '1回の質問で「残る候補」がどれだけ減るか</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さが残っている候補の数（秘密の数が73のとき）</text>']
    for i in range(7):
        y = 66 + i * 40
        s.append(f'        <text x="24" y="{y+22}" fill="#ccc" font-size="11">{i+1}回目</text>')
        s.append(f'        <text x="86" y="{y+14}" fill="{RED}" font-size="10">1から順</text>')
        s.append(f'        <rect x="150" y="{y+2}" width="{a[i]*4.4:.0f}" height="15" rx="4" fill="{RED}" opacity="0.85"/>')
        s.append(f'        <text x="{150+a[i]*4.4+8:.0f}" y="{y+14}" fill="{RED}" font-size="10">{a[i]}個</text>')
        s.append(f'        <text x="86" y="{y+32}" fill="{GREEN}" font-size="10">まん中</text>')
        s.append(f'        <rect x="150" y="{y+20}" width="{max(b[i]*4.4,3):.0f}" height="15" rx="4" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{150+max(b[i]*4.4,3)+8:.0f}" y="{y+32}" fill="{GREEN}" font-size="10">{b[i]}個</text>')
    s.append(f'        <text x="350" y="{66+7*40+18}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '「1回でいちばん多く候補を減らす」選び方をすると、まん中を聞くことになる</text>')
    return fig(700, 66 + 7 * 40 + 36, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: アイテム集めパズル
# ────────────────────────────────────────────────────────────
def fig_items():
    cell = 34
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'アイテム集めパズル: 4つのアイテムを拾ってゴールへ</text>']
    panels = [(("A", "D", "B", "C"), "貪欲法: 38歩", 20, AMBER),
              (("C", "A", "D", "B"), "全探索: 22歩（最短）", 370, GREEN)]
    for order, title, x0, color in panels:
        path = full_path(order)
        s.append(f'        <rect x="{x0}" y="46" width="310" height="322" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+155}" y="68" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 82
        gx = x0 + 20
        on = set(path)
        for r in range(8):
            for c in range(8):
                x, y = gx + c * cell, y0 + r * cell
                wall = MAZE[r][c] == "#"
                fill = "#33302a" if wall else ("#1a2e0a" if (r, c) in on else "#141414")
                stroke = "#4a453a" if wall else (color if (r, c) in on else "#2a2a2a")
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-3}" height="{cell-3}" rx="4" fill="{fill}" stroke="{stroke}"/>')
                label = ""
                lc = "#7a7060"
                if wall:
                    label = "#"
                elif (r, c) == (0, 0):
                    label, lc = "S", BLUE
                elif (r, c) == (7, 7):
                    label, lc = "G", BLUE
                else:
                    for k, pos in ITEMS.items():
                        if pos == (r, c):
                            label, lc = k, AMBER
                if label:
                    s.append(f'        <text x="{x+(cell-3)/2}" y="{y+(cell-3)/2+5}" text-anchor="middle" fill="{lc}" font-size="13" font-weight="700">{label}</text>')
        pts = " ".join(f"{gx+c*cell+(cell-3)/2},{y0+r*cell+(cell-3)/2}" for r, c in path)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" '
                 f'stroke-linejoin="round" stroke-dasharray="1600" stroke-dashoffset="1600">'
                 f'<animate attributeName="stroke-dashoffset" values="1600;0;0" keyTimes="0;0.75;1" dur="12s" repeatCount="indefinite"/></polyline>')
        s.append(f'        <text x="{x0+155}" y="{y0+8*cell+20}" text-anchor="middle" fill="{GRAY}" font-size="11">'
                 f'拾う順番: S → {" → ".join(order)} → G</text>')
    s.append(f'        <text x="350" y="388" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '貪欲法はスタートのすぐ近くにあるCを後回しにして、大きく遠回りしている</text>')
    return fig(700, 404, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: ナップサックのDP表
# ────────────────────────────────────────────────────────────
def fig_knapsack():
    quests = [("村人を助ける", 6, 10), ("宝箱をあける", 5, 8),
              ("鉱石を掘る", 5, 8), ("釣りをする", 9, 12)]
    limit = 10
    n = len(quests)
    best = [[0] * (limit + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        name, m, sc = quests[i - 1]
        for t in range(limit + 1):
            best[i][t] = best[i - 1][t]
            if t >= m and best[i - 1][t - m] + sc > best[i][t]:
                best[i][t] = best[i - 1][t - m] + sc
    cw = 46
    x0, y0 = 148, 96
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'ナップサック問題の表: 使える時間ごとに最高得点を記録する</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'たて = 上から何個目まで使ってよいか　／　よこ = 使える時間（分）</text>']
    for t in range(0, limit + 1, 2):
        s.append(f'        <text x="{x0+t*cw/2+((cw-4)/2)}" y="{y0-10}" text-anchor="middle" fill="{GRAY}" font-size="11">{t}</text>')
    labels = ["何も使わない"] + [q[0] for q in quests]
    for i in range(n + 1):
        y = y0 + i * 40
        a = (1 - 0.16) * i / (n + 1)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{a:.3f};{min(a+0.03,0.999):.3f};1" '
                f'dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        note = "" if i == 0 else f"（{quests[i-1][1]}分 {quests[i-1][2]}点）"
        s.append(f'          <text x="136" y="{y+22}" text-anchor="end" fill="#ccc" font-size="11">{labels[i]}</text>')
        s.append(f'          <text x="136" y="{y+36}" text-anchor="end" fill="#666" font-size="9">{note}</text>')
        for k, t in enumerate(range(0, limit + 1, 2)):
            v = best[i][t]
            hot = i > 0 and v != best[i - 1][t]
            x = x0 + k * cw
            s.append(f'          <rect x="{x}" y="{y}" width="{cw-4}" height="30" rx="5" '
                     f'fill="{"#1a2e0a" if hot else "#141414"}" stroke="{GREEN if hot else "#2a2a2a"}"/>')
            s.append(f'          <text x="{x+(cw-4)/2}" y="{y+20}" text-anchor="middle" '
                     f'fill="{"#93D500" if hot else "#888"}" font-size="13" font-weight="{700 if hot else 400}">{v}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{y0+(n+1)*40+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '10分のマスの答えは16点。宝箱(5分8点)と鉱石(5分8点)を選んだときの得点</text>')
    return fig(700, y0 + (n + 1) * 40 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "ゲームと最適化 #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題1の候補の減り方"),
    ("#sec-examples", "tag-example", "観察記録", "例題3の差"),
    ("#sec-standard", "tag-standard", "標準課題1", "アイテムを動かすと？"),
    ("#sec-standard", "tag-standard", "標準課題2", "使える時間を変えると？"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第12回では、前期に作った数当てゲームと、迷路を使ったパズルを、
      後期に学んだ考え方で<strong>作り直します</strong>。
      同じゲームでも、「どのアルゴリズムで動かすか」を変えると、遊びごたえが大きく変わります。
    </p>

    <div class="analogy">
      ゲームの「敵の動き」や「ヒントの出し方」は、すべてアルゴリズムで決まっています。
      敵がプレイヤーへまっすぐ向かってくるなら貪欲法、
      壁を回りこんで最短で追ってくるなら幅優先探索やダイクストラ法が使われています。
      アルゴリズムを変えると、敵の「賢さ」が変わるということです。
    </div>

    <div class="concept-box">
      <h4>数当てゲームを最適化の目で見直す</h4>
      <p style="font-size:0.95rem">
        前期の数当てゲームでは「まん中を聞く」作戦を使いました。
        なぜまん中がよいのかを、後期の言葉で説明できます。
        <strong>1回の質問で、残る候補をいちばん多く減らせる選び方</strong>だからです。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        「その時点でいちばん得な選択をする」という点で、まん中を聞く作戦は<strong>貪欲法</strong>です。
        ただし第9回の貪欲法と違い、数当てゲームでは<strong>貪欲な選び方がそのまま最適</strong>になります。
        貪欲法がいつも損をするわけではない、という良い例です。
      </p>
    </div>

{fig_narrowing()}

    <div class="concept-box">
      <h4>アイテム集めパズルは巡回セールスマン問題</h4>
      <p style="font-size:0.95rem">
        迷路の中にアイテムがいくつか置いてあり、全部拾ってゴールへ向かうパズルを考えます。
        アイテムを拾う<strong>順番</strong>を決める問題なので、形は巡回セールスマン問題と同じです。
        違うのは、2地点のあいだの距離が「直線距離」ではなく<strong>迷路の中の最短歩数</strong>である点だけです。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        そこで2段階で解きます。
      </p>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li><strong>幅優先探索</strong>で、スタート・各アイテム・ゴールのあいだの歩数を全部求めて表にする</li>
        <li>できた表に対して、<strong>貪欲法</strong>や<strong>全探索</strong>を使って回る順番を決める</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        前期に学んだ幅優先探索と、後期に学んだ巡回セールスマン問題の解き方を、
        <strong>組み合わせて使う</strong>ということです。
      </p>
    </div>

{fig_items()}

    <div class="concept-box">
      <h4>ナップサック問題</h4>
      <p style="font-size:0.95rem">
        限られた時間や重さの中で、得点がいちばん高くなる組み合わせを選ぶ問題を
        <strong>ナップサック問題</strong>と呼びます。
        遠足のリュックに何を詰めるか、制限時間内にどのイベントをこなすか、といった場面にあたります。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        巡回セールスマン問題が「<strong>順番</strong>を決める問題」だったのに対し、
        ナップサック問題は「<strong>選ぶか選ばないか</strong>を決める問題」です。
        第10回で学んだ動的計画法が、そのまま使えます。
      </p>
    </div>

{fig_knapsack()}"""

ex1_body = f"""      <p>前期の数当てゲームを、「1回の質問で候補がどれだけ減るか」という目で見直します。
      1から100までのすべての数について、2つの作戦の質問回数を数えます。</p>

{code('AL2-12-ex1.py')}

{run('a12_ex1_result.png', '1から順に聞く作戦は、最悪で<strong>100回</strong>、平均で<strong>50.50回</strong>かかります。'
     'まん中を聞く作戦は、最悪でも<strong>7回</strong>、平均<strong>5.80回</strong>で終わります。'
     '下の表を見ると、1から順に聞く作戦は候補が 100個 → 99個 → 98個 と1個ずつしか減らないのに対し、'
     'まん中を聞く作戦は 100個 → 50個 → 24個 → 12個 と半分ずつ減っています。'
     '「1回の質問でいちばん多く候補を減らす」という貪欲な選び方が、そのままいちばん良い作戦になっています。')}

{notion('例題1の実行結果から、2つの作戦の「最悪の回数」と「平均の回数」を書く。'
        'あわせて、下の表を見て、7回目の時点で残っている候補の数がそれぞれいくつかを書く。')}"""

ex2_body = f"""      <p>迷路の中に置かれた4つのアイテムを、全部拾ってゴールへ向かうパズルを貪欲法で解きます。
      まず幅優先探索で地点どうしの歩数を表にしてから、いちばん近いアイテムへ向かうことをくり返します。</p>

{code('AL2-12-ex2.py')}

{run('a12_ex2_result.png', '6つの地点（S・A・B・C・D・G）のあいだの歩数が表になりました。'
     '表を見ると、SからAは2歩、SからCも2歩で、どちらもスタートのすぐ近くにあります。'
     '貪欲法は最初にAを選び、A → D → B → C と進んで、合計<strong>38歩</strong>になりました。'
     '最後に選んだCまでが14歩と、とても遠い移動になっています。'
     '第9回の「遠方のD宅」と同じ失敗のしかたです。')}"""

ex3_body = f"""      <p>同じパズルを全探索で解いて、貪欲法の答えと比べます。
      アイテムは4つなので、拾う順番は 4×3×2×1 = 24通りです。</p>

{code('AL2-12-ex3.py')}

{run('a12_ex3_result.png', '全探索が見つけた最短は「S → C → A → D → B → G」の<strong>22歩</strong>でした。'
     '貪欲法の38歩と比べて16歩も短く、貪欲法は最短より<strong>73%も長い</strong>という結果です。'
     '最短ルートは、スタートのすぐ近くにあるCを<strong>最初に</strong>拾っています。'
     '貪欲法はAとCがどちらも2歩なのでAを選びましたが、'
     'Cを先に拾っておけば、あとで14歩も戻る必要がなくなります。'
     '「その場でいちばん近い」を選ぶだけでは足りない、という良い例です。')}

{notion('例題3の実行結果から、貪欲法の答えと全探索の答え、その差を書く。'
        'あわせて、24通りの中でいちばん長かったルートとその歩数を書き、'
        '貪欲法がCを後回しにしてしまった理由を説明する。')}"""

ex4_body = f"""      <p>限られた時間の中で、得点がいちばん高くなる組み合わせを選ぶナップサック問題を、
      貪欲法と動的計画法の両方で解いて比べます。</p>

{code('AL2-12-ex4.py')}

{run('a12_ex4_result.png', '貪欲法は「1分あたりの得点」がいちばん高い「村人を助ける」（6分10点）を選び、'
     '残り4分では何もできず、合計<strong>10点</strong>で終わりました。'
     '動的計画法は「宝箱をあける」（5分8点）と「鉱石を掘る」（5分8点）を選び、'
     '10分をぴったり使い切って<strong>16点</strong>を取っています。'
     '差は6点で、貪欲法は最適解の6割ほどしか取れていません。'
     '表の右下（4個目・10分）が16になっており、そこから逆にたどると何を選んだかが分かります。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('12', ['AL2-12-ex1.py', 'AL2-12-ex2.py', 'AL2-12-ex3.py', 'AL2-12-ex4.py'])}

{keywords([
    ('ナップサック問題', 'knapsack problem', '決められた容量や時間の中で、価値の合計がいちばん高くなる組み合わせを選ぶ問題。'),
    ('組み合わせ最適化', 'くみあわせさいてきか', '「順番を決める」「選ぶか選ばないかを決める」など、有限の候補からいちばん良いものを選ぶ問題のまとめ。'),
    ('前処理', 'まえしょり / preprocessing', '本題を解く前に、必要な情報を計算して表にしておくこと。例題2では幅優先探索で歩数の表を作ることが前処理にあたる。'),
    ('復元', 'ふくげん / traceback', '動的計画法の表から「どれを選んだか」を逆にたどって調べること。'),
])}

{example(1, '数当てゲームを最適化の目で見直す', ex1_body)}

{example(2, 'アイテム集めパズルを貪欲法で解く', ex2_body)}

{example(3, '同じパズルを全探索で解く', ex3_body)}

{example(4, 'ナップサック問題を動的計画法で解く', ex4_body)}"""

std1_body = """      <p>例題2と例題3のファイルを開き、アイテム <strong>B</strong> の位置を変えます。
      いまの位置は迷路の右上のすみ (1, 7) ですが、ゴールのすぐ近くの (6, 7) に移します。</p>

<pre><span class="code-label">Python ── AL2-12-ex2.py と AL2-12-ex3.py の両方で書き換える行</span>
    <span class="str">"B"</span>: (<span class="num">6</span>, <span class="num">7</span>),   <span class="cmt"># ← (1, 7) を (6, 7) に変える</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、貪欲法と全探索それぞれの合計歩数がどうなるかを予測してNotionに書く</li>
          <li>2つのファイルの <code>items</code> を書き換えて保存し、両方を実行する</li>
          <li>歩数の表・貪欲法の答え・全探索の答えを記録する</li>
          <li>貪欲法が拾う順番が、書き換える前とどう変わったかを書く</li>
        </ol>
      </div>

      <table>
        <tr><th>方法</th><th>Bが(1,7)のとき</th><th>予測</th><th>実際</th></tr>
        <tr><td>貪欲法</td><td>38歩（S→A→D→B→C→G）</td><td></td><td></td></tr>
        <tr><td>全探索</td><td>22歩（S→C→A→D→B→G）</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> Bをゴールの近くに移したことで、
      貪欲法と最短ルートの差はどうなりましたか。差が変わった理由を説明してください。</p>
"""

std2_body = """      <p>例題4のファイル <code>AL2-12-ex4.py</code> を開き、使える時間 <code>limit</code> を変えて実行します。
      <strong>11分</strong>と<strong>16分</strong>の2通りを試してください。</p>

<pre><span class="code-label">Python ── 書き換える行</span>
limit = <span class="num">11</span>          <span class="cmt"># ← 10 を 11 に。次は 16 にする</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、11分と16分それぞれで貪欲法と動的計画法が何点になるかを予測してNotionに書く</li>
          <li><code>limit</code> を 11 に書き換えて実行し、結果を記録する</li>
          <li><code>limit</code> を 16 に書き換えて実行し、結果を記録する</li>
          <li>予測と実際を比べる</li>
        </ol>
      </div>

      <table>
        <tr><th>使える時間</th><th>貪欲法の予測</th><th>貪欲法の実際</th><th>DPの予測</th><th>DPの実際</th></tr>
        <tr><td>10分</td><td>—</td><td>10点</td><td>—</td><td>16点</td></tr>
        <tr><td>11分</td><td></td><td></td><td></td><td></td></tr>
        <tr><td>16分</td><td></td><td></td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 使える時間を増やすと、
      貪欲法と動的計画法の差はどうなりましたか。
      差が小さくなる時間と大きくなる時間があるとしたら、それはなぜかを説明してください。</p>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    どちらも<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, 'アイテムの位置を変えると答えはどう変わるか', std1_body)}
{notion('2つの方法についての予測と実際の表、拾う順番の変化、および差が変わった理由の説明。')}

{standard(2, '使える時間を変えると得点はどう変わるか', std2_body)}
{notion('11分と16分それぞれの予測と実際の表、および「差が小さくなる／大きくなる時間」の考察。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第12回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題1</strong>: 2つの作戦の最悪・平均の回数、7回目の残り候補</li>
        <li><strong>例題3</strong>: 貪欲法と全探索の答えと差、いちばん長いルート、Cを後回しにした理由</li>
        <li><strong>標準課題1</strong>: 予測と実際の表、拾う順番の変化、差が変わった理由</li>
        <li><strong>標準課題2</strong>: 11分・16分の予測と実際、差についての考察</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
      <div class="note-warn" style="margin-top:1rem">
        <strong>次回の予告:</strong> 第13回からは、自分でテーマを決めた作品づくりに入ります。
        第12回であつかった「アイテム集めパズル」や「ナップサック問題」は、そのまま作品の土台に使えます。
        どんな作品を作りたいか、次回までに考えておいてください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: アイテムBをゴールの近くに移したときの結果", """        <table>
          <tr><th>方法</th><th>Bが(1,7)のとき</th><th>Bが(6,7)のとき</th></tr>
          <tr><td>貪欲法</td><td>38歩（S→A→D→B→C→G）</td><td><strong style="color:#76B900">24歩（S→A→D→C→B→G）</strong></td></tr>
          <tr><td>全探索</td><td>22歩（S→C→A→D→B→G）</td><td><strong style="color:#76B900">18歩（S→C→A→D→B→G）</strong></td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>差は16歩から6歩へ、大きく縮まります。</strong>
        貪欲法は38歩から24歩へ14歩も短くなり、全探索も22歩から18歩へ4歩短くなりました。</p>
        <p style="margin-top:0.6rem"><strong>理由:</strong>
        書き換える前のBは迷路の右上のすみにあり、ゴールからも遠い場所でした。
        貪欲法がBを3番目に拾ったあと、まだ拾っていないCまで14歩も戻る必要がありました。
        Bをゴールの近く (6, 7) に移すと、Bとゴールが1歩の距離になります。
        貪欲法がBを最後に拾えば、そのままゴールへ入れるので、長い戻りが起きません。</p>
        <p style="margin-top:0.6rem">全探索の拾う順番は「S → C → A → D → B → G」のままで変わりません。
        もともとBを<strong>最後に</strong>拾ってゴールへ向かう形だったので、
        Bがゴールに近づいたぶんだけ、そのまま4歩短くなっています。</p>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        貪欲法が損をするのは「遠い場所を最後に残してしまうとき」です。
        遠い場所がゴールの近くにあると、最後に拾うことがそのまま得になるため、
        貪欲法の弱点が出にくくなります。
        アイテムの<strong>置き方しだいで、貪欲法で足りるかどうかが変わる</strong>ということです。</p>
"""),
    ("標準課題2: 使える時間を変えたときの得点", """        <table>
          <tr><th>使える時間</th><th>貪欲法</th><th>動的計画法</th><th>差</th></tr>
          <tr><td>10分</td><td>10点（村人）</td><td>16点（宝箱＋鉱石）</td><td><strong style="color:#FF5252">6点</strong></td></tr>
          <tr><td>11分</td><td>18点（村人＋宝箱）</td><td>18点（村人＋宝箱）</td><td><strong style="color:#76B900">0点</strong></td></tr>
          <tr><td>16分</td><td>26点（村人＋宝箱＋鉱石）</td><td>26点（村人＋宝箱＋鉱石）</td><td><strong style="color:#76B900">0点</strong></td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>11分のとき:</strong>
        貪欲法は村人（6分）を選んだあと、残り5分に宝箱（5分）がぴったり入ります。
        合計 10 + 8 = 18点で、動的計画法と同じになります。</p>
        <p style="margin-top:0.6rem"><strong>16分のとき:</strong>
        村人（6分）＋宝箱（5分）＋鉱石（5分）＝16分がぴったり収まり、合計26点です。
        貪欲法も動的計画法も同じ選び方になります。</p>
        <p style="margin-top:0.8rem"><strong>差が小さくなる時間・大きくなる時間:</strong></p>
        <ul class="point-list">
          <li><strong>差が0になるのは</strong>、貪欲法が選んだあとの<strong>残り時間にちょうど収まるもの</strong>がある場合です。時間があまらないので、むだが出ません。</li>
          <li><strong>差が大きくなるのは</strong>、貪欲法が選んだせいで<strong>中途半端な残り時間</strong>ができ、そこに何も入らない場合です。10分のときが、まさにその状態でした。村人（6分）を選んだせいで残り4分となり、5分のものが2つとも入りませんでした。</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        貪欲法は「1分あたりの得点」という<strong>1つの数字だけ</strong>を見て決めます。
        「あとで何が入るか」を考えないので、時間があまるかどうかを気にできません。
        動的計画法は、すべての時間について「そのとき最高何点取れるか」を表に記録するので、
        あまりが出ない組み合わせを見つけられます。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "ゲームと最適化", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("12", NAV, body)
