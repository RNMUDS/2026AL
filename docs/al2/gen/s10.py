# -*- coding: utf-8 -*-
"""第10回: 巡回セールスマン問題（3）動的計画法 の本文を組み立てる。"""
import math
from common import (AMBER, GRAY, GREEN, RED, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)


# ────────────────────────────────────────────────────────────
# 図1: 全探索は同じ計算をくり返している
# ────────────────────────────────────────────────────────────
def fig_duplicate():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索は、同じ計算を何度もくり返している</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '2つの道は、通ってきた順番だけが違う。着いた場所も、回り終えた都市も同じ</text>']
    paths = [("道A", ["0", "1", "2", "3"], 92), ("道B", ["0", "2", "1", "3"], 176)]
    for title, seq, y in paths:
        s.append(f'        <text x="40" y="{y+6}" fill="#ccc" font-size="12" font-weight="700">{title}</text>')
        for k, node in enumerate(seq):
            cx = 130 + k * 78
            col = AMBER if k == len(seq) - 1 else GREEN
            s.append(f'        <circle cx="{cx}" cy="{y}" r="18" fill="#1A1A1A" stroke="{col}" stroke-width="2"/>')
            s.append(f'        <text x="{cx}" y="{y+5}" text-anchor="middle" fill="#E0E0E0" font-size="13" font-weight="700">{node}</text>')
            if k < len(seq) - 1:
                s.append(f'        <line x1="{cx+18}" y1="{y}" x2="{cx+60}" y2="{y}" stroke="{GREEN}" stroke-width="2"/>')
                s.append(f'        <polygon points="{cx+60},{y} {cx+52},{y-4} {cx+52},{y+4}" fill="{GREEN}"/>')
        s.append(f'        <line x1="{130+3*78+18}" y1="{y}" x2="{130+3*78+70}" y2="{y}" stroke="#555" stroke-width="2" stroke-dasharray="5 4"/>')
        s.append(f'        <text x="{130+3*78+80}" y="{y+5}" fill="{GRAY}" font-size="11">この先は同じ</text>')
    s.append(f'        <rect x="112" y="66" width="{3*78+40}" height="146" rx="12" fill="none" stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append(f'        <rect x="130" y="238" width="440" height="86" rx="10" fill="#141414" stroke="{AMBER}"/>')
    s.append(f'        <text x="350" y="262" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '道Aと道Bに共通していること</text>')
    s.append(f'        <text x="350" y="284" text-anchor="middle" fill="#ccc" font-size="11">'
             '回った都市の集合 = 0・1・2・3　／　いまいる都市 = 3</text>')
    s.append(f'        <text x="350" y="306" text-anchor="middle" fill="#ccc" font-size="11">'
             'ここから先の最短の進み方は、どちらの道で来ても同じになる</text>')
    s.append(f'        <text x="350" y="348" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             '短いほうの距離だけを覚えておけば、長いほうは二度と調べなくてよい</text>')
    return fig(700, 364, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: ビットで集合を表す
# ────────────────────────────────────────────────────────────
def fig_bits():
    names = ["学校", "郵便局", "図書館", "カフェ", "公園"]
    examples = [(0, "まだどこにも行っていない"), (1, "学校だけ"), (5, "学校と図書館"),
                (7, "学校・郵便局・図書館"), (31, "5つ全部")]
    dur = 12
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '「回った都市の集合」を、2進数1つで表す</text>']
    cell = 78
    x0 = 152
    for i, name in enumerate(names):
        x = x0 + (4 - i) * cell
        s.append(f'        <text x="{x+cell/2-2}" y="66" text-anchor="middle" fill="{GRAY}" font-size="11">{name}</text>')
        s.append(f'        <text x="{x+cell/2-2}" y="82" text-anchor="middle" fill="#555" font-size="9">{i}番</text>')
    for k, (value, label) in enumerate(examples):
        y = 96 + k * 44
        a = (1 - 0.16) * k / len(examples)
        anim = (f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{a:.3f};{min(a+0.02,0.999):.3f};1" '
                f'dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'        <g opacity="0">{anim}')
        s.append(f'          <text x="130" y="{y+24}" text-anchor="end" fill="#ccc" font-size="13" font-weight="700">{value}</text>')
        for i in range(5):
            x = x0 + (4 - i) * cell
            on = bool(value & (1 << i))
            s.append(f'          <rect x="{x}" y="{y}" width="{cell-6}" height="34" rx="6" '
                     f'fill="{"#1a2e0a" if on else "#141414"}" stroke="{GREEN if on else "#2e2e2e"}"/>')
            s.append(f'          <text x="{x+(cell-6)/2}" y="{y+23}" text-anchor="middle" '
                     f'fill="{"#93D500" if on else "#555"}" font-size="15" font-weight="700">{1 if on else 0}</text>')
        s.append(f'          <text x="{x0+5*cell+8}" y="{y+23}" fill="{GRAY}" font-size="11">{label}</text>')
        s.append('        </g>')
    s.append(f'        <text x="350" y="{96+5*44+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '5個の都市なら、集合は 0 から 31 までの32通りの数で全部表せる</text>')
    return fig(700, 96 + 5 * 44 + 44, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 表の作り方
# ────────────────────────────────────────────────────────────
def fig_dp_table():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         'bitDP が作る表: たてが「回った集合」、よこが「いまいる都市」</text>']
    s.append(f'        <rect x="40" y="52" width="620" height="82" rx="10" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="76" text-anchor="middle" fill="{GREEN}" font-size="13" font-weight="700">'
             'best[回った集合][いまいる都市] = そこまでの最小の合計距離</text>')
    s.append(f'        <text x="350" y="100" text-anchor="middle" fill="#ccc" font-size="11">'
             '「00111 の都市を回り終えて、いま 2番の都市にいる」ときの最小距離が 15.3 という意味</text>')
    s.append(f'        <text x="350" y="122" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '同じマスに何通りの道でたどり着いても、いちばん短い値だけを残す</text>')
    # 更新のようす
    s.append(f'        <text x="350" y="164" text-anchor="middle" fill="{AMBER}" font-size="13" font-weight="700">'
             '表の1マスから、次のマスへ値を書きこむ</text>')
    boxes = [(80, "00111 の集合", "いま 2番にいる", "15.3", GREEN),
             (420, "01111 の集合", "いま 3番にいる", "15.3 + 8.5 = 23.8", AMBER)]
    for x, l1, l2, val, color in boxes:
        s.append(f'        <rect x="{x}" y="188" width="200" height="92" rx="10" fill="#1A1A1A" stroke="{color}" stroke-width="2"/>')
        s.append(f'        <text x="{x+100}" y="212" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">{l1}</text>')
        s.append(f'        <text x="{x+100}" y="232" text-anchor="middle" fill="#ccc" font-size="11">{l2}</text>')
        s.append(f'        <text x="{x+100}" y="262" text-anchor="middle" fill="#E0E0E0" font-size="14" font-weight="700">{val}</text>')
    s.append(f'        <line x1="286" y1="234" x2="414" y2="234" stroke="#666" stroke-width="2"/>')
    s.append(f'        <polygon points="414,234 404,229 404,239" fill="#666"/>')
    s.append(f'        <text x="350" y="224" text-anchor="middle" fill="{GRAY}" font-size="11">3番の都市へ移動</text>')
    s.append(f'        <text x="350" y="252" text-anchor="middle" fill="{GRAY}" font-size="10">距離 8.5</text>')
    s.append(f'        <text x="350" y="308" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             'すべてのマスについて同じことをすれば、全部の状態の最小距離が求まる</text>')
    return fig(700, 324, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 増え方の比較
# ────────────────────────────────────────────────────────────
def fig_growth_compare():
    rows = []
    for n in [10, 12, 14, 16, 18, 20]:
        fact = 1
        for k in range(1, n):
            fact *= k
        rows.append((n, (1 << n) * n, fact))
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '全探索と bitDP の「調べる量」の増え方</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '棒の長さは10倍ごとの目もり</text>']
    for i, (n, cells, fact) in enumerate(rows):
        y = 64 + i * 62
        s.append(f'        <text x="24" y="{y+24}" fill="#E0E0E0" font-size="12" font-weight="700">{n}都市</text>')
        wf = math.log10(fact) / 19 * 400
        wc = math.log10(cells) / 19 * 400
        s.append(f'        <text x="104" y="{y+16}" fill="{RED}" font-size="10">全探索</text>')
        s.append(f'        <rect x="160" y="{y+2}" width="{wf:.0f}" height="18" rx="4" fill="{RED}" opacity="0.85"/>')
        s.append(f'        <text x="{160+wf+8:.0f}" y="{y+16}" fill="{RED}" font-size="10">{fact:,}通り</text>')
        s.append(f'        <text x="104" y="{y+40}" fill="{GREEN}" font-size="10">bitDP</text>')
        s.append(f'        <rect x="160" y="{y+26}" width="{wc:.0f}" height="18" rx="4" fill="{GREEN}" opacity="0.85"/>')
        s.append(f'        <text x="{160+wc+8:.0f}" y="{y+40}" fill="{GREEN}" font-size="10">{cells:,}マス</text>')
    s.append(f'        <text x="350" y="{64+6*62+16}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '20都市では、全探索が1京2千兆通り。bitDP は2千万マスで済む</text>')
    return fig(700, 64 + 6 * 62 + 34, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "動的計画法 #sec-explanation",
    "例題 #sec-examples",
    "標準課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題2の表と答え"),
    ("#sec-examples", "tag-example", "観察記録", "例題4の増え方"),
    ("#sec-standard", "tag-standard", "標準課題1", "ビット表現を予測"),
    ("#sec-standard", "tag-standard", "標準課題2", "3手法の比較表"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第8回の全探索は必ず最適解を出しますが、12都市で終わらなくなりました。
      第9回の貪欲法は一瞬で終わりますが、最適解とはかぎりませんでした。
      第10回で学ぶ<strong>動的計画法</strong>（どうてきけいかくほう）は、
      <strong>必ず最適解を出しながら、全探索よりずっと速い</strong>方法です。
    </p>

    <div class="analogy">
      同じ計算を何度もしていることに気づいたら、答えをメモしておいて使い回す。
      たとえば「12×15」を1日に何度も計算するなら、最初の1回で180とメモしておけば、
      2回目以降は計算し直す必要がありません。
      動的計画法は、この「一度計算した答えをメモして使い回す」という考え方です。
    </div>

    <div class="concept-box">
      <h4>全探索のむだ</h4>
      <p style="font-size:0.95rem">
        全探索は「0 → 1 → 2 → 3 → …」と「0 → 2 → 1 → 3 → …」を、まったく別のものとして最後まで調べます。
        しかし2つの道は、4つ目の都市に着いた時点で<strong>状況がまったく同じ</strong>です。
        どちらも「0・1・2・3 を回り終えて、いま 3 にいる」という状態だからです。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        残っている都市も同じ、いる場所も同じなので、<strong>ここから先の最短の進み方も同じ</strong>になります。
        違うのは「ここまでにかかった距離」だけです。
        だとすれば、<strong>短いほうの距離だけを覚えておけば十分</strong>で、長いほうの道はもう調べる必要がありません。
      </p>
    </div>

{fig_duplicate()}

    <div class="concept-box">
      <h4>覚えておくべき2つのこと</h4>
      <table>
        <tr><th>覚えること</th><th>意味</th></tr>
        <tr><td>回った都市の集合</td><td>どの都市をすでに回ったか（順番は関係ない）</td></tr>
        <tr><td>いまいる都市</td><td>最後に到着した都市</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        2つが同じなら、そこまでの<strong>いちばん短い距離だけ</strong>を覚えておけば十分です。
        「どんな順番で来たか」は、この先の判断にまったく影響しません。
      </p>
    </div>

{fig_bits()}

    <div class="concept-box">
      <h4>集合をビットで表す</h4>
      <p style="font-size:0.95rem">
        「回った都市の集合」を、Pythonのリストや集合ではなく<strong>1つの整数</strong>で表します。
        都市が5個なら5けたの2進数を使い、i番の都市を回っていれば i けた目を 1 にします。
      </p>
      <table>
        <tr><th>書き方</th><th>意味</th></tr>
        <tr><td><code>1 &lt;&lt; i</code></td><td>i番の都市だけを表す数（1を左へ i けたずらす）</td></tr>
        <tr><td><code>visited | (1 &lt;&lt; i)</code></td><td>集合に i番の都市を<strong>足す</strong></td></tr>
        <tr><td><code>visited &amp; (1 &lt;&lt; i)</code></td><td>集合に i番の都市が<strong>入っているか</strong>調べる（0以外なら入っている）</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        整数1つで集合を表せるので、<code>best[visited][here]</code> のように
        <strong>リストの番号としてそのまま使えます</strong>。速く、書き方も短くなります。
        ビットを使った動的計画法なので、<strong>bitDP</strong>（ビットディーピー）と呼ばれます。
      </p>
    </div>

{fig_dp_table()}

{fig_growth_compare()}"""

ex1_body = f"""      <p>bitDP を書く前に、ビットで集合を表す練習をします。
      <code>&lt;&lt;</code>、<code>|</code>、<code>&amp;</code> の3つの記号だけ覚えれば足ります。</p>

{code('AL2-10-ex1.py')}

{run('a10_ex1_result.png', '数 <strong>5</strong> は2進数で <code>00101</code> となり、'
     '右から1けた目（0番の学校）と3けた目（2番の図書館）が 1 なので、「学校と図書館を回った」という意味になります。'
     '<code>1 &lt;&lt; 3</code> は <code>01000</code> で、3番のカフェだけを表します。'
     '<code>|</code> を使うと集合に都市を1つ足せ、<code>&amp;</code> を使うと入っているかどうかを調べられます。'
     '5個の都市なら、集合の種類は32通りしかありません。')}"""

ex2_body = f"""      <p>bitDP で巡回セールスマン問題を解きます。
      <code>best[visited][here]</code> という表を作り、
      「<code>visited</code> の都市を回り終えて、いま <code>here</code> にいる」ときの最小距離を記録していきます。</p>

{code('AL2-10-ex2.py')}

{run('a10_ex2_result.png', '表の一部が表示されました。<code>00001</code> の行は「学校だけ回った」状態で、'
     'いま学校（here=0）にいるときだけ 0.0 が入り、ほかは「-」です。'
     '<code>11111</code> の行は全部の都市を回り終えた状態で、5つの都市それぞれにいる場合の最小距離が入っています。'
     'いちばん小さいのは郵便局（here=1）の26.8で、そこから学校へ戻る8.1を足して<strong>34.9</strong>が答えになります。'
     '全探索の答えと完全に一致しました。')}

{notion('例題2の実行結果から、表の5行をそのまま書き写す。'
        'あわせて、<code>11111</code> の行のどの値が選ばれ、そこに何を足して34.9になったかを説明する。')}"""

ex3_body = f"""      <p>これまでに学んだ3つの方法を、同じ8都市の問題で比べます。</p>

{code('AL2-10-ex3.py')}

{run('a10_ex3_result.png', '全探索と bitDP はどちらも<strong>46.8</strong>で、答えが一致しました。'
     '貪欲法だけが53.2で、最適解より6.4長くなっています。'
     '時間を見ると、bitDP は全探索より<strong>3倍以上速く</strong>終わっています。'
     '都市が8個ではまだ差が小さいですが、都市が増えるほど差は大きくなります。'
     '「必ず最適解が出る」という点では全探索と bitDP は同じで、'
     '「速さ」の点で bitDP のほうがすぐれているということです。')}"""

ex4_body = f"""      <p>bitDP で都市をどこまで増やせるかを確かめます。
      あわせて、同じ都市数を全探索で解いたら何通り試すことになるかも表示します。</p>

{code('AL2-10-ex4.py')}

{run('a10_ex4_result.png', '<strong>20都市が5.876秒</strong>で解けました。'
     '同じ20都市を全探索で解こうとすると1京2千兆通りを試すことになり、まったく終わりません。'
     '第8回で確かめたとおり、全探索の限界は12都市くらいでした。'
     'bitDP は都市が1つ増えるたびに表がおよそ2倍になるだけなので、20都市あたりまで解けます。'
     'ただし「2倍ずつ」も十分に急な増え方なので、25都市を超えると bitDP でも解けなくなります。'
     '秒数はパソコンの性能で変わるので、自分の結果が画像と一致しなくても問題ありません。')}

{notion('例題4の表から、都市の数ごとの「表のマスの数」「かかった時間」「全探索なら何通りか」を書き写す。'
        'あわせて、都市が2つ増えたとき、表のマスの数と全探索の順番の数がそれぞれ何倍になったかを計算して書く。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題4は実行に10秒ほどかかります。まず作業フォルダを用意します。</p>

{setup_guide('10', ['AL2-10-ex1.py', 'AL2-10-ex2.py', 'AL2-10-ex3.py', 'AL2-10-ex4.py'])}

{keywords([
    ('動的計画法', 'どうてきけいかくほう / DP', '一度計算した答えを表に記録しておき、同じ計算をくり返さないようにする方法。'),
    ('bitDP', 'ビットディーピー', '「どの要素を選んだか」を2進数1つで表して行う動的計画法。巡回セールスマン問題によく使われる。'),
    ('ビット演算', 'ビットえんざん', '2進数のけたごとに行う計算。<code>&lt;&lt;</code>（ずらす）、<code>|</code>（または）、<code>&amp;</code>（かつ）を使う。'),
    ('状態', 'じょうたい / state', '動的計画法で「表のどのマスか」を決める情報。巡回セールスマン問題では「回った集合」と「いまいる都市」の2つ。'),
    ('メモ化', 'memoization', '一度求めた答えを覚えておいて使い回すこと。動的計画法の考え方の中心にある。'),
])}

{example(1, 'ビットで集合を表す練習', ex1_body)}

{example(2, 'bitDP で巡回セールスマン問題を解く', ex2_body)}

{example(3, '3つの方法を同じ問題で比べる', ex3_body)}

{example(4, 'bitDP はどこまで解けるか', ex4_body)}"""

std1_body = """      <p>プログラムを実行する<strong>前に</strong>、次の問いに答えてください。
      都市は5個で、番号と名前は例題1と同じ（0=学校、1=郵便局、2=図書館、3=カフェ、4=公園）です。</p>

      <table>
        <tr><th>問い</th><th>答え</th></tr>
        <tr><td>「学校とカフェを回った」を表す数は？（10進数と2進数の両方）</td><td></td></tr>
        <tr><td>「郵便局・図書館・公園を回った」を表す数は？</td><td></td></tr>
        <tr><td>2進数 <code>11010</code> はどの都市を回った状態か？</td><td></td></tr>
        <tr><td><code>18 | (1 &lt;&lt; 2)</code> の結果は？（10進数と2進数）</td><td></td></tr>
        <tr><td><code>18 &amp; (1 &lt;&lt; 4)</code> の結果は？ 公園は回った状態か？</td><td></td></tr>
        <tr><td>都市が10個のとき、集合の種類は何通りか？</td><td></td></tr>
      </table>

      <div class="setup-step">
        <p class="step-title">答え合わせのしかた</p>
        <ol>
          <li>すべての問いに答えてからNotionに書く</li>
          <li><code>AL2-10-std1.py</code> という名前で新しいファイルを作り、次のコードを貼り付けて実行する</li>
        </ol>
      </div>

<pre><span class="code-label">Python ── AL2-10-std1.py</span>
city_names = [<span class="str">"学校"</span>, <span class="str">"郵便局"</span>, <span class="str">"図書館"</span>, <span class="str">"カフェ"</span>, <span class="str">"公園"</span>]


<span class="kw">def</span> <span class="fn">show</span>(bits):
    names = []
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(<span class="num">5</span>):
        <span class="kw">if</span> bits &amp; (<span class="num">1</span> &lt;&lt; i):
            names.append(city_names[i])
    <span class="fn">print</span>(<span class="str">f"  {bits:&gt;2} = 2進数 {format(bits, '05b')} → "</span> + <span class="str">"、"</span>.join(names))


<span class="fn">show</span>(<span class="num">1</span> | (<span class="num">1</span> &lt;&lt; <span class="num">3</span>))
<span class="fn">show</span>((<span class="num">1</span> &lt;&lt; <span class="num">1</span>) | (<span class="num">1</span> &lt;&lt; <span class="num">2</span>) | (<span class="num">1</span> &lt;&lt; <span class="num">4</span>))
<span class="fn">show</span>(<span class="num">26</span>)
<span class="fn">show</span>(<span class="num">18</span> | (<span class="num">1</span> &lt;&lt; <span class="num">2</span>))
<span class="fn">print</span>(<span class="str">"18 &amp; (1 &lt;&lt; 4) ="</span>, <span class="num">18</span> &amp; (<span class="num">1</span> &lt;&lt; <span class="num">4</span>))
<span class="fn">print</span>(<span class="str">"都市が10個のときの集合の種類:"</span>, <span class="num">2</span> ** <span class="num">10</span>, <span class="str">"通り"</span>)</pre>
"""

std2_body = """      <p>第8回・第9回・第10回で学んだ3つの方法を、1つの表にまとめます。
      表はNotionに作り、空欄をすべて埋めてください。</p>

      <table>
        <tr><th>比べる点</th><th>全探索（第8回）</th><th>貪欲法（第9回）</th><th>bitDP（第10回）</th></tr>
        <tr><td>やり方をひとことで</td><td></td><td></td><td></td></tr>
        <tr><td>必ず最適解になるか</td><td></td><td></td><td></td></tr>
        <tr><td>8都市での答え</td><td></td><td></td><td></td></tr>
        <tr><td>調べる量の増え方</td><td></td><td></td><td></td></tr>
        <tr><td>解ける都市の数の目安</td><td></td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem">表を作ったうえで、次の3つの場面には、それぞれどの方法が向いているかを<strong>理由つきで</strong>答えてください。</p>
      <ul class="point-list">
        <li><strong>場面A:</strong> 修学旅行で6か所を回る順番を決める（必ず最短にしたい）</li>
        <li><strong>場面B:</strong> 工場のドリルが18か所の穴をあける順番を決める（1回決めれば10年使う）</li>
        <li><strong>場面C:</strong> 宅配便が毎日100軒を回る順番を、出発前の5秒で決める</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">標準課題1と標準課題2に取り組み、解答をNotionに記録してください。
    標準課題1は<strong>実行する前に予測を書く</strong>ことが大切です。</p>

{standard(1, 'ビット表現を予測する', std1_body)}
{notion('6つの問いへの予測、プログラムの実行結果、予測と合っていたか。')}

{standard(2, '3つの方法を1つの表にまとめる', std2_body)}
{notion('5行の比較表（空欄をすべて埋める）と、場面A・場面B・場面Cそれぞれに向いている方法とその理由。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>Notionに記録して、PDFでManabaに提出する</h3>
      </div>
      <p>第10回の提出物は次の4項目です。Notionに見出しを付けて順番に記録してください。</p>
      <ul class="point-list">
        <li><strong>例題2</strong>: 表の5行、11111 の行から34.9になるまでの説明</li>
        <li><strong>例題4</strong>: 都市数ごとの表・時間・全探索の通り数、2都市増えたときの倍率</li>
        <li><strong>標準課題1</strong>: 6つの問いへの予測と実行結果</li>
        <li><strong>標準課題2</strong>: 比較表、場面A・B・Cへの答えと理由</li>
      </ul>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>"""

ans = answers([
    ("標準課題1: ビット表現の答え", """        <table>
          <tr><th>問い</th><th>答え</th></tr>
          <tr><td>「学校とカフェを回った」を表す数</td><td><strong>9</strong>（2進数 <code>01001</code>）</td></tr>
          <tr><td>「郵便局・図書館・公園を回った」を表す数</td><td><strong>22</strong>（2進数 <code>10110</code>）</td></tr>
          <tr><td>2進数 <code>11010</code> はどの都市か</td><td>10進数で26。<strong>郵便局・カフェ・公園</strong></td></tr>
          <tr><td><code>18 | (1 &lt;&lt; 2)</code></td><td><strong>22</strong>（2進数 <code>10110</code>）</td></tr>
          <tr><td><code>18 &amp; (1 &lt;&lt; 4)</code></td><td><strong>16</strong>（0ではないので、公園は回っている）</td></tr>
          <tr><td>都市が10個のときの集合の種類</td><td><strong>1,024通り</strong>（2の10乗）</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>考え方:</strong></p>
        <ul class="point-list">
          <li>学校は0番なので <code>1 &lt;&lt; 0 = 1</code>、カフェは3番なので <code>1 &lt;&lt; 3 = 8</code>。足すと 9 です。</li>
          <li>郵便局(1番)=2、図書館(2番)=4、公園(4番)=16。合計 22 です。</li>
          <li><code>11010</code> は右から2けた目・4けた目・5けた目が1なので、1番・3番・4番、つまり郵便局・カフェ・公園です。</li>
          <li>18 は2進数で <code>10010</code>（郵便局と公園）。<code>1 &lt;&lt; 2 = 00100</code> を足すと <code>10110</code> = 22 になります。</li>
          <li><code>18 &amp; 16</code> は、両方のけたが1である5けた目だけが残るので16です。0でないので「入っている」と分かります。</li>
        </ul>
        <p style="margin-top:0.6rem"><strong>注意:</strong> <code>&amp;</code> の結果は「1」ではなく <code>1 &lt;&lt; i</code> の値になります。
        <code>if bits &amp; (1 &lt;&lt; i):</code> と書けば、0以外はすべて真として扱われるので、そのまま条件に使えます。</p>"""),
    ("標準課題2: 3つの方法の比較表と答え", """        <table>
          <tr><th>比べる点</th><th>全探索</th><th>貪欲法</th><th>bitDP</th></tr>
          <tr><td>やり方</td><td>すべての順番を試す</td><td>いちばん近い都市へ進むだけ</td><td>「回った集合と現在地」ごとに最小距離を表に記録する</td></tr>
          <tr><td>必ず最適解か</td><td>必ず最適</td><td>最適とはかぎらない</td><td>必ず最適</td></tr>
          <tr><td>8都市での答え</td><td>46.8</td><td>53.2</td><td>46.8</td></tr>
          <tr><td>調べる量の増え方</td><td>(n-1)! 通り（1つ増えると n-1 倍）</td><td>n×n 程度</td><td>2ⁿ×n マス（1つ増えると約2倍）</td></tr>
          <tr><td>解ける都市の目安</td><td>12都市くらいまで</td><td>何千都市でも</td><td>20〜25都市くらいまで</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>場面A（6か所・必ず最短）: 全探索</strong><br>
        6か所なら 5! = 120通りしかなく、一瞬で終わります。
        bitDP でも解けますが、コードが長くなるだけで得はありません。
        「小さい問題なら全探索がいちばん簡単で確実」という判断です。</p>
        <p style="margin-top:0.6rem"><strong>場面B（18か所・10年使う）: bitDP</strong><br>
        必ず最短にしたいので、貪欲法は使えません。
        18か所の全探索は 17! = 約3,556兆通りで終わりません。
        例題4のとおり bitDP なら18都市が約1.2秒で解けます。
        1回決めれば10年使うので、数秒の計算はまったく問題になりません。</p>
        <p style="margin-top:0.6rem"><strong>場面C（100軒・5秒で決める）: 貪欲法</strong><br>
        100軒では bitDP の表が 2の100乗マスになり、宇宙にあるすべての原子より多くなります。
        全探索も当然無理です。
        5秒で答えを出す必要があるので、最短をあきらめて貪欲法で近似解を作ります。
        第9回の例題3のように、複数の出発点で試していちばん良いものを選べば、精度も上げられます。</p>
        <p style="margin-top:0.6rem"><strong>まとめ:</strong>
        「都市の数」と「最適解が必要かどうか」と「使える時間」の3つで決めます。
        1つの方法がいつでも最良ということはありません。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "動的計画法（bitDP）", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "標準課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("10", NAV, body)
