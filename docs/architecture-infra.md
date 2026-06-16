# RPX — Architecture & Infrastructure

*Rees Performance · f1.alphonsowoodbury.com · 2026-06-15*

**Purpose.** Map the full system we *could* build — every layer, the real data
sources (including **real-time**), the stack options with honest trade-offs, and a
scope tiered from "lean weekend project" to "live-timing + AI platform." Nothing
decided; this is the scope menu. Written to learn from.

> **The strategic fork up front.** Two philosophies pull in different directions:
> - **Cheapest + most elegant** → a serverless, edge-native stack (Cloudflare).
>   Tiny cost, fast, real-time capable, distinctive.
> - **Most industry-standard** → the "enterprise data" stack (Kafka, Postgres,
>   dbt, an orchestrator, containers, a cloud) — the toolset top motorsport data
>   teams actually run.
>
> The pragmatic answer is a **hybrid**: ship the site on the edge stack, but build
> *one* pipeline the enterprise way for a genuine streaming/orchestration story.
> Flagged again at the end.

---

## 1. The layers (reference map)

```
                          ┌─────────────────────────────────────────┐
   SOURCES                │  Jolpica (results/schedule)  · FastF1     │
                          │  OpenF1 (LIVE telemetry/timing) · Weather │
                          └───────────────┬───────────────────────────┘
                                          │  ingest (batch + stream)
                          ┌───────────────▼───────────────────────────┐
   DATA PIPELINES         │  extract → validate → transform → load     │
   (orchestrated)         │  bronze (raw) → silver (clean) → gold (marts)│
                          └───────────────┬───────────────────────────┘
                          ┌───────────────▼───────────────────────────┐
   STORAGE                │  object store (parquet) · SQL (results)    │
                          │  time-series (telemetry) · vector (AI)     │
                          └───────────────┬───────────────────────────┘
              ┌───────────────────────────┼───────────────────────────┐
   AI / ML    │  predictions model        │   ANALYTICS  · metrics     │
   & ANALYTICS│  LLM + RAG (NL queries)   │   notebooks · dashboards   │
              │  deterministic rules engine│                           │
              └───────────────┬───────────┴───────────────────────────┘
                          ┌───▼────────────────────────────────────────┐
   BACKEND / API          │  REST/GraphQL · WebSockets (live) · cache  │
                          └───────────────┬───────────────────────────┘
                          ┌───────────────▼───────────────────────────┐
   FRONTEND / UI          │  the site · data viz · live timing · 3D    │
                          └───────────────────────────────────────────┘

   CROSS-CUTTING:  orchestration · observability · data quality ·
                   security/secrets · CI-CD · IaC · cost control
```

---

## 2. Data sources (the "real data" question)

| Source | What it gives | Real-time? | Notes |
|---|---|---|---|
| **Jolpica-F1** | Results, schedules, qualifying, standings (1950–now) | No (post-session) | Ergast successor; what we already use. The historical spine. |
| **FastF1** (Python) | Detailed timing, lap data, **car telemetry**, tyre/stint, weather | Mostly post-session (has a live client) | Telemetry coverage ~2018+. The richest analysis source. |
| **OpenF1** (openf1.org) | **Live** car telemetry, positions, intervals, pit, team radio, race control, weather | **Yes** — near-real-time during sessions (seconds–minutes delay) | The real-time enabler. Free, open. Also has full historical. |
| **Weather APIs** | Forecasts/conditions per circuit | Yes | Feature for predictions; OpenF1 also carries trackside weather. |

**Takeaway:** historical depth is solved. Real-time is *feasible* and cheap via
OpenF1 — the main cost is engineering, not access.

---

## 3. Layer-by-layer: options, recommendation, what it teaches

### 3.1 Frontend / UI
- **Now:** static HTML/CSS (already shipped).
- **Options:** stay static (+ vanilla JS / D3 for viz) · a framework (Astro for
  content-heavy + islands, or SvelteKit/Next for app-like) · WebGL (Three.js) for 3D tracks.
- **Recommend:** **Astro** when we outgrow hand-HTML — it keeps the static speed,
  adds components and data-driven pages, and ships zero JS by default ("islands"
  for interactivity only where needed).
- **Teaches:** component architecture, islands/partial hydration, data viz, SSR vs SSG.

### 3.2 Backend / API
- **Purpose:** serve data + predictions to the UI; handle live connections.
- **Options:** serverless functions (Cloudflare Workers / AWS Lambda) · a server
  (FastAPI/Node) · static JSON files (no backend) for read-only data.
- **API styles:** **REST** (simple, cache-friendly) · **GraphQL** (flexible queries)
  · **WebSockets/SSE** for live push.
- **Recommend:** start with **pre-baked JSON + a thin Workers API**; add WebSockets
  only for live timing.
- **Teaches:** API design, caching/CDN, serverless, statelessness, rate limiting.

### 3.3 Data pipelines (ingestion + transformation)
- **Pattern:** **medallion / bronze-silver-gold** — land raw, clean, then build
  analysis-ready "marts." **ELT** (load then transform) over ETL for flexibility.
- **Batch:** scheduled pulls (Jolpica/FastF1 after each session).
- **Stream:** OpenF1 during sessions → a queue → consumers.
- **Tools to know:** **dlt** (extract/load), **dbt** (SQL transforms + tests/lineage),
  an orchestrator below.
- **Teaches:** idempotency, incremental loads, schema evolution, data contracts, ELT.

### 3.4 Orchestration & scheduling
- **Options:** cron (simplest) · **GitHub Actions** (free cron + CI) · **Dagster**
  / **Prefect** / **Airflow** (real DAG orchestration, retries, backfills, lineage).
- **Recommend:** GitHub Actions or **Cloudflare Cron Triggers** for batch now;
  stand up **Dagster** for *one* pipeline as the "I can orchestrate" portfolio piece.
- **Teaches:** DAGs, dependencies, retries/backfills, observability of pipelines.

### 3.5 Storage
- **Object store** (raw + parquet): **Cloudflare R2** (S3-compatible, no egress fees) or S3.
- **SQL** (results/marts): **DuckDB** (analytics, embeddable, blazing on parquet) ·
  **Cloudflare D1** (serverless SQLite for the API) · **Postgres** (if we go enterprise).
- **Time-series** (telemetry): parquet partitioned by session, or a TSDB (TimescaleDB).
- **Vector** (AI/RAG): **Cloudflare Vectorize** / pgvector.
- **Recommend:** R2 (raw+parquet) + DuckDB (analysis) + D1 (serve). Add Vectorize for AI.
- **Teaches:** lakehouse vs warehouse, columnar formats, partitioning, OLAP vs OLTP.

### 3.6 Real-time / streaming (the ambitious bit)
- **Flow:** OpenF1 live → ingest Worker → **queue** (Cloudflare Queues / Kafka /
  Redpanda) → **Durable Object** per session holds live state → **WebSocket** push to UI.
- **Cloudflare Durable Objects** are *purpose-built* for this: one stateful object
  per live session, fan-out to many connected browsers. (There's a skill for it.)
- **Enterprise variant:** **Kafka/Redpanda** topics + a stream processor (Flink/
  Faust) — heavier, but the industry-standard streaming skill set.
- **Teaches:** stream processing, backpressure, stateful coordination, WebSockets,
  exactly-once vs at-least-once.

### 3.7 AI / ML / Analytics
Three distinct sub-systems:
1. **Predictions model** — features from history (form, track type, pole→win by
   circuit, team pace, weather) → probabilities per race. Start simple
   (logistic regression / gradient boosting), serve outputs as static JSON per weekend.
   *Teaches:* feature engineering, train/test, calibration, model serving.
2. **LLM + RAG layer** — natural-language questions over our data ("which circuits
   suit a strong qualifier?"). Embeddings → Vectorize → retrieve → answer. Ties to
   your agent vision (Alpha/AgentContext/etc.).
   *Teaches:* RAG, embeddings, prompt design, tool-use, eval.
3. **Deterministic rules engine** — your stated differentiator (FIA-style
   auditability): rules/calculations that are exact and traceable, with the LLM as
   the *interface*, not the source of truth. This is the credibility core.
   *Teaches:* deterministic vs probabilistic design, auditability, hybrid AI systems.

### 3.8 Cross-cutting
- **Observability:** structured logs, metrics, tracing; pipeline run history.
- **Data quality:** tests in dbt / **Great Expectations** — assert row counts,
  freshness, no nulls in keys. (A "race didn't load" alert.)
- **Security/secrets:** API keys in a secrets store (never in repo); least privilege.
- **CI/CD:** GitHub Actions — test + deploy site and pipelines on push.
- **IaC:** **Terraform** / **Pulumi** / **Wrangler** config — infra as code, reproducible.
- **Cost:** edge/serverless + free tiers keep this near-$0 until real scale.

---

## 4. Stack archetypes (pick a philosophy)

**A. Edge-serverless (Cloudflare) — recommended for the site.**
Pages (site) · Workers (API) · R2 (storage) · D1 (SQL) · Queues (stream) ·
Durable Objects (live timing) · Workers AI + Vectorize (AI) · Cron Triggers
(schedule) · Workflows (orchestration) · Agents SDK (the agent).
*Pros:* cheap, fast, real-time ready, one platform, distinctive. *Cons:* less
"enterprise-stack" signal; some lock-in.

**B. Modern data stack — best for analytics learning.**
dlt + DuckDB/MotherDuck + dbt + Dagster + Evidence/Streamlit dashboards.
*Pros:* current best-practice analytics; great dbt/orchestration story. *Cons:*
more moving parts; not built for real-time UI.

**C. Enterprise / streaming — industry standard.**
Postgres + FastAPI + **Kafka/Redpanda** + Flink + Airflow + Docker/**Kubernetes**
+ GCP/AWS.
*Pros:* the toolset top motorsport data teams run (Kafka, K8s, GCP). *Cons:*
heaviest, costs real money, overkill for a hobby site.

**Recommended blend:** **A for the product**, borrow **B's dbt + Dagster** for the
transformation/orchestration story, and build **one C-style streaming pipeline**
(Kafka/Redpanda) as the standout engineering centerpiece.

---

## 5. Scope tiers (how far to take it)

**Tier 0 — where we are.** Static site, one-off Python pull, CSV/SQLite.

**Tier 1 — Lean real-data platform.**
Scheduled batch (Jolpica + FastF1) → R2 parquet → DuckDB marts → JSON → static/Astro
site. dbt transforms, GitHub Actions cron, data-quality tests. *Real, fresh,
reproducible data. Cheap. ~weeks.*

**Tier 2 — API + richer analysis.**
Workers API over D1, predictions model serving JSON, more analyses, basic dashboards.

**Tier 3 — Real-time.**
OpenF1 live → Queue → Durable Object per session → WebSocket live-timing UI on the
site during race weekends. *The wow feature.*

**Tier 4 — AI platform.**
RAG/NL query over the data, the deterministic rules engine, agentic exploration.
Optionally the enterprise streaming pipeline as a standout engineering piece.

---

## 6. Open decisions (for later)
1. **Stack philosophy** — A, or A+borrow, or go heavier for system-design depth?
2. **Framework** — stay static, or move to Astro now?
3. **How real-time** — Durable Objects (cheap/elegant) vs Kafka (industry-standard)?
4. **Predictions scope** — simple model first, or invest in a real feature pipeline?
5. **Public vs private** — is the architecture itself a public "How it's built" page
   (great system-design signal) or internal only?

*Living doc — we'll annotate as we build each tier. When we implement on Cloudflare,
we have skills for Workers, D1, R2, Durable Objects, Vectorize, Agents SDK, and Wrangler.*
