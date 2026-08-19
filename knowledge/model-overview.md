# Model Overview

## Instrument
- **Market:** NQ (E-mini Nasdaq-100 futures)
- **Sizing instrument:** MNQ (Micro NQ) — used for position sizing/testing

## Current direction (as of 2026-08-19)

The model went through three pivots in one day, in order:

1. **Midnight-deviation + OTE, dropped.** Too much discretion required to draw consistently
   (which method, where exactly the swing point is) to build a reliable system around. See
   "Archived approaches" below.
2. **ICT confluence-clustering, dropped.** The follow-up direction — trend-following built on
   structural ICT confluences (FVG/OB/BPR/etc.) automatically clustered into zones — was itself
   dropped same day in favor of something simpler and more directly testable.
3. **Current: Trend Bias + QQE.** Market structure (BOS/CHoCH) computed independently on Daily,
   Weekly, and Hourly sets a directional bias (shown in a dashboard). QQE (smoothed-RSI with an
   ATR-trailing band) crossovers trigger entries, taken only in the direction the bias allows. An
   ATR trailing stop manages risk. This is implemented as an actual backtestable strategy:
   `pinescript/trend-bias-qqe-strategy.pine`.

## Framework (current)

### 1. Bias
- Market structure — BOS (Break of Structure) for trend continuation, CHoCH (Change of
  Character)/MSS for reversal — computed on Daily, Weekly, and Hourly independently.
- One timeframe (default Daily, configurable) is the "primary" bias that gates trade direction;
  optionally require all three to agree before trading at all.
- Simplified detection model: last confirmed swing high/low broken by a close = signal. This is a
  simplification of the full Protected-High/Low nuance in `ict-glossary.md` — good enough to read
  bias at a glance and drive trade direction, not a precise PLC/PL model.

### 2. Entry — QQE
- QQE: RSI smoothed with an EMA, with an ATR-of-RSI-derived trailing band (same shape as a
  SuperTrend, but computed in RSI space). A crossover of the smoothed RSI over/under its own
  trailing band is the raw signal.
- Only acted on when it agrees with the current bias: longs only when bias is bullish, shorts
  only when bias is bearish.

### 3. Exit
- ATR trailing stop, always active (protects capital, lets winners run — consistent with this
  project's long-standing "no fixed R:R" philosophy).
- Optional early exit on an opposing QQE cross, or on the HTF bias flipping against the position.

### 4. No painting, no re-entries (explicit requirements)
- **No painting:** every signal (structure break, QQE cross, entry) is only acted on/plotted once
  its bar is confirmed closed (`barstate.isconfirmed`) — nothing shown ever flips back off after
  the fact.
- **No re-entries:** `pyramiding = 0` plus an explicit `strategy.position_size` check on every
  entry condition — a same-direction signal while already in that direction is a no-op; you only
  get a new order on a flip from flat/opposite.

## Archived approaches (kept for reference, not deleted)

- **Midnight deviation + OTE** — `midnight-deviation-method.md`, `ote-method.md`,
  `automation-requirements.md`. A specific 5m-candle + fib method aligned with a top-down HTF→LTF
  confluence zone, refined with an OTE fib. Dropped: too discretionary.
- **ICT confluence clustering** — `pinescript/confluence-cluster.pine`,
  `pinescript/confluence-viewer.pine`, and the bulk of `confluences.yaml` (FVG, iFVG, BPR, Order
  Block, Breaker Block, Rejection Block, Inverse Rejection Block, liquidity concepts, Premium/
  Discount, Protected High/Low, Range Settlement — all marked `deprecated`). `market_structure`
  and `change_of_structure` remain active since they're the basis for the current bias model.
  `ict-glossary.md` and `trade-strength-framework.md` stay as reference material regardless of
  which approach is active.
- **Basic EMA-crossover strategy** — `pinescript/basic-trend-strategy.pine`. The very first
  scaffold, superseded but kept as the simplest possible fallback.

## Working documents

- `confluences.yaml` — registry from the ICT-clustering phase; mostly `deprecated` now except
  structure-related entries.
- `ict-glossary.md` — definitions for every ICT concept encountered (reference material).
- `trade-strength-framework.md` — general confluence-stacking checklist (reference material).
- `examples.md` — trade/reference examples.
- `open-questions.md` — running list from the ICT-clustering phase; mostly moot now, worth a
  fresh pass for the Trend Bias + QQE model specifically (primary bias timeframe choice, QQE
  parameter tuning, stop multiple, etc.) once there's backtest data to react to.
