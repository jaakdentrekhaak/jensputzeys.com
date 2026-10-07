# jensputzeys.com

Static site for GitHub Pages (custom domain via `CNAME`). Vanilla HTML/CSS/JS, no build step to host.

## Structure

- `index.html` - home page: just a small centred `jensputzeys.com` on the palette background. No links.
- `asoiaf/index.html` - small index of the A Song of Ice and Fire books; only A Game of Thrones is linked, the rest are "coming soon". No link to the home page.
- `asoiaf/agot/index.html` - spoiler-safe reading companion for A Game of Thrones; standalone, no link back to the home page. Last chapter is stored in `localStorage` under `asoiaf:agot:chapter` (namespace new books as `asoiaf:<slug>:chapter`).
- `asoiaf/agot/chapters/NN.html` - one pre-rendered fragment per chapter (00 = Prologue, 01-72), fetched on demand at `/asoiaf/agot/chapters/NN.html`. Each contains only that chapter's overview, so later chapters never load. `labels.json` holds only the picker labels.
- `got/index.html` - redirect (meta refresh + JS) from the old `/got/` URL to `/asoiaf/agot/`.
- `tools/build_book.py` - generates a book's fragments from markdown overviews.
- `tools/check_contrast.py` - WCAG 2.2 contrast check of the palette in `assets.css`.
- `assets.css` - shared design tokens and base styles. `404.html`, `CNAME`, `.nojekyll`.

## Regenerate chapters

    python3 tools/build_book.py [OVERVIEWS_DIR [BOOK_DIR]]

Defaults to the AGOT case: `../got-overview/overviews` (must contain `00.md` ... `72.md`) and `asoiaf/agot`. Only overview files are read; no raw book text is used or published.

## Palette "Ink & Ember"

Defined as CSS custom properties in `assets.css`, used by every page; light by default, dark via `prefers-color-scheme`. Check with `python3 tools/check_contrast.py` (exit code non-zero on failure). Targets: WCAG 2.2 AA, 4.5:1 text, 3:1 UI/focus.

| Token | Light | Dark |
|---|---|---|
| `--bg` | #f5efe4 (warm parchment) | #1e1a2e (deep ink-aubergine) |
| `--surface` | #fffcf5 | #2a2540 |
| `--text` | #251f33 | #eee9f6 |
| `--muted` | #5b5469 | #b9b2cc |
| `--accent` | #8c3a12 | #f2b985 |
| `--border` (decorative) | #d9cfbd | #443d62 |
| `--border-strong` (controls) | #847a6b | #8a82a8 |
| `--highlight` (new entries) | #fbebb0 | #3c3217 |
| `--highlight-edge` | #8a6200 | #d9aa3a |
| `--focus` | #3a3fc8 | #9fc0ff |
| `--chevron` | #251f33 | #eee9f6 |

Contrast results (all pass):

```
== light ==
ok   13.88:1 (min 4.5) text #251f33 on bg #f5efe4 - body text on page
ok   15.50:1 (min 4.5) text #251f33 on surface #fffcf5 - text on cards/controls
ok    6.29:1 (min 4.5) muted #5b5469 on bg #f5efe4 - muted text on page
ok    7.03:1 (min 4.5) muted #5b5469 on surface #fffcf5 - muted text on surface
ok    6.72:1 (min 4.5) accent #8c3a12 on bg #f5efe4 - links on page
ok    7.51:1 (min 4.5) accent #8c3a12 on surface #fffcf5 - links on surface
ok   13.32:1 (min 4.5) text #251f33 on highlight #fbebb0 - text on new-entry highlight
ok    6.45:1 (min 4.5) accent #8c3a12 on highlight #fbebb0 - links on highlight
ok    5.35:1 (min 3.0) highlight-edge #8a6200 on surface #fffcf5 - highlight edge (UI)
ok    3.69:1 (min 3.0) border-strong #847a6b on bg #f5efe4 - control border on page (UI)
ok    4.12:1 (min 3.0) border-strong #847a6b on surface #fffcf5 - control border on surface (UI)
ok    6.73:1 (min 3.0) focus #3a3fc8 on bg #f5efe4 - focus ring on page (UI)
ok    7.52:1 (min 3.0) focus #3a3fc8 on surface #fffcf5 - focus ring on surface (UI)
ok    6.46:1 (min 3.0) focus #3a3fc8 on highlight #fbebb0 - focus ring on highlight (UI)
ok   15.50:1 (min 3.0) chevron #251f33 on surface #fffcf5 - select chevron (UI)
== dark ==
ok   14.18:1 (min 4.5) text #eee9f6 on bg #1e1a2e - body text on page
ok   12.26:1 (min 4.5) text #eee9f6 on surface #2a2540 - text on cards/controls
ok    8.29:1 (min 4.5) muted #b9b2cc on bg #1e1a2e - muted text on page
ok    7.17:1 (min 4.5) muted #b9b2cc on surface #2a2540 - muted text on surface
ok    9.70:1 (min 4.5) accent #f2b985 on bg #1e1a2e - links on page
ok    8.39:1 (min 4.5) accent #f2b985 on surface #2a2540 - links on surface
ok   10.61:1 (min 4.5) text #eee9f6 on highlight #3c3217 - text on new-entry highlight
ok    7.26:1 (min 4.5) accent #f2b985 on highlight #3c3217 - links on highlight
ok    6.79:1 (min 3.0) highlight-edge #d9aa3a on surface #2a2540 - highlight edge (UI)
ok    4.70:1 (min 3.0) border-strong #8a82a8 on bg #1e1a2e - control border on page (UI)
ok    4.06:1 (min 3.0) border-strong #8a82a8 on surface #2a2540 - control border on surface (UI)
ok    9.22:1 (min 3.0) focus #9fc0ff on bg #1e1a2e - focus ring on page (UI)
ok    7.97:1 (min 3.0) focus #9fc0ff on surface #2a2540 - focus ring on surface (UI)
ok    6.90:1 (min 3.0) focus #9fc0ff on highlight #3c3217 - focus ring on highlight (UI)
ok   12.26:1 (min 3.0) chevron #eee9f6 on surface #2a2540 - select chevron (UI)
```

Also: visible `:focus-visible` outline, `color-scheme` property/meta, and `prefers-reduced-motion` disables animation/transitions. The select chevron is an inline SVG data URI (colour duplicated per theme in the page, matching `--chevron`).

## Local preview

    python3 -m http.server 8000

Then open http://localhost:8000/ (the chapter picker needs HTTP; `fetch` does not work from `file://`).

Unofficial fan reading aid; content is AI-generated and may contain mistakes.
