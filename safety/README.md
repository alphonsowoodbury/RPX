# Safety — RPX

> A classifier, shipped with the eval set that proves it works. **Phase 6.** Status: planned.

A classifier (anomaly detection on telemetry, or content/quality classification) built
the honest way: with a **labeled evaluation set** and real precision/recall reporting.
The "Safeguards" discipline — a classifier without its eval set is a guess.

## Scope
- A focused classifier with a clear task definition.
- A **labeled eval set** built with the [`/human-data`](../human-data/) tooling.
- Precision/recall/F1 reporting + threshold analysis; tracked in [`/eval`](../eval/).

## Stack
`Python` · `scikit-learn`/`PyTorch` · a labeled eval set · standard classification metrics

## Inputs → Outputs
- **In:** features/events from the marts; labels from [`/human-data`](../human-data/).
- **Out:** an evaluated classifier with honest, reported performance.

---
*Part of the RPX platform.*
