"""
Neofetch-style info card for Tarun Madhav Gudipati.
Fades/slides in line-by-line alongside the ASCII portrait.
STATIC=1 emits a frozen frame for previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 490, 430
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 100
LINE_H = 21.5

BG      = "#0d1117"
BG2     = "#111722"
FRAME   = "#30363d"
MUTED   = "#7d8590"
INK     = "#c9d1d9"
KEY     = "#ffa657"        # orange keys
SECTION = "#58a6ff"        # blue section headers
GREEN   = "#3fb950"
ACCENT  = "#22d3ee"        # cyan — matches the profile README accent
RED     = "#f85149"

ROWS = [
    ("host",),
    ("kv",  "Role",     "Security Engineer · AI Builder · Full-Stack"),
    ("kv",  "Status",   "B.Tech CSE @ KLEF · Class of 2027"),
    ("kv",  "Location", "Hyderabad / Vijayawada, India 🇮🇳"),
    ("gap",),
    ("sec", "Building"),
    ("bul", "🤖  JARVIS — fully local AI voice assistant (Llama 3.2)"),
    ("bul", "📅  ChronoPA — AI-powered cross-platform calendar"),
    ("bul", "☁️  CloudGuard — AWS/Azure IAM misconfiguration auditor"),
    ("bul", "🔍  SentinelScan — Nmap + NVD CVE vulnerability scanner"),
    ("gap",),
    ("sec", "Stack"),
    ("kv",  "Security",  "Python · Nmap · CVE APIs · Zero-Trust"),
    ("kv",  "Backend",   "Java · Spring Boot · FastAPI · Node.js"),
    ("kv",  "Frontend",  "React · React Native · Expo · TypeScript"),
    ("kv",  "Cloud",     "AWS ☑  Azure ☑  GCP ☑  Docker · K8s"),
    ("kv",  "AI / ML",   "Ollama · LLaMA · Whisper · TensorFlow"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "AWS Certified Cloud Practitioner"),
    ("bul", "Microsoft Azure Fundamentals AZ-900"),
    ("bul", "Google Cloud Cybersecurity Internship"),
    ("bul", "CIIE Innovation Hub — Lead @ KLEF"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """Fade + slight upward slide staggered by row index, freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.12 + i * 0.055
    return (
        f'<g opacity="0" transform="translate(0,5)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',

    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',

    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">tarun@github: ~$ neofetch</text>'
)

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.45
        continue

    if kind == "host":
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
            f'<tspan fill="{GREEN}">tarun</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT}">github</tspan></text>'
            f'<line x1="{KEY_X + 112}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "sec":
        title = esc(row[1])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
            f'&#8212; {title}</text>'
            f'<line x1="{KEY_X + 14 + len(row[1])*7}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12" font-weight="700">{key}</text>'
            f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12">{val}</text>'
        )
    elif kind == "bul":
        txt = esc(row[1])
        inner = (
            f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
            f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12">{txt}</text>'
        )
    else:
        continue

    parts.append(rise(inner, i))
    y += LINE_H

# blinking cursor at the bottom
cursor_y = y + 8
parts.append(
    f'<text x="{KEY_X}" y="{cursor_y:.1f}" fill="{MUTED}" font-size="12">'
    f'tarun@github:~$ <tspan fill="{INK}">▌</tspan></text>'
)
parts.append(
    f'<rect x="{KEY_X + 148}" y="{cursor_y-12:.1f}" width="8" height="13" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}  {len(svg)} bytes  {W}x{H}")
