# Midnight Deviation — Marking Method

How the midnight deviation level/zone is actually drawn. This is the anchor referenced by the
`midnight_deviation` confluence in `confluences.yaml`. Captured from the trader's description —
**needs a worked chart example to fully confirm**, some details are still fuzzy (marked below).

## Setup

- Timeframe used for marking: **5-minute chart** — explicitly not the 1m or 10m.
- Reference clock: midnight, i.e. 00:00. Exact session/timezone convention is still unconfirmed
  (see "Open questions" below) — working assumption for now is the trader's local reference point
  around 00:00, likely UTC-aligned, possibly the Asia session open. **Do not hard-code a timezone
  in Pine Script until this is confirmed.**

## Base case — single reversal candle

1. Watch the 5-minute candle that forms starting at 00:00.
2. If that candle is **bearish**, and it is followed by a **bullish** candle (i.e. price
   immediately reverses up), that first bearish candle is the trigger candle.
3. Take the **top (high/open wick)** and the **bottom (low wick)** of that bearish candle.
4. Use those two points to draw a Fibonacci retracement/extension ("fib") from the candle —
   marked out both **up and down** from the candle.
5. The resulting fib levels are the **midnight deviation** — this becomes the primary point(s) of
   interest for the session.

*(Same logic applies mirrored for a bullish first candle followed by a bearish one — trader
described the bearish→bullish case explicitly; confirm the bullish→bearish mirror case is
identical in method.)*

## Extended case — multiple same-direction candles before the reversal

- If instead of one bearish candle you get a **run of several bearish candles** (e.g. three)
  before price shoots back up:
  - Mark the **high of the first** bearish candle in the run.
  - Mark the **low of the last** bearish candle in the run (the one immediately before the
    reversal/"shoot" back up).
  - These two points replace the single-candle high/low used in the base case, and the same
    fib-marking process is applied.

## Trend-day variant

- If a **trend is already running through midnight** (price isn't chopping/reversing but pushing
  directionally), the marking approach changes. Trader flagged this as a distinct case to define
  later — **not yet specified**. Do not assume the base-case method applies unmodified on trend
  days.

## Confirmed from chart example (2026-08-19, MNQ1! 5m, TradingView)

Trader supplied a live chart + the exact Fib Retracement tool dialog used to mark the deviation.
This confirms/refines the method above:

- The trigger candle is explicitly labeled on-chart as the **"Deciding 12:00AM candle"** — i.e.
  the 5m candle beginning at 00:00 is literally called "the deciding candle." This is the anchor
  candle referenced in the base case and the extended (multi-candle-run) case above.
- Chart annotation: **"Candles connected based on close."** This means when a run of same-
  direction candles precedes the reversal (the extended case), the candles are treated as
  connected/joined at their **close** prices, not by simple high/low wick extremes across the
  whole run. This refines step "Extended case" above — **needs one more confirmation pass**:
  whether the fib anchor points end up being close-to-close of the run's boundary candles, or
  close is just how the run is visually chained together while the actual anchor points are still
  the first candle's high and the last candle's low. Treat as open until the trader confirms
  which.

### Fib Retracement tool — exact settings

TradingView's built-in **Fib Retracement** drawing tool, anchored on the deciding candle's two
extremes (candle top = anchor "1", candle bottom = anchor "0", per the tool's default two-point
anchoring — confirm which physical price, high or low, maps to "1" vs "0" once a numeric example
is given).

- **Extend:** Don't extend
- **Reverse:** ON
- **Fib levels based on log scale:** OFF
- **Use one color:** ON (single bicolor swatch — red/teal, i.e. bearish/bullish coloring rather
  than per-level custom colors)
- **Levels (Style tab), enabled/checked only** — all other stock levels (0.5, 0.618, 0.75, 1.272,
  1.618, 2.272, 3.618, etc.) are left **unchecked/disabled**:

  | Level | Enabled |
  |-------|---------|
  | 1     | ✅ |
  | 0     | ✅ |
  | -1    | ✅ |
  | -2    | ✅ |
  | -2.5  | ✅ |
  | -3.25 | ✅ |
  | -3.5  | ✅ |
  | -4    | ✅ |
  | -4.5  | ✅ |
  | -5    | ✅ |

  So the tool is used purely as a way to **project a ladder of negative extension levels below
  the 0–1 anchor range** (1, 0, then -1 through -5 in irregular steps) — not as a classic
  0.5/0.618 retracement. This is consistent with "mark it up and then down" — the 0/1 anchor is
  the deciding candle itself, and the negative levels are what get projected out as the actual
  points of interest (the "midnight deviation" levels).
- Labels: Left-aligned, Values shown, font size 12.

**Still open:** exact price↔ratio mapping (which of candle-high/candle-low is ratio "0" vs "1"),
and whether "up and down" means this same tool is also drawn a second time projecting *upward*
(positive levels beyond 1) as a mirror, or whether "up and down" was already fully described by
this single negative-extension ladder. Needs one worked numeric example (actual prices + which
resulting level was traded from) to fully close out.

## Open questions (do not build/automate around these until confirmed)

- [ ] Exact timezone/session definition for "00:00" (trader is US-Georgia based but says they
      reference UTC; also unsure if this lines up with the Asia session open — needs to be
      pinned down precisely, since a Pine Script implementation needs an exact `timestamp()`/
      session string).
- [ ] Confirm mirrored bullish-candle-first case works identically.
- [ ] Trend-day variant of the marking method.
- [ ] Which candle extreme (high or low) maps to fib ratio "1" vs "0".
- [ ] Whether "connected based on close" changes the actual anchor points for multi-candle runs,
      or is just a visual chaining convention.
- [ ] Whether the upward projection is a second/mirrored fib draw, or already covered.
- [ ] Which of the enabled levels (1, 0, -1, -2, -2.5, -3.25, -3.5, -4, -4.5, -5) are actually
      treated as "the" points of interest vs. just visual reference — likely all of them feed the
      confluence stack with -2/-2.5 or similar being more heavily weighted, but this needs a
      worked trade example to confirm.

## Automation note

This is designed to be **fully automatable** (per trader's stated goal — no manual chart
marking, all confluences including this one auto-plotted). Once the open questions above are
closed out, the Pine Script implementation is straightforward: detect the 00:00 candle(s) per the
base/extended-case logic, take the two anchor prices, and replicate the same fixed ratio ladder
(1, 0, -1, -2, -2.5, -3.25, -3.5, -4, -4.5, -5) as horizontal levels/lines rather than using
TradingView's interactive Fib Retracement tool.

## Next step

One worked numeric example (actual candle prices + which level price was the actual entry) closes
out the remaining open questions above.
