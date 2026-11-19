#!/usr/bin/env python3
"""Render the news poster for Thursday 19 November 2026.

Draws a 1024x1024 newspaper front page with Pillow: masthead, six stories
(each drawn with simple geometric illustration + headline + short factual
summary), and a ticker strip. Fully deterministic: no randomness, no clock,
no network. Run: python3 render.py  ->  entry.png in this directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 227)      # warm newsprint
INK = (26, 26, 26)           # near-black ink
RED = (176, 42, 30)          # masthead / kicker red
NAVY = (31, 78, 121)         # ticker band
MUTED = (90, 86, 76)         # secondary text
LINE = (26, 26, 26)
SOFT = (226, 219, 200)       # panel divider

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=1.28):
    """Draw lines of text; returns y after the last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, label):
    f = font(SANS_B, 17)
    draw.text((x, y), label, font=f, fill=RED)
    return y + 24


def headline(draw, x, y, text, fnt, max_w):
    lines = wrap(draw, text, fnt, max_w)
    return text_block(draw, x, y, lines, fnt, leading=1.08)


def body(draw, x, y, text, max_w, size=19):
    f = font(SANS, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, x, y, lines, f, leading=1.3)


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=LINE, width=2)


# ---------------------------------------------------------------- illustrations
def draw_skyline(d, x, y, w, h):
    """Vice City at dusk: gradient sky, sun, skyline, palms, sea."""
    top, bot = (255, 170, 90), (235, 90, 110)
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun
    cx, cy, r = x + int(w * 0.72), y + int(h * 0.34), 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 170))
    # skyline blocks
    base = y + h - 26
    blocks = [(0.00, 0.16, 0.52), (0.15, 0.12, 0.66), (0.27, 0.20, 0.44),
              (0.46, 0.13, 0.74), (0.58, 0.18, 0.55), (0.74, 0.12, 0.68),
              (0.85, 0.15, 0.50)]
    for fx, fw, fh in blocks:
        bx, bw = x + int(w * fx), int(w * fw)
        bh = int(h * fh)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(38, 32, 54))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 5, bx + bw - 4, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 120))
    # palms (two simple silhouettes)
    for px, ph in [(0.06, 0.30), (0.93, 0.26)]:
        tx = x + int(w * px)
        ty = base
        d.line([(tx, ty), (tx + 6, ty - int(h * ph))], fill=(30, 46, 32), width=4)
        apex = (tx + 6, ty - int(h * ph))
        for dx, dy in [(-22, -4), (-16, -14), (2, -18), (16, -14), (22, -2),
                       (-12, 4), (12, 6)]:
            d.line([apex, (apex[0] + dx, apex[1] + dy)], fill=(30, 46, 32), width=3)
    # sea strip
    d.rectangle([x, base, x + w, y + h], fill=(44, 90, 130))
    d.line([(x, base + 8), (x + w, base + 8)], fill=(150, 200, 230), width=2)
    d.line([(x, base + 17), (x + w, base + 17)], fill=(150, 200, 230), width=2)


def draw_flags(d, x, y, w, h):
    """Three abstract flag panels: US, China, Russia. No text inside art."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    pw, gap = (w - 2 * 14) // 3, 14
    # US: stripes + blue canton
    ux = x
    for i in range(7):
        d.rectangle([ux, y + i * (h // 7), ux + pw, y + (i + 1) * (h // 7)],
                    fill=(178, 34, 52) if i % 2 == 0 else (245, 245, 245))
    d.rectangle([ux, y, ux + int(pw * 0.45), y + int(h * 0.55)], fill=(40, 60, 120))
    for sy in range(3):
        for sx in range(2):
            d.ellipse([ux + 6 + sx * 12, y + 8 + sy * 16,
                       ux + 11 + sx * 12, y + 13 + sy * 16], fill=(255, 255, 255))
    # China: red field + stars
    cx = x + pw + gap
    d.rectangle([cx, y, cx + pw, y + h], fill=(222, 41, 16))
    d.ellipse([cx + 12, y + 12, cx + 26, y + 26], fill=(255, 222, 0))
    for sx, sy in [(34, 14), (40, 24), (36, 36), (24, 38)]:
        d.ellipse([cx + sx, y + sy, cx + sx + 7, y + sy + 7], fill=(255, 222, 0))
    # Russia: white / blue / red horizontal bands
    rx = x + 2 * (pw + gap)
    d.rectangle([rx, y, rx + pw, y + h // 3], fill=(245, 245, 245))
    d.rectangle([rx, y + h // 3, rx + pw, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([rx, y + 2 * h // 3, rx + pw, y + h], fill=(213, 0, 50))


def draw_dome(d, x, y, w, h):
    """US Capitol dome abstraction, scaled to fit its box."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 235))
    cx = x + w // 2
    base = y + h - 8
    # low side wings to fill the wide panel
    d.rectangle([x + 8, base - 22, cx - 78, base], fill=(235, 234, 228))
    d.rectangle([cx + 78, base - 22, x + w - 8, base], fill=(235, 234, 228))
    # dome: half-ellipse cap
    d.pieslice([cx - 70, base - 74, cx + 70, base - 8], 180, 360,
               fill=(245, 244, 238))
    # drum under the dome
    d.rectangle([cx - 64, base - 34, cx + 64, base - 14], fill=(245, 244, 238))
    # finial
    d.rectangle([cx - 3, base - 82, cx + 3, base - 72], fill=(120, 110, 96))
    d.ellipse([cx - 5, base - 88, cx + 5, base - 78], fill=(120, 110, 96))
    # columns across the drum
    for i in range(5):
        colx = cx - 58 + i * 26
        d.rectangle([colx, base - 14, colx + 9, base], fill=(245, 244, 238))
    d.rectangle([x, base, x + w, y + h], fill=(120, 128, 110))


def draw_cyclone(d, x, y, w, h):
    """Spiral storm over a coastline: concentric arcs + rain streaks."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    cx, cy = x + int(w * 0.62), y + int(h * 0.52)
    for r in range(14, 92, 14):
        d.arc([cx - r, cy - int(r * 0.8), cx + r, cy + int(r * 0.8)],
              start=200, end=470, fill=(255, 255, 255), width=7)
    d.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(245, 244, 238))
    # coastline strip bottom-left
    d.polygon([(x, y + h), (x, y + h - 34), (x + int(w * 0.42), y + h - 52),
               (x + int(w * 0.55), y + h - 30), (x + int(w * 0.5), y + h)],
              fill=(150, 130, 90))
    # rain streaks
    for rx in range(x + 14, x + w - 10, 26):
        d.line([(rx, y + 10), (rx - 6, y + 34)], fill=(120, 150, 180), width=3)


def draw_bars(d, x, y, w, h):
    """Pew projection bars: Muslims 2.57bn vs Christians 2.52bn by 2035."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    f_lab = font(SANS_B, 16)
    f_num = font(SANS_B, 20)
    rows = [("MUSLIMS", "2.57 bn", 2.57, (34, 120, 90)),
            ("CHRISTIANS", "2.52 bn", 2.52, (31, 78, 121))]
    ry = y + 8
    for label, num, val, col in rows:
        d.text((x + 6, ry), label, font=f_lab, fill=INK)
        d.text((x + w - 84, ry - 2), num, font=f_num, fill=col)
        bar_y = ry + 23
        bar_w = int((w - 12) * (val / 2.57))
        d.rectangle([x + 6, bar_y, x + 6 + bar_w, bar_y + 16], fill=col)
        ry += 44
    d.text((x + 6, ry), "Projected population, 2035  •  Pew Research Center",
           font=font(SANS, 14), fill=MUTED)


def draw_strata(d, x, y, w, h):
    """Great Unconformity: young rock sitting on ancient rock, gap between."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    # young sandstone layers (top)
    for i, col in enumerate([(222, 196, 140), (214, 182, 120), (226, 204, 152)]):
        d.rectangle([x, y + i * 11, x + w, y + (i + 1) * 11], fill=col)
    # the gap: jagged dark line
    gy = y + 36
    pts = [(x, gy)]
    step = w // 12
    for i in range(13):
        pts.append((x + i * step, gy + (8 if i % 2 else -5)))
    pts.append((x + w, gy))
    d.line(pts, fill=(120, 40, 30), width=3)
    d.text((x + 8, gy + 7), "1.2 BILLION YEARS MISSING", font=font(SANS_B, 15),
           fill=(176, 42, 30))
    # ancient basement rock (bottom)
    for i, col in enumerate([(96, 92, 110), (82, 78, 96), (110, 104, 122)]):
        d.rectangle([x, gy + 28 + i * 11, x + w, gy + 39 + i * 11], fill=col)
    # rising arrow (mantle currents), right side
    ax = x + w - 34
    d.line([(ax, y + h - 8), (ax, gy + 56)], fill=(176, 42, 30), width=3)
    d.polygon([(ax - 6, gy + 66), (ax + 6, gy + 66), (ax, gy + 54)],
              fill=(176, 42, 30))


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((W // 2, 24), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=INK, anchor="ma")
    d.text((W // 2, 88), "T H U R S D A Y ,  1 9  N O V E M B E R  2 0 2 6",
           font=font(SANS_B, 22), fill=INK, anchor="ma")
    d.rectangle([24, 122, 1000, 126], fill=RED)
    d.rectangle([24, 130, 1000, 131], fill=LINE)

    # ---- lead row: GTA VI (left, wide) + Shenzhen summit (right)
    y0 = 142
    lead_h = 288
    # GTA VI
    panel(d, 24, y0, 576, lead_h)
    draw_skyline(d, 30, y0 + 6, 564, 138)
    ty = y0 + 152
    ty = kicker(d, 36, ty, "CULTURE  •  GAMING")
    ty = headline(d, 36, ty, "VICE CITY OPENS", font(SERIF_B, 40), 552)
    body(d, 36, ty + 6,
         "Grand Theft Auto VI begins its global rollout after a 13-year wait, "
         "sending gamers back to Vice City.", 552)
    # Summit
    panel(d, 612, y0, 388, lead_h)
    draw_flags(d, 618, y0 + 6, 376, 118)
    ty = y0 + 132
    ty = kicker(d, 624, ty, "DIPLOMACY  •  SHENZHEN")
    ty = headline(d, 624, ty, "THREE LEADERS, ONE ROOM", font(SERIF_B, 24), 364)
    body(d, 624, ty + 6,
         "Trump, Xi and Putin meet today in Shenzhen for first-ever three-way "
         "talks. Nuclear arms top the agenda.", 364, size=18)

    # ---- middle row: Jeffries + Cyclone Akvan
    y1 = 442
    mid_h = 252
    panel(d, 24, y1, 482, mid_h)
    draw_dome(d, 30, y1 + 6, 470, 104)
    ty = y1 + 118
    ty = kicker(d, 36, ty, "WASHINGTON")
    ty = headline(d, 36, ty, "FIRST BLACK SPEAKER NOMINEE",
                  font(SERIF_B, 27), 458)
    body(d, 36, ty + 6,
         "House Democrats nominate Hakeem Jeffries for Speaker — a first for "
         "an African-American.", 458, size=18)

    panel(d, 518, y1, 482, mid_h)
    draw_cyclone(d, 524, y1 + 6, 470, 104)
    ty = y1 + 118
    ty = kicker(d, 530, ty, "WEATHER  •  INDIA")
    ty = headline(d, 530, ty, "STORM BEARS DOWN ON INDIA",
                  font(SERIF_B, 27), 458)
    body(d, 530, ty + 6,
         "Severe Cyclone Akvan nears India's east coast. Red alerts are out; "
         "schools shut until 21 Nov.", 458, size=18)

    # ---- bottom row: Pew + Great Unconformity
    y2 = 706
    bot_h = 210
    panel(d, 24, y2, 482, bot_h)
    ty = y2 + 8
    ty = kicker(d, 36, ty, "DEMOGRAPHICS")
    ty = headline(d, 36, ty, "ISLAM TO PASS CHRISTIANITY BY 2035",
                  font(SERIF_B, 24), 458)
    draw_bars(d, 36, ty + 4, 458, 108)

    panel(d, 518, y2, 482, bot_h)
    ty = y2 + 8
    ty = kicker(d, 530, ty, "SCIENCE")
    ty = headline(d, 530, ty, "EARTH'S MISSING BILLION YEARS",
                  font(SERIF_B, 24), 458)
    draw_strata(d, 530, ty + 4, 458, 108)

    # ---- ticker
    d.rectangle([0, 928, W, H], fill=NAVY)
    tick_lines = [
        "VOYAGER 1  •  NASA to confirm one-light-day milestone at noon ET",
        "FED MINUTES  •  More rate hikes ahead   —   NVIDIA halts H-series chips to China",
        "EU unveils €45bn Ukraine loan plan   —   Oil falls 3.2% to $83.26",
    ]
    f_tick = font(SANS_B, 16)
    for i, line in enumerate(tick_lines):
        assert d.textlength(line, font=f_tick) <= 976, line
        d.text((24, 934 + i * 22), line, font=f_tick,
               fill=(245, 244, 238) if i == 0 else (200, 212, 226))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    render()
