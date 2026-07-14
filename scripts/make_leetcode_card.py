#!/usr/bin/env python3
"""
Fetch LeetCode stats and render a beautiful, custom dashboard SVG (leetcode-card.svg)
displaying total solved questions, easy/medium/hard progress bars, global ranking,
and current submission streak.
"""
import json
import os
import sys
import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "Raghavendra-1729-cell")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "leetcode-card.svg")

def fetch_leetcode_stats(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userLeetCodeStats($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        profile {
          ranking
          reputation
        }
        userCalendar {
          streak
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    headers = {
        "content-type": "application/json",
        "referer": f"https://leetcode.com/{username}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    payload = {
        "query": query,
        "variables": {"username": username}
    }
    
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        print(f"User {username} not found on LeetCode", file=sys.stderr)
        sys.exit(1)
        
    return {
        "all_questions": data["data"]["allQuestionsCount"],
        "solved_questions": matched_user["submitStats"]["acSubmissionNum"],
        "ranking": matched_user["profile"]["ranking"],
        "reputation": matched_user["profile"]["reputation"],
        "streak": matched_user["userCalendar"]["streak"]
    }

def render_svg(stats):
    # Extract numbers
    total_questions = {q["difficulty"]: q["count"] for q in stats["all_questions"]}
    solved_questions = {q["difficulty"]: q["count"] for q in stats["solved_questions"]}
    
    solved_all = solved_questions.get("All", 0)
    total_all = total_questions.get("All", 0)
    
    solved_easy = solved_questions.get("Easy", 0)
    total_easy = total_questions.get("Easy", 0)
    
    solved_med = solved_questions.get("Medium", 0)
    total_med = total_questions.get("Medium", 0)
    
    solved_hard = solved_questions.get("Hard", 0)
    total_hard = total_questions.get("Hard", 0)
    
    ranking = stats["ranking"]
    streak = stats["streak"]
    
    # Progress math
    pct_all = solved_all / total_all if total_all else 0
    pct_easy = solved_easy / total_easy if total_easy else 0
    pct_med = solved_med / total_med if total_med else 0
    pct_hard = solved_hard / total_hard if total_hard else 0
    
    # Circular progress (radius=48, circumference=301.6)
    r = 48
    circ = 2 * 3.14159265 * r
    offset_all = circ * (1 - pct_all)
    
    # Bar width (max 260px)
    max_bar_w = 260
    w_easy = max_bar_w * pct_easy
    w_med = max_bar_w * pct_med
    w_hard = max_bar_w * pct_hard
    
    # Theme colors
    BG = "#0d1117"
    BG2 = "#111722"
    FRAME = "#30363d"
    MUTED = "#7d8590"
    INK = "#c9d1d9"
    CYAN = "#22d3ee"
    GREEN = "#2ec866"
    ORANGE = "#fea116"
    RED = "#f25f5c"
    GOLD = "#f2cc60"
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200" viewBox="0 0 860 200" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  <defs>
    <linearGradient id="lbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG2}"/>
      <stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <style>
      @keyframes countUp {{
        from {{ stroke-dashoffset: {circ:.1f}; }}
        to {{ stroke-dashoffset: {offset_all:.1f}; }}
      }}
      @keyframes barEasy {{ from {{ width: 0; }} to {{ width: {w_easy:.1f}px; }} }}
      @keyframes barMed {{ from {{ width: 0; }} to {{ width: {w_med:.1f}px; }} }}
      @keyframes barHard {{ from {{ width: 0; }} to {{ width: {w_hard:.1f}px; }} }}
      .ring {{
        stroke-dasharray: {circ:.1f};
        stroke-dashoffset: {offset_all:.1f};
        animation: countUp 1.2s cubic-bezier(.2,.8,.2,1) forwards;
        transform: rotate(-90deg);
        transform-origin: 90px 115px;
      }}
      .easy-fill {{ animation: barEasy 1s ease-out forwards; }}
      .med-fill {{ animation: barMed 1.1s ease-out forwards; }}
      .hard-fill {{ animation: barHard 1.2s ease-out forwards; }}
    </style>
  </defs>

  <rect width="860" height="200" rx="12" fill="url(#lbg)"/>
  <rect x="0.5" y="0.5" width="859" height="199" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>
  
  <!-- Title bar -->
  <line x1="0" y1="30" x2="860" y2="30" stroke="{FRAME}"/>
  <circle cx="20" cy="15" r="5" fill="#ff5f56"/>
  <circle cx="36" cy="15" r="5" fill="#ffbd2e"/>
  <circle cx="52" cy="15" r="5" fill="#27c93f"/>
  <text x="430" y="19" fill="{MUTED}" font-size="12" text-anchor="middle">raghav@leetcode: ~$ leetcode-cli --stats</text>

  <!-- Left: Circular progress (All solved) -->
  <circle cx="90" cy="115" r="{r}" fill="none" stroke="{FRAME}" stroke-width="8"/>
  <circle cx="90" cy="115" r="{r}" fill="none" stroke="{CYAN}" stroke-width="8" stroke-linecap="round" class="ring"/>
  <text x="90" y="112" fill="{INK}" font-size="22" font-weight="700" text-anchor="middle">{solved_all}</text>
  <text x="90" y="128" fill="{MUTED}" font-size="11" text-anchor="middle">/ {total_all} Solved</text>

  <!-- Middle: Difficulty Progress Bars -->
  <!-- Easy -->
  <text x="210" y="79" fill="{GREEN}" font-size="12" font-weight="700">Easy</text>
  <rect x="270" y="70" width="{max_bar_w}" height="10" rx="5" fill="{FRAME}"/>
  <rect x="270" y="70" width="{w_easy:.1f}" height="10" rx="5" fill="{GREEN}" class="easy-fill"/>
  <text x="550" y="79" fill="{INK}" font-size="12" font-weight="700">{solved_easy}<tspan fill="{MUTED}" font-weight="400">/{total_easy}</tspan></text>

  <!-- Medium -->
  <text x="210" y="119" fill="{ORANGE}" font-size="12" font-weight="700">Medium</text>
  <rect x="270" y="110" width="{max_bar_w}" height="10" rx="5" fill="{FRAME}"/>
  <rect x="270" y="110" width="{w_med:.1f}" height="10" rx="5" fill="{ORANGE}" class="med-fill"/>
  <text x="550" y="119" fill="{INK}" font-size="12" font-weight="700">{solved_med}<tspan fill="{MUTED}" font-weight="400">/{total_med}</tspan></text>

  <!-- Hard -->
  <text x="210" y="159" fill="{RED}" font-size="12" font-weight="700">Hard</text>
  <rect x="270" y="150" width="{max_bar_w}" height="10" rx="5" fill="{FRAME}"/>
  <rect x="270" y="150" width="{w_hard:.1f}" height="10" rx="5" fill="{RED}" class="hard-fill"/>
  <text x="550" y="159" fill="{INK}" font-size="12" font-weight="700">{solved_hard}<tspan fill="{MUTED}" font-weight="400">/{total_hard}</tspan></text>

  <!-- Right: Stats Panel -->
  <line x1="620" y1="45" x2="620" y2="185" stroke="{FRAME}" stroke-dasharray="3,3"/>
  
  <!-- Global Rank -->
  <g transform="translate(645, 55)">
    <text x="0" y="20" fill="{MUTED}" font-size="12">Global Rank</text>
    <text x="0" y="44" fill="{GOLD}" font-size="20" font-weight="700">#{ranking:,}</text>
  </g>

  <!-- Streak -->
  <g transform="translate(645, 120)">
    <text x="0" y="20" fill="{MUTED}" font-size="12">Active Streak</text>
    <text x="0" y="44" fill="{ORANGE}" font-size="20" font-weight="700">{streak} Days 🔥</text>
  </g>
</svg>
"""
    return svg

if __name__ == "__main__":
    stats = fetch_leetcode_stats(USERNAME)
    svg = render_svg(stats)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"successfully wrote LeetCode card to {OUT_PATH}")
