#!/usr/bin/env python3
"""Python のソースを、授業ページの <pre> と同じ配色の HTML に変換する。

使い方:
    python3 pyhl.py AL2-01-ex1.py            # 変換結果を標準出力へ
    python3 pyhl.py AL2-01-ex1.py --label "Python ── AL2-01-ex1.py"

配色クラス: kw=予約語 / fn=関数名 / str=文字列 / cmt=コメント / num=数値
"""
import html as H
import re
import sys

KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
}
BUILTINS = {
    "abs", "all", "any", "bool", "dict", "enumerate", "float", "format", "input",
    "int", "len", "list", "map", "max", "min", "open", "print", "range", "repr",
    "reversed", "round", "set", "sorted", "str", "sum", "tuple", "type", "zip",
}

TOKEN = re.compile(r"""
    (?P<comment>\#[^\n]*)
  | (?P<string>(?:[fFrRbB]{0,2})(?:'''.*?'''|\"\"\".*?\"\"\"|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"))
  | (?P<number>\b\d+(?:\.\d+)?\b)
  | (?P<name>[A-Za-z_][A-Za-z_0-9]*)
""", re.X | re.S)


def highlight(code):
    out = []
    pos = 0
    for m in TOKEN.finditer(code):
        out.append(H.escape(code[pos:m.start()]))
        pos = m.end()
        text = H.escape(m.group(0))
        if m.lastgroup == "comment":
            out.append(f'<span class="cmt">{text}</span>')
        elif m.lastgroup == "string":
            out.append(f'<span class="str">{text}</span>')
        elif m.lastgroup == "number":
            out.append(f'<span class="num">{text}</span>')
        else:
            word = m.group(0)
            after = code[m.end():m.end() + 1]
            before = code[max(0, m.start() - 4):m.start()]
            if word in KEYWORDS:
                out.append(f'<span class="kw">{text}</span>')
            elif word in BUILTINS and after == "(":
                out.append(f'<span class="fn">{text}</span>')
            elif before.endswith("def ") or (after == "(" and not before.endswith(".")):
                out.append(f'<span class="fn">{text}</span>')
            else:
                out.append(text)
    out.append(H.escape(code[pos:]))
    return "".join(out)


if __name__ == "__main__":
    path = sys.argv[1]
    label = None
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]
    else:
        label = "Python ── " + path.split("/")[-1]
    src = open(path, encoding="utf-8").read().rstrip("\n")
    print(f'<pre><span class="code-label">{H.escape(label)}</span>')
    print(highlight(src) + "</pre>")
