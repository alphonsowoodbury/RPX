<div align="center">

# RPX — Formula 1 Race Companion

**A fast, race-day Formula 1 companion — and an open portfolio of the engineering behind it.**

[![Live](https://img.shields.io/badge/live-f1.alphonsowoodbury.com-111?style=flat-square)](https://f1.alphonsowoodbury.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-111?style=flat-square)](LICENSE)
[![Data](https://img.shields.io/badge/data-1950–2026-111?style=flat-square)](data/)

</div>

---

**RPX** (Rees Performance) is a Formula 1 project by **Alphonso Woodbury**: a product
you open *while watching a Grand Prix*, built on a reproducible data platform spanning
every World Championship race since 1950. It's where an F1 obsession meets software,
data, AI, and design — and the whole thing is built in the open.

> The deployed site is the centerpiece, but this repository is the portfolio: the data
> pipeline, the analysis, the 3D work, and the architecture that ties it together.

## Highlights

- **🏁 Race Hub** — the next Grand Prix with a live countdown, the full session schedule
  auto-converted to your timezone, the circuit and its pole→win history, championship
  snapshots, and last-race results. Live from the [Jolpica F1 API](https://github.com/jolpica/jolpica-f1).
- **📊 70+ years of data** — every Grand Prix from 1950–2026 (**1,156 races**, 77 seasons)
  in one clean, reproducible dataset of winners and pole positions.
- **🌐 3D Track Explorer** — six circuits rendered from real geometry with Three.js
  (orbit, zoom, switch). Built from open WGS84 circuit data projected to local meters.
- **🔎 Insights** — data-driven analysis, starting with *The Pole Position Premium*
  (pole converts to a win 43.5% of the time — but that's nearly doubled since the 1980s).
- **🎨 Monochrome design system** — custom, dependency-free CSS; a telemetry-inspired aesthetic.

## Tech

| Layer | Stack |
|---|---|
| Frontend | Static HTML / CSS / vanilla JS · zero build step · Three.js (3D) via CDN |
| Data | Python (pandas) pipelines over the Jolpica F1 API + open circuit geometry |
| Live data | Fetched client-side from the Jolpica API (results, schedule, standings) |
| Target architecture | Edge-serverless (Cloudflare) with real-time live timing & an AI layer on the roadmap — see [`docs/`](docs/) |

## Repository layout

```
.
├── site/                  # the deployed companion (static, no build step)
│   ├── index.html         #   Race Hub (home)
│   ├── standings.html     #   championships
│   ├── insights/          #   analysis articles
│   ├── tracks/            #   3D Track Explorer (Three.js)
│   ├── about.html         #   who + how it's built
│   └── assets/style.css   #   monochrome design system
├── data/                  # data pipelines
│   ├── build_grands_prix.py    #   the 1950–2026 dataset
│   ├── build_circuit_stats.py  #   per-circuit pole→win stats
│   ├── build_tracks.py         #   3D circuit geometry
│   └── grands_prix.csv         #   the dataset
├── analysis/              # analysis scripts + generated reports
└── docs/                  # product plan, architecture, design exploration
```

## Run it locally

```bash
git clone https://github.com/alphonsowoodbury/RPX.git
cd RPX/site
python3 -m http.server 8000
# open http://localhost:8000
```

The site is fully static and fetches live race data in the browser — no backend required.

## Rebuild the data

```bash
cd data
python3 build_grands_prix.py     # every GP 1950–2026  → grands_prix.csv (+ sqlite)
python3 build_circuit_stats.py   # per-circuit pole→win → site/data/circuit_stats.json
python3 build_tracks.py          # 3D circuit geometry  → site/tracks/data/*.json
```

## Roadmap

- **Real-time live timing** — lap-by-lap during a session (OpenF1 + WebSockets / Durable Objects)
- **Race predictions** — a model forecasting qualifying, podium, and upsets
- **3D telemetry** — elevation and ghost-car replays from real lap data
- **AI layer** — natural-language queries over the data, backed by a deterministic rules engine

## Data & credits

- Race results, schedules, and standings — [Jolpica F1 API](https://github.com/jolpica/jolpica-f1) (the Ergast successor)
- Circuit geometry — the open [f1-circuits](https://github.com/bacinger/f1-circuits) dataset

## License

[MIT](LICENSE) © 2026 Alphonso Woodbury

<div align="center">
<sub>Built by <a href="https://alphonsowoodbury.com">Alphonso Woodbury</a> · a subsite of alphonsowoodbury.com</sub>
</div>
