# Lakehouse & Datasets — RPX

> The warehouse, the transforms, and training-ready datasets. **Phase 1 → 4.** Status: planned.

Where clean data becomes useful. dbt builds tested, lineage-tracked marts in
BigQuery; the dataset layer adds versioning, dedup/quality filtering, and shards a
model trainer can actually load. This is the "Research Data Platform" core.

## Scope
- **dbt** project: silver → gold marts, with tests + documented lineage. *(Phase 1)*
- **Great Expectations** data-quality gates (row counts, freshness, key integrity).
- **Dataset versioning** (lakeFS / DVC), dedup + quality filtering, tokenization. *(Phase 4)*
- **Data loaders** that stream training shards downstream.

## Stack
`dbt` · `BigQuery` · `Apache Iceberg` · `Parquet` · `Great Expectations` · `lakeFS`/`DVC`

## Inputs → Outputs
- **In:** silver tables from [`/ingestion`](../ingestion/).
- **Out:** gold marts (BigQuery) + versioned, training-ready datasets for [`/modeling`](../modeling/).

---
*Part of the RPX platform — orchestrated by [`/orchestration`](../orchestration/).*
