#!/usr/bin/env python3
"""Draw the news-image-20261124 entry v4: "THE DAY IN NUMBERS", 1024x1024.
14 stories, all reported 23-24 Nov 2026 (see notes.md + parent brief).
Signature: every main panel is led by one GIANT numeral in its accent
colour -- 3, 31%, 60, 2009 -- so the page reads at 300px and looks
nothing like the rivals' dense text newspapers or map-led entries.
No drawn icons in the panels; the numbers ARE the visual. A thin gold
rule under the navy header and above the footer is the page's accent.
PIL + DejaVu only; no photos, so no garbled text.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

TITLE = f("DejaVuSerif-Bold.ttf", 50)
SUB = f("DejaVuSans.ttf", 24)
TAG = f("DejaVuSans-Bold.ttf", 20)
HEAD = f("DejaVuSans-Bold.ttf", 24)
CAP = f("DejaVuSans.ttf", 18)
MORE_T = f("DejaVuSans-Bold.ttf", 20)
MORE = f("DejaVuSans.ttf", 18)
FOOT = f("DejaVuSans.ttf", 16)

NAVY = (16, 42, 87)
STEEL = (24, 78, 150)
GREEN = (0, 128, 0)
TEAL = (0, 128, 128)
RUST = (178, 58, 32)
SLATE = (70, 85, 105)
PAPER = (240, 244, 248)
GOLD = (255, 193, 7)

# --- header: navy band, date unmistakable, gold rule signature ---
d.rectangle([0, 0, W, 128], fill=NAVY)
d.text((32, 16), "TUESDAY 24 NOVEMBER 2026", font=TITLE, fill="white")
d.text((32, 84), "THE DAY IN NUMBERS  •  FOURTEEN STORIES THAT DEFINED THE DAY",
       font=SUB, fill=(205, 222, 242))
d.rectangle([0, 128, W, 136], fill=GOLD)

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

def num_font(text, max_size, max_width):
    """Biggest bold size (up to max_size) whose width fits max_width."""
    size = max_size
    while size > 20 and d.textlength(text, font=f("DejaVuSans-Bold.ttf", size)) > max_width:
        size -= 2
    return f("DejaVuSans-Bold.ttf", size)

def panel(x, y, w, h, colour, tag, number, num_size, headline, caption):
    d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=PAPER,
                        outline=colour, width=4)
    d.rounded_rectangle([x, y, x + w, y + 40], radius=16, fill=colour)
    d.rectangle([x, y + 22, x + w, y + 40], fill=colour)
    d.text((x + 16, y + 8), tag, font=TAG, fill="white")

    # Giant number, left column, vertically centred in the content area.
    y0 = y + 48
    content_h = h - 48 - 8
    nfont = num_font(number, num_size, 176)
    bbox = d.textbbox((0, 0), number, font=nfont)
    n_top = y0 + (content_h - (bbox[3] - bbox[1])) // 2 - bbox[1]
    d.text((x + 16, n_top), number, font=nfont, fill=colour)

    # Headline + caption, right column, block vertically centred.
    tx, tw = x + 200, w - 200 - 16
    hlines = wrap(headline, HEAD, tw)
    clines = wrap(caption, CAP, tw)
    block_h = len(hlines) * 30 + 6 + len(clines) * 23
    yy = y0 + max(0, (content_h - block_h) // 2)
    for line in hlines:
        d.text((tx, yy), line, font=HEAD, fill=(20, 20, 20))
        yy += 30
    yy += 6
    for line in clines:
        d.text((tx, yy), line, font=CAP, fill=SLATE)
        yy += 23
    print(tag, "headline lines:", len(hlines), "caption lines:", len(clines))

PW, PH = 478, 248
panel(24, 152, PW, PH, STEEL, "SECURITY  •  EUROPE", "3", 170,
      "THREE RUSSIAN MISSILES LAND IN POLAND",
      "Three Kh-101 missiles came down in Poland on Friday; NATO will "
      "send an AWACS jet.")
panel(522, 152, PW, PH, GREEN, "TECH  •  USA", "31%", 110,
      "NVIDIA SOARS AS HUANG RETURNS",
      "Board reinstates Huang unanimously, 11 days after he quit; shares "
      "add about $950bn; Nasdaq up 6.5%.")
panel(24, 412, PW, PH, RUST, "SANCTIONS  •  EUROPE", "60", 140,
      "EU'S 22ND RUSSIA SANCTIONS PACKAGE",
      "About 60 banks face a SWIFT cut-off, 70+ shadow-fleet ships listed, "
      "crypto platforms targeted.")
panel(522, 412, PW, PH, TEAL, "CLIMATE  •  TURKEY", "2009", 90,
      "COP31 ENDS WITH NO DEAL",
      "First summit since Copenhagen 2009 to end with no deal; EU rejected "
      "a text silent on fossil fuels.")

# --- MORE TODAY strip ---
d.rectangle([24, 676, W - 24, 978], fill=NAVY)
d.text((44, 688), "MORE TODAY", font=MORE_T, fill=GOLD)
more = [
    ("USA — Treasury sanctions dozens of people and firms in Iran's shadow-banking networks.",
     "SOUTH KOREA — Education minister resigns over AI cheating rules."),
    ("LIBYA — Ukraine says its drones sank a Russian corvette; Zelenskyy warns of new Russian strikes.",
     "UN — Chief calls for a global AI safety framework within a year."),
    ("USA — O'Hare ground stop over staffing shortage in Thanksgiving rush.",
     "EU — Indonesia trade deal signed, from palm oil to medicines."),
    ("IRAN — Singer and four of her team each sentenced to 74 lashes.",
     "CHINA — Official sentenced to death for leaking state secrets."),
    ("UK — Manchester concert evacuated; 12,000 leave over a gas alert.",
     "SPACE — BepiColombo reaches Mercury orbit after eight years; thruster glitch reported."),
]
yy = 722
for left, right in more:
    for i, line in enumerate(wrap("•  " + left, MORE, 460)[:2]):
        d.text((44, yy + i * 24), line, font=MORE, fill="white")
    for i, line in enumerate(wrap("•  " + right, MORE, 460)[:2]):
        d.text((532, yy + i * 24), line, font=MORE, fill="white")
    yy += 50

# --- footer: gold rule + centred line ---
d.rectangle([0, 984, W, 988], fill=GOLD)
foot = "THE DAY IN NUMBERS  •  COMPILED 24 NOVEMBER 2026"
d.text(((W - d.textlength(foot, font=FOOT)) / 2, 994), foot,
       font=FOOT, fill=SLATE)

img.save("/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png",
         optimize=True)
import os
path = "/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png"
print("saved", img.size, "bytes", os.path.getsize(path))
