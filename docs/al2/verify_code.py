"""公開HTMLの <pre> から取り出したコードが、検証済みの src/*.py と
完全に一致するか（学生がコピーするコードが正しいか）を確かめる。"""
import html as H
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ng = []
checked = 0

for page in sorted(HERE.glob("session*.html")):
    text = page.read_text(encoding="utf-8")
    for block in re.findall(r"<pre>(.*?)</pre>", text, re.S):
        m = re.search(r'<span class="code-label">(.*?)</span>', block)
        if not m:
            continue
        label = H.unescape(re.sub("<.*?>", "", m.group(1)))
        if "── " not in label:
            continue
        name = label.split("── ")[-1].strip()
        if not name.endswith(".py"):
            continue
        code = H.unescape(re.sub("<.*?>", "",
               re.sub(r'<span class="code-label">.*?</span>', "", block, flags=re.S))).strip("\n")
        src = HERE / "src" / name
        if not src.exists():
            print(f"  {page.name}: {name} は src にない（課題用の断片）")
            continue
        checked += 1
        expected = src.read_text(encoding="utf-8").rstrip("\n")
        if code != expected:
            ng.append((page.name, name))
            # どこが違うか1行だけ示す
            for i, (a, b) in enumerate(zip(code.splitlines(), expected.splitlines())):
                if a != b:
                    print(f"  !! {page.name} {name} {i+1}行目がちがう")
                    print(f"     HTML: {a!r}")
                    print(f"     src : {b!r}")
                    break

print(f"照合したコードブロック: {checked}個")
print("不一致:", ng or "なし")

# ついでに、HTML から取り出したコードがそのまま動くかを確かめる
print()
print("HTMLから取り出したコードをそのまま実行して確認")
import tempfile, os
tmp = tempfile.mkdtemp()
fail = []
for src in sorted((HERE / "src").glob("*.py")):
    r = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        fail.append((src.name, r.stderr.strip().splitlines()[-1]))
print("実行失敗:", fail or "なし")
