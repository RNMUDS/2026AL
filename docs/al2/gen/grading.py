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
    <p>毎回の「解説スライド3枚」をどう見て、どう点を付けるか。1クラスあたり5〜10分で終わる手順にしてある。</p>
  </div>
</header>

<section id="sec-flow">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">1</div>
      <h2>毎回の採点手順</h2>
    </div>

    <div class="step-card">
      <h4>Step 1: PDFの最後の3枚だけを見る</h4>
      <ul>
        <li>スライドは毎回積み上がるので、<strong>その回に追加された3枚</strong>だけを見ればよい</li>
        <li>1人あたり20〜30秒。下のルーブリック4項目を上から順に見る</li>
      </ul>
    </div>

    <div class="step-card">
      <h4>Step 2: 気になった提出だけ、共有URLで変更履歴を見る</h4>
      <ul>
        <li>Googleスライドを開き、<strong>ファイル → 変更履歴 → 変更履歴を表示</strong></li>
        <li>右側に「いつ・誰が編集したか」が日付ごとに並ぶ</li>
        <li>その回の授業日の前後に編集があれば正常。全部の回が同じ日に固まっていれば、まとめて作っている</li>
      </ul>
      <p style="font-size:0.9rem;color:#888;margin-top:0.5rem">
        全員分を見る必要はない。下の「疑わしいサイン」に当てはまったものだけでよい。</p>
    </div>

    <div class="step-card">
      <h4>Step 3: 点を付ける</h4>
      <ul>
        <li>1回10点 × 15回 ＝ 150点。学期末に100点へ換算する</li>
        <li>提出があれば最低3点。未提出は0点</li>
      </ul>
    </div>
  </div>
</section>

<section id="sec-rubric">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">2</div>
      <h2>ルーブリック（毎回10点）</h2>
    </div>

    <table>
      <tr><th>観点</th><th>配点</th><th>満点</th><th>半分</th><th>0点</th></tr>
      <tr>
        <td><strong>図を自分で作ったか</strong></td><td>3</td>
        <td>自分で図形を並べた図。指定の3要素がすべて入っている</td>
        <td>自分で作っているが、3要素のうち1つが抜けている</td>
        <td>授業ページの図のスクリーンショット／図がない</td>
      </tr>
      <tr>
        <td><strong>自分で動かした証拠</strong></td><td>2</td>
        <td>VS Codeのウィンドウ全体。フォルダ名 <code>AL2/NoXX</code> とファイル名が読める</td>
        <td>実行結果は写っているが、フォルダ名が読めない</td>
        <td>スクリーンショットがない／教材の実行結果画像を貼っている</td>
      </tr>
      <tr>
        <td><strong>数値を根拠にしたか</strong></td><td>3</td>
        <td>自分の実行結果の数値を引用し、説明と一致している</td>
        <td>数値はあるが、説明とのつながりが弱い</td>
        <td>数値がない／数値と説明が食い違っている</td>
      </tr>
      <tr>
        <td><strong>言葉が自分のものか</strong></td><td>2</td>
        <td>専門用語を言いかえ、前期未履修者に伝わる書き方になっている</td>
        <td>一部は自分の言葉だが、教材の文が混ざっている</td>
        <td>教材や生成AIの文をそのまま貼っている</td>
      </tr>
    </table>

    <div class="concept-box">
      <h4>迷ったときの目安</h4>
      <ul class="point-list">
        <li><strong>図の出来ばえは問わない</strong>。線が曲がっていても、自分で引いていれば満点でよい</li>
        <li><strong>結論が間違っていても減点しない</strong>。自分の数値を根拠に考えていれば点になる</li>
        <li><strong>日本語の巧拙は問わない</strong>。見るのは「教材の写しでないか」だけ</li>
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

    <p style="margin-bottom:1.2rem">次のどれかに当てはまったら、共有URLから変更履歴を確認する。</p>

    <div class="flag">
      <strong>図が授業ページの図とまったく同じ</strong><br>
      色・フォント・配置が一致していれば、スクリーンショットを貼っている。図の点（3点）は0。
    </div>
    <div class="flag">
      <strong>スクリーンショットにフォルダ名が写っていない</strong><br>
      ターミナルの文字だけを切り取ったもの、教材の実行結果画像の貼りつけ。証拠の点（2点）は0。
    </div>
    <div class="flag">
      <strong>数値と説明が食い違っている</strong><br>
      生成AIの文をそのまま貼ると起きやすい。たとえば「600倍速かった」と書きながら、貼った画像は20倍。
    </div>
    <div class="flag">
      <strong>専門用語が唐突に増える</strong><br>
      授業で扱っていない語（「償却計算量」「A*」など）が出てきたら、書いた本人が理解していない可能性が高い。
      次回の授業で口頭で1つ質問すれば分かる。
    </div>
    <div class="flag">
      <strong>変更履歴が1日に固まっている</strong><br>
      15回ぶんが同じ日に作られていれば、まとめて作っている。
      該当する回をさかのぼって減点するか、口頭確認に切りかえる。
    </div>

    <div class="concept-box">
      <h4>それでも残る抜け道と、その扱い</h4>
      <p style="font-size:0.95rem">
        生成AIに文章だけ書かせ、図とスクリーンショットは自分で用意する、という使い方は防げない。
        ただしその場合でも、<strong>図を作る・自分の環境で動かす・自分の数値を拾う</strong>という作業は本人がしている。
        そこまでやれば理解は進むので、実害は小さいと考えてよい。
      </p>
      <p style="font-size:0.95rem;margin-top:0.6rem">
        逆に、完全に丸投げしようとすると「自分で作った図」と「自分のフォルダ名が写ったスクリーンショット」で必ず詰まる。
        この2つが、この課題の要になっている。
      </p>
    </div>
  </div>
</section>

<section id="sec-final">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#FFB800">4</div>
      <h2>学期末の扱い</h2>
    </div>

    <div class="step-card">
      <h4>成績</h4>
      <ul>
        <li>15回 × 10点 ＝ 150点を、100点満点に換算する（点数 ÷ 1.5）</li>
        <li>第13回・第14回は自分の作品についての回なので、内容は人によって違う。ルーブリックは同じでよい</li>
        <li>第15回の提出をもって、45枚のスライドが完成する。全体を通して見ると、その学生の理解度がひと目で分かる</li>
      </ul>
    </div>

    <div class="step-card">
      <h4>欠席・遅れの扱い</h4>
      <ul>
        <li>スライドは1本を育てる形なので、欠席回はあとから足せる</li>
        <li>ただし変更履歴に日付が残るため、遅れて出したことは分かる。減点するかどうかは運用で決める</li>
      </ul>
    </div>

    <div class="note-warn">
      <strong>学生に見せてよいページです。</strong>評価の観点は各回のページにも同じ内容が載せてあります。
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
       '<a href="#sec-flow">採点手順</a>'
       '<a href="#sec-rubric">ルーブリック</a>'
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
