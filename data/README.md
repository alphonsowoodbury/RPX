# F1 Grands Prix Dataset (v1)

**Project:** Rees Performance — RPX F1 platform (foundation dataset)
**Built:** 2026-06-15
**Source:** [Jolpica F1 API](https://api.jolpi.ca/) (Ergast-compatible successor)
**Scope:** Every F1 World Championship Grand Prix, 1950 → the generated 2026 snapshot (77 seasons, 1,156 races)

## Files
- `grands_prix.csv` — one row per Grand Prix (the analysis table)
- `build_grands_prix.py` — reproducible builder (caches raw JSON in `raw/`)
- `raw/` — local cached API responses when the builder is run; not committed

## Columns
| column | meaning |
|---|---|
| season, round | championship season + race number |
| date, raceName | race date and official name |
| circuitId, circuitName, country, locality, lat, long | venue |
| winnerDriverId, winnerDriver, winnerNationality | race winner |
| winnerConstructorId, winnerConstructor | winning car/team |
| winnerGrid | grid slot the winner started from |
| poleDriverId, poleDriver, poleConstructor | pole / qualifying P1 |
| poleSource | `qualifying` (true quali, 2003+) or `grid` (started P1, pre-2003) |
| poleWon | did the pole sitter win? (null if pole unknown) |

## Known caveats (v1)
- **Pole before 2003** is derived from *grid position 1* (actual starting front-row),
  which is the pole sitter except in rare grid-penalty cases. True qualifying
  classification is only fully available from 2003 onward (`poleSource` flags which).
- 2026 season is in progress; the committed artifact reflects its generation date and must not be treated as a final season total.
- Includes the Indianapolis 500 (part of the championship 1950–1960).

## Headline stat
**43.5%** of all Grands Prix were won from pole position.
