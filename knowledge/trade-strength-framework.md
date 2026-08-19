# Trade Strength & Confluence — Checklist

The general ICT framework for what makes one setup stronger than another: confluence is multiple
independent concepts aligning in the same direction. No single concept guarantees a win, but more
high-quality aligned factors = stronger setup. Strong trades combine **location, liquidity,
timing, and confirmation** rather than relying on one signal.

Captured 2026-08-19. Note: the source material included a letter-grade scoring table
(A+/Average/Low-Quality); **that grading scheme is intentionally excluded here** per instruction —
we'll define our own scoring approach later once weights are tuned in `confluences.yaml`. This
doc keeps only the underlying checklist of factors.

## The factors

1. **Higher Timeframe Bias (HTF Narrative)** — Daily/4H/1H structure, bullish/bearish bias, HTF
   PDAs, major liquidity targets. An LTF setup is stronger when it aligns with HTF direction.
2. **Liquidity Target (Draw on Liquidity)** — where price is likely trying to go: BSL/SSL, ERL,
   IRL, equal highs/lows, previous day/week highs-lows. Stronger trade = clear liquidity
   objective.
3. **Premium & Discount Location** — longs preferred in Discount, shorts in Premium; entries near
   the 50% EQ are weaker. See `premium_discount_zone` in `confluences.yaml` (hard filter).
4. **Higher Timeframe PDA** — a valid point of interest giving price a reason to react: FVG, OB,
   Breaker, Mitigation Block, BPR, RB, IFVG. Stronger when the LTF entry occurs inside one.
5. **Liquidity Sweep** — evidence price took stops before reversing/continuing: taking a
   prior high/low, sweeping equal highs/lows, running ERL. Often the manipulation phase before the
   real move.
6. **Market Structure Confirmation** — MSS, COS, BOS, or strong displacement after price reaches a
   key area — confirms reaction rather than pure continuation-through.
7. **Displacement & Imbalance** — large impulsive candles, strong rejection, a new FVG, aggressive
   move away from the level. Shows intent, creates the retracement entry area.
8. **Time & Session Alignment** — London Kill Zone, New York Kill Zone, market open,
   session highs/lows. Setups during active trading windows are generally stronger than low-volume
   periods. **Cross-reference:** this is where session/kill-zone timing could eventually connect
   to the still-open midnight/session-timezone question in `midnight-deviation-method.md`.
9. **Lower Timeframe Entry Model** — once everything above aligns, LTF (5m/1m) is used for
   precision: MSS, FVG entry, OB entry, Breaker entry, rejection confirmation. LTF should refine
   the trade, not create the whole idea.

## Rough shape of a strong setup

`HTF Bias → Liquidity Target → Premium/Discount Location → HTF PDA → Liquidity Sweep →
MSS/Displacement → LTF Entry`

More of these aligning = higher setup quality — this is the general "confluence stacking"
principle the whole model (`model-overview.md`, `confluences.yaml`) is built around; the 9 factors
above are effectively categories that the individual confluences we're tracking fall into.

## What's still open

- [ ] How to turn "more factors aligned = stronger" into an actual numeric score — this connects
      directly to the confidence-score requirement in `automation-requirements.md`.
- [ ] Our own scoring/grading bands (deliberately deferred, replacing the source's A+/Average/Low
      table).
