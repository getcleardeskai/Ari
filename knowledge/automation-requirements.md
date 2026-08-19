# Automation Requirements — Alerts & Confidence Scoring

Functional requirements for the eventual Pine Script tooling, as distinct from the model logic
itself (which lives in `model-overview.md`, `midnight-deviation-method.md`, `ote-method.md`,
`confluences.yaml`). Captured 2026-08-19.

## Alerting behavior

- The trader wants **alerts before price reaches a high-probability point of interest** — a
  point of interest being a midnight deviation level and/or OTE zone that has other confluences
  "funded into" it (i.e. stacked/aligned confluence, per the core model).
- High-probability areas should be **marked with a percent-confidence score**, not just flagged
  as binary "is/isn't a zone."
- **Alert timing:** fire an alert once price crosses a defined distance threshold from the level —
  trader's example: **~25 ticks before** the level. This threshold should be configurable, not
  hard-coded, since it's given as "or so."
- Trader will define **what makes a zone lower vs. higher probability** in more detail later —
  this doc should be extended once that's given, and should end up consuming the per-confluence
  `weight` values in `confluences.yaml` (i.e. confidence score = some function of which
  confluences are stacked at a level and their current weights).

## Design implication for Pine Script

- Confidence scoring needs to be a **first-class output**, not an afterthought — the alert
  system depends on it directly (threshold-based alerts should fire relative to a zone's score,
  not just its raw existence).
- Suggests the eventual strategy/indicator should maintain, per potential point-of-interest zone:
  - which confluences are aligned there (from `confluences.yaml`)
  - a combined confidence score (weighted sum/product of aligned confluences — exact formula
    TBD, pending more trader guidance and backtest data)
  - distance from current price, to drive the alert-threshold logic

## What's still open

- [ ] Exact confidence-score formula (how per-confluence weights combine into one score).
- [ ] Confirmed alert distance threshold (currently "~25 ticks," treat as a starting default/
      configurable input, not a fixed constant).
- [ ] Full definition of what makes a zone "lower probability" (trader said this is coming later).
