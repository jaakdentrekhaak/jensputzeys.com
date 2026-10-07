#!/usr/bin/env python3
"""Build per-chapter HTML fragments from the markdown overviews.

Usage: python3 tools/build_book.py [OVERVIEWS_DIR [BOOK_DIR]]
Defaults (AGOT): OVERVIEWS_DIR=../got-overview/overviews (relative to the site root),
BOOK_DIR=asoiaf/agot (relative to the site root; e.g. asoiaf/acok for another book).
Each BOOK_DIR/chapters/NN.html is derived solely from overviews/NN.md.
Also writes BOOK_DIR/chapters/labels.json (picker labels only, no content).
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "got-overview" / "overviews"
book = sys.argv[2] if len(sys.argv) > 2 else "asoiaf/agot"
out = ROOT / book / "chapters"
out.mkdir(parents=True, exist_ok=True)


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)\*(?![\w*])", r"<em>\1</em>", t)
    t = t.replace("\U0001F195", '<span class="new-badge" title="New this chapter">\U0001F195<span class="sr-only"> new this chapter</span></span>')
    return t


def li(text):
    head = text.split(" – ", 1)[0]
    cls = ' class="is-new"' if "\U0001F195" in text else ""
    return f"<li{cls}>{inline(text)}</li>"


def render(md):
    lines = md.splitlines()
    parts, state = [], {"details": False, "ul": False, "section": None}

    def close_ul():
        if state["ul"]:
            parts.append("</ul>")
            state["ul"] = False

    def close_details():
        close_ul()
        if state["details"]:
            parts.append("</details>")
            state["details"] = False

    def close_section():
        close_details()
        if state["section"]:
            parts.append("</section>")
            state["section"] = None

    para = []
    def flush_para():
        if para:
            parts.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    for ln in lines:
        s = ln.rstrip()
        if s.startswith("# "):
            parts.append(f'<h2 class="ch-title" tabindex="-1">{inline(s[2:])}</h2>')
        elif s.startswith("> "):
            parts.append(f'<p class="summary">{inline(s[2:])}</p>')
        elif s.startswith("## "):
            flush_para(); close_section()
            name = s[3:].strip()
            state["section"] = name.lower()
            parts.append(f'<section class="group-section" data-section="{state["section"]}"><h3>{inline(name)}</h3>')
            if name.lower() == "places":
                parts.append("<details open><summary>Places</summary>")
                state["details"] = True
        elif s.startswith("### "):
            flush_para(); close_details()
            parts.append(f"<details open><summary>{inline(s[4:])}</summary>")
            state["details"] = True
        elif s.startswith("- "):
            flush_para()
            if not state["ul"]:
                parts.append("<ul>")
                state["ul"] = True
            parts.append(li(s[2:]))
        elif s.strip():
            close_ul()
            para.append(s.strip())
        else:
            flush_para()
    flush_para(); close_section()
    return "\n".join(parts) + "\n"


labels = {}
files = sorted(src.glob("[0-9][0-9].md"))
if not files:
    sys.exit(f"No overviews found in {src}")
for f in files:
    n = f.stem
    md = f.read_text(encoding="utf-8")
    (out / f"{n}.html").write_text(render(md), encoding="utf-8")
    title = md.splitlines()[0].lstrip("# ").strip()
    labels[int(n)] = "Prologue" if int(n) == 0 else title
(out / "labels.json").write_text(json.dumps([labels[k] for k in sorted(labels)], ensure_ascii=False, indent=0), encoding="utf-8")
print(f"Wrote {len(files)} fragments to {out}")
