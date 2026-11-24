#!/usr/bin/env python3
"""Draw the news-image-20261124 entry v3: a newspaper front page, 1024x1024.
14 stories, all reported 23-24 Nov 2026 (see notes.md + parent brief).
Main panels carry the day's biggest security/sanctions stories and hard
numbers; the MORE TODAY strip carries 10 short items. PIL + DejaVu only;
no photos, so no garbled text.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

TITLE = f("DejaVuSerif-Bold.ttf", 50)
SUB = f("DejaVuSans.ttf", 26)
TAG = f("DejaVuSans-Bold.ttf", 21)
HEAD = f("DejaVuSans-Bold.ttf", 28)
CAP = f("DejaVuSans.ttf", 20)
MORE_T = f("DejaVuSans-Bold.ttf", 20)
MORE = f("DejaVuSans.ttf", 18)

NAVY = (16, 42, 87)
STEEL = (24, 78, 150)
GREEN = (0, 128, 0)
TEAL = (0, 128, 128)
RUST = (178, 58, 32)
SLATE = (70, 85, 105)
PAPER = (240, 244, 248)

d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((32, 22), "TUESDAY 24 NOVEMBER 2026", font=TITLE, fill="white")
d.text((32, 90), "THE WORLD IN ONE DAY  •  FOURTEEN STORIES THAT DEFINED THE DAY",
       font=SUB, fill=(205, 222, 242))
d.rectangle([0, 148, W, 156], fill=(255, 193, 7))

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def panel(x, y, w, h, colour, tag, headline, caption, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=PAPER,
                        outline=colour, width=4)
    d.rounded_rectangle([x, y, x + w, y + 42], radius=16, fill=colour)
    d.rectangle([x, y + 24, x + w, y + 42], fill=colour)
    d.text((x + 16, y + 8), tag, font=TAG, fill="white")
    icon(x + w - 106, y + 62)
    yy = y + 56
    for line in wrap(headline, HEAD, w - 150):
        d.text((x + 16, yy), line, font=HEAD, fill=(20, 20, 20))
        yy += 34
    yy += 28  # captions start below the icons, so no text runs under them
    for line in wrap(caption, CAP, w - 32):
        d.text((x + 16, yy), line, font=CAP, fill=SLATE)
        yy += 26

def icon_jet(x, y):
    # Top-view jet: wide fuselage, long swept wings, tail fins.
    # Drawn bigger and simpler after viewing v3: the thin fuselage
    # read as an arrow at small sizes.
    d.polygon([(x + 42, y), (x + 50, y + 16), (x + 50, y + 60),
               (x + 46, y + 84), (x + 38, y + 84), (x + 34, y + 60),
               (x + 34, y + 16)], fill=STEEL)
    d.polygon([(x + 42, y + 24), (x + 88, y + 50), (x + 88, y + 60),
               (x + 42, y + 46)], fill=STEEL)
    d.polygon([(x + 42, y + 24), (x - 4, y + 50), (x - 4, y + 60),
               (x + 42, y + 46)], fill=STEEL)
    d.polygon([(x + 42, y + 58), (x + 66, y + 78), (x + 66, y + 84),
               (x + 42, y + 72)], fill=STEEL)
    d.polygon([(x + 42, y + 58), (x + 18, y + 78), (x + 18, y + 84),
               (x + 42, y + 72)], fill=STEEL)
    d.ellipse([x + 37, y + 8, x + 47, y + 22], fill="white")

def icon_chip(x, y):
    d.rounded_rectangle([x, y, x + 84, y + 84], radius=12, fill=GREEN)
    d.rectangle([x + 28, y + 28, x + 56, y + 56], fill="white")
    for i in range(3):
        d.rectangle([x + 12 + i * 26, y - 8, x + 20 + i * 26, y + 4], fill=GREEN)
        d.rectangle([x + 12 + i * 26, y + 80, x + 20 + i * 26, y + 92], fill=GREEN)
        d.rectangle([x - 8, y + 12 + i * 26, x + 4, y + 20 + i * 26], fill=GREEN)
        d.rectangle([x + 80, y + 12 + i * 26, x + 92, y + 20 + i * 26], fill=GREEN)

def icon_bank(x, y):
    # Bank building: pediment roof, three columns, steps.
    d.polygon([(x + 42, y), (x + 84, y + 26), (x, y + 26)], fill=RUST)
    d.rectangle([x + 4, y + 30, x + 80, y + 36], fill=RUST)
    for i in range(3):
        d.rectangle([x + 12 + i * 26, y + 40, x + 22 + i * 26, y + 66], fill=RUST)
    d.rectangle([x + 4, y + 68, x + 80, y + 74], fill=RUST)
    d.rectangle([x, y + 76, x + 84, y + 84], fill=RUST)

def icon_globe(x, y):
    d.ellipse([x, y, x + 84, y + 84], fill=TEAL)
    d.ellipse([x + 12, y + 12, x + 72, y + 72], outline="white", width=3)
    d.line([x + 42, y + 6, x + 42, y + 78], fill="white", width=3)
    d.line([x + 6, y + 42, x + 78, y + 42], fill="white", width=3)
    d.ellipse([x + 26, y + 20, x + 58, y + 64], outline="white", width=3)
    d.ellipse([x + 22, y + 22, x + 40, y + 40], fill="white")
    d.ellipse([x + 48, y + 50, x + 64, y + 66], fill="white")

PW, PH = 478, 236
panel(24, 176, PW, PH, STEEL, "SECURITY  •  EUROPE",
      "NATO SENDS AWACS TO POLAND",
      "Three Russian Kh-101 missiles came down in Poland on Friday; "
      "NATO will forward-deploy an early-warning jet.", icon_jet)
panel(522, 176, PW, PH, GREEN, "TECH  •  USA",
      "NVIDIA SOARS +31% AS HUANG RETURNS",
      "Board unanimously reinstates Huang 11 days after he quit; shares "
      "add about $950bn in value. Nasdaq jumps 6.5%.", icon_chip)
panel(24, 428, PW, PH, RUST, "SANCTIONS  •  USA / IRAN",
      "US HITS IRAN'S SHADOW BANKS",
      "Treasury sanctions dozens of people and firms in Iran's "
      "shadow-banking networks.", icon_bank)
panel(522, 428, PW, PH, TEAL, "CLIMATE  •  TURKEY",
      "COP31 ENDS WITH NO DEAL",
      "First climate summit since Copenhagen 2009 to end with no deal; "
      "EU rejected a text with no mention of fossil fuels.", icon_globe)

d.rectangle([24, 680, W - 24, 1000], fill=NAVY)
d.text((44, 692), "MORE TODAY", font=MORE_T, fill=(255, 193, 7))
more = [
    ("LIBYA — Ukraine says its drones sank a Russian corvette; Zelenskyy warns of new Russian strikes.",
     "SOUTH KOREA — Education minister resigns over AI cheating rules."),
    ("EU — 22nd Russia sanctions package proposed: about 60 banks off SWIFT, 70+ shadow-fleet ships.",
     "UN — Chief calls for a global AI safety framework within a year."),
    ("USA — O'Hare ground stop over staffing shortage in Thanksgiving rush.",
     "EU — Indonesia trade deal signed, from palm oil to medicines."),
    ("IRAN — Singer and four of her team each sentenced to 74 lashes.",
     "CHINA — Official sentenced to death for leaking state secrets."),
    ("UK — Manchester concert evacuated; 12,000 leave over a gas alert.",
     "SPACE — BepiColombo reaches Mercury orbit after eight years; thruster glitch reported."),
]
yy = 724
for left, right in more:
    for i, line in enumerate(wrap("•  " + left, MORE, 460)[:2]):
        d.text((44, yy + i * 24), line, font=MORE, fill="white")
    for i, line in enumerate(wrap("•  " + right, MORE, 460)[:2]):
        d.text((532, yy + i * 24), line, font=MORE, fill="white")
    yy += 52

img.save("/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png",
         optimize=True)
import os
path = "/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png"
print("saved", img.size, "bytes", os.path.getsize(path))
