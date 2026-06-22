# Orchestration — RPX

> The scheduler that runs everything, in order, reliably. **Phase 1.** Status: planned.

Apache Airflow DAGs that wire the platform together: pull new session data, run the
Spark jobs, build the dbt marts, run the data-quality gates, and trigger a redeploy.
Backfills and retries are the point — this is where reliability is engineered.

## Scope
- DAG: post-session pull → Spark feature jobs → load → dbt → Great Expectations → redeploy.
- **Backfills** across 77 seasons; idempotent tasks; retry + alerting on failure.
- Documented run history / lineage for observability.

## Stack
`Apache Airflow` · `Python` · runs on Kubernetes (see [`/infra`](../infra/))

## Inputs → Outputs
- **In:** schedules + upstream/downstream task dependencies.
- **Out:** orchestrated runs of [`/ingestion`](../ingestion/) and [`/lakehouse`](../lakehouse/).

---
*Part of the RPX platform.*
