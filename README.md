[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/bal-mond/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/bal-mond/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Sum up 23 November's world news in one image

A one-page newspaper poster for **Monday 23 November 2026**: 31 stories
across war and diplomacy, the Americas and markets, and science, sport
and culture — led by the collapse of the COP31 climate talks in Antalya,
Iran's strike on a civilian site in Bahrain, and Ukraine's claimed
sinking of a Russian corvette at Benghazi. Every story was verified
against news reported on 23 November 2026 (Just Security, Algenom,
Shadow, World Watch, The Edge, GenFlow, Off the Wire, Gizmodo, AP,
The Register, LiveScore, DAZN and others); nothing was invented, and
claims are phrased as reported ("says", "reportedly").

## Why copy-only

The 22 November entry taught us the pattern: a version that rendered its
poster with Pillow at grade time failed in the grader, while the
copy-only version graded fine (v3: 97.72%). So `main.py` here does no
rendering at all — standard library only, no fonts, no network. It
copies the pre-rendered `entry.png` (1024×1024, rendered and verified at
build time with Pillow) byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`,
then verifies the copy (exists, size ≤ 1 MiB, PNG magic bytes,
1024×1024 read from the IHDR chunk, sha256 identical to the source)
and exits non-zero with a clear stderr message on any failure.

## How the poster was built

- Researched the day's news via web search on 23 November 2026 and
  kept only stories verifiable from that day's reporting.
- Rendered at build time with a Pillow script (`render_poster.py`):
  masthead with the date, three lead stories, three section columns,
  a small pictogram drawn with PIL primitives beside every story, and
  a headline ticker at the foot. No photos or downloaded artwork —
  every pixel is drawn by the build script.
- Viewed the finished poster at full size and at ~300 px across to
  confirm the text stays legible and nothing is garbled.

## Verification (local, Python 3.12 — stdlib-only code, so behaviour is
identical on the grader's Python 3.13)

- `entry.png`: 1024×1024, 235,965 bytes
- sha256: `a66a6082a67419265df1f9c961be3b71f6e75dac1213a5afd9a2eaa4e2517030`
- `main.py` run twice into fresh output dirs: byte-identical outputs,
  same sha256 as above
- No Pillow/network imports in `main.py` (grep for PIL/socket/urllib/
  requests/http/subprocess: no matches)
