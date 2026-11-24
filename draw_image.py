#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a newspaper front page, 1024x1024.
Stories are the ones researched in notes.md, reported 24 Nov 2026.
Built with PIL + DejaVu only; no photos, so no garbled text.
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
GREEN = (0, 128, 0)
TEAL = (0, 128, 128)
RUST = (178, 58, 32)
GOLD = (176, 128, 8)
SLATE = (70, 85, 105)
PAPER = (240, 244, 248)

d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((32, 22), "TUESDAY 24 NOVEMBER 2026", font=TITLE, fill="white")
d.text((32, 90), "THE WORLD IN ONE DAY  •  TEN STORIES THAT DEFINED THE DAY",
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

def icon_chip(x, y):
    d.rounded_rectangle([x, y, x + 84, y + 84], radius=12, fill=GREEN)
    d.rectangle([x + 28, y + 28, x + 56, y + 56], fill="white")
    for i in range(3):
        d.rectangle([x + 12 + i * 26, y - 8, x + 20 + i * 26, y + 4], fill=GREEN)
        d.rectangle([x + 12 + i * 26, y + 80, x + 20 + i * 26, y + 92], fill=GREEN)
        d.rectangle([x - 8, y + 12 + i * 26, x + 4, y + 20 + i * 26], fill=GREEN)
        d.rectangle([x + 80, y + 12 + i * 26, x + 92, y + 20 + i * 26], fill=GREEN)

def icon_globe(x, y):
    d.ellipse([x, y, x + 84, y + 84], fill=TEAL)
    d.ellipse([x + 12, y + 12, x + 72, y + 72], outline="white", width=3)
    d.line([x + 42, y + 6, x + 42, y + 78], fill="white", width=3)
    d.line([x + 6, y + 42, x + 78, y + 42], fill="white", width=3)
    d.ellipse([x + 26, y + 20, x + 58, y + 64], outline="white", width=3)
    d.ellipse([x + 30, y + 24, x + 44, y + 38], fill="white")

def icon_ship(x, y):
    # Warship: grey hull, mast and bridge block, not a sailboat.
    d.rectangle([x + 38, y + 2, x + 46, y + 40], fill=NAVY)
    d.rectangle([x + 28, y + 18, x + 56, y + 40], fill=RUST)
    d.rectangle([x + 12, y + 40, x + 72, y + 52], fill=SLATE)
    d.polygon([(x, y + 52), (x + 84, y + 52), (x + 70, y + 76), (x + 14, y + 76)],
              fill=NAVY)
    d.rectangle([x + 22, y + 58, x + 62, y + 66], fill="white")
    d.ellipse([x + 46, y + 6, x + 54, y + 14], fill=RUST)

def icon_plane(x, y):
    # Side view: long fuselage, tail fin, swept wing.
    d.polygon([(x + 4, y + 40), (x + 72, y + 28), (x + 84, y + 34),
               (x + 76, y + 44), (x + 20, y + 54)], fill=GOLD)
    d.polygon([(x + 10, y + 16), (x + 22, y + 16), (x + 32, y + 40),
               (x + 18, y + 40)], fill=GOLD)
    d.polygon([(x + 36, y + 48), (x + 54, y + 48), (x + 48, y + 72),
               (x + 36, y + 72)], fill=GOLD)
    d.ellipse([x + 62, y + 30, x + 70, y + 38], fill="white")

PW, PH = 478, 296
panel(24, 176, PW, PH, GREEN, "TECH  •  USA",
      "NVIDIA BRINGS BACK HUANG",
      "Jensen Huang reinstated as chief executive; shares jump sharply. "
      "Senate hearing set for 3 December.", icon_chip)
panel(522, 176, PW, PH, TEAL, "CLIMATE  •  TURKEY",
      "COP31 TALKS COLLAPSE",
      "UN climate summit ends without a deal on moving away from fossil fuels.",
      icon_globe)
panel(24, 488, PW, PH, RUST, "SECURITY  •  LIBYA",
      "RUSSIAN WARSHIP HIT AT BENGHAZI",
      "Navy corvette reported destroyed after fire in port; drone attack suspected.",
      icon_ship)
panel(522, 488, PW, PH, GOLD, "TRAVEL  •  USA",
      "O'HARE GROUND STOP",
      "Chicago airport halts departures briefly over staffing shortage in the "
      "Thanksgiving travel rush.", icon_plane)

d.rectangle([24, 800, W - 24, 1000], fill=NAVY)
d.text((44, 812), "MORE TODAY", font=MORE_T, fill=(255, 193, 7))
more = [
    ("UK — Manchester concert evacuated; 12,000 leave over a gas alert.",
     "IRAN — Singer sentenced to 74 lashes for performing without a hijab."),
    ("SOUTH KOREA — Education minister resigns over AI cheating rules.",
     "UN — Chief calls for a global AI safety framework within a year."),
    ("CHINA — Official sentenced to death for leaking state secrets.",
     "EU — Indonesia trade deal signed, from palm oil to medicines."),
]
yy = 846
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
