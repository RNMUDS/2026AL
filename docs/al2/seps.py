"""区切り線（---- や ====）の長さが、その下の表の幅とずれていないか調べる"""
import pathlib, re, subprocess, sys, unicodedata
def w(t): return sum(2 if unicodedata.east_asian_width(c) in "WFA" else 1 for c in t)
bad = []
for path in sorted(pathlib.Path("src").glob("*.py")):
    lines = subprocess.run([sys.executable, str(path)], capture_output=True,
                           text=True, timeout=600).stdout.splitlines()
    for i, line in enumerate(lines):
        if not re.fullmatch(r"[-=]{10,}", line.strip()):
            continue
        block = []
        for j in range(i + 1, min(i + 8, len(lines))):
            t = lines[j]
            if not t.strip() or re.fullmatch(r"[-=]{10,}", t.strip()):
                break
            block.append(w(t))
        if block:
            widest = max(block)
            diff = w(line) - widest
            if abs(diff) >= 4:
                bad.append((path.name, i + 1, w(line), widest, diff))
for name, ln, sep, tbl, diff in bad:
    print(f"  {name} {ln}行目: 区切り線{sep}桁 / 表{tbl}桁 (差 {diff:+d})")
print("  ずれなし" if not bad else "")
