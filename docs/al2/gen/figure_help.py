# -*- coding: utf-8 -*-
"""標準課題の「描き方」を示す小さな図。課題セクションに入れる（答えは含まない）。"""
from common import fig, GREEN, AMBER, GRAY


def tree_help(unit="か所", root="出発点", names=("A", "B"), unit_word="分"):
    """枝分かれ図（木）とは何かを、2か所だけ回る小さな例で示す。
    3か所の答えは含まない（学生が自分で6本に広げる）。"""
    a, b = names
    s = [f'        <text x="350" y="24" text-anchor="middle" fill="{GREEN}" font-weight="700" font-size="15">'
         f'枝分かれ図（木）の描き方 ── 2{unit}を回る場合の例</text>',
         f'        <text x="350" y="44" text-anchor="middle" fill="{GRAY}" font-size="11">'
         '上から下へ「次にどこへ行くか」で枝を分け、いちばん下に合計を書く</text>']

    def box(x, y, w, h, text, color="#444", fill="#141414", tcolor="#E0E0E0", bold=False):
        s.append(f'        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        weight = ' font-weight="700"' if bold else ""
        s.append(f'        <text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" fill="{tcolor}" font-size="12"'
                 f'{weight}>{text}</text>')

    def arrow(x1, y1, x2, y2):
        s.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="2"/>')
        s.append(f'        <polygon points="{x2},{y2} {x2 - 5},{y2 - 9} {x2 + 5},{y2 - 9}" fill="#777"/>')

    # 根
    box(230, 62, 80, 30, root, GREEN, "#0f1f08", GREEN, True)
    # 1段目: 2つに分かれる
    for i, first in enumerate((a, b)):
        x = 130 + i * 200
        arrow(270, 92, x + 40, 122)
        box(x, 124, 80, 30, first)
        second = b if first == a else a
        arrow(x + 40, 154, x + 40, 184)
        box(x, 186, 80, 30, second)
        arrow(x + 40, 216, x + 40, 246)
        box(x, 248, 80, 30, f"{root}へ戻る", "#444", "#141414", "#bbb")
        arrow(x + 40, 278, x + 40, 308)
        box(x - 6, 310, 92, 30, f"合計 ○○{unit_word}", AMBER, "#1a1200", AMBER, True)
    # 説明
    s.append(f'        <text x="470" y="140" fill="{GRAY}" font-size="11">← 最初に行く場所で枝が分かれる</text>')
    s.append(f'        <text x="470" y="202" fill="{GRAY}" font-size="11">← 残りの場所（2{unit}なら1つしか残らない）</text>')
    s.append(f'        <text x="470" y="326" fill="{AMBER}" font-size="11">← 枝の先に、その順番の合計を書く</text>')
    s.append(f'        <text x="350" y="366" text-anchor="middle" fill="#E0E0E0" font-size="12">'
             f'3{unit}を回るときは、1段目が3つ、2段目が2つに分かれて、枝の先は 3×2×1 = 6本になる</text>')
    s.append(f'        <text x="350" y="386" text-anchor="middle" fill="{GRAY}" font-size="11">'
             '合計は自分の数値で実行した結果から写す。いちばん短い枝に★などの印を付ける</text>')
    return fig(700, 400, "\n".join(s))
