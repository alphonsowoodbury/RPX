# App — Serving, Frontend & Agent — RPX

> The application surface: API, real-time dashboard, and the agent. **Phase 3 → 6.** Status: planned.

A thin edge API and WebSocket bridge over the marts and the live stream, a real-time
dashboard built app-grade, and a natural-language agent that queries the platform
through tools. The static companion in [`/site`](../site/) stays as the marketing
front door; this is the interactive product.

## Scope
- **API:** Cloudflare Workers over gold marts + a WebSocket bridge to the live stream. *(Phase 3)*
- **Frontend:** React + TypeScript + Vite dashboard (shadcn/ui, TanStack Query/Table). *(Phase 3)*
- **Agent:** natural-language interface with **tool use** over the data, backed by a
  deterministic rules engine as the source of truth. Talks to a **provider-agnostic
  LLM gateway** — one interface, model/provider chosen by config — so the agent
  never hard-codes a vendor. *(Phase 6)*

## Stack
`React` · `TypeScript` · `Vite` · `Cloudflare Workers` · `WebSocket` · `LLM gateway` (Cloudflare AI Gateway / LiteLLM) · default **Claude** (Sonnet 4.6 / Opus 4.8 / Haiku 4.5), swappable to **Gemini** or **open models** (Workers AI) on cost

> **AI-agnostic by design.** Provider and model live behind one interface; switching
> is a config change, not a rewrite. The [`/eval`](../eval/) harness scores models
> across providers, so model choice is evidence-driven, not vendor-driven.

## Inputs → Outputs
- **In:** gold marts ([`/lakehouse`](../lakehouse/)), live stream ([`/ingestion/streaming`](../ingestion/streaming/)).
- **Out:** the dashboard + agent; agent quality measured in [`/eval`](../eval/).

---
*Part of the RPX platform.*
