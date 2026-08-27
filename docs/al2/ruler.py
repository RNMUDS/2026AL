"""実行結果を、表示幅つきで表示する（桁ぞろえの確認用）"""
import pathlib, subprocess, sys, unicodedata
def w(t): return sum(2 if unicodedata.east_asian_width(c) in "WFA" else 1 for c in t)
name = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 999
out = subprocess.run([sys.executable, str(pathlib.Path("src") / name)],
                     capture_output=True, text=True, timeout=600).stdout
for i, line in enumerate(out.splitlines()[:limit], 1):
    mark = " <<<" if w(line) > 100 else ""
    print(f"{w(line):>3}| {line}{mark}")
