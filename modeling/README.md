# Models — ML · RL · CV · more — RPX

> The full breadth of AI, not just an LLM. **Phase 4 → 5.** Status: planned.

F1 is a rich domain for many kinds of model. This layer deliberately spans the
spectrum — classical ML, time-series, reinforcement learning, computer vision,
unsupervised learning, anomaly detection, and embeddings — with an LLM as just
*one* head, behind a provider-agnostic gateway (see [`/app`](../app/)).

## Scope
- **Supervised ML** — race / qualifying outcome prediction; tyre-degradation
  regression. Gradient boosting (XGBoost/LightGBM) + calibration.
- **Time-series forecasting** — lap-time and gap-to-leader evolution, weather impact
  (statistical + sequence models).
- **Reinforcement learning** — a pit-strategy / race-line policy, *and* the RLHF
  loop: a **Bradley-Terry reward model** from [`/human-data`](../human-data/)
  preferences → policy optimization → eval.
- **Computer vision** — event/overtake detection or car detection from onboard /
  track imagery (builds on prior CV work).
- **Unsupervised** — driving-style and circuit-archetype clustering.
- **Anomaly detection** — telemetry / mechanical-failure signals (feeds [`/safety`](../safety/)).
- **Embeddings + vector search** — "similar laps/races" semantic retrieval (feeds the agent's RAG).

Every artifact is versioned and scored in [`/eval`](../eval/) — model choice is evidence-driven.

## Stack
`Python` · `scikit-learn` · `XGBoost`/`LightGBM` · `PyTorch` · RL (e.g., PPO) · time-series (`statsmodels`/`Prophet`) · `OpenCV`/`torchvision` · sentence embeddings + `Cloudflare Vectorize`

## Inputs → Outputs
- **In:** feature marts ([`/lakehouse`](../lakehouse/)), preference data ([`/human-data`](../human-data/)), imagery/telemetry.
- **Out:** trained models (predictive, RL, CV, anomaly, embeddings) — all evaluated in [`/eval`](../eval/).

---
*Part of the RPX platform.*
