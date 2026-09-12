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
    <p>標準課題（毎回スライド1枚）と発展課題（単元ごとのアプリ作品）をどう見て、どう点を付けるか。標準課題は1クラスあたり5〜10分で終わる手順にしてある。</p>
  </div>
</header>

<section id="sec-flow">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">1</div>
      <h2>標準課題の採点手順（毎回）</h2>
    </div>

    <div class="step-card">
      <h4>Step 1: PDFの最後の1枚を見て、その回の「○になる条件」だけを確かめる</h4>
      <ul>
        <li>スライドは毎回積み上がるので、<strong>その回に追加された1枚</strong>だけを見ればよい</li>
        <li>各回のページの標準課題に「○（満点）になる条件」が1文で書いてある。見るのはそれだけ</li>
        <li>条件は毎回「図の数値が、自分の数値で動かした実行結果と一致しているか」の形になっている。図の出来ばえは問わない</li>
        <li>1人あたり15〜20秒</li>
      </ul>
    </div>

    <div class="step-card">
      <h4>Step 2: △の判定</h4>
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
        <li>○ 5点／△ 2点／未提出 0点。締切（次回授業の開始時刻）後の提出は△まで、次回授業日以降は0点</li>
        <li>15回で75点になるが、<strong>70点で打ち切る</strong>（1回ぶんの余裕）</li>
      </ul>
    </div>
  </div>
</section>

<section id="sec-rubric">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#FFB800">2</div>
      <h2>発展課題の採点手順（単元ごと・4作品）</h2>
    </div>

    <p style="margin-bottom:1.2rem">
      発展課題は任意。AI の利用は認めている。見るのは<strong>5つの要件を満たしているか</strong>だけで、コードの良し悪しは見ない。
      1作品10点（要件1つにつき2点）。締切（その単元の次の回の授業開始時刻）後は受けつけない。
    </p>

    <table>
      <tr><th>#</th><th>要件</th><th>確かめ方（1〜2分）</th></tr>
      <tr><td>1</td><td><strong>自分のデータが入っている</strong></td><td>作品スライドのスクリーンショットに、例題と違う駅名・迷路・座標が出ているか</td></tr>
      <tr><td>2</td><td><strong>画面で入力を変えられる</strong></td><td>スクリーンショットにボタン・入力欄・スライダーが写っているか。疑わしければ <code>streamlit run app.py</code> で開く</td></tr>
      <tr><td>3</td><td><strong>結果が図で表示される</strong></td><td>経路の線・色付きのマスなどが画面に描かれているか。文字だけなら0</td></tr>
      <tr><td>4</td><td><strong>変な入力で落ちない</strong></td><td><code>app.py</code> を開き、空・範囲外を扱う <code>if</code> があるか。疑わしければ動かして空欄で実行する</td></tr>
      <tr><td>5</td><td><strong>例題と同じ答えになる</strong></td><td>作品スライドに「アプリの答え」と「例題の答え」が並んで書かれ、一致しているか</td></tr>
    </table>

    <div class="concept-box">
      <h4>作品スライドに必ず入っているもの</h4>
      <ul class="point-list">
        <li>アプリの画面のスクリーンショット（要件1〜3をここで見る）</li>
        <li><strong>アルゴリズムがアプリのどこで働くか</strong>を図形で描いた図。この図がないか、画像の貼り付けなら、その作品は受けつけない</li>
        <li>例題と同じ答えになった証拠（2つの数値を並べたもの）</li>
      </ul>
    </div>

    <div class="concept-box">
      <h4>迷ったときの目安</h4>
      <ul class="point-list">
        <li><strong>コードが AI の出力そのものでも減点しない</strong>。要件5（例題と一致）を自分で確かめている時点で、動作の理解はしている</li>
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
      色・配置・数値が一致していれば、スクリーンショットの貼り付けか、例題の数値のまま描いている。△。
    </div>
    <div class="flag">
      <strong>図をクリックすると1枚の絵として選ばれる</strong><br>
      AI が生成した画像、または手描きの写真。△。
    </div>
    <div class="flag">
      <strong>図の数値が実行結果としてありえない</strong><br>
      幅優先探索の歩数が同心円状になっていない、6通りの合計時間が全部同じ、など。自分で動かしていない。△。
    </div>
    <div class="flag">
      <strong>変更履歴が1日に固まっている</strong><br>
      共有URLから <strong>ファイル → 変更履歴 → 変更履歴を表示</strong>。何回ぶんかが同じ日に作られていれば、締切後にまとめて作っている。該当する回は△まで。
    </div>

    <div class="concept-box">
      <h4>この課題設計のねらい</h4>
      <p style="font-size:0.95rem">
        図を Google スライドの図形で描かせるのは、<strong>AI の出力をそのまま貼れない形式</strong>だからである。
        AI に一般的な図を作らせても、自分の数値で動かした結果と一致するように図形に写す作業は本人がするしかなく、
        写す途中でアルゴリズムの動きを追うことになる（自己説明の効果）。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        発展課題は逆に AI を使う前提で、<strong>1回の指示ではそろわない5つの要件</strong>を置いている。
        往復して直す過程で、要件5（例題との一致）を通じて正しさを自分で確かめることになる。
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
        <li>標準課題: 5点 × 15回 ＝ 75点 → <strong>70点で打ち切り</strong></li>
        <li>発展課題: 10点 × 4作品 ＝ 40点</li>
        <li>合計 <strong>100点で打ち切り</strong>。標準を全回○なら70点。S（90点以上）には発展2作品以上が必要</li>
      </ul>
      <table style="margin-top:0.8rem">
        <tr><th>例</th><th>標準</th><th>発展</th><th>合計</th></tr>
        <tr><td>毎回○、発展なし</td><td>70</td><td>0</td><td>70</td></tr>
        <tr><td>毎回○、発展2作品</td><td>70</td><td>20</td><td>90</td></tr>
        <tr><td>毎回○、発展4作品</td><td>70</td><td>40</td><td>100（打ち切り）</td></tr>
        <tr><td>○12回・△3回、発展1作品</td><td>66</td><td>10</td><td>76</td></tr>
      </table>
    </div>

    <div class="step-card">
      <h4>欠席・遅れの扱い</h4>
      <ul>
        <li>標準課題の締切は次回授業の開始時刻。それを過ぎた提出は△（2点）まで、次回授業日以降は0点</li>
        <li>70点の打ち切りがあるので、1回の欠席は満点に影響しない</li>
        <li>発展課題は締切後に受けつけない（4作品のうち何作品でもよい）</li>
      </ul>
    </div>

    <div class="note-warn">
      <strong>学生に見せてよいページです。</strong>配点と「○になる条件」は各回のページにも同じ内容が載せてあります。
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
