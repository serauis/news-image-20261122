#!/usr/bin/env python3
"""Build the Sunday 22 November 2026 front page: 39 sourced stories
(3 illustrated heroes, 6 pictured tiles, 30 ALSO items) composed from
fresh illustration sheets into one 1024x1024 newspaper page."""
import glob
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2
W = 1024 * S
page = Image.new("RGB", (W, W), (247, 242, 231))
d = ImageDraw.Draw(page)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
INK = (20, 32, 46)
RED = (179, 52, 31)
GREY = (90, 84, 70)
CARD = (255, 253, 246)
LINE = (205, 196, 172)
BODY = (52, 48, 40)


def F(path, px):
    return ImageFont.truetype(path, int(px * S))


def wrap(text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, w, text, font, fill, leading):
    for ln in wrap(text, font, w):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def cover(im, tw, th, ybias=0.5):
    tw, th = int(tw), int(th)
    r = max(tw / im.width, th / im.height)
    im2 = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)),
                    Image.LANCZOS)
    x = (im2.width - tw) // 2
    y = int((im2.height - th) * ybias)
    return im2.crop((x, y, x + tw, y + th))


def find_art(pat):
    hits = sorted(glob.glob(os.path.join(HERE, pat + ".png")) +
                  glob.glob(os.path.join(HERE, pat + ".webp")))
    return hits[0]


# ---------- art ----------
strip = Image.open(find_art("media-generation-hero-strip-20261122-0-*")).convert("RGB")
sw, sh = strip.size


def panel(i):
    return strip.crop((int(sw * (i / 3 + 0.006)), int(sh * 0.012),
                       int(sw * ((i + 1) / 3 - 0.006)), int(sh * 0.988)))


HERO = {"cop31": panel(0), "cricket": panel(1), "bahrain": panel(2)}
HERO_BIAS = {"cop31": 0.35, "cricket": 0.45, "bahrain": 0.30}

sheet = Image.open(find_art("media-generation-sprite-sheet-20261122-0-*")).convert("RGB")
gw, gh = sheet.size


def cell(c, r):
    return sheet.crop((int(gw * (c / 4 + 0.008)), int(gh * (r / 3 + 0.011)),
                       int(gw * ((c + 1) / 4 - 0.008)),
                       int(gh * ((r + 1) / 3 - 0.011))))


ART = {
    "nepal": cell(0, 0), "vegas": cell(1, 0), "france": cell(2, 0),
    "peru": cell(3, 0), "nigeria": cell(0, 1), "euindo": cell(1, 1),
}
TILE_BIAS = {"nepal": 0.40, "vegas": 0.40, "france": 0.45,
             "peru": 0.35, "nigeria": 0.45, "euindo": 0.35}

M = 28 * S
CW = W - 2 * M
gap = 13 * S
tw3 = (CW - 2 * gap) // 3
cellw = CW // 6

# ---------- masthead ----------
f_kick = F(SANS_B, 12.5)
d.text((M, 13 * S), "T H E   W O R L D   I N   O N E   D A Y", font=f_kick, fill=RED)
r = "39 STORIES · 7 REGIONS"
d.text((W - M - d.textlength(r, font=f_kick), 13 * S), r, font=f_kick, fill=RED)
f_title = F(SERIF_B, 45)
t = "Sunday 22 November 2026"
d.text(((W - d.textlength(t, font=f_title)) / 2, 28 * S), t, font=f_title, fill=INK)
f_sub = F(SANS_I, 13)
sub = ("COP31 nears a deal at dawn · Pant's 128 puts India 261 ahead · "
       "Gulf strikes hit US bases in Bahrain")
d.text(((W - d.textlength(sub, font=f_sub)) / 2, 83 * S), sub, font=f_sub,
       fill=(70, 62, 48))
d.line([M, 99 * S, W - M, 99 * S], fill=INK, width=2 * S)
d.line([M, 103 * S, W - M, 103 * S], fill=INK, width=S)

# ---------- stats ----------
stats = [("128", "Pant's runs in Wellington"),
         ("261", "India's lead at lunch, day four"),
         ("24", "dead in the Bayelsa boat capsize"),
         ("152", "homes uninhabitable in Peru"),
         ("82,500", "counted at France's marches"),
         ("$50m", "COP31 loss-and-damage pledges")]
f_num = F(SANS_B, 18)
f_cap = F(SANS, 9.5)
for i, (n, c) in enumerate(stats):
    x = M + i * cellw
    if i:
        d.line([x, 105 * S, x, 133 * S], fill=LINE, width=S)
    d.text((x + 6 * S, 108 * S), n, font=f_num, fill=RED if i in (2, 5) else INK)
    d.text((x + 6 * S, 129 * S), c, font=f_cap, fill=GREY)
d.line([M, 140 * S, W - M, 140 * S], fill=LINE, width=S)

# ---------- UTC timeline ----------
d.text((M, 148 * S), "THE DAY IN UTC", font=F(SANS_B, 11), fill=RED)
tl = [("00:02", "Israel alleges Hamas is tightening its hold on Gaza"),
      ("00:03", "Pant's hundred takes India past 600 in Wellington"),
      ("03:00", "Deadline for objections to the COP31 deal text"),
      ("04:00", "Las Vegas Grand Prix lights go out on the Strip"),
      ("06:00", "COP31 reconvenes to approve the deal"),
      ("08:00", "Nepal's PM departs Kathmandu for Delhi (13:45 local)")]
f_tt = F(SANS_B, 11)
f_tx = F(SANS, 9)
for i, (tm, tx) in enumerate(tl):
    x = M + i * cellw
    d.text((x + 2 * S, 162 * S), tm, font=f_tt, fill=INK)
    block(x + 2 * S, 175 * S, cellw - 8 * S, tx, f_tx, BODY, 10 * S)

# ---------- heroes ----------
heroes = [
    ("cop31", (24, 110, 70), "1 · ANTALYA — CLIMATE",
     "COP31 nears a deal at dawn after a night of talks",
     "A new package went to a late-night plenary, the presidents saying all "
     "parties could agree; objections by 03:00 GMT, approval at 06:00 GMT. — Reuters"),
    ("cricket", (28, 84, 140), "2 · WELLINGTON — CRICKET",
     "Pant's 128 puts India 261 ahead on day four",
     "India reach 629-6 at lunch; Pant's ninth Test hundred takes him past "
     "McCullum for career sixes. — ESPNcricinfo"),
    ("bahrain", (140, 40, 40), "3 · BAHRAIN — GULF",
     "IRGC strikes two US bases; fire at a Bahrain plant",
     "Bahrain reports a fire at an industrial facility and no injuries, as Iran "
     "says it hit US positions at two bases. — Hatha Alyoum, wires"),
]
f_cat = F(SANS_B, 11)
f_hh = F(SANS_B, 19)
f_deck = F(SANS, 10.5)
hy = 202 * S
hh = 230 * S
for i, (art, color, cat, head, deck) in enumerate(heroes):
    x = M + i * (tw3 + gap)
    d.rectangle([x, hy, x + tw3, hy + hh], fill=CARD, outline=LINE, width=S)
    page.paste(cover(HERO[art], tw3, 112 * S, HERO_BIAS[art]), (x, hy))
    d.rectangle([x, hy + 112 * S, x + tw3, hy + 118 * S], fill=color)
    block(x + 12 * S, hy + 128 * S, tw3 - 24 * S, cat, f_cat, color, 13 * S)
    block(x + 12 * S, hy + 146 * S, tw3 - 24 * S, head, f_hh, INK, 21.5 * S)
    block(x + 12 * S, hy + 190 * S, tw3 - 24 * S, deck, f_deck, BODY, 12.7 * S)
    print("hero", art, "head lines:",
          len(wrap(head, f_hh, tw3 - 24 * S)),
          "deck lines:", len(wrap(deck, f_deck, tw3 - 24 * S)))

# ---------- pictured tiles: 6, 3 x 2 ----------
tiles = [
    ("nepal", (28, 84, 140), "4 · NEW DELHI — NEPAL",
     "Nepal's PM lands in Delhi for first state visit",
     "Shah meets President Murmu and Jaishankar today; talks with Modi on Monday. — MEA, Nepal MoFA"),
    ("vegas", (165, 40, 30), "5 · LAS VEGAS — FORMULA 1",
     "Verstappen on pole as the Strip race starts at 04:00 UTC",
     "Antonelli was fastest in qualifying but drops five places; the race runs under lights. — Formula 1"),
    ("france", (24, 110, 70), "6 · PARIS — PROTESTS",
     "Sixth weekend of marches as turnout falls",
     "The ministry counts 82,500 nationwide; organisers say 150,000. — AFP, wires"),
    ("peru", (140, 40, 40), "7 · JUNIN — QUAKE",
     "Revised toll: 152 homes uninhabitable in Peru",
     "Eight injured and four homes destroyed in the 6.7 quake, civil defence says. — INDECI, AppiSToS"),
    ("nigeria", (28, 84, 140), "8 · BAYELSA — NIGERIA",
     "Boat toll rises to 24 as the search goes on",
     "Up to 300 were aboard the mourners' boat; 24 were rescued. — AP, NEMA"),
    ("euindo", (24, 110, 70), "9 · BRUSSELS — TRADE",
     "EU and Indonesia sign trade and investment deals",
     "The CEPA and IPA are signed after years of talks; ratification still to come. — European Commission"),
]
f_tc = F(SANS_B, 10.5)
f_th = F(SANS_B, 13)
f_td = F(SANS, 9)
ty = 440 * S
th = 128 * S
tgap = 9 * S
for r in range(2):
    for c in range(3):
        art, color, cat, head, deck = tiles[r * 3 + c]
        x = M + c * (tw3 + gap)
        y = ty + r * (th + tgap)
        d.rectangle([x, y, x + tw3, y + th], fill=CARD, outline=LINE, width=S)
        page.paste(cover(ART[art], tw3, 50 * S, TILE_BIAS[art]), (x, y))
        d.rectangle([x, y + 50 * S, x + tw3, y + 53 * S], fill=color)
        block(x + 8 * S, y + 59 * S, tw3 - 16 * S, cat, f_tc, color, 12 * S)
        block(x + 8 * S, y + 73 * S, tw3 - 16 * S, head, f_th, INK, 15 * S)
        block(x + 8 * S, y + 104 * S, tw3 - 16 * S, deck, f_td, BODY, 11.5 * S)
        print("tile", art, "head lines:",
              len(wrap(head, f_th, tw3 - 16 * S)),
              "deck lines:", len(wrap(deck, f_td, tw3 - 16 * S)))

# ---------- also ----------
ay = 715 * S
d.text((M, ay), "ALSO ON SUNDAY 22 NOVEMBER", font=F(SANS_B, 13), fill=RED)
d.line([M, ay + 20 * S, W - M, ay + 20 * S], fill=LINE, width=S)
also = [
    ("WASHINGTON —", "Trump calls Iran's new leaders “probably more reasonable, but very, very difficult” in a Fox interview."),
    ("TEHRAN —", "Iran will not send enriched uranium abroad, its deputy foreign minister says after Qatari talks."),
    ("KYIV —", "Zelensky calls the Crimean Bridge strikes a “fair response” as he meets the UK's Streeting."),
    ("COPENHAGEN —", "Denmark urges the EU to halt tourist visas for Russians."),
    ("TALLINN —", "Estonia scrambles allied jets after a morning drone alert; its Russia border crossings close from 1 Dec."),
    ("HELSINKI —", "Finland probes a suspected Russian helicopter airspace violation of up to 4.1 km."),
    ("GULF OF FINLAND —", "A Russian cargo vessel is on fire after a strike and drifts into Finnish waters."),
    ("BRUSSELS —", "Costa proposes a €1.78tn EU budget for 2028–2034; agreement still pending."),
    ("GAZA —", "WCK denial: the military says a strike hit Islamic Jihad members."),
    ("LONDON —", "The Princess of Wales fronts BBC film “Heal” on her cancer recovery; it airs 29 Nov."),
    ("MOSCOW —", "Wildberries' CEO steps down days after EU sanctions, media report."),
    ("WASHINGTON —", "The FBI investigates an apparent hack of its national crime database."),
    ("OSLO —", "The Trafalgar Square Christmas tree sets off from Oslo for London."),
    ("RANCHI —", "Fourteen flights are cancelled amid Cyclone Akvan."),
    ("LONDON —", "Prince William announces an insurance scheme for 10,000 temporary forest staff."),
    ("CANBERRA —", "Pat Cummins keeps Cricket Australia's backing to remain Test captain."),
    ("ANTALYA —", "COP31's AI pledge fails to attract major US tech companies."),
    ("ANTALYA —", "The “35 by 35” power goal is backed by some 90 countries in the draft."),
    ("ANTALYA —", "Just $50m is pledged for loss and damage, against $135m last year."),
    ("LONDON —", "Heavy rain is tipped for Devon and Cornwall on Sunday as cold snaps ease."),
    ("GAZA —", "Israel alleges Hamas is tightening its hold on the Strip."),
    ("WASHINGTON —", "A lock of George Washington's hair fetches $4,000 at auction."),
    ("LOS ANGELES —", "A suspect is convicted over the deadly 2025 Palisades blaze."),
    ("WASHINGTON —", "Trump shares a Democratic senator-elect's “TrumpCare” plan on Truth Social."),
    ("ZURICH —", "CAF confirms unanimous support for Infantino's re-election bid."),
    ("LONDON —", "The UK and EU finalise a cooperation deal amid a tuition-fee dispute."),
    ("WASHINGTON —", "SpaceX hires Democratic lobbyists ahead of congressional inquiries."),
    ("TEHRAN —", "Iran officials debate a possible shift in nuclear doctrine."),
    ("HEBRON —", "Residents brace for demolition of permitted buildings in a Palestinian-controlled zone."),
    ("NOWA DEBA —", "Exercise Koalicja, with some 5,000 coalition troops, wraps up in south-east Poland."),
]
assert len(also) == 30, len(also)
f_lead = F(SANS_B, 9.5)
f_item = F(SANS, 9.5)
colw = (CW - 2 * gap) // 3
iy = ay + 26 * S
pos = [(ci, j - a) for ci, (a, b) in enumerate([(0, 10), (10, 20), (20, 30)])
       for j in range(a, b)]
for i, (lead, body) in enumerate(also):
    x = M + pos[i][0] * (colw + gap)
    y = iy + pos[i][1] * 23 * S
    d.text((x, y), "▪ " + lead, font=f_lead, fill=INK)
    lw = d.textlength("▪ " + lead + " ", font=f_lead)
    lines = wrap(body, f_item, colw - lw)
    d.text((x + lw, y), lines[0], font=f_item, fill=BODY)
    for j, ln in enumerate(lines[1:], 1):
        d.text((x, y + j * 11.5 * S), ln, font=f_item, fill=BODY)
    if len(lines) > 2:
        print("ALSO OVERFLOW", i, lead, len(lines), lines)

# ---------- footer ----------
fy = 987 * S
d.line([M, fy - 7 * S, W - M, fy - 7 * S], fill=INK, width=S)
f_foot = F(SANS, 9.5)
block(M, fy, CW,
      "DATE CHECK — every story on this page happened, or was first reported, "
      "on Sunday 22 November 2026, in some time zone. Claims are attributed, "
      "not stated as fact.", f_foot, GREY, 12 * S)
block(M, fy + 13 * S, CW,
      "Sources: Reuters, AP, AFP, ESPNcricinfo, European Commission, INDECI, "
      "MEA and news wires. Pictures: original illustrations. Page drawn in code.",
      f_foot, GREY, 12 * S)

page = page.resize((1024, 1024), Image.LANCZOS)
out = os.path.join(HERE, "entry.png")
page.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), "bytes")
