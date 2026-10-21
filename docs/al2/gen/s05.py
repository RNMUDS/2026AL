# -*- coding: utf-8 -*-
"""第5回: ダイクストラ法（1）考え方 の本文を組み立てる。
例題は「参考（新宿の路線図）」と「クリエイティブ演習（ディズニーランドの地図）」の2本立て。"""
from slides_data import SLIDES
from slide_examples import slide_example
from common import (plain, slide_submission, slides_for, rubric_section, advanced_section, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, section, setup_guide, write)

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
BLUE = "#5AAAFF"


def trace(start="新宿"):
    """各手順の (確定した駅, 距離表のコピー, 確定済みの集合, [(駅, 前の値, 新しい値, 区間の時間)]) を返す。"""
    dist = {s: INF for s in STATIONS}
    dist[start] = 0
    settled = set()
    steps = [(None, dict(dist), set(), [])]
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
        changes = []
        for name, w in RAIL[cur]:
            if name in settled:
                continue
            if dist[cur] + w < dist[name]:
                changes.append((name, dist[name], dist[cur] + w, w))
                dist[name] = dist[cur] + w
        steps.append((cur, dict(dist), set(settled), changes))
    return steps


# ────────────────────────────────────────────────────────────
# 図1: ダイクストラ法の3つの手順
# ────────────────────────────────────────────────────────────
def fig_three_steps():
    steps = [
        ("① 選ぶ", "まだ決まっていない駅のうち、\n今わかっている時間がいちばん\n小さい駅を1つ選ぶ", GREEN),
        ("② 確定する", "選んだ駅の時間を「もう変わらない」\nと決める（確定させる）", AMBER),
        ("③ 書き直す", "選んだ駅のとなりの駅について、\nより短い行き方が見つかれば\n時間を書き直す", GREEN),
    ]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'ダイクストラ法は ①②③ のくり返し（1回ぶんを「手順1」「手順2」…と数える）</text>']
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
# 図2: グラフと距離表を並べて、手順1〜6を1つずつ追う（手計算のお手本）
# ────────────────────────────────────────────────────────────
def fig_trace():
    steps = trace()
    sc, row_h = 0.42, 118
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'ダイクストラ法で 新宿 から各駅までの時間を求める（手順1〜6）</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '白い枠 = いま確定した駅、緑 = 確定済み、橙 = 時間が書かれたがまだ確定していない駅、橙の線 = 書き込み・書き直しに使った区間</text>']
    for k, (cur, dist, settled, changes) in enumerate(steps[1:], 1):
        y0 = 60 + (k - 1) * row_h
        p = {st: (14 + (x - 150) * sc, y0 + 12 + (y - 50) * sc) for st, (x, y) in POS.items()}
        used = {frozenset((cur, n)) for n, *_ in changes}
        for a, b, w in EDGES:
            (x1, y1), (x2, y2) = p[a], p[b]
            on = frozenset((a, b)) in used
            s.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="{AMBER if on else "#3a3a3a"}" stroke-width="{3 if on else 1.5}"/>')
            dx = -8 if abs(x1 - x2) < 5 else 0
            s.append(f'        <text x="{(x1+x2)/2+dx:.0f}" y="{(y1+y2)/2-3:.0f}" text-anchor="middle" '
                     f'fill="{AMBER if on else "#666"}" font-size="8">{w}</text>')
        for st, (x, y) in p.items():
            ring = "#444"
            if dist[st] != INF:
                ring = AMBER
            if st in settled:
                ring = GREEN
            if st == cur:
                ring = "#FFFFFF"
            s.append(f'        <circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="#1A1A1A" stroke="{ring}" '
                     f'stroke-width="{2.5 if st == cur else 1.5}"/>')
            s.append(f'        <text x="{x:.0f}" y="{y+3:.0f}" text-anchor="middle" fill="#ddd" font-size="8">{st}</text>')
        tx = 236
        s.append(f'        <text x="{tx}" y="{y0+16}" fill="#E0E0E0" font-size="12" font-weight="700">'
                 f'手順{k}　{cur}（{dist[cur]}分）を確定</text>')
        for i, (n, old, new, w) in enumerate(changes):
            text = (f"{n} に {new}分 を書き込む（{dist[cur]} + {w}）" if old == INF
                    else f"{n} を {old}分 → {new}分 に書き直す（{dist[cur]} + {w}）")
            s.append(f'        <text x="{tx}" y="{y0+36+i*16}" fill="{RED if old != INF else "#bbb"}" '
                     f'font-size="11"{" font-weight=" + chr(34) + "700" + chr(34) if old != INF else ""}>{text}</text>')
        if not changes:
            s.append(f'        <text x="{tx}" y="{y0+36}" fill="{GRAY}" font-size="11">となりはすべて確定済み、'
                     'または表の時間が同じかもっと短い → 何もしない</text>')
        cw = 74
        for j, st in enumerate(STATIONS):
            x = tx + j * cw
            done = st in settled
            hit = any(n == st for n, *_ in changes)
            v = dist[st]
            s.append(f'        <rect x="{x}" y="{y0+74}" width="{cw-4}" height="30" rx="5" '
                     f'fill="{"#1a2e0a" if done else "#141414"}" stroke="{AMBER if hit else (GREEN if done else "#2e2e2e")}"/>')
            s.append(f'        <text x="{x+(cw-4)/2}" y="{y0+86}" text-anchor="middle" fill="{GRAY}" font-size="8">{st}</text>')
            s.append(f'        <text x="{x+(cw-4)/2}" y="{y0+100}" text-anchor="middle" '
                     f'fill="{AMBER if hit else ("#93D500" if done else "#999")}" font-size="11" '
                     f'font-weight="{700 if hit or done else 400}">{"－" if v == INF else str(v)}</text>')
        if k < len(steps) - 1:
            s.append(f'        <line x1="14" y1="{y0+row_h-6}" x2="686" y2="{y0+row_h-6}" stroke="#2a2a2a"/>')
    y = 60 + (len(steps) - 1) * row_h + 10
    s.append(f'        <text x="350" y="{y}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '品川は手順1で 30分 と書かれたが、手順2で渋谷を確定したときに 16分 に書き直された</text>')
    return fig(700, y + 16, "\n".join(s))


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
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("05")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第4回では、重み付きグラフで「合計時間がいちばん短い道」をさがしました。
      第4回の路線図には、辺に<strong>区間ごとにかかる時間（分）</strong>が書いてありました（重み付きグラフ）。
      ところが幅優先探索は、その時間を使わずに<strong>路線の本数</strong>だけを数えます。
      そのため新宿から品川へは、路線1本で着く直通（30分）を選び、渋谷で乗りかえる16分の道を見のがしました。
      全探索は正しい道を選べますが、地図が少し大きくなるだけで、調べる行き方の数が爆発的に増えます。
      そこで第5回は、<strong>行き方を全部は調べずに</strong>、合計時間がいちばん短い道を求める方法を学びます。
      全部調べなくてよいのは、<strong>出発点から近い駅の順に</strong>時間を決めていくからです。
      近い駅から決めていけば、ある駅の時間が決まった時点で、それより遠い駅を回る行き方はどれも長くなるとわかるので、
      調べる必要がありません（くわしい理由は、下の「いちばん小さい駅を確定してよい理由」で説明します）。
      <strong>ダイクストラ法</strong>です。1959年にエドガー・ダイクストラが考えた方法で、
      今のカーナビや乗換案内の中でも使われています。
    </p>

    <div class="analogy">
      出発点から各駅までの所要時間を、鉛筆で表に書いていく場面を思い浮かべてください。
      最初はどの駅も「わからない」ので空欄です。
      調べていくうちに「渋谷は7分で行ける」と分かれば書き込み、
      あとで「もっと早い行き方があった」と分かれば、消して書き直します。
      「この駅はもう書き直さない」と言い切れた駅から順に、ペンでなぞって確定させていきます。
      これがダイクストラ法です。
      第4回の全探索は、「新宿→品川」「新宿→渋谷→品川」「新宿→池袋→上野→東京→品川」のように、
      行き方を1本ずつ最後までたどって合計時間を比べました。
      行き方がちがえば同じ駅を何度も通るので、同じ駅を何度も調べ直すことになります。
      ダイクストラ法では、1つの駅からとなりの駅を調べるのは、<strong>その駅を確定させたときの1回だけ</strong>です。
      駅が6つなら、調べるのは6回で終わります。
    </div>

    <div class="concept-box">
      <h4>用語</h4>
      <table>
        <tr><th>用語</th><th>意味</th><th>路線図でいうと</th></tr>
        <tr><td><strong style="color:#76B900">距離表</strong></td><td>出発点から各頂点までの、今わかっているいちばん小さい合計コストを書いた表</td><td>新宿から各駅まで、今わかっている最短の時間</td></tr>
        <tr><td><strong style="color:#76B900">確定</strong></td><td>距離表の値が「もう変わらない」と決まること</td><td>ペンでなぞった駅</td></tr>
        <tr><td><strong style="color:#FFB800">書き直し（緩和）</strong></td><td>もっと小さい合計コストが見つかったときに、距離表の値を小さく書き直すこと</td><td>品川 30分 → 16分（渋谷で乗りかえるほうが早い）</td></tr>
        <tr><td><strong>inf（無限大）</strong></td><td>「まだ行き方が1つも見つかっていない」ことを表す印。表では「－」と書く</td><td>まだ空欄の駅</td></tr>
      </table>
    </div>

{fig_three_steps()}

    <div class="concept-box">
      <h4>ダイクストラ法で使う3つの入れもの</h4>
      <table>
        <tr><th>名前</th><th>中身</th><th>最初の状態</th></tr>
        <tr><td><code>distance</code></td><td>距離表。出発点からその駅までの、今わかっているいちばん短い時間</td><td>出発点だけ0、ほかはすべて <code>inf</code>（無限大）</td></tr>
        <tr><td><code>settled</code></td><td>「もう変わらない」と決まった（確定した）駅を入れる集合</td><td>空</td></tr>
        <tr><td><code>came_from</code></td><td>その駅へいちばん早く来るとき、1つ前にどの駅にいたか（例題2で使う）</td><td>すべて <code>None</code></td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        <code>inf</code> は Python で <code>float("inf")</code> と書く「無限大」の値です。
        どんな数と比べても必ず大きくなるので、「まだ行き方が1つも見つかっていない」ことを表すのに使えます。
      </p>
    </div>

    <h3 style="margin:2rem 0 0.8rem">手計算で1手順ずつたどる</h3>
    <p style="margin-bottom:1rem">
      第4回の路線図で、新宿から各駅までの時間をダイクストラ法で求めます。
      紙に6駅ぶんの表を書き、新宿だけ 0、ほかは「－」から始めます。
      1つの手順でやることは、①まだ確定していない駅のうち時間がいちばん小さい駅を選ぶ、②その駅を確定する、
      ③その駅のとなりの駅について「確定した駅の時間 ＋ 区間の時間」を計算し、表の値より小さければ書き直す、の3つです。
    </p>

{fig_trace()}

    <div class="concept-box">
      <h4>いちばん小さい駅を確定してよい理由</h4>
      <p style="font-size:0.95rem">
        手順の②で「もう変わらない」と決めてしまってよいのは、<strong>重み（区間の時間）がすべて0以上</strong>だからです。
        手順4で、まだ確定していない駅のうち時間がいちばん小さいのは品川（16分）でした。
        品川へ別の行き方でたどり着くには、必ず他の未確定の駅を通ります。
        他の未確定の駅は、どれも16分以上かかります（上野 21分、東京 －）。
        そこから品川へ進むと、重みが0以上なのでさらに時間が増えます。
        つまり<strong>16分より短くなることはありえません</strong>。
      </p>
    </div>

{fig_why_settle()}

    <div class="note-warn">
      <strong>成り立たなくなる場合:</strong> 重みにマイナスの値が混ざると、上の理由が使えなくなります。
      「遠回りをすると時間が減る」ことが起きてしまうためです。
      後期の路線図や迷路、今回のディズニーランドの地図では、時間がマイナスになることはないので安心して使えます。
    </div>

{fig_negative()}"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>グラフと距離表を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜4回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で、
      グラフと距離表を並べて、ダイクストラ法が1手順ずつ進むようすを見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜4回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜4回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（手計算と見比べたり、標準課題の図を描いたりするときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各ファイルの<strong>いちばん下</strong>
        （「ここから下は、…pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。
        丸の並べ方は、線の交わりが少なくなるように窓が自動で決めます。</p>
      </div>
    </div>"""

trouble = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>park に「○○」の行がない</code></td><td>足した場所の行（<code>"○○": [ ... ],</code>）を書き忘れたか、名前の打ちまちがい。行を足すか、名前をそろえる</td></tr>
          <tr><td><code>SyntaxError</code><br>（<code>Perhaps you forgot a comma?</code> など）</td><td>カンマ・かっこ・<code>"</code> の閉じ忘れ。<code>("場所", 時間)</code> の組と組のあいだにカンマ、行の最後にもカンマ。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>○○ の行の … がおかしい</code><br><code>… の時間がおかしい</code></td><td>組を <code>[ ]</code> で書いた、または時間を <code>"3"</code> のように <code>" "</code> で囲んだ。<code>("場所", 3)</code> のように <code>( )</code> で囲み、時間は数で書く</td></tr>
          <tr><td><code>A の行に（B, 3）があるのに、B の行に（A, 3）がない</code></td><td>道を片方の行にしか書いていないか、行きと帰りで時間がちがう。両方の行に同じ時間で書く</td></tr>
          <tr><td><code>start の「○○」が park にない</code><br><code>plan の「○○」が park にない</code></td><td>名前の打ちまちがい。<code>park</code> に書いた名前と1文字もちがわないようにする</td></tr>
          <tr><td><code>where の「○○」が park にない</code></td><td><code>park</code> を貼りかえたり場所を消したりしたのに、<code>where</code> に古い名前が残っている。<code>where</code> も同じ名前にそろえるか、その行を消す</td></tr>
          <tr><td><code>closed は [ ] で囲もう</code><br><code>closed の … がおかしい</code></td><td><code>closed = [("場所", "場所")]</code> のように、<code>[ ]</code> の中に <code>( )</code> の組を並べる。名前は <code>park</code> と同じにする</td></tr>
          <tr><td><code>closed の A と B の間には、もともと道がない</code></td><td>通行止めにできるのは、<code>park</code> に書いてある道だけ。となり合う2つの場所を選ぶ</td></tr>
          <tr><td><code>plan は [ ] で囲んで…</code><br><code>plan で「○○」が2回続いている</code></td><td><code>plan = ["エントランス", "プラザ"]</code> のように <code>[ ]</code> で囲み、同じ場所を続けて書かない</td></tr>
          <tr><td>ターミナルに「○○: 行けない」、窓に赤字「○○ へは行けない」</td><td>その場所が、どの道ともつながっていないか、<code>closed</code> の通行止めで切れている</td></tr>
        </table>
      </div>"""

missions1 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の地図</td><td>行ってみたいアトラクションやお店を、場所として<strong>2つ以上</strong>足す。
              歩く時間も自分の感覚で書き換え、<code>TITLE</code> も自分の題名にする。
              場所を足すときは、<strong>足した場所の行</strong>と、<strong>つなぐ相手の行</strong>の両方に書く（下の例）。
              <code>where</code> にも位置を足すと、窓の地図のその位置に描かれる（書かなければ、つながっている場所の近くに自動で置かれる）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>しかけ</td><td>「まっすぐ行く道より、寄り道したほうが早い」場所を作り、ターミナルの「書き直した」の行を<strong>2つ以上</strong>にする（ひな形はいま2つ。場所を足したあとも2つ以上残す）
              （コツ: 近い2つの場所を大きな時間の道でつなぎ、別の場所を通る道に小さな時間を付ける）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>通行止め</td><td><code>closed</code> に道を1本入れて実行する。どの場所の時間が何分に変わるかを、<strong>先に紙で予想してから</strong>窓で確かめる（いちばん早い道の上にある道を選ぶと、時間が変わる）</td></tr>
        </table>
{plain('''    "クリッターカントリー": [("ウエスタンランド", 4), ("スプラッシュ", 2)],   # ← 相手の行に足す
    "スプラッシュ": [("クリッターカントリー", 2)],                          # ← 足した場所の行''', "例: 場所「スプラッシュ」を、クリッターカントリーから歩いて2分の所に足す")}
      </div>"""

missions2 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>地図</td><td><code>park = {{ ... }}</code> を、演習1で作った自分の地図に貼りかえる（<code>where</code> と <code>closed</code> も同じ）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>回る順番</td><td><code>plan</code> に、回りたい場所を回る順に<strong>4つ以上</strong>並べる。最後を <code>"エントランス"</code> にすると帰り道まで案内する</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換えて、自分らしい案内文にする。
              使える材料: <code>route</code>（通る場所の並び）、<code>minutes</code>（区間の合計時間）、<code>walk(a, b)</code>（となりの a から b まで歩く時間）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>ひとこと</td><td><code>finish</code> 関数で、合計時間 <code>total</code> によって<strong>3通り以上</strong>のちがうメッセージを出す（<code>if</code> / <code>elif</code> / <code>else</code>）</td></tr>
        </table>
{plain('''    print(f"{route[0]}を出発！ {route[-1]}まで {minutes}分")
    for i in range(len(route) - 1):
        there = route[i + 1]
        print(f"  {i + 1}. {there}へ {walk(route[i], there)}分 歩く")''', "Lv3 の書き換えの例（そのまま使わず、自分で考えた文にする）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">文の中に絵文字を入れてもかまいません（ターミナルによっては表示されないことがあります）。</p>
      </div>"""

ex1_body = f"""      <p>例題1（参考）は、第4回の路線図で、ダイクストラ法を1手順ずつ進めるプログラムです。
      1章の「手計算で1手順ずつたどる」の図と同じことを、ターミナルと窓に表示します。
      演習1では、同じプログラムを<strong>自分で作ったディズニーランドの地図</strong>で動かします。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>distance[station] = INF</code></td><td>距離表を「－」（無限大）で埋め、出発点だけ <code>0</code> にする</td></tr>
        <tr><td><code>if current is None or distance[station] &lt; distance[current]:</code></td><td>①: まだ確定していない駅を1つずつ見て、時間がいちばん小さい駅を <code>current</code> に残す</td></tr>
        <tr><td><code>settled.add(current)</code></td><td>②: <code>current</code> を確定する</td></tr>
        <tr><td><code>new_distance = distance[current] + minutes</code></td><td>③: 「確定した駅までの時間 ＋ 区間の時間」を計算し、表の値より小さければ書き直す</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: グラフ</td><td>丸の外の数字 = 距離表の時間。白い枠 = いま確定した場所、緑 = 確定済み、橙 = 時間が書かれたがまだ確定していない場所。
            橙の線 = いま書き込み・書き直しに使った道。赤い点線 = 通行止め</td></tr>
        <tr><td>右: 距離表</td><td>確定した場所の行は緑。この手順で変わった時間は <code>30分 → 16分</code> のように橙で出る</td></tr>
        <tr><td>右下</td><td>その手順で確定した場所と、書き込み・書き直しの足し算。最後の画面には、書き直しが全部で何回あったかが出る</td></tr>
      </table>

{example_pair('AL2-05-ex1.py', '手順1で新宿を確定すると、渋谷7分・池袋9分・品川30分が書き込まれます。'
     '手順2で渋谷を確定したとき、<strong>品川の時間が30分から16分に書き直されて</strong>います。'
     '直通の30分より、渋谷で乗りかえる 7 + 9 = 16分 のほうが早いことが見つかったためです。'
     '品川の16分はそのあと書き直されず、手順4で確定しています。'
     '新宿から東京までは27分と求まりました。1章の手計算の図と、確定の順番も時間も一致しています。',
     creative=missions1)}
{trouble}

{notion('標準課題の①②は、演習1で作った<strong>自分の地図</strong>を使う。ターミナルの「確定」の行から確定の順番と時間を、'
        '「書き直した」の行から書き直しの足し算を写す。窓を → キーで1手順ずつ進めると、どの道で書き直したかが分かる。')}"""

ex2_body = f"""      <p>ダイクストラ法は最短時間を求めますが、そのままでは「どの道を通ったか」が分かりません。
      時間を書き直すときに、<strong>どの場所から来たか</strong>（<code>came_from</code>）も一緒に書き直しておけば、
      あとでゴールから逆にたどって道順を組み立てられます。第1回の幅優先探索で道を組み立てたときと同じやり方です。
      演習2では、これを使って<strong>自分だけの園内ナビ</strong>を作ります。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>def dijkstra(start):</code></td><td>例題1と同じダイクストラ法を関数にしたもの。<code>return distance, came_from, log</code> で3つをまとめて返す</td></tr>
        <tr><td><code>came_from[name] = current</code></td><td>時間を書き直すときに、「<code>name</code> へは <code>current</code> から来るのがいちばん早い」も書き直す</td></tr>
        <tr><td><code>def build_route(goal, came_from):</code></td><td>ゴールから <code>came_from</code> を1つずつ読んで出発点までもどり、最後に <code>reverse()</code> で順番をひっくり返す</td></tr>
        <tr><td><code>for i in range(len(plan) - 1):</code></td><td>（演習2）<code>plan</code> のとなり合う2つの場所ごとに、ダイクストラ法をやり直して道順を求める</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓の場面</th><th>読み方</th></tr>
        <tr><td>前半: 道をさがす</td><td>緑の線 = <code>came_from</code>（その場所へ、いちばん早く来た道）。右の表に <code>came_from</code> の列が増え、書き直されたところは橙で出る</td></tr>
        <tr><td>後半: 逆にたどる</td><td>ゴールから1つずつ <code>came_from</code> を読んで線が伸びていく。出発点に着いたら、ひっくり返した道順が出る</td></tr>
        <tr><td>最後の画面</td><td>できあがった道順。演習2では、区間ごとに色を変えて重ねて描き、合計時間を出す</td></tr>
      </table>

{example_pair('AL2-05-ex2.py', '各駅への最短の行き方が、駅名を矢印でつないだ形で表示されました。'
     '東京へは「新宿 → 渋谷 → 品川 → 東京」の27分が最短です。'
     '<code>came_from</code> の中身を見ると、東京には「品川」、品川には「渋谷」、渋谷には「新宿」と書かれています。'
     '東京から逆にたどると 東京 ← 品川 ← 渋谷 ← 新宿 となり、順番をひっくり返せば道順になります。'
     '品川の <code>came_from</code> は、時間が30分から16分に書き直されたときに「新宿」から「渋谷」に書き直されています（窓の前半の手順2）。',
     creative=missions2)}
{trouble}

{notion('標準課題の③は、演習2の<strong>自分のナビ</strong>を使う。ターミナルの【○○ から ○○ へ】の区間を1つ選び、'
        'ゴールから <code>came_from</code> を逆にたどる矢印（ゴール ← … ← 出発）で描く。'
        '通る場所の並びで、となりの左側がその場所の <code>came_from</code> になっている。窓の後半で、ゴールから線が伸びていく順番と見比べるとよい。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回は、例題（参考）を動かしてダイクストラ法の進み方をつかんだら、
    <strong>クリエイティブ演習</strong>で、ディズニーランドを題材に自分の作品を作ります。
    演習1で園内の地図を作り、演習2でその地図を使った園内ナビを作ります。</p>
    <p style="margin-bottom:1.5rem">ひな形の地図は、東京ディズニーリゾート公式ブログ
    「<a href="https://www.tokyodisneyresort.jp/tdrblog/detail/190415/" style="color:#76B900" target="_blank" rel="noopener">開園当時のマップをご紹介</a>」（2019年4月）に載っている
    「今の東京ディズニーランドのマップ」をもとにしました。エントランスからワールドバザールを通ってプラザ（シンデレラ城の前の広場）に出て、
    そこから各テーマランドへ分かれるつながり方は、地図のとおりです。
    歩く時間は目安なので、自分の感覚で変えてかまいません（2020年にできた「美女と野獣」のエリアなどは、この地図にはありません。足したい人は自分で足してよい）。
    まず作業フォルダを用意します。</p>

{setup_guide('05', ['AL2-05-ex1.py', 'AL2-05-ex2.py'])}

{pygame_card}

{keywords([
    ('ダイクストラ法', 'Dijkstra法', '重みが0以上のグラフで、出発点から各頂点までの最小コストを求めるアルゴリズム。'),
    ('距離表', 'distance', '出発点から各頂点までの、今わかっているいちばん小さい合計コスト。最初は出発点だけ0、ほかは inf。'),
    ('確定', 'かくてい / settled', 'その頂点までの最小コストが「もう変わらない」と決まった状態。確定した頂点は二度と書き直さない。'),
    ('書き直し（緩和）', 'かんわ / relaxation', '「別の道を通ったほうが短い」と分かったときに、距離表の値を小さく書き直す操作。'),
    ('inf', 'infinity / 無限大', 'Pythonで <code>float("inf")</code> と書く。どんな数より大きいので「まだ行き方が見つかっていない」印として使える。'),
    ('came_from', 'カム・フロム', 'その頂点へいちばん早く来るときの、1つ前の頂点。ゴールから逆にたどると道順になる。'),
    ('複数の値を返す', 'return a, b, c', '<code>return distance, came_from, log</code> のようにカンマで並べると、3つまとめて返せる。'
     '受け取る側は <code>distance, came_from, log = dijkstra(here)</code> のように、同じ数の変数を並べて受け取る。'),
])}

{example(1, '距離表が埋まっていく様子を見て、自分のディズニー地図を作る', ex1_body)}

{example(2, '道順を組み立てて、自分だけの園内ナビを作る', ex2_body)}"""

ans = answers([slide_example("05"),
    ("演習のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの地図で、エントランスから各場所までの時間と確定の順番です。自分の地図に書き換えたあとは、数字が変わります。</p>
        <table>
          <tr><th>確定の順番</th><th>場所</th><th>時間</th></tr>
          <tr><td>1</td><td>エントランス</td><td>0分</td></tr>
          <tr><td>2</td><td>ワールドバザール</td><td>3分</td></tr>
          <tr><td>3</td><td>プラザ</td><td>6分</td></tr>
          <tr><td>4</td><td>シンデレラ城</td><td>7分</td></tr>
          <tr><td>5</td><td>アドベンチャーランド</td><td>9分</td></tr>
          <tr><td>6</td><td>ファンタジーランド</td><td>9分</td></tr>
          <tr><td>7</td><td>トゥモローランド</td><td>9分</td></tr>
          <tr><td>8</td><td>ウエスタンランド</td><td>12分</td></tr>
          <tr><td>9</td><td>トゥーンタウン</td><td>13分</td></tr>
          <tr><td>10</td><td>クリッターカントリー</td><td>16分</td></tr>
        </table>
        <p style="margin-top:0.6rem">書き直しは2回です（アドベンチャーランド 10→9、トゥモローランド 10→9。ワールドバザールの横の通路より、プラザを通るほうが早い）。
        同じ9分の場所が3つあります。同じ時間のときは、<code>park</code> に先に書いた場所が先に確定します。</p>"""),
    ("理解度チェックの答えの例（ひな形の地図の場合）", """        <p><strong>通行止めにした道</strong>: プラザ—シンデレラ城（1分）</p>
        <p><strong>予想</strong>: シンデレラ城とファンタジーランドへは、プラザから城を通って行けなくなる。
        ファンタジーランドへは トゥモローランド経由 9 + 6 = 15分 と ウエスタンランド経由 12 + 5 = 17分 のうち、小さいほうの <strong>15分</strong>。
        シンデレラ城へは、ファンタジーランドから 15 + 2 = <strong>17分</strong>。
        トゥーンタウンは、ファンタジーランド経由の13分が使えなくなり、トゥモローランド経由 9 + 5 = <strong>14分</strong>。</p>
        <p><strong>結果</strong>: ファンタジーランド 9分→15分、シンデレラ城 7分→17分、トゥーンタウン 13分→14分 で、予想どおりだった。ほかの場所は変わらない。</p>"""),
    ("演習2のひな形の確かめ用", """        <p><code>plan = ["エントランス", "クリッターカントリー", "トゥーンタウン", "エントランス"]</code> のとき、区間ごとの時間は
        エントランス→クリッターカントリー 16分、クリッターカントリー→トゥーンタウン 13分、トゥーンタウン→エントランス 13分 で、合計 <strong>42分</strong> です。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "ダイクストラ法の考え方", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("05", SLIDES),
    advanced_section("05"),
    rubric_section("05"),
    ans,
])

write("05", NAV, body)
