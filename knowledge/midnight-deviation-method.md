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

## Open questions (do not build/automate around these until confirmed)

- [ ] Exact timezone/session definition for "00:00" (trader is US-Georgia based but says they
      reference UTC; also unsure if this lines up with the Asia session open — needs to be
      pinned down precisely, since a Pine Script implementation needs an exact `timestamp()`/
      session string).
- [ ] Confirm mirrored bullish-candle-first case works identically.
- [ ] Trend-day variant of the marking method.
- [ ] Exactly how the fib is drawn "up and down" (which fib levels are considered the actual
      points of interest — 0.5? 0.618? 1.0? extensions beyond 1.0?) — trader said a worked
      example will clarify this.

## Next step

Trader is going to provide a chart example — once given, update this doc with the concrete
picture and remove the ambiguity noted above.
