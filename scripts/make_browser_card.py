#!/usr/bin/env python3
"""
Generate a premium browser mockup SVG (browser-card.svg) showcasing the Diablo AI Agent.
Titled with URL: https://raghav-1729-diablo-ai-agent.hf.space
Clickable link in README redirects to the live Hugging Face Space.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "browser-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 860, 340
TITLEBAR_H = 45

BG = "#0d1117"
BG2 = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
CYAN = "#38bdf8"
ACCENT = "#1f6feb"

def fade(inner, delay):
    if STATIC:
        return f"<g>{inner}</g>"
    return (f'<g opacity="0">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="bbg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    
    # Browser Titlebar / Header
    f'<rect x="0" y="0" width="{W}" height="{TITLEBAR_H}" rx="12" fill="{BG2}"/>',
    f'<rect x="0" y="{TITLEBAR_H-12}" width="{W}" height="12" fill="{BG2}"/>', # cover bottom rounding
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# Window Control Dots (MacOS Style)
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{25 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

# Browser URL Address Bar
url_w = 480
url_x = (W - url_w) / 2
parts.append(f'<rect x="{url_x}" y="9" width="{url_w}" height="26" rx="13" fill="{BG}" stroke="{FRAME}"/>')
parts.append(f'<text x="{W/2}" y="26" fill="{CYAN}" font-size="11.5" text-anchor="middle">https://raghav-1729-diablo-ai-agent.hf.space</text>')

# 1. User Bubble
y1 = TITLEBAR_H + 25
user_bubble = (
    f'<rect x="40" y="{y1}" width="780" height="52" rx="8" fill="#21262d" stroke="{FRAME}"/>'
    f'<text x="60" y="{y1+22}" fill="{MUTED}" font-size="12" font-weight="700">USER</text>'
    f'<text x="60" y="{y1+39}" fill="{INK}" font-size="12">Who is Raghavendra and what is Diablo?</text>'
)
parts.append(fade(user_bubble, 0.2))

# 2. Diablo Agent Bubble
y2 = y1 + 72
diablo_bubble = (
    f'<rect x="40" y="{y2}" width="780" height="96" rx="8" fill="{BG}" stroke="{CYAN}" stroke-width="1.5"/>'
    f'<text x="60" y="{y2+24}" fill="{CYAN}" font-size="12" font-weight="700">DIABLO_AGENT</text>'
    f'<text x="60" y="{y2+44}" fill="{INK}" font-size="12">I am an autonomous AI agent built by Raghavendra. He is a Software</text>'
    f'<text x="60" y="{y2+62}" fill="{INK}" font-size="12">Engineering Student at Scaler School of Technology focusing on AI and RAG.</text>'
    f'<text x="60" y="{y2+80}" fill="{CYAN}" font-size="12" font-weight="700">Click anywhere on this browser to start chatting with me live! 💬</text>'
)
parts.append(fade(diablo_bubble, 0.6))

# 3. Simulated Input Bar
y3 = y2 + 116
input_bar = (
    f'<rect x="40" y="{y3}" width="780" height="40" rx="20" fill="{BG2}" stroke="{FRAME}"/>'
    f'<text x="60" y="{y3+24}" fill="{MUTED}" font-size="12">Type a message to Diablo... <tspan fill="{INK}">|</tspan></text>'
)
parts.append(fade(input_bar, 1.0))

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("successfully wrote browser card to", OUT)
