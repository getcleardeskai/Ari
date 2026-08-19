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

## What's still open / to define as we go
- [ ] Exact timezone/session convention for "midnight"
- [ ] Specific tools used to identify HTF confluence (e.g. order blocks, FVGs, liquidity pools,
      volume profile, prior highs/lows — whichever ones you actually use)
- [ ] Exact timeframe ladder used when scaling down (e.g. Weekly → Daily → 4H → 1H → 15m → ...)
- [ ] Stop loss placement rule once alignment is found
- [ ] Take profit rule (fixed R multiple vs. next opposing confluence, etc.)
- [ ] Rules for when the setup is invalidated / no-trade conditions

This file should stay high-level. Individual confluence definitions, weights, and status live in
`confluences.yaml`. Concrete trade examples live in `examples.md`.
