#!/usr/bin/env python3
"""Generate entry.png: a newspaper-style one-image summary of 23 Nov 2026 world news.
Deterministic, PIL-only, run locally. The submitted main.py just copies this PNG."""
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (247, 243, 234)
INK = (18, 18, 20)
SUB = (70, 70, 76)
CARD = (255, 255, 255)
LINE = (205, 198, 182)

FB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FS = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, W), BG)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=font(FS, 62), fill=INK, anchor="ma")
d.rectangle([28, 108, W - 28, 114], fill=(178, 34, 34))
d.rectangle([0, 128, W, 188], fill=INK)
d.text((W // 2, 143), "MONDAY  23  NOVEMBER  2026", font=font(FB, 41), fill=(255, 255, 255), anchor="ma")

# ---- Icons (drawn inside a coloured circle, centre cx, cy, r=40) ----
def circle(cx, cy, color):
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=color)

def icon_globe(cx, cy):
    circle(cx, cy, (37, 99, 168))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(255, 255, 255), width=4)
    d.line([cx - 26, cy, cx + 26, cy], fill=(255, 255, 255), width=3)
    d.arc([cx - 12, cy - 26, cx + 12, cy + 26], 90, 270, fill=(255, 255, 255), width=3)
    d.arc([cx - 12, cy - 26, cx + 12, cy + 26], 270, 90, fill=(255, 255, 255), width=3)
    d.line([cx + 8, cy - 20, cx - 2, cy - 2, cx + 10, cy + 8, cx + 2, cy + 24], fill=(255, 210, 63), width=4)

def icon_chip(cx, cy):
    circle(cx, cy, (22, 140, 74))
    d.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], outline=(255, 255, 255), width=4)
    for i in (-14, 0, 14):
        d.line([cx + i, cy - 30, cx + i, cy - 20], fill=(255, 255, 255), width=4)
        d.line([cx + i, cy + 20, cx + i, cy + 30], fill=(255, 255, 255), width=4)
        d.line([cx - 30, cy + i, cx - 20, cy + i], fill=(255, 255, 255), width=4)
        d.line([cx + 20, cy + i, cx + 30, cy + i], fill=(255, 255, 255), width=4)
    d.polygon([(cx - 10, cy + 10), (cx + 2, cy - 6), (cx + 6, cy + 2), (cx + 14, cy - 12), (cx + 14, cy + 10)], fill=(255, 210, 63))

def icon_drone(cx, cy):
    circle(cx, cy, (90, 70, 160))
    # sea waves
    for k, yy in enumerate((cy + 18, cy + 28)):
        pts = [(cx - 28 + i * 8, yy + (3 if (i + k) % 2 else -3)) for i in range(8)]
        d.line(pts, fill=(140, 200, 255), width=3)
    # ship hull
    d.polygon([(cx - 4, cy + 14), (cx + 30, cy + 14), (cx + 24, cy + 4), (cx  - 2, cy + 4)], fill=(255, 255, 255))
    d.rectangle([cx + 14, cy - 6, cx + 24, cy + 4], fill=(255, 255, 255))
    # quadcopter drone, top-left
    d.rectangle([cx - 22, cy - 14, cx - 6, cy - 6], fill=(255, 210, 63))
    for rx in (cx - 28, cx):
        d.line([rx, cy - 20, rx + 12, cy - 20], fill=(255, 210, 63), width=3)
        d.line([rx + 6, cy - 26, rx + 6, cy - 20], fill=(255, 210, 63), width=2)
    d.line([cx - 14, cy - 6, cx - 14, cy + 0], fill=(255, 210, 63), width=2)

def icon_tanker(cx, cy):
    circle(cx, cy, (178, 90, 20))
    d.polygon([(cx - 30, cy + 8), (cx + 30, cy + 8), (cx + 22, cy + 20), (cx - 22, cy + 20)], fill=(255, 255, 255))
    d.rectangle([cx - 26, cy - 2, cx + 18, cy + 8], fill=(255, 255, 255))
    d.rectangle([cx + 20, cy - 14, cx + 28, cy + 8], fill=(255, 255, 255))
    d.ellipse([cx - 8, cy - 16, cx + 10, cy - 2], outline=(255, 210, 63), width=4)  # oil drop ring

def icon_factory(cx, cy):
    circle(cx, cy, (178, 34, 34))
    d.polygon([(cx - 28, cy + 24), (cx - 28, cy - 4), (cx - 8, cy + 6), (cx - 8, cy - 4), (cx + 12, cy + 6), (cx + 12, cy - 16), (cx + 22, cy - 16), (cx + 22, cy + 24)], outline=(255, 255, 255), width=4)
    # flame
    d.polygon([(cx + 2, cy - 30), (cx + 12, cy - 12), (cx + 7, cy - 4), (cx - 3, cy - 12)], fill=(255, 150, 40))
    d.polygon([(cx + 3, cy - 20), (cx + 8, cy - 10), (cx + 2, cy - 6), (cx - 1, cy - 12)], fill=(255, 210, 63))

def icon_city(cx, cy):
    circle(cx, cy, (30, 120, 130))
    d.rectangle([cx - 28, cy - 2, cx - 12, cy + 28], fill=(255, 255, 255))
    d.rectangle([cx - 8, cy - 12, cx + 10, cy + 28], fill=(255, 255, 255))
    d.rectangle([cx + 14, cy + 4, cx + 29, cy + 28], fill=(255, 255, 255))
    for wx in (cx - 23, cx - 3, cx + 18):
        for wy in (cy + 4, cy + 14):
            d.rectangle([wx, wy, wx + 5, wy + 6], fill=(30, 120, 130))
    # UN flag on the tall building
    d.line([cx + 1, cy - 30, cx + 1, cy - 12], fill=(255, 255, 255), width=3)
    d.rectangle([cx + 1, cy - 30, cx + 25, cy - 17], fill=(90, 170, 255))
    d.text((cx + 13, cy - 30), "UN", font=font(FB, 12), fill=(255, 255, 255), anchor="ma")

def icon_eye(cx, cy):
    circle(cx, cy, (200, 60, 120))
    d.ellipse([cx - 30, cy - 16, cx + 30, cy + 16], outline=(255, 255, 255), width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 255, 255))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(30, 30, 40))
    d.polygon([(cx, cy + 22), (cx - 8, cy + 32), (cx + 8, cy + 32)], fill=(255, 210, 63))

def icon_planet(cx, cy):
    circle(cx, cy, (40, 50, 110))
    d.ellipse([cx - 4, cy - 4, cx + 30, cy + 30], fill=(190, 185, 175))  # Mercury
    d.ellipse([cx + 6, cy + 6, cx + 13, cy + 13], fill=(150, 145, 135))
    d.ellipse([cx + 16, cy + 16, cx + 22, cy + 22], fill=(150, 145, 135))
    # spacecraft
    d.rectangle([cx - 26, cy - 18, cx - 12, cy - 8], fill=(255, 210, 63))
    d.rectangle([cx - 30, cy - 22, cx - 20, cy - 4], fill=(90, 170, 255))
    d.line([cx - 12, cy - 13, cx + 2, cy - 2], fill=(255, 255, 255), width=3)
    for sx, sy in ((-26, 24), (-12, 28), (24, -22), (30, -8)):
        d.line([cx + sx - 3, cy + sy, cx + sx + 3, cy + sy], fill=(255, 255, 255), width=2)
        d.line([cx + sx, cy + sy - 3, cx + sx, cy + sy + 3], fill=(255, 255, 255), width=2)

PANELS = [
    ("CLIMATE", icon_globe, "COP31 ENDS WITH\nNO DEAL", "Antalya talks split over fossil fuels"),
    ("TECH / MARKETS", icon_chip, "NVIDIA RESTORES\nCEO HUANG", "Shares jump +30% in a day"),
    ("WAR / EUROPE-AFRICA", icon_drone, "UKRAINE DRONES SINK\nRUSSIAN WARSHIP", "Ukraine says: at Benghazi, Libya"),
    ("MIDDLE EAST / ENERGY", icon_tanker, "IRAN-US STANDOFF\nIN HORMUZ STRAIT", "Tankers hit - oil near $92"),
    ("DISASTER / ASIA", icon_factory, "INDONESIA FACTORY\nFIRE KILLS 24", "About 30 people still missing"),
    ("AFRICA / WAR", icon_city, "DRONES HIT HOMES &\nUN BUILDING", "Night strikes on Khartoum, Sudan"),
    ("ASIA / POLITICS", icon_eye, "S. KOREA NAMES FIRST\nWOMAN SPY CHIEF", "A first in the agency since 1961"),
    ("SCIENCE / SPACE", icon_planet, "PROBE SAFE IN\nMERCURY ORBIT", "Europe-Japan, after 8-year trip"),
]

X0, Y0 = 24, 206
PW, PH, GAP = 488, 186, 12
for i, (cat, icon, head, sub) in enumerate(PANELS):
    col, row = i % 2, i // 2
    x = X0 + col * (PW + GAP)
    y = Y0 + row * (PH + GAP)
    d.rounded_rectangle([x, y, x + PW, y + PH], radius=14, fill=CARD, outline=LINE, width=2)
    icon(x + 66, y + PH // 2)
    tx = x + 128
    d.text((tx, y + 18), cat, font=font(FB, 19), fill=(178, 34, 34))
    size = 31
    while size > 22:
        f = font(FB, size)
        if max(d.textlength(line, font=f) for line in head.split("\n")) <= PW - 128 - 14:
            break
        size -= 1
    d.multiline_text((tx, y + 46), head, font=font(FB, size), fill=INK, spacing=3)
    d.text((tx, y + PH - 40), sub, font=font(FR, 22), fill=SUB)

d.text((W // 2, 992), "ONE DAY OF WORLD NEWS - AS REPORTED ON 23 NOVEMBER 2026", font=font(FB, 19), fill=SUB, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image/entry.png")
print("saved", img.size)
