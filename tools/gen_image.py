#!/usr/bin/env python3
"""Hand-drawn flat-vector world news page for 24 Nov 2026 (36 stories).
Renders entry.png at 1024x1024 with PIL only. Run: python3 tools/gen_image.py
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "entry.png")
FD = "/usr/share/fonts/truetype/dejavu"

def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

FB = lambda s: F("DejaVuSans-Bold.ttf", s)
FR = lambda s: F("DejaVuSans.ttf", s)
FSB = lambda s: F("DejaVuSerif-Bold.ttf", s)

W, H = 1024, 1024
PAPER = (247, 243, 232); INK = (26, 26, 26); MUT = (90, 88, 80)
RED = (192, 57, 43); BLUE = (31, 78, 121); TEAL = (18, 120, 110)
OCEAN = (168, 200, 220); LAND = (232, 217, 168); LAND2 = (214, 200, 150)
GOLD = (212, 160, 40); GREEN = (46, 125, 60)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def fit_lines(text, font, maxw, maxlines):
    lines = wrap(text, font, maxw)
    while len(lines) > maxlines and len(lines) > 1:
        # drop trailing words from the last line, then re-wrap shorter text
        words = text.split()
        text = " ".join(words[:-3]) + "."
        lines = wrap(text, font, maxw)
    return lines

def text(drw, xy, s, font, fill=INK):
    drw.text(xy, s, font=font, fill=fill)

# ---------------------------------------------------------------- map data
# Real coastline data (Natural Earth 50m, public domain), pre-projected to
# MAP pixel space by research/geo/prep_mapdata.py from ne_50m_land.geojson
# and ne_50m_admin_0_countries.geojson:
#   https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
#   https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
# This replaces the hand-written continent polygons. The finished entry.png
# needs no external data; main.py never touches this file.
# lon/lat polygons, equirectangular: lon -180..180 -> map x, lat 75..-55 -> map y
MAP = (8, 438, 684, 576)  # x0,y0,x1,y1
def proj(lon, lat):
    x0, y0, x1, y1 = MAP
    x = x0 + (lon + 180) / 360.0 * (x1 - x0)
    y = y0 + (75 - lat) / 130.0 * (y1 - y0)
    return (x, y)

with open(os.path.join(HERE, "mapdata.json")) as _f:
    _MAPDATA = json.load(_f)
LAND_POLYS = [[tuple(p) for p in poly] for poly in _MAPDATA["land"]]
LAKE_POLYS = [[tuple(p) for p in poly] for poly in _MAPDATA["lakes"]]
BORDER_RINGS = [[tuple(p) for p in poly] for poly in _MAPDATA["borders"]]

PINS = [  # (lon, lat, story no.) — number IS the story number (1,2,3,4,6,7,8,9,10,11,14,30,31);
    # stories 5, 12, 13 have no pin (company story / global report / alliance statement)
    (-74, 41, 1), (56, 26, 2), (47, 25, 3), (20, 32, 4), (121, 31, 6),
    (-17, 15, 7), (2, 49, 8), (30, 40, 9), (106, 21, 10), (-76, 10, 11),
    (35, 48, 14), (34, 31, 30), (45, 13, 31),
]


# ---------------------------------------------------------------- header
d.rectangle([0, 0, W, 62], fill=(26, 32, 44))
d.rectangle([0, 62, W, 66], fill=RED)
text(d, (16, 8), "THE WORLD IN ONE DAY", FB(30), fill=(247, 243, 232))
text(d, (16, 42), "TUESDAY, 24 NOVEMBER 2026  \u00b7  36 STORIES, ONE DAY", FR(12), fill=(200, 205, 215))
d.text((W - 16, 12), "No. 24", font=FB(14), fill=GOLD, anchor="ra")
d.text((W - 16, 34), "ALL HAND-DRAWN", font=FR(11), fill=(200, 205, 215), anchor="ra")

# ---------------------------------------------------------------- headlines
HEADLINES = [
    ("1  HUAWEI GUILTY OF TRADE-SECRET THEFT AND BANK FRAUD",
     "A US jury in Brooklyn convicted Huawei of trade-secret theft and bank fraud, guilty on 10 of 12 counts, but acquitted it of racketeering. Huawei expects to appeal.",
     "AP"),
    ("2  IRAN SAYS FOUR TANKERS HIT MINES IN STRAIT OF HORMUZ",
     "Iran's Revolutionary Guard said three oil tankers hit naval mines in the Strait of Hormuz and caught fire, then reported a fourth. The mine claims were unconfirmed.",
     "AL JAZEERA"),
    ("3  HOUTHI STRIKE HITS RIYADH TOWER, 11 HURT",
     "A Houthi attack hit a tower in Riyadh's King Abdullah Financial District, wounding at least 11 people. It was the second hit on the capital's tallest tower in under a week.",
     "REUTERS / AFP"),
]

def illu_huawei(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 240)); d.rectangle(box, outline=INK, width=2)
    d.rounded_rectangle([x0+95, y0+14, x0+225, y0+58], 8, fill=(40, 44, 54), outline=(200,200,200), width=2)
    d.line([x0+150, y0+20, x0+185, y0+40, x0+165, y0+54], fill=(255,255,255), width=2)
    d.line([x0+185, y0+40, x0+205, y0+30], fill=(255,255,255), width=2)
    d.polygon([(x0+40, y0+14), (x0+110, y0+6), (x0+116, y0+22), (x0+46, y0+30)], fill=(120, 72, 30))
    d.line([x0+78, y0+26, x0+118, y0+52], fill=(120, 72, 30), width=6)
    d.rectangle([x0+235, y0+48, x0+305, y0+58], fill=(120, 72, 30))
    d.rectangle([x0+225, y0+4, x0+312, y0+28], outline=RED, width=3)
    text(d, (x0+231, y0+8), "GUILTY", FB(17), fill=RED)

def illu_hormuz(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(170, 205, 225)); d.rectangle(box, outline=INK, width=2)
    d.polygon([(x0, y0), (x0+70, y0), (x0+40, y0+40), (x0, y0+40)], fill=(150, 125, 90))
    d.polygon([(x1, y0), (x1-70, y0), (x1-40, y0+40), (x1, y0+40)], fill=(150, 125, 90))
    for i, cx in enumerate([x0+95, x0+165, x0+235]):
        d.rectangle([cx-28, y0+44, cx+28, y0+56], fill=(60, 60, 60))
        d.polygon([(cx-8, y0+44), (cx+8, y0+44), (cx, y0+28)], fill=(230, 110, 30))
        d.ellipse([cx-6, y0+14, cx+6, y0+28], fill=(60, 60, 60))
    d.ellipse([x0+140, y0+52, x0+152, y0+60], fill=(30, 30, 30))
    d.line([x0, y0+58, x1, y0+58], fill=(31, 78, 121), width=2)

def illu_riyadh(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(225, 225, 230)); d.rectangle(box, outline=INK, width=2)
    d.polygon([(x0+130, y0+10), (x0+180, y0+10), (x0+180, y0+60), (x0+130, y0+60)], fill=(90, 140, 180))
    for yy in range(y0+18, y0+58, 10):
        d.line([x0+134, yy, x0+176, yy], fill=(220, 235, 245), width=2)
    d.ellipse([x0+150, y0+0, x0+172, y0+14], fill=(120, 120, 120))
    d.ellipse([x0+185, y0+4, x0+210, y0+20], fill=(150, 150, 150))
    d.ellipse([x0+235, y0+10, x0+255, y0+22], fill=(40, 40, 40))
    d.line([x0+228, y0+8, x0+262, y0+8], fill=INK, width=2)
    d.rectangle([x0+30, y0+46, x0+70, y0+60], fill=(255, 255, 255), outline=RED, width=2)
    text(d, (x0+44, y0+49), "+", FB(12), fill=RED)
    d.rectangle([x0+240, y0+46, x0+280, y0+60], fill=(255, 255, 255), outline=RED, width=2)
    text(d, (x0+254, y0+49), "+", FB(12), fill=RED)

ILLU_BIG = [illu_huawei, illu_hormuz, illu_riyadh]
for i, (title, body, src) in enumerate(HEADLINES):
    x = 8 + i * 340; w = 332
    d.rectangle([x, 72, x + w, 250], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x, 72, x + w, 92], fill=(26, 32, 44))
    text(d, (x + 8, 76), "TOP STORY " + str(i + 1) + "  \u00b7  " + src, FB(11), fill=(247, 243, 232))
    ILLU_BIG[i]((x + 8, 98, x + w - 8, 98 + 62))
    lines = fit_lines(title, FB(13), w - 16, 2)
    yy = 166
    for ln in lines:
        text(d, (x + 8, yy), ln, FB(13)); yy += 16
    blines = fit_lines(body, FR(11), w - 16, 3)
    yy += 2
    for ln in blines:
        text(d, (x + 8, yy), ln, FR(11)); yy += 14

# ---------------------------------------------------------------- small stories
SMALL = [
    ("4  UKRAINE HITS RUSSIAN SHIPS", "Ukraine said drones sank Merkury off Benghazi; Libya said damaged, not sunk.", "ship"),
    ("5  NVIDIA'S HUANG IN THERAPY", "Huang apologised to staff a day after his return. Shares fell about 7%.", "chart"),
    ("6  CHINA PROBES CHEN JINING", "Shanghai chief Chen Jining, a Politburo member, is under investigation.", "glass"),
    ("7  SENEGAL REGAIN AFCON TITLE", "CAS reinstated Senegal as 2025 AFCON winners on appeal. The 1-0 win stands.", "cup"),
    ("8  SANOFI BUYS INSMED, $41BN", "Sanofi agreed to buy US biotech Insmed for $41 billion in cash, $175 a share.", "pill"),
    ("9  TURKISH HELICOPTER CRASH", "An AS-532 crashed after take-off from Eskisehir, killing all five crew.", "heli"),
    ("10  HANOI RESTAURANT BLAST", "A blast at a hotpot restaurant killed at least six and injured at least ten.", "flame"),
    ("11  CARTAGENA HOSTAGES", "Armed men seized a supermarket and held 25 people hostage; five were released.", "shop"),
    ("12  LANDMINE TOLL: 5-YR HIGH", "Landmines killed or injured 6,929 people in 2025, the highest toll since 2020.", "mine"),
    ("13  NATO TO DEFEND SPACE", "NATO will defend against space threats after reports of a Russian satellite.", "sat"),
]

def illu_small(kind, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(box, fill=(235, 238, 240)); d.rectangle(box, outline=INK, width=1)
    if kind == "ship":
        d.rectangle([x0+8, cy, x1-8, cy+8], fill=(90, 90, 90))
        d.polygon([(cx-14, cy), (cx+14, cy), (cx, cy-14)], fill=(192, 57, 43))
        d.line([x0+4, y1-4, x1-4, y1-4], fill=BLUE, width=2)
    elif kind == "chart":
        d.line([x0+6, y0+6, x0+40, y0+14, x0+75, y0+8, x1-8, y1-6], fill=RED, width=3)
        d.rectangle([x1-26, y0+4, x1-8, y0+14], fill=GREEN)
    elif kind == "glass":
        d.ellipse([cx-16, cy-12, cx+16, cy+12], outline=INK, width=3)
        d.line([cx+12, cy+10, cx+24, cy+20], fill=INK, width=3)
        d.rectangle([x0+6, y0+4, x0+26, y0+14], fill=RED)
    elif kind == "cup":
        d.polygon([(cx-14, cy-12), (cx+14, cy-12), (cx+10, cy+6), (cx-10, cy+6)], fill=GOLD)
        d.rectangle([cx-16, cy+6, cx+16, cy+10], fill=GOLD)
        for px, pc in [(x0+10, RED), (x0+30, GOLD), (x0+50, GREEN)]:
            d.rectangle([px, y0+4, px+5, y0+9], fill=pc)
    elif kind == "pill":
        d.ellipse([cx-22, cy-9, cx+22, cy+9], fill=(255, 255, 255), outline=RED, width=2)
        d.line([cx-22, cy, cx+22, cy], fill=RED, width=2)
        text(d, (x1-52, y0+2), "$41bn", FB(10), fill=RED)
    elif kind == "heli":
        d.ellipse([cx-20, cy-6, cx+20, cy+6], fill=(120, 120, 120))
        d.line([cx-30, cy-6, cx+30, cy-6], fill=INK, width=2)
        d.line([cx+20, cy, cx+34, cy-8], fill=INK, width=2)
        d.polygon([(x0+4, y1-4), (x0+40, y1-4), (x0+22, y1-14)], fill=GREEN)
    elif kind == "flame":
        d.polygon([(cx, cy-14), (cx+10, cy+2), (cx+5, cy+10), (cx-5, cy+10), (cx-10, cy+2)], fill=(230, 110, 30))
        d.polygon([(cx, cy-6), (cx+5, cy+4), (cx-5, cy+4)], fill=(240, 200, 40))
    elif kind == "shop":
        d.rectangle([x0+10, cy-8, x1-10, cy+12], fill=(255, 255, 255), outline=BLUE, width=2)
        d.rectangle([x0+10, cy-8, x1-10, cy-2], fill=BLUE)
        text(d, (cx-12, cy+1), "SHOP", FB(8), fill=INK)
    elif kind == "mine":
        d.polygon([(cx, cy-14), (cx+14, cy+10), (cx-14, cy+10)], fill=(255, 255, 255), outline=RED, width=2)
        text(d, (cx-3, cy-2), "!", FB(12), fill=RED)
        d.ellipse([cx+14, cy+6, cx+22, cy+12], fill=INK)
    elif kind == "sat":
        d.ellipse([cx+26, cy-18, cx+52, cy+6], fill=(200, 210, 190), outline=INK, width=1)
        d.rectangle([cx-14, cy-6, cx+6, cy+6], fill=(90, 140, 180), outline=INK, width=1)
        d.rectangle([cx-26, cy-3, cx-14, cy+3], fill=BLUE)
        d.rectangle([cx+6, cy-3, cx+18, cy+3], fill=BLUE)

for i, (title, body, kind) in enumerate(SMALL):
    col, row = i % 5, i // 5
    x = 8 + col * 204; y = 258 + row * 78; w = 196; h = 74
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    illu_small(kind, (x + 4, y + 4, x + w - 4, y + 30))
    tlines = fit_lines(title, FB(10), w - 10, 2)
    yy = y + 33
    for ln in tlines:
        text(d, (x + 5, yy), ln, FB(10)); yy += 12
    blines = fit_lines(body, FR(9), w - 10, 2 if len(tlines) == 1 else 1)
    for ln in blines:
        text(d, (x + 5, yy), ln, FR(9)); yy += 11

# ---------------------------------------------------------------- map + regions
text(d, (8, 416), "WHERE IT HAPPENED  \u00b7  13 PLACES PINNED", FB(14))
d.rectangle(MAP, fill=OCEAN, outline=INK, width=2)
# faint graticule, every 30 degrees, drawn on the ocean only (land covers it)
GRID = (145, 180, 205)
for _lon in range(-180, 181, 30):
    _gx = MAP[0] + (_lon + 180) / 360.0 * (MAP[2] - MAP[0])
    d.line([_gx, MAP[1], _gx, MAP[3]], fill=GRID, width=1)
for _lat in (60, 30, 0, -30):
    _gy = proj(0, _lat)[1]
    d.line([MAP[0], _gy, MAP[2], _gy], fill=GRID, width=1)
for poly in LAND_POLYS:
    d.polygon(poly, fill=LAND, outline=(150, 140, 100))
for poly in LAKE_POLYS:
    d.polygon(poly, fill=OCEAN, outline=(150, 140, 100))
for ring in BORDER_RINGS:
    d.line(ring, fill=(120, 110, 70), width=1)
# pin check, run BEFORE pins are drawn: each pin must have land or
# coastline pixels within a 16px radius. Sea pins (Hormuz, off Libya,
# Bab el-Mandeb) sit in water next to a coast, so they pass on nearby
# land; no pin is ever moved to pass the check.
_px = img.load()
_COAST = {(150, 140, 100), (120, 110, 70)}
_disc = {}
for (lon, lat, n) in PINS:
    _x, _y = proj(lon, lat); _xi, _yi = int(_x), int(_y)
    _hit = 0
    for _dx in range(-16, 17):
        for _dy in range(-16, 17):
            if math.hypot(_dx, _dy) <= 16:
                _xx, _yy = _xi + _dx, _yi + _dy
                if 0 <= _xx < W and 0 <= _yy < H and (_px[_xx, _yy] == LAND or _px[_xx, _yy] in _COAST):
                    _hit += 1
    _disc[n] = _hit
    if _hit == 0:
        print(f"PIN {n} has no land/coastline pixels within 16px"); sys.exit(1)
print("pin disc check: 13/13 have land/coastline within 16px:", _disc)
# label last (with a white halo), so no label can ever be covered by
# another pin's marker. This fixes pin 4 (Benghazi): its "4" used to be
# drawn before the later pins, and the neighbouring red marker covered
# the right half of the "4" at 2x zoom.
for (lon, lat, n) in PINS:
    x, y = proj(lon, lat)
    d.ellipse([x - 7, y - 16, x + 7, y - 2], fill=RED, outline=(255, 255, 255), width=1)
    d.polygon([(x - 6, y - 4), (x + 6, y - 4), (x, y + 4)], fill=RED)
    d.ellipse([x - 2, y - 13, x + 2, y - 9], fill=(255, 255, 255))
for (lon, lat, n) in PINS:
    x, y = proj(lon, lat)
    off = {9: (-18, -18), 14: (8, -28), 30: (-20, -2), 2: (8, 6), 3: (8, -28)}.get(n, (8, -18))
    d.text((x + off[0], y + off[1]), str(n), font=FB(10), fill=RED,
           stroke_width=2, stroke_fill=(255, 255, 255))
# pin legend under map handled by numbers in stories; region panel
RX0, RY0 = 700, 438
d.rectangle([RX0, RY0, 1016, 576], fill=(255, 255, 255), outline=INK, width=2)
text(d, (RX0 + 10, RY0 + 6), "STORIES BY REGION", FB(12))
REGIONS = [("Europe", 9, (31, 78, 121)), ("North America", 7, (192, 57, 43)),
           ("Asia", 8, (18, 120, 110)), ("Middle East", 5, (212, 160, 40)),
           ("Africa", 4, (46, 125, 60)), ("South America", 1, (120, 72, 30)),
           ("Global", 2, (90, 88, 80))]
yy = RY0 + 24
for name, cnt, col in REGIONS:
    text(d, (RX0 + 10, yy), name, FR(11))
    bw = int(cnt / 9.0 * 150)
    d.rectangle([RX0 + 120, yy + 2, RX0 + 120 + bw, yy + 12], fill=col)
    text(d, (RX0 + 278, yy), str(cnt), FB(12))
    yy += 13
text(d, (RX0 + 10, yy + 2), "TOTAL  36 STORIES", FB(12), fill=RED)

# ---------------------------------------------------------------- briefs 14-36
BRIEFS = [
    (14, "RUSSIAN STRIKE KILLS 2 IN ZAPORIZHZHIA", "A Russian strike killed two people and wounded 22, including two children, in Zaporizhzhia overnight, an official said Tuesday."),
    (15, "MONDAY: 460,000 RUSSIAN WAR DEAD", "The Guardian's analysis of 11 million leaked Russian death certificates found over 460,000 war-linked deaths since February 2022."),
    (16, "RUSSIAN DRONE ENTERS POLISH AIRSPACE", "A Russian drone entered Polish airspace during strikes on Ukraine, four days after three Russian missiles crossed into Poland."),
    (17, "UK SANCTIONS HOUTHIS, FOUR OFFICIALS", "Britain designated the Houthis under its Yemen sanctions regime and sanctioned four figures over torture, rape and attacks on shipping."),
    (18, "BURNHAM RULES OUT EU REJOIN VOTE", "Labour leader Andy Burnham ruled out rejoining the EU without a referendum, hitting back at former prime ministers."),
    (19, "MONDAY: IOWA BLAST CLEARED BY COURT", "A US appeals court cleared the Army to detonate 68 barrels of lead azide in Iowa on Wednesday morning."),
    (20, "MONDAY: STATES SUE MUSK OVER GROK", "Virginia and Oregon sued Musk's SpaceX Super Intelligence, the first states to sue over Grok making sexualised images of children."),
    (21, "TRUMP TO HONOUR GIULIANI", "Trump gave the Medal of Freedom, the top US civilian honour, to ex-New York mayor Rudy Giuliani."),
    (22, "TRUMP PLANS NEW TARIFFS ON CHINA", "Trump is preparing tariffs on China, the EU and 14 other economies over industrial subsidies, the Wall Street Journal reported."),
    (23, "ABREGO GARCIA TO LEAVE US", "Salvadoran migrant Kilmar Abrego Garcia will leave the US voluntarily to avoid deportation, flying to Europe on a commercial flight."),
    (24, "SATURDAY FIRE TOLL RISES TO 26", "Authorities confirmed 26 workers died in the Serang candy factory fire, with eight still missing and police probing negligence."),
    (25, "SHENZHOU 24 CREW UNVEILED", "China unveiled the Shenzhou 24 crew, including Pakistani Muhammad Zeeshan Ali, 40, the first foreigner to board the Tiangong station."),
    (26, "CHINA OFFICIAL GETS DEATH FOR SPYING", "A Chinese official surnamed Ma was sentenced to death for spying, passing 35 state secrets for over one million yuan."),
    (27, "MALAYSIA TO RETURN 6,803 TO MYANMAR", "Malaysia will return 6,803 migrants to Myanmar: 1,500 by naval ships in December and 5,303 by aircraft."),
    (28, "SOUTH KOREA SCRAMBLES JETS", "South Korea scrambled fighter jets and ordered Ulleungdo residents to shelter after Russian aircraft entered its air defence zone."),
    (29, "SINGAPORE LIFTS GROWTH FORECAST", "Singapore raised its 2026 growth forecast to around 6% after the economy grew 6.1% in the third quarter."),
    (30, "ISRAEL KILLS HAMAS SECURITY CHIEF", "An Israeli strike killed Hamas security chief Naeem Abu Nahal in Gaza City, with six others killed despite the ceasefire."),
    (31, "HOUTHIS 60 KM FROM ADEN", "Yemen's military said Houthi fighters are about 60 km from Aden, the temporary capital, and ready to attack."),
    (32, "IRAQ ORDERS KURDISH OILFIELDS SEIZED", "Iraq's prime minister ordered federal control of oilfields in Diyala, Kirkuk, Salahuddin and Nineveh, and of Kurdish border crossings."),
    (33, "NIGERIA TRIMS 2026 BUDGET TO $48BN", "President Bola Tinubu asked parliament to cut 2026 spending to 65.2 trillion naira ($48 billion) from 68.3 trillion naira."),
    (34, "SUNDAY: CONGO PLANE MISSING", "DR Congo lost a Cessna 208 plane, while rebels claimed they shot down an aircraft near Minembwe with four aboard."),
    (35, "CONGO MINING FORUM PLEDGES $965M", "The Makutano Forum in Kinshasa announced $965 million in mining financing for DR Congo, including $265 million via the IFC."),
    (36, "QUASAR IS OLDEST EVER SEEN", "Astronomers found the most distant quasar yet, formed 630 million years after the Big Bang."),
]
text(d, (8, 586), "THE DAY IN BRIEF  \u00b7  14\u201336", FB(14))
d.line([8, 606, 1016, 606], fill=INK, width=1)
yy = 610
for num, title, body in BRIEFS:
    size = 11
    while size >= 9:
        fb, fr = FB(size), FR(size)
        head = f"{num}. {title}  "
        if fb.getlength(head) + fr.getlength(body) <= 1000:
            break
        size -= 1
    else:
        fb, fr = FB(9), FR(9)
        head = f"{num}. {title}  "
        words = body.split()
        while fb.getlength(head) + fr.getlength(body) > 1000 and len(words) > 8:
            words = words[:-2]; body = " ".join(words) + "."
    text(d, (8, yy), head, fb)
    text(d, (8 + fb.getlength(head), yy), body, fr)
    yy += 16
assert yy <= 985, f"briefs overflow: end y={yy}"

# ---------------------------------------------------------------- footer
d.line([8, 982, 1016, 982], fill=INK, width=1)
text(d, (8, 988), "Map drawn from public coastline data; all other illustrations are hand-drawn flat-vector art made for this page. No photographs and no wire-service images are used.",
     FR(9), fill=MUT)
text(d, (8, 1001), "Sources: AP, Reuters, AFP, The Guardian, Al Jazeera, WSJ, SCMP, CNN, The Hindu, Fox News, NPR, Sanofi, ICBL, CNA, BBC.",
     FR(9), fill=MUT)
text(d, (8, 1013), "Follow-ups are labelled in the item itself: Monday (15, 19, 20), Saturday (24), Sunday (34). All figures are as reported on 24 Nov 2026.",
     FR(9), fill=MUT)

# ---------------------------------------------------------------- checks before save
img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
print("counts: headlines 3, small 10, briefs", len(BRIEFS), "total", 3 + 10 + len(BRIEFS),
      "regions total", sum(c for _, c, _ in REGIONS))
