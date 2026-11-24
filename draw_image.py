#!/usr/bin/env python3
"""Draw the news-image-20261124 entry v5: broadsheet front page, 1024x1024.
36 stories, all happened or first reported Tue 24 Nov 2026 (see
~/workspace/makefun/news-image-20261124-v5-notes.md for the fact list).
Keeps the v4 identity (numbers-led, same 4 main stories) and rebuilds it
as a newspaper front page per the top-entry study: masthead + giant date,
numbers strip, 4 numeral-led lead panels with flat illustrations, UTC
timeline, mid grid, world map with numbered pins, ALSO list, DATE CHECK
footer, epistemic tags + per-story sources on every story.
PIL + DejaVu only; no photos, so no garbled text.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

SERIF = f("DejaVuSerif-Bold.ttf", 46)
MAST = f("DejaVuSans-Bold.ttf", 17)
SUB = f("DejaVuSans-Bold.ttf", 20)
COUNT = f("DejaVuSans-Bold.ttf", 16)
STRIP_N = f("DejaVuSans-Bold.ttf", 23)
STRIP_L = f("DejaVuSans-Bold.ttf", 10)
STRIP_T = f("DejaVuSans-Bold.ttf", 13)
TAG = f("DejaVuSans-Bold.ttf", 13)
TAGSM = f("DejaVuSans-Bold.ttf", 11)
HEAD = f("DejaVuSans-Bold.ttf", 18)
CAP = f("DejaVuSans.ttf", 13)
TL_H = f("DejaVuSans-Bold.ttf", 15)
TL_T = f("DejaVuSans-Bold.ttf", 11)
MID_T = f("DejaVuSans-Bold.ttf", 13)
MID_C = f("DejaVuSans.ttf", 11)
MID_S = f("DejaVuSans.ttf", 10)
ALSO = f("DejaVuSans-Bold.ttf", 10)
LAB = f("DejaVuSans-Bold.ttf", 13)
FOOT = f("DejaVuSans.ttf", 12)
FOOTB = f("DejaVuSans-Bold.ttf", 12)
PIN = f("DejaVuSans-Bold.ttf", 9)
PINSM = f("DejaVuSans-Bold.ttf", 8)

NAVY = (16, 42, 87)
STEEL = (24, 78, 150)
GREEN = (0, 128, 0)
RUST = (178, 58, 32)
TEAL = (0, 128, 128)
AMBER = (166, 110, 0)
SLATE = (70, 85, 105)
PAPER = (240, 244, 248)
GOLD = (255, 193, 7)
GOLDD = (176, 124, 0)
REDL = (255, 130, 120)
MAPFILL = (205, 214, 224)
MAPLINE = (150, 162, 175)
OCEAN = (232, 240, 247)

TAGC = {"CONFIRMED": GREEN, "OFFICIAL": STEEL, "REPORTED": AMBER,
        "CLAIM": RUST}

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
    size = max_size
    while size > 20 and d.textlength(text, font=f("DejaVuSans-Bold.ttf", size)) > max_width:
        size -= 2
    return f("DejaVuSans-Bold.ttf", size)

def draw_segments(x, y, segs, font):
    """Draw [(text, colour), ...] left to right; returns end x."""
    for text, colour in segs:
        d.text((x, y), text, font=font, fill=colour)
        x += d.textlength(text, font=font)
    return x

# ---------------------------------------------------------------- header
d.rectangle([0, 0, W, 108], fill=NAVY)
d.text((32, 10), "THE DAY IN NUMBERS", font=MAST, fill=GOLD)
counts = "36 STORIES  •  7 REGIONS  •  17 FIELDS"
d.text((W - 32 - d.textlength(counts, font=COUNT), 10), counts,
       font=COUNT, fill="white")
d.text((32, 34), "TUESDAY 24 NOVEMBER 2026", font=SERIF, fill="white")
d.text((32, 84), "NVIDIA SOARS  •  MISSILES IN POLAND  •  COP31 NO DEAL",
       font=SUB, fill=REDL)
d.rectangle([0, 108, W, 112], fill=GOLD)

# ---------------------------------------------------------- numbers strip
d.text((32, 122), "BY THE", font=STRIP_T, fill=GOLDD)
d.text((32, 138), "NUMBERS", font=STRIP_T, fill=GOLDD)
strip = [
    ("292", "FLIGHTS DELAYED", STEEL),
    ("+6.5%", "NASDAQ", GREEN),
    ("1,448", "DOW POINTS", RUST),
    ("12,000", "MANCHESTER", STEEL),
    ("133", "ILLINOIS PTS", GREEN),
    ("7,000", "LANDMINE CASUALTIES", RUST),
]
sx = 150
for num, lab, col in strip:
    d.text((sx, 120), num, font=STRIP_N, fill=col)
    d.text((sx, 148), lab, font=STRIP_L, fill=SLATE)
    sx += 142
d.rectangle([0, 160, W, 163], fill=GOLD)

# ------------------------------------------------------------- lead panels
def illustration(kind, x, y, col):
    """Small flat scene, 64x64 box at (x, y)."""
    if kind == "radar":
        for r in (28, 20, 12):
            d.ellipse([x + 32 - r, y + 32 - r, x + 32 + r, y + 32 + r],
                      outline=col, width=3)
        d.ellipse([x + 44, y + 18, x + 52, y + 26], fill=RUST)
        d.line([x + 32, y + 32, x + 50, y + 12], fill=col, width=3)
        d.ellipse([x + 28, y + 28, x + 36, y + 36], fill=col)
    elif kind == "chip":
        d.rounded_rectangle([x + 12, y + 12, x + 52, y + 52], radius=6,
                            fill=col)
        d.rectangle([x + 24, y + 24, x + 40, y + 40], fill="white")
        for i in range(3):
            yy = y + 18 + i * 14
            d.line([x + 4, yy, x + 12, yy], fill=col, width=3)
            d.line([x + 52, yy, x + 60, yy], fill=col, width=3)
            xx = x + 18 + i * 14
            d.line([xx, y + 4, xx, y + 12], fill=col, width=3)
            d.line([xx, y + 52, xx, y + 60], fill=col, width=3)
    elif kind == "bank":
        d.polygon([(x + 32, y + 6), (x + 6, y + 22), (x + 58, y + 22)],
                  fill=col)
        for i, xx in enumerate((x + 12, x + 28, x + 44)):
            d.rectangle([xx, y + 26, xx + 8, y + 52], fill=col)
        d.rectangle([x + 6, y + 54, x + 58, y + 60], fill=col)
    elif kind == "globe":
        d.ellipse([x + 8, y + 8, x + 56, y + 56], fill=col)
        d.arc([x + 8, y + 8, x + 56, y + 56], 200, 340, fill="white",
              width=3)
        d.arc([x + 16, y + 14, x + 48, y + 50], 200, 340, fill="white",
              width=2)
        d.line([x + 8, y + 32, x + 56, y + 32], fill="white", width=2)
        d.ellipse([x + 40, y + 40, x + 54, y + 54], fill=GREEN)
        d.line([x + 47, y + 40, x + 47, y + 30], fill=GREEN, width=3)

def panel(x, y, w, h, colour, num, tag, tagline, source, headline, caption,
          kind):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=PAPER,
                        outline=colour, width=3)
    d.rounded_rectangle([x, y, x + w, y + 28], radius=12, fill=colour)
    d.rectangle([x, y + 14, x + w, y + 28], fill=colour)
    d.text((x + 12, y + 6), tagline, font=TAG, fill="white")
    right = f"{tag} · {source}"
    d.text((x + w - 12 - d.textlength(right, font=TAGSM), y + 7), right,
           font=TAGSM, fill="white")
    # Giant numeral, left column.
    nfont = num_font(num, 92, 150)
    bbox = d.textbbox((0, 0), num, font=nfont)
    n_top = y + 28 + (h - 28 - (bbox[3] - bbox[1])) // 2 - bbox[1]
    d.text((x + 14, n_top), num, font=nfont, fill=colour)
    # Headline + caption, middle column.
    tx, tw = x + 172, w - 172 - 84
    hlines = wrap(headline, HEAD, tw)[:2]
    clines = wrap(caption, CAP, tw)[:3]
    block_h = len(hlines) * 22 + 4 + len(clines) * 16
    yy = y + 28 + max(0, (h - 28 - block_h) // 2)
    for line in hlines:
        d.text((tx, yy), line, font=HEAD, fill=(20, 20, 20))
        yy += 22
    yy += 4
    for line in clines:
        d.text((tx, yy), line, font=CAP, fill=SLATE)
        yy += 16
    illustration(kind, x + w - 76, y + 28 + (h - 28 - 64) // 2, colour)
    print(tagline, "headline:", len(hlines), "caption:", len(clines))

PW, PH = 478, 138
panel(24, 168, PW, PH, STEEL, "3", "REPORTED", "1 · SECURITY • EUROPE",
      "REUTERS", "THREE RUSSIAN MISSILES LAND IN POLAND",
      "Missiles fell Fri 20 Nov; NATO will send an AWACS jet.", "radar")
panel(522, 168, PW, PH, GREEN, "31%", "CONFIRMED", "2 · TECH • USA",
      "REUTERS", "NVIDIA SOARS AS HUANG RETURNS",
      "Board reinstates Huang, 11 days after he quit; shares add ~$950bn.",
      "chip")
panel(24, 314, PW, PH, RUST, "60", "OFFICIAL", "3 · SANCTIONS • EUROPE",
      "EU", "EU'S 22ND RUSSIA SANCTIONS PACKAGE",
      "About 60 banks face a SWIFT cut-off; 70+ ships listed.", "bank")
panel(522, 314, PW, PH, TEAL, "2009", "CONFIRMED", "4 · CLIMATE • TURKEY",
      "REUTERS", "COP31 ENDS WITH NO DEAL",
      "First summit since Copenhagen 2009 to end with no deal.", "globe")

# ------------------------------------------------------------ UTC timeline
d.text((32, 464), "THE DAY IN UTC", font=LAB, fill=NAVY)
timeline = [
    ("03:00", "Quake M4.1 hits Pakistan"),
    ("06:00", "Nikkei closes +3.9%"),
    ("12:00", "Iran currency plunges on sanctions"),
    ("13:00", "Zaporizhzhia strike: 2 killed, 40 hurt"),
    ("17:00", "FAA ground stop at O'Hare begins"),
]
tx = 32
for hour, ev in timeline:
    d.text((tx, 484), hour, font=TL_H, fill=RUST)
    for i, line in enumerate(wrap(ev, TL_T, 156)[:2]):
        d.text((tx, 502 + i * 13), line, font=TL_T, fill=SLATE)
    tx += 195

# -------------------------------------------------------------- mid stories
d.text((32, 534), "MORE FROM THE DAY", font=LAB, fill=NAVY)
mids = [
    ("5. US SANCTIONS IRAN SHADOW BANKS",
     "Treasury sanctions dozens of people and firms.", "OFFICIAL",
     "US TREASURY"),
    ("6. BRITAIN WARNS OF SABOTAGE",
     "MI5 warns Ukraine suppliers of Russian sabotage.", "OFFICIAL",
     "REUTERS"),
    ("7. MARKETS RALLY ON NVIDIA NEWS",
     "Nasdaq +6.5%, S&P +4.7%, Dow +1,448.", "CONFIRMED", "ZACKS"),
    ("8. GAZA STRIKES KILL HAMAS CHIEF",
     "Naeem Abu Nahel and six others killed, medics say.", "REPORTED",
     "AP"),
    ("9. ZAPORIZHZHIA FLATS HIT",
     "Overnight strike kills 2, wounds 40, incl. 4 children.", "REPORTED",
     "AP"),
    ("10. NATO VOWS SPACE DEFENCE",
     "Rutte answers reports of a Russian nuclear satellite.", "REPORTED",
     "BBC"),
    ("11. RUSSIAN JETS ENTER S. KOREA ADIZ",
     "Several jets flew over waters between Korea and Japan.", "OFFICIAL",
     "JOINT CHIEFS"),
    ("12. GERMANY GETS DELTA ACCESS",
     "First access to Kyiv's Delta system.", "OFFICIAL",
     "KYIV INDEPENDENT"),
    ("13. INDONESIA FACTORY FIRE: 26 DEAD",
     "Toll rises to 26; fire broke out on Saturday.", "REPORTED", "AP"),
    ("14. IRAQ TAKES KURDISH OILFIELDS",
     "PM orders ministry to run fields in four provinces.", "OFFICIAL",
     "REUTERS"),
    ("15. O'HARE GROUND STOP",
     "FAA halts arrivals; 292 flights delayed.", "OFFICIAL", "FAA"),
    ("16. MANCHESTER CONCERT EVACUATED",
     "12,000 leave over a gas alert.", "REPORTED", "NEWSREEL"),
]
for i, (title, cap, tag, src) in enumerate(mids):
    cx = 24 + (i % 3) * 329
    cy = 556 + (i // 3) * 45
    d.text((cx, cy), title, font=MID_T, fill=(20, 20, 20))
    d.text((cx, cy + 17), cap, font=MID_C, fill=SLATE)
    draw_segments(cx, cy + 31, [(tag, TAGC[tag]), (" · " + src, SLATE)],
                  MID_S)
    print("mid", title[:20], "title w:",
          round(d.textlength(title, font=MID_T)), "cap w:",
          round(d.textlength(cap, font=MID_C)))

# ------------------------------------------------------- map + ALSO TODAY
d.text((32, 738), "WHERE IT HAPPENED — PINS = STORY NUMBERS", font=LAB,
       fill=NAVY)
d.text((530, 738), "ALSO TODAY", font=LAB, fill=NAVY)
d.rectangle([24, 760, 506, 918], fill=OCEAN)

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 64)],
    # South America
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-45, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-73, -53), (-70, -20), (-80, -5), (-80, 5)],
    # Africa
    [(-10, 35), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (48, 11), (40, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, 4), (-8, 4), (-15, 12),
     (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 52),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (110, 20), (108, 12), (105, 9), (100, 8),
     (97, 16), (92, 21), (88, 22), (80, 13), (77, 8), (73, 16),
     (66, 25), (60, 25), (57, 26), (52, 26), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (27, 37), (23, 36), (19, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Australia
    [(114, -22), (114, -30), (116, -35), (124, -33), (130, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -23), (146, -19), (142, -11), (137, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
     (142, 44), (140, 42)],
    # Indonesia islands
    [(95, 5), (100, 0), (104, -3), (106, -6), (104, -6), (99, -1)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3),
     (109, 0)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -7), (136, -4), (131, -2)],
]

def mx(lon):
    return 24 + (lon + 170) / 360 * 482

def my(lat):
    return 760 + (75 - lat) / 130 * 158

for poly in CONTINENTS:
    pts = [(mx(lon), my(lat)) for lon, lat in poly]
    d.polygon(pts, fill=MAPFILL, outline=MAPLINE)

PINS = [
    ("1", 19, 52), ("2", -122, 37), ("5·7", -76, 40), ("3·12", 8, 51),
    ("4·8", 32, 34), ("9", 35, 48), ("11", 127, 37),
    ("13", 106, -6), ("14·22", 47, 34), ("15", -88, 42), ("6·16", -5, 53),
    ("21", 116, 40), ("27", 96, 20), ("32", 145, -38), ("33", 30, 2),
    ("34", 43, 15), ("36", -73, 4),
]
for label, lon, lat in PINS:
    x, y = mx(lon), my(lat)
    r = 8 if "·" in label else 6
    font = PINSM if "·" in label else PIN
    d.ellipse([x - r, y - r, x + r, y + r], fill=RUST, outline="white",
              width=1)
    tw = d.textlength(label, font=font)
    th = font.getbbox(label)[3]
    d.text((x - tw / 2, y - th / 2 - 1), label, font=font, fill="white")

also = [
    (17, "S. KOREA MINISTER RESIGNS", "AP", "OFFICIAL"),
    (18, "$375K AI-CHEAT BOUNTY", "SEOUL", "OFFICIAL"),
    (19, "UN: AI RULES IN A YEAR", "UN", "OFFICIAL"),
    (20, "EU-INDONESIA TRADE DEAL", "EU", "OFFICIAL"),
    (21, "CHINA DEATH SENTENCE", "AP", "REPORTED"),
    (22, "SINGER GETS 74 LASHES", "AP", "REPORTED"),
    (23, "COMMANDERS 22, BENGALS 20", "AP", "CONFIRMED"),
    (24, "BUCKS END 13-GAME SKID", "AP", "CONFIRMED"),
    (25, "BLAZERS SNAP 76ERS STREAK", "AP", "CONFIRMED"),
    (26, "ILLINOIS 133, BIG TEN MARK", "AP", "CONFIRMED"),
    (27, "UK SANCTIONS MYANMAR", "UK", "OFFICIAL"),
    (28, "ARMENIA CONSTITUTION", "SCMP", "REPORTED"),
    (29, "ZEESHAN ALI TO FLY", "ONETURN", "REPORTED"),
    (30, "LANDMINE TOLL HITS 7,000", "SCMP", "REPORTED"),
    (31, "US STATES SUE MUSK FIRMS", "SCMP", "REPORTED"),
    (32, "CANBERRA DUTY OF CARE", "AL JAZEERA", "OFFICIAL"),
    (33, "CONGO EBOLA TEAMS TRAPPED", "UN", "REPORTED"),
    (34, "HOUTHIS CLAIM 17 KILLED", "IQMIA", "CLAIM"),
    (35, "ARM CEO HAAS TO 2033", "IQMIA", "REPORTED"),
    (36, "COLOMBIA CAR BOMB", "ONETURN", "REPORTED"),
]
for i, (n, title, src, tag) in enumerate(also):
    ax = 530 + (i % 2) * 238
    ay = 762 + (i // 2) * 15
    num = f"{n}."
    d.text((ax, ay), num, font=ALSO, fill=TAGC[tag])
    d.text((ax + 24, ay), f"{title} ({src})", font=ALSO, fill=(20, 20, 20))
    print("also", n, "w:",
          round(24 + d.textlength(f"{title} ({src})", font=ALSO)))

# ------------------------------------------------------------------ footer
d.rectangle([0, 926, W, 930], fill=GOLD)
draw_segments(32, 938, [
    ("TAGS:  ", (20, 20, 20)),
    ("CONFIRMED", GREEN), (" 2+ outlets   ", SLATE),
    ("OFFICIAL", STEEL), (" on record   ", SLATE),
    ("REPORTED", AMBER), (" one outlet   ", SLATE),
    ("CLAIM", RUST), (" one side's word", SLATE),
], FOOTB)
dc = ("DATE CHECK — Every story happened, or was first reported, on Tuesday "
      "24 November 2026 (UTC). Left out: COP31 collapsed Sun 22 Nov · missiles "
      "fell Fri 20 Nov · corvette claim Sun 22 Nov · BepiColombo orbit Sat "
      "21 Nov · Boca win Sun 23 Nov · Indonesia fire Sat 21 Nov · Meldrum "
      "died Mon 23 Nov.")
yy = 958
for line in wrap(dc, FOOT, 960):
    d.text((32, yy), line, font=FOOT, fill=SLATE)
    yy += 15
foot = "THE DAY IN NUMBERS  •  36 STORIES  •  COMPILED 24 NOVEMBER 2026"
d.text(((W - d.textlength(foot, font=FOOTB)) / 2, 996), foot,
       font=FOOTB, fill=NAVY)

img.save("/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png",
         optimize=True)
import os
path = "/home/hatch/workspace/makefun/news-image-20261124-entry/entry.png"
print("saved", img.size, "bytes", os.path.getsize(path))
