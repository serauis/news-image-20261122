# Sunday 22 November 2026 — The World in One Day

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/serauis/news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/serauis/news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122)

One 1024×1024 newspaper front page summing up the world's news of
Sunday 22 November 2026: **39 sourced stories across 7 regions** —
3 illustrated heroes, 6 pictured tiles, and 30 ALSO items — plus a
stats strip, a UTC timeline, and a date-check footer.

## The day on the page

- **COP31 nears a deal at dawn** — after talks ran through Saturday
  night, a new package went to a late-night plenary in Antalya, with
  objections due by 03:00 GMT and an approval session at 06:00 GMT.
- **Pant's 128 puts India 261 ahead** — day four in Wellington,
  India 629-6 at lunch, Pant past McCullum for career sixes.
- **Gulf strikes hit US bases in Bahrain** — the IRGC says it hit
  two US positions; Bahrain reports a fire at an industrial facility
  and no injuries.

Tiles cover Nepal's PM landing in Delhi for his first state visit,
Verstappen on pole for the Las Vegas Grand Prix, France's sixth
weekend of cost-of-living marches, Peru's revised quake toll, the
Bayelsa boat toll rising to 24, and the EU–Indonesia trade deals.

## How it is built

`build_v1.py` composes `entry.png` from two fresh, original
illustration sheets (a 3-panel hero triptych and a 4×3 sprite sheet)
with Pillow — no photographs, no copied artwork. `main.py` copies
`entry.png` to `/output/entry.png`; it is deterministic and standard
library only. `SOURCES.md` documents every story with its source
and why its date is 22 November 2026.

## Verification

- `entry.png`: 1024×1024, 834,842 bytes (limit 1,048,576).
- `build_v1.py` run three times: identical sha256 each run.
- `main.py` run twice to separate output dirs: byte-identical output.
- Page read visually: no overflow, overlap, or garbled text.
