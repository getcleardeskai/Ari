# Model Overview

## Instrument
- **Market:** NQ (E-mini Nasdaq-100 futures)
- **Sizing instrument:** MNQ (Micro NQ) — used for position sizing/testing
- **Why MNQ matters:** its behavior around the midnight open is central to this model; midnight
  price action is treated as a key structural reference, not just a session marker.

## Framework

### 1. Midnight Level & Midnight Deviation
- The **midnight open** (price at 00:00, exchange/reference timezone TBD — confirm and lock this
  in `confluences.yaml` once decided) is charted as a level for the session.
- The **midnight deviation** is the move price makes away from that level — this deviation is the
  primary timing/anchor mechanism for entries.

### 2. Top-down confluence mapping
- Start on a **large/higher timeframe** (HTF) and identify areas of significant confluence —
  zones with substantial historical buying or selling pressure (structure, liquidity, whatever
  specific tools/concepts we define in `confluences.yaml`).
- **Scale down** through progressively smaller timeframes, re-testing/refining those same areas
  each step down, so a broad HTF zone becomes a tight, precise LTF zone.

### 3. Alignment = entry
- The trade trigger is the **alignment** of:
  a) the midnight deviation (timing/anchor), with
  b) a confluence zone that has survived the top-down refinement process (location/precision).
- When both line up, the model expects a very tight, well-defined stop loss and a large
  target — historically **1:6 to 1:10 (sometimes 1:1**0**) reward-to-risk**.

### 4. Precision requirement
- Because targets are large relative to risk, **entry precision is critical** — imprecise entries
  either get stopped out on noise or blow the R:R math. This is the reason confluences need to be
  individually weighted and constantly re-ranked rather than treated as a flat checklist.

## Confluence vocabulary

Confluences are described in **ICT (Inner Circle Trader) terminology**:

- **Market structure / bias** — Break of Structure (BOS), Change of Character (CHoCH), and trend
  read on the Daily. Called out by the trader as likely the single most important factor, since
  it sets directional bias before anything else is considered.
- **Previous session liquidity** — prior day/session high and low.
- **Fair Value Gap (FVG)** / **Inverse FVG (iFVG)**
- **Balanced Price Range (BPR)**
- **Rejection Block**
- **Order Block**

All of the above (except market structure, which is Daily-based) get scaled down through the
**timeframe ladder**:

```
Daily -> 4H -> 1H -> 45m -> 30m -> 15m -> 5m (final refinement)
```

See `confluences.yaml` for the full, weighted, editable registry of these.

## Midnight deviation — marking method

The midnight deviation is not just "distance from the midnight open" — it's marked using a
specific 5-minute-candle + fib method with a couple of variant cases (single reversal candle vs.
a run of same-direction candles, plus a distinct trend-day variant). Full detail lives in
`midnight-deviation-method.md` — that doc is still partially unconfirmed pending a worked chart
example from the trader.

## Entry trigger & trade management (no fixed R:R)

- **Entry:** there is no fixed risk:reward entry rule. The trigger is an **immediate, high-volume
  spike/reaction at or around** the level where the midnight deviation aligns with a refined
  confluence zone. No reaction = no entry, even if the levels line up.
- **Exit / management:** no fixed take-profit rule either. Trade is managed against **other
  midnight deviation levels** and broader **higher-timeframe support/resistance**, or closed on
  signs of price reversing against the position.
- Historical R:R outcomes (1:6–1:10) are a result of this process, not a target set in advance.

## What's still open / to define as we go
- [ ] Exact timezone/session convention for "midnight" (trader is US-Georgia based, references
      UTC, unsure if it aligns with the Asia session open — see `midnight-deviation-method.md`)
- [ ] Full midnight-deviation marking method confirmation (worked chart example pending)
- [ ] Rules for when the setup is invalidated / no-trade conditions
- [ ] How structure/bias interacts with the midnight deviation on trend days specifically

This file should stay high-level. Individual confluence definitions, weights, and status live in
`confluences.yaml`. Concrete trade examples live in `examples.md`. The midnight-marking mechanics
live in `midnight-deviation-method.md`.
