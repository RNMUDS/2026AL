# -*- coding: utf-8 -*-
"""第2回: 幅優先探索・深さ優先探索の発展 の本文を組み立てる。"""
from collections import deque
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, blank_answers, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, write)

MAZE = ["S.....#", ".####.#", ".#....#", ".#.##..", ".#..#.#", ".##.#.#", "......G"]


def find(maze, ch):
    for r, line in enumerate(maze):
        c = line.find(ch)
        if c >= 0:
            return (r, c)


def search(maze, mode, log=None):
    """調べた順番と経路を返す。mode は "bfs" か "dfs"。
    log にリストを渡すと、手順ごとの（読んだマス, そのあとのメモ）を書き足す。"""
    rows, cols = len(maze), len(maze[0])
    start, goal = find(maze, "S"), find(maze, "G")
    memo = deque([start])
    came = {start: None}
    order = []
    while memo:
        cur = memo.popleft() if mode == "bfs" else memo.pop()
        order.append(cur)
        if cur == goal:
            break
        r, c = cur
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if maze[nr][nc] == "#" or (nr, nc) in came:
                continue
            came[(nr, nc)] = cur
            memo.append((nr, nc))
        if log is not None:
            log.append((cur, list(memo)))
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = came[node]
    return order, list(reversed(path))


# ────────────────────────────────────────────────────────────
# 図1: メモの読み方の違い（キューとスタック）
# ────────────────────────────────────────────────────────────
def fig_queue_vs_stack():
    items = ["ア", "イ", "ウ", "エ", "オ"]
    n = len(items)
    dur = 10
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '2つの探索の違いは「メモのどこを読むか」だけ</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'メモに書き足す場所は同じ。読んで消す場所だけが違う</text>']
    panels = [
        ("幅優先探索（キュー）", "いちばん古い行を読む　popleft()", 30, lambda i: (i + 1) / (n + 1), GREEN),
        ("深さ優先探索（スタック）", "いちばん新しい行を読む　pop()", 380, lambda i: (n - i) / (n + 1), AMBER),
    ]
    for title, note, x0, gone_at, color in panels:
        s.append(f'        <text x="{x0+145}" y="82" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        s.append(f'        <text x="{x0+145}" y="102" text-anchor="middle" fill="{GRAY}" font-size="11">{note}</text>')
        s.append(f'        <text x="{x0}" y="140" fill="#666" font-size="10">古い</text>')
        s.append(f'        <text x="{x0+290}" y="140" text-anchor="end" fill="#666" font-size="10">新しい</text>')
        for i, label in enumerate(items):
            x = x0 + 6 + i * 56
            t = gone_at(i)
            s.append(f'        <g>')
            s.append(f'          <rect x="{x}" y="148" width="48" height="42" rx="8" fill="#1A1A1A" stroke="#444">'
                     f'<animate attributeName="opacity" values="1;1;0.12;0.12" '
                     f'keyTimes="0;{t:.3f};{min(t+0.02,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
            s.append(f'          <text x="{x+24}" y="175" text-anchor="middle" fill="#E0E0E0" font-size="15">{label}'
                     f'<animate attributeName="opacity" values="1;1;0.12;0.12" '
                     f'keyTimes="0;{t:.3f};{min(t+0.02,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/></text>')
            s.append(f'          <text x="{x+24}" y="128" text-anchor="middle" fill="{color}" font-size="13" font-weight="700" opacity="0">'
                     f'読む▼<animate attributeName="opacity" values="0;0;1;1;0;0" '
                     f'keyTimes="0;{max(t-0.08,0):.3f};{max(t-0.07,0.001):.3f};{t:.3f};{min(t+0.01,0.999):.3f};1" '
                     f'dur="{dur}s" repeatCount="indefinite"/></text>')
            s.append('        </g>')
        order = "ア → イ → ウ → エ → オ" if color == GREEN else "オ → エ → ウ → イ → ア"
        s.append(f'        <text x="{x0+145}" y="222" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">読む順番: {order}</text>')
    s.append('        <line x1="355" y1="70" x2="355" y2="232" stroke="#333" stroke-width="1"/>')
    return fig(700, 245, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図: メモの変化を1手順ずつ追う（例題の迷路の手順1〜4）
# ────────────────────────────────────────────────────────────
def fig_memo_steps(steps=4):
    """手順ごとに、迷路の図（読んだマス・メモにあるマス）とメモの中身を並べる。"""
    cell = 16
    bw, bh = 44, 20
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'メモの変化を1手順ずつ追う（例題の迷路の手順1〜4）</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '迷路の上の数字が列、左の数字が行。(行,列) でマスの場所を表す（どちらも 0 から数える）</text>']
    # 凡例
    legend = [("#8a6a2a", "#8a6a2a", "壁"), ("#E0E0E0", "#E0E0E0", "いま読んだマス"), ("#3a3a3a", "#999", "前に読んだマス"),
              ("#141414", GREEN, "メモ（幅優先）"), ("#141414", AMBER, "メモ（深さ優先）")]
    for i, (fillc, strokec, label) in enumerate(legend):
        x = 30 + i * 132
        s.append(f'        <rect x="{x}" y="60" width="13" height="13" rx="2" fill="{fillc}" stroke="{strokec}" stroke-width="2"/>')
        s.append(f'        <text x="{x+19}" y="71" fill="#ccc" font-size="11">{label}</text>')
    s.append(f'        <text x="350" y="92" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '「次」の文字が付いたマスが、次の手順で読まれる行（メモの箱の太枠と同じマス）</text>')

    top = 112
    block_h = 7 * cell + 34
    for col, (mode, title, color) in enumerate([("bfs", "幅優先探索（キュー）: 左端を読む", GREEN),
                                                ("dfs", "深さ優先探索（スタック）: 右端を読む", AMBER)]):
        x0 = 20 + col * 345
        log = []
        search(MAZE, mode, log)
        s.append(f'        <text x="{x0+160}" y="{top}" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        read_before = set()
        for k in range(steps):
            cur, memo = log[k]
            nxt = memo[0] if mode == "bfs" else memo[-1]
            y0 = top + 30 + k * block_h
            mx, my = x0 + 36, y0 + 12
            s.append(f'        <text x="{x0}" y="{y0+4}" fill="#E0E0E0" font-size="12" font-weight="700">手順{k+1}</text>')
            # 列・行の番号
            for c in range(7):
                s.append(f'        <text x="{mx+c*cell+cell/2}" y="{my-3}" text-anchor="middle" fill="#666" font-size="8">{c}</text>')
            for r in range(7):
                s.append(f'        <text x="{mx-5}" y="{my+r*cell+11}" text-anchor="end" fill="#666" font-size="8">{r}</text>')
            for r in range(7):
                for c in range(7):
                    x, y = mx + c * cell, my + r * cell
                    ch = MAZE[r][c]
                    if ch == "#":
                        fillc, strokec, sw = "#8a6a2a", "#8a6a2a", 1
                    elif (r, c) == cur:
                        fillc, strokec, sw = "#E0E0E0", "#E0E0E0", 1
                    elif (r, c) in memo:
                        fillc, strokec, sw = "#141414", color, 2
                    elif (r, c) in read_before:
                        fillc, strokec, sw = "#3a3a3a", "#999", 1
                    else:
                        fillc, strokec, sw = "#141414", "#333", 1
                    s.append(f'        <rect x="{x+1}" y="{y+1}" width="{cell-2}" height="{cell-2}" rx="2" '
                             f'fill="{fillc}" stroke="{strokec}" stroke-width="{sw}"/>')
                    if ch in "SG":
                        tc = "#111" if (r, c) == cur else AMBER
                        s.append(f'        <text x="{x+cell/2}" y="{y+12}" text-anchor="middle" fill="{tc}" font-size="9" font-weight="700">{ch}</text>')
                    elif (r, c) == nxt:
                        s.append(f'        <text x="{x+cell/2}" y="{y+12}" text-anchor="middle" fill="{color}" font-size="8" font-weight="700">次</text>')
            # 右側: 読んだマスとメモ
            tx = mx + 7 * cell + 14
            s.append(f'        <text x="{tx}" y="{my+14}" fill="#ccc" font-size="11">読んだマス ({cur[0]},{cur[1]})</text>')
            s.append(f'        <text x="{tx}" y="{my+38}" fill="{GRAY}" font-size="10">そのあとのメモ（左が古い）</text>')
            for i, (r, c) in enumerate(memo):
                on = (r, c) == nxt
                x = tx + i * (bw + 4)
                s.append(f'        <rect x="{x}" y="{my+46}" width="{bw}" height="{bh}" rx="5" fill="#1A1A1A" '
                         f'stroke="{color if on else "#444"}" stroke-width="{2 if on else 1}"/>')
                s.append(f'        <text x="{x+bw/2}" y="{my+60}" text-anchor="middle" fill="{color if on else "#E0E0E0"}" '
                         f'font-size="10">({r},{c})</text>')
            s.append(f'        <text x="{tx}" y="{my+84}" fill="{color}" font-size="10">次に読む: ({nxt[0]},{nxt[1]})</text>')
            read_before.add(cur)
    y = top + 30 + steps * block_h + 6
    s.append(f'        <line x1="350" y1="{top-14}" x2="350" y2="{y-20}" stroke="#333" stroke-width="1"/>')
    s.append(f'        <text x="350" y="{y}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '幅優先探索はスタートのまわりを少しずつ広げ、深さ優先探索は (1,0) を残したまま右へ進み続ける</text>')
    return fig(700, y + 16, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 同じ迷路を調べる順番の比較
# ────────────────────────────────────────────────────────────
def fig_visit_order():
    cell = 22
    dur = 16
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '同じ迷路を調べる順番の比較（数字は何番目に調べたか）</text>']
    for panel, (mode, title, x0, color) in enumerate(
            [("bfs", "幅優先探索", 46, GREEN), ("dfs", "深さ優先探索", 396, AMBER)]):
        order, path = search(MAZE, mode)
        pos = {cell_pos: i + 1 for i, cell_pos in enumerate(order)}
        s.append(f'        <text x="{x0+77}" y="52" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 62
        for r in range(7):
            for c in range(7):
                x, y = x0 + c * cell, y0 + r * cell
                ch = MAZE[r][c]
                if ch == "#":
                    s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="3" fill="#33302a" stroke="#4a453a"/>')
                    s.append(f'        <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+4}" text-anchor="middle" fill="#7a7060" font-size="11" font-weight="700">#</text>')
                    continue
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="3" fill="#141414" stroke="#333"/>')
                k = pos.get((r, c))
                if k is None:
                    continue
                a = (1 - 0.15) * (k - 1) / len(order)
                s.append(f'        <g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
                         f'keyTimes="0;{a:.3f};{min(a+0.015,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
                s.append(f'          <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="3" fill="#1a2e0a" stroke="{color}" stroke-width="1.2"/>')
                s.append(f'          <text x="{x+(cell-2)/2}" y="{y+(cell-2)/2+4}" text-anchor="middle" fill="{color}" font-size="10">{k}</text>')
                s.append('        </g>')
        note = f"{len(order)}マス調べてゴール到着 ／ 経路は{len(path)-1}歩"
        s.append(f'        <text x="{x0+77}" y="{y0+7*cell+22}" text-anchor="middle" fill="#ccc" font-size="11">{note}</text>')
    s.append('        <line x1="350" y1="40" x2="350" y2="240" stroke="#333" stroke-width="1"/>')
    s.append(f'        <text x="350" y="266" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '幅優先探索は近い順にじわじわ広がる。深さ優先探索は一方向へどんどん進む</text>')
    return fig(700, 280, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 歩数と調べたマス数のトレードオフ
# ────────────────────────────────────────────────────────────
def fig_tradeoff():
    data = [("経路の歩数（小さいほど良い）", 12, 18, 14),
            ("調べたマス数（小さいほど手間が軽い）", 31, 19, 14)]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '一長一短: 幅優先探索は道が短く、深さ優先探索は手間が軽い</text>']
    for i, (title, bfs_v, dfs_v, scale) in enumerate(data):
        y = 58 + i * 108
        s.append(f'        <text x="30" y="{y}" fill="#E0E0E0" font-size="12" font-weight="700">{title}</text>')
        for j, (name, v, color) in enumerate([("幅優先探索", bfs_v, GREEN), ("深さ優先探索", dfs_v, AMBER)]):
            yy = y + 16 + j * 34
            s.append(f'        <text x="30" y="{yy+18}" fill="{GRAY}" font-size="11">{name}</text>')
            s.append(f'        <rect x="140" y="{yy+2}" width="{v*scale}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
            s.append(f'        <text x="{140+v*scale+10}" y="{yy+19}" fill="{color}" font-size="12" font-weight="700">{v}</text>')
    s.append(f'        <text x="350" y="{58+2*108+6}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '最短の道がほしいなら幅優先探索。ゴールへ行けるかだけ知りたいなら深さ優先探索でも足りる</text>')
    return fig(700, 58 + 2 * 108 + 24, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 壁のない広場での経路の違い
# ────────────────────────────────────────────────────────────
def fig_open_field():
    def field(mode, size=10):
        start, goal = (0, 0), (size - 1, size - 1)
        memo = deque([start])
        came = {start: None}
        while memo:
            cur = memo.popleft() if mode == "bfs" else memo.pop()
            if cur == goal:
                break
            r, c = cur
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if not (0 <= nr < size and 0 <= nc < size) or (nr, nc) in came:
                    continue
                came[(nr, nc)] = cur
                memo.append((nr, nc))
        p, node = [], goal
        while node is not None:
            p.append(node)
            node = came[node]
        return list(reversed(p))

    cell = 24
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '壁のない10マス×10マスの広場を、左上から右下まで進んだ道</text>']
    for mode, title, x0, color in [("bfs", "幅優先探索: 18歩", 60, GREEN), ("dfs", "深さ優先探索: 54歩", 400, AMBER)]:
        p = field(mode)
        mark = {cellpos: i for i, cellpos in enumerate(p)}
        s.append(f'        <text x="{x0+120}" y="52" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        y0 = 62
        for r in range(10):
            for c in range(10):
                x, y = x0 + c * cell, y0 + r * cell
                on = (r, c) in mark
                fillc = "#1a2e0a" if on else "#141414"
                strokec = color if on else "#2e2e2e"
                s.append(f'        <rect x="{x}" y="{y}" width="{cell-2}" height="{cell-2}" rx="3" fill="{fillc}" stroke="{strokec}"/>')
        s.append(f'        <text x="{x0+11}" y="{y0+15}" text-anchor="middle" fill="{AMBER}" font-size="11" font-weight="700">S</text>')
        s.append(f'        <text x="{x0+9*cell+11}" y="{y0+9*cell+15}" text-anchor="middle" fill="{AMBER}" font-size="11" font-weight="700">G</text>')
        # 道順をなぞる線
        pts = " ".join(f"{x0+c*cell+(cell-2)/2},{y0+r*cell+(cell-2)/2}" for r, c in p)
        s.append(f'        <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" '
                 f'stroke-linejoin="round" stroke-dasharray="1600" stroke-dashoffset="1600">'
                 f'<animate attributeName="stroke-dashoffset" values="1600;0;0" keyTimes="0;0.75;1" dur="10s" repeatCount="indefinite"/></polyline>')
    s.append(f'        <text x="350" y="{62+10*cell+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '深さ優先探索は行き止まりに当たるまで進み続けるため、広場では大きく蛇行する</text>')
    return fig(700, 62 + 10 * cell + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "2つの探索 #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("02")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      前期の最後に学んだ幅優先探索に加えて、第2回では<strong>深さ優先探索</strong>をあつかいます。
      2つの探索は、コードの見た目こそよく似ていますが、見つける道がまったく違います。
      違いは<strong>たった1行</strong>、「メモのどこを読むか」だけです。
    </p>

    <div class="concept-box">
      <h4>2つの探索の呼び名（略したアルファベット）</h4>
      <table>
        <tr><th>日本語</th><th>略した呼び名</th><th>英語（元の言葉）</th><th>言葉の意味</th></tr>
        <tr><td><strong style="color:#76B900">幅優先探索</strong></td><td><strong style="color:#76B900">BFS</strong>（ビー・エフ・エス）</td>
            <td><strong>B</strong>readth-<strong>F</strong>irst <strong>S</strong>earch</td><td>breadth = 幅、first = 優先（先に）、search = 探索</td></tr>
        <tr><td><strong style="color:#FFB800">深さ優先探索</strong></td><td><strong style="color:#FFB800">DFS</strong>（ディー・エフ・エス）</td>
            <td><strong>D</strong>epth-<strong>F</strong>irst <strong>S</strong>earch</td><td>depth = 深さ、first = 優先（先に）、search = 探索</td></tr>
      </table>
      <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">
        本やWebの説明では略した呼び名がよく使われます。例題のコードでも、<code>search("bfs")</code> は幅優先探索、<code>search("dfs")</code> は深さ優先探索を表します。</p>
    </div>

    <div class="analogy">
      迷路で分かれ道に来ると、進める方向が2つ以上見えることがあります。
      体は1つなので、同時に両方へは進めません。そこで「あとで見に行く場所」をメモに書いておきます。
      メモの<strong>上から順に</strong>読めば幅優先探索、<strong>いちばん最後に書いた行から</strong>読めば深さ優先探索になります。
      人が迷路を歩くときは、たいてい深さ優先探索と同じで「行けるところまで進んで、行き止まりなら引き返す」やり方をしています。
    </div>

{fig_queue_vs_stack()}

    <div class="concept-box">
      <h4>キューとスタック</h4>
      <p style="font-size:0.95rem">
        <strong style="color:#76B900">キュー</strong>（queue）は「先に入れたものを先に取り出す入れもの」です。
        レジの行列と同じで、先に並んだ人から順に呼ばれます。Pythonでは <code>deque</code> の <code>popleft()</code> で先頭を取り出します。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        <strong style="color:#FFB800">スタック</strong>（stack）は「あとから入れたものを先に取り出す入れもの」です。
        積み重ねた本と同じで、いちばん上に置いた本から取ります。Pythonでは <code>pop()</code> で末尾を取り出します。
      </p>
    </div>

    <p style="margin:1.5rem 0 0.5rem">
      では、実際の迷路でメモがどう変わるかを見てみます。下の図は、例題の迷路で2つの探索を動かしたときの<strong>最初の4手順</strong>です。
      マスの場所は <strong>(行,列)</strong> で表します。行は上から、列は左から数え、どちらも <strong>0 から</strong>数えます（スタートの左上が (0,0)）。
      どちらの探索も、手順1ではスタート (0,0) を読み、となりの (1,0)（下）と (0,1)（右）をメモに書き足します。
      ちがいが出るのは手順2からです。
    </p>

{fig_memo_steps()}

    <div class="analogy">
      幅優先探索は、メモの<strong>左端（いちばん古い行）</strong>を読むので、下の (1,0) と右の (0,1) を交互に読み、スタートのまわりを少しずつ広げていきます。
      深さ優先探索は、メモの<strong>右端（いちばん新しい行）</strong>を読むので、いま書き足したばかりの右のマスへ進み続けます。
      下の (1,0) はメモの左端に書かれたまま、行き止まりに当たるまで読まれません。
      この1行のちがいが、調べる順番と、見つかる道のちがいになります。
    </div>

    <div class="concept-box">
      <h4>幅優先探索が最短を保証する理由</h4>
      <p style="font-size:0.95rem">
        幅優先探索はメモを古い順に読むため、<strong>1歩で行ける場所をすべて調べ終えるまで、2歩の場所には進みません</strong>。
        同じように、2歩の場所をすべて調べ終えてから3歩へ進みます。
        歩数が少ない場所から順に調べているので、ゴールに最初に届いたときの歩数が、必ずいちばん少ない歩数になります。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        深さ優先探索は歩数の順に調べません。行き止まりに当たるまで一方向へ進み続けるため、
        遠回りの道を先に見つけてしまうことがあります。<strong>深さ優先探索が見つけた道は、最短とはかぎりません</strong>。
      </p>
    </div>"""

ex1_body = f"""      <p>前期に幅優先探索で解いたのと同じ形の迷路を、深さ優先探索で解きます。
      幅優先探索のコードと見比べると、変わっているのは<strong>メモから取り出す行</strong>だけです。</p>

      <table>
        <tr><th>探索方法</th><th>メモの入れもの</th><th>取り出す命令</th><th>取り出す場所</th></tr>
        <tr><td>幅優先探索</td><td><code>deque</code>（キュー）</td><td><code>popleft()</code></td><td>いちばん古い行</td></tr>
        <tr><td>深さ優先探索</td><td><code>list</code>（スタック）</td><td><code>pop()</code></td><td>いちばん新しい行</td></tr>
      </table>

{example_pair('AL2-02-ex1.py', '深さ優先探索が見つけた道は<strong>18歩</strong>でした。'
     '同じ迷路で幅優先探索が見つける道は12歩なので、6歩も長い道になっています。'
     '窓の図を見ると、上の行を右へ進んでから下りてくる大回りの道になっています。'
     '一方で調べたマスの数は<strong>19マス</strong>だけでした。')}"""

ex2_body = f"""      <p>幅優先探索と深さ優先探索を1つのプログラムにまとめ、同じ迷路で走らせて比べます。
      <code>search</code> 関数の中で <code>mode</code> が <code>"bfs"</code> か <code>"dfs"</code> かによって、取り出す行だけを切り替えています。
      実行すると、ターミナルに2つ、窓に1つ表示されます。</p>


      <table>
        <tr><th>表示されるもの</th><th>読み方</th></tr>
        <tr><td>（ターミナル）歩数と調べたマス数の表</td><td>歩数 = ゴールまでの道のマス数 − 1。調べたマス数 = メモから読んだマスの数</td></tr>
        <tr><td>（ターミナル）メモの変化（手順1〜5）</td><td>「読んだマス」と、そのあとのメモの中身。左が古い行、右が新しい行</td></tr>
        <tr><td>（窓）調べた順番のアニメーション</td><td>色の付いたマスの数字 = 何番目に調べたか。灰色のブロックは壁、色の付いていないマスは調べなかったマス、
        枠だけのマスはメモにあるマス、「次」の字は次に読むマス。最後まで進むと、通り道が白い線で示される</td></tr>
      </table>

{example_pair('AL2-02-ex2.py', '幅優先探索は<strong>12歩・31マス調査</strong>、深さ優先探索は<strong>18歩・19マス調査</strong>という結果でした。'
     '「調べた順番」を見ると、幅優先探索の番号はスタートから近い順に 1, 2, 3, … と少しずつ広がり、'
     '深さ優先探索の番号は 1 → 2 → … → 6 と上の行を一直線に右へ進んでいます。'
     '幅優先探索は短い道を見つけるかわりに、たくさんのマスを調べています。'
     '深さ優先探索は調べるマスが少ないかわりに、遠回りの道を答えとして返しています。'
     'どちらが優れているかではなく、<strong>何がほしいかで選ぶ</strong>という点が大切です。', fig_visit_order())}

{notion('例題2（実践）の実行結果で、「メモの変化」の手順2〜3を見比べ、幅優先探索と深さ優先探索が<strong>それぞれどのマスを読んだか</strong>を確かめる。'
        '読んだマスがメモの左端か右端かを、自分の目で確認しておく（標準課題の「キュー」と「スタック」の図と同じ動きになっている）。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1と例題2のコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('02', ['AL2-02-ex1.py', 'AL2-02-ex2.py'])}

    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>迷路を絵で表示する道具（pygame）を入れる</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題は、探索のようすを<strong>窓（ウィンドウ）の中のアニメーション</strong>で見せます。
      マスが1つずつ色づき、何番目に調べたかの数字が入っていき、最後にゴールまでの通り道が白い線で示されます。
      そのために <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）を使います。</p>
      <div class="setup-step">
        <p class="step-title">1. VS Code のターミナルで pygame を入れる（1回だけ・Windows）</p>
        <ol>
          <li><strong>VS Code を開く</strong>（上の「準備」で開いた AL2/No02 フォルダのままでよい）</li>
          <li>画面いちばん上のメニューから <strong>「ターミナル」→「新しいターミナル」</strong>を選ぶ
              （キーボードなら <strong>Ctrl + @</strong> でも開く）</li>
          <li>画面の下に黒い（または白い）枠が開き、<code>PS C:&#92;Users&#92;あなたの名前&#92;Desktop&#92;AL2&#92;No02&gt;</code> のような行が出る。
              これが<strong>ターミナル</strong>（文字で命令を打ちこむ場所）</li>
          <li>その行の最後をクリックして、次の1行を<strong>そのまま打ちこむ</strong>（コピーして右クリックで貼り付けてもよい）</li>
        </ol>
{plain("py -m pip install pygame", "ターミナル（Windows）")}
        <ol start="5">
          <li><strong>Enter</strong> を押す。英語の文字が何行か流れ、数十秒〜数分かかる</li>
          <li>最後のほうに <code>Successfully installed pygame-2.6.1</code>（数字はちがってよい）と出れば成功</li>
          <li>入ったかを確かめる。次の1行を打ちこんで Enter を押し、<code>2.6.1</code> のような数字が出ればよい</li>
        </ol>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <div class="note-warn" style="margin-top:0.8rem">
          <strong>うまくいかないとき</strong>
          <table style="margin-top:0.4rem">
            <tr><th>出たメッセージ</th><th>やること</th></tr>
            <tr><td><code>'py' は、内部コマンドまたは外部コマンド…として認識されていません</code><br>
                    または <code>py : 用語 'py' は…認識されません</code></td>
                <td>最初の <code>py</code> を <code>python</code> に変えて、<code>python -m pip install pygame</code> を実行する</td></tr>
            <tr><td><code>Requirement already satisfied</code></td>
                <td>すでに入っている。何もしなくてよい</td></tr>
            <tr><td>赤い文字のエラーで止まる（<code>error: subprocess-exited-with-error</code> など）</td>
                <td><code>py -m pip install pygame-ce</code> を実行する（pygame の別版。使い方は同じ）</td></tr>
            <tr><td>例題を ▷ で実行すると <code>ModuleNotFoundError: No module named 'pygame'</code></td>
                <td>▷ が使う Python と、pygame を入れた Python がちがう。ターミナルで
                    <code>python -m pip install pygame</code> も実行してから、もう一度 ▷ を押す</td></tr>
          </table>
        </div>
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>py</code> のかわりに <code>python3</code> と打つ（<code>python3 -m pip install pygame</code>）。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各例題ファイルの<strong>いちばん下</strong>
        （「ここから下は、迷路を pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動くので、ほかのファイルを用意する必要はありません。
        ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。</p>
      </div>
    </div>

    <div class="note-warn">
      <strong>穴埋めの注意:</strong> まちがった候補を入れると、プログラムが<strong>止まらなくなる</strong>ことがあります
      （ターミナルに何も出ないまま動き続ける）。そのときはターミナルをクリックして <strong>Ctrl+C</strong> を押して止め、穴を見直してください。
      たとえば、メモを読むだけで消さない書き方（<code>memo[-1]</code> や <code>stack[0]</code> など）にすると、同じ行を何度も読み続けて先へ進みません。
    </div>

{keywords([
    ('幅優先探索（BFS）', 'はばゆうせんたんさく / BFS', 'BFS は Breadth-First Search の略。スタートから近いマスから順に、同じ歩数のマスをすべて調べてから次の歩数へ進む探し方。見つかる道は必ず最短の歩数になる。'),
    ('深さ優先探索（DFS）', 'ふかさゆうせんたんさく / DFS', 'DFS は Depth-First Search の略。行き止まりに当たるまで一方向へ進み、行き止まりなら、まだ調べていない道が残っているいちばん最近の分かれ道まで戻って別の道を試す探し方。見つかる道は最短とはかぎらない。'),
    ('スタック', 'stack', 'あとから入れたものを先に取り出す入れもの。積み重ねた本と同じ。Pythonのリストでは <code>append()</code> で入れて <code>pop()</code> で取り出す。'),
    ('キュー', 'queue', '先に入れたものを先に取り出す入れもの。レジの行列と同じ。Pythonでは <code>deque</code> の <code>append()</code> と <code>popleft()</code> を使う。'),
    ('到達可能性', 'とうたつかのうせい / reachability', '「ゴールへ行けるかどうか」だけを判定すること。最短の道は要らないので、深さ優先探索でも十分な場合が多い。'),
    ('トレードオフ', 'trade-off', '一方を良くすると他方が悪くなる関係。幅優先探索と深さ優先探索は「道の短さ」と「調べる手間」がトレードオフの関係にある。'),
])}

{example(1, '深さ優先探索で迷路を解く', ex1_body)}

{example(2, '2つの探索を同じ迷路で比べる', ex2_body)}"""

ans = answers([slide_example("02"), blank_answers("02"),
    ("理解度チェックの答えの例", """        <p><strong>問い</strong>: 3つ読んで消したあとに、新しいものを1つ書き足した。次に読まれるのはどれか（キュー・スタックそれぞれ）。</p>
        <p style="margin-top:0.6rem"><strong>答えの例</strong>（書き足した順番: りんご → みかん → ぶどう → もも → なし、あとから「いちご」を書き足した場合）</p>
        <table>
          <tr><th></th><th>3つ読んだあとのメモ</th><th>いちごを書き足したメモ</th><th>次に読まれるもの</th><th>理由</th></tr>
          <tr><td><strong style="color:#76B900">キュー</strong></td><td>もも、なし</td><td>もも、なし、いちご</td>
              <td><strong>もも</strong></td><td>いちばん古い行（左端）から読むので、残っていたうちで先に書いた「もも」</td></tr>
          <tr><td><strong style="color:#FFB800">スタック</strong></td><td>りんご、みかん</td><td>りんご、みかん、いちご</td>
              <td><strong>いちご</strong></td><td>いちばん新しい行（右端）から読むので、いま書き足した「いちご」</td></tr>
        </table>
        <p style="margin-top:0.6rem">迷路でいえば、スタック（深さ優先探索）は<strong>いま見つけたばかりのマス</strong>をすぐ読むので一方向へ進み続け、
        キュー（幅優先探索）は<strong>前から待っているマス</strong>を先に読むので、スタートに近いマスから順に広がる。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "2つの探索の違い", explanation),
    section("sec-examples", "2", "例題", examples),
    slides_for("02", SLIDES),
    advanced_section("02"),
    rubric_section("02"),
    ans,
])

write("02", NAV, body)
