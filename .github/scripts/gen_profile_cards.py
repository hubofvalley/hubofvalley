#!/usr/bin/env python3
"""Generate self-hosted profile cards (stats, languages, streak) as SVG.

Data comes from the public GitHub REST API and the public contributions
calendar, so the numbers match what a visitor sees on the profile. Standard
library only. If any fetch fails the script exits non-zero and writes nothing,
so the last good cards stay in place.
"""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

USER = os.environ.get("PROFILE_USER", "hubofvalley")
OUT = os.environ.get("PROFILE_CARDS_DIR", "assets")
FIRST_YEAR = 2022  # account created 2022-03-04

BG, BORDER = "#0a0a0a", "#2a2a2a"
TITLE, ACCENT, TEXT, MUTED = "#ffc355", "#ff6b00", "#e8e8e8", "#8b8b8b"
LANG_COLOURS = {
    "Shell": "#89e051", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Python": "#3572a5", "HTML": "#e34c26", "Go": "#00add8", "Jinja": "#a52a22",
    "Vue": "#41b883", "Rust": "#dea584", "CSS": "#663399", "Makefile": "#427819",
}
FALLBACK = ["#ff6b00", "#ffc355", "#ffd157", "#c9d1d9", "#8b8b8b", "#5c5c5c"]


def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        return ""


TOKEN = token()


def get(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "gv-profile-cards"})
    if TOKEN and url.startswith("https://api.github.com"):
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode()


def api(path):
    return json.loads(get("https://api.github.com" + path))


def repos():
    out, page = [], 1
    while True:
        chunk = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
        out += chunk
        if len(chunk) < 100:
            return [r for r in out if not r["fork"]]
        page += 1


def search_count(q):
    return api("/search/issues?per_page=1&q=" + urllib.request.quote(q))["total_count"]


def collect_stats():
    rs = repos()
    user = api(f"/users/{USER}")
    langs = {}
    for r in rs:
        for k, v in api(f"/repos/{USER}/{r['name']}/languages").items():
            langs[k] = langs.get(k, 0) + v
    return {
        "stars": sum(r["stargazers_count"] for r in rs),
        "repos": len(rs),
        "followers": user["followers"],
        "prs": search_count(f"author:{USER} type:pr is:public"),
        "merged": search_count(f"author:{USER} type:pr is:public is:merged"),
        "issues": search_count(f"author:{USER} type:issue is:public"),
        "langs": langs,
    }


def collect_days():
    today = dt.date.today()
    days = {}
    for year in range(FIRST_YEAR, today.year + 1):
        page = get(f"https://github.com/users/{USER}/contributions?from={year}-01-01&to={year}-12-31", "text/html")
        dates = dict(re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?id="(contribution-day-component-\d+-\d+)"', page))
        by_id = {v: k for k, v in dates.items()}
        for tid, text in re.findall(r'for="(contribution-day-component-\d+-\d+)"[^>]*>([^<]*)</tool-tip>', page):
            m = re.match(r"(No|\d[\d,]*) contributions?", text.strip())
            if m and tid in by_id:
                d = dt.date.fromisoformat(by_id[tid])
                if d.year == year and d <= today:
                    days[d] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))
    if not days:
        raise RuntimeError("no contribution data parsed")
    return days, today


def streaks(days, today):
    ordered = sorted(days)
    best, best_range, run, start = 0, None, 0, None
    prev = None
    for d in ordered:
        if days[d] > 0:
            if prev is not None and (d - prev).days == 1 and run:
                run += 1
            else:
                run, start = 1, d
            if run > best:
                best, best_range = run, (start, d)
            prev = d
        else:
            run, prev = 0, None
    cur, end = 0, today if days.get(today, 0) > 0 else today - dt.timedelta(days=1)
    d = end
    while days.get(d, 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    cur_range = (d + dt.timedelta(days=1), end) if cur else None
    return cur, cur_range, best, best_range


def fmt_range(r):
    if not r:
        return "-"
    a, b = r
    f = lambda x: f"{x:%b} {x.day}"
    return f"{f(a)}" if a == b else f"{f(a)} - {f(b)}"


def card(width, height, title, desc, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-labelledby="t d"><title id="t">{html.escape(title)}</title><desc id="d">{html.escape(desc)}</desc>'
        f'<style>text{{font-family:"Segoe UI",Ubuntu,"Helvetica Neue",Arial,sans-serif}}</style>'
        f'<rect x="0.5" y="0.5" rx="8" width="{width-1}" height="{height-1}" fill="{BG}" stroke="{BORDER}"/>'
        f'{body}</svg>\n'
    )


def stats_svg(s):
    rows = [("Total Stars Earned", s["stars"]), ("Public Repositories", s["repos"]),
            ("Pull Requests", s["prs"]), ("Merged Pull Requests", s["merged"]),
            ("Issues", s["issues"]), ("Followers", s["followers"])]
    body = f'<text x="25" y="35" font-size="18" font-weight="600" fill="{TITLE}">Grand Valley GitHub Stats</text>'
    for i, (k, v) in enumerate(rows):
        y = 68 + i * 26
        body += (f'<circle cx="31" cy="{y-5}" r="4" fill="{ACCENT}"/>'
                 f'<text x="46" y="{y}" font-size="14" fill="{TEXT}">{html.escape(k)}:</text>'
                 f'<text x="285" y="{y}" font-size="14" font-weight="600" fill="{TEXT}" text-anchor="end">{v:,}</text>')
    ring = (f'<circle cx="395" cy="105" r="42" fill="none" stroke="#1f1f1f" stroke-width="8"/>'
            f'<circle cx="395" cy="105" r="42" fill="none" stroke="{ACCENT}" stroke-width="8"/>'
            f'<text x="395" y="112" font-size="20" font-weight="700" fill="{TITLE}" text-anchor="middle">{s["stars"]:,}</text>'
            f'<text x="395" y="164" font-size="12" fill="{MUTED}" text-anchor="middle">stars earned</text>')
    return card(495, 215, "Grand Valley GitHub Stats",
                "Stars earned, public repositories, pull requests, issues and followers for hubofvalley.", body + ring)


def langs_svg(s):
    total = sum(s["langs"].values()) or 1
    top = [kv for kv in sorted(s["langs"].items(), key=lambda kv: -kv[1]) if kv[1] / total >= 0.001][:6]
    body = f'<text x="25" y="35" font-size="18" font-weight="600" fill="{TITLE}">Most Used Languages</text>'
    x, bar = 25.0, ""
    for i, (k, v) in enumerate(top):
        w = 250 * v / total
        c = LANG_COLOURS.get(k, FALLBACK[i % len(FALLBACK)])
        bar += f'<rect x="{x:.1f}" y="52" width="{max(w,2):.1f}" height="8" fill="{c}"/>'
        x += w
    body += f'<clipPath id="c"><rect x="25" y="52" width="250" height="8" rx="4"/></clipPath><g clip-path="url(#c)">{bar}</g>'
    for i, (k, v) in enumerate(top):
        c = LANG_COLOURS.get(k, FALLBACK[i % len(FALLBACK)])
        col, row = i % 2, i // 2
        px, py = 25 + col * 130, 90 + row * 30
        body += (f'<circle cx="{px+5}" cy="{py-4}" r="5" fill="{c}"/>'
                 f'<text x="{px+16}" y="{py}" font-size="12" fill="{TEXT}">{html.escape(k)} {100*v/total:.1f}%</text>')
    return card(300, 215, "Most Used Languages",
                "Language share across public, non-fork repositories of hubofvalley.", body)


def streak_svg(days, today):
    total = sum(days.values())
    cur, cur_r, best, best_r = streaks(days, today)
    first = min(d for d in days if days[d] > 0)
    cols = [
        (82, f"{total:,}", "Total Contributions", f"{first:%b} {first.day}, {first.year} - Present"),
        (247, f"{cur}", "Current Streak", fmt_range(cur_r)),
        (412, f"{best}", "Longest Streak", fmt_range(best_r) + (f", {best_r[1].year}" if best_r else "")),
    ]
    body = ""
    for i, (cx, big, label, sub) in enumerate(cols):
        if i:
            body += f'<line x1="{cx-82}" y1="40" x2="{cx-82}" y2="150" stroke="{BORDER}"/>'
        if i == 1:
            body += (f'<circle cx="{cx}" cy="72" r="38" fill="none" stroke="{ACCENT}" stroke-width="5"/>'
                     f'<text x="{cx}" y="82" font-size="28" font-weight="700" fill="{TITLE}" text-anchor="middle">{big}</text>'
                     f'<text x="{cx}" y="132" font-size="14" font-weight="600" fill="{ACCENT}" text-anchor="middle">{label}</text>')
        else:
            body += (f'<text x="{cx}" y="82" font-size="28" font-weight="700" fill="{TEXT}" text-anchor="middle">{big}</text>'
                     f'<text x="{cx}" y="112" font-size="14" fill="{TEXT}" text-anchor="middle">{label}</text>')
        body += f'<text x="{cx}" y="{150 if i == 1 else 134}" font-size="12" fill="{MUTED}" text-anchor="middle">{html.escape(sub)}</text>'
    return card(495, 180, "Contribution streak",
                "Total contributions, current streak and longest streak for hubofvalley.", body)


def main():
    stats = collect_stats()
    days, today = collect_days()
    files = {"stats.svg": stats_svg(stats), "langs.svg": langs_svg(stats), "streak.svg": streak_svg(days, today)}
    os.makedirs(OUT, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("ok", {k: v for k, v in stats.items() if k != "langs"}, "contributions", sum(days.values()))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # keep last good cards
        print("failed:", exc, file=sys.stderr)
        sys.exit(1)
