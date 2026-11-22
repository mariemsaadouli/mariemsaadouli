"""Draws assets/heatmap.svg from Mariem's REAL public GitHub contribution calendar.

Run by .github/workflows/heatmap.yml every day. Uses GitHub's public
contributions page, so no token or secret is needed. If the fetch or parsing
fails, the existing heatmap is left untouched (never replaced with fake data).

    python scripts/heatmap.py mariemsaadouli
"""
import datetime as dt
import html
import os
import re
import sys
import urllib.request

from svgkit import *  # noqa: F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "heatmap.svg")
LEVELS = ["#1E1838", "#3B2A7A", "#5B3DC4", "#8B5CF6", "#DDD6FE"]


def fetch(user):
    url = f"https://github.com/users/{user}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "profile-heatmap (github action)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(page):
    def attrs(tag):
        return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))

    tips = {}
    for m in re.finditer(r"<tool-tip\b([^>]*)>(.*?)</tool-tip>", page, re.S):
        a = attrs(m.group(1))
        txt = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        n = re.match(r"([\d,]+)\s+contribution", txt)
        tips[a.get("for", "")] = int(n.group(1).replace(",", "")) if n else 0

    days = {}
    for m in re.finditer(r"<td\b([^>]*)>", page):
        a = attrs(m.group(1))
        if "data-date" not in a:
            continue
        d = dt.date.fromisoformat(a["data-date"])
        lvl = int(a.get("data-level", "0") or 0)
        cnt = tips.get(a.get("id", ""))
        if cnt is None:
            cnt = a.get("data-count")
            cnt = int(cnt) if cnt and cnt.isdigit() else (1 if lvl else 0)
        days[d] = (cnt, lvl)
    if len(days) < 300:
        raise ValueError(f"only parsed {len(days)} days; page format may have changed")

    total = None
    h = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    if h:
        total = int(h.group(1).replace(",", ""))
    return days, total


def stats(days):
    ds = sorted(days)
    active = sum(1 for d in ds if days[d][0] > 0)
    best_d = max(ds, key=lambda d: days[d][0])
    best, cur, cur_start, s0, s1 = 0, 0, None, None, None
    for d in ds:
        if days[d][0] > 0:
            if cur == 0:
                cur_start = d
            cur += 1
            if cur > best:
                best, s0, s1 = cur, cur_start, d
        else:
            cur = 0
    return active, best, s0, s1, days[best_d][0]


def fmt(d):
    return d.strftime("%-d %b %Y").upper() if d else ""


def draw(user, days, total, num):
    p, W, H = "mhm", 900, 470
    ds = sorted(days)
    start = ds[0] - dt.timedelta(days=(ds[0].weekday() + 1) % 7)  # back to Sunday
    if total is None:
        total = sum(c for c, _ in days.values())
    active, streak, s0, s1, best = stats(days)

    gx, gy, cell, step = 104, 300, 11, 14
    cells, months, seen = [], [], set()
    for d in ds:
        col = (d - start).days // 7
        row = (d.weekday() + 1) % 7
        cnt, lvl = days[d]
        x, y = gx + col * step, gy + row * step
        cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{LEVELS[min(lvl,4)]}">'
                     f'<title>{cnt} on {d.isoformat()}</title></rect>')
        key = (d.year, d.month)
        if d.day <= 7 and row == 0 and key not in seen and col < 52:
            seen.add(key)
            months.append(f'<text x="{x}" y="{gy-10}" class="mono" font-size="9" fill="{MUTED}">{d.strftime("%b")}</text>')
    gw = ((ds[-1] - start).days // 7 + 1) * step

    def stat(x, label, value, sub):
        return (f'<text x="{x}" y="166" class="mono" font-size="9" fill="{MUTED}" letter-spacing="1.5">{t(label)}</text>'
                f'<text x="{x}" y="206" class="serif" font-size="38" fill="{IVORY}">{t(value)}</text>'
                f'<text x="{x}" y="224" class="mono" font-size="9" fill="{MUTED}">{t(sub)}</text>')

    legend = "".join(f'<rect x="{744 + i*14}" y="{gy+112}" width="11" height="11" rx="2.5" fill="{c}"/>'
                     for i, c in enumerate(LEVELS))
    streak_txt = (f"LONGEST STREAK · {streak} DAYS · {fmt(s0)} – {fmt(s1)}" if streak
                  else "NO STREAK YET · THE FIRST SQUARE IS THE HARDEST")
    updated = dt.datetime.now(dt.timezone.utc).strftime("%-d %b %Y").upper()

    svg = svg_open(W, H, f"{user}: {total} contributions in the last year", p)
    svg += f"""<defs>{base_defs(p, W, H)}
  <linearGradient id="{p}-scan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{PALE}" stop-opacity="0"/><stop offset=".5" stop-color="{PALE}" stop-opacity=".22"/>
    <stop offset="1" stop-color="{PALE}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="{p}-gclip"><rect x="{gx}" y="{gy}" width="{gw}" height="{7*step}"/></clipPath>
</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
{panel(p, W, H, (160, 360, 240))}<g transform="translate(0 24)">
{section_header(p, num, 'COMMIT LOG', 'A year of ', 'uptime', '.', right='REAL DATA · REFRESHED DAILY')}
{card(p, 40, 116, 820, 316)}
<text x="66" y="148" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">GITHUB ACTIVITY · @{t(user.upper())}</text>
<text x="66" y="196" class="serif" font-size="30" fill="{IVORY}">Every square is a day</text>
<text x="66" y="228" class="it" font-size="30" fill="{PALE}">spent building.</text>
{stat(400, 'CONTRIBUTIONS', f'{total:,}', 'last 12 months')}
{stat(530, 'ACTIVE DAYS', str(active), f'of {len(ds)} days')}
{stat(650, 'LONGEST STREAK', str(streak), 'days in a row')}
{stat(770, 'BEST DAY', str(best), 'contributions')}
<text x="{gx-12}" y="{gy+1*step+9}" text-anchor="end" class="mono" font-size="9" fill="{MUTED}">Mon</text>
<text x="{gx-12}" y="{gy+3*step+9}" text-anchor="end" class="mono" font-size="9" fill="{MUTED}">Wed</text>
<text x="{gx-12}" y="{gy+5*step+9}" text-anchor="end" class="mono" font-size="9" fill="{MUTED}">Fri</text>
{''.join(months)}
{''.join(cells)}
<g clip-path="url(#{p}-gclip)"><rect x="{gx-80}" y="{gy}" width="80" height="{7*step}" fill="url(#{p}-scan)">
  <animate attributeName="x" from="{gx-80}" to="{gx+gw}" dur="6s" repeatCount="indefinite"/></rect></g>
<text x="66" y="{gy+121}" class="mono" font-size="9" fill="{LILAC}" letter-spacing="1.5">{t(streak_txt)}</text>
<text x="736" y="{gy+121}" text-anchor="end" class="mono" font-size="9" fill="{MUTED}">LESS</text>{legend}
<text x="{744+5*14+4}" y="{gy+121}" class="mono" font-size="9" fill="{MUTED}">MORE</text>
<text x="836" y="148" text-anchor="end" class="mono" font-size="8.5" fill="{MUTED}" letter-spacing="1.5">UPDATED {updated}</text>
</g></svg>
"""
    return svg


def section_number():
    has_projects = os.path.exists(os.path.join(ROOT, "assets", "project-1.svg"))
    return "04" if has_projects else "03"


def placeholder(user):
    p, W, H = "mhm", 900, 300
    return svg_open(W, H, "GitHub activity: first sync pending", p) + f"""<defs>{base_defs(p, W, H)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
{panel(p, W, H, (160, 260, 220))}<g transform="translate(0 24)">
{section_header(p, section_number(), 'COMMIT LOG', 'A year of ', 'uptime', '.', right='REAL DATA · REFRESHED DAILY')}
{card(p, 40, 116, 820, 130)}
<circle cx="72" cy="181" r="5" fill="{GREEN}" class="pulse"/>
<text x="90" y="176" class="serif" font-size="26" fill="{IVORY}">Syncing real activity<tspan class="blink">…</tspan></text>
<text x="90" y="200" class="mono" font-size="10" fill="{MUTED}" letter-spacing="1.5">THE DAILY GITHUB ACTION DRAWS THIS FROM @{t(user.upper())}'S CONTRIBUTION CALENDAR</text>
</g></svg>
"""


if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "mariemsaadouli"
    if "--placeholder" in sys.argv:
        open(OUT, "w", encoding="utf-8").write(placeholder(user))
        sys.exit(0)
    try:
        days, total = parse(fetch(user))
    except Exception as e:  # keep the last good heatmap
        print(f"heatmap: skipped ({e})")
        sys.exit(0)
    svg = draw(user, days, total, section_number())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"heatmap: wrote {OUT} ({len(days)} days, {total} contributions)")
