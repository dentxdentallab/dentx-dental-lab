"""Builds the DentX logo as pure vector (font outlines + drawn tooth). Run: python3 tools/logo.py <fontdir>"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

fd = sys.argv[1]
serif = TTFont(f"{fd}/GildaDisplay-Regular.ttf")
sans = instantiateVariableFont(TTFont(f"{fd}/Montserrat%5Bwght%5D.ttf"), {"wght": 500})

def text_path(font, text, x, y, size, tracking=0):
    """Return (svg path d, advance width) for text with baseline at y."""
    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[g].width * s + tracking
    return pen.getCommands(), cx - x - tracking

W = 1000
# wordmark
dent, dw = text_path(serif, "Dent", 0, 0, 300)
xg, xw = text_path(serif, "X", 0, 0, 300)
total = dw + xw
x0 = (W - total) / 2
base = 560
dent, _ = text_path(serif, "Dent", x0, base, 300)
xg, _ = text_path(serif, "X", x0 + dw, base, 300)
# DENTAL LAB
lab, lw = text_path(sans, "DENTAL LAB", 0, 0, 56, tracking=24)
lx = (W - lw) / 2
lab, _ = text_path(sans, "DENTAL LAB", lx, 680, 56, tracking=24)
rule_y, rule_h = 657, 5
rules = (f'<rect x="{x0:.1f}" y="{rule_y}" width="{lx - 40 - x0:.1f}" height="{rule_h}" rx="2.5"/>'
         f'<rect x="{lx + lw + 40:.1f}" y="{rule_y}" width="{x0 + total - (lx + lw + 40):.1f}" height="{rule_h}" rx="2.5"/>')

# tooth: three brush ribbons like the original mark: left cusp + side, right cusp + side, and the cervical line underneath.
# Each ribbon is one solid tapered outline (no breaks inside a stroke); the gaps sit between ribbons.
import math
def bez(p0, p1, p2, p3, n=40):
    return [tuple((1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t*t*c + t**3*d for a, b, c, d in zip(p0, p1, p2, p3))
            for t in (i / n for i in range(n + 1))]
def ribbon(segs, wmax, w0=1.2, w1=1.2, peak=.45):
    pts = []
    for sg in segs: pts += bez(*sg)[(1 if pts else 0):]
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        t = L[i] / L[-1]
        w = (w0 + (wmax - w0) * math.sin(min(1, t / peak) * math.pi / 2)) if t < peak else (w1 + (wmax - w1) * math.sin(min(1, (1 - t) / (1 - peak)) * math.pi / 2))
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n * w / 2, dx / n * w / 2
        left.append((x + nx, y + ny)); right.append((x - nx, y - ny))
    poly = left + right[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + "Z"
A = ribbon([((166, 46), (132, 46), (104, 10), (64, 12)), ((64, 12), (28, 14), (14, 52), (22, 102)), ((22, 102), (28, 146), (48, 186), (62, 224))], 30, peak=.35)
B = ribbon([((138, 34), (170, 20), (200, 4), (234, 10)), ((234, 10), (266, 16), (280, 46), (272, 88)), ((272, 88), (268, 114), (260, 134), (252, 154))], 28, peak=.45)
C = ribbon([((286, 192), (240, 180), (182, 172), (142, 178)), ((142, 178), (110, 184), (96, 210), (92, 238)), ((92, 238), (90, 252), (90, 262), (92, 274))], 26, peak=.4)
tooth = ('<g transform="translate(350 32)">'
         f'<path fill="url(#dxa)" d="{A}"/><path fill="url(#dxb)" d="{B}"/><path fill="url(#dxc)" d="{C}"/></g>')

METAL = ('<stop offset="0" stop-color="#8a5f1c"/><stop offset=".22" stop-color="#c8963a"/><stop offset=".42" stop-color="#f7e7a8"/>'
         '<stop offset=".55" stop-color="#d9b25a"/><stop offset=".78" stop-color="#a7782a"/><stop offset="1" stop-color="#e9cd7c"/>')
grad = ('<defs>'
        f'<linearGradient id="dxg" x1="0" y1="0" x2="1" y2="1">{METAL}</linearGradient>'
        f'<linearGradient id="dxa" x1="1" y1="0" x2="0" y2="1">{METAL}</linearGradient>'
        f'<linearGradient id="dxb" x1="0" y1="0" x2="1" y2="1">{METAL}</linearGradient>'
        f'<linearGradient id="dxc" x1="1" y1="0" x2="0" y2="1">{METAL}</linearGradient></defs>')

for name, ink in (("logo.svg", "#1d3268"), ("logo-white.svg", "#f6f1e6")):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 {W} 680" role="img" aria-label="DentX Dental Lab">{grad}'
           f'{tooth}<path fill="{ink}" stroke="{ink}" stroke-width="5" stroke-linejoin="round" d="{dent}"/><path fill="url(#dxg)" stroke="url(#dxg)" stroke-width="5" stroke-linejoin="round" d="{xg}"/>'
           f'<path fill="{ink}" d="{lab}"/><g fill="url(#dxg)">{rules}</g></svg>')
    open(f"assets/{name}", "w").write(svg)
print("ok", round(x0), round(total), round(lx), round(lw))
open("assets/favicon.svg", "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="330 20 340 300">{grad}'
    f'<rect x="330" y="20" width="340" height="300" rx="60" fill="#071a3d"/>{tooth}</svg>')
