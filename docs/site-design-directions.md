# RPX Site — Design Directions & Learning Brief

*Rees Performance · f1.alphonsowoodbury.com · 2026-06-15*

**Purpose.** A menu of art directions for the site, written to be *learned from*.
For each direction: the concept, its visual components, the underlying data/tech
model it needs, honest pros/cons, reference touchstones, and what you'll learn
building it. Then a shared vocabulary glossary and a recommended production
sequence. Nothing here is decided — this is the map. We'll prototype all of them.

> **The key strategic idea:** build **one content + data layer**, then render it
> through **multiple "skins."** Each art direction becomes a theme over the *same*
> pages. That's how real design systems work, it makes the directions truly
> comparable (apples to apples), and it's the most efficient way to "explore all of
> them." Decide the winner after you can click through real versions.

---

## Part 0 — The shared foundation (every direction sits on this)

Before any direction, these exist once and are reused. Learning these *is* the
core of modern front-end.

### 0.1 Design tokens
The atomic values of a design — colors, spacing, font sizes, radii, durations —
stored as named variables (CSS custom properties like `--space-4`, `--text-xl`).
Change the token, the whole site changes. This is what lets us re-skin: each
direction is mostly a **different set of token values** over the same markup.

### 0.2 The content / data layer
What the site is *about*, independent of how it looks. For us:
- **Grands Prix dataset** — `data/grands_prix.csv` / `f1.sqlite` (already built).
- **Analyses** — structured findings (pole premium, etc.) as data, not hand-typed HTML.
- **Predictions** — model outputs (later).
- **Circuits** — geometry + metadata for track viz (later).

Best practice: store content as **structured data (JSON)** and *generate* pages
from it, so a redesign never means re-typing numbers. (Today the analysis page
hardcodes numbers; step one of "going pro" is to drive it from JSON.)

### 0.3 The universal craft layer (applies to all directions)
- **Responsive/fluid layout** — works phone → ultrawide.
- **Accessibility (a11y)** — contrast, keyboard nav, `prefers-reduced-motion`.
- **Performance** — fast load, no layout shift.
- **Motion system** — consistent easing + durations (even "no motion" is a choice).

These are *graded* per direction below (some demand far more).

---

## Part 1 — The Directions

Six directions, ordered conservative → bleeding-edge. Each is a real, buildable skin.

---

### A. Editorial / Magazine
**Concept.** A great print feature, on the web. Type-led, generous whitespace,
light theme, color used sparingly as accent. Calm, confident, *readable*.

**Visual components.**
- Large display headlines with a serif or refined grotesk
- Wide margins, narrow text **measure** (~65 characters)
- Drop caps, pull quotes, captioned figures
- Restrained charts that look like they belong in a magazine
- A clear **type scale** doing the hierarchy work, not color

**Data/tech model.** Lowest. Static HTML/CSS, content from JSON. No JS required.
Charts can be pre-rendered SVG.

**Pros.** Timeless; hardest to get *wrong*; foregrounds writing/thinking;
fast; accessible by default. **Cons.** Lower "wow" on first glance; doesn't by
itself scream "engineer"; risk of looking like a blog if type isn't dialed in.

**Touchstones.** *The Pudding* (calmer pieces), Stripe Press, NYT long-form,
Robin Rendle / good personal sites.

**You'll learn.** Typographic hierarchy, modular scale, vertical rhythm/baseline
grid, measure & leading, editorial grids, restraint.

---

### B. Telemetry Terminal *(extends the current v1)*
**Concept.** Dark, engineering-forward, monospace, timing-tower density. Looks
like the pit wall. Signals "I build systems."

**Visual components.**
- Monospace data, thin rules, tabular numerals
- "Timing tower" lists, live-clock/REC motifs, status dots
- Dense tables with inline bar encodings
- A command/query motif (`> grands_prix.where(...)`)
- Dark surfaces, high contrast, grid lines everywhere

**Data/tech model.** Medium. Shines with **live or live-feeling data** — a small
JSON API or pre-baked "latest" snapshot, optional WebSocket fakery for a ticking
feel. Tabular data is the hero.

**Pros.** Distinctive; instantly reads "data/engineering"; great for dense info;
already partly built. **Cons.** Can feel cold/niche; dark + monospace fatigues
over long reading; harder to make *beautiful* vs merely *technical*; accessibility
needs care (contrast, font size).

**Touchstones.** F1 broadcast timing graphics, Bloomberg Terminal, aerospace
mission-control UIs, Vercel/Linear dark aesthetics.

**You'll learn.** Data-dense layout, tabular figures, monospace typesetting,
information density vs clarity, dark-theme contrast, "diegetic" UI (UI that feels
in-world).

---

### C. Swiss / International Typographic Style
**Concept.** Mathematical precision. A strict modular grid, asymmetric balance,
Helvetica-lineage type, flat color blocks. Design-school rigor. (Closely related
to editorial but more systematic and grid-exposed.)

**Visual components.**
- Visible, rigorous **column grid** (often 12-col) used assertively
- Asymmetric layouts, big size contrast, lots of negative space
- Flat geometric blocks; one bold accent at most
- Numbers and labels as compositional elements

**Data/tech model.** Low. Static; the discipline is in CSS Grid mastery.

**Pros.** Looks deeply "designed"; ages well; teaches grid thinking better than
anything; very strong for a data site. **Cons.** Can feel austere/corporate;
unforgiving — small misalignments are obvious; less "fun."

**Touchstones.** Josef Müller-Brockmann, Massimo Vignelli (NYC subway map),
Swiss poster design, modern fintech sites.

**You'll learn.** Grid systems (columns/gutters/margins), the golden ratio &
modular scales, asymmetric balance, negative space, alignment discipline,
CSS Grid in depth.

---

### D. Modern Sport Brand
**Concept.** Energetic, kinetic, bold accent color (a "team color"), angular
shapes, motion-rich cards. Like an actual F1 team site or F1.com. High-impact,
product-y. Furthest from monochrome.

**Visual components.**
- Strong **brand accent color** + dynamic gradients
- Angular/diagonal cuts, speed lines, oversized numerals
- Animated cards, hover states, marquees, "next race" countdown
- Bold condensed type, energetic imagery

**Data/tech model.** Medium-high. Wants a **brand system** (logo, color, motion
guidelines), a "next race" countdown (needs the upcoming-races calendar), and
hero imagery. Benefits from a component library.

**Pros.** Highest immediate "wow"; reads as product/brand sense; a natural fit
for sports/automotive. **Cons.** Trend-prone (can date fast); color + motion are
easy to overdo; most work to make tasteful; needs real assets (logo, photos).

**Touchstones.** Formula1.com, F1 team sites (McLaren, Red Bull), Nike, EA Sports.

**You'll learn.** Brand identity systems, color theory (accent/neutral roles),
motion design & easing, component-driven UI, countdown/stateful UI, restraint
under high energy.

---

### E. Cinematic Data-Editorial  *(the strongest portfolio play)*
**Concept.** Full-bleed immersive hero + **scrollytelling**, but built *around*
beautiful data viz and typography. Combines C's rigor, A's writing, and motion.
Shows design + data + engineering together.

**Visual components.**
- Full-bleed hero (image/video/canvas) with a huge display headline
- **Scroll-triggered** sequences: charts that draw themselves, numbers that count
  up, sticky visuals with stepping text ("scrollytelling")
- Parallax depth, generous cinematic spacing
- Data viz as the emotional centerpiece, not decoration

**Data/tech model.** High. Needs the structured data layer + a charting approach
(D3.js or hand-rolled SVG/Canvas), an **intersection-observer**/scroll engine
(e.g., GSAP ScrollTrigger or vanilla), and hero media. Heaviest performance budget.

**Pros.** Highest ceiling; uniquely shows *all four* skills at once; memorable;
exactly "a beautiful site like I've never built." **Cons.** Most effort and the
most ways to fail (jank, motion sickness, slow load, accessibility); needs
discipline so motion serves the story, not ego.

**Touchstones.** *The Pudding* (flagship pieces), NYT/Reuters/Bloomberg graphics,
Apple product pages, Active Theory / Stripe annual reports.

**You'll learn.** Scrollytelling, intersection observers, scroll-linked animation,
data viz (D3, encodings, transitions), narrative structure, performance budgets,
`prefers-reduced-motion`, art direction.

---

### F. Experimental / WebGL-Immersive  *(bleeding edge, stretch)*
**Concept.** Real-time 3D. Render circuits as **3D geometry**, shader effects,
a hero you can orbit. The "I can do anything on the front end" flex.

**Visual components.**
- 3D track models (extruded from circuit geometry), camera moves
- Shaders (heat maps of speed, particle trails), GPU-driven motion
- Interactive 3D hero; physical/spatial navigation

**Data/tech model.** Highest. **Three.js / WebGL** (or react-three-fiber),
circuit geometry (GeoJSON → 3D), telemetry/speed data to drive shaders, asset
pipeline, heavy performance + fallback (a 2D version for weak devices/reduced-motion).

**Pros.** Maximum wow + technical flex; genuinely rare in portfolios; perfect home
for track viz. **Cons.** Steepest learning curve; biggest performance/accessibility
risk; easy to be impressive-but-useless; long build. Best as *one feature*
(the track explorer), not the whole site.

**Touchstones.** Bruno Simon's portfolio, Active Theory, Awwwards "Site of the
Day" WebGL work, F1 2024-era broadcast 3D track graphics.

**You'll learn.** WebGL/Three.js, 3D math (cameras, meshes, coordinate spaces),
shaders (GLSL), GPU performance, graceful degradation, asset pipelines.

---

## Part 2 — The cross-cutting features (recur in every direction)

These are *content*, not style — they get skinned by whatever direction wins.

### Feature: Analyses (e.g., Pole Position)
- **Data model:** analysis findings as JSON (`{title, dek, stat, series[], tables[], notes}`)
  generated from the dataset, so pages are data-driven, not hand-typed.
- **Powers:** every direction's "article" pages.

### Feature: Race Predictions ("the AI feature")
- **Data model needed:** historical results + qualifying + a **feature set**
  (recent form, track type, pole→win rate by circuit, team pace, weather later).
  Output: per-race probabilities `{driver, p_win, p_podium, p_pole}`.
- **Tech:** a model (start simple — logistic regression / gradient boosting on the
  existing data; the pole-premium finding is literally a feature). Serve predictions
  as static JSON regenerated per race weekend.
- **Learning:** feature engineering, train/test discipline, calibration, honest
  uncertainty, ML serving.

### Feature: Track Visualizations ("the design+data feature")
- **Data model needed:** **circuit geometry** (centerline as GeoJSON/SVG path),
  corner annotations, DRS zones, plus our per-circuit pole→win stat.
- **Tech:** 2D (SVG/Canvas) in directions A–E; 3D (WebGL) in F.
- **Learning:** geospatial data, SVG path math, map projections, annotation UX.

---

## Part 3 — Design / UX glossary (the vocabulary you'll learn)

**Typography**
- **Type scale / modular scale** — a ratio-based set of font sizes for harmony.
- **Hierarchy** — using size/weight/space to rank importance.
- **Measure** — line length; ~45–75 chars is the readable range.
- **Leading / tracking / kerning** — line-height / letter-spacing / pair-spacing.
- **Vertical rhythm / baseline grid** — consistent vertical spacing unit.
- **Tabular figures** — digits of equal width so numbers align in columns.

**Layout & composition**
- **Grid system** — columns, gutters, margins structuring the page.
- **Negative / white space** — intentional emptiness; a design tool, not waste.
- **Gestalt principles** — proximity, similarity, continuity: how we group things.
- **Focal point / visual weight** — where the eye lands first.
- **F-pattern / Z-pattern** — common reading scan paths.
- **Above the fold** — what's visible before scrolling.
- **Rule of thirds / asymmetric balance** — composition without symmetry.

**Color & theme**
- **Palette roles** — neutral / surface / accent / semantic (success, danger).
- **Contrast ratio** — legibility metric; WCAG **AA** = 4.5:1 body text, 3:1 large
  text & UI; **AAA** = 7:1.
- **Dark vs light theme** — and supporting both via tokens.

**Motion & interaction**
- **Microinteractions** — tiny feedback animations (hover, toggle).
- **Easing / cubic-bezier** — the acceleration curve of motion; "ease-out" feels natural.
- **Scrollytelling** — narrative driven by scroll position.
- **Parallax** — layers moving at different speeds for depth.
- **Intersection Observer** — browser API to trigger things as they enter view.
- **`prefers-reduced-motion`** — respect users who disable animation (a11y + ethics).
- **Affordance** — a control looking like what it does.
- **Progressive disclosure** — reveal complexity gradually.
- **Skeleton / loading states** — placeholders while data loads.

**Data visualization**
- **Encoding** — mapping data to visual channels (position > length > angle > color
  for accuracy — *preattentive attributes*).
- **Data-ink ratio (Tufte)** — maximize ink that shows data; cut **chartjunk**.
- **Small multiples** — a grid of mini-charts for comparison.
- **Sparkline** — a tiny inline trend chart.
- **Choropleth** — a shaded map (relevant to circuits/countries).

**Systems & engineering**
- **Design system / component library** — reusable, documented UI parts.
- **Atomic design** — atoms → molecules → organisms → templates → pages.
- **Design tokens** — named design values (see 0.1).
- **Responsive / fluid type** — `clamp()`-based sizing across breakpoints.
- **Mobile-first** — design small, enhance up.
- **Core Web Vitals** — **LCP** (load, <2.5s good), **CLS** (layout shift, <0.1),
  **INP** (interaction latency, <200ms).
- **Progressive enhancement / graceful degradation** — works everywhere, better on capable devices.

---

## Part 4 — Recommended production sequence

Rationale: build the foundation once, then climb the difficulty curve so each
direction *teaches the next*. Lower directions are fast; the payoff is comparing
them all as real, clickable pages.

**Phase 0 — Foundation (do once).**
1. Extract content to a **JSON data layer**; make the analysis page data-driven.
2. Define a **design-token system** + shared base CSS (reset, grid, type scale).
3. Pick the same 2 pages to theme everywhere: **Home** + **Pole Position** (so
   every direction renders identical content).

**Phase 1 — The fundamentals (fast, high-learning).**
4. **A. Editorial** — learn type, scale, rhythm, measure. Cheapest to nail.
5. **C. Swiss grid** — learn grid systems & alignment discipline (builds on A).

**Phase 2 — Identity & data feel.**
6. **B. Telemetry terminal** — refine the v1 into something genuinely beautiful,
   not just technical; learn dense data layout.
7. **D. Modern sport brand** — learn color, brand systems, motion, components.

**Phase 3 — The showcase.**
8. **E. Cinematic data-editorial** — the flagship; combines everything above plus
   scrollytelling + real data viz. This is the likely "winner" candidate.

**Phase 4 — The flex (optional, as a single feature).**
9. **F. WebGL track explorer** — bring 3D in as the *track-visualization* feature
   rather than the whole site. Lower risk, maximum payoff.

**Phase 5 — Decide & build out.**
10. Click through all skins, pick the direction (or a blend), then build the
    **predictions** and **tracks** features in the chosen language.

---

## Part 5 — How we'll decide later
Score each prototype on: **wow factor**, **skill-signal** (does it show SWE/AI/
data/design?), **readability**, **performance**, **maintainability**, **on-brand
for F1 + Rees**. A blend is allowed and likely — e.g., Cinematic (E) as the site
with a WebGL (F) track feature and Telemetry (B) accents for live data.

*This is a living document — we'll annotate it as we build each prototype.*
