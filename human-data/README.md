# Human Data — "F1 Judgments" — RPX

> Collecting human preference, the right way. **Phase 4.** Status: planned.

A faithful miniature of an RLHF data pipeline. People judge **preference pairs** —
which overtake was better, which strategy call smarter, driver-of-the-day — and the
output is a clean preference dataset with the quality machinery a real labeling
operation needs. This is the Human Data Interface skill set, in F1.

## Scope
- **Annotation tool** (built in the [`/app`](../app/) React stack): pairwise judgments.
- **Preference dataset** with provenance + per-annotator records.
- **Inter-annotator agreement** (Krippendorff's α); spam/quality review dashboard.
- **Versioned guidelines** — judgments are tied to the guideline version in force.

## Stack
`React`/`TypeScript` (UI) · `Python` (pipeline) · preference-data schema · agreement metrics

## Inputs → Outputs
- **In:** candidate events/clips from the marts ([`/lakehouse`](../lakehouse/)).
- **Out:** a versioned preference dataset for the reward model in [`/modeling`](../modeling/).

---
*Part of the RPX platform.*
