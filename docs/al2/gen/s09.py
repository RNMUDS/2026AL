# -*- coding: utf-8 -*-
"""第9回: 巡回セールスマン問題（2）貪欲法による近似 の本文を組み立てる。
例題は「参考（学校など5都市・8都市）」と「クリエイティブ演習（ナガシマスパーランドで回りたい場所を貪欲法で回る）」の2本立て。"""
import ast
import math
import re
from itertools import permutations
from slides_data import SLIDES
from slide_examples import slide_example
from common import (HERE, plain, slide_submission, slides_for, rubric_section, advanced_section, example_pair,
                    AMBER, GRAY, GREEN, RED, answers, example, fig,
                    keywords, notion, section, setup_guide, write)
from pyhl import highlight   # noqa: E402（common が読みこみ先を追加したあとで読む）

CITIES = [("学校", 2, 2), ("郵便局", 10, 3), ("図書館", 14, 9),
          ("カフェ", 6, 12), ("公園", 3, 8), ("駅", 17, 4),
          ("病院", 12, 13), ("書店", 8, 7)]
HOUSES = [("営業所", 0, 8), ("A宅", 1, 5), ("遠方のD宅", 11, 2),
          ("B宅", 6, 4), ("E宅", 0, 12), ("C宅", 5, 9)]


def template_spots(filename):
    """演習のひな形（src のファイル）に書いてある spots を読みとる。本文の数値をひな形と必ず一致させるため。"""
    src = (HERE / "src" / filename).read_text(encoding="utf-8")
    return ast.literal_eval(re.search(r"^spots = (\[\n.*?\n\])", src, re.S | re.M).group(1))


NAGA = template_spots("AL2-09-ex1.py")
assert NAGA == template_spots("AL2-09-ex2.py"), "演習1と演習2のひな形の spots がちがう"


def table(cs):
    """距離の表（例題・演習と同じく、小数第1位に丸める）。"""
    n = len(cs)
    return [[round(math.hypot(cs[i][1] - cs[j][1], cs[i][2] - cs[j][2]), 1) for j in range(n)] for i in range(n)]


def greedy(cs, start=0):
    """例題・演習と同じ貪欲法。回る順番・合計・えらんだ記録 (いまいる所, 候補, えらんだ所) を返す。"""
    t = table(cs)
    n = len(cs)
    visited, total, here, steps = [start], 0, start, []
    while len(visited) < n:
        nearest, cand = None, []
        for j in range(n):
            if j in visited:
                continue
            cand.append(j)
            if nearest is None or t[here][j] < t[here][nearest]:
                nearest = j
        steps.append((here, cand, nearest))
        total += t[here][nearest]
        visited.append(nearest)
        here = nearest
    return visited, round(total + t[here][start], 1), steps


def optimal(cs):
    t = table(cs)
    n = len(cs)
    best, bo = None, None
    for o in permutations(range(1, n)):
        s, h = 0, 0
        for c in o:
            s += t[h][c]
            h = c
        s += t[h][0]
        if best is None or s < best:
            best, bo = s, o
    return [0] + list(bo), round(best, 1)


def percent(longer, shorter):
    return round(round(longer - shorter, 1) / shorter * 100, 1)


def names(cs, route, back=True):
    seq = list(route) + ([route[0]] if back else [])
    return " → ".join(cs[i][0] for i in seq)


G5, G5_LEN, G5_STEPS = greedy(CITIES[:5])
O5, O5_LEN = optimal(CITIES[:5])
G8, G8_LEN, _ = greedy(CITIES)
O8, O8_LEN = optimal(CITIES)
P8 = percent(G8_LEN, O8_LEN)
GH, GH_LEN, _ = greedy(HOUSES)
OH, OH_LEN = optimal(HOUSES)
PH = percent(GH_LEN, OH_LEN)
GN, GN_LEN, GN_STEPS = greedy(NAGA)
ON, ON_LEN = optimal(NAGA)
PN = percent(GN_LEN, ON_LEN)
assert G5_LEN == O5_LEN and G8_LEN > O8_LEN and GN_LEN > ON_LEN and PN < 10 and PH > 30


def draw_route(cs, route, x0, y0, sx, sy, color, r=11, labels=True, closed=True):
    out = []
    seq = route + [route[0]] if closed else route
    for k in range(len(seq) - 1):
        a, b = seq[k], seq[k + 1]
        x1, y1 = x0 + cs[a][1] * sx, y0 + cs[a][2] * sy
        x2, y2 = x0 + cs[b][1] * sx, y0 + cs[b][2] * sy
        out.append(f'        <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{color}" stroke-width="2.5"/>')
    order = {c: i for i, c in enumerate(route)}
    for i, (name, x, y) in enumerate(cs):
        cx, cy = x0 + x * sx, y0 + y * sy
        col = AMBER if i == route[0] else color
        out.append(f'        <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
        mark = "S" if i == route[0] else str(order[i])
        out.append(f'        <text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" fill="#E0E0E0" font-size="{r-2}" font-weight="700">{mark}</text>')
        if labels:
            out.append(f'        <text x="{cx:.0f}" y="{cy-r-5:.0f}" text-anchor="middle" fill="{GRAY}" font-size="9">{name}</text>')
    return out


# ────────────────────────────────────────────────────────────
# 図1: 貪欲法の進み方
# ────────────────────────────────────────────────────────────
def fig_greedy_steps():
    cs = CITIES[:5]
    t = table(cs)
    route, total = G5, G5_LEN
    sx, sy, ox, oy = 30, 20, 60, 78
    dur = 14
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '貪欲法: いまいる都市から、いちばん近い都市へ進むことをくり返す</text>']
    for i in range(5):
        for j in range(i + 1, 5):
            x1, y1 = ox + cs[i][1] * sx, oy + cs[i][2] * sy
            x2, y2 = ox + cs[j][1] * sx, oy + cs[j][2] * sy
            s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#242424" stroke-width="1"/>')
    seq = route + [route[0]]
    for k in range(len(seq) - 1):
        a, b = seq[k], seq[k + 1]
        x1, y1 = ox + cs[a][1] * sx, oy + cs[a][2] * sy
        x2, y2 = ox + cs[b][1] * sx, oy + cs[b][2] * sy
        p0 = (1 - 0.18) * k / (len(seq) - 1)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{p0:.3f};{p0+0.03:.3f};1" '
                f'dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="3.5"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'          <text x="{mx}" y="{my-8}" text-anchor="middle" fill="{GREEN}" font-size="11" font-weight="700">{t[a][b]}</text>')
        s.append('        </g>')
        label = ("出発点へ戻る" if k == len(seq) - 2
                 else f"{cs[a][0]} から見ていちばん近いのは {cs[b][0]}")
        s.append(f'        <text x="350" y="52" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{p0:.3f};{p0+0.02:.3f};{p0+0.14:.3f};{p0+0.16:.3f};1" dur="{dur}s" repeatCount="indefinite"/>'
                 f'{k+1}本目: {label}</text>')
    for i, (name, x, y) in enumerate(cs):
        cx, cy = ox + x * sx, oy + y * sy
        col = AMBER if i == 0 else GREEN
        s.append(f'        <circle cx="{cx}" cy="{cy}" r="15" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
        s.append(f'        <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">{i}</text>')
        s.append(f'        <text x="{cx}" y="{cy-20}" text-anchor="middle" fill="{GRAY}" font-size="10">{name}</text>')
    s.append(f'        <text x="350" y="{oy+13*sy+30}" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             f'貪欲法の答え: 合計 {total}　（この5都市では、全探索の答えと同じになった）</text>')
    return fig(700, oy + 13 * sy + 46, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 8都市での比較
# ────────────────────────────────────────────────────────────
def fig_compare8():
    cs = CITIES
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '都市が8個になると、貪欲法は最短ルートを見つけられない</text>']
    for panel, (route, total, title, color) in enumerate([
            (G8, G8_LEN, "貪欲法", AMBER), (O8, O8_LEN, "全探索（本当の最短）", GREEN)]):
        x0 = 20 + panel * 350
        s.append(f'        <rect x="{x0}" y="46" width="330" height="258" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="68" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">'
                 f'{title}: 合計 {total}</text>')
        s += draw_route(cs, route, x0 + 24, 88, 15.5, 12.5, color, 11)
    s.append(f'        <text x="350" y="326" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             f'差は {round(G8_LEN-O8_LEN,1)}。貪欲法は最短ルートより {P8}% 長い（丸の数字 = 回る順番、S = 出発点）</text>')
    return fig(700, 342, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 出発点を変えたときの結果
# ────────────────────────────────────────────────────────────
def start_results(cs):
    return [(cs[start][0], greedy(cs, start)[1]) for start in range(len(cs))]


def fig_starts():
    cs = CITIES
    results = start_results(cs)
    worst = max(v for _, v in results)
    hits = [name for name, v in results if v == O8_LEN]
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '出発する都市を変えるだけで、貪欲法の答えは大きく変わる</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         f'全探索で求めた本当の最短は {O8_LEN}（緑の点線）。棒 = その都市から出発した貪欲法の合計</text>']
    x0, wmax = 130, 440
    for i, (name, v) in enumerate(results):
        y = 62 + i * 34
        w = v / worst * wmax
        color = GREEN if v == O8_LEN else (RED if v == worst else AMBER)
        s.append(f'        <text x="118" y="{y+19}" text-anchor="end" fill="#ccc" font-size="11">{name}から出発</text>')
        s.append(f'        <rect x="{x0}" y="{y+4}" width="{w:.0f}" height="22" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{x0+w+10:.0f}" y="{y+21}" fill="{color}" font-size="12" font-weight="700">{v}</text>')
    xline = x0 + O8_LEN / worst * wmax
    s.append(f'        <line x1="{xline:.0f}" y1="56" x2="{xline:.0f}" y2="{62+8*34}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'        <text x="350" y="{62+8*34+22}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             f'{"・".join(hits)}から出発したときだけ、たまたま最短ルートに当たっている</text>')
    return fig(700, 62 + 8 * 34 + 40, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 貪欲法が大きく損をする配置
# ────────────────────────────────────────────────────────────
def fig_trap():
    cs = HOUSES
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{RED}" font-weight="700" font-size="15">'
         '遠くに1軒だけ離れた家があると、貪欲法は大きく損をする（宅配便の例）</text>']
    for panel, (route, total, title, color) in enumerate([
            (GH, GH_LEN, "貪欲法", RED), (OH, OH_LEN, "全探索（本当の最短）", GREEN)]):
        x0 = 20 + panel * 350
        s.append(f'        <rect x="{x0}" y="46" width="330" height="250" rx="10" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x0+165}" y="68" text-anchor="middle" fill="{color}" font-size="13" font-weight="700">'
                 f'{title}: 合計 {total}</text>')
        s += draw_route(cs, route, x0 + 46, 92, 22, 15, color, 12)
    last = HOUSES[GH[-1]][0]
    s.append(f'        <text x="350" y="318" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             f'貪欲法は最短より {PH}% 長い。{last}を最後まで残し、そこへの行きと帰りの2回が長い移動になった</text>')
    return fig(700, 334, "\n".join(s))


def pycode(src, label):
    """Python のコードを色つきの <pre> にする（本文の説明用）。"""
    return f'<pre data-blanks="0"><span class="code-label">{label}</span>\n{highlight(src)}</pre>'


def trace_table(cs, steps, route, unit=""):
    """貪欲法の進み方を、1回ごとの表にする（いまいる所・行った所・候補と距離・えらんだ所）。"""
    t = table(cs)
    rows = []
    for k, (here, cand, nearest) in enumerate(steps):
        went = " → ".join(str(i) for i in route[:k + 1])
        cands = "　".join(
            (f'<strong style="color:#76B900">{cs[j][0]} {t[here][j]}{unit}</strong>' if j == nearest else f'{cs[j][0]} {t[here][j]}{unit}')
            for j in cand)
        rows.append(f'          <tr><td style="white-space:nowrap">{k + 1}回目</td><td style="white-space:nowrap">{here}（{cs[here][0]}）</td>'
                    f'<td style="white-space:nowrap"><code>[{went.replace(" → ", ", ")}]</code></td><td>{cands}</td>'
                    f'<td style="white-space:nowrap">{nearest}（{cs[nearest][0]}）</td></tr>')
    last = route[-1]
    rows.append(f'          <tr><td>最後</td><td style="white-space:nowrap">{last}（{cs[last][0]}）</td>'
                f'<td style="white-space:nowrap"><code>[{", ".join(str(i) for i in route)}]</code></td>'
                f'<td>候補はもうない（<code>while</code> が終わる）。出発点へ戻る {t[last][route[0]]}{unit}</td>'
                f'<td style="white-space:nowrap">{route[0]}（{cs[route[0]][0]}）へ戻る</td></tr>')
    return ('        <table>\n          <tr><th></th><th>here<br>（いまいる所）</th><th>visited<br>（行った所）</th>'
            '<th>候補（まだ行っていない所）と、そこまでの距離</th><th>nearest<br>（えらんだ所）</th></tr>\n'
            + "\n".join(rows) + "\n        </table>")


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "貪欲法とは #sec-explanation",
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("09")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第8回で確かめたとおり、巡回セールスマン問題（すべての地点を1回ずつ回って出発点へ戻る、いちばん短いルートをさがす問題）は、
      地点が増えると全探索（すべての順番を試す方法）が使えなくなります。15か所で数時間、20か所では何百年〜千年以上かかる見積もりでした。
      そこで発想を変えます。<strong>「必ず最短」をあきらめて、「そこそこ短いルートを一瞬で作る」</strong>方法を考えます。
      いちばん単純な作戦が<strong>貪欲法</strong>（どんよくほう）です。
    </p>

    <div class="analogy">
      ナガシマスパーランド（三重県にある、ジェットコースターで有名な遊園地）に着いた場面を思い浮かべてください。
      乗りたいものは10個以上あります。第8回の方法で全部の回り方を調べると、10か所で約36万通り、15か所なら何時間もかかり、調べ終わる前に閉園してしまいます。
      実際には、多くの人が<strong>「とりあえず、いまいる場所からいちばん近いものに乗る。終わったら、またそこからいちばん近いものへ行く」</strong>と決めているはずです。
      全部の回り方を頭の中で比べる人はいません。
      先のことは考えず、目の前でいちばん良さそうな選択をくり返す考え方が、貪欲法です。
      「貪欲」は「よくばり」という意味で、毎回その場でいちばん得なもの（いちばん近い場所）をよくばって取ることから、この名前が付いています。
      今回のクリエイティブ演習では、<strong>自分が回りたい場所</strong>を貪欲法で回り、全探索の答えとどれくらいちがうかを調べます。
    </div>

    <div class="concept-box">
      <h4>貪欲法の手順（最近傍法）</h4>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li>出発点に立つ</li>
        <li>まだ行っていない都市のうち、<strong>いまいる場所からいちばん近い都市</strong>を選ぶ</li>
        <li>そこへ移動する</li>
        <li>まだ行っていない都市がある間、2と3をくり返す</li>
        <li>全部回り終えたら出発点へ戻る</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        「いちばん近い都市へ進む」という選び方から、<strong>最近傍法</strong>（さいきんぼうほう。「最も近い、となり」という意味）とも呼ばれます。
        都市が n 個なら、えらぶ回数は n − 1 回で、そのたびに残りの都市までの距離を比べるだけです。
        比べる回数は全部で <code>n × (n − 1) ÷ 2</code> 回なので、8都市なら28回、1000都市でも約50万回で終わります
        （全探索は、8都市で 7! = 5,040通り、1000都市では宇宙が終わるまでかけても終わりません）。
      </p>
    </div>

{fig_greedy_steps()}

    <div class="concept-box">
      <h4>貪欲法が最短にならない理由</h4>
      <p style="font-size:0.95rem">
        貪欲法は、1歩先だけを見て決めます。「いま近い」都市を選んだせいで、
        あとから<strong>遠く離れた都市が取り残される</strong>ことがあります。
        取り残された都市へ行くには長い移動が必要になり、その1回で、それまでに節約した分をすべて失ってしまいます。
        とくに<strong>最後に出発点へ戻る1本</strong>は、えらぶことができません。どれだけ遠くても行くしかありません。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        目の前だけを見て決めた結果、全体としては良くならないことを<strong>局所最適</strong>（きょくしょさいてき）と呼びます。
        「部分的にはいちばん良い」けれど「全体でいちばん良いとはかぎらない」という意味です。
        遊園地でいえば、「近いものから順に乗っていたら、いちばん奥のコースターだけが残り、最後に園内を1往復することになった」という状態です。
      </p>
    </div>

{fig_compare8()}

{fig_trap()}

    <div class="concept-box">
      <h4>近似解という考え方</h4>
      <table>
        <tr><th></th><th>全探索（第8回）</th><th>貪欲法（第9回）</th></tr>
        <tr><td>答えの質</td><td>必ず最短（最適解）</td><td>最短とはかぎらない（近似解）</td></tr>
        <tr><td>8都市での結果（上の図）</td><td>{O8_LEN}</td><td>{G8_LEN}（{P8}%長い）</td></tr>
        <tr><td>調べる数</td><td>(n−1)! 通りの順番</td><td>n × (n−1) ÷ 2 回の比べ</td></tr>
        <tr><td>20都市</td><td>何百年もかかる</td><td>一瞬で終わる</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        考えられる中で本当にいちばん良い答えを<strong>最適解</strong>（さいてきかい）、
        最適ではないけれど実用的な答えを<strong>近似解</strong>（きんじかい。「近くて似ている答え」という意味）と呼びます。
        配送計画では「1%短いルートを1週間かけて計算する」より
        「10%長くても1秒で出す」ほうが役に立つ場面がほとんどです。
        遊園地でも、回り方を何時間も計算するより、少し遠回りでもすぐ歩き始めたほうが、たくさん乗れます。
      </p>
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>地図と計算の進み方を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜8回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で表示します。
      例題1・演習1は<strong>貪欲法が「いちばん近い場所」を1つずつえらぶようす</strong>を、
      例題2・演習2は<strong>貪欲法のルートと全探索のルートを左右に並べたもの</strong>を見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜8回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜8回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（貪欲法が場所を1つえらぶごと。標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各ファイルの<strong>いちばん下</strong>
        （「ここから下は、…pygame の窓に絵で表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。</p>
      </div>
    </div>"""

trouble1 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習1）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>SyntaxError</code></td><td>かっこ・<code>"</code> の閉じ忘れ。<code>spots</code> の各行は <code>("白鯨", 15, 3),</code> のように書く。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>TypeError: 'tuple' object is not callable</code></td><td><code>spots</code> の行の<strong>最後のカンマ</strong>を書き忘れた。<code>( … )</code> の後ろに <code>,</code> を付ける</td></tr>
          <tr><td><code>spots の ○番目の位置がおかしい</code></td><td>x や y を <code>"7"</code> のように <code>" "</code> で囲んだ。数は囲まずに <code>7</code> と書く</td></tr>
          <tr><td><code>spots の ○番目が ("名前", x, y) の形になっていない</code></td><td>名前・x・y の3つがそろっていない。カンマが2つあるかを見る</td></tr>
          <tr><td><code>「○」が2回出てくる</code> ／ <code>同じ位置にある</code></td><td>同じ名前か同じ位置の場所が2つある。名前か x・y のどちらかを変える</td></tr>
          <tr><td><code>spots が ○か所ある</code></td><td>17か所以上にした。貪欲法は計算できるが、窓に入りきらないので16か所までにする</td></tr>
          <tr><td><code>START の「○」が spots にない</code></td><td>名前が1文字ちがう（「2000」のあるなし、全角と半角など）。<code>spots</code> の名前をコピーして貼る。0番から出発するときは <code>START = None</code>（<code>" "</code> で囲まない）</td></tr>
          <tr><td>同じ距離の場所が2つあるとき、どちらをえらぶ？</td><td><strong>番号の小さいほう</strong>をえらぶ。<code>&lt;</code>（より小さい）で比べているので、同じ距離では書きかえないため</td></tr>
        </table>
      </div>"""

trouble2 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習2）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td>演習1と貪欲法の時間がちがう</td><td><code>spots</code> か <code>WALK</code> を貼りかえ忘れた。演習1の <code>spots = [</code> から <code>]</code> までと、<code>WALK = …</code> の行をそのまま貼る。
              演習1で <code>START</code> を変えていた人は、演習2では0番から出発するので、下の「出発する場所を変えると」の表の同じ番号の行と比べる</td></tr>
          <tr><td><code>spots が 11か所 ある。…全探索が …</code></td><td>演習1は16か所まで増やせるが、演習2は全探索も動かすので<strong>10か所まで</strong>。残さない場所の行の先頭に <code>#</code> を付けて減らす（<code>#</code> を付けた行は実行されない）</td></tr>
          <tr><td><code>spots が少なすぎる。3か所だと …</code></td><td>3か所だと回り方が1通り（とその逆回り）しかなく、貪欲法と全探索が必ず同じになる。メインゲートのほかに3か所以上にする</td></tr>
          <tr><td>「速さ: 約○倍」が実行のたびに変わる</td><td>貪欲法が速すぎて（100万分の数秒）、ほかのアプリの動きなどで時間がゆれるため。何回か実行して、だいたいの大きさを見ればよい</td></tr>
          <tr><td>貪欲法と全探索が同じ時間になった</td><td>まちがいではない。場所が少ないときや、きれいに輪の形に並んでいるときは、貪欲法が最短に当たることがある。場所を足したり動かしたりして試す（Lv3）</td></tr>
          <tr><td>2つのルートは形が同じなのに、順番が逆</td><td>逆回りは同じ道を反対向きに歩くだけなので、合計は同じ（第8回で確かめた）。丸の数字ではなく、線の形を見比べる</td></tr>
        </table>
      </div>"""

missions1 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> を、<strong>自分が回りたい場所</strong>にする（名前と位置 x・y を書き換える。乗り物・プール・お店など何でもよい）。0番はメインゲート（入り口）のまま。
              <code>TITLE</code> も自分のものにする。位置は、ナガシマスパーランド公式サイトの園内マップなどを見て、だいたいでよい（1目もり = 歩いて1分くらい）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>8か所以上</td><td>場所を<strong>8か所以上</strong>（メインゲート＋7か所以上。16か所まで）にする。ターミナルに「Lv2 達成」と出ればよい。
              「調べた候補」の数（<code>n × (n-1) ÷ 2</code>）と、「全探索なら」の順番の数を見比べる（8か所なら 28 と 5,040）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>出発を変える</td><td><code>START</code> に、出発する場所の名前を書く（例: <code>START = "白鯨"</code>。ホテルや別の入り口から入った、という想定）。
              0番から出発したときより<strong>何分早く（おそく）なるか</strong>が表示される。変わらない場所もあるので、何か所か試す</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、自分らしい「回り方の案内」にする。
              使える材料: <code>route</code>（回る場所の名前の並び。<code>route[1]</code> が最初に行く場所）、<code>total</code>（合計の分）</td></tr>
        </table>
      </div>"""

missions2 = """      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の場所</td><td><code>spots</code> と <code>WALK</code> を、<strong>演習1で作った自分のもの</strong>に貼りかえる（10か所まで。多いときは行の先頭に <code>#</code> を付けて減らす）。
              貪欲法の回り方が、全探索の「本当にいちばん早い回り方」より<strong>何分おそいか（何%長いか）</strong>を確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>8か所以上</td><td>場所を<strong>8か所以上</strong>にして実行する（10か所まで）。2つの方法の「かかった時間」を比べる。
              いちばん下の表で、15か所・20か所・100か所のときの<strong>貪欲法の時間（実測）と全探索の時間（見積もり）</strong>を確かめる。<strong>標準課題で使うので、20か所の行をメモしておく</strong></td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>貪欲法の弱点</td><td>場所の位置を動かしたり、場所を足したりして、貪欲法が本当の最短より<strong>10%以上おそくなる配置</strong>を作る。ターミナルに「Lv3 達成」と出ればよい。
              ヒント: 上の「宅配便の例」の図のように、<strong>遠くに1か所だけ離れた場所</strong>を置く。「出発する場所を変えると」の表で、どの場所から出発すると損が大きいかも見る</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>案内文</td><td><code>announce</code> 関数の <code>print</code> を書き換え、2つの回り方を自分らしく案内する。
              使える材料: <code>greedy_route</code>・<code>best_route</code>（回る場所の名前の並び）、<code>greedy_total</code>・<code>best_total</code>（合計の分）</td></tr>
        </table>
      </div>"""

GREEDY_CODE = """visited = [start]                 # ① 行った都市を、行った順に入れるリスト
total = 0
here = start
while len(visited) < count:       # ② まだ行っていない都市がある間、くり返す
    nearest = None
    for j in range(count):
        if j in visited:          # ③ もう行った都市は、候補にしない
            continue
        if nearest is None or table[here][j] < table[here][nearest]:
            nearest = j           # ④ これまでの候補より近ければ、書きかえる
    total = total + table[here][nearest]
    visited.append(nearest)       # ⑤ えらんだ都市を「行った」に足して、そこへ移動する
    here = nearest
total = total + table[here][start]    # ⑥ 最後に出発点へ戻る"""

ex1_body = f"""      <p>第8回と同じ5つの都市に、貪欲法を使います。
      「いまいる都市から、まだ行っていない都市のうちいちばん近いところへ進む」をくり返すだけです。
      最後に、全探索の答え（本当の最短）と比べます。
      演習1では、同じしくみで<strong>ナガシマスパーランドの回りたい場所を、近い順に回る回り方</strong>を作ります。</p>

      <h4 style="margin:1.8rem 0 0.6rem">貪欲法のコードの書き方 ── 6つの大事な行</h4>
      <p>例題1の <code>greedy</code> 関数から、表示のための行を取りのぞくと、次の十数行になります。
      <code>table</code> は第8回で作った距離の表（<code>table[i][j]</code> = i番から j番までの距離）、<code>count</code> は都市の数、<code>start</code> は出発点の番号です。
      演習1（ナガシマスパーランド）でも、「距離」が「歩く時間（分）」に変わるだけで、まったく同じ書き方をしています。</p>
{pycode(GREEDY_CODE, "Python ── 例題1の貪欲法の部分（表示用の行を省いたもの）")}

      <div class="concept-box">
        <h4>①② <code>visited</code> ── 「行った都市」を覚えておくリスト</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>visited</code>（ビジテッド: 「訪れた」という意味）は、行った都市の番号を<strong>行った順に</strong>入れていくリストです。
        はじめは出発点だけの <code>[0]</code> で、1つえらぶたびに <code>append</code>（リストの最後に足す）で1つ増えます。
        <code>len(visited)</code>（リストの長さ = 行った都市の数）が都市の数 <code>count</code> と同じになったら、全部回り終えたので <code>while</code> のくり返しが終わります。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜそう書くか:</strong>
        巡回セールスマン問題には「同じ都市は1回だけ」というきまりがあります。どこへ行ったかを覚えておかないと、いちばん近い2つの都市のあいだを行ったり来たりして、いつまでも終わりません。
        また、このリストは最後に<strong>そのまま答え（回る順番）</strong>になります。</p>
      </div>

      <div class="concept-box">
        <h4>③ <code>if j in visited: continue</code> ── 行った都市は候補から外す</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>j in visited</code> は「j がリスト visited の中にあるか」を調べる書き方で、あれば True（はい）になります。
        <code>continue</code>（コンティニュー）は「この回の残りを飛ばして、次の j へ進む」命令です。
        つまり、もう行った都市は、距離を比べる前に飛ばします。いまいる都市 <code>here</code> も visited に入っているので、自分自身（距離 0）をえらんでしまうこともありません。</p>
      </div>

      <div class="concept-box">
        <h4>④ <code>if nearest is None or table[here][j] &lt; table[here][nearest]</code> ── いちばん近い候補をさがす</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        <code>nearest</code>（ニアレスト: 「いちばん近い」という意味）は、「いまのところいちばん近い候補」の番号です。
        候補を1つずつ見て、<code>table[here][j]</code>（いまいる都市から j までの距離）が、いまの nearest までの距離より小さければ、nearest を j に書きかえます。
        全部の候補を見終わったとき、nearest がいちばん近い都市になっています。
        第1回・第8回の「いまのところ最短」を書きかえていく方法と同じです。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>なぜ <code>nearest is None or</code> が要るか:</strong>
        さがし始めたときは、まだ候補を1つも見ていないので、nearest は <code>None</code>（「まだ何もない」を表す値）です。
        None のまま <code>table[here][None]</code> と書くとエラーになるので、「nearest がまだ None なら、最初の候補をそのまま入れる」と先に書いています。
        <code>or</code> は、左側が True なら右側を調べないので、エラーになりません。</p>
      </div>

      <div class="concept-box">
        <h4>⑤⑥ えらんだ都市へ移動し、最後に出発点へ戻る</h4>
        <p style="font-size:0.95rem"><strong>何をしているか:</strong>
        えらんだ都市までの距離を <code>total</code>（合計）に足し、<code>visited</code> に足し、<code>here</code>（いまいる都市）を書きかえます。これで「移動した」ことになります。
        <code>while</code> が終わったら、最後にいる都市から出発点までの距離 <code>table[here][start]</code> を足します。</p>
        <p style="font-size:0.95rem;margin-top:0.6rem"><strong>全探索とのちがい:</strong>
        全探索は「順番を1つ作る → 合計を計算する」を (n−1)! 回くり返して、いちばん短いものを残しました。
        貪欲法は、<strong>順番を1つだけ</strong>、前から1か所ずつ決めていきます。いちど決めた所は、あとで「やっぱり別の順番にしよう」とやり直しません。
        だから速く、そして最短とはかぎらないのです。</p>
      </div>

      <p style="margin-top:0.8rem">例題1の5都市で、変数がどう変わっていくかを表にすると、次のようになります（緑 = えらんだ候補）。ターミナルの「貪欲法の進み方」と見比べてください。</p>
{trace_table(CITIES[:5], G5_STEPS, G5)}

      <p style="margin-top:1rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 地図</td><td>丸の数字 = 地点の番号（橙の丸 = 出発点）。白い輪 = いまいる所。うすい線と数字 = いまいる所から候補までの距離（演習1では歩く時間）</td></tr>
        <tr><td>白い線</td><td>えらんだ「いちばん近い所」への道。次の手順で、太い緑（通った道）に変わる</td></tr>
        <tr><td>右: 候補の一覧</td><td>まだ行っていない所と、そこまでの距離。緑の行 = えらんだ所。下の「行った順（visited）」が1つずつ増えていく</td></tr>
        <tr><td>最後の画面</td><td>丸の数字が回る順番（S = 出発点）に変わり、右に1本ずつの距離と合計が出る</td></tr>
      </table>

{example_pair('AL2-09-ex1.py', f'貪欲法は「{names(CITIES, G5)}」というルートを作り、合計は<strong>{G5_LEN}</strong>でした。'
     f'全探索で求めた最短も{O5_LEN}なので、<strong>差は0</strong>です。'
     '2つのルートをよく見ると、回る向きが逆になっているだけで、通る道はまったく同じです。'
     '貪欲法がえらんだのは4回で、調べた候補はのべ10か所（4 + 3 + 2 + 1）だけです。全探索は24通りの順番をすべて計算しました。'
     '都市が5個と少ないため、たまたま最短に当たったという点に注意してください。',
     creative=missions1)}
{trouble1}"""

ex2_body = f"""      <p>都市を8個に増やして、貪欲法と全探索を<strong>答えの良さ</strong>と<strong>速さ</strong>の2つで比べます。
      後半では、出発する都市を変えて貪欲法をやり直します。
      演習2では、<strong>演習1の自分の場所</strong>で同じ比較をし、貪欲法が損をする配置をさがします。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>greedy(distance, 0)</code></td><td>例題1と同じ貪欲法。0番から出発して、回る順番と合計距離を返す</td></tr>
        <tr><td><code>brute_force(distance)</code></td><td>第8回と同じ全探索。<code>permutations</code>（並べ方をすべて作る道具）で (n−1)! 通りを試し、いちばん短いものを返す</td></tr>
        <tr><td><code>time.perf_counter()</code></td><td>いまの時刻（秒）。計算の前と後で読んで、差をかかった時間にする（第7・8回と同じ）</td></tr>
        <tr><td><code>difference / best_length * 100</code></td><td>差が、本当の最短の何%にあたるか。最短が 50 で差が 5 なら、5 ÷ 50 × 100 = 10% 長い</td></tr>
        <tr><td><code>for start in range(n): greedy(distance, start)</code></td><td>出発点を0番、1番、…と変えて、貪欲法を n 回やり直す</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左の地図: 橙の線</td><td>貪欲法のルート。→ キーで、えらんだ順に1本ずつ増える</td></tr>
        <tr><td>右の地図: 緑の線</td><td>全探索のルート（本当の最短）。貪欲法の線が全部引けたあと、最後の手順で表示される</td></tr>
        <tr><td>丸の数字</td><td>はじめは地点の番号。ルートができると、回る順番（S = 出発点）に変わる</td></tr>
      </table>

{example_pair('AL2-09-ex2.py', f'貪欲法は<strong>{G8_LEN}</strong>、全探索は<strong>{O8_LEN}</strong>で、差は{round(G8_LEN - O8_LEN, 1)}でした。'
     f'貪欲法のルートは最短ルートより<strong>{P8}%長い</strong>という結果です。'
     '一方で速さは、貪欲法のほうが全探索よりけたちがいに速く、この実行では100倍以上でした（倍率はパソコンや実行のたびに変わります）。'
     '都市が5個のときは同じ答えでしたが、8個になると差が出ています。'
     '後半の表では、出発する都市を変えると合計が大きく変わり、書店から出発したときだけ最短と同じになりました。'
     '全探索の答えは輪なので、どこから出発しても合計は変わりません。貪欲法は、出発点しだいでえらび方が変わるので、答えも変わります。',
     fig_starts(), creative=missions2)}
{trouble2}

{notion('標準課題は、<strong>自分の場所</strong>をメインゲート＋4〜9か所にして演習1を実行し、貪欲法が進む順番を番号つきの矢印で描く。'
        '演習1の窓を → キーで1手順ずつ進めると、1回目・2回目の候補と歩く分が見える。演習2の「全探索の合計」と差、20か所のときの2つの時間も、図の横に書く。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回も、例題（参考）を動かして貪欲法の進み方をつかんだら、
    <strong>クリエイティブ演習</strong>で自分の作品を作ります。題材は <strong>ナガシマスパーランド</strong>（三重県桑名市の遊園地）です。
    演習1で「回りたい場所を、近い順に回る回り方」を貪欲法で作り、演習2で「全探索が見つけた、本当にいちばん早い回り方」と比べます。</p>
    <p style="margin-bottom:1.5rem">ひな形の場所の位置は、下のまん中にメインゲート、左上にスチールドラゴン2000、右上に白鯨（はくげい）、
    左に嵐（あらし）、まん中に大観覧車オーロラ、右にアクロバットがある、という<strong>おおまかな例</strong>です（実際の位置とはちがいます）。
    実際の位置はナガシマスパーランド公式サイトの園内マップを見て、自由に直してかまいません。
    行ったことがない人は、乗り物の名前を公式サイトで調べるか、行ってみたい別の遊園地の場所に書き換えてもかまいません（そのときも、0番は入り口にします）。まず作業フォルダを用意します。</p>

{setup_guide('09', ['AL2-09-ex1.py', 'AL2-09-ex2.py'])}

{pygame_card}

{keywords([
    ('貪欲法', 'どんよくほう / greedy algorithm', '先のことを考えず、その時点でいちばん良さそうな選択をくり返す方法。速いが最適とはかぎらない。'),
    ('最近傍法', 'さいきんぼうほう / nearest neighbor', '巡回セールスマン問題に貪欲法を使ったもの。いまいる場所からいちばん近い場所へ進む。'),
    ('局所最適', 'きょくしょさいてき / local optimum', '部分的にはいちばん良いが、全体で見るといちばん良いとはかぎらない状態。'),
    ('近似解', 'きんじかい / approximate solution', '最適解ではないが、実用上じゅうぶん良い答え。速く求められることが利点。'),
    ('最適解', 'さいてきかい / optimal solution', '考えられる中で本当にいちばん良い答え。全探索や、第10回の動的計画法で求まる。'),
    ('visited', 'ビジテッド / 行った場所のリスト', '行った場所の番号を、行った順に入れていくリスト。同じ場所へ2回行かないために使い、最後は回る順番の答えになる。'),
])}

{example(1, '貪欲法で5都市を回り、ナガシマスパーランドを近い順に回る', ex1_body)}

{example(2, '8都市で全探索と比べ、ナガシマスパーランドで貪欲法の弱点をさがす', ex2_body)}"""


# ── 解答例に載せる、ひな形（書き換える前）の確かめ用の数値 ──
def naga_steps_rows():
    t = table(NAGA)
    rows = []
    for k, (here, cand, nearest) in enumerate(GN_STEPS):
        cands = "　".join(f"{j}番 {t[here][j]}分" for j in cand)
        rows.append(f"          <tr><td>{k + 1}回目</td><td>{NAGA[here][0]}</td><td>{cands}</td>"
                    f"<td><strong>{NAGA[nearest][0]}</strong>（{t[here][nearest]}分）</td></tr>")
    return "\n".join(rows)


def naga_start_rows():
    rows = []
    for name, v in start_results(NAGA):
        rows.append(f"          <tr><td>{name}</td><td>{v}分</td><td>{round(v - ON_LEN, 1)}分</td></tr>")
    return "\n".join(rows)


LV3_START = "アクロバット"
LV3_TOTAL = greedy(NAGA, [s[0] for s in NAGA].index(LV3_START))[1]
POOL = ("ジャンボ海水プール", 0, 14)
NAGA_POOL = NAGA + [POOL]
GP, GP_LEN, _ = greedy(NAGA_POOL)
OP, OP_LEN = optimal(NAGA_POOL)
PP = percent(GP_LEN, OP_LEN)
assert PP >= 10 and LV3_TOTAL > GN_LEN
T_NAGA = table(NAGA)

ans = answers([slide_example("09"),
    ("演習1のひな形（書き換える前）の確かめ用", f"""        <p>ひな形のままの6か所の結果です。自分の場所に書き換えたあとは変わります。</p>
        <table>
          <tr><th></th><th>いまいる場所</th><th>候補と歩く分</th><th>えらんだ場所</th></tr>
{naga_steps_rows()}
          <tr><td>最後</td><td>{NAGA[GN[-1]][0]}</td><td>候補なし</td><td>メインゲートへ戻る（{T_NAGA[GN[-1]][0]}分）</td></tr>
        </table>
        <ul style="margin:0.6rem 0 0 1.2rem;line-height:1.9">
          <li>貪欲法の回り方: {names(NAGA, GN)}（<strong>{GN_LEN}分</strong>）</li>
          <li>えらんだのは5回、調べた候補はのべ15か所（6 × 5 ÷ 2）。全探索なら (6−1)! = 120通り</li>
          <li>Lv3（<code>START</code>）: <code>START = "{LV3_START}"</code> にすると {LV3_TOTAL}分で、0番から出発するより<strong>{round(LV3_TOTAL - GN_LEN, 1)}分おそく</strong>なる。
              ほかの場所から出発したときの合計は、下の演習2の表のとおり</li>
        </ul>"""),
    ("演習2のひな形（書き換える前）の確かめ用", f"""        <ul style="margin-left:1.2rem;line-height:1.9">
          <li>貪欲法: {names(NAGA, GN)}（<strong>{GN_LEN}分</strong>）</li>
          <li>全探索: {names(NAGA, ON)}（<strong>{ON_LEN}分</strong>）</li>
          <li>貪欲法は {round(GN_LEN - ON_LEN, 1)}分おそい（<strong>{PN}%</strong> 長い）。ちがいは最後の2か所の順番だけ。
              貪欲法は大観覧車オーロラから近いアクロバット（{T_NAGA[4][5]}分）を先にえらんだため、最後に白鯨からメインゲートまでの長い道（{T_NAGA[2][0]}分）が残った</li>
        </ul>
        <table>
          <tr><th>出発する場所</th><th>貪欲法の合計</th><th>いちばん早い回り方との差</th></tr>
{naga_start_rows()}
        </table>
        <p style="margin-top:0.6rem"><strong>Lv3 の例:</strong> ひな形に <code>("{POOL[0]}", {POOL[1]}, {POOL[2]}),</code>（左下のすみに1か所だけ離れた場所）を足すと、
        貪欲法は {GP_LEN}分、全探索は {OP_LEN}分で、<strong>{PP}%</strong> おそくなります。貪欲法は近い場所を先に回り、離れたプールを最後まで残すためです。
        ほかにも、場所を1つ動かすだけで10%をこえる配置がいくつもあります。</p>
        <p style="margin-top:0.6rem">かかった時間・速さの倍率・見積もりは、パソコンによって変わります。
        20か所のとき、貪欲法は 0.0001秒より短く、全探索の見積もりは数百年〜千年以上になるのがふつうです。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "貪欲法とは", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("09", SLIDES),
    advanced_section("09"),
    rubric_section("09"),
    ans,
])

write("09", NAV, body)
