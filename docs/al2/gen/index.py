# -*- coding: utf-8 -*-
"""学生に配布する目次ページ（docs/al2/index.html）を組み立てる。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from build import SESSIONS, ORDER   # noqa: E402

GREEN, AMBER, GRAY = "#76B900", "#FFB800", "#888888"

TOPICS = {
    "01": ("復習", "二分探索・幅優先探索・全探索"),
    "02": ("復習", "幅優先探索・深さ優先探索・キュー・スタック"),
    "03": ("グラフ", "頂点・辺・隣接リスト・隣接行列"),
    "04": ("グラフ", "重み・コスト・重み付きグラフ"),
    "05": ("最短経路", "ダイクストラ法・確定・緩和"),
    "06": ("最短経路", "優先度付きキュー・heapq"),
    "07": ("最短経路", "床コスト迷路・計算量"),
    "08": ("巡回", "巡回セールスマン問題・階乗・NP困難"),
    "09": ("巡回", "貪欲法・局所最適・近似解"),
    "10": ("巡回", "動的計画法・bitDP・ビット演算"),
    "11": ("整理", "アルゴリズムの使い分け"),
    "12": ("応用", "ナップサック問題・アイテム収集"),
    "13": ("制作", "設計シート・動く最小版"),
    "14": ("制作", "テスト・デバッグ・レポート"),
    "15": ("まとめ", "焼きなまし法・遺伝的アルゴリズム"),
}

PHASE_COLOR = {"復習": "#888888", "グラフ": GREEN, "最短経路": GREEN,
               "巡回": AMBER, "整理": "#4FC3F7", "応用": AMBER,
               "制作": "#4FC3F7", "まとめ": GREEN}


def jp_date(text):
    y, m, d = text.split("-")
    return f"{int(m)}月{int(d)}日"


cards = []
for num in ORDER:
    title, lead, date, _next = SESSIONS[num]
    phase, keywords = TOPICS[num]
    color = PHASE_COLOR[phase]
    cards.append(f"""      <a class="week-card" href="session{num}.html">
        <div class="week-head">
          <span class="week-num">第{int(num)}回</span>
          <span class="week-phase" style="background:{color}22;color:{color};border:1px solid {color}55">{phase}</span>
          <span class="week-date">{jp_date(date)}（水）</span>
        </div>
        <h3>{title}</h3>
        <p>{lead}</p>
        <p class="week-keywords">{keywords}</p>
      </a>""")

extra_css = """
.lead { font-size: 1.05rem; margin-bottom: 1.5rem; }
.week-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }
.week-card { display: block; background: #1A1A1A; border: 1px solid #2a2a2a; border-left: 4px solid #76B900;
  border-radius: 14px; padding: 1.1rem 1.3rem; text-decoration: none; color: inherit; transition: all 0.2s; }
.week-card:hover { border-color: #4A7A00; border-left-color: #93D500; background: #1e1e1e; transform: translateY(-2px); }
.week-head { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem; flex-wrap: wrap; }
.week-num { font-size: 0.95rem; font-weight: 900; color: #76B900; }
.week-phase { font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.6rem; border-radius: 100px; }
.week-date { font-size: 0.75rem; color: #666; margin-left: auto; }
.week-card h3 { font-size: 1.02rem; font-weight: 700; margin-bottom: 0.45rem; line-height: 1.4; }
.week-card p { font-size: 0.86rem; color: #999; line-height: 1.7; }
.week-keywords { margin-top: 0.5rem; font-size: 0.78rem; color: #666; }
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1rem 0; }
"""

body = f"""
<header class="hero">
  <div class="container">
    <div class="hero-badge">2026年度後期 ─ 水曜4限</div>
    <h1>アルゴリズム論及び演習II</h1>
    <p>最短経路と最適化のアルゴリズムを、コードを動かしながら学ぶ全15回。担当: 中村 亮太</p>
  </div>
</header>

<section id="sec-about">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">1</div>
      <h2>この授業について</h2>
    </div>

    <p class="lead">
      前期のアルゴリズム論及び演習Iでは「たくさんのデータから目的の1つを探す」方法を学びました。
      後期は一歩進んで、<strong>やり方が何通りもあるとき、いちばん良いやり方を見つける</strong>方法を学びます。
      カーナビの経路案内、宅配便の配送計画、工場の作業順番は、すべて同じ形の問題として解けます。
    </p>

    <div class="info-grid">
      <div class="mini-card">
        <h5>身につくこと</h5>
        <p>地図や迷路をグラフに書き直し、ダイクストラ法・貪欲法・動的計画法で最適な答えを求められるようになる。</p>
      </div>
      <div class="mini-card">
        <h5>使うもの</h5>
        <p>Visual Studio Code と Python。前期に用意した環境をそのまま使う。デスクトップに AL2 フォルダを作って進める。</p>
      </div>
      <div class="mini-card">
        <h5>評価方法</h5>
        <p>定期試験なし。毎回の演習課題の提出で100%。Notionに記録し、PDFに書き出してManabaに提出する。</p>
      </div>
    </div>

    <div class="recap">
      前期（アルゴリズム論及び演習I）の資料は
      <a href="../sessions/session01.html" style="color:#93D500">こちら</a>から見られます。
      後期の説明では、前期の内容をたびたび参照します。
    </div>

    <div class="concept-box">
      <h4>毎回の進め方</h4>
      <table>
        <tr><th>順番</th><th>すること</th></tr>
        <tr><td>1</td><td>ページの上にある<strong>提出ガイド</strong>で、今回の提出物を確かめる</td></tr>
        <tr><td>2</td><td><strong>説明</strong>を読み、図とアニメーションで仕組みをつかむ</td></tr>
        <tr><td>3</td><td><strong>例題</strong>のコードをコピーして自分のパソコンで実行し、実行結果と見比べる</td></tr>
        <tr><td>4</td><td><strong>標準課題</strong>に取り組み、答えをNotionに記録する</td></tr>
        <tr><td>5</td><td>NotionをPDFに書き出して<strong>Manabaに提出</strong>する</td></tr>
      </table>
      <p style="font-size:0.95rem;margin-top:0.8rem">
        解答例は各ページのいちばん下にあります。<strong>次回の授業が始まる時刻に自動で公開</strong>されます。
      </p>
    </div>
  </div>
</section>

<section id="sec-weeks">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#76B900">2</div>
      <h2>全15回</h2>
    </div>

    <div class="week-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>

<section id="sec-flow">
  <div class="container">
    <div class="section-header">
      <div class="section-num" style="background:#FFB800">3</div>
      <h2>後期の流れ</h2>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 700 200" width="700" xmlns="http://www.w3.org/2000/svg" font-family="Noto Sans JP, sans-serif" style="background:#0A0A0A">
        <text x="350" y="28" text-anchor="middle" fill="#76B900" font-weight="700" font-size="15">5つの段階を、15回かけて進む</text>
        <rect x="20" y="56" width="124" height="92" rx="12" fill="#1A1A1A" stroke="#555" stroke-width="1.5"/>
        <text x="82" y="80" text-anchor="middle" fill="#888" font-size="11">第1〜2回</text>
        <text x="82" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">前期の復習</text>
        <text x="82" y="124" text-anchor="middle" fill="#888" font-size="10">探索を思い出す</text>
        <line x1="144" y1="102" x2="152" y2="102" stroke="#555" stroke-width="2"/>
        <rect x="154" y="56" width="124" height="92" rx="12" fill="#1A1A1A" stroke="#76B900" stroke-width="1.5"/>
        <text x="216" y="80" text-anchor="middle" fill="#888" font-size="11">第3〜4回</text>
        <text x="216" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">グラフ</text>
        <text x="216" y="124" text-anchor="middle" fill="#888" font-size="10">地図をデータにする</text>
        <line x1="278" y1="102" x2="286" y2="102" stroke="#555" stroke-width="2"/>
        <rect x="288" y="56" width="124" height="92" rx="12" fill="#1A1A1A" stroke="#76B900" stroke-width="1.5"/>
        <text x="350" y="80" text-anchor="middle" fill="#888" font-size="11">第5〜7回</text>
        <text x="350" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">ダイクストラ法</text>
        <text x="350" y="124" text-anchor="middle" fill="#888" font-size="10">最短コストの道</text>
        <line x1="412" y1="102" x2="420" y2="102" stroke="#555" stroke-width="2"/>
        <rect x="422" y="56" width="124" height="92" rx="12" fill="#1A1A1A" stroke="#FFB800" stroke-width="1.5"/>
        <text x="484" y="80" text-anchor="middle" fill="#888" font-size="11">第8〜12回</text>
        <text x="484" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">最適化</text>
        <text x="484" y="124" text-anchor="middle" fill="#888" font-size="10">いちばん良い順番</text>
        <line x1="546" y1="102" x2="554" y2="102" stroke="#555" stroke-width="2"/>
        <rect x="556" y="56" width="124" height="92" rx="12" fill="#1A1A1A" stroke="#4FC3F7" stroke-width="1.5"/>
        <text x="618" y="80" text-anchor="middle" fill="#888" font-size="11">第13〜15回</text>
        <text x="618" y="102" text-anchor="middle" fill="#E0E0E0" font-size="12" font-weight="700">作品制作</text>
        <text x="618" y="124" text-anchor="middle" fill="#888" font-size="10">自分のテーマで作る</text>
        <text x="350" y="180" text-anchor="middle" fill="#FFB800" font-size="12" font-weight="700">前期は「探す」。後期は「たくさんある選び方の中から、いちばん良い選び方を見つける」</text>
      </svg>
    </div>

    <div class="note-warn">
      <strong>授業日について:</strong> 各回のカードに書かれている日付は予定です。
      進み方によって前後することがあります。実際の日程はManabaの案内を確認してください。
    </div>
  </div>
</section>
"""

head = (HERE / "tpl" / "head.html").read_text(encoding="utf-8")
head = head.replace("{{TITLE}}", "全15回の目次")
head = head.replace("</style>", extra_css + "</style>")

tail = """<footer>
  <div class="container">
    アルゴリズム論及び演習II ── 2026年度後期 ／ 担当: 中村 亮太
  </div>
</footer>

</body>
</html>
"""

out = HERE / "index.html"
out.write_text(head + "\n<body>\n" + body + "\n" + tail, encoding="utf-8")
print(f"wrote index.html ({out.stat().st_size:,} bytes)")
