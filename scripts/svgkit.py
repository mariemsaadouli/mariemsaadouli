"""Shared design system for Mariem's profile SVGs.

Fonts (SIL OFL 1.1): Instrument Serif, JetBrains Mono, Inter, all from Fontsource.
They are subset to Latin characters and embedded as base64, because GitHub
shows README SVGs as images and those cannot load external web fonts.
"""
import base64, io, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---- palette ------------------------------------------------------------
BG0 = "#0B0A14"   # midnight
BG1 = "#14102A"   # deep indigo
CARD = "#15112A"
CARD2 = "#1C1638"
LINE = "#2F2757"
VIOLET = "#7C3AED"
LILAC = "#A78BFA"
PALE = "#DDD6FE"
IVORY = "#F5F3FF"
MUTED = "#8C86AB"
GREEN = "#4ADE80"

SERIF = "'MS Serif', 'Instrument Serif', Georgia, 'Times New Roman', serif"
MONO = "'MS Mono', 'JetBrains Mono', Consolas, 'Courier New', monospace"
SANS = "'MS Sans', Inter, 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"

_FONTS = {
    # family alias: (file, style, weight)
    "serif": ("serif.woff2", "MS Serif", "normal", 400),
    "serif-italic": ("serif-italic.woff2", "MS Serif", "italic", 400),
    "mono": ("mono.woff2", "MS Mono", "normal", 500),
    "sans": ("sans.woff2", "MS Sans", "normal", 400),
    "sans-bold": ("sans-bold.woff2", "MS Sans", "normal", 600),
}
_CHARS = "".join(chr(c) for c in range(0x20, 0x7F)) + "·×²→—–★•…’“”é°"
_cache = {}


def _subset_b64(fname):
    if fname in _cache:
        return _cache[fname]
    path = os.path.join(FONT_DIR, fname)
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        font = TTFont(path)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        sub = subset.Subsetter(opts)
        sub.populate(text=_CHARS)
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        data = buf.getvalue()
    except Exception:  # fontTools/brotli missing: embed the full file
        data = open(path, "rb").read()
    _cache[fname] = base64.b64encode(data).decode()
    return _cache[fname]


def font_css(*aliases):
    out = []
    for a in aliases:
        f, fam, style, weight = _FONTS[a]
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{_subset_b64(f)}) format('woff2');}}"
        )
    return "\n".join(out)


def t(s):
    """Escape text for SVG."""
    return escape(s, quote=True)


def svg_open(w, h, label, prefix):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{t(label)}">\n'
        f"<title>{t(label)}</title>\n"
    )


def base_defs(p, w, h):
    """Common gradients, grid and glow. p = unique id prefix."""
    return f"""
  <linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
  </linearGradient>
  <linearGradient id="{p}-card" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CARD2}"/><stop offset="1" stop-color="{CARD}"/>
  </linearGradient>
  <linearGradient id="{p}-rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{LILAC}"/><stop offset="1" stop-color="{LILAC}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="{p}-stroke" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{LILAC}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{LINE}"/>
    <stop offset="1" stop-color="{LILAC}" stop-opacity=".35"/>
  </linearGradient>
  <radialGradient id="{p}-orb" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="{p}-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{LILAC}" stroke-opacity=".06"/>
  </pattern>
  <filter id="{p}-glow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="{p}-clip"><rect width="{w}" height="{h}" rx="22"/></clipPath>"""


def base_css():
    return f"""
  .serif{{font-family:{SERIF};font-weight:400}}
  .it{{font-family:{SERIF};font-style:italic;font-weight:400}}
  .mono{{font-family:{MONO};font-weight:500}}
  .sans{{font-family:{SANS};font-weight:400}}
  .sansb{{font-family:{SANS};font-weight:600}}
  .blink{{animation:blink 1.1s steps(2,start) infinite}}
  .pulse{{animation:pulse 1.8s ease-in-out infinite}}
  @keyframes blink{{to{{visibility:hidden}}}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}"""


def section_header(p, num, kicker, head, accent, tail, y=0, right=""):
    """Editorial section header: '01 · ABOUT' + big serif line with italic accent."""
    r = (f'<text x="860" y="{y+26}" text-anchor="end" class="mono" font-size="10" '
         f'fill="{MUTED}" letter-spacing="2">{t(right)}</text>') if right else ""
    return f"""
  <text x="40" y="{y+26}" class="mono" font-size="11" fill="{LILAC}" letter-spacing="3">{num} · {t(kicker)}</text>{r}
  <text x="40" y="{y+74}" class="serif" font-size="44" fill="{IVORY}">{t(head)}<tspan class="it" fill="{LILAC}">{t(accent)}</tspan>{t(tail)}</text>
  <rect x="40" y="{y+90}" width="420" height="1.5" fill="url(#{p}-rule)"/>"""


def card(p, x, y, w, h, rx=16):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{p}-card)" '
            f'stroke="url(#{p}-stroke)" stroke-width="1"/>')


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > max_chars:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def panel(p, w, h, orb=(760, 80, 220)):
    """Dark rounded background so every section reads on GitHub light AND dark themes."""
    ox, oy, r = orb
    return (f'<rect width="{w}" height="{h}" rx="22" fill="url(#{p}-bg)"/>'
            f'<rect width="{w}" height="{h}" rx="22" fill="url(#{p}-grid)"/>'
            f'<circle cx="{ox}" cy="{oy}" r="{r}" fill="url(#{p}-orb)" opacity=".7" clip-path="url(#{p}-clip)"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="url(#{p}-stroke)"/>')
