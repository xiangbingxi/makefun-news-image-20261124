# THE WORLD IN ONE DAY — Tuesday, 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/xiangbingxi/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/xiangbingxi/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Built for make.fun's ["Sum up 24 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261124), $100 in USDC.

A single 1024×1024 hand-drawn flat-vector newspaper page covering 36 verified
news stories from one day: 3 big headlines, 10 illustrated small stories,
a world map with 13 numbered pins, and 23 numbered briefs (14–36).

## Files

- `entry.png` — the finished page (1024×1024, RGB, PNG, ≤ 1 MiB)
- `main.py` — entry point. Pure standard library. It only copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) after validating the
  PNG magic bytes, the 1 MiB size limit, every chunk CRC through IEND, and
  the 1024×1024 RGB header. It never renders anything.
- `tools/gen_image.py` — the development renderer (PIL, hand-written). Run it
  to rebuild `entry.png`: `python3 tools/gen_image.py`. It also runs the
  point-in-polygon check for all 13 pins and the land-pixel ring check.
- `NEWS.md` — all 36 stories in full, with sources, region counts and pins.
- `HANDOFF.md` — competition info, what is on the page, and the change log.
- `prompt.txt` — the user's original request, one line.
- `LICENSE` — MIT.

## What's on the page

- Top stories: 1 Huawei guilty (10 of 12 counts, Brooklyn jury), 2 Iran says
  four tankers hit mines in the Strait of Hormuz, 3 Houthi strike on a Riyadh
  tower, 11 hurt.
- Small stories 4–13: Ukraine hits Russian ships, Nvidia's Huang in therapy,
  China probes Chen Jining, Senegal regain AFCON title, Sanofi buys Insmed
  for $41bn, Turkish helicopter crash, Hanoi restaurant blast, Cartagena
  hostages, landmine toll at a five-year high, NATO vows to defend space.
- Map "WHERE IT HAPPENED": 13 pins — New York, Strait of Hormuz, Riyadh,
  Benghazi, Shanghai, Dakar, Paris, Eskisehir, Hanoi, Cartagena,
  Zaporizhzhia, Gaza City, Aden.
- Briefs 14–36, one line each, with follow-ups labelled in the item itself:
  Monday (15, 19, 20), Saturday (24), Sunday (34).
- Regions: Europe 9, North America 7, Asia 8, Middle East 5, Africa 4,
  South America 1, Global 2 — total 36.

## Notes

- Map drawn from public coastline data (Natural Earth 50m); all other
  illustrations are hand-drawn flat-vector art made with PIL. No
  photographs and no wire-service images are used.
- All figures are as reported on 24 Nov 2026, not later updates.
- Fonts: local DejaVu (DejaVuSans, DejaVuSans-Bold, DejaVuSerif-Bold).
  The judging machine has no font library, so `main.py` never renders —
  it only copies the pre-rendered `entry.png`.
