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

**2026-08-20, later — price-in-gap filter + TP target dot:** trader flagged a cluster of Short
labels printing while price was clearly nowhere near the band (SMMA-side gating alone doesn't
check where price actually is — the SMMA is slow, so it can sit outside the outer band for a long
stretch while price bounces around well inside the channel the whole time). Added
`priceInGapShort`/`priceInGapLong`: the signal bar itself must have wicked into the shaded zone
between the inner and outer band, not just have the SMMA outside somewhere. Also added a TP target
dot (`plot.style_circles`) that tracks the opposite outer band every bar after a signal, until
price actually touches it, then clears until the next signal — purely visual, shows where the
setup expects price to go.

**2026-08-20, later still — stop level + more customizability:** added a stop level, on the SAME
side as entry (R2 for a short, S2 for a long), frozen at that band's value on the signal bar. If
price was already within `slBufferTicks` (default 25) of that band right at entry, R2/S2 would
leave almost no room, so a fixed `slFixedTicks` (default 100) from the entry price is used
instead; clears on a target hit, a stop hit, or a fresh opposite signal taking over. Also added:
independent on/off toggles for the SMMA-side gate and the price-in-gap gate (`enableMASideFilter` /
`enablePriceGapFilter`, for testing/comparison), a choice of which band the price-in-gap check
uses (Inner/Outer, `gapFilterBand`), and a tick-size override for symbols where
`syminfo.mintick` isn't the desired unit.

**2026-08-20, even later — stop now follows the band:** trader asked for the stop to "follow the
lowest band" instead of staying frozen at its entry-bar value. Changed `slLevel` from a one-time
computation at the signal bar into a live expression re-evaluated every bar, same pattern as the
TP dot — it now tracks S2/R2 continuously, with the near-band buffer/fixed-tick exception also
re-checked every bar (not just at entry). Not a one-directional ratchet: it moves wherever the
band (or the buffer fallback) currently sits, in either direction.

**2026-08-20, final round — opacity actually works, fixed-tick stop actually locks, TP always
bottom, QQE colors exposed:**
1. **Opacity bugfix:** every plot passed a hardcoded transparency number straight into
   `color.new()`, silently discarding whatever alpha the color picker itself was set to — changing
   opacity visibly did nothing. Added an explicit opacity % input per element (inner/outer band,
   band shade, mean line, SMMA, QQE labels, TP dot, stop level), each actually wired into its plot.
2. **Fixed-tick stop bugfix:** the tick-stop fallback was `close - slFixedTicks*tick`, recomputed
   off the live `close` every bar — that's not "fixed," it's a very tight trail that moves with
   price. Added `slIsFixed`/`slFixedLvl` state: the first bar price comes within `slBufferTicks` of
   the band, the fixed level is computed ONCE and locked for the rest of the trade, not
   recalculated afterward even if price drifts back away from the band.
3. **TP always at the bottom line:** per trader request, `tpLevel` now always tracks the bottom
   outer band (S2) for either direction, instead of the opposite-of-entry band (which was top for a
   long). Deliberate change, not a bugfix — flagged since it changes what the dot means for longs.
4. **QQE colors:** `colQQELong`/`colQQEShort` inputs replace the hardcoded green/red on the
   Long/Short labels.

**2026-08-20, ground-up rewrite — trade tracking + session-based exit:** trader took a pass at
rewriting this file directly (adding session logic, a flat hard-tick stop, TP-band-by-location) but
reported it back "takes no trades... can't even see SL or TP." Root cause: the draft's
`entryLong`/`entryShort` required `inSession` (the full "0930-1600" window) to be true for ANY
entry — restricting trading to a ~5.5 hour daytime window. With futures trading nearly 24/5 and
the trader testing overnight/extended hours, that gate alone produced zero entries; with zero
entries `tradeDirection` never left 0, so the TP/SL lines (which only plot when a trade is active)
never had anything to draw — same root cause explaining both complaints at once.

Rebuilt on top of the trader's own draft, keeping its structure and intent, fixing:
- **Entries no longer require `inSession`.** Blocked ONLY in the `sessionBufferMinutes` window
  right before the session's close (`blockedNow`, built as a standalone session string covering
  just that window, e.g. "1540-1600" — checkable at any hour, not just while already in-session).
  Matches "not take trades within 20 minutes of market close" literally, not "only trade market
  hours." `sessionEnded` (the RTH-window closing) still force-flattens any open trade ("stop out on
  market session change").
- **Stop-loss simplified to a flat hard-tick distance** (`hardStopTicks`, default 250, no
  band-following/lock complexity) — the old MRC-band-following stop logic was removed entirely per
  request.
- **TP band selection:** outer band (R2/S2) if price was outside the MRC when the signal fired,
  inner band (R1/S1, the closer one) if price was inside — this was already correct in the
  trader's draft, kept as-is.
- **Opacity actually wired for every plot** — the Mean line and 200 SMMA plots bypassed
  `color.new()` entirely in the draft (raw color, no opacity effect at all); now every element
  routes through it, plus two new inputs (`meanOpacity`, `maOpacity`) to control them.
- **Decluttering added:** `declutter` + `idleOpacity` (default 90% transparent) fades the MRC
  bands/mean/SMMA/shading whenever nothing is active, snapping back to each element's own
  configured opacity the instant the SMMA goes light-blue or a trade is open
  (`conditionsActive = maOutsideMRC or tradeDirection != 0`).
- QQE Long/Short colors (`qqeLongColor`/`qqeShortColor`) were already exposed correctly in the
  trader's draft, unchanged.

Pure visual indicator, no `strategy.*` — plots signals and alerts only, doesn't trade.

**2026-08-20, another ground-up rewrite — TPT session logic, flat tick stop, TP-by-location:**
trader wrote yet another independent version directly (dropped the RTH-restriction bug from the
previous rewrite entirely — this one correctly used `hour(time, "America/New_York")`/
`minute(time, "America/New_York")` from the start, a cleaner approach than the session-string
surgery in the version before it) with: no session restriction at all except a "TPT" 5pm ET flat
deadline (new trades blocked in the 20 minutes before, any open trade force-cleared at the
deadline itself), a flat configurable tick stop-loss, and TP fixed to the inner band
(R1 for longs, S1 for shorts, tracked live). Reported back "does everything I want, just doesn't
take as many trades as it could" with a chart example of a missed setup.

**Root cause:** `qqeLong`/`qqeShort` required the price-in-gap touch (`gapLongOk`/`gapShortOk`)
and the QQE cross to land on the exact same bar. QQE (RSI-smoothed + ATR trailing band) is
inherently laggy — its counter often doesn't hit 1 until several bars after price already wicked
into the gap and started pulling back, so by the actual signal bar price is usually back inside
the zone and the same-bar check silently fails on a perfectly valid setup. (Same root bug already
found and fixed once before in this project, in `auto-reversion-strategy.pine` — reintroduced here
in a fresh independent rewrite.) Fixed with touch memory: `longArmed`/`shortArmed` persist across
however many bars it takes for the signal to print, as long as the bias (SMMA side) that armed
them keeps holding — clearing only when the bias itself breaks or a matching signal consumes the
touch. Also removed two small pieces of dead code (`crossLongBand`/`crossShortBand`, an unused
`ThreshHold` input) while in there.

**2026-08-20, reverted:** trader pasted back the earlier "price-in-gap filter + TP target dot"
version (the state right before the stop level was ever added — no stop, no opacity system, no TP
always-bottom, and neither of the two ground-up session rewrites) and said to undo everything since
then: "this one was golden," it caught a trade the later TPT-session/inner-band-TP rewrite had
missed. File restored to that exact content — direction-agnostic-bug already fixed, price-in-gap
filter present (same-bar check, no touch memory), TP target dot tracking the opposite outer band,
no stop-loss logic at all, hardcoded QQE label colors. The same-bar touch/signal bug described just
above still exists in this restored version (it predates that fix) — left as-is per the explicit
revert request, not silently reapplied; flagged in case the trader wants that specific fix layered
back on top of this version once behavior here is confirmed good.

**2026-08-20, merged:** trader clarified the ask — keep the golden version's entry/signal logic
exactly as-is (that's what was taking trades correctly), but layer the TPT session rule, the fixed-
tick stop, and the inner-band TP from the later draft on top of it. Not a rewrite of WHEN a signal
fires — `qqeLong`/`qqeShort` are byte-for-byte the same condition as the golden version
(`maBelowOuter`/`maAboveOuter` + `priceInGapShort`/`priceInGapLong`, same-bar check, no touch
memory), with exactly one addition: `allowNewTrade` (the TPT pre-close buffer) ANDed in. Everything
downstream of a signal firing — TP/SL tracking, the TPT force-flatten at the deadline — is the
trader's own TPT-draft code, also unchanged. Left out of the merge: the enable/disable filter
toggles and the Inner/Outer `gapFilterBand` selector from the TPT draft (not part of what was asked
for — "session rules, new SL, new TP" — easy to add back if wanted).

**2026-08-20, TP-by-location + fixed 1:1 SL:** trader's next hand-written iteration, pasted in and
saved as the file's current content. TP now depends on where price was relative to the MRC at the
signal: R2/S2 (outer) if the signal fired outside the MRC, R1/S1 (inner) if inside — then follows
that selected band live. SL changed from a flat tick count to a 1:1 risk/reward computed ONCE at
entry from the initial TP distance (e.g. entry 7000, initial TP 7010 → SL 6990) and held fixed
even as the live TP (and thus the R:R) moves afterward. Entry/signal logic (`qqeLong`/`qqeShort`,
`maBelowOuter`/`maAboveOuter` + `priceInGapShort`/`priceInGapLong`) and the TPT session rule are
unchanged from the merged version above.

**2026-08-20, configurable ratio + trailing SL:** trader asked to change the fixed 1:1 SL to a
configurable ratio (`slRatio`, default 0.7 — SL distance = 0.7x the TP distance at entry) and to
have the SL trail the TP's own movement afterward instead of staying frozen: `slTrailSpeed` (default
0.5) — for however many points the TP has moved from its entry-time value, the SL moves
`slTrailSpeed` x that many points from ITS entry-time value, in the same direction. New state vars
`initialTPTracked`/`initialSLTracked` snapshot both at entry so the live trail has a fixed reference
point to measure movement from. Not a ratchet, matching the earlier "stop follows the band" design
in this file's history: if the TP band gives back ground, the SL follows it back too, proportionally
— same live-tracking philosophy as the TP itself, just at half speed by default and applied to the
SL's own starting point rather than the band directly.

**How to use it:** TradingView → open your chart → Pine Editor → paste this file's contents →
Add to Chart. Hand-written, not yet run through TradingView's compiler — send me the exact error
text if it throws one on first load.

## `mrc-200sma-qqe-strategy.pine` — strategy port of the indicator above

Added 2026-08-20. Same entry/signal logic, TP-by-location selection, and fixed-1:1-SL math as
`mrc-200sma-qqe-indicator.pine` (TP-by-location version) — nothing about *when* a signal fires or
*what* TP/SL get computed to was changed. Converted to a backtestable `strategy()` following the
same pattern already used in this repo for `gold-elephant-reversal-strategy.pine`: the original
manual state tracking (`qqeDir`/`entryPriceTracked`/`slLevel`/`tpLevel`/`tpBand`) is kept exactly
as-is and still drives the plots, with real `strategy.entry()`/`strategy.exit()` calls added
alongside it, driven off those same variables, so backtest fills match what the indicator's plots
already show. `process_orders_on_close = true` so entries fill at the signal bar's close (matching
`entryPriceTracked := close`); `pyramiding = 0` blocks same-direction stacking, while an opposite-
direction signal reverses the position — matching the indicator's own manual tracking, which always
let a fresh signal overwrite the tracked state regardless of what was currently held. The TPT
deadline force-flattens via `strategy.close_all()` in addition to resetting the manual state.

**2026-08-20, configurable ratio + trailing SL:** same change as the indicator above, ported
identically — `slRatio`/`slTrailSpeed` inputs, `initialTPTracked`/`initialSLTracked` state, SL now
trails the TP's movement at `slTrailSpeed` instead of staying frozen at its entry-time value. The
real `strategy.exit()` calls already read `slLevel` live each bar, so they automatically pick up the
trailing value — no separate change needed there.

**How to use it:** TradingView → open your chart → Pine Editor → paste this file's contents →
Add to Chart → Strategy Tester tab for backtest results. Hand-written, not yet run through
TradingView's compiler — send me the exact error text if it throws one on first load.

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
