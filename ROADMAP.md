# RPX — Roadmap (0 → 100)

The full build, high level. Detail lives in each layer's README and in
[`docs/`](docs/). Everything runs at **$0/month** across five clouds, in public.

Cross-cutting from day one: CI/CD (GitHub Actions), secrets management, infra-as-code (Terraform), and a hard $0 cost line.

---

## Phase 0 — Foundations
- [x] Static race companion live on Cloudflare Pages
- [x] Historical dataset, every Grand Prix 1950–2026
- [x] 3D Track Explorer (Three.js)
- [x] Monorepo structure + public Scope page
- [ ] Provision the free backbone: **Oracle Always Free** VM + **k3s**, GCP project (**BigQuery**), Cloudflare, Actions secrets
- [ ] Terraform baseline — buckets (R2/GCS/S3), BigQuery datasets, IAM
- [ ] Auto-deploy the site via GitHub Actions

## Phase 1 — Batch lakehouse
- [ ] **Spark** jobs over Jolpica + FastF1 → bronze → silver
- [ ] Partitioned **Iceberg/Parquet** tables on R2
- [ ] **dbt** project → gold marts in **BigQuery**, with tests + lineage
- [ ] **Great Expectations** data-quality gates
- [ ] **Airflow** DAG: pull → Spark → dbt → DQ → redeploy
- [ ] Backfill all 77 seasons (idempotent, retried)
- [ ] *Market spike:* Databricks Community Edition + Delta Lake comparison

## Phase 2 — Streaming (the showpiece)
- [ ] **Redpanda/Kafka** on k3s; **OpenF1** live producer → topics
- [ ] **Flink** stateful job: gap-to-leader, sector deltas, tyre-deg, pit-window
- [ ] Keyed state · windowing · checkpointing · **exactly-once** sink → BigQuery + WebSocket
- [ ] **Run it live during a real race weekend**; capture the reliability story
- [ ] *Market spike:* same tier on **GKE** (trial) → k3s vs GKE comparison

## Phase 3 — Serving + frontend
- [ ] **Workers** API over the marts + WebSocket bridge to the live stream
- [ ] **React + TypeScript + Vite** dashboard (shadcn/ui, TanStack)
- [ ] Real-time live-timing UI; deploy on Pages

## Phase 4 — Research-data platform + models
**Data platform**
- [ ] Dataset **versioning** (lakeFS/DVC), dedup + quality filtering, tokenization, data loaders
- [ ] **F1 Judgments** annotation tool (preference pairs)
- [ ] Preference dataset + **inter-annotator agreement** + quality review + versioned guidelines

**Models — the full breadth of AI, not just LLMs**
- [ ] **Supervised ML** — race/qualifying prediction, tyre-deg regression (XGBoost)
- [ ] **Time-series forecasting** — lap-time / gap evolution
- [ ] **Reinforcement learning** — pit-strategy policy + the **Bradley-Terry reward** → RL loop
- [ ] **Computer vision** — event/overtake detection on race imagery
- [ ] **Unsupervised** clustering · **anomaly detection** · **embeddings + vector search**

## Phase 5 — Eval + observability
- [ ] **Eval harness** — predictions, reward model, agent on fixed tasks
- [ ] **Experiment tracking** (Weights & Biases) + a leaderboard
- [ ] **OpenTelemetry** tracing + metrics across pipelines and models
- [ ] **Grafana Cloud** dashboards + data-quality and model-drift alerts

## Phase 6 — Agent + safety
- [ ] **Agentic interface** (tool use) over a **provider-agnostic LLM gateway** — default Claude, swappable to Gemini / open models on cost — + deterministic rules engine
- [ ] Agent **eval suite** (scores models across providers)
- [ ] **Safety classifier** + labeled eval set + precision/recall reporting

## Phase 7 — Proof & polish (the 100)
- [ ] Public **writeups** per layer ("how it's built")
- [ ] One real **upstream open-source PR** (FastF1 / a connector / f1-circuits)
- [ ] Public `about.html` / architecture page updated to match what actually shipped
- [ ] End-to-end **demo** + a root README that tells the whole story
- [ ] **Cross-cloud comparison** writeup — the multi-vendor market thesis, evidenced

---

### Coverage checkpoints
- **Reddit-ready** → after Phases 1–2
- **Human Data Interface-ready** → after Phases 3 + 4
- **Research Data Platform / RL Data-ready** → after Phase 4
- **Research Tools / Safeguards / Applied AI-ready** → after Phases 5–6
