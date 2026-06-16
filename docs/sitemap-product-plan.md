# RPX Site — Product Plan & Sitemap

*Rees Performance · f1.alphonsowoodbury.com · 2026-06-15*

## The reframe
The site is **a product, not a portfolio.** It's a **race companion** — something
Alphonso and others actually open *while watching a Grand Prix*. The portfolio value
(SWE/AI/data/design) becomes a **byproduct** of building something genuinely useful,
not the point. Everything we've built stays; it gets reorganized around real use.

**Primary user & job:** "I'm watching the race — give me the schedule, the track, the
stakes, the standings, and the results, clearly, without digging."

**First real target weekend:** 🇦🇹 **Austrian GP · Red Bull Ring · Round 8 ·
Qualifying Jun 27, Race Jun 28.** ~11-day runway.

---

## Sitemap

```
f1.alphonsowoodbury.com
│
├── /                     RACE HUB  (home = the current / next Grand Prix)
│                           countdown · sessions (local time) · circuit (3D) ·
│                           what to watch · grid/quali · results · standings snapshot
│
├── /standings            Drivers' + Constructors' championships (live-ish)
│
├── /tracks               Track Explorer (3D) — all circuits      [built]
│     └── /tracks/?c=…       individual circuit
│
├── /insights             Analysis & writing (the "thinking" content)
│     └── /insights/pole-position    The Pole Position Premium     [built, moves here]
│
└── /about                Who + How it's built
        (merges current homepage "about" + the architecture page)   [built, merges]
```

**Top nav (every page):** `Race · Standings · Tracks · Insights · About`
Wordmark → Race Hub. Clear, five items, product-first ordering.

---

## Page-by-page

### / — Race Hub (the centerpiece, new)
The page you open during a weekend. Sections, top to bottom:
1. **This weekend** — race name, circuit, round, **countdown to next session**.
2. **Sessions** — FP1/2/3, Qualifying, Race with **times auto-converted to the
   viewer's local timezone** (this is the single most useful feature).
3. **The circuit** — embedded 3D track + key facts (length, our **pole→win % here**,
   corners). Red Bull Ring = 38.5% pole conversion — pole matters less here.
4. **The stakes** — top of both championships + last-race form.
5. **Results** — grid/qualifying after Saturday; race result + updated standings after Sunday.
6. *(later)* Predictions; *(v2)* live timing.

### /standings
Both championship tables, updated after each session. Sortable, clean.

### /tracks  [built]
The 3D explorer. Add **Red Bull Ring** (at-1969) for the Austria weekend.

### /insights  [pole-position moves here]
Index of analyses; the Pole Position piece becomes the first entry.

### /about  [merge]
The current homepage's "about" copy + the architecture/"How it's built" page,
combined into one credibility page. This is where the portfolio story lives now.

---

## Data: how each page gets fresh data
- **v1 (this weekend): fetch Jolpica directly from the browser on page load.** No
  pipeline needed — schedule, standings, results are all there and update after each
  session. Cache lightly. Ships fastest, reliable.
- **Our data:** circuit pole→win stats (from `grands_prix.csv`) baked into JSON.
- **3D:** existing `tracks/data/*.json`.
- **v2 (later): true live timing** during the race (lap-by-lap, intervals) → needs
  **OpenF1** + WebSockets/Durable Objects. This is the only "real-time" piece, and
  it's deferred. Jolpica refreshes *between* sessions, not *during* a lap — be honest
  about that in the UI ("updated after each session").

---

## MVP cut for the Austrian GP (in / out)

**IN (ship by Jun 26):**
- Race Hub with countdown + **local-time session schedule**
- Red Bull Ring in 3D + our circuit stats
- Standings (both championships)
- Results surfacing (grid → quali → race) from Jolpica
- New 5-item nav + reorganized site (insights, about merge)

**OUT (later, clearly roadmapped):**
- Live lap-by-lap timing (v2, OpenF1)
- Predictions model (v2)
- Track elevation / ghost cars (3D v2)

---

## Build sequence (the ~11 days)
1. **Nav + IA refactor** — new 5-item nav, move pole-position → /insights, merge
   about + architecture → /about. (Fast, makes the structure real.)
2. **Race Hub page** — schedule + countdown + local-time conversion + circuit + standings.
3. **Add Red Bull Ring** to the 3D tracks.
4. **Standings page.**
5. **Polish + test on a phone** (you'll use it on the couch — mobile matters).
6. Dry-run with last weekend's data, then it's live for Austria.

---

## What changes from today
- **Home stops being a portfolio hero** → becomes the Race Hub.
- **Pole analysis** → lives under /insights.
- **Architecture page + about** → merge into /about.
- **Nav** → product-first: Race · Standings · Tracks · Insights · About.

## Open questions
1. Weekend scope: companion-now / live-timing-v2 (recommended) — or push to attempt
   live timing for Austria?
2. Keep a small "by Alphonso Woodbury / how it's built" link visible for the
   portfolio angle, or keep it fully in /about?
3. Predictions: simple heuristic for Austria, or wait for the real model?
