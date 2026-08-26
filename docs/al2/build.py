#!/usr/bin/env python3
"""アルゴリズム論及び演習II の授業ページを組み立てるビルドスクリプト。

  parts/sNN.html （本文）＋ tpl/head.html ＋ tpl/tail.html → sessionNN.html

使い方:
    python3 build.py            # parts/ にある全ての回を組み立てる
    python3 build.py 01 02      # 指定した回だけ組み立てる

parts/sNN.html の先頭には、ページ内ナビに並べるリンクを次の形式で書く。

    <!--NAV
    提出 #sec-submission
    説明 #sec-explanation
    -->
"""
import pathlib, re, sys, subprocess

HERE = pathlib.Path(__file__).resolve().parent

# 回番号 → (タイトル, ヒーローの説明文, 授業日, 次回の授業日)
SESSIONS = {
    "01": ("ガイダンス・前期の復習",
           "後期の目標（最適化アルゴリズム × ゲーム）を確認し、前期に学んだ探索アルゴリズムを動かして思い出す",
           "2026-09-30", "2026-10-07"),
    "02": ("幅優先探索・深さ優先探索の発展",
           "障害物を増やした迷路で2つの探索を動かし、幅優先探索と深さ優先探索の得意・不得意を比べる",
           "2026-10-07", "2026-10-14"),
    "03": ("グラフとデータ構造の再確認",
           "頂点・辺・重みを図で確かめ、隣接リストと隣接行列という2つの表現方法でグラフをPythonに書き写す",
           "2026-10-14", "2026-10-21"),
    "04": ("重み付きグラフとは",
           "移動のしやすさを「コスト」として扱い、幅優先探索では最短コストを求められない場面を確かめる",
           "2026-10-21", "2026-10-28"),
    "05": ("ダイクストラ法（1）考え方",
           "非負の重み付きグラフで最短経路を求める手順を、手計算で1ステップずつたどる",
           "2026-10-28", "2026-11-04"),
    "06": ("ダイクストラ法（2）実装入門",
           "優先度付きキュー（heapq）の使い方を確認し、ダイクストラ法をPythonで組み上げる",
           "2026-11-04", "2026-11-11"),
    "07": ("ダイクストラ法（3）迷路への応用",
           "床コスト付きの迷路にダイクストラ法を適用し、幅優先探索との違いと実行速度を観察する",
           "2026-11-11", "2026-11-18"),
    "08": ("巡回セールスマン問題（1）概要",
           "全ての都市を1回ずつ巡って出発点に戻る最短ルートを、全探索で求めて計算量の爆発を体感する",
           "2026-11-18", "2026-11-25"),
    "09": ("巡回セールスマン問題（2）貪欲法による近似",
           "最寄りの都市へ順に進む貪欲法を実装し、全探索が出した最適解とのズレを測る",
           "2026-11-25", "2026-12-02"),
    "10": ("巡回セールスマン問題（3）動的計画法",
           "部分集合を使った動的計画法（bitDP）で最適解を求め、全探索・貪欲法と結果と速度を比べる",
           "2026-12-02", "2026-12-09"),
    "11": ("アルゴリズム比較・復習",
           "幅優先探索・深さ優先探索・ダイクストラ法・貪欲法・動的計画法を一覧に整理し、同じ問題で実測して比べる",
           "2026-12-09", "2026-12-16"),
    "12": ("数当てゲーム・パズルの再応用",
           "数当てゲームと宝物集めパズルを、貪欲法と動的計画法の考え方で作り直す",
           "2026-12-16", "2026-12-23"),
    "13": ("実践的課題（1）設計と実装",
           "自分でテーマを決め、最適化アルゴリズムを使った小さなプログラムの設計と実装に取りかかる",
           "2026-12-23", "2027-01-13"),
    "14": ("実践的課題（2）仕上げとレポート作成",
           "動作を検証して作品を仕上げ、使ったアルゴリズムの構成と実行結果をレポートにまとめる",
           "2027-01-13", "2027-01-20"),
    "15": ("まとめ：最適化アルゴリズムの振り返り",
           "後期に学んだ最適化アルゴリズムを体系的に振り返り、次に学ぶ手法（焼きなまし法・遺伝的アルゴリズム）を知る",
           "2027-01-20", "2027-01-20"),
}

ORDER = [f"{i:02d}" for i in range(1, 16)]


def build_nav(current, links):
    """ページ上部の固定ナビを組み立てる。"""
    week = []
    for n in ORDER:
        if n == current:
            week.append(f'<a style="color:#76B900;background:rgba(118,185,0,0.15);'
                        f'font-size:0.6rem;padding:0.2rem 0.5rem;border-radius:4px" '
                        f'href="session{n}.html">{int(n)}</a>')
        else:
            week.append(f'<a style="color:#666;font-size:0.6rem;padding:0.2rem 0.5rem" '
                        f'href="session{n}.html">{int(n)}</a>')
    head = ('<div style="display:flex;align-items:center;gap:0.1rem;margin-right:0.8rem;'
            'border-right:1px solid #333;padding-right:0.8rem">'
            '<span style="color:#666;font-size:0.5rem;white-space:nowrap">回:</span>'
            + " ".join(week) + "</div>")
    body = "\n  ".join(f'<a href="{href}"{cls}>{label}</a>' for label, href, cls in links)
    return f'<nav class="section-nav">{head}\n  {body}\n</nav>'


def parse_nav(text):
    """本文先頭の <!--NAV ... --> を読み取ってリンクの一覧に変換する。"""
    m = re.search(r"<!--NAV\s*(.*?)-->", text, re.S)
    if not m:
        return [], text
    links = []
    for line in m.group(1).strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        label, href = parts[0], parts[1]
        cls = f' class="{parts[2]}"' if len(parts) > 2 else ""
        links.append((label, href, cls))
    return links, text[m.end():].lstrip("\n")


def build(num):
    part = HERE / "parts" / f"s{num}.html"
    if not part.exists():
        print(f"skip {num} (parts/s{num}.html がない)")
        return
    title, lead, _date, next_date = SESSIONS[num]
    body = part.read_text(encoding="utf-8")
    links, body = parse_nav(body)

    head = (HERE / "tpl" / "head.html").read_text(encoding="utf-8")
    head = head.replace("{{TITLE}}", f"第{int(num)}回: {title}")
    tail = (HERE / "tpl" / "tail.html").read_text(encoding="utf-8")
    tail = tail.replace("{{FOOTER}}", f"第{int(num)}回 {title}")

    hero = f"""
<header class="hero">
  <div class="container">
    <div class="hero-badge">アルゴリズム論及び演習II ─ 2026年度後期</div>
    <h1>第{int(num)}回: {title}</h1>
    <p>{lead}</p>
  </div>
</header>
"""
    body = body.replace("{{RELEASE}}", f"{next_date}T14:40")

    out = HERE / f"session{num}.html"
    out.write_text(head + "\n<body>\n\n"
                   + build_nav(num, links) + "\n" + hero + "\n" + body + "\n" + tail,
                   encoding="utf-8")
    print(f"built session{num}.html  ({out.stat().st_size:,} bytes)")

    # 解答例を暗号化する（平文のまま公開しない）
    if 'id="answers-content"' in out.read_text(encoding="utf-8"):
        r = subprocess.run(["node", str(HERE / "encrypt-answers.js"),
                            "internship-career", str(out)],
                           capture_output=True, text=True)
        print("  " + r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "  (encrypt skipped)")


if __name__ == "__main__":
    targets = sys.argv[1:] or ORDER
    for n in targets:
        build(n)
