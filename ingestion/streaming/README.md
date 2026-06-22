# Ingestion · Streaming — RPX

> Real-time telemetry ingestion during live sessions. **Phase 2 — the showpiece.** Status: planned.

The rarest, highest-value tier: the OpenF1 live feed becomes a genuine event stream,
processed statefully in real time. Run it **during an actual race weekend** so the
reliability story (lag, backpressure, replay) is observed, not assumed.

## Scope
- **Producer:** OpenF1 live (car telemetry, positions, intervals, weather) → Kafka topics.
- **Flink** stateful job, keyed by driver: rolling gap-to-leader, sector deltas,
  tyre-degradation curves, pit-window prediction.
- Windowing · keyed state · checkpointed recovery · **exactly-once** sink.
- Dual sink: BigQuery (analytics) + WebSocket fan-out (the live dashboard).

## Stack
`Apache Kafka` (or Redpanda) · `Apache Flink` · `Kubernetes (GKE)` · `Python/Java`

## Inputs → Outputs
- **In:** OpenF1 live feed.
- **Out:** Kafka topics → live feature stream → BigQuery + WebSocket (`/app`).

---
*Part of the RPX platform — deployed via [`/infra`](../../infra/), surfaced by [`/app`](../../app/).*
