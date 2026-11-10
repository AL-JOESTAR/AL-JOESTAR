#!/usr/bin/env python3
"""Generate every SVG asset + README.md for the profile.

1. Edit the CONFIG section below.
2. Run:  python tools/generate.py
"""
import random
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape as esc

# =====================================================================
# CONFIG  (edit this)
# =====================================================================
NAME = "John Doe"
ROLE = "Builds things at Acme."            # shown under the name, in big letters
SUBTITLE = "After hours, I build tiny, delightful toys for the web."
USERNAME = "johndoe"                         # GitHub username
HOME_URL = "https://github.com/johndoe"

# --- contribution graph panel (placeholder; see README note about snake) ---
GRAPH_CONTRIBUTIONS = "1,234 CONTRIBUTIONS"
GRAPH_BEST_DAY = "BEST DAY 42"
GRAPH_CAPTION = "↑ my real contribution graph, redrawn every day as a game of snake"

# --- stack panel ---
STACK_TITLE = "STACK"
STACK_CAPTION = "TOOLS I BUILD WITH"
STACK = {
    "LANG":     ["Python", "TypeScript", "Go", "SQL"],
    "FRONTEND": ["React", "Next.js", "Tailwind"],
    "BACKEND":  ["Node.js", "FastAPI", "Laravel"],
    "DATA":     ["PostgreSQL", "Redis", "MongoDB"],
    "DEVOPS":   ["Docker", "GitHub Actions", "Linux", "AWS"],
}

# --- project cartridges (exactly 3) ---
PROJECTS = [
    dict(title="Project One",   desc="A short description of your first project goes here.",  url="https://github.com/johndoe/project-one"),
    dict(title="Project Two",   desc="A short description of your second project goes here.", url="https://github.com/johndoe/project-two"),
    dict(title="Project Three", desc="A short description of your third project goes here.",  url="https://github.com/johndoe/project-three"),
]

# --- credits panel ---
CREDITS_TEXT = "Made with love, coffee and too many side projects. Free to use, fork and remix."
CREDITS_URL = "https://github.com/johndoe"
CREDITS_CTA = "INSERT COIN TO CONTINUE"

# =====================================================================
# THEMES
# =====================================================================
THEMES = {
    "dark": dict(
        bg="#1b1030", panel="#05060a", panel2="#120d22", border="#3a2a5e",
        title="#ffd479", shadow="#e0457b", accent="#7ee8d0", text="#efe8ff",
        muted="#9a8fb5", ink="#1b1030", outline="#05060a",
        cats=["#7ee8d0", "#f7a8c8", "#ffd479", "#8ab4ff", "#c3a6ff"],
        grid=["#16171c", "#0e4429", "#006d32", "#26a641", "#39d353"],
        snake="#f7a8c8", head="#ffd479"),
    "light": dict(
        bg="#fff8ec", panel="#ffffff", panel2="#f6efff", border="#cdbdf0",
        title="#d9480f", shadow="#ffc2da", accent="#0b8a74", text="#2a1f3d",
        muted="#6e6585", ink="#fff8ec", outline="#2a1f3d",
        cats=["#0b8a74", "#d6336c", "#d9480f", "#1c64d9", "#7048e8"],
        grid=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
        snake="#d6336c", head="#d9480f"),
}

FONT = "'Courier New', Courier, monospace"


# =====================================================================
# HELPERS
# =====================================================================
def attr(s):
    return esc(s, {'"': "&quot;"})


def svg(w, h, body, label, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{attr(label)}">{bgrect}{body}</svg>')


def text(x, y, s, size, fill, anchor="start", weight="bold", ls=0, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size:.1f}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}" {extra}>{esc(s)}</text>')


def fit(n_chars, avail, base, ratio=0.66):
    return min(base, avail / (max(n_chars, 1) * ratio))


# =====================================================================
# ASSETS
# =====================================================================
def header(t, phone):
    w, h = (400, 130) if phone else (768, 200)
    pad = 14 if phone else 28
    lines = [NAME.upper(), ROLE.upper()]
    fs = fit(max(map(len, lines)), w - 2 * pad, 30 if phone else 52)
    y1 = pad + fs
    y2 = y1 + fs * 1.2
    sub_fs = fit(len(SUBTITLE), w - 2 * pad, 14 if phone else 20, 0.6)
    ys = y2 + (26 if phone else 38)
    body = ""
    for line, y in zip(lines, (y1, y2)):
        body += text(pad + 3, y + 3, line, fs, t["shadow"], ls=1)
        body += text(pad, y, line, fs, t["title"], ls=1)
    body += text(pad, ys, SUBTITLE, sub_fs, t["text"], weight="normal")
    return svg(w, h, body, f"{NAME}. {ROLE} {SUBTITLE}", t["bg"])


EGG = [
    "....KKKKKK....",
    "..KKPPPPPPKK..",
    ".KPPWWPPPPPPK.",
    ".KPWPPPPPPPPK.",
    "KPPPPLLLLPPPPK",
    "KPPPLLLLLLPPPK",
    "KPPPLLDDLLPPPK",
    "KPPPLLDDLLPPPK",
    "KPPPLLLLLLPPPK",
    "KPPPPLLLLPPPPK",
    "KPPPPPPPPPPPPK",
    "KPPPYPPPPYPPPK",
    "KPPPYPPPPYPPPK",
    ".KPPPPPPPPPPK.",
    "..KKPPPPPPKK..",
    "....KKKKKK....",
]


def egg(t, phone):
    w, h = (100, 130) if phone else (192, 200)
    s = 7 if phone else 10
    pal = {"K": t["outline"], "P": "#f7a8c8", "W": "#ffffff",
           "L": "#dcd6ff", "D": "#2a1f55", "Y": "#ffd479"}
    ox = (w - 14 * s) / 2
    oy = (h - 16 * s) / 2 + 4
    rects = ""
    for r, row in enumerate(EGG):
        for c, ch in enumerate(row):
            if ch != ".":
                rects += (f'<rect x="{ox + c * s:.1f}" y="{oy + r * s:.1f}" width="{s}" '
                          f'height="{s}" fill="{pal[ch]}" shape-rendering="crispEdges"/>')
    body = ('<g><animateTransform attributeName="transform" type="translate" '
            'values="0 0;0 -5;0 0" dur="1.2s" repeatCount="indefinite"/>' + rects + '</g>')
    return svg(w, h, body, "A tiny egg wiggles in the corner.", t["bg"])


def graph(t, phone):
    w = 400 if phone else 800
    cols = 26 if phone else 53
    pad = 14 if phone else 20
    inner = 14 if phone else 24
    step = (w - 2 * pad - 2 * inner) / cols
    size = step * 0.78
    top = pad
    fs = 10 if phone else 12
    grid_y = top + (36 if phone else 48)
    panel_h = (grid_y - top) + 7 * step + inner - 4
    cap_fs = 10 if phone else 13
    cap_y = top + panel_h + (18 if phone else 24)
    h = int(cap_y + 12)

    body = (f'<rect x="{pad}" y="{top}" width="{w - 2 * pad}" height="{panel_h:.1f}" rx="10" '
            f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="2"/>')
    ty = top + (23 if phone else 31)
    body += text(pad + inner, ty, f"P1 · {USERNAME.upper()}", fs, t["accent"], ls=1)
    if phone:
        body += text(w - pad - inner, ty, GRAPH_CONTRIBUTIONS, fs, t["accent"], "end", ls=1)
    else:
        body += text(w / 2, ty, GRAPH_CONTRIBUTIONS, fs, t["accent"], "middle", ls=1)
        body += text(w - pad - inner, ty, GRAPH_BEST_DAY, fs, t["accent"], "end", ls=1)

    rng = random.Random(7)
    snake_col = cols - 4
    for c in range(cols):
        for r in range(7):
            if c == snake_col and r < 6:
                color = t["head"] if r == 0 else t["snake"]
            else:
                lvl = rng.choice([1, 2, 3, 4]) if rng.random() < 0.3 else 0
                color = t["grid"][lvl]
            x = pad + inner + c * step
            y = grid_y + r * step
            body += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" '
                     f'rx="{size * 0.2:.1f}" fill="{color}"/>')
    cap_size = fit(len(GRAPH_CAPTION), w - 2 * pad - 8, cap_fs, 0.68)
    body += text(pad + 4, cap_y, GRAPH_CAPTION, cap_size, t["muted"], weight="normal")
    return svg(w, h, body, "A snake eats my GitHub contribution graph.", t["bg"])


def stack(t, phone):
    w = 400 if phone else 800
    pad = 14 if phone else 20
    ip = 16 if phone else 24
    fs = 12 if phone else 15
    chip_h = fs + 12
    gap = 8
    label_w = 0 if phone else 112
    head_fs = 14 if phone else 17

    hy = pad + head_fs
    sx, sy, sr = pad + 2 + head_fs * 0.5, hy - head_fs * 0.35, head_fs * 0.5
    pts = " ".join(f"{sx + sr * (1 if k % 2 == 0 else 0.42) * __import__('math').sin(k * 0.6283):.1f},"
                   f"{sy - sr * (1 if k % 2 == 0 else 0.42) * __import__('math').cos(k * 0.6283):.1f}"
                   for k in range(10))
    head = f'<polygon points="{pts}" fill="{t["title"]}"/>'
    head += text(pad + 2 + head_fs * 1.4, hy, STACK_TITLE, head_fs, t["title"], ls=3)
    cap_fs = fit(len(STACK_CAPTION), w * 0.45, 10 if phone else 12, 0.7)
    head += text(w - pad - 2, hy, STACK_CAPTION, cap_fs, t["muted"], "end", ls=1)

    top = hy + 14
    y = top + ip
    x0 = pad + ip + label_w
    limit = w - pad - ip
    content = ""
    for i, (cat, items) in enumerate(STACK.items()):
        col = t["cats"][i % len(t["cats"])]
        if phone:
            content += text(pad + ip, y + fs * 0.8, f"[{cat}]", fs - 1, col, ls=1)
            y += fs + 8
        else:
            content += text(pad + ip, y + chip_h / 2 + fs * 0.35, f"[{cat}]", fs, col, ls=1)
        x = x0
        for name in items:
            cw = len(name) * fs * 0.6 + 22
            if x + cw > limit:
                x = x0
                y += chip_h + gap
            content += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{chip_h}" rx="4" '
                        f'fill="{t["panel2"]}" stroke="{col}" stroke-width="1.5"/>')
            content += text(x + cw / 2, y + chip_h / 2 + fs * 0.35, name, fs, t["text"],
                            "middle", weight="normal")
            x += cw + gap
        y += chip_h + 14
    bottom = y - 14 + ip
    panel = (f'<rect x="{pad}" y="{top}" width="{w - 2 * pad}" height="{bottom - top:.1f}" rx="10" '
             f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="2"/>')
    h = int(bottom + pad)
    flat = ", ".join(i for v in STACK.values() for i in v)
    return svg(w, h, head + panel + content, f"{STACK_TITLE}: {flat}", t["bg"])


def cart(t, i, phone):
    w, h = 256, 300
    col = t["cats"][i % len(t["cats"])]
    p = PROJECTS[i]
    body = (f'<rect x="6" y="6" width="244" height="288" rx="16" fill="{t["panel"]}" '
            f'stroke="{col}" stroke-width="3"/>')
    for gy in (16, 24):
        body += f'<rect x="88" y="{gy}" width="80" height="4" rx="2" fill="{t["border"]}"/>'
    body += (f'<rect x="22" y="40" width="212" height="170" rx="8" fill="{t["panel2"]}" '
             f'stroke="{t["border"]}" stroke-width="2"/>')
    body += text(34, 62, f"PLAYER {i + 1}", 11, col, ls=2)
    y = 98
    for line in textwrap.wrap(p["title"].upper(), 13)[:2]:
        body += text(34, y, line, 22, t["title"])
        y += 28
    y += -4
    for line in textwrap.wrap(p["desc"], 28)[:(205 - int(y)) // 17]:
        body += text(34, y, line, 12, t["muted"], weight="normal")
        y += 17
    body += f'<rect x="38" y="226" width="180" height="40" rx="8" fill="{col}"/>'
    body += text(128, 252, "PRESS START", 16, t["ink"], "middle", ls=1)
    for k in range(8):
        body += f'<rect x="{40 + k * 22}" y="278" width="10" height="8" fill="{t["border"]}"/>'
    return svg(w, h, body, f"{p['title']}: {p['desc']}", t["bg"])


def credits(t, phone):
    w = 400 if phone else 800
    pad = 14 if phone else 20
    fs = 12 if phone else 14
    lines = textwrap.wrap(CREDITS_TEXT, int((w - 2 * pad - 40) / (fs * 0.6)))
    top = pad
    y = top + 30
    body = text(pad + 20, y, "CREDITS", fs, t["accent"], ls=3)
    y += 26
    for line in lines:
        body += text(pad + 20, y, line, fs, t["text"], weight="normal")
        y += fs * 1.6
    y += fs * 0.8
    body += (f'<text x="{pad + 20}" y="{y:.1f}" font-family="{FONT}" font-size="{fs}" '
             f'font-weight="bold" fill="{t["title"]}" letter-spacing="2">{esc(CREDITS_CTA)}'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="1.4s" '
             f'repeatCount="indefinite"/></text>')
    panel_h = y + 18 - top
    panel = (f'<rect x="{pad}" y="{top}" width="{w - 2 * pad}" height="{panel_h:.1f}" rx="10" '
             f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="2" stroke-dasharray="6 6"/>')
    h = int(top + panel_h + pad)
    return svg(w, h, panel + body, f"Credits: {CREDITS_TEXT} {CREDITS_CTA}.", t["bg"])


# =====================================================================
# README
# =====================================================================
def pic(name, width, alt, href):
    a = attr(alt)
    return (f'<a href="{href}"><picture>'
            f'<source media="(max-width: 600px) and (prefers-color-scheme:light)" srcset="assets/phone/{name}-light.svg">'
            f'<source media="(max-width: 600px)" srcset="assets/phone/{name}.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">'
            f'<img src="assets/{name}.svg" width="{width}" align="top" alt="{a}">'
            f'</picture></a>')


def readme():
    flat = ", ".join(i for v in STACK.values() for i in v)
    out = ['<div align="center">']
    out.append(pic("header", "76.8%", f"{NAME}. {ROLE} {SUBTITLE}", HOME_URL)
               + pic("egg", "19.2%", "A tiny egg wiggles in the corner.", HOME_URL) + "<br>")
    out.append(pic("graph", "96%", "A snake eats my GitHub contribution graph.", HOME_URL) + "<br>")
    out.append(pic("stack", "96%", f"{STACK_TITLE}: {flat}.", HOME_URL) + "<br>")
    carts = "".join(pic(f"cart-{i + 1}", "32%", f"{p['title']}: {p['desc']}", p["url"])
                    for i, p in enumerate(PROJECTS))
    out.append(carts + "<br>")
    out.append(pic("credits", "96%", f"Credits: {CREDITS_TEXT}", CREDITS_URL))
    out.append("</div>")
    return "\n".join(out) + "\n"


# =====================================================================
# MAIN
# =====================================================================
def main():
    root = Path(__file__).resolve().parent.parent
    for theme, suf in (("dark", ""), ("light", "-light")):
        t = THEMES[theme]
        for phone in (False, True):
            d = root / "assets" / ("phone" if phone else "")
            d.mkdir(parents=True, exist_ok=True)
            files = {"header": header(t, phone), "egg": egg(t, phone),
                     "graph": graph(t, phone), "stack": stack(t, phone),
                     "credits": credits(t, phone)}
            for i in range(len(PROJECTS)):
                files[f"cart-{i + 1}"] = cart(t, i, phone)
            for name, content in files.items():
                (d / f"{name}{suf}.svg").write_text(content, encoding="utf-8")
    (root / "README.md").write_text(readme(), encoding="utf-8")
    print("Done: README.md + assets/ (desktop, phone, dark, light)")


if __name__ == "__main__":
    main()
