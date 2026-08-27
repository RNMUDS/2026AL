"""実行結果の表示幅を調べる:
  1. Windows の標準コンソール（80桁）で折り返さないか
  2. 表になっている部分の桁がそろっているか
全角（W）と、日本語環境で全角扱いになる曖昧幅（A）を2桁として数える。
"""
import pathlib
import re
import subprocess
import sys
import unicodedata

SRC = pathlib.Path(__file__).resolve().parent / "src"


def width(text):
    total = 0
    for ch in text:
        total += 2 if unicodedata.east_asian_width(ch) in "WFA" else 1
    return total


def columns(line):
    """空白2つ以上を区切りとして、各列の（始まる位置, 終わる位置）を返す"""
    spans = []
    pos = 0
    for part in re.split(r"( {2,})", line):
        w = width(part)
        if not part.startswith("  ") and part.strip():
            spans.append((pos, pos + w))
        pos += w
    return spans


over80 = []
ragged = []
for path in sorted(SRC.glob("*.py")):
    out = subprocess.run([sys.executable, str(path)], capture_output=True,
                         text=True, timeout=600).stdout
    lines = out.splitlines()

    widest = 0
    for i, line in enumerate(lines):
        w = width(line)
        widest = max(widest, w)
        if w > 80:
            over80.append((path.name, i + 1, w, line[:50]))

    # 3行以上つづく「列が2つ以上ある行」のかたまりを表とみなす
    block = []
    for line in lines + [""]:
        cols = columns(line)
        if len(cols) >= 3 and line.strip():
            block.append((line, cols))
        else:
            if len(block) >= 3:
                counts = {len(c) for _, c in block}
                if len(counts) == 1:
                    for k in range(len(block[0][1])):
                        # 左そろえなら「始まる位置」、右そろえなら「終わる位置」が一致する
                        starts = {c[k][0] for _, c in block}
                        ends = {c[k][1] for _, c in block}
                        if len(starts) > 1 and len(ends) > 1:
                            ragged.append((path.name, k + 1,
                                           f"始まり{sorted(starts)} 終わり{sorted(ends)}",
                                           block[0][0][:44]))
                            break
            block = []
    print(f"{path.name:<20} 最大幅 {widest:>3}桁 {'← 80桁を超える' if widest > 80 else ''}")

print()
print("=== 80桁を超える行 ===")
for name, ln, w, text in over80:
    print(f"  {name} {ln}行目 {w}桁: {text}")
print("  なし" if not over80 else "")
print("=== 桁がそろっていない表 ===")
for name, col, pos, sample in ragged:
    print(f"  {name} {col}列目の位置がばらばら {pos}: {sample}")
print("  なし" if not ragged else "")
