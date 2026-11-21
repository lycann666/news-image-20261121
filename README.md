# news-image-20261121 — THE WORLD TODAY

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/lycann666/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/lycann666/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the [make.fun bounty "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121).

## What it is

`main.py` draws a one-page newspaper front page — **THE WORLD TODAY**,
Saturday 21 November 2026 — entirely procedurally: a hand-written 5x7 bitmap
font, a pure-stdlib PNG encoder, and drawing code for the masthead, a cyclone
spiral over the Bay of Bengal, a map of Poland, a falling markets chart, the
Union Jack and the EU flag, a cricket scoreboard and a globe.
No images, fonts or data are read from disk and no network is used at
runtime, so the output is byte-identical on every run.

## The news on the page

- **Cyclone Akvan weakens over Odisha** — 440,000 moved to safety, no major
  damage, after landfall near Gopalpur
- **Missiles in Poland** — a day after Russian missiles came down, Warsaw
  seeks more allied cover; NATO calls it a grave violation
- **Wall Street slumps** — S&P 500 into correction, down 3.7% on Friday as
  AI shares slide
- **UK and EU sign three deals** — food, carbon and youth mobility, in
  Brussels
- **Rahul's century lifts India** — 344/2 at lunch on day 3 in Wellington,
  after New Zealand's 368 (Nicholls 175 not out)
- **COP31 climate talks in their final stage** in Turkey — fossil fuels and
  climate finance on the table
- Also: NSE now the world's 5th-largest exchange; Hyundai unveils the 2027
  Elantra at the Los Angeles Auto Show

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024 PNG, under 1 MiB, deterministic
```

Python 3, standard library only.

## License

MIT — see [LICENSE](LICENSE).
