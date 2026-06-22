# Ingestion · Batch — RPX

> Bulk historical ingestion over seventy years of F1 data. **Phase 1.** Status: planned.

Apache Spark jobs that read the full archive (Jolpica results/qualifying/schedules
1950–2026 + FastF1 lap data and car telemetry, ~2018+) and write partitioned,
analysis-ready tables to the lakehouse. This is the "raw Spark" story — a real
cluster, real partitioning, a real tuning pass — not managed/serverless Spark.

## Scope
- Extract from Jolpica (history) and FastF1 (lap/telemetry); land **bronze** (raw).
- Spark transforms → **silver** (clean, typed, deduped) → partitioned Parquet/Iceberg.
- Idempotent, re-runnable; multi-season **backfills** without duplication.
- A documented tuning story (partitioning, skew, shuffle, file sizing).

## Stack
`Apache Spark` · `Parquet` · `Apache Iceberg` · `Python` · runs on Dataproc or Spark-on-K8s

## Inputs → Outputs
- **In:** Jolpica API, FastF1 cache, object store (raw landing).
- **Out:** partitioned silver tables in the lakehouse (`/lakehouse`).

---
*Part of the RPX platform — orchestrated by [`/orchestration`](../../orchestration/), consumed by [`/lakehouse`](../../lakehouse/).*
