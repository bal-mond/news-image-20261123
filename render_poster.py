#!/usr/bin/env python3
"""Render the 23 November 2026 world-news poster (1024x1024) with Pillow.

Newspaper layout, all artwork drawn here with PIL primitives: no photos,
no downloaded images, no network. Stories were verified against web
search results dated Monday 23 November 2026 before being written in.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # warm paper
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (18, 32, 62)
GREY = (110, 108, 100)
LINE = (200, 192, 175)
WHITE = (255, 255, 255)
ACCENT = {
    "war": (140, 30, 30), "climate": (31, 110, 72), "market": (24, 74, 130),
    "tech": (90, 50, 130), "space": (40, 60, 120), "sport": (176, 96, 0),
    "culture": (150, 60, 110), "health": (20, 120, 110), "us": (24, 74, 130),
    "world": (90, 90, 90),
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 54)
F_DATE = font(SANS_B, 20)
F_META = font(SANS_B, 14)
F_KICK = font(SANS_B, 11)
F_HEAD = font(SANS_B, 14)
F_BODY = font(SANS, 11)
F_TOP_HEAD = font(SANS_B, 21)
F_TOP_BODY = font(SANS, 12)
F_SRC = font(SANS, 10)
F_TICK = font(SANS_B, 13)
F_FOOT = font(SANS, 11)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, f, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def glyph(draw, kind, x, y, s, color):
    """Draw a tiny white pictogram inside an s x s box at (x, y)."""
    if kind == "globe":  # circle + meridians
        draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=2)
        draw.ellipse([x + s // 2 - 3, y + 2, x + s // 2 + 3, y + s - 2], outline=color, width=1)
        draw.line([x + 2, y + s // 2, x + s - 2, y + s // 2], fill=color, width=1)
    elif kind == "flame":  # simple flame / explosion
        draw.polygon([(x + s // 2, y + 1), (x + s - 2, y + s - 6),
                      (x + s // 2 + 2, y + s - 2), (x + 2, y + s - 6)], fill=color)
    elif kind == "ship":
        draw.polygon([(x + 2, y + s - 6), (x + s - 2, y + s - 6),
                      (x + s - 5, y + s - 1), (x + 5, y + s - 1)], fill=color)
        draw.line([x + s // 2, y + 2, x + s // 2, y + s - 7], fill=color, width=2)
        draw.polygon([(x + s // 2, y + 2), (x + s - 4, y + s - 7), (x + s // 2, y + s - 7)], fill=color)
    elif kind == "chart":  # rising bars
        draw.rectangle([x + 2, y + s - 6, x + 5, y + s - 2], fill=color)
        draw.rectangle([x + 7, y + s - 10, x + 10, y + s - 2], fill=color)
        draw.rectangle([x + 12, y + s - 14, x + 15, y + s - 2], fill=color)
    elif kind == "chip":
        draw.rectangle([x + 4, y + 4, x + s - 4, y + s - 4], outline=color, width=2)
        for px in (x + 6, x + s // 2, x + s - 7):
            draw.line([px, y + 1, px, y + 4], fill=color, width=1)
            draw.line([px, y + s - 4, px, y + s - 1], fill=color, width=1)
    elif kind == "rocket":
        draw.polygon([(x + s // 2, y + 1), (x + s - 3, y + s - 8),
                      (x + s // 2, y + s - 5), (x + 3, y + s - 8)], fill=color)
        draw.polygon([(x + s // 2 - 2, y + s - 5), (x + s // 2 + 2, y + s - 5),
                      (x + s // 2, y + s - 1)], fill=color)
    elif kind == "ball":
        draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=2)
        draw.polygon([(x + s // 2, y + s // 2 - 3), (x + s // 2 + 3, y + s // 2 + 1),
                      (x + s // 2 - 3, y + s // 2 + 1)], fill=color)
    elif kind == "cross":  # health
        draw.rectangle([x + s // 2 - 2, y + 2, x + s // 2 + 2, y + s - 2], fill=color)
        draw.rectangle([x + 2, y + s // 2 - 2, x + s - 2, y + s // 2 + 2], fill=color)
    elif kind == "ballot":  # ballot box + tick
        draw.rectangle([x + 2, y + 4, x + s - 2, y + s - 2], outline=color, width=2)
        draw.line([x + 4, y + s // 2 + 1, x + s // 2, y + s - 4,
                   x + s - 3, y + 3], fill=color, width=2)
    elif kind == "star":
        cx, cy, r = x + s // 2, y + s // 2, s // 2 - 1
        pts = [(cx, cy - r), (cx + 3, cy - 2), (cx + r, cy - 2), (cx + 5, cy + 2),
               (cx + 7, cy + r - 1), (cx, cy + 4), (cx - 7, cy + r - 1),
               (cx - 5, cy + 2), (cx - r, cy - 2), (cx - 3, cy - 2)]
        draw.polygon(pts, fill=color)
    elif kind == "film":  # camera / culture
        draw.rectangle([x + 2, y + 5, x + s - 2, y + s - 3], outline=color, width=2)
        draw.ellipse([x + s // 2 - 3, y + s // 2 - 2, x + s // 2 + 3, y + s // 2 + 4],
                     outline=color, width=2)
    else:  # "dot" fallback
        draw.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=color)


def icon(draw, kind, accent, x, y):
    s = 18
    draw.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=accent)
    glyph(draw, kind, x + 1, y + 1, s - 2, WHITE)


# ---------- data: (kicker, headline, summary, sources, icon kind, accent) ----------
TOP = [
    ("1. CLIMATE  •  ANTALYA",
     "COP31 COLLAPSES — NO DEAL",
     "UN climate talks end with no deal as the EU rejects a text that never "
     "mentions fossil fuels — the longest COP ever.",
     "Just Security / Algenom / Democracy Now", "globe", "climate"),
    ("2. WAR  •  THE GULF",
     "IRAN HITS BAHRAIN SITE; US WAITS",
     "An Iranian strike hits a civilian industrial site, wounding two; the "
     "White House says a decision on new strikes is at least a week away.",
     "Just Security / World Watch", "flame", "war"),
    ("3. WAR  •  LIBYA",
     "UKRAINE SAYS ITS DRONES SANK A RUSSIAN SHIP",
     "Zelenskyy says sea drones sank the corvette Merkury at Benghazi; "
     "10 people are reported hurt.",
     "Algenom / Shadow / World Watch", "ship", "war"),
]

COLS = [
    ("WAR & DIPLOMACY", "8", [
        ("UKRAINE  —  Just Security / Daily Fox",
         "Russian strike on Dymer kills at least 11",
         "A drone strike partly destroys a flat block near Kyiv; 14 were first reported missing.",
         "flame", "war"),
        ("POLAND  —  Shadow / World Watch",
         "Fallen objects were Russian missiles",
         "Prosecutors say debris came from Kh-101 cruise missiles.",
         "flame", "war"),
        ("GAZA  —  Just Security",
         "Israeli strike on Gaza truck kills 3",
         "Gaza's Health Ministry says three were killed; the truck was said to carry food aid.",
         "flame", "war"),
        ("WEST BANK  —  Just Security",
         "Settler arson called 'Jewish terrorism'",
         "PM-elect Eisenkot condemns arson attacks on villages near Ramallah.",
         "flame", "war"),
        ("RUSSIA  —  Shadow / Off the Wire",
         "Russian ship Sparta II towed after fire",
         "A cargo ship with military ties caught fire in the Gulf of Finland after a suspected drone strike.",
         "ship", "war"),
        ("US–IRAN  —  Access24",
         "Trump warns Iran of 'very traumatic' outcome",
         "The president warns of consequences if a nuclear deal fails; a second carrier is weighed.",
         "flame", "war"),
        ("USA  —  GenFlow",
         "Senate GOP open to cutting Iran war funds",
         "Thune and Collins will discuss Democrats' demand to avoid a shutdown on 11 December.",
         "ballot", "us"),
        ("COLOMBIA  —  Open Chronicle",
         "Colombia nears 10 years since FARC peace deal",
         "The November 2016 accord that ended five decades of war turns ten.",
         "star", "world"),
    ]),
    ("AMERICAS & MARKETS", "10", [
        ("USA  —  GenFlow / Mueller",
         "Democrats reach 258 House seats",
         "After a recount, Foxx concedes in North Carolina — the biggest majority since 1992.",
         "ballot", "us"),
        ("USA  —  Daily 8 News",
         "Peltola flips Alaska Senate seat",
         "The Democrat beats two-term Republican Sullivan; Democrats reach 56 seats.",
         "ballot", "us"),
        ("USA  —  Mueller / The Guardian",
         "Mamdani plans to close Rikers Island",
         "New York's mayor unveils a plan to shut the jail complex.",
         "ballot", "us"),
        ("USA  —  Off the Wire",
         "Trump order limits Congress's access to data",
         "An executive order says lawmakers must show a valid legislative purpose.",
         "ballot", "us"),
        ("USA  —  Off the Wire",
         "FBI probes hack of police database",
         "An apparent hack of the National Crime Information Center is under investigation.",
         "chip", "tech"),
        ("MEXICO  —  Off the Wire",
         "Mexico captures 'El Chapo Isidro'",
         "Forces seize Fausto Isidro Meza Flores, one of the FBI's 10 most wanted, in Sinaloa.",
         "star", "world"),
        ("MARKETS  —  Algenom",
         "Asian chip stocks slide",
         "Kospi falls as much as 5.8% before closing down 3.3% after Wall Street's rout.",
         "chart", "market"),
        ("MARKETS  —  The Edge / GenFlow",
         "Wall Street rebounds sharply",
         "The Nasdaq 100 jumps about 7% in early trade; a Fed hike on 9 December is seen as near-certain.",
         "chart", "market"),
        ("TECH  —  The Edge / GenFlow",
         "Nvidia brings back Jensen Huang as CEO",
         "The board reinstates Huang as CEO; the stock rebounds.",
         "chip", "tech"),
    ]),
    ("SCIENCE, SPORT & CULTURE", "10", [
        ("SPACE  —  Gizmodo / AP / The Register",
         "BepiColombo reaches Mercury orbit",
         "Only the second mission to orbit Mercury; a thruster glitch is reported.",
         "rocket", "space"),
        ("TECH  —  The Edge",
         "CrowdStrike to buy Zscaler for $43.9bn",
         "An all-stock deal joining two cybersecurity giants.",
         "chip", "tech"),
        ("HEALTH  —  Access24",
         "Bangladesh vaccinates 50m children",
         "A month-long typhoid drive targets drug-resistant strains.",
         "cross", "health"),
        ("INDONESIA  —  Shadow",
         "Factory-fire search goes on",
         "Rescuers keep looking for workers missing after the blaze.",
         "flame", "world"),
        ("NIGERIA  —  Off the Wire",
         "Boat capsizes; at least 24 dead",
         "A mourners' boat overturns in Bayelsa State; the search goes on.",
         "ship", "world"),
        ("FOOTBALL  —  LiveScore",
         "Liverpool thrash Man Utd 4–0",
         "A one-sided Premier League night at Anfield on Monday.",
         "ball", "sport"),
        ("NFL  —  DAZN / NWKS Radio",
         "Chiefs roll 34–7; 49ers win in Mexico City",
         "Mahomes throws 3 TDs; San Francisco beats Minnesota 35–10.",
         "ball", "sport"),
        ("BASEBALL  —  Off the Wire",
         "Skubal signs record $450m Mets deal",
         "Nine years — the biggest contract ever for a pitcher.",
         "ball", "sport"),
        ("CULTURE  —  Off the Wire",
         "Miley Cyrus marries Maxx Morando",
         "An intimate Palm Springs wedding on Saturday.",
         "star", "culture"),
        ("OBITUARY  —  Off the Wire",
         "Tom Jackson, Broncos star, dies at 75",
         "Ex-linebacker and longtime ESPN analyst, remembered.",
         "star", "culture"),
    ]),
]

TICKER = ("TICKER  •  COP31: NO DEAL  •  IRAN HITS BAHRAIN  •  UKRAINE SINKS "
          "RUSSIAN SHIP  •  KOSPI −5.8%  •  HUANG BACK AT NVIDIA")

# ---------- masthead ----------
d.rectangle([0, 0, W, 6], fill=RED)
y = 16
d.text((24, y), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
y += 66
d.text((24, y), "MONDAY  •  23 NOVEMBER 2026", font=F_DATE, fill=RED)
right = "31 STORIES  •  WORLDWIDE  •  ONE DAY"
d.text((W - 24 - d.textlength(right, font=F_META), y + 3), right, font=F_META, fill=GREY)
y += 30
d.line([24, y, W - 24, y], fill=INK, width=2)
y += 9

# ---------- top stories ----------
col_w = (W - 48 - 2 * 16) // 3
top_y = y
top_h = 0
for i, (kick, head, body, src, kind, acc) in enumerate(TOP):
    x = 24 + i * (col_w + 16)
    yy = top_y
    d.line([x, yy, x + col_w, yy], fill=RED, width=3)
    yy += 8
    icon(d, kind, ACCENT[acc], x, yy)
    d.text((x + 24, yy + 2), kick, font=F_KICK, fill=RED)
    yy += 22
    for line in wrap(head, F_TOP_HEAD, col_w):
        d.text((x, yy), line, font=F_TOP_HEAD, fill=INK)
        yy += 25
    yy += 1
    for line in wrap(body, F_TOP_BODY, col_w):
        d.text((x, yy), line, font=F_TOP_BODY, fill=INK)
        yy += 16
    yy += 3
    d.text((x, yy), src, font=F_SRC, fill=GREY)
    yy += 13
    top_h = max(top_h, yy - top_y)
y = top_y + top_h + 4

# ---------- three columns ----------
sec_y = y
for ci, (title, count, items) in enumerate(COLS):
    x = 24 + ci * (col_w + 16)
    d.rectangle([x, sec_y, x + col_w, sec_y + 24], fill=NAVY)
    d.text((x + 8, sec_y + 4), title, font=F_KICK, fill=WHITE)
    d.text((x + col_w - 8 - d.textlength(count, font=F_KICK), sec_y + 4),
           count, font=F_KICK, fill=WHITE)
    yy = sec_y + 30
    for kick, head, body, kind, acc in items:
        icon(d, kind, ACCENT[acc], x, yy)
        d.text((x + 24, yy + 3), kick, font=F_KICK, fill=RED)
        yy += 19
        for line in wrap(head, F_HEAD, col_w):
            d.text((x, yy), line, font=F_HEAD, fill=INK)
            yy += 17
        for line in wrap(body, F_BODY, col_w):
            d.text((x, yy), line, font=F_BODY, fill=(60, 60, 60))
            yy += 14
        yy += 2
        d.line([x, yy, x + col_w, yy], fill=LINE, width=1)
        yy += 4
    if ci == 0:
        col_bottom = yy
    col_bottom = max(col_bottom, yy)
y = col_bottom + 2

# ---------- ticker + footer ----------
d.rectangle([0, y, W, y + 26], fill=NAVY)
d.text((24, y + 6), TICKER, font=F_TICK, fill=WHITE)
y += 26
d.text((24, y + 5),
       "All events of Monday 23 November 2026, as reported that day.",
       font=F_FOOT, fill=GREY)

assert y + 20 <= H, "layout overflow: %d" % (y + 20)
img.save("/home/hatch/workspace/make-fun-bounty/build/news-image-20261123/entry.png",
         optimize=True)
print("saved, bottom y =", y)
