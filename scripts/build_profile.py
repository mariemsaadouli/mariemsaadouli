"""Builds the static profile SVGs in assets/.

Edit PROFILE / PROJECTS below, then run:  python scripts/build_profile.py
"""
import os
from svgkit import *  # noqa: F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

PROFILE = {
    "first": "Mariem",
    "last": "Saadouli",
    "kicker": "EMBEDDED · IOT · HARDWARE × SOFTWARE",
    "role": "EMBEDDED SYSTEMS · IOT · FIRMWARE",
    "tagline": "Bringing hardware and software together.",
    "school_line": "EMBEDDED SYSTEMS & IOT · ISI MAHDIA",
    "platform_line": "STM32 · ESP32 · ARDUINO · RASPBERRY PI",
    "about": ("I graduated in Embedded Systems and IoT from ISI Mahdia. I enjoy working "
              "with microcontrollers, sensors and connected devices, building projects "
              "that bring hardware and software together."),
    "datasheet": [
        ("FIELD", "Embedded Systems & IoT"),
        ("STUDIED", "ISI Mahdia"),
        ("FOCUS", "Firmware · Sensors · IoT"),
        ("CONTACT", "mariem.saadouli@ieee.org"),
    ],
}

# Fill in real projects only. Each one becomes assets/project-N.svg.
# {"name": "...", "tags": "EMBEDDED · IOT · 2025", "desc": "One line on what it does.",
#  "built": ["STM32", "C", "MQTT"], "metrics": [("4", "sensors read"), ...]  # optional, real numbers only
# }
PROJECTS = []


def write(name, svg):
    write_pair(ASSETS, name, svg)


# ---------------------------------------------------------------- hero
def hero():
    p, W, H = "mh", 900, 460
    cx, cy = 705, 205
    traces = [  # (id, d, pad_x, pad_y, label, lx, ly, anchor, begin)
        ("t1", "M645 175 H600 L585 160 H560", 560, 160, "GPIO", 560, 146, "middle", "0s"),
        ("t2", "M765 175 H805 L820 160 H850", 850, 160, "I²C", 850, 146, "middle", ".6s"),
        ("t3", "M645 235 H600 L585 250 H560", 560, 250, "SPI", 560, 274, "middle", "1.2s"),
        ("t4", "M765 235 H805 L820 250 H850", 850, 250, "UART", 850, 274, "middle", ".3s"),
        ("t5", "M705 145 V92", 705, 92, "VCC", 722, 96, "start", ".9s"),
        ("t6", "M705 265 V318", 705, 318, "GND", 722, 322, "start", "1.5s"),
    ]
    tr = []
    for tid, d, px, py, lab, lx, ly, anc, b in traces:
        tr.append(f'<path id="{p}-{tid}" d="{d}" fill="none" stroke="{LILAC}" stroke-opacity=".55" '
                  f'stroke-width="1.6" stroke-linejoin="round"/>')
        tr.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{BG0}" stroke="{PALE}" stroke-width="1.6"/>')
        tr.append(f'<text x="{lx}" y="{ly}" text-anchor="{anc}" class="mono" font-size="9" '
                  f'fill="{MUTED}" letter-spacing="1.5">{t(lab)}</text>')
        tr.append(f'<circle r="2.6" fill="{IVORY}" filter="url(#{p}-glow)" opacity="0">'
                  f'<animateMotion dur="2.4s" begin="{b}" repeatCount="indefinite"><mpath href="#{p}-{tid}"/></animateMotion>'
                  f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="2.4s" begin="{b}" repeatCount="indefinite"/></circle>')
    # chip pins
    pins = []
    for i in range(6):
        o = 157 + i * 19
        pins.append(f'<rect x="{655 + i*19}" y="137" width="4" height="9" rx="1" fill="{LILAC}" fill-opacity=".75"/>')   # top
        pins.append(f'<rect x="{655 + i*19}" y="264" width="4" height="9" rx="1" fill="{LILAC}" fill-opacity=".75"/>')   # bottom
        pins.append(f'<rect x="637" y="{o-2}" width="9" height="4" rx="1" fill="{LILAC}" fill-opacity=".75"/>')         # left
        pins.append(f'<rect x="764" y="{o-2}" width="9" height="4" rx="1" fill="{LILAC}" fill-opacity=".75"/>')         # right

    L = PROFILE
    svg = svg_open(W, H, f"{L['first']} {L['last']}: {L['role'].title()}", p)
    svg += f"""<defs>{base_defs(p, W, H)}
  <linearGradient id="{p}-die" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".9"/><stop offset="1" stop-color="#3B1D8F"/>
  </linearGradient>
</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
<g clip-path="url(#{p}-clip)">
  <rect width="{W}" height="{H}" fill="url(#{p}-bg)"/>
  <rect width="{W}" height="{H}" fill="url(#{p}-grid)"/>
  <circle cx="{cx}" cy="{cy}" r="260" fill="url(#{p}-orb)"/>

  <!-- terminal pill -->
  <rect x="36" y="34" width="268" height="30" rx="15" fill="#0E0B1C" stroke="{LINE}"/>
  <circle cx="54" cy="49" r="4" fill="{GREEN}" class="pulse"/>
  <text x="68" y="53" class="mono" font-size="12" fill="{PALE}">~/{L['first'].lower()} <tspan fill="{LILAC}">$</tspan> make flash</text>
  <rect x="226" y="42" width="7" height="14" fill="{LILAC}" class="blink"/>
  <text x="864" y="53" text-anchor="end" class="mono" font-size="10" fill="{MUTED}" letter-spacing="2">REV 2026 · MS-01</text>

  <!-- identity -->
  <text x="40" y="118" class="mono" font-size="11" fill="{LILAC}" letter-spacing="3">—— {t(L['kicker'])}</text>
  <text x="34" y="208" class="serif" font-size="96" fill="{IVORY}">{t(L['first'])}</text>
  <text x="34" y="292" class="serif" font-size="96" fill="{IVORY}">{t(L['last'])}<tspan fill="{VIOLET}">.</tspan></text>
  <text x="40" y="334" class="mono" font-size="12" fill="{IVORY}" letter-spacing="2.5">{t(L['role'])}</text>
  <text x="40" y="370" class="it" font-size="25" fill="{PALE}">{t(L['tagline'])}</text>

  <!-- chip illustration -->
  <circle cx="{cx}" cy="{cy}" r="168" fill="none" stroke="{LILAC}" stroke-opacity=".18" stroke-dasharray="2 6"/>
  <circle cx="{cx}" cy="{cy}" r="128" fill="none" stroke="{LILAC}" stroke-opacity=".08"/>
  <g>
    <circle cx="{cx}" cy="{cy-168}" r="3.5" fill="{PALE}" filter="url(#{p}-glow)"/>
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="24s" repeatCount="indefinite"/>
  </g>
  {''.join(tr)}
  {''.join(pins)}
  <rect x="645" y="145" width="120" height="120" rx="12" fill="#110D22" stroke="{LILAC}" stroke-opacity=".7"/>
  <circle cx="659" cy="159" r="3" fill="none" stroke="{LILAC}" stroke-opacity=".7"/>
  <rect x="673" y="173" width="64" height="64" rx="7" fill="url(#{p}-die)"/>
  <text x="{cx}" y="{cy+11}" text-anchor="middle" class="serif" font-size="32" fill="#FFFFFF">MS</text>
  <circle cx="752" cy="252" r="3" fill="{GREEN}" filter="url(#{p}-glow)" class="pulse"/>
  <text x="{cx}" y="384" text-anchor="middle" class="mono" font-size="9" fill="{MUTED}" letter-spacing="2">FIG. 01 · WHERE EVERY PROJECT STARTS</text>

  <!-- footer line -->
  <rect x="40" y="404" width="820" height="1" fill="{LINE}"/>
  <text x="40" y="430" class="mono" font-size="10" fill="{MUTED}" letter-spacing="2">{t(L['school_line'])}</text>
  <text x="860" y="430" text-anchor="end" class="mono" font-size="10" fill="{MUTED}" letter-spacing="2">{t(L['platform_line'])}</text>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="url(#{p}-stroke)"/>
</g>
</svg>
"""
    write("hero.svg", svg)


# ---------------------------------------------------------------- about
def about():
    p, W, H = "ma", 900, 370
    lines = wrap(PROFILE["about"], 52)
    para = "".join(f'<tspan x="68" dy="{0 if i == 0 else 27}">{t(l)}</tspan>' for i, l in enumerate(lines))
    rows = []
    y0 = 190
    for i, (k, v) in enumerate(PROFILE["datasheet"]):
        y = y0 + i * 30
        rows.append(f'<text x="586" y="{y}" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="2">{t(k)}</text>'
                    f'<text x="836" y="{y}" text-anchor="end" class="sans" font-size="13" fill="{IVORY}">{t(v)}</text>'
                    f'<rect x="586" y="{y+11}" width="250" height="1" fill="{LINE}"/>')
    svg = svg_open(W, H, "About Mariem", p)
    svg += f"""<defs>{base_defs(p, W, H)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono', 'sans')}{base_css()}</style>
{panel(p, W, H)}<g transform="translate(0 24)">
{section_header(p, '01', 'ABOUT', "Hello, I'm ", PROFILE['first'], '.')}
{card(p, 40, 116, 820, 206)}
<text x="68" y="150" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">// README.md</text>
<text x="68" y="190" class="sans" font-size="16" fill="{PALE}">{para}</text>
<rect x="560" y="136" width="1" height="166" fill="{LINE}"/>
<text x="586" y="150" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">DATASHEET</text>
<circle cx="830" cy="146" r="3.5" fill="{GREEN}" class="pulse"/>
{''.join(rows)}
</g></svg>
"""
    write("about.svg", svg)


# ---------------------------------------------------------------- toolkit
def toolkit():
    p, W, H = "mt", 900, 510

    def diamond(x, y):
        return f'<rect x="{x-5}" y="{y-5}" width="10" height="10" transform="rotate(45 {x} {y})" fill="{BG0}" stroke="{LILAC}"/>'

    svg = svg_open(W, H, "Toolkit", p)
    svg += f"""<defs>{base_defs(p, W, H)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
{panel(p, W, H)}<g transform="translate(0 24)">
{section_header(p, '03', 'TOOLKIT', 'The tools I ', 'reach for', '.', right='LANGUAGES · HARDWARE · TOOLS')}

{card(p, 40, 116, 400, 180)}
<text x="66" y="148" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">01 · LANGUAGES</text>
<text x="66" y="208" class="serif" font-size="46" fill="{IVORY}">C <tspan fill="{MUTED}">·</tspan> C++</text>
<text x="66" y="252" class="serif" font-size="32" fill="{PALE}">Python</text>
<text x="66" y="278" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="1.5">FIRMWARE · SCRIPTING · TOOLING</text>

{card(p, 460, 116, 400, 180)}
<text x="486" y="148" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">02 · HARDWARE</text>
<text x="486" y="208" class="serif" font-size="46" fill="{IVORY}">STM32 <tspan fill="{MUTED}">·</tspan> ESP32</text>
<text x="486" y="252" class="serif" font-size="32" fill="{PALE}">Arduino <tspan fill="{MUTED}">·</tspan> Raspberry Pi</text>
<text x="486" y="278" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="1.5">MICROCONTROLLERS · SINGLE-BOARD COMPUTERS</text>

{card(p, 40, 316, 540, 140)}
<text x="66" y="348" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">03 · WHAT I BUILD WITH THEM</text>
<text x="66" y="398" class="serif" font-size="34" fill="{IVORY}">Firmware <tspan fill="{MUTED}">·</tspan> <tspan class="it" fill="{PALE}">Sensors</tspan> <tspan fill="{MUTED}">·</tspan> Connected devices</text>
<text x="66" y="432" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="1.5">FROM THE PIN TO THE NETWORK</text>

{card(p, 600, 316, 260, 140)}
<text x="626" y="348" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">04 · TOOLS</text>
<text x="626" y="398" class="serif" font-size="40" fill="{IVORY}">Git</text>
<text x="626" y="432" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="1.5">VERSION CONTROL</text>

{diamond(450, 206)}{diamond(450, 306)}{diamond(590, 386)}
</g></svg>
"""
    write("toolkit.svg", svg)


# ---------------------------------------------------------------- projects
def projects_placeholder():
    """Visible 'coming soon' slot shown until PROJECTS is filled in."""
    p, W, H = "mpp", 900, 330
    slots = ""
    for i, x in enumerate((40, 320, 600)):
        slots += (f'<rect x="{x}" y="116" width="260" height="150" rx="16" fill="url(#{p}-card)" '
                  f'stroke="{LILAC}" stroke-opacity=".35" stroke-dasharray="5 6"/>'
                  f'<text x="{x+24}" y="148" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">0{i+1} · PROJECT SLOT</text>'
                  f'<rect x="{x+24}" y="170" width="150" height="14" rx="4" fill="{LINE}" class="pulse"/>'
                  f'<rect x="{x+24}" y="196" width="200" height="8" rx="4" fill="{LINE}" opacity=".7"/>'
                  f'<rect x="{x+24}" y="212" width="170" height="8" rx="4" fill="{LINE}" opacity=".7"/>'
                  f'<rect x="{x+24}" y="236" width="52" height="16" rx="8" fill="#211A42" stroke="{LINE}"/>'
                  f'<rect x="{x+84}" y="236" width="52" height="16" rx="8" fill="#211A42" stroke="{LINE}"/>')
    svg = svg_open(W, H, "Selected work: projects coming soon", p)
    svg += f"""<defs>{base_defs(p, W, H)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
{panel(p, W, H)}<g transform="translate(0 24)">
{section_header(p, '02', 'SELECTED WORK', 'Hardware, not just ', 'homework', '.', right='COMING SOON')}
{slots}
</g></svg>
"""
    write("projects-header.svg", svg)


def projects():
    if not PROJECTS:
        projects_placeholder()
        return
    p0, W = "mpH", 900
    svg = svg_open(W, 140, "Selected work", p0)
    svg += f"""<defs>{base_defs(p0, W, 140)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono')}{base_css()}</style>
{panel(p0, W, 140)}<g transform="translate(0 24)">{section_header(p0, '02', 'SELECTED WORK', 'Hardware, not just ', 'homework', '.', right='REAL BOARDS · REAL SIGNALS')}
</g></svg>
"""
    write("projects-header.svg", svg)
    for n, pr in enumerate(PROJECTS, 1):
        p = f"mp{n}"
        H = 300 if pr.get("metrics") else 230
        desc = "".join(f'<tspan x="70" dy="{0 if i == 0 else 24}">{t(l)}</tspan>'
                       for i, l in enumerate(wrap(pr["desc"], 56)))
        chips, x = [], 70
        for b in pr["built"]:
            w = 18 + len(b) * 7.4
            chips.append(f'<rect x="{x}" y="{H-58}" width="{w}" height="24" rx="12" fill="#211A42" stroke="{LINE}"/>'
                         f'<text x="{x + w/2}" y="{H-42}" text-anchor="middle" class="mono" font-size="11" fill="{PALE}">{t(b)}</text>')
            x += w + 8
        mets = ""
        for i, (num, lab) in enumerate(pr.get("metrics", [])[:3]):
            mx = 70 + i * 150
            mets += (f'<text x="{mx}" y="{H-100}" class="serif" font-size="38" fill="{IVORY}">{t(num)}</text>'
                     f'<text x="{mx}" y="{H-80}" class="mono" font-size="9.5" fill="{MUTED}" letter-spacing="1">{t(lab)}</text>')
        svg = svg_open(W, H, pr["name"], p)
        svg += f"""<defs>{base_defs(p, W, H)}</defs>
<style>{font_css('serif', 'serif-italic', 'mono', 'sans')}{base_css()}</style>
{panel(p, W, H, (760, H/2, 200))}
<circle cx="760" cy="{H/2}" r="130" fill="url(#{p}-orb)"/>
<g opacity=".9">
  <rect x="690" y="{H/2-50}" width="120" height="84" rx="8" fill="#110D22" stroke="{LILAC}" stroke-opacity=".5" transform="rotate(-8 750 {H/2})"/>
  <rect x="700" y="{H/2-38}" width="120" height="84" rx="8" fill="#16112C" stroke="{LILAC}" stroke-opacity=".7" transform="rotate(4 760 {H/2})"/>
  <rect x="742" y="{H/2-12}" width="34" height="34" rx="4" fill="{VIOLET}" fill-opacity=".8"/>
  <circle cx="805" cy="{H/2+30}" r="3" fill="{GREEN}" class="pulse"/>
</g>
<text x="70" y="50" class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">{n:02d} · {t(pr['tags'])}</text>
<text x="68" y="98" class="serif" font-size="44" fill="{IVORY}">{t(pr['name'])}</text>
<text x="70" y="130" class="sans" font-size="15" fill="{PALE}">{desc}</text>
{mets}
{''.join(chips)}
</svg>
"""
        write(f"project-{n}.svg", svg)


# ---------------------------------------------------------------- footer
def footer():
    p, W, H = "mf", 900, 110
    bits = [1,0,1,1,0,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,1,1,0,1,0,1,0,0,1,1]
    d, x = "M0 56", 0
    for b in bits:
        d += f" V{34 if b else 56} H{x+30}"; x += 30
    svg = svg_open(W, H, "Thanks for visiting", p)
    svg += f"""<defs>
  <linearGradient id="{p}-fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{LILAC}" stop-opacity="0"/><stop offset=".15" stop-color="{LILAC}"/>
    <stop offset=".85" stop-color="{LILAC}"/><stop offset="1" stop-color="{LILAC}" stop-opacity="0"/>
  </linearGradient>
  <filter id="{p}-glow" x="-10%" y="-100%" width="120%" height="300%">
    <feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>{font_css('mono', 'serif-italic')}{base_css()}
  .sig{{fill:none;stroke:url(#{p}-fade);stroke-width:2;stroke-opacity:.35;stroke-linejoin:round}}
  .run{{fill:none;stroke:{PALE};stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round;
        stroke-dasharray:90 1500;animation:run 5s linear infinite}}
  @keyframes run{{from{{stroke-dashoffset:1590}}to{{stroke-dashoffset:0}}}}
</style>
<rect width="{W}" height="{H}" rx="22" fill="{BG0}"/><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{LINE}"/>
<clipPath id="{p}-clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<g clip-path="url(#{p}-clip)"><path class="sig" d="{d}"/>
<path class="run" d="{d}" filter="url(#{p}-glow)"/></g>
<text x="450" y="94" text-anchor="middle" class="it" font-size="20" fill="{PALE}">Thanks for visiting <tspan class="mono" font-size="10" fill="{LILAC}" letter-spacing="2">· EOF</tspan></text>
</svg>
"""
    write("footer.svg", svg)


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    hero(); about(); toolkit(); projects(); footer()
