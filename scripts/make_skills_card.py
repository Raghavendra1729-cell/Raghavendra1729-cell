#!/usr/bin/env python3
"""
Generate a beautiful, column-based technical skills terminal SVG card (skills-card.svg)
to sit BELOW the top table. 
Titled: raghav@github: ~$ ./show_skills.sh
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "skills-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 860, 260
PAD = 25
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
SECTION = "#58a6ff"  # Blue section titles
GREEN = "#3fb950"
ACCENT = "#22d3ee"   # Cyan sub-info
KEY = "#ffa657"      # Orange bullet dots

COL1_X = PAD + 10
COL2_X = PAD + 285
COL3_X = PAD + 560

# Data structure for layout
COLS = [
    # Column 1
    {
        "x": COL1_X,
        "sections": [
            {
                "title": "🔭 CURRENT FOCUS",
                "items": [
                    ("bul", "AI Eng. (RAG, Embeddings, LLMs)"),
                    ("bul", "Backend (High-Perf Architectures)"),
                    ("bul", "Problem Solving (DSA & CP)")
                ]
            },
            {
                "title": "💻 LANGUAGES",
                "items": [
                    ("txt", "Java, C++, Python"),
                    ("txt", "JavaScript, SQL")
                ]
            }
        ]
    },
    # Column 2
    {
        "x": COL2_X,
        "sections": [
            {
                "title": "⚙️ BACKEND & ARCHITECTURE",
                "items": [
                    ("bul", "Spring Boot, Node.js"),
                    ("bul", "Apache Kafka, Redis"),
                    ("bul", "Microservices, Socket.io")
                ]
            },
            {
                "title": "🤖 ARTIFICIAL INTELLIGENCE",
                "items": [
                    ("txt", "GenAI, RAG Pipelines"),
                    ("txt", "Scikit-Learn, Pandas, NumPy")
                ]
            }
        ]
    },
    # Column 3
    {
        "x": COL3_X,
        "sections": [
            {
                "title": "📚 CS FUNDAMENTALS",
                "items": [
                    ("bul", "Data Structures & Algorithms"),
                    ("bul", "OOP, Operating Systems (OS)"),
                    ("bul", "Computer Networks, DBMS")
                ]
            },
            {
                "title": "🔧 TOOLS & PLATFORMS",
                "items": [
                    ("txt", "Git, Docker, Postman"),
                    ("txt", "MongoDB, MySQL")
                ]
            }
        ]
    }
]

def rise(inner, delay_idx):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.2 + delay_idx * 0.04
    return (f'<g opacity="0" transform="translate(0,4)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.3s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#sbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">raghav@github: ~$ ./show_skills.sh</text>')

delay_idx = 0
for col in COLS:
    cx = col["x"]
    y = TITLEBAR_H + 28
    for sec in col["sections"]:
        # Section title
        sec_title = sec["title"]
        title_inner = f'<text x="{cx}" y="{y:.1f}" fill="{SECTION}" font-size="12" font-weight="700">{sec_title}</text>'
        title_inner += f'<line x1="{cx}" y1="{y+4:.1f}" x2="{cx+245}" y2="{y+4:.1f}" stroke="{FRAME}" stroke-opacity="0.5"/>'
        parts.append(rise(title_inner, delay_idx))
        delay_idx += 1
        y += 24
        
        # Section items
        for item_type, text in sec["items"]:
            if item_type == "bul":
                item_inner = (f'<circle cx="{cx+3}" cy="{y-4:.1f}" r="2" fill="{GREEN}"/>'
                              f'<text x="{cx+12}" y="{y:.1f}" fill="{INK}" font-size="11.5">{text}</text>')
            else: # txt
                item_inner = f'<text x="{cx}" y="{y:.1f}" fill="{INK}" font-size="11.5">{text}</text>'
            
            parts.append(rise(item_inner, delay_idx))
            delay_idx += 1
            y += 18
        y += 14  # Space between sections

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("successfully wrote skills card to", OUT)
