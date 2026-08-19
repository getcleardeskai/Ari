# Pine Script

Strategies/indicators implementing the model from `../knowledge/automation-architecture.md`.

## `auto-reversion-strategy.pine` — current focus

Current focus (2026-08-19) — the mean-reversion half of the two-strategy plan (see
`../knowledge/strategies/mean-reversion.md`). 200 MA bias filter + an approximated MRC-style
multi-band channel (overextension) + QQE entry signal + a volume-vs-average confirmation window
(with a "pending" grace period if volume doesn't confirm on the signal bar itself). ATR/tick stop,
band-level take-profit.

**v1 locked in, 2026-08-19:** simple, long + short. MRC and QQE are exact ports of the trader's
real source scripts (fareidzulkifli's Mean Reversion Channel, colinmck's QQE signals) with the
outer multiplier corrected to 1.5 (the trader's actual setting, confirmed from their settings
dialog — not the public script's own default of 2.415). Entry: bias (MA fully outside the outer
band) + price has touched the outer band at some point (persists across bars, doesn't need to
coincide with the signal) + a QQE signal in the matching direction, confirmed-close only. Exit:
take profit at the live inner band on the opposite side, stop at the live outer band on the entry
side. No volume filter — deferred to a later version. See the file's own header comment and
`../knowledge/strategies/mean-reversion.md` for the full history of what changed to get here
(SMMA-vs-SMA bug, wrong outer multiplier, dropped rules in an earlier comparison attempt).

**How to use it:** TradingView → open an MNQ1! or NQ1! chart → Pine Editor → paste this file's
contents → Add to Chart → Strategy Tester tab. Hand-written, not yet run through TradingView's
compiler — send me the exact error text if it throws one on first load.

## `trend-bias-qqe-strategy.pine` — other active strategy

Current focus (2026-08-19) — full pivot away from ICT confluences entirely. This is a real,
backtestable **strategy**: Daily/Weekly/Hourly bias computed from market structure (BOS =
continuation, CHoCH = reversal), shown in a top-right dashboard table; QQE (smoothed-RSI +
ATR-trailing-band) crossovers trigger entries, but only in the direction the bias allows; an ATR
trailing stop manages risk, with optional early exit on an opposing QQE cross or a bias flip.

No painting (every signal only fires once its bar is confirmed closed) and no re-entries
(pyramiding=0 plus an explicit position-size check) were both built in from the start, per
request. See the file's own header comment for full detail on both.

**How to use it:** TradingView → open an MNQ1! or NQ1! chart → Pine Editor → paste this file's
contents → Add to Chart → Strategy Tester tab for backtest results; the bias dashboard and
buy/sell arrows show directly on the chart. Hand-written, not yet run through TradingView's
compiler — send me the exact error text if it throws one on first load.

## `confluence-viewer.pine` — earlier iteration, kept for reference

Current focus (2026-08-19) — a pure **visualization indicator**: pulls Structure (BOS/MSS-ChoCH),
Fair Value Gaps, an approximate POC, and auto trendlines from a higher timeframe (default 1H,
configurable) and plots them directly on whatever chart you're actually viewing (e.g. 1m). Goal
is to just *see* the confluences clearly, not to backtest or cluster them.

**Behavior:**
- Structure labels (BOS/MSS), the POC line, and trendlines are permanent historical markers —
  they don't get deleted once price passes them.
- FVG boxes DO get removed, but only once the **current chart's** close fully trades through
  them (reached + reacted to), not just gotten close.

**v1 scope:** Structure, FVG, approximate POC, auto trendlines (last 2 swing highs/lows). NOT yet
included: Order Block, BPR, IFVG, Breaker Block, liquidity levels (STH/STL/ITH/ITL, prior session
high/low) — see `../knowledge/ict-glossary.md`. Structure detection is a simplified swing-break
model (BOS = break of last swing in bias direction, MSS/ChoCH = break against it), not the full
Protected-High/Low model from the glossary yet. POC is a close-price/volume approximation using
the current chart's own bars, not a true tick-level volume profile.

**How to use it:** TradingView → open an MNQ1! or NQ1! chart → Pine Editor → paste this file's
contents → Add to Chart. Set "Higher timeframe" in the input panel (default 1H) — everything is
computed from that timeframe and displayed on whatever chart you're looking at. This is
hand-written and not yet run through TradingView's compiler — if it throws a syntax error on
first load, send me the exact error text and I'll fix it immediately.

## `confluence-cluster.pine` — earlier iteration, kept for reference

An earlier attempt (2026-08-19, same day) that instead *merges* nearby confluences into one
combined box when several stack within a tick tolerance. Superseded by `confluence-viewer.pine`
above for the main "just show me everything clearly" goal, but the clustering approach might be
useful again later (e.g. as a "hot zone" overlay once individual confluences are trusted). Same
single-timeframe/3-zone-type limitations as before — see the file's own header comment.

## `basic-trend-strategy.pine` — first scaffold, kept for reference

The very first script (2026-08-19) — a simple EMA-crossover trend-following **strategy** (not an
indicator) with an ATR-based stop/target, backtestable in the TradingView Strategy Tester. Not
the current direction (the actual goal turned out to be visualization, not a backtestable
strategy), but kept as the simplest possible baseline in case a strategy/backtest angle comes
back into play later.
