# HANDOFF — news-image-20261124

## Competition

- Bounty: make.fun news image, 24 November 2026 edition ("THE WORLD IN ONE DAY").
- Deliverable: one 1024×1024 RGB PNG (≤ 1 MiB), produced by `main.py`
  copying the pre-rendered `entry.png`. No submission has been made from
  this repo; no GitHub repo or bundle was created here.

## What's in the image

- Header: "THE WORLD IN ONE DAY", "TUESDAY, 24 NOVEMBER 2026 · 36 STORIES, ONE DAY".
- 3 big headlines with hand-drawn illustrations: Huawei verdict (gavel +
  cracked phone + GUILTY stamp), Hormuz tankers (three burning tankers
  between cliffs + mine), Riyadh tower (smoking skyscraper + drone +
  ambulances).
- 10 small story cards (4–13), each with a small hand-drawn illustration.
- Map "WHERE IT HAPPENED" with 13 numbered red pins, equirectangular
  projection (lon −180…180, lat 75…−55), hand-written continent polygons.
- 23 numbered briefs (14–36), one line each: bold title + body.
- Region bars: Europe 9, North America 7, Asia 8, Middle East 5, Africa 4,
  South America 1, Global 2 (total 36).
- Footer: hand-drawn / no-photos note, source line (AP, Reuters, AFP,
  The Guardian, Al Jazeera, WSJ, SCMP, CNN, etc.), follow-up labelling note.

## Verification (all passed)

- `entry.png`: 1024×1024, RGB, ≤ 1 MiB, decodes fully with PIL.
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values: identical
  sha256 both times, matching the rendered file.
- Counts: 3 + 10 + 23 = 36 stories; region bars total 36; 13 pins.
- All 13 pins pass the point-in-polygon land check, and each pin has land
  pixels in its 9–16 px ring (checked by `tools/gen_image.py` on every run).

## Change log (fixes made after looking at the rendered image)

1. Five pins first landed on coastline boundaries (Hormuz, Benghazi,
   Shanghai, Cartagena, Gaza) — widened the Arabia, North Africa, China
   coast, South America north coast and Levant polygons until all 13 pins
   passed point-in-polygon.
2. Big illustrations spilled past their 62 px boxes into the headlines —
   redrew all three to fit inside the box (gavel handle, tanker hulls,
   tower base and ambulances shortened).
3. Header "No. 24" was clipped at the right edge — right-anchored it.
4. Headline bodies and small-story bodies ended mid-sentence after the
   auto-shortener dropped words — shortened the copy by hand so every
   sentence ends cleanly (e.g. story 13 now ends "…reports of a Russian
   satellite.").
5. Two-line small-story titles (11, 12, 13) pushed body text past the card
   bottom — shortened those titles to one line and added a guard: a
   two-line title only gets one body line.
6. Middle-East pin numbers overlapped — gave pins 8, 11, 12, 2 and 3
   individual label offsets.
7. "TOTAL 36 STORIES" was clipped by the region panel border — tightened
   the region rows so it fits inside the panel.
8. `main.py`: first version validated magic, size and chunk CRCs; second
   write added the trailing-data-after-IEND check and the IHDR
   1024×1024 RGB check.
9. Pin 4 (Benghazi) label was half-covered by a neighbouring red pin
   marker at 2x zoom — split pin drawing into two passes (all 13 markers
   first, all 13 number labels last) and gave every label a white halo
   (`stroke_width=2`, white), so all 13 numbers sit on top of the markers
   and read fully. No label offsets, copy or numbers changed.
10. User review (13:20): (a) headline 2 title changed to "2  IRAN SAYS FOUR
    TANKERS HIT MINES IN STRAIT OF HORMUZ" (measured: still wraps to 2
    lines at FB(13), no font change); (b) story 4 body rewritten with both
    attributions — "Ukraine said drones sank Merkury off Benghazi; Libya
    said damaged, not sunk." (76 chars, wraps to exactly 2 lines at FR(9);
    the longer "badly damaged" variant wrapped to 3 lines and was rejected);
    (c) map pins renumbered to the story numbers — 1, 2, 3, 4, 6, 7, 8, 9,
    10, 11, 14, 30, 31 (stories 5, 12, 13 have no pin); label offsets
    followed their locations (now keyed 9, 14, 30, 2, 3). Verified at 2x
    zoom: all 13 numbers fully readable, Middle East cluster clear, Hanoi
    "10" sits clear of the Shanghai marker. NEWS.md pin table updated to
    the new numbering.
