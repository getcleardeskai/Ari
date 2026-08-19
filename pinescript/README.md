# Pine Script

Strategies/indicators implementing the model from `../knowledge/model-overview.md`.

## `basic-trend-strategy.pine`

First scaffold (2026-08-19) — a simple EMA-crossover trend-following strategy with an ATR-based
stop/target, meant to backtest cleanly in the TradingView Strategy Tester. Superseded in
direction (not deleted) by `confluence-cluster.pine` below, which is where active development is
now — this one stays as the simplest possible baseline to fall back to.

## `confluence-cluster.pine`

Current focus (2026-08-19) — an **indicator** (not a strategy/backtester) that detects individual
ICT PDAs — Fair Value Gaps, Order Blocks, Rejection Blocks — tracks which are still active
(unmitigated), and whenever several land within a configurable price band (default 50 ticks) of
each other, draws one box around the combined area labeled with every confluence type found
inside it. This is the automated version of "go find where a lot of confluence stacks into one
tight area."

**Current scope/limitations (v1):**
- Single timeframe only — runs on whatever timeframe the chart is on. Multi-timeframe scaling
  (pulling FVG/OB/RB from Daily/4H/1H/etc. via `request.security` into the same cluster pass,
  per the ladder in `../knowledge/model-overview.md`) is the natural next step, not yet built.
- Only 3 zone types so far: FVG, Order Block, Rejection Block. Not yet included: BPR, IFVG,
  Breaker Block, structure highs/lows (STH/STL/ITH/ITL), previous session liquidity — see
  `../knowledge/ict-glossary.md` for what those are. Straightforward to add once this base
  version is validated.
- Order Block detection is simplified (last opposite-color candle before a displacement candle
  defined by ATR multiple) rather than the full structure-break-aware ICT definition.
- Zones are considered "mitigated" (removed from tracking) on a full close through them; this
  version doesn't yet flip a mitigated zone into an IFVG/Breaker/IRB the way the real concepts do
  — that's future work.

**How to use it:** open TradingView → open an MNQ1! or NQ1! chart → Pine Editor → paste this
file's contents → Add to Chart. It's an indicator, so it draws directly on the chart rather than
running in the Strategy Tester. Tune detection sensitivity and the cluster tolerance/min-zone-
count via the input panel.
