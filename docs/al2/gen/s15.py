# -*- coding: utf-8 -*-
"""第15回: まとめ の本文を組み立てる。"""
import math
from common import (AMBER, GRAY, GREEN, RED, BLUE, answers, code, example, fig,
                    keywords, notion, reveal, run, section, setup_guide,
                    standard, submission, write)


# ────────────────────────────────────────────────────────────
# 図1: 前期と後期をつなぐ全体像
# ────────────────────────────────────────────────────────────
def fig_whole():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '前期と後期で学んだことのつながり</text>']
    groups = [
        ("前期（アルゴリズム論及び演習I）", 24, "#555",
         [("探す", "逐次探索・二分探索・ハッシュ法"),
          ("並べる", "挿入ソート・カウンティングソート"),
          ("たどる", "幅優先探索・深さ優先探索")]),
        ("後期（アルゴリズム論及び演習II）", 366, GREEN,
         [("最短の道をさがす", "ダイクストラ法"),
          ("いちばん良い順番をさがす", "全探索・貪欲法・bitDP"),
          ("そこそこ良い答えを速く出す", "焼きなまし法・遺伝的アルゴリズム")]),
    ]
    for title, x0, color, items in groups:
        s.append(f'        <rect x="{x0}" y="48" width="310" height="222" rx="12" fill="#141414" stroke="{color}" stroke-width="1.6"/>')
        s.append(f'        <text x="{x0+155}" y="72" text-anchor="middle" fill="{color if color != "#555" else "#aaa"}" font-size="12" font-weight="700">{title}</text>')
        for i, (name, detail) in enumerate(items):
            y = 90 + i * 60
            s.append(f'        <rect x="{x0+14}" y="{y}" width="282" height="50" rx="8" fill="#1A1A1A" stroke="#3a3a3a"/>')
            s.append(f'        <text x="{x0+26}" y="{y+21}" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
            s.append(f'        <text x="{x0+26}" y="{y+40}" fill="{GRAY}" font-size="10">{detail}</text>')
    s.append(f'        <text x="350" y="296" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '前期の「たどる」が、後期の「最短の道をさがす」につながっている</text>')
    return fig(700, 312, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図2: 焼きなまし法の考え方
# ────────────────────────────────────────────────────────────
def fig_annealing():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '焼きなまし法: わざと悪くなる変更も、たまには受け入れる</text>',
         f'        <text x="350" y="48" text-anchor="middle" fill="{GRAY}" font-size="11">'
         'たての位置が「ルートの長さ」。下にあるほど良い（谷の底がいちばん良い）</text>']
    # なだらかな起伏を、いくつかの目印の点をつないで作る
    anchors = [(60, 150), (140, 208), (200, 236), (270, 192), (330, 148),
               (400, 216), (470, 282), (540, 204), (640, 162)]
    pts = []
    for k in range(len(anchors) - 1):
        x1, y1 = anchors[k]
        x2, y2 = anchors[k + 1]
        steps = max(int((x2 - x1) / 3), 1)
        for i in range(steps):
            t = i / steps
            smooth = (1 - math.cos(t * math.pi)) / 2      # なめらかにつなぐ
            pts.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * smooth))
    pts.append(anchors[-1])
    path = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s.append(f'        <polyline points="{path}" fill="none" stroke="#444" stroke-width="3"/>')

    local = (200, 236)
    glob = (470, 282)
    s.append(f'        <circle cx="{local[0]}" cy="{local[1]}" r="10" fill="{AMBER}"/>')
    s.append(f'        <text x="{local[0]}" y="{local[1]+26}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">貪欲法はここで止まる</text>')
    s.append(f'        <text x="{local[0]}" y="{local[1]+44}" text-anchor="middle" fill="{AMBER}" font-size="11">（局所最適）</text>')
    s.append(f'        <circle cx="{glob[0]}" cy="{glob[1]}" r="10" fill="{GREEN}"/>')
    s.append(f'        <text x="{glob[0]}" y="{glob[1]+26}" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">本当にいちばん良い場所</text>')
    s.append(f'        <text x="{glob[0]}" y="{glob[1]+44}" text-anchor="middle" fill="{GREEN}" font-size="11">（全体最適）</text>')
    s.append(f'        <path d="M {local[0]} {local[1]-16} Q 335 96 {glob[0]} {glob[1]-16}" '
             f'fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    s.append(f'        <polygon points="{glob[0]},{glob[1]-16} {glob[0]-9},{glob[1]-27} {glob[0]+3},{glob[1]-28}" fill="{RED}"/>')
    s.append(f'        <text x="335" y="84" text-anchor="middle" fill="{RED}" font-size="12" font-weight="700">'
             'いったん悪くなる山を越えないと、たどり着けない</text>')
    s.append(f'        <text x="330" y="140" text-anchor="middle" fill="{GRAY}" font-size="11">山</text>')
    s.append(f'        <rect x="60" y="344" width="580" height="62" rx="10" fill="#141414" stroke="{GREEN}"/>')
    s.append(f'        <text x="350" y="368" text-anchor="middle" fill="{GREEN}" font-size="12" font-weight="700">'
             '最初は熱い（悪い変更もよく受け入れる）→ だんだん冷ます（受け入れなくなる）</text>')
    s.append(f'        <text x="350" y="390" text-anchor="middle" fill="#ccc" font-size="11">'
             '熱いうちに山を越え、冷めてから谷の底へ落ち着く</text>')
    return fig(700, 422, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図3: 遺伝的アルゴリズムの考え方
# ────────────────────────────────────────────────────────────
def fig_genetic():
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '遺伝的アルゴリズム: 良いルートどうしを組み合わせて次の世代を作る</text>']
    steps = [("① 集団を作る", "ばらばらのルートを100個用意する", GREEN),
             ("② 親を選ぶ", "3つ選んで、いちばん短いものを親にする", GREEN),
             ("③ 子を作る", "親1の一部＋親2の残りで、新しいルートを作る", AMBER),
             ("④ 突然変異", "まれに2か所を入れかえる", AMBER),
             ("⑤ 世代を進める", "②〜④で次の100個を作り、くり返す", GREEN)]
    for i, (title, note, color) in enumerate(steps):
        y = 52 + i * 44
        s.append(f'        <rect x="40" y="{y}" width="620" height="36" rx="9" fill="#141414" stroke="#333"/>')
        s.append(f'        <text x="60" y="{y+24}" fill="{color}" font-size="13" font-weight="700">{title}</text>')
        s.append(f'        <text x="220" y="{y+24}" fill="#ccc" font-size="11">{note}</text>')
    y = 52 + 5 * 44 + 6
    s.append(f'        <rect x="40" y="{y}" width="620" height="62" rx="10" fill="#141414" stroke="{AMBER}"/>')
    s.append(f'        <text x="350" y="{y+24}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '「良いものどうしを混ぜると、もっと良いものができやすい」という考え方</text>')
    s.append(f'        <text x="350" y="{y+45}" text-anchor="middle" fill="#ccc" font-size="11">'
             '突然変異があることで、集団全体が同じ答えに固まってしまうことを防いでいる</text>')
    return fig(700, y + 80, "\n".join(s))


# ────────────────────────────────────────────────────────────
# 図4: 20都市での5手法比較
# ────────────────────────────────────────────────────────────
def fig_five():
    rows = [("貪欲法", 105.7, 0.000, "第9回", RED, 15.9),
            ("貪欲法(全出発点)", 95.0, 0.000, "第11回", AMBER, 4.2),
            ("焼きなまし法", 95.2, 0.015, "第15回", AMBER, 4.5),
            ("遺伝的アルゴリズム", 96.3, 0.533, "第15回", AMBER, 5.7),
            ("bitDP（必ず最適）", 91.1, 6.214, "第10回", GREEN, 0.0)]
    best = 91.1
    s = [f'        <text x="350" y="26" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         '20都市の巡回セールスマン問題を5つの方法で解いた結果</text>',
         f'        <text x="350" y="46" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '全探索なら19の階乗＝約12京通り。まったく終わらない（秒数は測ったときの一例）</text>']
    for i, (name, value, t, week, color, pct) in enumerate(rows):
        y = 64 + i * 54
        w = (value - 85) / (110 - 85) * 380
        s.append(f'        <text x="24" y="{y+20}" fill="#E0E0E0" font-size="12" font-weight="700">{name}</text>')
        s.append(f'        <text x="24" y="{y+38}" fill="{GRAY}" font-size="10">{week}　／　{t:.3f}秒</text>')
        s.append(f'        <rect x="230" y="{y+6}" width="{w:.0f}" height="24" rx="5" fill="{color}" opacity="0.85"/>')
        s.append(f'        <text x="{230+w+10:.0f}" y="{y+24}" fill="{color}" font-size="12" font-weight="700">{value}</text>')
        if value > best:
            s.append(f'        <text x="{230+w+62:.0f}" y="{y+24}" fill="{GRAY}" font-size="10">'
                     f'最適より{pct}%長い</text>')
    xline = 230 + (best - 85) / 25 * 380
    s.append(f'        <line x1="{xline:.0f}" y1="58" x2="{xline:.0f}" y2="{64+5*54-8}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'        <text x="350" y="{64+5*54+18}" text-anchor="middle" fill="{AMBER}" font-size="12" font-weight="700">'
             '近似解の3つは、最適の4〜6%長いだけ。しかも bitDP より圧倒的に速い</text>')
    return fig(700, 64 + 5 * 54 + 36, "\n".join(s))


# ────────────────────────────────────────────────────────────
NAV = [
    "提出 #sec-submission",
    "後期の総括 #sec-explanation",
    "例題 #sec-examples",
    "課題 #sec-standard nav-assignment",
    "提出まとめ #sec-notion",
    "解答 #answers-section",
]

sub = submission([
    ("#sec-examples", "tag-example", "観察記録", "例題4の5手法比較"),
    ("#sec-standard", "tag-standard", "課題1", "後期の振り返り"),
    ("#sec-standard", "tag-standard", "課題2", "発展手法の観察"),
    ("#sec-notion", "tag-advanced", "最終確認", "第13〜14回の提出物"),
], 4)

explanation = f"""    <p style="font-size:1.05rem;margin-bottom:1.5rem">
      第15回は後期のまとめです。学んだ内容を振り返り、
      後期の授業では扱いきれなかった<strong>発展的な手法</strong>を2つ体験します。
      あわせて、第13回・第14回で作った作品とレポートの最終チェックを行います。
    </p>

{fig_whole()}

    <div class="concept-box">
      <h4>後期でいちばん大切だったこと</h4>
      <p style="font-size:0.95rem">
        後期で学んだのは、6つのアルゴリズムそのものよりも、次の考え方です。
      </p>
      <ol style="padding-left:1.5rem;font-size:0.95rem;line-height:2;color:#ccc">
        <li><strong>問題を、頂点と辺のグラフに書き直す</strong>と、見た目が違うものも同じ方法で解ける</li>
        <li><strong>「必ず最適」と「速い」は両立しないことがある</strong>。どちらを取るかは、場面によって決める</li>
        <li><strong>問題の大きさが、使える方法を決める</strong>。10都市と100都市では、選ぶ方法がまったく違う</li>
      </ol>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        3つの考え方は、アルゴリズムに限らず、企画・マーケティング・経理・データ分析など、
        「限られた時間の中でいちばん良い選択をする」あらゆる場面に当てはまります。
      </p>
    </div>

    <div class="concept-box">
      <h4>後期で扱わなかったこと</h4>
      <p style="font-size:0.95rem">
        巡回セールスマン問題は、bitDP でも25都市あたりが限界でした。
        では、実際の配送計画で扱う100都市や1000都市はどうしているのでしょうか。
        答えは<strong>「最適解をあきらめて、良い近似解を上手にさがす」</strong>です。
        そのための代表的な手法を2つ体験します。
      </p>
      <table>
        <tr><th>手法</th><th>まねているもの</th><th>考え方</th></tr>
        <tr><td><strong style="color:#76B900">焼きなまし法</strong></td><td>熱した金属をゆっくり冷ますこと</td><td>最初は悪い変更も受け入れ、だんだん受け入れなくなる</td></tr>
        <tr><td><strong style="color:#76B900">遺伝的アルゴリズム</strong></td><td>生き物の進化</td><td>良い答えどうしを組み合わせて、次の世代を作る</td></tr>
      </table>
    </div>

{fig_annealing()}

    <div class="concept-box">
      <h4>なぜ「わざと悪くする」必要があるのか</h4>
      <p style="font-size:0.95rem">
        貪欲法は「いま良くなる方向」にしか進みません。
        そのため、まわりより少し良いだけの場所（<strong>局所最適</strong>）に着くと、そこから動けなくなります。
        本当にいちばん良い場所へ行くには、<strong>いったん悪くなる山を越える</strong>必要があります。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        焼きなまし法は「温度」という数を用意し、温度が高いうちは悪い変更もよく受け入れます。
        温度を少しずつ下げていくと、しだいに良い変更しか受け入れなくなり、答えが落ち着きます。
        高いところから山を越え、冷めてから谷の底に落ち着く、というしくみです。
      </p>
    </div>

{fig_genetic()}

{fig_five()}"""

ex1_body = f"""      <p>後期に学んだ6つのアルゴリズムを、1つのプログラムでまとめて動かします。
      前半は2地点間の経路、後半は全部回って戻る最短ルートです。</p>

{code('AL2-15-ex1.py')}

{run('a15_ex1_result.png', '前半では、ダイクストラ法だけが<strong>27分</strong>の経路を見つけています。'
     '幅優先探索と深さ優先探索は路線の本数が少ない41分の経路を返しました。'
     '後半では、全探索と bitDP がどちらも<strong>50.1</strong>という同じ答えを出し、'
     '貪欲法だけが58.2と長くなっています。'
     'かかった時間は、全探索が0.08秒ほどに対し bitDP は0.002秒ほどで、数十倍の差がつきました。'
     '後期の授業で1行ずつ書いてきたコードが、すべてここに集まっています。')}"""

ex2_body = f"""      <p>後期では扱わなかった<strong>焼きなまし法</strong>を体験します。
      20都市の問題を、貪欲法が作ったルートから始めて、少しずつ短くしていきます。</p>

      <div class="concept-box">
        <h4>コードの中で起きていること</h4>
        <ul class="point-list">
          <li>2つの都市を選んで、順番を<strong>入れかえてみる</strong></li>
          <li>短くなったら、必ず受け入れる</li>
          <li>長くなった場合も、<code>math.exp(-差 / 温度)</code> の確率で受け入れる</li>
          <li>1回ごとに温度を0.9995倍して、少しずつ冷ましていく</li>
        </ul>
        <p style="font-size:0.92rem;margin-top:0.6rem;color:#bbb">
          <code>math.exp(-差 / 温度)</code> は、差が小さいほど、また温度が高いほど1に近づく値です。
          「少しだけ悪くなる変更」は受け入れやすく、「大きく悪くなる変更」は受け入れにくくなります。
        </p>
      </div>

{code('AL2-15-ex2.py')}

{run('a15_ex2_result.png', '貪欲法が作った<strong>105.7</strong>のルートが、'
     '20,000ステップの改善で<strong>95.2</strong >まで短くなりました。約9.9%の改善です。'
     '途中経過を見ると、温度が9.995から0.005まで下がっていく間に答えが落ち着いていきます。'
     '「悪くなる変更」を478回受け入れており、その回り道があったからこそ局所最適から抜け出せています。'
     '<code>random.seed(2026)</code> で乱数を固定しているので、何度実行しても同じ結果になります。')}"""

ex3_body = f"""      <p>もう1つの発展手法、<strong>遺伝的アルゴリズム</strong>を体験します。
      100個のルートを「集団」として持ち、良いものどうしを組み合わせて次の世代を作ります。</p>

{code('AL2-15-ex3.py')}

{run('a15_ex3_result.png', '第1世代ではいちばん良いルートでも<strong>170.6</strong>と、でたらめに近い長さでした。'
     '100世代で98.2まで縮み、最終的に<strong>96.7</strong>になっています。'
     '集団の平均も219.7から105前後まで下がっており、集団全体が良くなっていることが分かります。'
     '200世代以降は最良の値が変わっていません。集団の中身が似てきて、'
     '新しい組み合わせが生まれにくくなったためです。'
     '突然変異の確率を上げると、もう少し先まで改善が続くことがあります。')}"""

ex4_body = f"""      <p>20都市の問題を、後期に学んだ方法と発展手法を合わせて5つで解き、まとめて比べます。
      実行に10秒ほどかかります。</p>

{code('AL2-15-ex4.py')}

{fig_five()}

{run('a15_ex4_result.png', '<strong>bitDP だけが最適の91.1</strong>を出し、6秒ほどかかりました。'
     '近似解の3つ（貪欲法の全出発点版・焼きなまし法・遺伝的アルゴリズム）は、'
     '最適より<strong>わずか4〜6%長いだけ</strong>で、いずれも1秒以内に終わっています。'
     '出発点を1つに固定した貪欲法だけが15.9%長く、明らかに劣っています。'
     '20都市では bitDP が使えましたが、25都市を超えると表が大きすぎて使えなくなります。'
     'そのとき頼りになるのが、この3つの近似解法です。')}

{notion('例題4の表から、5つの方法それぞれの「答え」「最適との差」「かかった時間」を書き写す。'
        'あわせて、「25都市を超えたらどの方法を使うか」を、理由とともに書く。')}"""

examples = f"""    <p style="margin-bottom:1.5rem">例題1から例題4までのコードを実行してください。
    例題4は実行に10秒ほどかかります。まず作業フォルダを用意します。</p>

{setup_guide('15', ['AL2-15-ex1.py', 'AL2-15-ex2.py', 'AL2-15-ex3.py', 'AL2-15-ex4.py'])}

{keywords([
    ('焼きなまし法', 'やきなましほう / Simulated Annealing', '悪くなる変更もときどき受け入れながら、少しずつ受け入れにくくしていく方法。局所最適から抜け出せる。'),
    ('遺伝的アルゴリズム', 'いでんてきアルゴリズム / GA', 'たくさんの答えを集団として持ち、良いものどうしを組み合わせて次の世代を作る方法。'),
    ('メタヒューリスティクス', 'metaheuristics', '焼きなまし法や遺伝的アルゴリズムのように、いろいろな問題に使える「良い答えのさがし方」のまとめ。'),
    ('乱数の種', 'らんすうのたね / random seed', '<code>random.seed(2026)</code> のように決めておくと、乱数を使っても毎回同じ結果になる。実験をやり直せるようにするために使う。'),
    ('局所最適', 'きょくしょさいてき', 'まわりより良いが、全体でいちばん良いとはかぎらない答え。貪欲法がはまりこみやすい。'),
])}

{example(1, '後期に学んだ6つを一度に動かす', ex1_body)}

{example(2, '焼きなまし法を体験する', ex2_body)}

{example(3, '遺伝的アルゴリズムを体験する', ex3_body)}

{example(4, '5つの方法をまとめて比べる', ex4_body)}"""

std1_body = """      <p>後期の授業全体を振り返り、次の4つの問いに答えてください。
      教材を見ながらで構いません。それぞれ4行以上で書いてください。</p>

      <div class="setup-step">
        <p class="step-title">問い1: いちばん印象に残ったアルゴリズム</p>
        <p style="font-size:0.95rem;color:#ccc">後期に学んだ6つ（幅優先探索・深さ優先探索・ダイクストラ法・全探索・貪欲法・bitDP）から1つ選び、
        <strong>どんな場面で使うか</strong>と<strong>なぜ印象に残ったか</strong>を書いてください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">問い2: 前期とのつながり</p>
        <p style="font-size:0.95rem;color:#ccc">前期に学んだこと（探索・整列・計算量）のうち、
        後期でいちばん役に立ったものを1つ挙げ、<strong>どの回のどの場面で役に立ったか</strong>を具体的に書いてください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">問い3: 身のまわりへの応用</p>
        <p style="font-size:0.95rem;color:#ccc">自分の生活・アルバイト・サークル・将来の仕事の中で、
        後期に学んだ考え方が使えそうな場面を1つ挙げ、<strong>どのアルゴリズムをどう使うか</strong>を書いてください。</p>
      </div>

      <div class="setup-step">
        <p class="step-title">問い4: いちばん難しかったこと</p>
        <p style="font-size:0.95rem;color:#ccc">後期でいちばん理解に時間がかかったところを1つ挙げ、
        <strong>どこがつまずきの原因だったか</strong>と<strong>どうやって乗り越えたか</strong>を書いてください。
        まだ理解できていない場合は、それも正直に書いてください。</p>
      </div>
"""

std2_body = """      <p>例題2の焼きなまし法と例題3の遺伝的アルゴリズムを、設定を変えて動かし、
      結果がどう変わるかを観察します。</p>

      <div class="setup-step">
        <p class="step-title">実験1: 焼きなまし法の温度を変える</p>
        <p style="font-size:0.95rem;color:#ccc">
        <code>AL2-15-ex2.py</code> の <code>temperature = 10.0</code> を、
        <strong>0.1</strong> と <strong>100.0</strong> に変えて実行してください。</p>
      </div>

      <table>
        <tr><th>最初の温度</th><th>最後のルート</th><th>悪い変更を受け入れた回数</th></tr>
        <tr><td>0.1</td><td></td><td></td></tr>
        <tr><td>10.0（もとの値）</td><td>95.2</td><td>478回</td></tr>
        <tr><td>100.0</td><td></td><td></td></tr>
      </table>

      <div class="setup-step">
        <p class="step-title">実験2: 遺伝的アルゴリズムの突然変異を変える</p>
        <p style="font-size:0.95rem;color:#ccc">
        <code>AL2-15-ex3.py</code> の <code>if random.random() &lt; 0.3:</code> を、
        <strong>0.0</strong> と <strong>0.8</strong> に変えて実行してください。</p>
      </div>

      <table>
        <tr><th>突然変異の確率</th><th>最後のルート</th><th>集団の平均（900世代）</th></tr>
        <tr><td>0.0</td><td></td><td></td></tr>
        <tr><td>0.3（もとの値）</td><td>96.7</td><td>104.8</td></tr>
        <tr><td>0.8</td><td></td><td></td></tr>
      </table>

      <p style="margin-top:1rem"><strong>問い:</strong> 2つの実験の結果から、次の3つに答えてください。</p>
      <ul class="point-list">
        <li>最初の温度を変えると、「悪い変更を受け入れた回数」はどう変わりましたか。答えの長さとの関係を書いてください。</li>
        <li>突然変異の確率を 0.0 にしたとき、集団の平均と最良の値はどうなりましたか。なぜそうなるのかを説明してください。</li>
        <li>2つの実験から、「新しいことを試す力」を強めると答えは良くなりましたか、悪くなりましたか。<strong>実際の数値を根拠に</strong>答えてください。</li>
      </ul>
"""

standard_sec = f"""    <p style="margin-bottom:1.5rem">課題1と課題2に取り組み、解答をNotionに記録してください。</p>

{standard(1, '後期の振り返り', std1_body)}
{notion('問い1〜問い4への解答。それぞれ4行以上で、具体的な回や場面を挙げて書く。')}

{standard(2, '発展手法の設定を変えて観察する', std2_body)}
{notion('実験1・実験2それぞれの表（空欄をすべて埋める）と、3つの問いへの解答。')}"""

notion_sec = """    <div class="card" style="border-left:4px solid #FFB800">
      <div class="card-header">
        <span class="tag tag-advanced">提出まとめ</span>
        <h3>後期の提出物の最終チェック</h3>
      </div>
      <p>第15回の提出物は次の4項目です。</p>
      <ul class="point-list">
        <li><strong>例題4</strong>: 5つの方法の答え・差・時間の表、25都市を超えたときの選択と理由</li>
        <li><strong>課題1</strong>: 後期の振り返り（問い1〜問い4）</li>
        <li><strong>課題2</strong>: 実験1・実験2の表と、3つの問いへの解答</li>
        <li><strong>最終確認</strong>: 第13回・第14回の作品とレポートが提出済みかを確かめる</li>
      </ul>
      <div class="note-warn" style="margin-top:1rem">
        <strong>作品とレポートについて:</strong> 第13回・第14回で提出した作品とレポートは、
        第15回の授業中まで修正して出し直すことができます。
        直したい部分があれば、この時間に修正して提出し直してください。
      </div>
      <div style="background:#0a1a0a;border:1px solid #4A7A00;border-radius:0.3rem;padding:0.6rem 0.8rem;margin-top:0.8rem;font-size:0.8rem;color:#93D500">
        <strong>Notionに書いただけでは提出になりません。</strong>必ずPDFに書き出し、Manabaに提出してください。
      </div>
    </div>

    <div class="card" style="border-left:4px solid #76B900;margin-top:1.5rem">
      <div class="card-header">
        <span class="tag tag-example">この先へ</span>
        <h3>もっと学びたい人へ</h3>
      </div>
      <p>後期の内容の先には、次のような世界が広がっています。</p>
      <table>
        <tr><th>分野</th><th>内容</th><th>後期の内容とのつながり</th></tr>
        <tr><td>ネットワークフロー</td><td>「どれだけ流せるか」を求める問題</td><td>グラフの上で解く。ダイクストラ法の考え方を使う手法もある</td></tr>
        <tr><td>線形計画法</td><td>不等式の条件のもとで最大・最小を求める</td><td>配送計画や生産計画で実際に使われている</td></tr>
        <tr><td>A*（エースター）探索</td><td>ゴールの方向を手がかりに速く探索する</td><td>ダイクストラ法に「ゴールまでの見当」を足したもの。ゲームAIで広く使われる</td></tr>
        <tr><td>強化学習</td><td>試行錯誤しながら良い行動を学ぶ</td><td>「いま良い選択」と「先を見た選択」のバランスは、貪欲法と焼きなまし法の話と同じ構造</td></tr>
      </table>
      <p style="margin-top:0.8rem;font-size:0.95rem">
        後期に身につけた「問題をグラフに書き直す」「最適解と近似解を使い分ける」という考え方は、
        どの分野へ進んでも土台になります。半年間おつかれさまでした。
      </p>
    </div>"""

ans = answers([
    ("課題1: 振り返りの書き方の例", """        <p>正解のない課題です。次は「4行以上・具体的」という条件を満たす書き方の例です。</p>
        <p style="margin-top:0.8rem"><strong>問い1の例:</strong></p>
        <p style="margin-top:0.4rem">「いちばん印象に残ったのはダイクストラ法です。
        使う場面は、道ごとに時間や料金が違う地図で、出発点から目的地までの最も安い行き方を求めるときです。
        カーナビや乗換案内の中で実際に動いていると知って驚きました。
        印象に残った理由は、第4回で『幅優先探索では最短時間が求まらない』と分かったあとに学んだので、
        なぜ必要なのかが先に分かっていたからです。
        第5回で距離表が書き直されていく様子を見て、仕組みが目に見えたことも大きかったです。」</p>
        <p style="margin-top:0.8rem"><strong>問い2の例:</strong></p>
        <p style="margin-top:0.4rem">「前期の幅優先探索がいちばん役に立ちました。
        後期の第12回で、迷路のアイテムを集めるパズルを解くときに使いました。
        アイテムどうしの『歩数』を求める部分がまさに幅優先探索で、
        そこで作った表に対して巡回セールスマン問題の解き方を使う、という2段構えでした。
        前期に学んだものが、後期の問題の一部として組み込まれていることが分かりました。」</p>
        <p style="margin-top:0.8rem"><strong>問い3の例:</strong></p>
        <p style="margin-top:0.4rem">「アルバイト先のカフェで、開店前の準備の順番を決めるときに使えそうです。
        コーヒーを淹れる、パンを焼く、床を掃く、といった作業には、それぞれかかる時間と『先にやらないといけない順番』があります。
        『限られた時間の中で、できるだけ多くの準備を終わらせる』と考えれば、第12回のナップサック問題と同じ形です。
        作業を選ぶだけなら動的計画法、順番も決めるなら巡回セールスマン問題に近くなります。」</p>
        <p style="margin-top:0.8rem"><strong>問い4の例:</strong></p>
        <p style="margin-top:0.4rem">「第10回の bitDP がいちばん難しかったです。
        つまずいた原因は『集合を整数で表す』という発想でした。
        <code>1 &lt;&lt; i</code> や <code>|</code> が何をしているのかが分からず、コードが読めませんでした。
        例題1で2進数を1けたずつ表示させて、5という数が <code>00101</code> であり、
        1のけたが『回った都市』を表していると目で見て、ようやく分かりました。
        いまでも <code>&amp;</code> の結果が1ではなく <code>1 &lt;&lt; i</code> の値になる点は間違えやすいと感じています。」</p>"""),
    ("課題2: 実験の結果と考察", """        <p>乱数の種を <code>random.seed(2026)</code> で固定しているので、同じコードなら誰が実行しても同じ値になります。</p>
        <table>
          <tr><th>最初の温度</th><th>最後のルート</th><th>悪い変更を受け入れた回数</th></tr>
          <tr><td>0.1</td><td>96.4</td><td>2回</td></tr>
          <tr><td>10.0（もとの値）</td><td>95.2</td><td>478回</td></tr>
          <tr><td>100.0</td><td><strong style="color:#76B900">92.6</strong></td><td>2,378回</td></tr>
        </table>
        <table style="margin-top:0.8rem">
          <tr><th>突然変異の確率</th><th>最後のルート</th><th>集団の平均（900世代）</th></tr>
          <tr><td>0.0</td><td><strong style="color:#FF5252">117.4</strong></td><td>117.4（最良とまったく同じ）</td></tr>
          <tr><td>0.3（もとの値）</td><td>96.7</td><td>104.8</td></tr>
          <tr><td>0.8</td><td><strong style="color:#76B900">93.2</strong></td><td>151.1</td></tr>
        </table>
        <p style="margin-top:0.8rem"><strong>問い1（温度と受け入れ回数）:</strong>
        最初の温度を上げるほど、悪い変更を受け入れた回数が増えました（2回 → 478回 → 2,378回）。
        そして受け入れた回数が多いほど、最後のルートが短くなっています（96.4 → 95.2 → 92.6）。
        温度0.1のときは悪い変更をほとんど受け入れないため、貪欲法のルートから少し良くする程度で止まっています。
        いちばん良かったのは温度100.0で、山を何度も越えられたぶん、より良い谷にたどり着けました。</p>
        <p style="margin-top:0.8rem"><strong>問い2（突然変異が0のとき）:</strong>
        集団の平均が117.4となり、<strong>最良の値とまったく同じ</strong>になりました。
        これは、集団の100個がすべて同じルートになってしまったことを意味します。
        突然変異がないと、新しい形がどこからも生まれません。
        親を組み合わせて子を作っても、親が全員同じなら子も同じになります。
        こうなると何世代進めても値が動かず、117.4のまま止まってしまいます。</p>
        <p style="margin-top:0.8rem"><strong>問い3（試す力を強めると）:</strong>
        2つの実験とも、<strong>試す力を強めたほうが答えは良くなりました</strong>。
        焼きなまし法では温度100.0が92.6で最良、遺伝的アルゴリズムでは突然変異0.8が93.2で最良でした。
        どちらも、もとの設定（95.2 と 96.7）より良い結果です。</p>
        <p style="margin-top:0.6rem"><strong>ただし条件があります。</strong>
        どちらのプログラムも「<strong>いちばん良かった答えを別に取っておく</strong>」しくみを持っています。
        焼きなまし法では <code>best_length</code>、遺伝的アルゴリズムでは <code>next_population = [list(best_order)]</code> の行です。
        取っておくしくみがなければ、試す力を強めるほど良い答えが壊されてしまい、逆に悪くなります。
        <strong>「守る力」と「試す力」は、両方あって初めて働く</strong>ということです。</p>
        <p style="margin-top:0.6rem"><strong>注意:</strong>
        「温度は高いほど良い」「突然変異は多いほど良い」と言い切ることはできません。
        ステップ数が少なければ、高い温度から冷ましきれずに終わってしまいます。
        今回の20,000ステップ・冷却率0.9995という設定では、温度100.0でも最後には0.005程度まで下がりきるため、うまくいきました。
        設定どうしはたがいに影響し合うので、<strong>実際に試して確かめる</strong>しかありません。</p>"""),
])

body = "\n".join([
    sub,
    section("sec-explanation", "1", "後期の総括と発展手法", explanation),
    section("sec-examples", "2", "例題", examples),
    section("sec-standard", "3", "課題", standard_sec),
    section("sec-notion", "4", "提出まとめ", notion_sec, color="#FFB800"),
    ans,
])

write("15", NAV, body)
