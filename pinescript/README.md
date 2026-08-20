# Pine Script

Strategies/indicators implementing the model from `../knowledge/automation-architecture.md`.

## `mrc-200sma-qqe-indicator.pine` — MRC + 200 SMMA + QQE, signals gated by zone

Added 2026-08-20 — trader's own hand-written version (converted to v6, MRC sizing back to the
public script's original 2.415 outer multiplier rather than the 1.5 used elsewhere in this repo)
combining the MRC bands, the 200 SMMA, and QQE signals into one indicator: the SMMA plots white
while inside the outer MRC band and light blue while outside it, and QQE signals only print while
the SMMA is light blue.

**2026-08-20 bugfix:** the first version gated both QQE Long and QQE Short on the same direction-
agnostic "SMMA is outside the outer band, either side" condition — so a Long could print while the
SMMA was pinned in short-only territory (above the upper band) and vice versa. Trader caught it
live: a "Long" label printing well up in a clear short zone. Fixed by splitting that into
`maBelowOuter` (the actual long-valid zone) and `maAboveOuter` (the actual short-valid zone) so
each signal only fires in the zone that matches its own direction.

Pure visual indicator, no `strategy.*` — plots signals and alerts only, doesn't trade.

**How to use it:** TradingView → open your chart → Pine Editor → paste this file's contents →
Add to Chart. Hand-written, not yet run through TradingView's compiler — send me the exact error
text if it throws one on first load.

## `mrc-and-200ma-indicator.pine` — visual-only, MRC + 200 MA in one script

Added 2026-08-20. A plain **indicator** (no entries, no strategy logic) that combines
fareidzulkifli's MRC and the 200-period bias MA into a single chart overlay, so they don't need to
be stacked as two separate indicators. The MRC is trimmed down to exactly 4 lines — outer
upper/lower (R2/S2) and inner upper/lower (R1/S1) — dropping the original public script's
9-segment gradient shading, multi-timeframe table, and alternate filter types. Same exact
SuperSmoother math as the strategy scripts below (outer mult 1.5, inner mult 1.0, 200-bar
lookback), same MA (SMMA/200 by default). Toggle to also show the MRC's own internal mean line
(off by default, since only the 4 bands were asked for) and to turn the between-band shading on
or off.

**How to use it:** TradingView → open your chart → Pine Editor → paste this file's contents →
Add to Chart. Hand-written, not yet run through TradingView's compiler — send me the exact error
text if it throws one on first load.

## `mrc-gap-qqe-strategy.pine` — literal 6-rule version, added 2026-08-20

A fresh, minimal strategy built to read as closely as possible to the trader's plain-language
6-rule statement of this setup: (1) wait for the 200 MA to gap fully above/below the MRC's outer
band, (2) gap above = short bias, gap below = long bias, (3) wait for price to wick into/touch the
band on the bias side, (4) then wait for a matching-direction QQE signal, entering on that
candle's confirmed close, (5) fixed 35-tick stop, take profit on the first touch of the opposite
band. Same exact MRC (fareidzulkifli SuperSmoother) and QQE (colinmck counter-based) ports as
`auto-reversion-strategy.pine` below, but deliberately skips all the bugfix machinery that file
accumulated (bias consecutive-bar confirm, touch lookback/expiry, mean-crossback invalidation,
cooldown, volume filter) — this is the rules as stated, nothing more. See
`../knowledge/strategies/mean-reversion.md` for how the two files relate.

**How to use it:** TradingView → open an MNQ1!/NQ1!/MGC1! chart → Pine Editor → paste this file's
contents → Add to Chart → Strategy Tester tab. Hand-written, not yet run through TradingView's
compiler — send me the exact error text if it throws one on first load.

**2026-08-20 bugfix:** trader caught a Short firing with the bias MA plainly sitting inside the
MRC channel, not gapping it. Cause: `bias` is a persistent state variable that got armed on a real
gap but was never reset once the MA drifted back inside the band — it stayed armed indefinitely
and fired off a much-later, unrelated touch+signal. Fixed: bias now clears the instant the gap
condition is no longer true, so rule 2 has to hold at the moment of entry, not just at some
earlier point.

## `auto-reversion-strategy.pine` — hardened/iterated version

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

## `gold-elephant-reversal-strategy.pine` — separate Gold strategy

Added 2026-08-20. Not part of the two-strategy NQ/MNQ plan above — a separate 5-minute Gold
reversal **strategy** the trader built independently ("elephant bar" reversal: a large, dominant-
body candle followed by a confirmation candle closing back through its body/range, filtered by a
20/200 SMA pair). Converted from an indicator (which tracked a manual win/loss array and its own
on-chart stats table) into a `strategy()` script by adding real `strategy.entry()`/
`strategy.exit()` calls alongside the original manual tracking — both run in parallel on the same
signals, so it now also shows up in TradingView's Strategy Tester (List of Trades, Performance
Summary) in addition to the original custom table. All signal/pattern logic is unchanged from the
trader's own tested version.

**How to use it:** TradingView → Gold chart, 5m → Pine Editor → paste this file's contents → Add
to Chart → Strategy Tester tab for the native backtest stats, or just watch the on-chart table
(same as the original indicator).

## `basic-trend-strategy.pine` — first scaffold, kept for reference

The very first script (2026-08-19) — a simple EMA-crossover trend-following **strategy** (not an
indicator) with an ATR-based stop/target, backtestable in the TradingView Strategy Tester. Not
the current direction (the actual goal turned out to be visualization, not a backtestable
strategy), but kept as the simplest possible baseline in case a strategy/backtest angle comes
back into play later.
