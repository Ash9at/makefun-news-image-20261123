#!/usr/bin/env python3
"""v5: v4 + competitor-inspired upgrades: numbers strip, REPORTED/CLAIM certainty
tags, ALSO ON MONDAY micro-stories (verified 23 Nov items), DATE CHECK box."""
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

def fit(text, path, size, maxw, minsize=12):
    while size > minsize:
        f = font(path, size)
        if d.textlength(text, font=f) <= maxw:
            return f
        size -= 1
    return font(path, minsize)

def fit_multi(lines, path, size, maxw, minsize=16):
    while size > minsize:
        f = font(path, size)
        if max(d.textlength(l, font=f) for l in lines) <= maxw:
            return f
        size -= 1
    return font(path, minsize)

# ---- Masthead ----
d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=font(FS, 54), fill=INK, anchor="ma")
d.rectangle([28, 84, W - 28, 89], fill=RED)
d.rectangle([0, 100, W, 152], fill=INK)
d.text((W // 2, 126), "MONDAY  23  NOVEMBER  2026", font=font(FB, 36), fill=(255, 255, 255), anchor="mm")

# ---- Numbers strip ----
STATS = [
    ("+30%", "NVIDIA SHARES IN A DAY"),
    ("$92", "BRENT OIL, HORMUZ HITS"),
    ("24", "DEAD IN JAVA FIRE"),
    ("1st", "WOMAN TO LEAD KOREA NIS"),
    ("8 yrs", "BEPICOLOMBO TO MERCURY"),
]
SY, SH = 162, 54
d.rectangle([24, SY, W - 24, SY + SH], fill=(238, 231, 216))
cellw = (W - 48) / 5
for i, (num, lab) in enumerate(STATS):
    cx = 24 + cellw * i + cellw / 2
    d.text((cx, SY + 5), num, font=font(FB, 24), fill=RED, anchor="ma")
    d.text((cx, SY + 35), lab, font=fit(lab, FB, 12, cellw - 10, 10), fill=SUB, anchor="ma")
    if i:
        d.line([24 + cellw * i, SY + 8, 24 + cellw * i, SY + SH - 8], fill=LINE, width=2)

# ---- Icons ----
def circle(cx, cy, color, r=34):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def icon_globe(cx, cy):
    circle(cx, cy, (37, 99, 168))
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(255, 255, 255), width=3)
    d.line([cx - 22, cy, cx + 22, cy], fill=(255, 255, 255), width=3)
    d.arc([cx - 10, cy - 22, cx + 10, cy + 22], 90, 270, fill=(255, 255, 255), width=2)
    d.arc([cx - 10, cy - 22, cx + 10, cy + 22], 270, 90, fill=(255, 255, 255), width=2)
    d.line([cx + 7, cy - 17, cx - 2, cy - 2, cx + 8, cy + 7, cx + 2, cy + 20], fill=(255, 210, 63), width=3)

def icon_chip(cx, cy, r=48):
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
    for k, yy in enumerate((cy + 15, cy + 24)):
        pts = [(cx - 24 + i * 7, yy + (3 if (i + k) % 2 else -3)) for i in range(7)]
        d.line(pts, fill=(140, 200, 255), width=3)
    d.polygon([(cx - 3, cy + 12), (cx + 26, cy + 12), (cx + 20, cy + 3), (cx - 2, cy + 3)], fill=(255, 255, 255))
    d.rectangle([cx + 12, cy - 5, cx + 20, cy + 3], fill=(255, 255, 255))
    d.rectangle([cx - 19, cy - 12, cx - 5, cy - 5], fill=(255, 210, 63))
    for rx in (cx - 24, cx):
        d.line([rx, cy - 17, rx + 10, cy - 17], fill=(255, 210, 63), width=3)

def icon_strait(cx, cy):
    S = 72
    layer = Image.new("RGBA", (S, S), (20, 110, 150, 255))
    ld = ImageDraw.Draw(layer)
    ld.polygon([(0, 0), (41, 0), (24, 29), (0, 34)], fill=(196, 154, 92, 255))
    ld.polygon([(72, 0), (33, 0), (50, 31), (72, 36)], fill=(196, 154, 92, 255))
    ld.polygon([(0, 72), (29, 72), (22, 46), (0, 51)], fill=(196, 154, 92, 255))
    ld.polygon([(72, 72), (43, 72), (51, 48), (72, 53)], fill=(196, 154, 92, 255))
    ld.polygon([(22, 38), (51, 38), (47, 45), (27, 45)], fill=(255, 255, 255, 255))
    ld.rectangle([25, 32, (44), 38], fill=(255, 255, 255, 255))
    ld.rectangle([45, 27, 50, 38], fill=(255, 255, 255, 255))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([2, 2, S - 2, S - 2], fill=255)
    img.paste(layer, (cx - S // 2, cy - S // 2), mask)

def icon_factory(cx, cy):
    circle(cx, cy, (178, 34, 34))
    d.polygon([(cx - 24, cy + 20), (cx - 24, cy - 3), (cx - 7, cy + 5), (cx - 7, cy - 3), (cx + 10, cy + 5), (cx + 10, cy - 13), (cx + 19, cy - 13), (cx + 19, cy + 20)], outline=(255, 255, 255), width=3)
    d.polygon([(cx + 2, cy - 25), (cx + 10, cy - 10), (cx + 6, cy - 3), (cx - 2, cy - 10)], fill=(255, 150, 40))
    d.polygon([(cx + 3, cy - 17), (cx + 7, cy - 8), (cx + 2, cy - 5), (cx - 1, cy - 10)], fill=(255, 210, 63))

def icon_city(cx, cy):
    circle(cx, cy, (30, 120, 130))
    d.rectangle([cx - 24, cy - 2, cx - 10, cy + 24], fill=(255, 255, 255))
    d.rectangle([cx - 7, cy - 10, cx + 9, cy + 24], fill=(255, 255, 255))
    d.rectangle([cx + 12, cy + 3, cx + 25, cy + 24], fill=(255, 255, 255))
    for wx in (cx - 20, cx - 3, cx + 15):
        for wy in (cy + 3, cy + 12):
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(30, 120, 130))
    d.line([cx + 1, cy - 26, cx + 1, cy - 10], fill=(255, 255, 255), width=2)
    d.rectangle([cx + 1, cy - 26, cx + 21, cy - 15], fill=(90, 170, 255))
    d.text((cx + 11, cy - 26), "UN", font=font(FB, 10), fill=(255, 255, 255), anchor="ma")

def icon_gov(cx, cy):
    circle(cx, cy, (200, 60, 120))
    d.polygon([(cx - 26, cy - 15), (cx + 26, cy - 15), (cx, cy - 27)], fill=(255, 255, 255))
    d.rectangle([cx - 26, cy - 12, cx + 26, cy - 7], fill=(255, 255, 255))
    for i in (-19, -7, 7, 19):
        d.rectangle([cx + i - 3, cy - 3, cx + i + 3, cy + 14], fill=(255, 255, 255))
    d.rectangle([cx - 28, cy + 17, cx + 28, cy + 22], fill=(255, 255, 255))
    d.rectangle([cx - 22, cy + 12, cx + 22, cy + 17], fill=(255, 255, 255))
    d.ellipse([cx - 3, cy - 24, cx + 3, cy - 18], fill=(255, 210, 63))

def tag(x_right, y, kind):
    label = "CLAIM" if kind == "claim" else "REPORTED"
    bg = (240, 180, 60) if kind == "claim" else (225, 222, 214)
    fg = (60, 45, 0) if kind == "claim" else (95, 95, 100)
    f = font(FB, 12)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x_right - w, y, x_right, y + 19], radius=4, fill=bg)
    d.text((x_right - w / 2, y + 3), label, font=f, fill=fg, anchor="ma")

# ---- Featured: NVIDIA ----
FX, FY, FW, FH = 24, 224, W - 48, 154
d.rounded_rectangle([FX, FY, FX + FW, FY + FH], radius=16, fill=(24, 28, 38))
icon_chip(FX + 84, FY + FH // 2, 48)
tx = FX + 158
d.text((tx, FY + 15), "TOP STORY  ·  US / MARKETS", font=font(FB, 20), fill=(255, 190, 80))
tag(FX + FW - 16, FY + 13, "reported")
hf = fit_multi(["NVIDIA BRINGS BACK", "CEO JENSEN HUANG"], FB, 34, FW - 158 - 24)
d.multiline_text((tx, FY + 40), "NVIDIA BRINGS BACK\nCEO JENSEN HUANG", font=hf, fill=(255, 255, 255), spacing=2)
d.text((tx, FY + FH - 30), "Reinstated 11 days after his exit · shares surge 30%+", font=fit("Reinstated 11 days after his exit · shares surge 30%+", FR, 22, FW - 158 - 24, 16), fill=(205, 210, 220))

# ---- Grid panels ----
PANELS = [
    ("GLOBAL / CLIMATE", icon_globe, "COP31 ENDS WITH\nNO DEAL", "Antalya talks split over fossil fuels", "reported"),
    ("EUROPE-AFRICA / WAR", icon_drone, "UKRAINE DRONES SINK\nRUSSIAN WARSHIP", "Off Benghazi, Libya · Kyiv claims", "claim"),
    ("MIDDLE EAST / ENERGY", icon_strait, "IRAN-US STANDOFF IN\nSTRAIT OF HORMUZ", "Tankers hit · oil near $92", "reported"),
    ("ASIA / DISASTER", icon_factory, "INDONESIA FACTORY\nFIRE KILLS 24", "About 30 still missing near Jakarta", "reported"),
    ("AFRICA / WAR", icon_city, "KHARTOUM: DRONES HIT\nHOMES & UN SITE", "Night strikes on Sudan's capital", "reported"),
    ("ASIA / POLITICS", icon_gov, "S. KOREA NOMINATES\nFIRST WOMAN SPY CHIEF", "Awaits hearing · first since 1961", "reported"),
]
X0, Y0 = 24, 386
PW, PH, GAP = 488, 146, 9
for i, (cat, icon, head, sub, kind) in enumerate(PANELS):
    col, row = i % 2, i // 2
    x = X0 + col * (PW + GAP)
    y = Y0 + row * (PH + GAP)
    d.rounded_rectangle([x, y, x + PW, y + PH], radius=14, fill=CARD, outline=LINE, width=2)
    icon(x + 58, y + PH // 2)
    tx = x + 112
    d.text((tx, y + 13), cat, font=font(FB, 17), fill=RED)
    tag(x + PW - 12, y + 11, kind)
    hf = fit_multi(head.split("\n"), FB, 27, PW - 112 - 14)
    d.multiline_text((tx, y + 38), head, font=hf, fill=INK, spacing=3)
    d.text((tx, y + PH - 32), sub, font=fit(sub, FR, 20, PW - 112 - 14, 15), fill=SUB)

# ---- Bottom: ALSO ON MONDAY + DATE CHECK ----
BY = 386 + 3 * 146 + 2 * 9 + 10  # 852
BH = 124
d.rounded_rectangle([24, BY, 668, BY + BH], radius=12, fill=CARD, outline=LINE, width=2)
d.text((40, BY + 9), "ALSO ON MONDAY · 6 MORE STORIES", font=font(FB, 15), fill=RED)
ALSO = [
    ("ASIA", "India pledges $1.62bn for flood-hit Nepal"),
    ("EUROPE", "England: AI screening trial, 700,000 women"),
    ("EUROPE", "Spain court clears Puigdemont's return"),
    ("CENTRAL ASIA", "Tajikistan begins ICC withdrawal"),
    ("AFRICA", "Zambia charges 14 with treason"),
    ("AMERICAS", "Houston jumps to No. 1 in AP Top 25 poll"),
]
for i, (reg, line) in enumerate(ALSO):
    col, row = i % 2, i // 2
    x = 40 + col * 316
    y = BY + 33 + row * 29
    d.text((x, y), reg, font=font(FB, 10), fill=SUB)
    d.text((x, y + 11), line, font=fit(line, FR, 13, 306, 11), fill=INK)

d.rounded_rectangle([680, BY, W - 24, BY + BH], radius=12, fill=(253, 244, 238), outline=RED, width=2)
d.text((694, BY + 9), "DATE CHECK", font=font(FB, 15), fill=RED)
dc = ["Left out as other days' news:",
      "· Peru M6.7 quake (Fri 20)",
      "· Brazil storm (Fri 20)",
      "· Ōnosato's title (Sun 22)"]
for i, line in enumerate(dc):
    d.text((694, BY + 34 + i * 20), line, font=fit(line, FR, 14, W - 24 - 694 - 12, 11), fill=INK)

# ---- Footer ----
d.text((W // 2, 984), "Sources: Reuters, AP, AFP, CNN, Al Jazeera, Yonhap, ESA · Certainty: REPORTED = confirmed by officials or several outlets; CLAIM = one side's assertion", font=fit("Sources: Reuters, AP, AFP, CNN, Al Jazeera, Yonhap, ESA · Certainty: REPORTED = confirmed by officials or several outlets; CLAIM = one side's assertion", FB, 13, W - 48, 10), fill=SUB, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image/entry.png")
print("saved", img.size)
