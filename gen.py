#!/usr/bin/env python3
"""v3: newspaper-style one-image summary of 23 Nov 2026 world news.
Fixes applied: verified Indonesia figures (3 dead / 36 missing, official Sunday),
Korea = nominates + pending confirmation, unified REGION / THEME categories,
date band padding, NVIDIA as featured top story, distinct Hormuz strait icon,
government-building icon for Korea, sources footer, Strait of Hormuz wording."""
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (247, 243, 234)
INK = (18, 18, 20)
SUB = (70, 70, 76)
CARD = (255, 255, 255)
LINE = (205, 198, 182)
RED = (178, 34, 34)

FB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FS = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"

def font(p, s):
    return ImageFont.truetype(p, s)

img = Image.new("RGB", (W, W), BG)
d = ImageDraw.Draw(img)

def fit(text, path, size, maxw, minsize=16):
    while size > minsize:
        f = font(path, size)
        if d.textlength(text, font=f) <= maxw:
            return f
        size -= 1
    return font(path, minsize)

def fit_multi(lines, path, size, maxw, minsize=18):
    while size > minsize:
        f = font(path, size)
        if max(d.textlength(l, font=f) for l in lines) <= maxw:
            return f
        size -= 1
    return font(path, minsize)

# ---- Masthead ----
d.text((W // 2, 18), "THE WORLD IN ONE DAY", font=font(FS, 58), fill=INK, anchor="ma")
d.rectangle([28, 94, W - 28, 100], fill=RED)
# Date band with even padding
d.rectangle([0, 112, W, 166], fill=INK)
d.text((W // 2, 139), "MONDAY  23  NOVEMBER  2026", font=font(FB, 38), fill=(255, 255, 255), anchor="mm")

# ---- Icons ----
def circle(cx, cy, color, r=40):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def icon_globe(cx, cy):
    circle(cx, cy, (37, 99, 168))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(255, 255, 255), width=4)
    d.line([cx - 26, cy, cx + 26, cy], fill=(255, 255, 255), width=3)
    d.arc([cx - 12, cy - 26, cx + 12, cy + 26], 90, 270, fill=(255, 255, 255), width=3)
    d.arc([cx - 12, cy - 26, cx + 12, cy + 26], 270, 90, fill=(255, 255, 255), width=3)
    d.line([cx + 8, cy - 20, cx - 2, cy - 2, cx + 10, cy + 8, cx + 2, cy + 24], fill=(255, 210, 63), width=4)

def icon_chip(cx, cy, r=40):
    circle(cx, cy, (22, 140, 74), r)
    s = r / 40.0
    d.rectangle([cx - 20*s, cy - 20*s, cx + 20*s, cy + 20*s], outline=(255, 255, 255), width=max(3, int(4*s)))
    for i in (-14, 0, 14):
        d.line([cx + i*s, cy - 30*s, cx + i*s, cy - 20*s], fill=(255, 255, 255), width=max(3, int(4*s)))
        d.line([cx + i*s, cy + 20*s, cx + i*s, cy + 30*s], fill=(255, 255, 255), width=max(3, int(4*s)))
        d.line([cx - 30*s, cy + i*s, cx - 20*s, cy + i*s], fill=(255, 255, 255), width=max(3, int(4*s)))
        d.line([cx + 20*s, cy + i*s, cx + 30*s, cy + i*s], fill=(255, 255, 255), width=max(3, int(4*s)))
    d.polygon([(cx - 10*s, cy + 10*s), (cx + 2*s, cy - 6*s), (cx + 6*s, cy + 2*s), (cx + 14*s, cy - 12*s), (cx + 14*s, cy + 10*s)], fill=(255, 210, 63))

def icon_drone(cx, cy):
    circle(cx, cy, (90, 70, 160))
    for k, yy in enumerate((cy + 18, cy + 28)):
        pts = [(cx - 28 + i * 8, yy + (3 if (i + k) % 2 else -3)) for i in range(8)]
        d.line(pts, fill=(140, 200, 255), width=3)
    d.polygon([(cx - 4, cy + 14), (cx + 30, cy + 14), (cx + 24, cy + 4), (cx - 2, cy + 4)], fill=(255, 255, 255))
    d.rectangle([cx + 14, cy - 6, cx + 24, cy + 4], fill=(255, 255, 255))
    d.rectangle([cx - 22, cy - 14, cx - 6, cy - 6], fill=(255, 210, 63))
    for rx in (cx - 28, cx):
        d.line([rx, cy - 20, rx + 12, cy - 20], fill=(255, 210, 63), width=3)

def icon_strait(cx, cy):
    # tanker passing a narrow strait between two land masses, clipped to a circle
    S = 84
    layer = Image.new("RGBA", (S, S), (20, 110, 150, 255))
    ld = ImageDraw.Draw(layer)
    ld.polygon([(0, 0), (48, 0), (28, 34), (0, 40)], fill=(196, 154, 92, 255))
    ld.polygon([(84, 0), (38, 0), (58, 36), (84, 42)], fill=(196, 154, 92, 255))
    ld.polygon([(0, 84), (34, 84), (26, 54), (0, 60)], fill=(196, 154, 92, 255))
    ld.polygon([(84, 84), (50, 84), (60, 56), (84, 62)], fill=(196, 154, 92, 255))
    ld.polygon([(26, 44), (60, 44), (55, 52), (31, 52)], fill=(255, 255, 255, 255))
    ld.rectangle([29, 37, 51, 44], fill=(255, 255, 255, 255))
    ld.rectangle([53, 31, 58, 44], fill=(255, 255, 255, 255))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([2, 2, S - 2, S - 2], fill=255)
    img.paste(layer, (cx - S // 2, cy - S // 2), mask)

def icon_factory(cx, cy):
    circle(cx, cy, (178, 34, 34))
    d.polygon([(cx - 28, cy + 24), (cx - 28, cy - 4), (cx - 8, cy + 6), (cx - 8, cy - 4), (cx + 12, cy + 6), (cx + 12, cy - 16), (cx + 22, cy - 16), (cx + 22, cy + 24)], outline=(255, 255, 255), width=4)
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
    d.line([cx + 1, cy - 30, cx + 1, cy - 12], fill=(255, 255, 255), width=3)
    d.rectangle([cx + 1, cy - 30, cx + 25, cy - 17], fill=(90, 170, 255))
    d.text((cx + 13, cy - 30), "UN", font=font(FB, 12), fill=(255, 255, 255), anchor="ma")

def icon_gov(cx, cy):
    # government building: pediment, columns, steps (no eye/triangle symbolism)
    circle(cx, cy, (200, 60, 120))
    d.polygon([(cx - 30, cy - 18), (cx + 30, cy - 18), (cx, cy - 32)], fill=(255, 255, 255))
    d.rectangle([cx - 30, cy - 14, cx + 30, cy - 8], fill=(255, 255, 255))
    for i in (-22, -8, 8, 22):
        d.rectangle([cx + i - 3, cy - 4, cx + i + 3, cy + 16], fill=(255, 255, 255))
    d.rectangle([cx - 32, cy + 20, cx + 32, cy + 26], fill=(255, 255, 255))
    d.rectangle([cx - 26, cy + 14, cx + 26, cy + 20], fill=(255, 255, 255))
    d.ellipse([cx - 4, cy - 28, cx + 4, cy - 20], fill=(255, 210, 63))

def icon_planet(cx, cy):
    circle(cx, cy, (40, 50, 110), 30)
    d.ellipse([cx - 2, cy - 2, cx + 22, cy + 22], fill=(190, 185, 175))
    d.ellipse([cx + 5, cy + 5, cx + 10, cy + 10], fill=(150, 145, 135))
    d.ellipse([cx + 12, cy + 12, cx + 17, cy + 17], fill=(150, 145, 135))
    d.rectangle([cx - 20, cy - 14, cx - 9, cy - 6], fill=(255, 210, 63))
    d.rectangle([cx - 23, cy - 17, cx - 15, cy - 3], fill=(90, 170, 255))
    d.line([cx - 9, cy - 10, cx + 1, cy - 1], fill=(255, 255, 255), width=2)

# ---- Featured: NVIDIA ----
FX, FY, FW, FH = 24, 176, W - 48, 172
d.rounded_rectangle([FX, FY, FX + FW, FY + FH], radius=16, fill=(24, 28, 38))
icon_chip(FX + 92, FY + FH // 2, 56)
tx = FX + 178
d.text((tx, FY + 20), "TOP STORY  ·  US / MARKETS", font=font(FB, 21), fill=(255, 190, 80))
hf = fit_multi(["NVIDIA BRINGS BACK", "CEO JENSEN HUANG"], FB, 38, FW - 178 - 24)
d.multiline_text((tx, FY + 46), "NVIDIA BRINGS BACK\nCEO JENSEN HUANG", font=hf, fill=(255, 255, 255), spacing=2)
d.text((tx, FY + FH - 36), "Reinstated 11 days after his exit · shares surge 30%+", font=fit("Reinstated 11 days after his exit · shares surge 30%+", FR, 23, FW - 178 - 24, 18), fill=(205, 210, 220))

# ---- Grid panels ----
PANELS = [
    ("GLOBAL / CLIMATE", icon_globe, "COP31 ENDS WITH\nNO DEAL", "Antalya talks split over fossil fuels"),
    ("EUROPE-AFRICA / WAR", icon_drone, "UKRAINE DRONES SINK\nRUSSIAN WARSHIP", "Off Benghazi, Libya · Kyiv claims"),
    ("MIDDLE EAST / ENERGY", icon_strait, "IRAN-US STANDOFF IN\nSTRAIT OF HORMUZ", "Tankers hit · oil near $92"),
    ("ASIA / DISASTER", icon_factory, "INDONESIA FACTORY\nFIRE KILLS 24", "About 30 still missing near Jakarta"),
    ("AFRICA / WAR", icon_city, "KHARTOUM: DRONES HIT\nHOMES & UN SITE", "Night strikes on Sudan's capital"),
    ("ASIA / POLITICS", icon_gov, "S. KOREA NOMINATES\nFIRST WOMAN SPY CHIEF", "Awaits hearing · first since 1961"),
]
X0, Y0 = 24, 360
PW, PH, GAP = 488, 172, 10
for i, (cat, icon, head, sub) in enumerate(PANELS):
    col, row = i % 2, i // 2
    x = X0 + col * (PW + GAP)
    y = Y0 + row * (PH + GAP)
    d.rounded_rectangle([x, y, x + PW, y + PH], radius=14, fill=CARD, outline=LINE, width=2)
    icon(x + 66, y + PH // 2)
    tx = x + 128
    d.text((tx, y + 16), cat, font=font(FB, 19), fill=RED)
    hf = fit_multi(head.split("\n"), FB, 30, PW - 128 - 14)
    d.multiline_text((tx, y + 44), head, font=hf, fill=INK, spacing=3)
    d.text((tx, y + PH - 36), sub, font=fit(sub, FR, 21, PW - 128 - 14, 17), fill=SUB)

# ---- Bottom strip: space ----
SX, SY, SW, SH = 24, 904, W - 48, 72
d.rounded_rectangle([SX, SY, SX + SW, SY + SH], radius=12, fill=CARD, outline=LINE, width=2)
icon_planet(SX + 48, SY + SH // 2)
strip = "EUROPE-JAPAN / SPACE:  PROBE SAFE IN MERCURY ORBIT · BepiColombo, after an 8-year journey"
d.text((SX + 94, SY + SH // 2), strip, font=fit(strip, FB, 23, SW - 94 - 16, 16), fill=INK, anchor="lm")

# ---- Footer with sources ----
d.text((W // 2, 986), "Sources: Reuters, AP, AFP, CNN, Al Jazeera, Yonhap, ESA", font=font(FB, 18), fill=SUB, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image/entry.png")
print("saved", img.size)
