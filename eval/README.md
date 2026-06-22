# Evaluation & Experiment Tracking — RPX

> Did it actually get better? Measure, don't assert. **Phase 5.** Status: planned.

A reproducible evaluation harness over the predictions, the reward model, and the
agent, with experiment tracking and a leaderboard. This is the "Research Tools"
discipline — the thing that turns changes into evidence.

## Scope
- **Eval suites:** prediction accuracy/calibration; reward-model agreement vs held-out
  human judgments; agent task success on a fixed eval set.
- **Experiment tracking:** runs, params, metrics — comparable across versions.
- **Leaderboard:** every model/agent version ranked on the same tasks.

## Stack
`Python` · an eval framework · experiment tracking (e.g., Weights & Biases or MLflow)

## Inputs → Outputs
- **In:** artifacts from [`/modeling`](../modeling/) + the agent in [`/app`](../app/).
- **Out:** scored, tracked, comparable results — the basis for promoting anything.

---
*Part of the RPX platform.*
