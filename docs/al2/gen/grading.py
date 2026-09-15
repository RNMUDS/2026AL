# -*- coding: utf-8 -*-
"""教員用の採点ガイド（docs/al2/grading.html）を組み立てる。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent

extra_css = """
.step-card { background:#1A1A1A; border:1px solid #333; border-left:4px solid #76B900;
  border-radius:12px; padding:1.1rem 1.4rem; margin-bottom:1rem; }
.step-card h4 { color:#76B900; font-size:1rem; margin-bottom:0.5rem; }
.step-card ol, .step-card ul { padding-left:1.4rem; font-size:0.93rem; line-height:1.95; color:#ccc; }
.flag { background:#2b1a00; border-left:4px solid #FF5252; border-radius:10px;
  padding:1rem 1.2rem; margin:1rem 0; }
.flag strong { color:#FF5252; }
"""

body = """
<header class="hero">
  <div class="container">
    <div class="hero-badge">教員用 ─ アルゴリズム論及び演習II 2026年度後期</div>
    <h1>採点ガイド</h1>
    <p>毎回100点＝標準課題70点（Googleスライド）＋発展課題30点（アプリ作品の今回の到達点）。どう見て、どう点を付けるか。標準課題は1クラスあたり5〜10分で終わる手順にしてある。</p>
  </div>
</header>

<section id="sec-flow">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">1</div>
      <h2>標準課題の採点手順（毎回）</h2>
    </div>

    <div class="step-card">
      <h4>Step 1: PDFを開き、その回の「課題要件」だけを確かめる</h4>
      <ul>
        <li>スライドは回ごとに別ファイル。枚数は自由なので、複数枚あれば全部を見る</li>
        <li>各回のページの標準課題に「課題要件（満点の条件）」が1文で書いてある。見るのはそれだけ</li>
        <li>条件は毎回「図の数値が、自分の数値で動かした実行結果と一致しているか」の形になっている。図の出来ばえは問わない</li>
        <li>1人あたり15〜20秒</li>
      </ul>
    </div>

    <div class="step-card">
      <h4>Step 2: 減点の判定</h4>
      <ul>
        <li><strong>画像の貼り付け</strong>: 共有URLでスライドを開き、図をクリックする。図形なら個々の四角や矢印が選べる。画像なら1枚の絵として選ばれる</li>
        <li><strong>例題の数値のまま</strong>: 授業ページの例題と同じ数値（新宿→渋谷7分、迷路 S.....# など）が図に残っていれば、自分の数値にしていない</li>
        <li><strong>数値の不一致</strong>: 図の数値が実行結果としてありえない（幅優先探索の歩数が飛んでいる、heapq の親が子より大きい、など）</li>
        <li><strong>文章が3行以上</strong></li>
      </ul>
    </div>

    <div class="step-card">
      <h4>Step 3: 点を付ける</h4>
      <ul>
        <li>要件を満たした期限内の提出は70点。遅れた提出、要件を満たしていない提出は減点（目安: 要件不足は30点、次回授業日以降の提出は0点）。未提出は0点</li>
      </ul>
    </div>
  </div>
</section>

<section id="sec-rubric">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#FFB800">2</div>
      <h2>発展課題の採点手順（毎回・30点）</h2>
    </div>

    <p style="margin-bottom:1.2rem">
      発展課題は任意。AI の利用は認めている。4つの作品を3〜5回に分けて育てる形で、各回のページに<strong>「今回の到達点」（満たすこと3つ）</strong>が書いてある。
      見るのはその3つを満たしているかだけで、コードの良し悪しは見ない。
      <strong>3つとも満たしていれば30点、1つでも欠けていれば0点</strong>（部分点なし）。締切後は受けつけない。
      到達点は5つの要件（下の表）を回ごとに分けたものなので、最後の回の到達点を満たした作品は5要件をすべて満たしている。
    </p>

    <table>
      <tr><th>#</th><th>要件</th><th>確かめ方（1〜2分）</th></tr>
      <tr><td>1</td><td><strong>自分のデータが入っている</strong></td><td>作品スライドのスクリーンショットに、例題と違う駅名・迷路・座標が出ているか</td></tr>
      <tr><td>2</td><td><strong>画面で入力を変えられる</strong></td><td>スクリーンショットにボタン・入力欄・スライダーが写っているか。疑わしければ <code>python app.py</code> で開く</td></tr>
      <tr><td>3</td><td><strong>結果が図で表示される</strong></td><td>経路の線・色付きのマスなどが画面に描かれているか。文字だけなら0</td></tr>
      <tr><td>4</td><td><strong>変な入力で落ちない</strong></td><td><code>app.py</code> を開き、空・範囲外を扱う <code>if</code> があるか。疑わしければ動かして空欄で実行する</td></tr>
      <tr><td>5</td><td><strong>例題と同じ答えになる</strong></td><td>作品スライドに「アプリの答え」と「例題の答え」が並んで書かれ、一致しているか</td></tr>
    </table>

    <div class="concept-box">
      <h4>発展課題のスライドに入っているもの</h4>
      <ul class="point-list">
        <li>その回の到達点に書かれた<strong>証拠</strong>（画面のスクリーンショット、一致した数値、設計シートなど。各回のページの「発展課題のスライドに貼るもの」）</li>
        <li>単元の最後の回は、<strong>アルゴリズムがアプリのどこで働くか</strong>を図形で描いた図。画像の貼り付けなら0点</li>
        <li><code>app.py</code> が添付されている。疑わしければ <code>python app.py</code> で開く（1〜2分）</li>
      </ul>
    </div>

    <div class="concept-box">
      <h4>迷ったときの目安</h4>
      <ul class="point-list">
        <li><strong>コードが AI の出力そのものでも減点しない</strong>。到達点の「例題と一致」を自分で確かめている時点で、動作の理解はしている</li>
        <li><strong>前の回の到達点を満たしていなくても、今回の到達点を満たしていれば30点</strong>。途中の回から始めてもよい</li>
        <li><strong>見た目の良し悪しは問わない</strong>。要件3は「図が描かれているか」だけ</li>
        <li>動かして確かめるのは、スクリーンショットだけでは判断できない作品だけでよい</li>
      </ul>
    </div>
  </div>
</section>

<section id="sec-flags">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#FFB800">3</div>
      <h2>疑わしいサイン</h2>
    </div>

    <div class="flag">
      <strong>図が授業ページの図とまったく同じ</strong><br>
      色・配置・数値が一致していれば、スクリーンショットの貼り付けか、例題の数値のまま描いている。減点。
    </div>
    <div class="flag">
      <strong>図をクリックすると1枚の絵として選ばれる</strong><br>
      AI が生成した画像、または手描きの写真。減点。
    </div>
    <div class="flag">
      <strong>図の数値が実行結果としてありえない</strong><br>
      幅優先探索の歩数が同心円状になっていない、6通りの合計時間が全部同じ、など。自分で動かしていない。減点。
    </div>

    <div class="concept-box">
      <h4>この課題設計のねらい</h4>
      <p style="font-size:0.95rem">
        図を Google スライドの図形で描かせるのは、<strong>AI の出力をそのまま貼れない形式</strong>だからである。
        AI に一般的な図を作らせても、自分の数値で動かした結果と一致するように図形に写す作業は本人がするしかなく、
        写す途中でアルゴリズムの動きを追うことになる（自己説明の効果）。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        発展課題は逆に AI を使う前提で、<strong>1回の指示ではそろわない到達点</strong>を毎回置いている。
        往復して直す過程で、「例題との一致」を通じて正しさを自分で確かめることになる。
        部分点を出さないのは、到達点を満たす人を限ることで採点を確実にするためである。
      </p>
    </div>
  </div>
</section>

<section id="sec-final">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">4</div>
      <h2>学期末の扱い</h2>
    </div>

    <div class="step-card">
      <h4>成績</h4>
      <ul>
        <li>毎回100点（標準70＋発展30）。成績は<strong>15回の平均</strong></li>
        <li>標準を全回満点なら70点。発展の到達点を満たした回だけ、その回に30点が足される</li>
      </ul>
      <table style="margin-top:0.8rem">
        <tr><th>例</th><th>標準</th><th>発展</th><th>平均</th></tr>
        <tr><td>毎回満点、発展なし</td><td>70×15</td><td>0</td><td>70.0</td></tr>
        <tr><td>毎回満点、発展10回</td><td>70×15</td><td>30×10</td><td>90.0</td></tr>
        <tr><td>毎回満点、発展15回</td><td>70×15</td><td>30×15</td><td>100.0</td></tr>
        <tr><td>満点12回・減点（30点）3回、発展3回</td><td>70×12＋30×3</td><td>30×3</td><td>68.0</td></tr>
      </table>
    </div>

    <div class="step-card">
      <h4>欠席・遅れの扱い</h4>
      <ul>
        <li>標準課題の締切は次回授業の開始時刻。それを過ぎた提出は減点（目安30点）、次回授業日以降は0点</li>
        <li>欠席した回は0点として平均に入る（15回の平均なので、1回の欠席で最大 4.7 点下がる）</li>
        <li>発展課題は締切後に受けつけない。何回取り組んでもよい</li>
      </ul>
    </div>

    <div class="note-warn">
      <strong>学生に見せてよいページです。</strong>配点と「課題要件」は各回のページにも同じ内容が載せてあります。
      何を見て点を付けるかを先に示しておくほうが、提出の質が上がります。
    </div>
  </div>
</section>
"""

head = (HERE / "tpl" / "head.html").read_text(encoding="utf-8")
head = head.replace("{{TITLE}}", "採点ガイド（教員用）")
head = head.replace("</style>", extra_css + "</style>")

nav = ('<nav class="section-nav">'
       '<a href="index.html">← 全15回の目次へ</a>'
       '<a href="#sec-flow">標準課題</a>'
       '<a href="#sec-rubric">発展課題</a>'
       '<a href="#sec-flags">疑わしいサイン</a>'
       '<a href="#sec-final">学期末</a>'
       '</nav>')

tail = """<footer>
  <div class="container">
    アルゴリズム論及び演習II ── 採点ガイド（教員用）
  </div>
</footer>

</body>
</html>
"""

out = HERE / "grading.html"
out.write_text(head + "\n<body>\n" + nav + body + "\n" + tail, encoding="utf-8")
print(f"wrote grading.html ({out.stat().st_size:,} bytes)")
