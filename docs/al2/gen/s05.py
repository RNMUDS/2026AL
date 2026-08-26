# -*- coding: utf-8 -*-
"""第5回: ダイクストラ法（1）考え方 の本文を組み立てる。"""
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)

RAIL = {
    "新宿": [("渋谷", 7), ("池袋", 9), ("品川", 30)],
    "渋谷": [("新宿", 7), ("品川", 9)],
    "池袋": [("新宿", 9), ("上野", 12)],
    "上野": [("池袋", 12), ("東京", 6)],
    "東京": [("上野", 6), ("品川", 11)],
    "品川": [("新宿", 30), ("渋谷", 9), ("東京", 11)],
}
STATIONS = list(RAIL)
POS = {"新宿": (170, 96), "渋谷": (170, 246), "品川": (390, 246),
       "池袋": (390, 66), "上野": (560, 66), "東京": (560, 196)}
EDGES = [("新宿", "渋谷", 7), ("新宿", "池袋", 9), ("新宿", "品川", 30),
         ("渋谷", "品川", 9), ("池袋", "上野", 12), ("上野", "東京", 6),
         ("東京", "品川", 11)]
INF = float("inf")


def trace(start="新宿"):
    """各手順の (選んだ駅, 距離表のコピー, 書き直した駅の集合) を返す。"""
    dist = {s: INF for s in STATIONS}
    dist[start] = 0
    settled = set()
    steps = [(None, dict(dist), set(), set())]
    while len(settled) < len(STATIONS):
        cur = None
        for s in STATIONS:
            if s in settled or dist[s] == INF:
                continue
            if cur is None or dist[s] < dist[cur]:
                cur = s
        if cur is None:
            break
        settled.add(cur)
        changed = set()
        for name, w in RAIL[cur]:
            if name in settled:
                continue
            if dist[cur] + w < dist[name]:
                dist[name] = dist[cur] + w
                changed.add(name)
        steps.append((cur, dict(dist), set(settled), changed))
    return steps


def draw_graph(highlight=None, hcolor=GREEN):
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
    for a, b, w in EDGES:
        (x1, y1), (x2, y2) = POS[a], POS[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        on = frozenset((a, b)) in hedges
        out.append(f'        <rect x="{mx-17}" y="{my-11}" width="34" height="22" rx="6" fill="#0A0A0A" stroke="{hcolor if on else GRAY}"/>')
        out.append(f'        <text x="{mx}" y="{my+5}" text-anchor="middle" fill="{hcolor if on else "#bbb"}" font-size="11">{w}分</text>')
    for name, (x, y) in POS.items():
        on = highlight and name in highlight
        out.append(f'        <circle cx="{x}" cy="{y}" r="26" fill="{"#1a2e0a" if on else "#1A1A1A"}" stroke="{hcolor if on else "#555"}" stroke-width="2"/>')
        out.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: ダイクストラ法の3つの手順
# ────────────────────────────────────────────────────────────
def fig_three_steps():
    steps = [
        ("手順1", "まだ決まっていない駅のうち、\n今わかっている時間がいちばん\n小さい駅を1つ選ぶ", GREEN),
        ("手順2", "選んだ駅の時間を「もう変わらない」\nと決める（確定させる）", AMBER),
        ("手順3", "選んだ駅のとなりの駅について、\nより短い行き方が見つかれば\n時間を書き直す", GREEN),
    ]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'ダイクストラ法は3つの手順のくり返し</text>']
    for i, (title, body, color) in enumerate(steps):
        x = 24 + i * 224
        s.append(f'        <rect x="{x}" y="52" width="204" height="128" rx="12" fill="#141414" stroke="#444" stroke-width="1.5"/>')
        s.append(f'        <text x="{x+102}" y="78" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{title}</text>')
        for j, line in enumerate(body.split("\n")):
            s.append(f'        <text x="{x+102}" y="{104+j*20}" text-anchor="middle" fill="#ccc" font-size="11">{line}</text>')
        a, b = i / 3, (i + 1) / 3
        s.append(f'        <rect x="{x-3}" y="49" width="210" height="134" rx="14" fill="none" stroke="{color}" stroke-width="3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.01:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
        if i < 2:
            s.append(f'        <text x="{x+212}" y="120" text-anchor="middle" fill="#666" font-size="16">▶</text>')
    s.append(f'        <path d="M 630 190 L 630 208 L 126 208 L 126 190" fill="none" stroke="#555" stroke-width="2"/>')
    s.append(f'        <text x="378" y="226" text-anchor="middle" fill="{GRAY}" font-size="11">すべての駅が確定するまでくり返す</text>')
    return fig(700, 242, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 距離表が1ステップずつ決まっていく
# ────────────────────────────────────────────────────────────
def fig_table_animation():
    steps = trace()
    dur = 18
    colw = 90
    x0, y0 = 76, 76
    rowh = 30
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '新宿から各駅までの時間が、手順ごとに決まっていく</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '緑の枠 = その手順で確定した駅　／　オレンジの数字 = その手順で書き直された時間</text>']
    for j, st in enumerate(STATIONS):
        s.append(f'        <text x="{x0+j*colw+colw/2}" y="{y0-10}" text-anchor="middle" fill="{GRAY}" font-size="11">{st}</text>')
    n = len(steps)
    for i, (chosen, dist, settled, changed) in enumerate(steps):
        y = y0 + i * rowh
        a = (1 - 0.14) * i / n
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" '
                f'keyTimes="0;{a:.3f};{min(a+0.02,0.999):.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        label = f"手順{i}" if i else "はじめ"
        s.append(f'          <text x="16" y="{y+19}" fill="#bbb" font-size="11">{label}</text>')
        for j, st in enumerate(STATIONS):
            v = dist[st]
            text = "－" if v == INF else str(v)
            done = st in settled
            hit = st in changed
            fillc = "#1a2e0a" if done else "#141414"
            strokec = GREEN if done else "#2e2e2e"
            s.append(f'          <rect x="{x0+j*colw}" y="{y}" width="{colw-4}" height="{rowh-4}" rx="5" fill="{fillc}" stroke="{strokec}"/>')
            col = AMBER if hit else ("#93D500" if done else "#999")
            s.append(f'          <text x="{x0+j*colw+(colw-4)/2}" y="{y+18}" text-anchor="middle" fill="{col}" '
                     f'font-size="12" font-weight="{700 if (hit or done) else 400}">{text}</text>')
        if chosen:
            s.append(f'          <text x="{x0+6*colw+6}" y="{y+19}" fill="{GREEN}" font-size="10">{chosen} 確定</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{y0+n*rowh+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '品川は「30分」からいったん決まりかけたが、渋谷経由の16分に書き直された</text>')
    return fig(700, y0 + n * rowh + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: なぜ「いちばん小さい駅」を確定してよいのか
# ────────────────────────────────────────────────────────────
def fig_why_settle():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'なぜ「いちばん小さい駅」は、もう変わらないと決めてよいのか</text>',
         f'        <text x="350" y="48" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '品川16分と上野21分が未確定のとき、品川を確定させてよい理由</text>']
    s.append(f'        <circle cx="80" cy="140" r="30" fill="#1a2e0a" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'        <text x="80" y="145" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">新宿</text>')
    s.append(f'        <circle cx="380" cy="96" r="30" fill="#1A1A1A" stroke="{GREEN}" stroke-width="2"/>')
    s.append(f'        <text x="380" y="101" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">品川</text>')
    s.append(f'        <circle cx="380" cy="216" r="30" fill="#1A1A1A" stroke="{AMBER}" stroke-width="2"/>')
    s.append(f'        <text x="380" y="221" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">上野</text>')
    s.append(f'        <line x1="110" y1="130" x2="350" y2="100" stroke="{GREEN}" stroke-width="4"/>')
    s.append(f'        <text x="230" y="104" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">見つかっている行き方: 16分</text>')
    s.append(f'        <line x1="110" y1="152" x2="350" y2="210" stroke="{AMBER}" stroke-width="3"/>')
    s.append(f'        <text x="230" y="200" text-anchor="middle" fill="{AMBER}" font-size="12">見つかっている行き方: 21分</text>')
    s.append(f'        <path d="M 400 190 Q 470 150 400 122" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4"/>')
    s.append(f'        <text x="500" y="160" fill="{RED}" font-size="12">上野から品川へ回り道をしても</text>')
    s.append(f'        <text x="500" y="180" fill="{RED}" font-size="12">21分 ＋（0以上）＝ 21分以上</text>')
    s.append(f'        <rect x="60" y="256" width="580" height="56" rx="10" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="280" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             '重みが0以上なら、遠回りをして時間が減ることはない</text>')
    s.append(f'        <text x="350" y="300" text-anchor="middle" fill="#ccc" font-size="11">'
             'だから「今いちばん小さい16分」より短い行き方は、もう出てこない</text>')
    return fig(700, 326, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: マイナスの重みで壊れる
# ────────────────────────────────────────────────────────────
def fig_negative():
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{RED}" font-weight="700" font-size="15">'
         'マイナスの重みがあると、ダイクストラ法は間違える</text>']
    nodes = {"スタート": (110, 160), "A店": (560, 160), "B店": (335, 260)}
    for name, (x, y) in nodes.items():
        s.append(f'        <circle cx="{x}" cy="{y}" r="34" fill="#1A1A1A" stroke="#555" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
    s.append(f'        <line x1="144" y1="160" x2="526" y2="160" stroke="#666" stroke-width="2"/>')
    s.append(f'        <rect x="318" y="140" width="44" height="24" rx="6" fill="#0A0A0A" stroke="{GRAY}"/>')
    s.append(f'        <text x="340" y="157" text-anchor="middle" fill="#bbb" font-size="12">1円</text>')
    s.append(f'        <line x1="136" y1="180" x2="308" y2="248" stroke="#666" stroke-width="2"/>')
    s.append(f'        <rect x="196" y="200" width="44" height="24" rx="6" fill="#0A0A0A" stroke="{GRAY}"/>')
    s.append(f'        <text x="218" y="217" text-anchor="middle" fill="#bbb" font-size="12">2円</text>')
    s.append(f'        <line x1="366" y1="246" x2="534" y2="184" stroke="{RED}" stroke-width="3"/>')
    s.append(f'        <rect x="432" y="196" width="56" height="24" rx="6" fill="#0A0A0A" stroke="{RED}"/>')
    s.append(f'        <text x="460" y="213" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">-5円</text>')
    s.append(f'        <text x="460" y="240" text-anchor="middle" fill="{GRAY}" font-size="10">B店でもらえるクーポン</text>')

    phases = [
        (0.02, 0.30, GREEN, "① スタートを0円で確定", "A店は1円、B店は2円と分かった"),
        (0.32, 0.60, AMBER, "② いちばん小さいA店（1円）を確定", "「A店は1円で決まり」としてしまう"),
        (0.62, 0.98, RED, "③ B店（2円）を確定すると -3円 が見つかる", "しかしA店はもう確定済みなので、書き直されない"),
    ]
    for a, b, color, title, note in phases:
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <text x="350" y="60" text-anchor="middle" fill="{color}" font-size="14" font-weight="700">{title}</text>')
        s.append(f'          <text x="350" y="82" text-anchor="middle" fill="#ccc" font-size="11">{note}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="310" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             'ダイクストラ法の答え: A店は1円　／　本当の答え: A店は -3円</text>')
    return fig(700, 326, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "考え方 #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題1の書き直しの記録"),
    ("#sec-examples", "tag-example", "観察記録", "例題3の答えのちがい"),
    ("#sec-standard", "tag-standard", "標準課題1", "距離表を手で埋める"),
    ("#sec-standard", "tag-standard", "標準課題2", "重みを変えると？"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第4回で、重みの合計を最小にする経路は幅優先探索では求められないことを確かめました。
      重みの合計を最小にする経路を求めるアルゴリズムが<strong>ダイクストラ法</strong>です。
      1959年にエドガー・ダイクストラが考えた方法で、今のカーナビや乗換案内の中でも使われています。
    </p>

    <div class="analogy">
      出発点から各駅までの所要時間を、鉛筆で表に書いていく場面を思い浮かべてください。
      最初はどの駅も「わからない」ので空欄です。
      調べていくうちに「渋谷は7分で行ける」と分かれば書き込み、
      あとで「もっと早い行き方があった」と分かれば消して書き直します。
      書き直しがもう起こらないと確信できた駅から順に、ペンでなぞって確定させていく作業がダイクストラ法です。
    </div>

{fig_three_steps()}

    <div class="concept-box">
      <h4>ダイクストラ法で使う3つの入れもの</h4>
      <table>
        <tr><th>名前</th><th>中身</th><th>最初の状態</th></tr>
        <tr><td><code>distance</code></td><td>出発点からその駅までの、今わかっているいちばん短い時間</td><td>出発点だけ0、ほかはすべて <code>inf</code>（無限大）</td></tr>
        <tr><td><code>settled</code></td><td>「もう変わらない」と決まった駅を入れる集合</td><td>空</td></tr>
        <tr><td><code>came_from</code></td><td>その駅へ来るとき、直前にどの駅にいたか</td><td>すべて <code>None</code></td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        <code>inf</code> は Python で <code>float("inf")</code> と書く「無限大」の値です。
        どんな数と比べても必ず大きくなるので、「まだ行き方が1つも見つかっていない」ことを表すのに使えます。
      </p>
    </div>

{fig_table_animation()}

    <div class="concept-box">
      <h4>いちばん小さい駅を確定してよい理由</h4>
      <p style="font-size:0.95rem">
        手順2で「もう変わらない」と決めてしまってよいのは、<strong>重みがすべて0以上</strong>だからです。
        まだ確定していない駅のうち、時間がいちばん小さい駅を品川（16分）だとします。
        品川へ別の行き方でたどり着くには、必ず他の未確定の駅を通ります。
        他の未確定の駅は、どれも16分以上かかります。
        そこから品川へ進むと、重みが0以上なのでさらに時間が増えます。
        つまり<strong>16分より短くなることはありえません</strong>。
      </p>
    </div>

{fig_why_settle()}

    <div class="note-warn">
      <strong>成り立たなくなる場合:</strong> 重みにマイナスの値が混ざると、上の理由が使えなくなります。
      「遠回りをすると時間が減る」ことが起きてしまうためです。例題3で実際に確かめます。
    </div>"""

ex1_body = f"""      <p>ダイクストラ法を、手順が目に見える形で書いたプログラムです。
      1つの手順が終わるたびに、距離表の中身をそのまま表示します。
      表の中で <code>*</code> が付いている駅は「もう変わらない」と決まった駅です。</p>

{code('AL2-05-ex1.py')}

{run('a05_ex1_result.png', '手順1で新宿を確定させると、渋谷7分・池袋9分・品川30分が書き込まれます。'
     '手順2で渋谷を確定させたとき、<strong>品川の時間が30分から16分に書き直されて</strong>います。'
     '直通の30分より、渋谷で乗りかえる16分のほうが早いことが見つかったためです。'
     '手順3以降、品川の16分はもう書き直されず、手順4で確定しています。'
     '最終的に、新宿から東京までは27分と求まりました。')}

{notion('例題1の実行結果から、「時間を書き直した」と表示された行をすべて書き写す。'
        'あわせて、品川の時間が30分から16分に書き直された理由を、自分の言葉で説明する。')}"""

ex2_body = f"""      <p>ダイクストラ法は最短時間を求めますが、そのままでは「どの道を通ったか」が分かりません。
      距離を書き直すときに、<strong>どの駅から来たか</strong>も一緒に記録しておけば、あとで道順を組み立てられます。</p>

{code('AL2-05-ex2.py')}

{run('a05_ex2_result.png', '各駅への最短の行き方が、駅名を矢印でつないだ形で表示されました。'
     '東京へは「新宿 → 渋谷 → 品川 → 東京」で27分が最短です。'
     '<code>came_from</code> の中身を見ると、東京には「品川」、品川には「渋谷」、渋谷には「新宿」と書かれています。'
     '東京から逆にたどると 東京 → 品川 → 渋谷 → 新宿 となり、順番をひっくり返せば道順になります。'
     '第1回の幅優先探索で経路を復元したときと、まったく同じやり方です。')}"""

ex3_body = f"""      <p>ダイクストラ法が正しく動くのは「重みがすべて0以上」のときだけです。
      マイナスの重みが1本でも混ざると、答えを間違えます。
      3つのお店をめぐる例で確かめます。B店を通ると5円のクーポンがもらえるので、
      B店からA店へ向かう辺の重みは <code>-5</code> になっています。</p>

{code('AL2-05-ex3.py')}

{fig_negative()}

{run('a05_ex3_result.png', 'ダイクストラ法はA店を<strong>1円</strong>と答えましたが、'
     'すべての行き方を書き出すと「スタート → B店 → A店」で<strong>-3円</strong>で行けることが分かります。'
     'ダイクストラ法は、A店を1円で確定させたあとにB店を調べています。'
     'そのときA店へ -3円で行けることが見つかりますが、A店はすでに確定しているので<strong>無視されてしまいます</strong>。'
     '「遠回りをすると安くなる」ことが起きると、確定という考え方そのものが成り立たなくなります。')}

{notion('例題3の実行結果から、ダイクストラ法の答えと本当の答えを書く。'
        'あわせて、ダイクストラ法がA店の -3円 を採用できなかった理由を、実行結果の「無視された」という行を引用しながら説明する。')}"""

ex4_body = f"""      <p>出発点を6つの駅すべてに変えて距離表を作り、
      さらに全探索（すべての行き方を書き出す方法）の答えと一致するかを機械的に確かめます。</p>

{code('AL2-05-ex4.py')}

{run('a05_ex4_result.png', '6つの駅それぞれを出発点にした表ができました。'
     '表は左上から右下への線を軸にして<strong>対称</strong>になっています。'
     '行き帰りで同じ時間がかかる路線図なので、新宿から東京への27分と、東京から新宿への27分は同じ値になります。'
     'ダイクストラ法と全探索の答えは、すべての組み合わせで完全に一致しました。'
     '重みがすべて0以上であれば、ダイクストラ法は全探索と同じ正しい答えを、はるかに速く出せます。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。まず作業フォルダを用意します。</p>

{setup_guide('05', ['AL2-05-ex1.py', 'AL2-05-ex2.py', 'AL2-05-ex3.py', 'AL2-05-ex4.py'])}

{keywords([
    ('ダイクストラ法', 'Dijkstra法', '重みが0以上のグラフで、出発点から各頂点までの最小コストを求めるアルゴリズム。'),
    ('確定', 'かくてい / settled', 'その頂点までの最小コストが「もう変わらない」と決まった状態。確定した頂点は二度と書き直さない。'),
    ('緩和', 'かんわ / relaxation', '「別の道を通ったほうが短い」と分かったときに、記録してある値を小さく書き直す操作。'),
    ('inf', 'infinity / 無限大', 'Pythonで <code>float("inf")</code> と書く。どんな数より大きいので「まだ行き方が見つかっていない」印として使える。'),
    ('負の重み', 'ふのおもみ / negative weight', 'マイナスの重み。混ざるとダイクストラ法は正しく動かない。'),
])}

{example(1, '距離表が決まっていく様子を見る', ex1_body)}

{example(2, 'どの道を通ったかを記録する', ex2_body)}

{example(3, 'マイナスの重みがあると間違える', ex3_body)}

{example(4, '出発点を変える／全探索と答え合わせ', ex4_body)}"""

std1_body = """      <p>下の路線図について、<strong>プログラムを使わずに紙と鉛筆で</strong>ダイクストラ法を進め、距離表を完成させてください。
      出発点は <strong>渋谷</strong> です。</p>

      <div class="setup-step">
        <p class="step-title">路線図（第5回の例題と同じもの）</p>
        <ul>
          <li>新宿 ─ 渋谷: 7分</li>
          <li>新宿 ─ 池袋: 9分</li>
          <li>新宿 ─ 品川: 30分</li>
          <li>渋谷 ─ 品川: 9分</li>
          <li>池袋 ─ 上野: 12分</li>
          <li>上野 ─ 東京: 6分</li>
          <li>東京 ─ 品川: 11分</li>
        </ul>
      </div>

      <p>次の表をNotionに作り、手順ごとに埋めてください。まだ分かっていない駅は「－」と書きます。</p>

      <table>
        <tr><th>手順</th><th>選んだ駅</th><th>渋谷</th><th>新宿</th><th>品川</th><th>池袋</th><th>東京</th><th>上野</th></tr>
        <tr><td>はじめ</td><td>なし</td><td>0</td><td>－</td><td>－</td><td>－</td><td>－</td><td>－</td></tr>
        <tr><td>手順1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td>手順2</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td>手順3</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td>手順4</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td>手順5</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td>手順6</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      </table>

      <div class="setup-step">
        <p class="step-title">答え合わせ</p>
        <ol>
          <li>表を最後まで埋めてから、<code>AL2-05-ex1.py</code> の <code>start = "新宿"</code> を <code>start = "渋谷"</code> に書き換える</li>
          <li>保存して実行し、自分が手で作った表と見比べる</li>
          <li>ちがっていた場所があれば、どこで間違えたかを書く</li>
        </ol>
      </div>
"""

std2_body = """      <p>例題1のファイル <code>AL2-05-ex1.py</code> を開き、上野と東京のあいだの重みを 6分 から 40分 に変えます。
      工事のため、上野と東京のあいだが大きく遠回りになったという設定です。</p>

<pre><span class="code-label">Python ── 書き換える2か所</span>
    <span class="str">"上野"</span>: [(<span class="str">"池袋"</span>, <span class="num">12</span>), (<span class="str">"東京"</span>, <span class="num">40</span>)],   <span class="cmt"># ← 6 を 40 に</span>
    <span class="str">"東京"</span>: [(<span class="str">"上野"</span>, <span class="num">40</span>), (<span class="str">"品川"</span>, <span class="num">11</span>)],   <span class="cmt"># ← 6 を 40 に</span></pre>

      <div class="setup-step">
        <p class="step-title">やること</p>
        <ol>
          <li>実行する<strong>前に</strong>、新宿から各駅までの最短時間がどうなるかを予測してNotionに書く</li>
          <li>2か所を書き換えて保存し、実行する</li>
          <li>実際の結果を記録し、予測と比べる</li>
          <li><code>AL2-05-ex2.py</code> も同じように書き換えて実行し、東京への道順が変わったかを確かめる</li>
        </ol>
      </div>

      <table>
        <tr><th>駅</th><th>6分のとき</th><th>予測（40分のとき）</th><th>実際</th></tr>
        <tr><td>渋谷</td><td>7分</td><td></td><td></td></tr>
        <tr><td>池袋</td><td>9分</td><td></td><td></td></tr>
        <tr><td>品川</td><td>16分</td><td></td><td></td></tr>
        <tr><td>上野</td><td>21分</td><td></td><td></td></tr>
        <tr><td>東京</td><td>27分</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 上野と東京のあいだの重みを大きくしたのに、
      変わらなかった駅と変わった駅があります。どの駅が変わり、どの駅が変わらなかったかを書き、
      その理由を「最短経路がその辺を通っているかどうか」という観点から説明してください。</p>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    標準課題1は<strong>先に手で表を作ってから</strong>プログラムで答え合わせをします。</p>

{standard(1, '渋谷を出発点にして、距離表を手で埋める', std1_body)}
{notion('手で作った距離表（手順6まで）、プログラムの実行結果、ちがいがあった場合はどこで間違えたか。')}

{standard(2, '重みを変えると最短時間はどう変わるか', std2_body)}
{notion('5つの駅についての予測と実際の表、東京への道順の変化、および「変わった駅と変わらなかった駅」の理由。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第5回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題1</strong>: 「書き直した」行の書き写し、品川が16分に変わった理由</li>
        <li><strong>例題3</strong>: ダイクストラ法の答えと本当の答え、採用できなかった理由</li>
        <li><strong>標準課題1</strong>: 手で作った距離表、プログラムとの照合結果</li>
        <li><strong>標準課題2</strong>: 予測と実際の表、道順の変化、変わった駅と変わらない駅の理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: 渋谷を出発点にした距離表", """        <table>
          <tr><th>手順</th><th>選んだ駅</th><th>渋谷</th><th>新宿</th><th>品川</th><th>池袋</th><th>東京</th><th>上野</th></tr>
          <tr><td>はじめ</td><td>なし</td><td>0</td><td>－</td><td>－</td><td>－</td><td>－</td><td>－</td></tr>
          <tr><td>手順1</td><td>渋谷</td><td><strong>0</strong></td><td>7</td><td>9</td><td>－</td><td>－</td><td>－</td></tr>
          <tr><td>手順2</td><td>新宿</td><td><strong>0</strong></td><td><strong>7</strong></td><td>9</td><td>16</td><td>－</td><td>－</td></tr>
          <tr><td>手順3</td><td>品川</td><td><strong>0</strong></td><td><strong>7</strong></td><td><strong>9</strong></td><td>16</td><td>20</td><td>－</td></tr>
          <tr><td>手順4</td><td>池袋</td><td><strong>0</strong></td><td><strong>7</strong></td><td><strong>9</strong></td><td><strong>16</strong></td><td>20</td><td>28</td></tr>
          <tr><td>手順5</td><td>東京</td><td><strong>0</strong></td><td><strong>7</strong></td><td><strong>9</strong></td><td><strong>16</strong></td><td><strong>20</strong></td><td>26</td></tr>
          <tr><td>手順6</td><td>上野</td><td><strong>0</strong></td><td><strong>7</strong></td><td><strong>9</strong></td><td><strong>16</strong></td><td><strong>20</strong></td><td><strong>26</strong></td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>手順の中身:</strong></p>
        <ul class="point-list">
          <li>手順1: 渋谷を確定。となりの新宿を 0+7=7、品川を 0+9=9 と書き込む。</li>
          <li>手順2: 未確定でいちばん小さい新宿（7分）を確定。池袋を 7+9=16 と書き込む。品川へは 7+30=37 だが、すでに9分なので書き直さない。</li>
          <li>手順3: 品川（9分）を確定。東京を 9+11=20 と書き込む。</li>
          <li>手順4: 池袋（16分）を確定。上野を 16+12=28 と書き込む。</li>
          <li>手順5: 東京（20分）を確定。上野へ 20+6=26 のほうが短いので、28から<strong>26に書き直す</strong>。</li>
          <li>手順6: 上野（26分）を確定。すべての駅が確定して終了。</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>よくある間違い:</strong> 手順4で上野を28分と書いたあと、手順5で26分に書き直す部分を見落とすことが多いです。
        「一度書いた値は、確定するまで何度でも書き直される」という点に注意してください。</p>"""),
    ("標準課題2: 上野と東京のあいだを40分にしたときの結果", """        <table>
          <tr><th>駅</th><th>6分のとき</th><th>40分のとき</th><th>変わったか</th></tr>
          <tr><td>渋谷</td><td>7分</td><td>7分</td><td>変わらない</td></tr>
          <tr><td>池袋</td><td>9分</td><td>9分</td><td>変わらない</td></tr>
          <tr><td>品川</td><td>16分</td><td>16分</td><td>変わらない</td></tr>
          <tr><td>上野</td><td>21分</td><td>21分</td><td>変わらない</td></tr>
          <tr><td>東京</td><td>27分</td><td>27分</td><td>変わらない</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>どの駅も変わりません。</strong>東京への道順も「新宿 → 渋谷 → 品川 → 東京」のままです。</p>
        <p style="margin-top:0.6rem"><strong>理由:</strong>
        新宿から東京への最短経路は、もともと「新宿 → 渋谷 → 品川 → 東京」の27分でした。
        上野と東京をつなぐ辺は、この経路に<strong>1本も含まれていません</strong>。
        使っていない辺の重みをいくら大きくしても、使っている経路の合計は変わりません。</p>
        <p style="margin-top:0.6rem">上野への最短経路も「新宿 → 池袋 → 上野」の21分で、やはり上野と東京のあいだの辺を使っていません。
        書き換える前の実行結果（例題1）をよく見ると、東京は品川経由の27分で決まっており、
        上野経由の 21+6=27分 は「短くないので書き直さなかった」ことが分かります。
        書き換えたあとは上野経由が 21+40=61分 になりますが、もともと採用されていなかったので結果は同じです。</p>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        重みを変えたときに答えが変わるのは、その辺が<strong>最短経路の一部として使われているとき</strong>だけです。
        逆に、重みを小さくした場合は、使われていなかった辺が新しく最短経路に入ってくることがあり、答えが変わる可能性があります。
        （標準課題1の値を確かめたい場合は、6分を 3分 にして実行すると、東京が 21+3=24分 に変わることが観察できます。）</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "ダイクストラ法の考え方", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("05", NAV, body)
