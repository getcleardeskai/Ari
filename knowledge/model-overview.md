# Model Overview

## Instrument
- **Market:** NQ (E-mini Nasdaq-100 futures)
- **Sizing instrument:** MNQ (Micro NQ) — used for position sizing/testing

## Current direction (as of 2026-08-19)

The model went through two pivots, in order:

1. **2026-08-19, earlier:** the original midnight-deviation + OTE framework (see "Archived
   approach" below) was judged too hard to encode as deterministic Pine Script in one shot —
   decision made to build a codeable baseline first.
2. **2026-08-19, later:** midnight deviation and OTE were **dropped entirely**, not just
   deferred — the discretion required to draw them consistently (which method to use, where
   exactly the manipulation leg or swing point is) was judged too inconsistent to build a reliable
   system around. Current direction: a **trend-following model built on the remaining structural
   ICT confluences** — market structure/bias, FVG, iFVG, BPR, Order Block, Breaker Block,
   Rejection Block, Inverse Rejection Block, liquidity concepts (ERL/IRL, STH/STL/ITH/ITL) — with
   entries driven by trend + confluence stacking rather than a specific midnight-anchored timing
   mechanism.

## Framework (current)

### 1. Trend / bias
- Market structure (BOS for continuation, MSS/COS/ChoCH for reversal — see `ict-glossary.md`)
  sets directional bias. Still regarded as the most important single factor.

### 2. Confluence detection & clustering
- Rather than manually marking each PDA (FVG/OB/RB/etc.) on each timeframe, the working approach
  is now **automated clustering**: detect every active/unmitigated confluence zone, and whenever
  several land within a tight price band of each other, treat that as one high-probability
  refined area. See `pinescript/confluence-cluster.pine` — this is the first concrete
  implementation of that idea (currently single-timeframe; multi-timeframe scaling is the planned
  next step, still following the **timeframe ladder**:

  ```
  Daily -> 4H -> 1H -> 45m -> 30m -> 15m -> 5m (final refinement)
  ```

### 3. Alignment = entry
- Same core principle as before the pivot: multiple independent confluences landing in the same
  tight area is what makes a zone worth trading, not any single confluence alone. What changed is
  *how* that alignment gets found (automated clustering vs. a midnight-anchored manual process)
  and that midnight timing/OTE are no longer part of the "what to align" set.

See `confluences.yaml` for the full, weighted, editable registry — `midnight_deviation`, `ote`,
and `volume_expansion_pattern` are marked `deprecated` there, everything structural remains
active/testing.

## Entry trigger & trade management

Still open — see `open-questions.md`. Pre-pivot notes said: no fixed R:R, entry needs a
volume-spike reaction, exit managed against HTF S&R or reversal signs. Whether that still holds
in a pure trend/structural-confluence model (vs. specifically midnight-anchored) needs revisiting.

## Archived approach (pre-2026-08-19 pivot)

The original framework anchored entries to a **midnight deviation** (a specific 5m-candle + fib
method) aligned with a **top-down HTF→LTF confluence zone**, refined further with an **OTE** fib.
Full detail is preserved in `midnight-deviation-method.md` and `ote-method.md` in case anything
from it becomes useful again, but neither is part of the active model.

## Working documents

- `confluences.yaml` — the confluence registry (weights/status).
- `ict-glossary.md` — definitions for every ICT concept in use.
- `trade-strength-framework.md` — general confluence-stacking checklist.
- `examples.md` — trade/reference examples.
- `open-questions.md` — running list of what's still unresolved.
- `midnight-deviation-method.md`, `ote-method.md`, `automation-requirements.md` — archived/
  pre-pivot, kept for reference (automation-requirements.md's alerting ideas may still be
  relevant once the confluence-cluster approach is further along — revisit rather than assume
  moot).
