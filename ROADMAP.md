# RPX roadmap

This file separates deployed behavior from possible future work. An unchecked item is not a product capability and must not be described in present tense elsewhere.

## Shipped

- [x] Static race companion deployed on Cloudflare Pages
- [x] Historical Grand Prix dataset from 1950 through the current season
- [x] Pole-position analysis with a reproducible source table
- [x] Six-circuit Three.js explorer
- [x] Client-side current schedule, results, and standings
- [x] Automated deployment from `main`

## Next: strengthen what exists

- [ ] Validate committed CSV, JSON, and track artifacts in CI
- [ ] Record artifact generation time and upstream source version
- [ ] Add deterministic tests for published analysis figures
- [ ] Document geometry transformation and source licensing
- [ ] Improve API failure, stale-data, and offline states

## Later: one evaluated model

- [ ] Select one narrow predictive question
- [ ] Define a naive baseline before selecting a model
- [ ] Define time-aware train/validation/test splits
- [ ] Publish calibration and failure analysis with the result
- [ ] Serve the model only if it improves on the baseline

## Research archive

Documents and scaffold directories describing streaming, lakehouse, human-data, agent, safety, observability, and multi-cloud systems are architecture explorations. They are not scheduled commitments and are not evidence that those systems exist.

Any future phase must ship code, tests, reproducible evidence, and an updated status statement before the root README or public site describes it as implemented.
