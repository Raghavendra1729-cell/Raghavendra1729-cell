#!/usr/bin/env python3
"""
Scrape real daily submission counts from LeetCode's public GraphQL endpoint.
Writes data/contributions.json with raw days plus derived stats.

Run daily by .github/workflows/update-profile-art.yml.
"""
import datetime
import json
import os
import sys
import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "Raghavendra-1729-cell")
# Note: we use Raghavendra-1729-cell as the default username for LeetCode.
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

def fetch_leetcode_calendar(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProfileCalendar($username: String!) {
      matchedUser(username: $username) {
        userCalendar {
          submissionCalendar
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
        
    calendar_str = matched_user.get("userCalendar", {}).get("submissionCalendar", "{}")
    return json.loads(calendar_str)

def compute_current_streak(days):
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1  # today isn't over yet -- don't break the streak on it
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]

def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end

def build_data(submission_calendar):
    # LeetCode submissionCalendar is a dict of unix_timestamp (str) -> submission_count (int)
    # We need to map this to a grid of the last 365 days.
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)
    
    # Parse submissionCalendar timestamps to YYYY-MM-DD
    submissions_by_date = {}
    for ts_str, count in submission_calendar.items():
        try:
            ts = int(ts_str)
            dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()
            date_str = dt.strftime("%Y-%m-%d")
            submissions_by_date[date_str] = count
        except (ValueError, OSError):
            continue
            
    days = []
    curr = start_date
    while curr <= today:
        date_str = curr.strftime("%Y-%m-%d")
        count = submissions_by_date.get(date_str, 0)
        days.append({"date": date_str, "count": count})
        curr += datetime.timedelta(days=1)
        
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }

if __name__ == "__main__":
    calendar = fetch_leetcode_calendar(USERNAME)
    data = build_data(calendar)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT_PATH}: {data['total_contributions']} submissions, "
          f"current streak {data['current_streak']['length']}, "
          f"longest streak {data['longest_streak']['length']}")
