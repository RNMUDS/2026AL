# -*- coding: utf-8 -*-
"""第12回: 数当てゲーム・パズルの再応用 の本文を組み立てる。"""
import math
from collections import deque
from slides_data import SLIDES
from common import (slide_submission, slides_for, rubric_section,
                    AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)

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
    "課題 #sec-slides nav-assignment",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("12")

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

ans = answers([
    ("確かめ用の数値", """        <p><strong>問い2（使える時間を変えたとき）</strong></p>
        <table>
          <tr><th>使える時間</th><th>貪欲法</th><th>動的計画法</th><th>差</th></tr>
          <tr><td>10分</td><td>10点（村人）</td><td>16点（宝箱＋鉱石）</td><td><strong style="color:#FF5252">6点</strong></td></tr>
          <tr><td>11分</td><td>18点（村人＋宝箱）</td><td>18点（村人＋宝箱）</td><td><strong style="color:#76B900">0点</strong></td></tr>
          <tr><td>16分</td><td>26点</td><td>26点</td><td>0点</td></tr>
        </table>
        <p style="margin-top:0.6rem">11分だと、村人（6分）を選んだあとの残り5分に宝箱（5分）が
        <strong>ちょうど収まる</strong>ため、貪欲法でもむだが出ません。</p>
        <p style="margin-top:0.8rem"><strong>問い1の要点</strong>: 10分のときは村人（6分）を選んだせいで
        残りが4分になり、5分のものが2つとも入らなくなります。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "ゲームと最適化", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("12", SLIDES),
    rubric_section("12"),
    ans,
])

write("12", NAV, body)
