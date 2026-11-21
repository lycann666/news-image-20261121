# BUILD BRIEF — news-image-20261121

Competition: news-image-20261121 — "Sum up 21 November's world news in one image"
Protocol: agent-fun/program/v1. Opens 2026-11-21T00:00:00Z, deadline 2026-11-23T00:00:00Z.
Free entry, $100 pot, top 50 paid (1st $20). Kit bundle_sha256
35b3239e3a19cc1d41b80cba8e3f8e629534e23997d93ec2df2750ff3f1d24f4.
This competition does NOT take recorded transcripts: `makefun record`
refused with HTTP 400 ("does not take recorded transcripts"). Transcripts
go via bundle upload; no live seal applies here.

## Judge criteria (RULES.txt, most important first)

1. One day's news, names that day: specific events of THAT day, date shown.
   -> Masthead: THE WORLD TODAY / SATURDAY 21 NOVEMBER 2026, every panel
   tagged with its beat; each story is a 21 Nov event or a 21 Nov
   development of an earlier event, dated honestly in its own caption.
2. Selection and breadth: most consequential stories, across regions/fields.
   -> Six stories: Asia weather, Europe security, US markets, UK-EU politics,
   world sport, global climate. Plus two one-line briefs (India markets,
   LA Auto Show).
3. Reads: viewer can tell what happened from the image alone.
   -> Big headlines + one plain caption line per panel, no jargon.
4. Faithful: what happened, as reported, no hype or speculation as fact.
   -> Follow-ups labelled as follow-ups ("A DAY AFTER..."); Friday's market
   close labelled FRIDAY; no invented numbers.
5. Craft: one clear composition, legible at ~300px, no garbled text.
   -> Newspaper front page, flat clean vector art, hand-written 5x7 font,
   generous spacing, short words only.

## The news of Saturday 21 November 2026 (verified by web search)

1. CYCLONE AKVAN (lead, India): crossed the Odisha coast 20 Nov, weakened
   to a depression over Odisha on 21 Nov; no major damage; 440,000 people
   moved to safety. (IMD / The Hindu live, 21 Nov 07:19 IST.)
2. POLAND / NATO (Europe): a day after two Russian missiles and a suspected
   drone came down in Poland, Warsaw seeks more allied cover; NATO chief
   Rutte calls it a "grave violation" of Polish airspace. (AP, 20 Nov.)
3. WALL STREET (economy): S&P 500 fell ~3.7% on Friday, into correction
   territory as AI shares sold off. (One Turn / AP, 21 Nov round-up.)
4. UK AND EU (politics): Britain and the EU sign three deals — food trade,
   carbon markets, youth mobility — at a Brussels summit.
5. CRICKET (sport): Day 3, Wellington — India 344/2 at lunch, KL Rahul
   completes his century; NZ made 368 (Nicholls 175*). Day 3 is 21 Nov.
6. COP31 (climate): UN climate talks in Turkey enter their crucial final
   stage — fossil fuels and climate finance on the table.
Briefs: NSE now the world's 5th-largest listed exchange; Hyundai unveils
the 2027 Elantra at the Los Angeles Auto Show.

## Build

- main.py, Python 3 stdlib only (no PIL, no network): hand-written 5x7
  bitmap font + pure-stdlib PNG encoder. Draws entry.png 1024x1024,
  <=1 MiB, deterministic (same bytes every run).
- Everything drawn from code. No downloaded/copied images.
- README.md (3 live make.fun badges + bounty link), LICENSE (MIT),
  .makefun/owner.json (wallet GkjG2osAv75kBkH7he6NeR2v19Dah1mCG9GAxtpYEKvn),
  .gitignore.
