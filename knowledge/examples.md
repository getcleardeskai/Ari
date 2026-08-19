# Trade Examples

Concrete reference cases — real trades, backtested setups, or annotated chart examples. These are
used to sanity-check model/rule changes against reality ("does this new weighting still catch
this known-good example / still avoid this known-bad one?").

## Template

Copy this block per example:

```
### YYYY-MM-DD — MNQ (or NQ) — Long/Short

- Midnight open: <price>
- Midnight deviation: <description, e.g. "deviated 40pts above midnight open by 3:15am ET">
- HTF confluence: <what zone, what timeframe, why it qualified>
- LTF refinement: <how it tightened down, final zone>
- Entry: <price/time>
- Stop: <price> (<pts/ticks> risk)
- Target: <price> (<R multiple>)
- Outcome: <win/loss/scratch, actual R>
- Notes: <what worked, what didn't, any confluence that should be re-weighted because of this>
```

## Examples (personal trades, this model)

_None logged yet — add the first one whenever you're ready._

## Reference/illustrative examples (generic concept confirmation, not personal trades)

Chart examples used purely to confirm/illustrate a concept definition (not this trader's own
trades on NQ/MNQ, and not necessarily around midnight). Logged for future reference in case a
concept needs re-checking, not for backtest weighting.

- **2026-08-19 — Gold Spot (XAUUSD) 1h, generic Breaker Block illustration.** Downtrend into a
  small bullish reaction (marked as the origin Order Block), price breaks above it, later returns
  and the zone (~3280-3300) is confirmed as a **Bearish Breaker Block** — price rejects it and
  continues down hard. Straightforward visual confirmation of the `breaker_block` definition.
- **2026-08-19 — generic structure diagram, BOS+MSS vs. BOS+ChoCH.** Two side-by-side structure
  sequences (HH/HL/LH/LL labeling) showing that "Market Structure Shift" and "Change of
  Character" mark the identical break point (the prior swing low/high that had been forming the
  trend) — confirmed these are alternate names for the same signal, folded into
  `change_of_structure` in confluences.yaml.
- **2026-08-19 — generic structure diagram, STH/ITH/LTH nesting.** Confirmed a third structural
  tier (Long-Term High, and implied Long-Term Low) above STH/STL and ITH/ITL, built the same way
  (multiple ITH flank a point to form an LTH). See "Long-Term High / Low" in ict-glossary.md.
- **2026-08-19 — generic chart, ERL/IRL illustration.** A stepping rally where each consolidation
  range's boundary becomes External Range Liquidity (ERL) and the inside of the range becomes
  Internal Range Liquidity (IRL) for the next leg — straightforward confirmation of those
  definitions.
- **2026-08-19 — EURUSD Monthly/Weekly/Daily/H4, multi-timeframe fib top-down example.** Worked
  example of the HTF→LTF scaling approach from `model-overview.md`, using a standard fib
  retracement (0/0.5/0.618/1, not the OTE-specific level set) drawn on the Monthly leg, carried
  down through Weekly (marks a consolidation box) and Daily (marks a support zone + rising
  trendline) to H4, where the fib's 0.618 level, the carried-down S/R zone, and the trendline all
  stack at the same price — marked as a "possible buy area." Good generic illustration of
  "alignment across timeframes = high-probability zone," the core mechanic this whole model is
  built on (though this example uses plain retracement fib, not the trader's own midnight-dev or
  OTE tools specifically).
