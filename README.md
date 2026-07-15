<div align="center">

# RPX — Formula 1 Race Companion

**Race-weekend context built on reproducible Formula 1 data.**

[![Live](https://img.shields.io/badge/live-f1.alphonsowoodbury.com-111?style=flat-square)](https://f1.alphonsowoodbury.com)
[![Validation](https://img.shields.io/github/actions/workflow/status/alphonsowoodbury/RPX/validate.yml?style=flat-square&label=data)](https://github.com/alphonsowoodbury/RPX/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-111?style=flat-square)](LICENSE)

</div>

RPX is a deployed Formula 1 companion by Alphonso Woodbury. It combines current race-weekend information from the Jolpica API with a reproducible historical dataset, original analysis, and browser-based 3D circuit geometry.

## What is shipped

| Capability | Evidence |
|---|---|
| Race hub | Next-race countdown, localized session schedule, standings, and recent results on the [live site](https://f1.alphonsowoodbury.com) |
| Historical dataset | One generated row per World Championship Grand Prix from 1950 through the current 2026 season |
| Analysis | Reproducible pole-position analysis and published methodology |
| Track explorer | Six circuits rendered from open WGS84 geometry with Three.js |
| Delivery | Static site deployed to Cloudflare Pages from `main` |

The repository also contains planning documents and placeholder directories for possible future work. Those files are explicitly marked **planned** and are not implemented capabilities.

## Current architecture

| Layer | Implementation |
|---|---|
| Interface | Static HTML, custom CSS, and vanilla JavaScript |
| Live context | Client-side requests to the Jolpica F1 API |
| Historical data | Python builders over Jolpica data, with generated CSV/JSON artifacts |
| 3D | Three.js with open circuit geometry projected to local coordinates |
| Delivery | GitHub Actions and Cloudflare Pages |

There is currently no production streaming platform, lakehouse, prediction model, LLM agent, or multi-cloud deployment.

## Repository map

```text
site/       deployed companion
data/       reproducible builders and generated datasets
analysis/   analysis scripts and reports
tests/      validation for committed data artifacts
docs/       design and architecture research, not shipped functionality
```

## Run locally

```bash
git clone https://github.com/alphonsowoodbury/RPX.git
cd RPX/site
python3 -m http.server 8000
```

## Validate the committed data

```bash
python3 -m unittest discover -s tests -v
```

## Rebuild data

The builders fetch public upstream data, so results may advance as the season progresses.

```bash
python3 data/build_grands_prix.py
python3 data/build_circuit_stats.py
python3 data/build_tracks.py
```

See [`data/README.md`](data/README.md) for definitions and caveats.

## Near-term roadmap

1. Add freshness and schema checks to every generated artifact.
2. Expand the track explorer while documenting geometry provenance.
3. Build one evaluated predictive question only after defining its baseline, split, and success metric.

Broader architecture explorations remain research until corresponding code, tests, and operational evidence exist. See [`ROADMAP.md`](ROADMAP.md).

## Data and credits

- Results, schedules, and standings: [Jolpica F1](https://github.com/jolpica/jolpica-f1)
- Circuit geometry: [f1-circuits](https://github.com/bacinger/f1-circuits)

## License

[MIT](LICENSE) © 2026 Alphonso Woodbury. Upstream data and geometry remain subject to their respective source terms.
