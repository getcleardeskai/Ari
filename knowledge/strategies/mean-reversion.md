# Auto Reversion (Mean Reversion Strategy)

Status: **rules captured 2026-08-19, ready to formalize into Pine Script.** Trader calls this
strategy "Auto Reversion" specifically — use that name going forward. This is one of the two
strategies in `../automation-architecture.md`; runs alongside `trend-following.md` and is meant
to eventually confirm/deny it.

## Indicators involved

- **MRC** ("the big outward band") — **RESOLVED 2026-08-19**, trader supplied the actual source:
  "Mean Reversion Channel" by fareidzulkifli (Pine v4, MPL 2.0, publicly shared). It's an Ehlers
  SuperSmoother of `hlc3` (default) over a 200-bar lookback as the mean line, with band width =
  SuperSmoother of True Range over the same lookback, scaled by `pi * multiplier` — inner band
  multiplier 1.0, outer band multiplier 2.415. Only **2** real band levels (inner R1/S1, outer
  R2/S2), not 3 — an earlier ATR-multiple approximation was wrong on both the formula shape and
  the band count, which is why the first backtest attempt produced zero trades. Now ported exactly
  in `../../pinescript/auto-reversion-strategy.pine`.
- **200-period moving average** (the white line running through price) — the bias/validity
  filter, not the overextension signal itself. Separate from MRC's own internal mean line (MRC
  uses `hlc3` + SuperSmoother). **Correction 2026-08-19:** confirmed from the trader's own
  TradingView object list this is an **SMMA** (Smoothed MA), not a plain SMA — SMMA is what Pine
  calls RMA (Wilder's smoothing, `ta.rma()`). The first Pine port used `ta.sma()`, which was
  wrong and likely a real contributor to bias conditions rarely/never triggering — fixed.
- **Hawkeye Volume** — the volume histogram at the bottom with a white average-volume line. We
  don't need to replicate the full Hawkeye indicator (it does its own bar-by-bar climax
  classification) — the actual rule used here only needs **current volume vs. its own moving
  average**, which is simple to build directly (`volume >= ta.sma(volume, N)`).
- **QQE** — **RESOLVED 2026-08-19**, trader supplied the actual source: "QQE signals" by colinmck
  (Pine v4, MPL 2.0). Same underlying RSI/EMA/ATR math as the trend strategy's QQE, but the signal
  itself is extracted differently — a counter that increments while the trend-line/RSI
  relationship holds and resets to 0 otherwise; the signal fires on the bar the counter first hits
  1 (i.e. the relationship just turned true). This is subtly different from `ta.crossover` and is
  now matched exactly in the Pine port.

## Setup validity — ALL of the following must be true (long example; short is the exact mirror)

1. **Bias filter:** the 200 MA must be **fully below the entire MRC band**. If any part of the MA
   is inside or above the band, longs are not valid.
2. **Location filter:** the setup candle must be sitting in the **lower/outer sub-band** of the
   MRC (the downside-extended part of the channel) — this is what "overextended" means concretely
   for this strategy.
3. **Signal:** wait for a QQE long/buy signal as price comes back up out of that lower band.
4. **Volume confirmation:** volume must be **at or above** the average-volume line, either:
   - on the same candle as the QQE signal, OR
   - within the next **couple of candles after** the signal (a delayed bullish volume
     confirmation still counts).
   - If volume never confirms in that window, the setup is **invalid** — no trade. (This is
     exactly what the third reference screenshot shows: a QQE signal that never got volume
     confirmation → invalid, do not take.)
5. **Entry timing:** always enter on **candle close**, once every box above is checked — never on
   the signal appearing mid-candle. Direct continuity with the "no painting" principle already
   used in the trend strategy.

### Mirror for shorts
- 200 MA fully **above** the entire MRC band.
- Setup candle in the **upper/outer sub-band**.
- QQE short/sell signal.
- Same volume confirmation rule.
- Same candle-close entry timing.

## Exit rules

- **Stop loss:** ~25 ticks as a placeholder, or "the last low" (for longs — last high for
  shorts) as an alternative — **not yet decided which**, trader flagged this as something to
  refine later. Building both as options: a fixed-tick stop and a structure-based (last
  swing-low/high) stop, selectable, defaulting to the fixed-tick version for now.
- **Take profit:** the tip of the **opposite band** as price enters it (for a long: the upper
  band; for a short: the lower band). Exact band level (the MRC appears to have multiple nested
  bands) still needs pinning down — will implement as a selectable "target band" and adjust once
  we see it plotted against a real MRC.

## Session

- **24 hours a day** — no session restriction, trades every valid setup whenever it occurs
  (consistent with 24hr futures trading).

## Can this be done in Pine Script?

**Yes — no third-party backtester needed.** Every piece here (200 MA, an MRC-style multi-band
channel, a volume-vs-its-average check, QQE, close-confirmed entries, tick or structure-based
stops, band-level take-profit) is standard, buildable Pine. The only real open item is getting the
MRC band math to actually match your specific indicator — everything else is mechanical.

## 2026-08-19 — v1 locked in: simple, long-only

Trader confirmed the diagnostic approach found real bugs (SMMA vs SMA, outer multiplier 1.5 vs
2.415) and asked to go simple for the first real version rather than keep iterating on the full
5-rule/toggle system. Locked-in v1 rules, implemented in
`../../pinescript/auto-reversion-strategy.pine`:

1. **Bias:** entire MRC channel sits above the 200 MA (equivalently: MA fully below the outer
   band) — same condition as before, just phrased the other way round.
2. **Touch (persistent, not same-bar):** price touches the outer band at some point while bias
   holds. Explicitly confirmed: the touch and the QQE signal do **not** need to happen on the same
   candle — once touched, the setup stays "armed" until a signal arrives or bias breaks.
3. **Signal:** the next QQE long signal after a touch, however long that takes.
4. **Timing:** confirmed bar close only.
5. **Long only** for v1 — no shorts, no volume filter. Both explicitly deferred to a later
   version once this one is validated.

**Exit:** take profit at the **inner** top band (R1), continuously updated to the live level each
bar (not frozen at entry) — matches "exit at candle touching inner part of top MRC band"
literally. Stop loss stays as a safety net (fixed ticks by default).

The diagnostic funnel table and rule toggles from the debugging phase were removed from the
script now that the ruleset is settled — they did their job (found the real bugs) and would just
be clutter now. Can be added back if useful once shorts/volume are reintroduced.

## 2026-08-19 — comparison against a simplified version, diagnostics added (superseded above)

Trader shared a version (written elsewhere) that produced trades where the full port didn't.
Diffed it directly: that version only implements 2 of the 5 rules (bias + QQE signal) — it drops
the location filter (candle tagging the outer band) and the volume confirmation entirely, and
uses a tighter outer-band multiplier (1.5 vs. the real MRC's default 2.415). That's why it fires
more often — fewer, looser conditions — not because anything in the fuller port was broken. Worth
being explicit: dropping volume confirmation means it would take the exact trade the trader
called out as invalid (QQE signal with no volume behind it).

(**Correction 2026-08-19, later:** confirmed directly from the trader's real MRC settings dialog —
their actual Outer Channel Size Multiplier is **1.5**, not the public script's own default of
2.415. So that simplified version's 1.5 wasn't arbitrary — it happened to match the trader's real
config on this one setting, even though it still dropped the location and volume rules entirely.
`outerMult` default corrected to 1.5 in the Pine port; everything else — hlc3 source,
SuperSmoother filter, 200 lookback, inner mult 1.0 — already matched.)

Rather than pick a side, added to `../../pinescript/auto-reversion-strategy.pine`:
- A **diagnostic funnel table** (bottom-left on the chart) counting how many confirmed bars pass
  each stage — bias → +location → +QQE signal → +volume→entered — so it's possible to see exactly
  where the funnel is choking instead of just "zero trades."
- **Toggles** to disable the location and volume rules independently (`useLocationFilter`,
  `requireVolume`), so their actual effect on trade frequency can be tested empirically.
- A **bias MA type selector** (SMMA vs. SMA) instead of asserting one is correct.

## What's still open

- [x] MRC exact formula — resolved, see above.
- [x] QQE exact signal logic — resolved, see above.
- [ ] Stop-loss: fixed ticks vs. last swing low/high — which, and if fixed, confirm ~25 ticks.
      (Both implemented as a toggle, defaulting to fixed-ticks.)
- [ ] Take-profit: which specific band level — defaulted to the outer band (R2/S2), matching "the
      second band" (inner=1st, outer=2nd). Confirm or correct once backtest results are in.
- [ ] Volume average length (Hawkeye's default, or whatever you're actually using) — defaulted to
      20.
- [ ] How many candles counts as "the next couple" for delayed volume confirmation — defaulted to
      3.

## Reference examples (from chart screenshots, 2026-08-19)

- **Valid long example** (2nd screenshot, Micro Gold Futures, 1m): 200 MA below MRC, candle
  tagged the lower band, QQE long signal, volume confirmed → valid entry per all 5 rules above.
- **Invalid example** (3rd screenshot, Micro Gold Futures, 1m, different time window): a setup
  that looks similar but fails one of the validity checks (trader confirmed this is NOT a valid
  trade) — exact failing condition not yet pinned down from the image alone; worth a follow-up
  pass once the Pine Script is running so we can check it against the actual computed
  conditions.
