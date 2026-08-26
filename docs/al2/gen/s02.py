# -*- coding: utf-8 -*-
"""第2回: 幅優先探索・深さ優先探索の発展 の本文を組み立てる。"""
from collections import deque
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

MAZE = ["S.....#", ".####.#", ".#....#", ".#.##..", ".#..#.#", ".##.#.#", "......G"]


def find(maze, ch):
    for r, line in enumerate(maze):
        c = line.find(ch)
        if c >= 0:
            return (r, c)


def search(maze, mode):
    """調べた順番と経路を返す。mode は "bfs" か "dfs"。"""
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
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2の歩数と調査数"),
    ("#sec-examples", "tag-example", "観察記録", "例題4の広場での差"),
    ("#sec-standard", "tag-standard", "標準課題1", "壁を1つ足すと？"),
    ("#sec-standard", "tag-standard", "標準課題2", "使い分けの表"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      前期の最後に学んだ幅優先探索に加えて、第2回では<strong>深さ優先探索</strong>をあつかいます。
      2つの探索は、コードの見た目こそよく似ていますが、見つける道がまったく違います。
      違いは<strong>たった1行</strong>、「メモのどこを読むか」だけです。
    </p>

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

ex1_body = f"""      <p>第1回の例題3で使った迷路を、深さ優先探索で解きます。
      幅優先探索のコードと見比べると、変わっているのは<strong>メモから取り出す行</strong>だけです。</p>

      <table>
        <tr><th>探索方法</th><th>メモの入れもの</th><th>取り出す命令</th><th>取り出す場所</th></tr>
        <tr><td>幅優先探索</td><td><code>deque</code>（キュー）</td><td><code>queue.popleft()</code></td><td>いちばん古い行</td></tr>
        <tr><td>深さ優先探索</td><td><code>list</code>（スタック）</td><td><code>stack.pop()</code></td><td>いちばん新しい行</td></tr>
      </table>

{code('AL2-02-ex1.py')}

{run('a02_ex1_result.png', '深さ優先探索が見つけた道は<strong>18歩</strong>でした。'
     '第1回の例題3で幅優先探索が見つけた道は12歩だったので、6歩も長い道になっています。'
     '迷路の絵を見ると、上の行を右へ進んでから下りてくる大回りの道になっています。'
     '一方で調べたマスの数は<strong>19マス</strong>だけでした。')}"""

ex2_body = f"""      <p>幅優先探索と深さ優先探索を1つのプログラムにまとめ、同じ迷路で走らせて比べます。
      <code>search</code> 関数の中で <code>mode</code> が <code>"bfs"</code> か <code>"dfs"</code> かによって、取り出す行だけを切り替えています。</p>

{code('AL2-02-ex2.py')}

{fig_visit_order()}

{run('a02_ex2_result.png', '幅優先探索は<strong>12歩・31マス調査</strong>、深さ優先探索は<strong>18歩・19マス調査</strong>という結果でした。'
     '幅優先探索は短い道を見つけるかわりに、たくさんのマスを調べています。'
     '深さ優先探索は調べるマスが少ないかわりに、遠回りの道を答えとして返しています。'
     'どちらが優れているかではなく、<strong>何がほしいかで選ぶ</strong>という点が大切です。')}

{notion('例題2の実行結果から、幅優先探索と深さ優先探索の「歩数」と「調べたマス数」を表にまとめる。'
        'あわせて、2つの迷路の絵を見比べて、経路がどう違うかを言葉で説明する。')}"""

ex3_body = f"""      <p>迷路を15マス×15マスに大きくし、壁（障害物）を増やして同じ比較をします。
      迷路が大きくなると、2つの探索の差はどう変わるかを観察してください。</p>

{code('AL2-02-ex3.py')}

{fig_tradeoff()}

{run('a02_ex3_result.png', '幅優先探索は<strong>48歩・127マス調査</strong>、深さ優先探索は<strong>64歩・76マス調査</strong>でした。'
     '通れるマスは全部で128マスなので、幅優先探索はほぼ全部のマスを調べています。'
     '迷路が大きくなっても、「幅優先探索は道が短いが手間が重い」「深さ優先探索は手間が軽いが道が長い」という関係は変わりません。')}"""

ex4_body = f"""      <p>壁がまったくない広場で、2つの探索がどんな道を選ぶかを見ます。
      広場は10マス×10マス、20マス×20マス、40マス×40マスの3種類を試します。</p>

{code('AL2-02-ex4.py')}

{fig_open_field()}

{run('a02_ex4_result.png', '40マス×40マスの広場では、幅優先探索が<strong>78歩</strong>なのに対し、深さ優先探索は<strong>780歩</strong>でした。10倍の差です。'
     '一方で調べたマスの数は、幅優先探索が1600マス（広場のすべて）、深さ優先探索は859マスと約半分です。'
     '10マス×10マスの経路の絵を見ると、深さ優先探索が行をまたいで蛇のように往復していることが分かります。')}

{notion('例題4の表から、40マス×40マスのときの「歩数の差」と「調べたマス数の差」を書く。'
        'あわせて、深さ優先探索の経路が蛇のようになる理由を、メモの読み方（pop）と結びつけて説明する。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    第1回と同じように、まず作業フォルダを用意します。</p>

{setup_guide('02', ['AL2-02-ex1.py', 'AL2-02-ex2.py', 'AL2-02-ex3.py', 'AL2-02-ex4.py'])}

{keywords([
    ('深さ優先探索', 'ふかさゆうせんたんさく / DFS', '行き止まりに当たるまで一方向へ進み、行き止まりなら1つ戻って別の道を試す探し方。見つかる道は最短とはかぎらない。'),
    ('スタック', 'stack', 'あとから入れたものを先に取り出す入れもの。積み重ねた本と同じ。Pythonのリストでは <code>append()</code> で入れて <code>pop()</code> で取り出す。'),
    ('キュー', 'queue', '先に入れたものを先に取り出す入れもの。レジの行列と同じ。Pythonでは <code>deque</code> の <code>append()</code> と <code>popleft()</code> を使う。'),
    ('到達可能性', 'とうたつかのうせい / reachability', '「ゴールへ行けるかどうか」だけを判定すること。最短の道は要らないので、深さ優先探索でも十分な場合が多い。'),
    ('トレードオフ', 'trade-off', '一方を良くすると他方が悪くなる関係。幅優先探索と深さ優先探索は「道の短さ」と「調べる手間」がトレードオフの関係にある。'),
])}

{example(1, '深さ優先探索で迷路を解く', ex1_body)}

{example(2, '2つの探索を同じ迷路で比べる', ex2_body)}

{example(3, '障害物を増やした大きい迷路で比べる', ex3_body)}

{example(4, '壁のない広場で比べる', ex4_body)}"""

std1_body = """      <p>例題2のファイル <code>AL2-02-ex2.py</code> を開き、迷路のいちばん下の行を書き換えます。</p>

<pre><span class="code-label">Python ── 書き換える行</span>
    <span class="str">"......G"</span>,      <span class="cmt"># ← "..#...G" に書き換える（下の通路に壁を1つ置く）</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、幅優先探索の歩数がどうなるかを予測してNotionに書く（増える／変わらない／減る のどれか、と理由）</li>
          <li>迷路を書き換えて保存し、実行する</li>
          <li>幅優先探索と深さ優先探索の歩数・調べたマス数を記録する</li>
          <li>迷路の絵をよく見て、経路がどう変わったかを書く</li>
        </ol>
      </div>

      <table>
        <tr><th>項目</th><th>書き換える前</th><th>書き換えたあと</th></tr>
        <tr><td>幅優先探索の歩数</td><td>12歩</td><td></td></tr>
        <tr><td>幅優先探索の調べたマス数</td><td>31マス</td><td></td></tr>
        <tr><td>深さ優先探索の歩数</td><td>18歩</td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 予測は当たりましたか。
      当たっても外れても、実行結果の迷路の絵を見て、通り道がどう変わったかを言葉で説明してください。</p>
"""

std2_body = """      <p>例題2・例題3・例題4の結果をもとに、2つの探索の使い分けを表にまとめます。
      表はNotionに作り、空欄をすべて埋めてください。</p>

      <table>
        <tr><th>比べる点</th><th>幅優先探索</th><th>深さ優先探索</th></tr>
        <tr><td>メモから取り出す場所</td><td></td><td></td></tr>
        <tr><td>見つかる道は最短か</td><td></td><td></td></tr>
        <tr><td>調べるマスの数（多い／少ない）</td><td></td><td></td></tr>
        <tr><td>広場（例題4・40マス四方）での歩数</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem">表を作ったうえで、次の2つの場面には、それぞれどちらの探索が向いているかを<strong>理由つきで</strong>答えてください。</p>
      <ul class="point-list">
        <li><strong>場面A:</strong> 配達アプリで「いちばん早く着く道順」を案内する</li>
        <li><strong>場面B:</strong> 迷路ゲームで「そもそもゴールにたどり着けるか」だけを判定する</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    標準課題1は<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, '壁を1つ足すと歩数はどうなるか', std1_body)}
{notion('予測（増える／変わらない／減る と理由）、書き換えたあとの歩数と調べたマス数の表、経路がどう変わったかの説明。')}

{standard(2, '幅優先探索と深さ優先探索の使い分け', std2_body)}
{notion('4行の比較表（空欄をすべて埋める）と、場面A・場面Bそれぞれに向いている探索とその理由。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第2回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 歩数と調べたマス数の表、経路の違いの説明</li>
        <li><strong>例題4</strong>: 40マス四方での差、蛇行する理由</li>
        <li><strong>標準課題1</strong>: 予測、書き換えたあとの結果、経路の変化</li>
        <li><strong>標準課題2</strong>: 比較表、場面A・場面Bへの答えと理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: 壁を1つ足したときの結果", """        <table>
          <tr><th>項目</th><th>書き換える前</th><th>書き換えたあと</th></tr>
          <tr><td>幅優先探索の歩数</td><td>12歩</td><td><strong style="color:#76B900">12歩（変わらない）</strong></td></tr>
          <tr><td>幅優先探索の調べたマス数</td><td>31マス</td><td>26マス</td></tr>
          <tr><td>深さ優先探索の歩数</td><td>18歩</td><td>18歩</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>歩数は変わりませんが、通り道はまったく別の道に変わります。</strong>
        書き換える前は左の列を下りて下の行を右へ進む道でしたが、書き換えたあとは上の行を右へ進んでから右側の列を下りる道になります。</p>
<pre><span class="code-label">Terminal ── 書き換えたあとの幅優先探索の経路</span>
  S*****#
  .####*#
  .#...*#
  .#.##*.
  .#..#*#
  .##.#*#
  ..#..*G</pre>
        <p style="margin-top:0.8rem"><strong>歩数が変わらない理由:</strong>
        スタートは左上のマス、ゴールは右下のマスです。たてに6マス、よこに6マス離れているので、
        まっすぐ進めるならどう回っても12歩かかります。書き換える前の道も書き換えたあとの道も、
        「もどる動き」をまったく含まない道なので、どちらも12歩で済みます。
        壁を1つ置いても、もう1本の12歩の道が残っていたということです。</p>
        <p style="margin-top:0.6rem">調べたマス数が31マスから26マスに減ったのは、壁が1つ増えたことで、そもそも通れるマスが1つ減り、
        その先にあった行き止まりのマスも調べなくてよくなったためです。</p>"""),
    ("標準課題2: 使い分けの表と答え", """        <table>
          <tr><th>比べる点</th><th>幅優先探索</th><th>深さ優先探索</th></tr>
          <tr><td>メモから取り出す場所</td><td>いちばん古い行（<code>popleft()</code>）</td><td>いちばん新しい行（<code>pop()</code>）</td></tr>
          <tr><td>見つかる道は最短か</td><td>必ず最短</td><td>最短とはかぎらない</td></tr>
          <tr><td>調べるマスの数</td><td>多い（近い順にすべて調べる）</td><td>少ないことが多い</td></tr>
          <tr><td>広場（40マス四方）での歩数</td><td>78歩</td><td>780歩</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>場面A（配達アプリの経路案内）: 幅優先探索</strong><br>
        利用者がほしいのは「いちばん早く着く道順」です。深さ優先探索が返す道は最短とはかぎらず、
        例題4では最短の10倍もの遠回りになりました。遠回りの道を案内してしまうと役に立ちません。
        最短が必要な場面では、調べる手間が重くなっても幅優先探索を選びます。</p>
        <p style="margin-top:0.6rem"><strong>場面B（ゴールにたどり着けるかの判定）: 深さ優先探索</strong><br>
        知りたいのは「行けるか、行けないか」だけで、道の長さは関係ありません。
        どちらの探索でも同じ答えが出るので、調べるマスが少なくて済む深さ優先探索のほうが軽く終わります。
        例題4の40マス四方では、調べたマスが1600マスから859マスへ、およそ半分に減りました。</p>
        <p style="margin-top:0.6rem"><strong>補足:</strong>
        深さ優先探索にはもう1つ利点があります。メモに残る場所の数が少なくて済むため、
        非常に大きい迷路でもコンピュータのメモリを使いすぎません。
        幅優先探索は「同じ歩数のマス全部」をメモに持つので、迷路が広いほどメモが長くなります。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "2つの探索の違い", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("02", NAV, body)
