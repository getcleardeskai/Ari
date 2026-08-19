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

## Method B — Manipulation Leg (2026-08-19, more discretionary)

There are **two** valid ways to draw the midnight deviation. Everything above (base case +
extended/chained-candle case) is **Method A**. There is also **Method B**:

- A **manipulation leg** is the higher-low (in a bullish context) or lower-high (in a bearish
  context) that forms right before or after a large move at/around midnight.
- Draw the same fib-ladder tool off the two points of that leg instead of off the candle-run high/
  low used in Method A.
- This is explicitly called out as **more discretionary** than Method A — identifying what counts
  as "the" manipulation leg (vs. just noise) requires judgment, not a fixed rule. Treat this as a
  harder confluence to automate cleanly; may need a scoring/heuristic approach rather than a
  strict detection rule, or may need to stay semi-manual longer than Method A.
- Not yet specified: exactly when to prefer Method B over Method A on a given session — trader has
  not yet given a rule for which method applies when. **Open question**, do not assume a default.

## Level significance & discretion

- General rule: **the higher the level number, the higher the probability** (i.e. -3.25 through
  -5 the reversion band are read as higher probability than the -1 to -2.5 pullback band,
  consistent with the level-meaning section below) — but application is **discretionary**, not a
  hard automated trigger.
- Worked example given by the trader: a session had a "perfect" setup at level **-5**, but in the
  lead-up there was unusually high volume, so the trader deliberately waited for confirmation
  (see `volume_spike_reaction` in `confluences.yaml`) rather than blindly entering — out of
  concern the level would simply get blown through by that volume rather than reacting. Ended up
  not taking the trade. This illustrates that **high pre-level volume can be a reason to withhold
  entry**, not just a trigger to enter — i.e. the volume filter cuts both ways depending on
  context, which is inherently discretionary and hard to reduce to one automated rule. Flag this
  as a nuance to capture in backtesting notes rather than hard-code naively.

## Do not trade news

- Explicitly and repeatedly stressed by the trader (echoing their mentor): **never trade around
  news events.** This should be an **automated filter** — see the `news_filter` confluence in
  `confluences.yaml`. Implementation approach still TBD (Pine Script has no native news feed —
  likely needs either a manual high-impact-news time input, a known recurring schedule e.g. FOMC/
  NFP/CPI, or an external data feed/session blackout list).
- Related pattern the trader described: a **small drawdown followed by a large expansion** around
  a level (example given: ~15 tick drawdown followed by an almost 500 tick expansion) is
  frequently associated with these high-volume/news-driven moves and "typically" precedes
  incredible moves. See `volume_expansion_pattern` in `confluences.yaml`.

## Confirmed from chart example (2026-08-19, MNQ1! 5m, TradingView)

Trader supplied a live chart + the exact Fib Retracement tool dialog used to mark the deviation.
This confirms/refines the method above:

- The trigger candle is explicitly labeled on-chart as the **"Deciding 12:00AM candle"** — i.e.
  the 5m candle beginning at 00:00 is literally called "the deciding candle." This is the anchor
  candle referenced in the base case and the extended (multi-candle-run) case above.
- **"Candles connected based on close" — resolved.** This is a visual/conceptual chaining
  convention, not an alternate price source. Starting from the 00:00 anchor candle (say it's
  red), you keep chaining every consecutive same-color candle to it — "like a string" — until you
  hit an opposite-color candle, which breaks the chain ("a rotting part"). That determines how
  long the run is (and therefore its size). **The actual anchor prices are unchanged from the
  Extended Case above: first candle's wick high + last candle's (in the chain) wick low** — close
  price is not itself used as an anchor point, it's just how the run of candles is identified.

### Fib Retracement tool — exact settings & anchor mapping (resolved)

TradingView's built-in **Fib Retracement** drawing tool, drawn **once** — a single two-point tool
anchored on the deciding candle's wick high and wick low (not open/close). Trader confirmed this
is deliberately one tool doing both directions (not two separate fibs drawn up and down) — that
was a UX pain point in how they currently do it manually, which is exactly why this should be
automated in Pine Script instead of using the interactive tool at all.

- **Anchor "0"** = the point the deviation "sits" at — i.e. the near/reference wick, the level
  price is currently closest to.
- **Anchor "1"** = the far wick — the very **first level of support/resistance** price can
  rebound off.
- Both anchors are **wicks** (high/low), confirmed — not open/close.
- **Extend:** Don't extend
- **Reverse:** ON
- **Fib levels based on log scale:** OFF
- **Use one color:** ON (single bicolor swatch — red/teal, bearish/bullish)
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

  So the tool projects a ladder of negative extension levels below/beyond the 0–1 anchor range —
  not a classic 0.5/0.618 retracement.
- Labels: Left-aligned, Values shown, font size 12.

### What each level means (trader's read, 2026-08-19)

- **Levels 1 through ~2.5** ("1" through "-2.5"): **pullback zone** — areas where price can pull
  back / minor support-resistance reactions, not necessarily the big move.
- **Levels -3.25, -3.5, -4, -4.5, -5**: **reversion zone** — where the trader is looking for the
  actual big reversion move.
- Reactions are typically visible at **each** individual level, whether or not it lines up with
  another confluence — i.e. these levels have some standalone predictive value, and stacking
  other confluence on top of one just increases confidence/precision, per the original "alignment
  = tight entry" framework in `model-overview.md`.
- **Not yet quantified:** exact per-level weight. The pullback-vs-reversion split above gives a
  first-pass grouping — reasonable starting point is weighting the -3.25 to -5 band higher for
  the "big move" 1:6–1:10 setups this model is built around, and the 1–2.5 band lower/as a
  secondary pullback signal. To be tuned via backtesting.

## Open questions (do not build/automate around these until confirmed)

- [ ] Exact timezone/session definition for "00:00" (trader is US-Georgia based but says they
      reference UTC; also unsure if this lines up with the Asia session open — needs to be
      pinned down precisely, since a Pine Script implementation needs an exact `timestamp()`/
      session string).
- [ ] Confirm mirrored bullish-candle-first case works identically (i.e. same rules, colors
      flipped — not yet explicitly walked through with an example).
- [ ] Trend-day variant of the marking method.
- [ ] Per-level weighting within `midnight_deviation` (pullback band vs. reversion band) —
      pending backtest data.
- [ ] When Method A (candle-run) vs. Method B (manipulation leg) applies — no rule given yet for
      which to use on a given session.
- [ ] How to systematically identify a "manipulation leg" for Method B (currently pure
      discretion).
- [ ] News-event detection/blackout implementation approach for `news_filter`.

## Resolved (previously open, now confirmed 2026-08-19)

- ~~Which candle extreme maps to fib ratio "1" vs "0"~~ — both are wicks; "0" = near/reference
  wick, "1" = far wick / first support-resistance level.
- ~~Whether "connected based on close" changes the anchor points~~ — no, it's just the chaining
  convention for identifying the run; anchors are still first-candle-high / last-candle-low.
- ~~Whether the upward projection is a second/mirrored fib draw~~ — no, it's one single fib tool;
  the ladder above (1, 0, -1 ... -5) already covers it.

## Automation note

This is designed to be **fully automatable** (per trader's stated goal — no manual chart
marking, all confluences including this one auto-plotted, and specifically to stop having to
place the fib tool by hand every session). The math is now fully specified:

1. Detect the 00:00 candle and, if needed, chain consecutive same-color candles to it until an
   opposite-color candle breaks the chain (per the resolved logic above).
2. Anchor 0 = near wick, anchor 1 = far wick, using the run's boundary candles.
3. Compute `level_price = anchor0 + (anchor1 - anchor0) * ratio` for each ratio in
   `[1, 0, -1, -2, -2.5, -3.25, -3.5, -4, -4.5, -5]` and plot as horizontal lines — no need to use
   TradingView's interactive Fib Retracement tool at all once this is in Pine Script.

Remaining blockers before coding this are just the timezone/session definition and the trend-day
variant, both still open above.

## Next step

Nail down the 00:00 session/timezone definition and the trend-day variant, then this confluence
is ready to move into `pinescript/`.
