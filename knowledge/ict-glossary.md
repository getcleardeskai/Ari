# ICT Concept Glossary

Reference definitions for every ICT concept fed into this model so far. This is the "what is it"
layer — weighting/rating is deliberately **not** addressed here (per trader's instruction,
2026-08-19: "ignore name stuff and any star/rating stuff, we will edit this later, mostly just
take notes at WHAT confluences exist"). Weights live in `confluences.yaml` and get tuned later.

Each concept below that acts as an actual detectable confluence has a matching entry in
`confluences.yaml` — check there for its id/category/weight.

## PDA (Price Delivery Array) — umbrella term

"PDA" is used throughout below as the general term for any of these reactive zones — FVG, IFVG,
BPR, Rejection Block, Order Block, Breaker Block. When a definition says "retraces into a PDA," it
means any of these.

## Fair Value Gap (FVG)

Forms when price moves so aggressively in one direction that it leaves an imbalance — a gap
between the first and third candle of a 3-candle sequence where little to no trading occurred.
Can form bullish or bearish. When price later retraces into an FVG, it often reacts from that
area before continuing in the original direction — support or resistance.

## Inverse Fair Value Gap (IFVG)

Forms when price completely trades through a previously respected FVG, showing the imbalance
failed. The old FVG flips role: a broken bullish FVG often becomes resistance, a broken bearish
FVG often becomes support. Price returning to an IFVG often reacts there before continuing in the
direction of the break — high-probability entry area.

## Balanced Price Range (BPR)

Forms when a bullish and bearish FVG overlap, creating a zone where buying and selling pressure
are more balanced. Because both imbalances occupy the same price range, it often acts as a strong
point of interest. Watch for a reaction aligned with current market structure when price retraces
into it.

## Protected Low / High + Catalyst (PLC / PHC, PL / PH)

A confirmation model layered on top of any valid PDA (FVG, IFVG, BPR, etc.) — waiting for this
instead of entering on the first touch significantly increases probability.

- **Bullish trend:** price retraces into the PDA → the first rejection is the **Protected Low
  Catalyst (PLC)**. If price retraces again, respects the same PDA, and forms a **higher low**
  above the PLC, that higher low becomes the **Protected Low (PL)** — confirms buyers are still
  defending the imbalance, increasing probability of resumption higher.
- **Bearish trend (mirrored):** first rejection from a bearish PDA = **Protected High Catalyst
  (PHC)**. A subsequent **lower high** below the PHC, off the same PDA, = **Protected High (PH)**
  — confirms sellers still in control.
- Trader's explicit caveat: **this is the strongest confluence but not the strongest decider on
  its own** — trading PLC/PL or PHC/PH alone still requires correct discount/premium positioning
  (see Premium/Discount Zone below) and correct trend/structure alignment. Many traders treat
  PLC/PHC confirmations as one of the highest-probability entry models, but not a standalone
  green light.

## Rejection Block (RB)

Forms when price attempts to continue in one direction but is immediately rejected — the
candle(s) left behind represent strong buying/selling pressure. When price retraces into an RB it
often reacts and continues in the direction of the original rejection. Strong PDA.

## Inverse Rejection Block (IRB)

Forms when price breaks through a previously respected Rejection Block, showing the rejection
failed. The RB flips role (support↔resistance) same as IFVG. High-probability continuation area
after a shift in order flow.

## Order Block (OB)

The last opposing candle before a strong displacement move that breaks structure or creates a
significant imbalance — presumed area where institutions entered before the impulsive move. One
of the strongest PDAs for continuation entries when aligned with overall trend.

## Breaker Block (BB)

Forms when an Order Block fails and price breaks through it — signals a shift in order flow. The
old OB flips role (support↔resistance), same pattern as IFVG/IRB. Strong continuation entry after
a change in market structure.

## Break of Structure (BOS)

Occurs when price breaks a previous swing high in a bullish trend (or swing low in a bearish
trend) — **confirms the existing trend is continuing**. Distinct from MSS/COS below, which
signals reversal. After a BOS, traders typically wait for a retrace into a PDA before looking for
continuation entries.

## Change of Structure (COS) / Market Structure Shift (MSS)

Occurs when price breaks the **most recent Protected Low** in a bullish trend (or **most recent
Protected High** in a bearish trend) — signals the current trend **may be ending**, control has
shifted, reversal or deeper retrace becoming more likely. After an MSS, traders wait for a retrace
into a PDA before entering in the new direction.

**Important distinction this clarifies vs. earlier notes:** BOS ≠ CHoCH/MSS in trigger — BOS
breaks a swing high/low (continuation), MSS/COS breaks a *Protected* High/Low specifically
(reversal). The original `market_structure` confluence entry in `confluences.yaml` should be read
with this more precise distinction going forward.

## Range Settlement (RS) — indicator

Confirms where the market is likely to expand next, after price finishes building liquidity
within a defined range. Key idea: **wait for acceptance outside the range rather than assuming
the first breakout is valid.** Once price settles beyond the range, look for retracements into
PDAs in the new direction for continuation entries.

## Short-Term High / Low (STH / STL)

Smallest form of market structure — temporary swing points.

- **STH:** a candle's high that the candles immediately before and after fail to trade above.
  Temporary resistance.
- **STL:** mirrored — a low the surrounding candles fail to trade below. Temporary support.
- Create short-term liquidity (stops cluster above STH / below STL) — potential price targets.
  More significant when they form near a PDA or premium/discount zone.

## Intermediate-Term High / Low (ITH / ITL)

Larger/more significant structure built from multiple STHs/STLs.

- **ITH:** a high with STHs on both sides of it — larger buy-side liquidity pool.
- **ITL:** a low with STLs on both sides of it — larger sell-side liquidity pool.
- Used to understand larger market structure and where price may seek liquidity, paired with PDAs
  and MSS to determine targets/reversals/direction.

## External Range Liquidity (ERL)

Liquidity resting outside a defined trading range — above a significant high (buy-side liquidity,
BSL) or below a significant low (sell-side liquidity, SSL). Found at previous highs/lows, swing
highs/lows, ITH/ITL, major structure points. Price often expands toward ERL to take those stops,
then reverses or continues depending on context. Used with PDAs and MSS to judge whether a
liquidity sweep leads to reversal or continuation.

## Internal Range Liquidity (IRL)

Liquidity resting **inside** a defined range — at STHs, STLs, minor swing points, equal
highs/lows. Price often takes internal liquidity as a step toward external liquidity. Paired with
PDAs and premium/discount zones for entries and expected price delivery.

## Premium / Discount Zone (PDZ)

Range split at the 50% equilibrium (EQ) level between a significant high and low.

- **Premium Zone** = upper half — price considered expensive — look for **shorts**, especially at
  a bearish PDA.
- **Discount Zone** = lower half — price considered cheap — look for **longs**, especially at a
  bullish PDA.
- Used as a filter on trade location, not a standalone entry signal.
- **Trader's explicit hard rule: "NEVER SELL IN DISCOUNT, NEVER BUY IN PREMIUM. NO EXCEPTIONS."**
  Treat this as an unconditional filter in the model, same tier as `news_filter` — see
  `premium_discount_zone` in `confluences.yaml`.

## Multi-Timeframe Analysis (HTF / MTF / LTF)

Already reflected in this model's timeframe ladder (`model-overview.md`), but the general ICT
framing behind it:

- **HTF (Daily/4H/1H):** Direction & Location — bias, liquidity targets, major PDAs,
  premium/discount.
- **LTF (15m/5m/1m):** Entry & Execution — wait for price to reach the HTF area, confirm (MSS,
  displacement, FVG), refine entry, tighter risk.
- Short version: **HTF = Where and Why. LTF = When and How.**

## Expansion & Retracement (E&R)

The two-phase cycle price delivery moves through:

- **Expansion:** impulsive move, large-bodied candles, displacement, new FVGs — usually after
  liquidity is taken, heading toward ERL/prior highs-lows/HTF objective.
- **Retracement:** the corrective pullback into prior PDAs (FVG, OB, Breaker, Mitigation Block,
  BPR, etc.) that rebalances imbalances and offers a better entry before the next expansion.
- Practical takeaway: don't chase price during expansion — wait for the retracement into a
  high-probability area. Expansion shows where price wants to go; retracement shows where it may
  offer an entry.

## Risk management (starting note)

Trader's own framing: this is something to learn through experience over time, not a fixed rule
yet. **Starting point given: ~50 points of loss** (presumably NQ points, i.e. per-trade stop
size) as an initial default — expect this to be refined/replaced as we backtest, not treated as
final.
