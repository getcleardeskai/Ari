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
  uses `hlc3` + SuperSmoother, this bias filter is a plain SMA of `close`).
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
