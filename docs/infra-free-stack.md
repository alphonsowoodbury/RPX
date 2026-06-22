# RPX — Free, Public, Multi-Vendor Infrastructure

*Rees Performance · the operating constraints, and the stack that satisfies them.*

Three constraints shape every infrastructure choice in RPX:

1. **Free.** Development, deployment, and operation run on free tiers and free-
   forever compute. Target: **$0/month**. (One small exception — the LLM API; see §5.)
2. **Public.** Public repo, public deployments, public writeups. Free tiers and
   "public" reinforce each other — GitHub Actions is effectively unlimited for
   public repos, and most SaaS free tiers are aimed at personal/open use.
3. **Multi-vendor by design.** Where a category has several real options, use a
   *different* vendor for each so the project covers the breadth of the market —
   a genuine, speakable comparison. **Deliberate, not scattered:** every tool
   earns a "I used this here *because*…".

> The $0, all-public, multi-cloud constraint is itself an engineering story —
> cost discipline and breadth, demonstrated, not claimed.

---

## 1. The free always-on backbone

Three providers carry almost everything:

- **Oracle Cloud Always Free** — the keystone. Up to **4 ARM (Ampere) cores +
  24 GB RAM**, free forever. Real always-on compute to self-host the heavy OSS
  that has no free SaaS tier: Redpanda/Kafka, Flink, Airflow, a small k3s cluster,
  lakeFS, Grafana/Prometheus.
- **GitHub Actions** — free and effectively unlimited for **public** repos.
  CI/CD + scheduled batch (Spark jobs, dbt, pipeline runs) on cron.
- **Cloudflare** — Pages (site + React app), Workers (edge API), R2 (object store,
  **no egress fees**), D1, Workers AI. Generous free tiers.

Between them: always-on services (Oracle), scheduled compute (Actions), and the
edge (Cloudflare) — none of it billed.

---

## 2. Layer → free stack → "also try" (the market coverage)

Primary = where the real build lives. "Also try" = a deliberate second vendor for
the same job, run far enough to compare and speak to.

| Layer | Primary (free) | Also try (free) — to cover the market | Why two |
|---|---|---|---|
| **Batch compute** | Spark on GitHub Actions / k3s | **Databricks Community Edition** (Spark + Delta Lake) | Self-managed vs managed Spark; Delta vs Iceberg |
| **Streaming bus** | **Redpanda** self-host (Kafka API) | **Confluent Cloud** free credits (managed Kafka) | Self-host vs managed; same Kafka API |
| **Stream processing** | **Apache Flink** | Spark Structured Streaming / Kafka Streams | Compare stateful-stream engines |
| **Orchestration** | **Apache Airflow** (Oracle VM) | **Dagster** *and* **Prefect** (both as real builds, free tiers) | The incumbent vs the two modern challengers |
| **Durable workflows** | **Temporal** (self-host; Temporal Cloud trial) | covered by orchestration | Durable execution vs DAG scheduling |
| **Warehouse** | **BigQuery** (10 GB + 1 TB query/mo, free) | **Snowflake** 30-day trial · **MotherDuck**/DuckDB | The three warehouse paradigms |
| **OLAP / serving store** | **ClickHouse** (self-host on Oracle; ClickHouse Cloud trial) | DuckDB / MotherDuck | Real-time analytical serving vs embedded OLAP |
| **Query engine** | **Trino** (self-host on k3s) | Starburst Galaxy free tier | Federated SQL across lakehouse + warehouse |
| **Lakehouse format** | **Apache Iceberg** on R2 | **Delta Lake** (via Databricks CE) | The two open table formats |
| **Object store** | **Cloudflare R2** (no egress) | **AWS S3** + **GCS** free tiers | Multi-cloud storage, real cross-cloud reads |
| **Dataset versioning** | **lakeFS** (self-host) or **DVC** (R2 remote) | **Hugging Face Datasets** (public hosting) | Git-for-data vs a public dataset hub |
| **Containers / K8s** | **k3s** on Oracle Always Free (free-forever, always-on) | **GKE** (GCP trial) · **AKS** (Azure trial) · Oracle OKE | Self-managed vs the managed K8s the market runs |
| **Frontend / serving** | **Cloudflare Pages + Workers** | — | (edge is the right single choice) |
| **Real-time push** | WebSocket server on Oracle VM | Cloudflare Durable Objects | Self-host vs edge-stateful |
| **Experiment tracking** | **Weights & Biases** (free, public) | self-host **MLflow** | SaaS vs self-managed |
| **Observability** | **Grafana Cloud** free + OpenTelemetry | self-host Prometheus/Grafana; Datadog trial | Managed vs self-host (Datadog = keep-warm) |
| **Search / vector** | **Cloudflare Vectorize** | **Elasticsearch** (self-host) | Vector search vs full-text + hybrid |
| **Relational (if needed)** | **Neon** or **Supabase** free Postgres | Cloudflare D1 (SQLite) | Serverless Postgres vs edge SQLite |
| **GPU (if ever needed)** | **Google Colab** / **Kaggle** free GPU | — | Models here are small; rarely needed |

---

## 3. Clouds genuinely touched

A real, defensible **five-cloud** footprint — not a buzzword. Use the free tier of
every major provider, with a hard line between *free-forever* and *trial credits*:

| Cloud | What for | Free model |
|---|---|---|
| **Oracle** | Always-on backbone (k3s, Redpanda, Flink, Airflow) | **Always Free** (forever) |
| **Cloudflare** | Edge: Pages, Workers, R2, D1, Workers AI | **Free tier** (forever) |
| **GCP** | BigQuery + GCS (free tier) · **GKE** (trial) · Colab | Free tier *forever* + **$300 / 90-day** trial for GKE |
| **AWS** | S3, Lambda, DynamoDB always-free *(keep-warm)* | 12-month + always-free |
| **Azure** | **AKS** + Blob storage *(optional breadth)* | **$200 / 30-day** trial |

> **The discipline that keeps the bill at $0:** anything that must run continuously
> (the streaming backbone, the site, the warehouse) lives on **free-forever**
> (Oracle, Cloudflare, BigQuery free tier, R2). Anything on **trial credits**
> (GKE, AKS, Snowflake) is a **time-boxed spike**: stand it up, build something
> real, capture the experience and the comparison, **tear it down** before the
> credits expire. Never architect an always-on dependency on expiring credits.

The marquee comparison this unlocks: **self-managed Kubernetes (k3s on Oracle,
free-forever) vs managed Kubernetes (GKE on GCP, then AKS on Azure)** — run the
same Flink streaming tier on each and you can speak to all three first-hand.

"Built across Oracle, Cloudflare, GCP, AWS, and Azure, with data and workloads
crossing cloud boundaries" is true and earned.

---

## 4. Where to spend the experimentation budget

You already have **AWS** and **Datadog** (résumé). Don't burn the "try new things"
budget re-proving those — keep them as light keep-warm touches. Aim the
experimentation at what's *new* for you and most-screened-for:

**Highest priority new ground:** Flink, Airflow, raw Spark, BigQuery, GCP,
Kubernetes (k3s), Dagster/Prefect, lakeFS/DVC, Weights & Biases, Grafana.
**Nice breadth touches:** Snowflake, Databricks CE + Delta, Confluent Cloud,
Hugging Face.

---

## 5. The LLM layer — AI-agnostic, near-$0

The agent (§`/app`) is the only piece that touches a paid API — so it's built
**provider-agnostic** behind an **LLM gateway**: one interface, model and provider
chosen by config. If pricing or availability changes, swapping is a config change,
not a rewrite.

- **Gateway:** **Cloudflare AI Gateway** (free; provider-agnostic proxy with
  caching, rate-limiting, observability) or self-hosted **LiteLLM** on the Oracle VM.
- **Default:** **Claude** — **Haiku 4.5** for routine calls, **Sonnet 4.6 / Opus
  4.8** for showcase/hard-reasoning paths. (Targeting Anthropic, using the Claude
  API well is itself a signal — and it's pennies at this volume.)
- **Swap-in on cost:** **Gemini** (Google AI Studio free tier) and **open models**
  via **Cloudflare Workers AI** (free daily allocation) or OpenRouter.
- Cache aggressively; gate live calls behind the deterministic rules engine so the
  LLM is the *interface*, not every computation.
- The [`/eval`](../eval/) harness scores models **across providers**, so model
  choice is evidence-driven — and the abstraction is itself a portability signal.

---

## 6. Honesty guardrails

- **"Built on" vs "evaluated."** Be precise: a tool you ran a real pipeline on is
  "built on"; a tool you spiked for comparison is "evaluated." Don't inflate a
  spike into production experience.
- **No tool soup.** Multi-vendor is a strength *only* when deliberate. If you can't
  say why a tool is there, it shouldn't be. Each "also try" needs a comparison you
  can actually articulate.
- **Free tiers drift.** Limits and trial terms change — verify current quotas
  before relying on one; prefer free-*forever* (Oracle, GitHub public, BigQuery
  free tier, R2) over time-boxed trials for anything always-on.

---

*Living doc. As each layer lands, record which vendor it actually ran on and the
comparison learned — that record is the interview answer.*
