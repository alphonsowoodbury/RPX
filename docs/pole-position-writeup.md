# The Pole Position Premium — write-up

*Rees Performance · RPX · 2026-06-15*

A quick narrative pass on the first RPX analysis. Full tables live in
`/Volumes/F1/analysis/grands_prix_overview.md`; the public version is
`/Volumes/F1/site/work/pole-position.html`.

## The question
Across every F1 World Championship Grand Prix ever run (1,156 races, 1950–2026),
**how often does the pole sitter win?**

## The headline
**43.5% overall** — but the all-time average hides the real finding. Pole-to-win
conversion has **more than doubled** across the modern era:

- 1980s: **28.2%** (the low point)
- 1990s: 42.6%
- 2000s: 48.9%
- 2010s: 49.5%
- 2020s: **58.0%**

This is the fingerprint of modern F1: wider cars, dirtier aero, and qualifying-mode
engine specialness have made overtaking harder and Saturday more decisive. **Track
position is king, more than ever.**

## The people
- **Hamilton** leads everything raw — **107 poles and 106 wins**, more of each than
  anyone in history.
- **Verstappen is the greatest closer on record**: **78.4%** pole→win conversion
  (40 of 51) among drivers with 15+ poles — clear of Alonso (60.9%), Schumacher
  (58.0%), and Hamilton (57.9%). When Max starts first, it's effectively over.
- **Ferrari** is the deepest well: 249 wins, 250 poles.

## The places (min 15 races)
- **Pole is gold:** Yas Marina (70.6%), Marina Bay/Singapore (68.8%),
  Barcelona (66.7%), Shanghai (63.2%) — modern, low-overtaking layouts.
- **Pole means least:** Monza (33.3%), Silverstone (38.3%), Spa (39.7%),
  Hungaroring (37.5%) — slipstreams and chaos. Monza over 75 races is the purest case.

## Honesty / caveats
- Separate qualifying classification only exists from **2003**; earlier "pole" =
  who started P1 (`poleSource` flags each row).
- The 1950–60 Indy 500s were championship rounds with a different qualifying format
  and slightly drag down the early-era numbers.

## So what (next)
The pole-premium trend is the seed of a **predictive** angle: if track position is
this decisive in the current era, qualifying becomes the dominant feature for
forecasting race winners — exactly the model RPX will build next.
