# Project Prompt: TermForge — A Universal Terminal UI/UX Design System

Paste this into your agent loop as the seed prompt / `AGENTS.md`. It is written to be read by a coordinator agent that spawns subagents, so it speaks directly to the agent, not to a human reader.

---

## 1. Mission

Build **TermForge**: a Python library and companion "storybook" docs site for rendering rich, organized, beautifully composed terminal UIs — text, images (converted to colored ASCII/half-block art), every major chart type including OHLC/candlestick stock charts, animations, ASCII logos, windows, and border systems — all driven by a single, consistent, deeply configurable component and theming model.

This is v1 of a multi-language project. Python ships first, but **every architectural decision must assume the core will be re-implemented in Go and/or Rust and/or TypeScript later.** Anything that can't be described language-agnostically doesn't belong in the core.

## 2. Non-negotiable design principles

1. **Separate the spec from the renderer.** Every visual thing in TermForge (a component, a theme, a chart, a border style) must be describable as plain data (a dataclass / dict / JSON-serializable spec) *before* it touches a rendering backend. The renderer consumes specs; it never owns application state.
2. **One coordinate/layout model for everything.** Text blocks, images, charts, and windows all live inside the same box-model / flex-like layout engine. No component type gets a bespoke layout system.
3. **Color-depth tiering is a first-class concept, not an afterthought.** Every color value in the system must resolve through a fallback chain: truecolor (24-bit) → 256-color → 16-color → monochrome. Detect terminal capability at runtime (`COLORTERM`, terminfo) and degrade gracefully.
4. **Theming is data, not code.** Themes (built-in: at minimum a Catppuccin-compatible set, Dracula, Tokyo Night, and a high-contrast accessible theme) are swappable JSON/YAML token files: colors, spacing scale, border-glyph sets, typography weights (bold/dim/italic support tiers). Components reference tokens, never hardcode colors.
5. **Everything is configurable via both code and config file.** A user should be able to build a window with kwargs *or* declare it in YAML/TOML and load it. Treat the declarative path as equally important as the imperative API — it's what will make the eventual Go/Rust ports and the "storybook" tooling straightforward.
6. **Animation is a first-class primitive**, not a hack bolted onto rendering — build a frame-scheduler/tick abstraction that any component (spinner, transition, chart, logo reveal) can hook into.
7. **No component may assume it's the only thing on screen.** Everything must compose inside windows/panes and survive resize.

## 3. Module map (build in roughly this order)

1. **`termforge.core`** — capability detection (color depth, terminal size, Unicode support), the box-model layout engine, the tick/animation scheduler, the theme-token system, and the spec/renderer split (abstract `Renderable` protocol).
2. **`termforge.text`** — styled text primitives, markup parsing, wrapping/truncation, rich text runs (bold/italic/color spans).
3. **`termforge.image`** — image → colored terminal art pipeline. Support at least two fidelity tiers: half-block Unicode rendering (upper/lower block trick) for true color terminals, and character-ramp ASCII (brightness → glyph) for degraded terminals. This is squarely what `rich-pixels` and `chafa` already solve well — study both implementations for the algorithm, but implement natively so the pipeline can be ported later without a C dependency.
4. **`termforge.charts`** — a unified chart spec (one API surface, many chart types): line, bar, scatter, histogram, stacked/multi-bar, heatmap, sparkline, and **candlestick/OHLC** for stock data. Study `plotext` (broadest chart-type coverage, including candlestick and datetime axes) and `plotille` (Braille-dot high-resolution rendering) as prior art, but design the chart spec so a chart is just another `Renderable` that plugs into the same layout/theme system as everything else — don't let it become an island with its own styling rules.
5. **`termforge.borders`** — a border/frame system with swappable glyph sets (single, double, rounded, heavy, ASCII-only fallback), per-side control, and title/label slots.
6. **`termforge.windows`** — composable window/pane containers: draggable-feel focus states, z-ordering, modal/overlay support, scroll regions. Built on top of `core` layout + `borders`.
7. **`termforge.animation`** — spinners, transitions (fade via color interpolation, slide, wipe), animated logo reveals, chart animation (e.g., streaming candlesticks).
8. **`termforge.logos`** — ASCII/ANSI logo/banner rendering with figlet-style fonts plus the colored-block image pipeline for raster logos.
9. **`termforge.theme`** — the token system + built-in theme packs + a theme editor/preview mode.
10. **`termforge.config`** — YAML/TOML/JSON declarative loader that maps 1:1 onto the imperative API surface.

Rendering substrate: build on **Rich** for styled-text primitives and terminal control, with **Textual**'s reactive/compositor patterns as a reference for the windowing layer if you need a running event loop — but keep `termforge.core` renderer-agnostic underneath so a future port isn't fighting Rich/Textual idioms baked into the design.

## 4. The "storybook" layer

Every component needs a canonical example ("story") that:
- Renders deterministically (no real-time data, seeded random data only)
- Has a matching **VHS tape file** (`.tape`) that records it to GIF/PNG for the docs site
- Has a golden-file `.ascii`/`.txt` snapshot for regression testing

Structure: `stories/<module>/<component>.py` (renders the demo) + `stories/<module>/<component>.tape` (VHS script) + `stories/<module>/<component>.golden.txt` (snapshot). Build a `termforge-story` CLI subcommand that runs all stories, regenerates goldens, and fails CI on unintended diffs.

## 5. Portability contract (read this before writing any core code)

- `termforge.core`'s data model (specs, tokens, layout results) must be expressible as plain JSON. If you can't serialize a `Renderable`'s spec to JSON and back, redesign it.
- Keep **all business logic** (layout math, color-depth resolution, theme token resolution, chart data-to-geometry transforms) in pure functions with no Rich/Textual types in their signatures. Only the outermost rendering layer should import Rich.
- Document every core algorithm (half-block image encoding, candlestick geometry, border-glyph selection) in a language-agnostic `SPEC.md` per module, written as pseudocode + examples — this is what the Go/Rust/TS ports will translate from directly, so treat it as a real deliverable, not an afterthought.
- Avoid Python-only conveniences (metaclasses, decorators-as-API, `__getattr__` magic) in anything that touches the spec model. Dataclasses/plain structs only.

## 6. Agent loop orchestration

You are running as a coordinator agent in a loop with subagents. Structure the work like this:

**Coordinator responsibilities each iteration:**
1. Read `PROGRESS.md` (create it if absent) to see what's done, in progress, blocked.
2. Pick the next module in dependency order (see Section 3 — `core` must be stable before anything else starts).
3. Spawn a subagent per module with a scoped prompt (template below). Never let a subagent touch `termforge.core` once it's marked stable without an explicit coordinator-approved task.
4. After subagents report back, run the full story/golden-file suite yourself before marking anything done.
5. Update `PROGRESS.md` and `SPEC.md` files, commit, loop.

**Subagent roles to spawn (one per active module):**
- `core-agent` — layout engine, capability detection, theming tokens, animation scheduler. Highest priority, blocks everyone else.
- `image-agent` — image-to-ASCII/half-block pipeline.
- `charts-agent` — unified chart spec + all chart types including candlestick.
- `borders-windows-agent` — border glyph system + window/pane compositor.
- `animation-logos-agent` — spinners/transitions + logo rendering, depends on `core`'s scheduler.
- `docs-storybook-agent` — writes stories, VHS tapes, golden files, and the docs site for whatever modules are marked stable.
- `qa-agent` — writes/runs tests, checks color-depth fallback behavior on simulated terminal capabilities, flags any spec that isn't JSON-serializable (portability contract violations).

**Subagent prompt template:**
```
You are the {role} for TermForge. Read SPEC.md files for any module you depend on
before writing code — do not guess their public API. Your module's public API and
data model must follow the portability contract in the coordinator prompt
(Section 5): specs must be JSON-serializable, business logic must be pure functions
with no Rich/Textual types in signatures. When you finish a component, write its
SPEC.md entry, its story, its VHS tape, and its golden file before reporting done.
Report back: what you built, what you deviated from spec and why, what's blocked.
```

**Iteration discipline:**
- One module reaches "stable" (all stories pass, SPEC.md written, portability-contract clean) before its dependents' subagents start real implementation — they can scaffold in parallel but shouldn't finalize APIs against a moving target.
- Every loop iteration ends with a real `git commit` and an updated `PROGRESS.md`, so a run that gets interrupted mid-loop is resumable.
- If `qa-agent` flags a portability-contract violation, that becomes the top-priority task next iteration, ahead of new features.

## 7. Definition of done for v1

- All modules in Section 3 implemented with stories + goldens.
- A working docs site (static, built from stories) with at least one full example per component and a live theme switcher.
- At least three built-in themes, all passing a contrast-check.
- Every module has a `SPEC.md` a non-Python engineer could implement from.
- A `termforge-demo` CLI that renders a full sample "dashboard" (candlestick stock chart + a colored-ASCII logo + a data table + an animated spinner, all inside a bordered window layout) as the flagship example.

## 8. Suggested repo layout

```
termforge/
  core/          (layout, capability detection, theming, scheduler)
  text/
  image/
  charts/
  borders/
  windows/
  animation/
  logos/
  config/
  stories/
  docs-site/
  tests/
  SPEC.md (index of all module SPEC.md files)
  PROGRESS.md
  AGENTS.md  (this file)
```
