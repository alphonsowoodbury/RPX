# RPX — Advanced Capabilities: LLMs, Agents & 3D

*Rees Performance · f1.alphonsowoodbury.com · 2026-06-15*

**Purpose.** The AAA+ ceiling. Two advanced layers — an **LLM/agent system** and a
**3D / Blender visual pipeline** — scoped the same way as the rest: components,
data models, honest trade-offs, vocabulary to learn, and where each slots into the
build tiers. All "over time." This is the map, not a commitment.

---

# Part A — LLMs & Agents

## A.1 Where LLMs actually earn their place on RPX
Not "add a chatbot." Specific, defensible jobs:
- **Ask-the-data (RAG):** "Which circuits reward a strong qualifier?" → retrieve
  from our dataset → grounded answer with the numbers.
- **Race reports:** auto-write a tight recap from the structured results of a GP.
- **Strategy explainer:** narrate *why* a model predicted an outcome, in plain English.
- **Learning guide:** the teaching layer — explain F1 + the engineering behind RPX.
- **Agentic tasks:** an agent that, on its own, pulls a session, runs an analysis,
  and drafts a write-up — the "it built this page itself" flex.

## A.2 The RPX agent system (built on your OSS stack)
You've already designed this; restating it as the RPX target (renamed from XRS):

**6 layers:** Data → Tools → Agents → Guardrails → Visibility → Intelligence.

| Your package | Role in RPX |
|---|---|
| **AgentContext** | Governance — guardrails, decisions, **audit trail** |
| **Alpha** | Privacy/visibility — who/what an agent can see |
| **MeristemLLM** | Provider abstraction — Claude + on-device, swappable |
| **TurboAgent** | Subagent framework — least-privilege, security hooks |
| **CXO** | Operator intelligence (meta-layer) |
| **Everything** | UI composition — agents compose views from primitives |
| **Folios / Tudo** | Auto-synthesizing race logs + learning artifacts |

**6 specialized agents:** Telemetry Analyst · Strategy Planner · Race Reporter ·
Simulation Runner · Learning Guide · Platform Architect.

> The differentiator (your stated pitch): **agents propose, the deterministic rules
> engine decides.** The LLM is the interface and the narrator; exact, auditable
> calculations are the source of truth. That FIA-style auditability is the credibility
> story that separates this from a toy chatbot.

## A.3 Patterns & vocabulary (what you'll learn)
- **RAG (retrieval-augmented generation)** — fetch relevant data, then answer; cuts hallucination.
- **Embeddings / vector search** — turn text/data into vectors for semantic retrieval.
- **Tool use / function calling** — the model calls real functions (query DB, run model).
- **Structured output** — force JSON-shaped answers (validated, not parsed-from-prose).
- **ReAct** — reason → act → observe loops for multi-step tasks.
- **Multi-agent orchestration** — specialist agents + a coordinator; fan-out/verify.
- **Memory** — short-term (context) vs long-term (persisted facts).
- **Guardrails** — input/output checks, allow-lists, least-privilege tools.
- **Evals** — test sets that measure answer quality/regressions (the unglamorous key to trust).
- **MCP (Model Context Protocol)** — standard way to expose tools/data to models.
- **Cost/latency tiering** — cheap fast model for routing/extraction, strong model for reasoning.

## A.4 Data model & infra
- **Vector store** (Vectorize / pgvector): embeddings of analyses, glossary, race facts.
- **Tool APIs**: thin functions over our data (`getRace`, `poleStats`, `predict`) the agents call.
- **Audit log**: every agent decision + tool call recorded (AgentContext) — for the auditability story.
- **Eval set**: curated Q→expected-answer pairs, run in CI.
- **Models**: via MeristemLLM — Claude tiers today (a cheap/fast tier for routing,
  a strong tier for reasoning), with an on-device fallback path. Serving on **Workers AI**
  or direct API.

## A.5 Pros / cons
**Pros:** the headline "AI" signal; genuinely useful (NL query, auto-reports); reuses
your OSS; the deterministic boundary makes it credible; maps to what F1 teams are
deploying in 2026. **Cons:** hallucination risk (mitigated by RAG + rules engine);
evals are real work; cost/latency to manage; easy to over-scope. Build *one* agent
well (Race Reporter or Ask-the-data) before the full six.

---

# Part B — 3D, Blender & Visual Production

## B.1 Where 3D earns its place (don't 3D everything)
- **Interactive track explorer** — the flagship: orbit a circuit, see corners, DRS
  zones, and a speed heatmap baked from telemetry. This is the "wow."
- **Telemetry replays** — "ghost cars" moving around the track from real position
  data (FastF1/OpenF1 carry x/y position).
- **Hero moment** — a single cinematic 3D element on the homepage, not the whole site.
- **Data-driven 3D viz** — e.g., a season as a 3D ribbon. Use sparingly.

## B.2 The production pipeline (how 3D gets to the web)
```
  MODEL            EXPORT           WEB RUNTIME            ENHANCE
  Blender   →   glTF / .glb   →   Three.js /          →  shaders (GLSL)
  (or data-                       react-three-fiber      physics (Rapier)
   generated mesh)                + drei helpers         postprocessing
                                                         (bloom, DoF)
                          ↓ optimize ↓
              Draco (geometry) · KTX2/Basis (textures) · LOD · instancing
```
- **Blender** — model/animate assets (a stylized car, track furniture), export **glTF/GLB**
  (the "JPEG of 3D" — the web standard).
- **Three.js** — the WebGL engine. **react-three-fiber (R3F)** if we go React, with
  **drei** for ready-made helpers (cameras, controls, loaders).
- **Track from data** — extrude the circuit centerline (GeoJSON/SVG path) into a 3D
  mesh programmatically — *no Blender needed* for the track itself.
- **Shaders (GLSL)** — custom GPU effects: speed gradients, glow, heat maps.
- **Physics (Rapier)** — only if we want real motion/collisions (probably not needed).

## B.3 Tooling options
| Tool | Use | Note |
|---|---|---|
| **Three.js** | The core WebGL library | Most control, biggest ecosystem |
| **react-three-fiber + drei** | Three.js in React | Cleaner if the site is React/Astro-React |
| **Blender** | Asset creation | Free, pro-grade; steep but worth it |
| **Spline** | No-code 3D in the browser | Fast for hero pieces; less control |
| **Babylon.js / PlayCanvas** | Alt engines | Babylon strong for games; PlayCanvas hosted |
| **CesiumJS / deck.gl** | Geospatial 3D | If we want real-world circuit geography |

## B.4 Data model
- **3D assets**: `.glb` files in R2, lazy-loaded.
- **Circuit geometry**: centerline + corner/DRS metadata (GeoJSON) → drives the track mesh.
- **Telemetry**: per-driver position + speed series → drives ghost cars + heatmaps.

## B.5 AAA techniques (the vocabulary)
- **glTF/GLB, Draco, KTX2** — model + compression formats.
- **PBR (physically based rendering)** — realistic materials via light/metalness/roughness.
- **LOD (level of detail) · instancing · frustum culling** — performance at scale.
- **Postprocessing** — bloom, depth of field, ambient occlusion for a cinematic look.
- **Camera choreography / scroll-linked 3D** — the camera flies as you scroll.
- **GPGPU particles** — thousands of GPU-driven particles (sparks, trails).
- **Draw calls / frame budget** — the 60fps discipline.

## B.6 Pros / cons
**Pros:** the highest-ceiling wow; genuinely rare in a portfolio; perfect home for
the track explorer; teaches a whole discipline. **Cons:** steepest learning curve;
real performance + accessibility risk (mobile, motion sensitivity); long build;
easy to be impressive-but-useless. **Rule:** 3D as *one feature* (the track explorer)
with a 2D fallback and `prefers-reduced-motion` respected — never a 3D-or-nothing site.

---

# Part C — How they slot into the build tiers
From the architecture doc, extended:
- **Tier 3 (Real-time):** add a **2D track viz** first (SVG/Canvas) — cheap, useful.
- **Tier 3.5 (3D):** the **WebGL track explorer** + telemetry ghost cars. The flagship visual.
- **Tier 4 (AI):** ship **one agent** (Ask-the-data or Race Reporter) on RAG +
  the deterministic engine; then grow toward the full 6-agent system.
- **Ongoing:** AAA polish — postprocessing, camera choreography, motion design —
  is continuous, applied to whichever design direction wins.

Sequence rule: **2D before 3D, one agent before many, evals before trust.**

---

# Part D — Open decisions (later)
1. **3D scope** — single hero moment, or the full interactive track explorer?
2. **Engine** — raw Three.js vs react-three-fiber (depends on the framework choice).
3. **Blender vs data-generated geometry** — model assets, or extrude tracks from data?
4. **First agent** — which one ships first (Race Reporter? Ask-the-data?).
5. **On-device vs API models** — how far to push MeristemLLM's local path.
6. **How public** — is the agent/3D work shown live, or demoed via recorded clips first?

*Living doc. We have skills available for the AI side (Workers AI, Vectorize, Agents
SDK) when we build; 3D will be a from-scratch learning track. Pairs with
`architecture-infra.md` and `site-design-directions.md`.*
