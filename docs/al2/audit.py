"""例題コードの検査:
  1. 実行してエラーが出ないか
  2. ソースと出力が Windows の cp932 で扱えるか（文字化け・例外の危険）
  3. 危ない文字（波ダッシュ U+301C など）が混ざっていないか
"""
import pathlib
import subprocess
import sys
import unicodedata

SRC = pathlib.Path(__file__).resolve().parent / "src"

# 注: 波ダッシュ U+301C は cp932 でも shift_jis でも扱える（安全）。
#     逆に全角チルダ U+FF5E は shift_jis で encode できないので使わない。
DANGER_NAMES = {
    "～": "全角チルダ U+FF5E（shift_jis で encode できない。波ダッシュ U+301C にする）",
    "−": "マイナス記号 U+2212（cp932 不可。半角 - にする）",
    " ": "ノーブレークスペース U+00A0",
    "‐": "ハイフン U+2010",
    "―": "水平バー U+2015（環境で幅が変わる）",
}


def bad_chars(text, label):
    """cp932 で表せない文字を集める"""
    out = {}
    for ch in set(text):
        if ch in "\n\r\t":
            continue
        try:
            ch.encode("cp932")
        except UnicodeEncodeError:
            out.setdefault(ch, 0)
            out[ch] += text.count(ch)
    return out


problems = []
print(f"{'ファイル':<20} {'実行':<6} {'出力行':<7} {'cp932(ソース)':<14} {'cp932(出力)':<14} 危険文字")
print("-" * 92)
for path in sorted(SRC.glob("*.py")):
    source = path.read_text(encoding="utf-8")
    result = subprocess.run([sys.executable, str(path)], capture_output=True,
                            text=True, timeout=600)
    ok = "OK" if result.returncode == 0 else "NG"
    out = result.stdout

    src_bad = bad_chars(source, "source")
    out_bad = bad_chars(out, "stdout")
    danger = {ch: DANGER_NAMES[ch] for ch in DANGER_NAMES if ch in source}

    print(f"{path.name:<20} {ok:<6} {len(out.splitlines()):<7} "
          f"{('OK' if not src_bad else 'NG ' + ''.join(src_bad)):<14} "
          f"{('OK' if not out_bad else 'NG ' + ''.join(out_bad)):<14} "
          f"{''.join(danger) if danger else '-'}")

    if result.returncode != 0:
        problems.append((path.name, "実行失敗", result.stderr.strip().splitlines()[-1:]))
    if src_bad or out_bad:
        detail = {}
        for ch in list(src_bad) + list(out_bad):
            detail[ch] = f"U+{ord(ch):04X} {unicodedata.name(ch, '?')}"
        problems.append((path.name, "cp932で表せない文字", detail))
    if danger:
        problems.append((path.name, "危険な文字", danger))

print()
if problems:
    print("=== 見つかった問題 ===")
    for name, kind, detail in problems:
        print(f"  {name}: {kind}")
        print(f"      {detail}")
else:
    print("問題なし")
