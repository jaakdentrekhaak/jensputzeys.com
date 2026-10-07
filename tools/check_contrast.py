#!/usr/bin/env python3
"""WCAG 2.2 contrast check for the palette defined in assets.css.

Parses the :root token blocks (light = default, dark = prefers-color-scheme block)
and checks every text/background and UI pair. Exits non-zero on any failure.
Usage: python3 tools/check_contrast.py
"""
import re, sys
from pathlib import Path

css = (Path(__file__).resolve().parent.parent / "assets.css").read_text()
light_blk = re.search(r"/\*light\*/\s*:root\{([^}]*)\}", css).group(1)
dark_blk = re.search(r"/\*dark\*/\s*:root[^{]*\{([^}]*)\}", css).group(1)
tok = lambda blk: dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", blk))
light = tok(light_blk)
dark = {**light, **tok(dark_blk)}


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (foreground, background, minimum ratio, description)
PAIRS = [
    ("text", "bg", 4.5, "body text on page"),
    ("text", "surface", 4.5, "text on cards/controls"),
    ("muted", "bg", 4.5, "muted text on page"),
    ("muted", "surface", 4.5, "muted text on surface"),
    ("accent", "bg", 4.5, "links on page"),
    ("accent", "surface", 4.5, "links on surface"),
    ("text", "highlight", 4.5, "text on new-entry highlight"),
    ("accent", "highlight", 4.5, "links on highlight"),
    ("highlight-edge", "surface", 3.0, "highlight edge (UI)"),
    ("border-strong", "bg", 3.0, "control border on page (UI)"),
    ("border-strong", "surface", 3.0, "control border on surface (UI)"),
    ("focus", "bg", 3.0, "focus ring on page (UI)"),
    ("focus", "surface", 3.0, "focus ring on surface (UI)"),
    ("focus", "highlight", 3.0, "focus ring on highlight (UI)"),
    ("chevron", "surface", 3.0, "select chevron (UI)"),
]
fail = 0
for name, t in (("light", light), ("dark", dark)):
    print(f"== {name} ==")
    for fg, bg, mn, d in PAIRS:
        r = ratio(t[fg], t[bg])
        ok = r >= mn
        fail += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {r:5.2f}:1 (min {mn}) {fg} {t[fg]} on {bg} {t[bg]} - {d}")
sys.exit(1 if fail else 0)
