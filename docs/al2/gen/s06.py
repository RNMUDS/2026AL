# -*- coding: utf-8 -*-
"""第6回: ダイクストラ法（2）実装入門 の本文を組み立てる。
例題は「参考（heapq の使い方・新宿の路線図）」と「クリエイティブ演習（ディズニーランドの待ち時間ボードと地図）」の2本立て。"""
import heapq

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
INF = float("inf")


def trace_q(start="新宿"):
    """heapq 版のダイクストラ法を動かし、heappop ごとの
    (取り出した組, 確定か読み飛ばしか, 取り出す前の箱の中身, [(駅, 前の値, 新しい値, 区間の時間)], 取り出した後に入れ終わった箱の中身) を返す。"""
    dist = {s: INF for s in RAIL}
    dist[start] = 0
    queue = [(0, start)]
    settled = set()
    rows = []
    while queue:
        before = list(queue)
        d, cur = heapq.heappop(queue)
        if cur in settled:
            rows.append(((d, cur), "skip", before, [], list(queue)))
            continue
        settled.add(cur)
        changes = []
        for name, w in RAIL[cur]:
            if name not in settled and d + w < dist[name]:
                changes.append((name, dist[name], d + w, w))
                dist[name] = d + w
                heapq.heappush(queue, (d + w, name))
        rows.append(((d, cur), "settle", before, changes, list(queue)))
    return rows


def fig_heap_rule():
    heap = [1, 3, 2, 8, 9, 5]
    pos = {0: (430, 92), 1: (330, 168), 2: (530, 168),
           3: (280, 244), 4: (380, 244), 5: (480, 244)}
    pairs = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'heapq が守っているたった1つのきまり: 親は必ず子より小さいか同じ</text>']
    # 左: リストとしての中身
    s.append(f'        <text x="118" y="86" text-anchor="middle" fill="{GRAY}" font-size="12">リストとしての中身</text>')
    for i, v in enumerate(heap):
        y = 104 + i * 34
        s.append(f'        <rect x="40" y="{y}" width="46" height="28" rx="6" fill="#141414" stroke="#444"/>')
        s.append(f'        <text x="63" y="{y+19}" text-anchor="middle" fill="#ccc" font-size="13">{v}</text>')
        s.append(f'        <text x="100" y="{y+19}" fill="#666" font-size="10">← {i}番目</text>')
    s.append(f'        <text x="118" y="{104+6*34+16}" text-anchor="middle" fill="{GRAY}" font-size="10">'
             '並びはバラバラに見える</text>')
    # 右: 木としての形
    s.append(f'        <text x="430" y="52" text-anchor="middle" fill="{GRAY}" font-size="12">同じ中身を木の形に描いたもの</text>')
    for a, b in pairs:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        s.append(f'        <line x1="{x1}" y1="{y1+20}" x2="{x2}" y2="{y2-20}" stroke="#555" stroke-width="2"/>')
    for i, v in enumerate(heap):
        x, y = pos[i]
        s.append(f'        <circle cx="{x}" cy="{y}" r="21" fill="#1A1A1A" stroke="{GREEN if i == 0 else "#555"}" stroke-width="2"/>')
        s.append(f'        <text x="{x}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="14" font-weight="700">{v}</text>')
        s.append(f'        <text x="{x}" y="{y-27}" text-anchor="middle" fill="#666" font-size="9">{i}番目</text>')
    # 親子の関係を順に光らせる
    for k, (a, b) in enumerate(pairs):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        p0, p1 = k / len(pairs), (k + 1) / len(pairs)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                f'keyTimes="0;{p0:.3f};{p0+0.01:.3f};{p1-0.02:.3f};{p1:.3f};1" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <line x1="{x1}" y1="{y1+20}" x2="{x2}" y2="{y2-20}" stroke="{AMBER}" stroke-width="4"/>')
        s.append(f'          <circle cx="{x1}" cy="{y1}" r="21" fill="none" stroke="{AMBER}" stroke-width="3"/>')
        s.append(f'          <circle cx="{x2}" cy="{y2}" r="21" fill="none" stroke="{AMBER}" stroke-width="3"/>')
        s.append(f'          <text x="430" y="298" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">'
                 f'親 {heap[a]} ＜ 子 {heap[b]}　きまりを守っている</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="326" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'きまりのおかげで、いちばん小さい数は必ず0番目にある。だから先頭を見るだけで最小が分かる</text>')
    return fig(700, 342, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 最小をさがす作業の違い
# ────────────────────────────────────────────────────────────
def fig_find_min():
    values = [24, 7, 31, 12, 45, 9, 38, 16, 52, 3, 27, 19]
    n = len(values)
    dur = 10
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '「いちばん小さいもの」をさがす作業のちがい</text>']
    # 左: 全部見る
    s.append(f'        <text x="175" y="56" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">第5回のやり方: 全部見る</text>')
    for i, v in enumerate(values):
        x = 34 + (i % 4) * 72
        y = 76 + (i // 4) * 40
        s.append(f'        <rect x="{x}" y="{y}" width="60" height="30" rx="6" fill="#141414" stroke="#444"/>')
        s.append(f'        <text x="{x+30}" y="{y+20}" text-anchor="middle" fill="#ccc" font-size="12">{v}</text>')
        a = 0.7 * i / n
        s.append(f'        <rect x="{x}" y="{y}" width="60" height="30" rx="6" fill="none" stroke="{AMBER}" stroke-width="2.5" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{a:.3f};{a+0.005:.3f};{a+0.05:.3f};{a+0.055:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    s.append(f'        <text x="175" y="212" text-anchor="middle" fill="{AMBER}" font-size="12">'
             f'{n}個あれば{n}回調べる（頂点がn個なら n 回）</text>')
    s.append('        <line x1="350" y1="46" x2="350" y2="232" stroke="#333" stroke-width="1"/>')
    # 右: heapq
    s.append(f'        <text x="525" y="56" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">第6回のやり方: heapq に任せる</text>')
    s.append(f'        <rect x="430" y="76" width="60" height="30" rx="6" fill="#1a2e0a" stroke="{GREEN}" stroke-width="2.5"/>')
    s.append(f'        <text x="460" y="96" text-anchor="middle" fill="#93D500" font-size="12" font-weight="700">3</text>')
    s.append(f'        <text x="500" y="96" fill="{GREEN}" font-size="11">← 先頭を見るだけ</text>')
    for i, v in enumerate([7, 9, 12, 16, 19, 24, 27, 31]):
        x = 400 + (i % 4) * 66
        y = 126 + (i // 4) * 36
        s.append(f'        <rect x="{x}" y="{y}" width="54" height="26" rx="5" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="{x+27}" y="{y+18}" text-anchor="middle" fill="#666" font-size="11">{v}</text>')
    s.append(f'        <text x="525" y="212" text-anchor="middle" fill="{GREEN}" font-size="12">'
             '取り出したあとの並べ直しも、100万個で20回程度</text>')
    s.append(f'        <text x="350" y="252" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '頂点が100万個あるとき、全部見る方法は100万回。heapq なら20回程度</text>')
    return fig(700, 268, "\n".join(s))




# ────────────────────────────────────────────────────────────
# 図3: heapq 版のダイクストラ法を、heappop 1回ずつたどる
# ────────────────────────────────────────────────────────────
def fig_trace_q():
    rows = trace_q()
    row_h = 58
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'heapq 版のダイクストラ法で 新宿 から各駅までの時間を求める（heappop 7回）</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '左 = 取り出す前の queue の中身（緑 = 先頭 = 次に取り出される組）、右 = 取り出した組をどうしたか</text>']
    for k, (popped, kind, before, changes, after) in enumerate(rows, 1):
        y0 = 62 + (k - 1) * row_h
        s.append(f'        <text x="14" y="{y0+22}" fill="#E0E0E0" font-size="12" font-weight="700">{k}回目</text>')
        x = 62
        for i, (m, st) in enumerate(before):
            w = 62 if m < 10 else 68
            first = i == 0
            s.append(f'        <rect x="{x}" y="{y0+6}" width="{w}" height="24" rx="5" '
                     f'fill="{"#1a2e0a" if first else "#141414"}" stroke="{GREEN if first else "#3a3a3a"}" stroke-width="{2 if first else 1}"/>')
            s.append(f'        <text x="{x+w/2}" y="{y0+22}" text-anchor="middle" fill="{"#93D500" if first else "#999"}" '
                     f'font-size="11"{" font-weight=" + chr(34) + "700" + chr(34) if first else ""}>({m}, {st})</text>')
            x += w + 4
        tx = 360
        if kind == "skip":
            s.append(f'        <text x="{tx}" y="{y0+22}" fill="{RED}" font-size="12" font-weight="700">'
                     f'({popped[0]}, {popped[1]}) → {popped[1]} はもう確定済み → 読み飛ばす</text>')
            s.append(f'        <text x="{tx}" y="{y0+40}" fill="{GRAY}" font-size="11">'
                     f'{popped[1]} は先に小さい組で確定している。この {popped[0]}分 は古い時間</text>')
        else:
            s.append(f'        <text x="{tx}" y="{y0+22}" fill="#E0E0E0" font-size="12" font-weight="700">'
                     f'({popped[0]}, {popped[1]}) → {popped[1]} を {popped[0]}分で確定</text>')
            if changes:
                parts = []
                for n, old, new, w in changes:
                    parts.append(f"{n} {old}→{new}" if old != INF else f"{n} {new}")
                rewrite = any(old != INF for _, old, _, _ in changes)
                s.append(f'        <text x="{tx}" y="{y0+40}" fill="{AMBER if rewrite else "#bbb"}" font-size="11"'
                         f'{" font-weight=" + chr(34) + "700" + chr(34) if rewrite else ""}>'
                         f'queue に入れる: {"、".join(parts)}</text>')
            else:
                s.append(f'        <text x="{tx}" y="{y0+40}" fill="{GRAY}" font-size="11">'
                         '入れるものなし（となりは確定済みか、表の時間のほうが短い）</text>')
        if k < len(rows):
            s.append(f'        <line x1="14" y1="{y0+row_h-6}" x2="686" y2="{y0+row_h-6}" stroke="#2a2a2a"/>')
    y = 62 + len(rows) * row_h + 8
    s.append(f'        <text x="350" y="{y}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '品川は (30, 品川) と (16, 品川) の2回 queue に入った。16 が先に出て確定し、最後に出た 30 は読み飛ばされた</text>')
    return fig(700, y + 16, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "heapqとは #sec-explanation",
    "例題と演習 #sec-examples",
    "標準課題 #sec-slides nav-assignment",
    "発展課題 #sec-advanced",
    "提出と評価 #sec-submit",
    "解答 #answers-section",
]

sub = slide_submission("06")

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第5回のダイクストラ法は、①②③（選ぶ・確定する・書き直す）のくり返しでした。
      このうち①の「まだ確定していない場所のうち、時間がいちばん小さい場所を選ぶ」では、
      <strong>毎回すべての場所を1つずつ見て</strong>くらべていました。
      第5回の地図は小さいので一瞬で終わりましたが、場所が10個なら1回選ぶのに10個、全部確定させるまでに 10 × 10 = 100回 見ます。
      交差点が10万個ある道路地図（カーナビ）なら、10万 × 10万 = 100億回です。
      第6回は、この①を速くする道具 <strong>heapq</strong>（ヒープキュー）を覚えて、ダイクストラ法を書き直します。
      答えは第5回とまったく同じで、①のやり方だけが変わります。
    </p>

    <div class="analogy">
      ディズニーランドで「いま待ち時間がいちばん短いアトラクションに行きたい」とします。
      毎回、園内のアトラクションを全部見て回って待ち時間をくらべるのは大変です。
      待ち時間の札を<strong>専用の箱</strong>に入れておくと、箱から取り出すと必ず待ち時間がいちばん短い札が出てくる、
      というしくみがあれば、見て回る必要はありません。
      この「いちばん小さいものがすぐ取り出せる箱」が<strong>優先度付きキュー</strong>で、Python では <code>heapq</code> という道具で使えます。
      今回のクリエイティブ演習1では、この箱を使って「待ち時間の短い順に回る待ち時間ボード」を作ります。
    </div>

{fig_find_min()}

    <div class="concept-box">
      <h4>heapq の3つの命令</h4>
      <table>
        <tr><th>命令</th><th>すること</th></tr>
        <tr><td><code>heapq.heappush(箱, 値)</code></td><td>箱に値を1つ入れる</td></tr>
        <tr><td><code>heapq.heappop(箱)</code></td><td>箱の中でいちばん小さい値を取り出す（箱からは消える）</td></tr>
        <tr><td><code>箱[0]</code></td><td>取り出さずに、いちばん小さい値を見るだけ</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        箱として使うのは、ふつうの Python のリストです（<code>import heapq</code> と書いてから使います）。
        ただし、リストの中身を <code>append()</code> などで直接いじると、下の「きまり」が崩れて正しく動かなくなります。
        箱に入れるときは <code>heappush</code>、取り出すときは <code>heappop</code> だけを使ってください。
      </p>
    </div>

{fig_heap_rule()}

    <div class="concept-box">
      <h4>組（タプル）を入れると、1番目の数でくらべる</h4>
      <p style="font-size:0.95rem">
        箱には <code>(40, "ビッグサンダー・マウンテン")</code> や <code>(16, "品川")</code> のような<strong>組</strong>（タプル: <code>( )</code> で囲んで並べた値のまとまり）も入れられます。
        組どうしは<strong>1番目の値</strong>でくらべるので、待ち時間や時間を先に書けば、その小さい順に取り出せます。
        1番目が同じときは、2番目の値（名前）でくらべます。名前の文字どうしは、文字に付いている番号（文字コード）の小さい順です。カタカナどうしなら、だいたい「アイウエオ順」になります。
      </p>
      <table style="margin-top:0.6rem">
        <tr><th>くらべる2つの組</th><th>小さいほう</th><th>理由</th></tr>
        <tr><td><code>(16, "品川")</code> と <code>(30, "品川")</code></td><td><code>(16, "品川")</code></td><td>1番目の 16 ＜ 30</td></tr>
        <tr><td><code>(20, "ホーンテッドマンション")</code> と <code>(20, "カリブの海賊")</code></td><td><code>(20, "カリブの海賊")</code></td><td>1番目が同じなので2番目でくらべる。「カ」は「ホ」より前</td></tr>
      </table>
    </div>

    <h3 style="margin:2rem 0 0.8rem">heapq を使ったダイクストラ法</h3>
    <p style="margin-bottom:1rem">
      第5回のダイクストラ法を、heapq を使う形に書き直します。箱の名前は <code>queue</code>（キュー: 待ち行列）にして、
      <code>(その駅までの時間, 駅名)</code> の組を入れます。変わるのは次の3か所です。
    </p>
    <div class="concept-box">
      <table>
        <tr><th></th><th>第5回（全部見る）</th><th>第6回（heapq）</th></tr>
        <tr><td>① 選ぶ</td><td>まだ確定していない場所を <code>for</code> で全部見て、いちばん小さい場所をさがす</td><td><code>heapq.heappop(queue)</code> の1行で、時間がいちばん小さい組を取り出す</td></tr>
        <tr><td>③ 書き直す</td><td>距離表 <code>distance</code> を書き直すだけ</td><td>書き直したら、<code>(新しい時間, 駅名)</code> の組を <code>heappush</code> で queue にも入れる</td></tr>
        <tr><td>取り出した駅が確定済みのとき</td><td>（起きない）</td><td><strong>読み飛ばす</strong>（下で説明）</td></tr>
        <tr><td>終わるとき</td><td>全部の駅が確定したとき</td><td>queue が空っぽになったとき</td></tr>
      </table>
    </div>

{fig_trace_q()}

    <div class="concept-box">
      <h4>確定済みの駅が、もう一度出てくることがある（読み飛ばし）</h4>
      <p style="font-size:0.95rem">
        heapq 版では、同じ駅が queue に<strong>何度も入る</strong>ことがあります。
        品川は、1回目の heappop で新宿を確定したときに <code>(30, 品川)</code> として入り、
        2回目で渋谷を確定したときに、もっと短い <code>(16, 品川)</code> としてもう一度入りました。
        箱の中の古い <code>(30, 品川)</code> は消さずに残しておきます（箱の途中の組を消すのは手間がかかるため）。
        小さい順に取り出すので、先に <code>(16, 品川)</code> が出てきて品川が確定し、
        最後に出てくる <code>(30, 品川)</code> は、もう確定した駅の古い時間なので<strong>読み飛ばします</strong>。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        読み飛ばさずに進めると、確定済みの駅をもう一度「確定」と表示し、そのとなりを調べ直す<strong>むだな作業</strong>が起きます
        （古い時間は大きいので距離表は書き直されず、答えは変わりませんが、表示がおかしくなり、作業も増えます）。
        読み飛ばしは、同じ駅の組を2回目以降に queue に入れたとき、つまり<strong>時間の書き直し</strong>があったときに、その回数だけ起きます。
      </p>
    </div>"""

pygame_card = f"""    <div class="card" style="border-left:4px solid #76B900;margin-bottom:2rem">
      <div class="card-header">
        <span class="tag" style="background:#1a2e0a;color:#76B900">準備</span>
        <h3>heapq の箱と距離表を絵で表示する道具（pygame）</h3>
      </div>
      <p style="font-size:0.95rem">今回の例題と演習も、第2〜5回と同じく <strong>pygame</strong>（パイゲーム: Python で絵やゲームの画面を作る道具）の窓で表示します。
      例題1・演習1は heapq の箱の中身を<strong>木の形とリスト</strong>で、例題2・演習2は<strong>グラフと queue と距離表</strong>を並べて見せます。</p>
      <div class="setup-step">
        <p class="step-title">1. pygame が入っているか確かめる</p>
        <p style="font-size:0.95rem">第2〜5回で入れた人は、そのまま使えます。VS Code の「ターミナル」→「新しいターミナル」で次の1行を打ちこみ、Enter を押します。
        <code>2.6.1</code> のような数字が出れば入っています。</p>
{plain('py -c "import pygame; print(pygame.version.ver)"', "ターミナル（Windows）")}
        <p style="font-size:0.95rem;margin-top:0.6rem"><code>ModuleNotFoundError</code> と出たら、まだ入っていません。次の1行で入れます
        （うまくいかないときは<a href="session02.html#sec-examples" style="color:#76B900">第2回の「うまくいかないとき」の表</a>を見る）。</p>
{plain("pip install pygame", "ターミナル（Windows）")}
        <p style="font-size:0.9rem;color:#888;margin-top:0.6rem">Mac の人は <code>pip</code> のかわりに <code>pip3</code>、<code>py</code> のかわりに <code>python3</code> と打つ。</p>
      </div>
      <div class="setup-step">
        <p class="step-title">2. 窓の操作（第2〜5回と同じ）</p>
        <table>
          <tr><th>キー</th><th>動き</th></tr>
          <tr><td>スペース</td><td>自動で再生／一時停止</td></tr>
          <tr><td>→（右矢印）</td><td>1手順だけ進める（例題2・演習2では、heappop 1回ぶん。標準課題の図を描くときに便利）</td></tr>
          <tr><td>R</td><td>最初からやり直す</td></tr>
          <tr><td>Esc または窓の × </td><td>終わる（窓を閉じるとプログラムも終わる）</td></tr>
        </table>
        <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">窓に絵を描くコードは、各ファイルの<strong>いちばん下</strong>
        （「ここから下は、…pygame の窓に…表示するための道具です」と書いた行より下）に入っています。そこは読まなくてかまいません。
        ファイルは1つだけで動きます。ターミナルに結果が出たあとで窓が開きます。窓が見当たらないときは、タスクバー（Mac は Dock）を見てください。</p>
      </div>
    </div>"""

trouble1 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習1）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>SyntaxError</code><br>（<code>Perhaps you forgot a comma?</code> など）</td><td>カンマ・かっこ・<code>"</code> の閉じ忘れ。<code>(40, "名前")</code> の組と組のあいだにカンマ、行の最後にもカンマ。エラーに出た行と、その1つ上の行を見る</td></tr>
          <tr><td><code>waits の … がおかしい</code></td><td><code>("名前", 40)</code> のように順番が逆か、待ち時間を <code>"40"</code> のように <code>" "</code> で囲んだか、<code>40.5</code> のような小数にした。<code>(40, "名前")</code> の順に書く（待ち時間でくらべるので、待ち時間が先）</td></tr>
          <tr><td>ひとことの所に <code>None</code> と出る</td><td><code>comment</code> の中に <code>return</code> しない分岐がある（<code>else</code> を消した、<code>return</code> のかわりに <code>print</code> と書いた など）。どの分岐でも <code>return "…"</code> で文字を返し、最後は <code>else</code> にする</td></tr>
          <tr><td><code>waits に「○○」が2回ある</code></td><td>同じアトラクションを2回書いた。待ち時間が変わったことは <code>news</code> で表す</td></tr>
          <tr><td><code>news の「○○」が waits にない</code></td><td><code>waits</code> を書き換えたのに <code>news</code> にひな形の名前（プーさんのハニーハント）が残っている、または名前の打ちまちがい。<code>waits</code> に書いた名前と1文字もちがわないようにする</td></tr>
          <tr><td><code>news の … の数がおかしい</code></td><td>乗った数が大きすぎるか、マイナス。乗った数は <code>0</code>〜（アトラクションの数 − 1）で書く</td></tr>
          <tr><td>「短くなっていないので入れない」と出て、読み飛ばしが出ない</td><td>お知らせの待ち時間が、元の待ち時間以上になっている。元より<strong>短い</strong>待ち時間にする</td></tr>
          <tr><td>「もう乗ったので使わない」と出る</td><td>お知らせが来る前に、そのアトラクションに乗ってしまった。乗った数を小さくするか、元の待ち時間を長くする</td></tr>
        </table>
      </div>"""

trouble2 = """      <div class="concept-box" style="margin-top:1rem">
        <h4>うまくいかないとき（演習2）</h4>
        <table>
          <tr><th>出たもの</th><th>原因と直し方</th></tr>
          <tr><td><code>park に「○○」の行がない</code></td><td>足した場所の行（<code>"○○": [ ... ],</code>）を書き忘れたか、名前の打ちまちがい。行を足すか、名前をそろえる</td></tr>
          <tr><td><code>SyntaxError</code></td><td>カンマ・かっこ・<code>"</code> の閉じ忘れ。第5回から貼りかえたときに、<code>park = {</code> の行や最後の <code>}</code> を消していないか確かめる</td></tr>
          <tr><td><code>A の行に（B, 3）があるのに、B の行に（A, 3）がない</code></td><td>道を片方の行にしか書いていないか、行きと帰りで時間がちがう。両方の行に同じ時間で書く（第5回と同じ）</td></tr>
          <tr><td><code>goal の「○○」が park にない</code><br><code>start の「○○」が park にない</code></td><td>名前の打ちまちがい。<code>park</code> に書いた名前と1文字もちがわないようにする</td></tr>
          <tr><td><code>where の「○○」が park にない</code></td><td><code>park</code> を貼りかえたのに、<code>where</code> に古い名前が残っている。<code>where</code> も第5回の自分のものに貼りかえる</td></tr>
          <tr><td>時間が第5回の演習1とちがう</td><td>貼りかえた <code>park</code> や <code>closed</code> が第5回とちがっていないか確かめる（同じ地図なら、必ず同じ時間になる）</td></tr>
        </table>
      </div>"""

missions1 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習1のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分のボード</td><td><code>waits</code> を、自分が乗りたいアトラクション<strong>6つ以上</strong>と、自分で決めた待ち時間にする。<code>TITLE</code> も自分の題名にする。
              <code>news</code> の名前も、自分の <code>waits</code> の名前に直す（まだ決めないなら <code>news = []</code> にして、Lv3 で足す）。
              窓の木で、どの親も子より小さいか同じになっていることを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>同じ待ち時間</td><td>待ち時間が<strong>同じ</strong>アトラクションを2つ作る。どちらが先に出てくるかを<strong>先に予想してから</strong>実行して確かめる（1章の「組（タプル）を入れると…」）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>お知らせ</td><td><code>news</code> にお知らせを足して、「読み飛ばす」の行を<strong>2回以上</strong>出す（ひな形はいま1回）。
              コツ: まだ乗っていない、待ち時間の長いアトラクションを、早いうちに短くする</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv4</strong><br>ひとこと</td><td><code>comment</code> 関数で、待ち時間 <code>minutes</code> によって<strong>3通り以上</strong>のちがうひとことを返す（<code>if</code> / <code>elif</code> / <code>else</code>）</td></tr>
        </table>
{plain('''news = [
    (2, 10, "プーさんのハニーハント"),
    (3, 30, "美女と野獣"),            # ← 3つ乗ったところで、美女と野獣が 60分 → 30分 に
]''', "Lv3 の例: お知らせを2つにする")}
      </div>"""

missions2 = f"""      <div class="concept-box" style="margin-top:0.6rem">
        <h4>演習2のミッション（★ の部分を書き換える）</h4>
        <table>
          <tr><th>レベル</th><th>やること</th></tr>
          <tr><td style="white-space:nowrap"><strong>Lv1</strong><br>自分の地図</td><td><code>park</code>・<code>where</code>・<code>closed</code> を、<strong>第5回の演習1で作った自分の地図</strong>に貼りかえる（<code>AL2/No05/AL2-05-ex1.py</code> からコピーする）。
              ターミナルの最短時間が、第5回の演習1の最後の時間と<strong>同じ</strong>になることを確かめる</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv2</strong><br>読み飛ばし</td><td>「読み飛ばす」の行を<strong>4回以上</strong>出す（ひな形はいま3回）。
              読み飛ばしは、時間の書き直しがあった場所の数だけ起きるので、「まっすぐ行くより寄り道したほうが早い」道を足す（第5回の Lv2 と同じコツ）</td></tr>
          <tr><td style="white-space:nowrap"><strong>Lv3</strong><br>案内文</td><td><code>goal</code> を行きたい場所にして、<code>announce</code> 関数の <code>print</code> を書き換え、自分らしい案内文にする。
              使える材料: <code>route</code>（通る場所の並び）、<code>minutes</code>（合計時間）、<code>len(route)</code>（通る場所の数）</td></tr>
        </table>
      </div>"""

ex1_body = f"""      <p>例題1（参考）は、<code>heapq</code> の箱に数や <code>(時間, 駅名)</code> の組を入れて、取り出す順番を確かめるプログラムです。
      窓では、箱の中身を<strong>木の形</strong>（1章の図「heapq が守っているきまり」と同じ形）と<strong>リスト</strong>で並べて、1手順ずつ見せます。
      演習1では、同じしくみで<strong>待ち時間の短い順に回る、自分の待ち時間ボード</strong>を作ります。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>heapq.heappush(numbers, value)</code></td><td>箱に1つ入れる。入れたあとも「先頭がいちばん小さい」が保たれるように、heapq が中身を並べかえる</td></tr>
        <tr><td><code>numbers[0]</code></td><td>取り出さずに、先頭（いちばん小さい数）を見る</td></tr>
        <tr><td><code>smallest = heapq.heappop(numbers)</code></td><td>いちばん小さい数を取り出す。箱からは消える</td></tr>
        <tr><td><code>minutes, station = heapq.heappop(tasks)</code></td><td>取り出した組を、時間と駅名の2つに分けて受け取る</td></tr>
        <tr><td><code>record(…)</code></td><td>窓に表示するために、そのときの箱の中身を写して残す（アルゴリズムには関係ない）</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: 木の形</td><td><code>[0]</code> がいちばん上、その子が <code>[1]</code> と <code>[2]</code>、<code>[1]</code> の子が <code>[3]</code> と <code>[4]</code>…。緑 = 先頭（次に取り出されるもの）、橙 = いま入れたもの</td></tr>
        <tr><td>右上: リストとしての中身</td><td>Python のリストに入っている本当の並び。木の <code>[番号]</code> と同じ順</td></tr>
        <tr><td>右下: 取り出した順</td><td>heappop で取り出したものを、取り出した順に並べたもの。小さい順になっている</td></tr>
      </table>

{example_pair('AL2-06-ex1.py', '8, 3, 5, 1, 9, 2 の順に入れたのに、取り出す順番は 1, 2, 3, 5, 8, 9 と小さい順になりました。'
     '入れ終わったときの中身 <code>[1, 3, 2, 8, 9, 5]</code> は小さい順に並んでいませんが、'
     '<strong>先頭だけは必ずいちばん小さい数</strong>になっています。窓の木で見ると、どの親も子より小さくなっています。'
     '後半では <code>(16, "品川")</code> のような組を入れており、1番目の要素である時間が小さい順に出てきています。'
     'ダイクストラ法では、この形をそのまま使います。',
     creative=missions1)}
{trouble1}

{notion('標準課題の①②は、演習1の<strong>自分の待ち時間ボード</strong>を使う。'
        'ターミナルの「箱の中身（リストの並び）」を、<code>[0]</code> を上にした木の形に描きかえる。窓を → キーで進めて、'
        '6つ入れ終わった画面の木と見比べるとよい。取り出した順は、ターミナルの「○番目」と「読み飛ばす」の行を写す。')}"""

ex2_body = f"""      <p>例題2（参考）は、第5回の例題1と同じ新宿の路線図を、<strong>heapq を使うダイクストラ法</strong>で解くプログラムです。
      1章の図「heapq 版のダイクストラ法で…」と同じことを、ターミナルと窓に表示します。
      演習2では、<strong>第5回で作った自分のディズニー地図</strong>を heapq 版で解き直し、同じ答えになることを確かめます。
      なお、時間が同じ場所がいくつかあるときは、確定の<strong>順番</strong>が第5回と入れかわることがあります
      （第5回は <code>park</code> に先に書いた場所から、heapq は組の2番目の名前の順）。最後の時間は必ず同じです。</p>

      <table>
        <tr><th>コードの部分</th><th>やっていること</th></tr>
        <tr><td><code>queue = [(0, start)]</code></td><td>箱に、出発点の組 <code>(0, 新宿)</code> だけを入れて始める</td></tr>
        <tr><td><code>minutes, current = heapq.heappop(queue)</code></td><td>①: 時間がいちばん小さい組を取り出す（第5回の「全部見てさがす」<code>for</code> の代わり）</td></tr>
        <tr><td><code>if current in settled:</code> … <code>continue</code></td><td>取り出した駅がもう確定済みなら、古い組なので読み飛ばして次を取り出す</td></tr>
        <tr><td><code>settled.add(current)</code></td><td>②: 確定する</td></tr>
        <tr><td><code>heapq.heappush(queue, (new_distance, name))</code></td><td>③: 時間を書き直したら、その組を箱に入れる（同じ駅の古い組は箱に残ったまま）</td></tr>
        <tr><td><code>while len(queue) &gt; 0:</code></td><td>箱が空っぽになるまでくり返す</td></tr>
      </table>

      <p style="margin-top:0.8rem">窓の読み方は次のとおりです。</p>
      <table>
        <tr><th>窓に表示されるもの</th><th>読み方</th></tr>
        <tr><td>左: グラフ</td><td>丸の外の数字 = 距離表の時間。白い枠 = いま確定した場所、<strong>赤い枠 = いま読み飛ばした場所</strong>、緑 = 確定済み、橙 = 時間が書かれたがまだ確定していない場所。
            橙の線 = 書き直して queue に入れた道。赤い点線 = 通行止め</td></tr>
        <tr><td>右上: queue（heapq の箱）</td><td>箱の中身を、リストの並び順のまま札にしたもの。緑の札（先頭）が、次に取り出される組。同じ場所の札が2枚あれば、あとで読み飛ばしが起きる</td></tr>
        <tr><td>右: 距離表</td><td>確定した場所の行は緑。この手順で変わった時間は <code>30分 → 16分</code> のように橙で出る</td></tr>
        <tr><td>右下</td><td>何回目の heappop で、どの組を取り出して、どうしたか。最後の画面には、heappop の回数と読み飛ばしの回数が出る</td></tr>
      </table>

{example_pair('AL2-06-ex2.py', '取り出した順番は (0分, 新宿) → (7分, 渋谷) → (9分, 池袋) → (16分, 品川) → (21分, 上野) → (27分, 東京) で、'
     '第5回の例題1で確定した順番と時間にまったく同じです。'
     'いちばん最後に <strong>(30分, 品川) → すでに確定済みなので読み飛ばす</strong> と表示されています。'
     '品川は最初に30分として箱に入れられ、渋谷を確定したときに16分として入れ直されました。'
     '16分のほうが先に取り出されて確定したので、残っていた30分の組は読み飛ばされています。'
     '道順（<code>came_from</code>）も第5回の例題2と同じです。',
     creative=missions2)}
{trouble2}

{notion('標準課題の③は、演習2の<strong>自分の地図</strong>を使う。ターミナルの「読み飛ばす」の行を1つ選び、'
        '同じ場所が「queue に入れた」「書き直して queue に入れた」と出ている2つの行をさがす。'
        '窓を → キーで進めると、右上の queue に同じ場所の札が2枚並ぶ手順が見つかる。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">今回も、例題（参考）を動かして heapq とダイクストラ法の進み方をつかんだら、
    <strong>クリエイティブ演習</strong>で、第5回に続いてディズニーランドを題材に自分の作品を作ります。
    演習1で「待ち時間の短い順に回る待ち時間ボード」を作り、演習2で第5回の自分の地図を heapq 版のダイクストラ法で解き直します。</p>
    <p style="margin-bottom:1.5rem">演習1のアトラクションと待ち時間はひな形の例です。待ち時間は、自分の感覚で決めても、
    東京ディズニーリゾート公式アプリの待ち時間を見て決めてもかまいません。
    演習2のひな形の地図は第5回と同じです（東京ディズニーリゾート公式ブログ
    「<a href="https://www.tokyodisneyresort.jp/tdrblog/detail/190415/" style="color:#76B900" target="_blank" rel="noopener">開園当時のマップをご紹介</a>」の、今のマップをもとにしたもの）。
    まず作業フォルダを用意します。</p>

{setup_guide('06', ['AL2-06-ex1.py', 'AL2-06-ex2.py'])}

{pygame_card}

{keywords([
    ('優先度付きキュー', 'ゆうせんどつきキュー / priority queue', '入れたものの中から、いつでも「いちばん小さいもの」を速く取り出せる入れもの。'),
    ('heapq', 'ヒープキュー', 'Python で優先度付きキューを使うための道具。<code>import heapq</code> と書いて使う。箱はふつうのリスト。'),
    ('heappush', 'ヒーププッシュ', '<code>heapq.heappush(箱, 値)</code> で、箱に値を1つ入れる。'),
    ('heappop', 'ヒープポップ', '<code>heapq.heappop(箱)</code> で、箱の中のいちばん小さい値を取り出す。'),
    ('組（タプル）', 'tuple', '<code>(16, "品川")</code> のように <code>( )</code> で囲んだ値のまとまり。くらべるときは1番目の値から順にくらべる。'),
    ('読み飛ばし', 'skip', '箱から取り出した場所がすでに確定しているとき、古い組なので何もせず次を取り出すこと。heapq 版のダイクストラ法で必要になる。'),
])}

{example(1, 'heapq の箱を確かめて、自分の待ち時間ボードを作る', ex1_body)}

{example(2, 'heapq 版のダイクストラ法で、自分の地図を解き直す', ex2_body)}"""

ans = answers([slide_example("06"),
    ("演習1のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの待ち時間ボードで、入れ終わったときの箱の中身と、取り出した順です。自分のボードに書き換えたあとは変わります。</p>
        <p><strong>箱の中身（リストの並び）</strong>: [0] (15, イッツ・ア・スモールワールド)、[1] (25, カリブの海賊)、[2] (20, ホーンテッドマンション)、
        [3] (40, ビッグサンダー・マウンテン)、[4] (50, プーさんのハニーハント)、[5] (60, 美女と野獣)</p>
        <table>
          <tr><th>取り出した順</th><th>組</th><th>どうしたか</th></tr>
          <tr><td>1</td><td>(15, イッツ・ア・スモールワールド)</td><td>1番目に乗る</td></tr>
          <tr><td>2</td><td>(20, ホーンテッドマンション)</td><td>2番目に乗る → お知らせで (10, プーさんのハニーハント) を入れる</td></tr>
          <tr><td>3</td><td>(10, プーさんのハニーハント)</td><td>3番目に乗る</td></tr>
          <tr><td>4</td><td>(25, カリブの海賊)</td><td>4番目に乗る</td></tr>
          <tr><td>5</td><td>(40, ビッグサンダー・マウンテン)</td><td>5番目に乗る</td></tr>
          <tr><td>6</td><td>(50, プーさんのハニーハント)</td><td>もう乗ったので読み飛ばす</td></tr>
          <tr><td>7</td><td>(60, 美女と野獣)</td><td>6番目に乗る</td></tr>
        </table>
        <p style="margin-top:0.6rem">待ち時間の合計は 15 + 20 + 10 + 25 + 40 + 60 = <strong>170分</strong> です。</p>"""),
    ("演習2のひな形（書き換える前）の確かめ用", """        <p>ひな形のままの地図（第5回と同じ）で、エントランスから各場所までの時間は第5回の演習1と同じです
        （ワールドバザール 3分、プラザ 6分、シンデレラ城 7分、アドベンチャーランド・ファンタジーランド・トゥモローランド 9分、ウエスタンランド 12分、トゥーンタウン 13分、クリッターカントリー 16分）。</p>
        <p>heappop は13回で、読み飛ばしは3回です（(10, アドベンチャーランド)、(10, トゥモローランド)、(14, トゥーンタウン)）。
        どれも、時間を書き直す前に入れた古い組が、箱に残っていたものです。</p>
        <p>アドベンチャーランドとトゥモローランドは、第5回の演習1でも書き直した場所です。
        トゥーンタウンは、第5回では書き直しがありませんでした。同じ9分の場所のうち、第5回は <code>park</code> に先に書いたファンタジーランドを先に確定しましたが、
        heapq 版では組の2番目（名前）でくらべるので「ト」で始まるトゥモローランドが先に確定し、トゥーンタウンにいったん14分が入ってから、ファンタジーランドの確定で13分に書き直されたためです。
        最後の時間は同じです。</p>
        <p>エントランスからトゥーンタウンへは、エントランス → ワールドバザール → プラザ → シンデレラ城 → ファンタジーランド → トゥーンタウン の <strong>13分</strong> です。</p>"""),
])
body = "\n".join([
    sub,
    section("sec-explanation", "1", "優先度付きキュー（heapq）と、heapq 版のダイクストラ法", explanation),
    section("sec-examples", "2", "例題とクリエイティブ演習", examples),
    slides_for("06", SLIDES),
    advanced_section("06"),
    rubric_section("06"),
    ans,
])

write("06", NAV, body)
