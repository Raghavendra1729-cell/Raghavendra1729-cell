#!/usr/bin/env python3
"""
Generate a beautiful coding profiles and connect terminal SVG card (profiles-card.svg).
Titled: raghav@github: ~$ ./show_profiles.sh
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "profiles-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 860, 150
PAD = 25
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
SECTION = "#58a6ff"
GREEN = "#3fb950"
GOLD = "#f2cc60"
ACCENT = "#22d3ee"

COL1_X = PAD + 10
COL2_X = PAD + 420

def rise(inner, delay_idx):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.2 + delay_idx * 0.05
    return (f'<g opacity="0" transform="translate(0,4)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.3s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#pbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">raghav@github: ~$ ./show_profiles.sh</text>')

# Column 1: Coding Profiles
y = TITLEBAR_H + 28
col1_title = f'<text x="{COL1_X}" y="{y:.1f}" fill="{SECTION}" font-size="12" font-weight="700">— CODING PROFILES —</text>'
col1_title += f'<line x1="{COL1_X}" y1="{y+4:.1f}" x2="{COL1_X+360}" y2="{y+4:.1f}" stroke="{FRAME}" stroke-opacity="0.5"/>'
parts.append(rise(col1_title, 0))

profiles = [
    ("LeetCode", "Raghavendra-1729-cell", "1750 Max", GOLD),
    ("Codeforces", "Raghavendra1729-cell", "1210 Max", ACCENT),
    ("CodeChef", "raghav1729420", "1680 Max", GREEN)
]

py = y + 24
for idx, (platform, handle, rating, rcolor) in enumerate(profiles):
    inner = (f'<text x="{COL1_X}" y="{py:.1f}" fill="{INK}" font-size="11.5">'
             f'{platform}: <tspan fill="{MUTED}">{handle}</tspan> '
             f'(<tspan fill="{rcolor}" font-weight="700">{rating}</tspan>)</text>')
    parts.append(rise(inner, idx + 1))
    py += 18

# Column 2: Resume & Connect
col2_title = f'<text x="{COL2_X}" y="{y:.1f}" fill="{SECTION}" font-size="12" font-weight="700">— RESUME & CONNECT —</text>'
col2_title += f'<line x1="{COL2_X}" y1="{y+4:.1f}" x2="{COL2_X+360}" y2="{y+4:.1f}" stroke="{FRAME}" stroke-opacity="0.5"/>'
parts.append(rise(col2_title, 4))

connects = [
    ("LinkedIn", "linkedin.com/in/raghavendra-linga", GREEN),
    ("Email", "lingaraghawendra@gmail.com", ACCENT),
    ("Resume", "Google Drive (View CV)", GOLD)
]

cy = y + 24
for idx, (label, val, lcolor) in enumerate(connects):
    inner = (f'<text x="{COL2_X}" y="{cy:.1f}" fill="{INK}" font-size="11.5">'
             f'{label}: <tspan fill="{lcolor}">{val}</tspan></text>')
    parts.append(rise(inner, idx + 5))
    cy += 18

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("successfully wrote profiles card to", OUT)
