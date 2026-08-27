"""データ行の桁に合わせた見出し行を計算する。
使い方: python3 fixhdr.py <実行結果の中の見出し行番号> <ファイル名> <見出し語1> <見出し語2> ...
"""
import pathlib, re, subprocess, sys, unicodedata
def w(t): return sum(2 if unicodedata.east_asian_width(c) in "WFA" else 1 for c in t)

name, header_line = sys.argv[1], int(sys.argv[2])
labels = sys.argv[3:]
out = subprocess.run([sys.executable, str(pathlib.Path("src") / name)],
                     capture_output=True, text=True, timeout=600).stdout.splitlines()
data = out[header_line]          # 見出しの次の行（データ行）
spans, pos = [], 0
for part in re.split(r"( {2,})", data):
    ww = w(part)
    if not part.startswith("  ") and part.strip():
        spans.append((pos, pos + ww))
    pos += ww
print(f"データ行: {data!r}")
print(f"列の位置: {spans}")
if len(spans) != len(labels):
    print(f"!! 列の数({len(spans)})と見出しの数({len(labels)})が合わない")
    sys.exit(1)
# 1列目は左そろえ、残りは右そろえで見出しを組み立てる
line = labels[0]
for k in range(1, len(spans)):
    end = spans[k][1]
    gap = end - w(line) - w(labels[k])
    if gap < 1:
        gap = 1
    line += " " * gap + labels[k]
print(f"見出し  : {line!r}   （幅 {w(line)}）")
