# Infrastructure — RPX

> Everything reproducible from code. **Phase 1 → 2.** Status: planned.

Terraform + Kubernetes manifests that stand up the platform on **free-tier and
free-forever infrastructure** ($0/month target). The keystone is **Oracle Cloud
Always Free** (4 ARM cores / 24 GB) running a small **k3s** cluster for the
always-on services; BigQuery datasets and object stores live on free SaaS tiers;
the edge is Cloudflare. Multi-cloud by design — see [`/docs/infra-free-stack.md`](../docs/infra-free-stack.md). No click-ops.

## Scope
- **Terraform:** R2/S3/GCS buckets, BigQuery datasets, IAM, the k3s nodes.
- **Kubernetes (k3s) manifests:** Redpanda/Kafka, Flink, Airflow, Spark.
- Secrets management (never in repo); least-privilege service accounts.
- Cost controls + teardown so the bill stays at zero between race weekends.

## Stack
`Terraform` · `Kubernetes (k3s)` · `Oracle Cloud Always Free` · `Cloudflare` · `GCP (BigQuery)` · `GitHub Actions`

## Inputs → Outputs
- **In:** declarative config.
- **Out:** the running platform every other dir deploys onto.

---
*Part of the RPX platform — the substrate for [`/ingestion`](../ingestion/), [`/orchestration`](../orchestration/), [`/app`](../app/).*
