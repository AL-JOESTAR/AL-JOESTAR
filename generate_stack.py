#!/usr/bin/env python3
"""Generate stack.svg (dark/light, desktop/phone) for the profile README.

Edit STACK below, then run:  python tools/generate_stack.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

TITLE = "STACK"
SUBTITLE = "tools I use to build things."

# Edit this: category -> list of technologies
STACK = {
    "LANG":     ["Python", "TypeScript", "Go", "SQL"],
    "FRONTEND": ["React", "Next.js", "Tailwind"],
    "BACKEND":  ["Node.js", "FastAPI", "Laravel"],
    "DATA":     ["PostgreSQL", "Redis", "MongoDB"],
    "DEVOPS":   ["Docker", "GitHub Actions", "Linux", "AWS"],
}

THEMES = {
    "dark":  dict(bg="#0d1117", border="#30363d", title="#39d353", text="#e6edf3",
                  muted="#8b949e", chip="#161b22", chip_border="#39d353", label="#58a6ff"),
    "light": dict(bg="#ffffff", border="#d0d7de", title="#1a7f37", text="#1f2328",
                  muted="#656d76", chip="#f6f8fa", chip_border="#1a7f37", label="#0969da"),
}

FONT = "'Courier New', Courier, monospace"
CHAR_W = 0.6  # monospace width ratio


def build(width, theme, compact):
    t = THEMES[theme]
    fs = 13 if compact else 15
    pad = 20 if compact else 28
    label_w = 0 if compact else 110          # phone: label sits above chips
    chip_h = fs + 14
    gap = 8
    row_gap = 18

    out = []
    y = pad + 30
    out.append(f'<text x="{pad}" y="{pad + 14}" font-family="{FONT}" font-size="{fs + 9}" '
               f'font-weight="bold" fill="{t["title"]}">&gt; {escape(TITLE)}</text>')
    out.append(f'<text x="{pad}" y="{pad + 36}" font-family="{FONT}" font-size="{fs - 1}" '
               f'fill="{t["muted"]}">{escape(SUBTITLE)}</text>')
    y = pad + 62

    for cat, items in STACK.items():
        x0 = pad + label_w
        if compact:
            out.append(f'<text x="{pad}" y="{y + 4}" font-family="{FONT}" font-size="{fs - 1}" '
                       f'font-weight="bold" fill="{t["label"]}">[{escape(cat)}]</text>')
            y += 12
        else:
            out.append(f'<text x="{pad}" y="{y + chip_h / 2 + fs * 0.35}" font-family="{FONT}" '
                       f'font-size="{fs}" font-weight="bold" fill="{t["label"]}">[{escape(cat)}]</text>')
        x = x0
        for name in items:
            w = int(len(name) * fs * CHAR_W + 22)
            if x + w > width - pad:      # wrap
                x = x0
                y += chip_h + gap
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{chip_h}" rx="4" '
                       f'fill="{t["chip"]}" stroke="{t["chip_border"]}" stroke-width="1.5"/>')
            out.append(f'<text x="{x + w / 2}" y="{y + chip_h / 2 + fs * 0.35}" text-anchor="middle" '
                       f'font-family="{FONT}" font-size="{fs}" fill="{t["text"]}">{escape(name)}</text>')
            x += w + gap
        y += chip_h + row_gap

    height = y + pad - row_gap + 6
    # blinking cursor
    out.append(f'<rect x="{pad}" y="{height - pad - 4}" width="{fs * 0.6}" height="{fs}" fill="{t["title"]}">'
               f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
    height += 18

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="Stack: '
           f'{escape(", ".join(i for v in STACK.values() for i in v))}">'
           f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" '
           f'fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="2"/>'
           + "".join(out) + '</svg>')
    return svg


def main():
    root = Path(__file__).resolve().parent.parent / "assets"
    (root / "phone").mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        suffix = "" if theme == "dark" else "-light"
        (root / f"stack{suffix}.svg").write_text(build(800, theme, False), encoding="utf-8")
        (root / "phone" / f"stack{suffix}.svg").write_text(build(380, theme, True), encoding="utf-8")
    print("Generated:", *sorted(p.relative_to(root.parent) for p in root.rglob("stack*.svg")), sep="\n  ")


if __name__ == "__main__":
    main()
