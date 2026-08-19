# Mean Reversion Strategy

Status: **not yet formalized.** Trader's one-line description (2026-08-19): "waiting for price to
overextend and then revert." Everything below is a skeleton to fill in — see
`../automation-architecture.md` for how this fits into the bigger plan.

## What we need to define (working through this incrementally)

- [ ] **What counts as "overextended"?** A specific indicator/measure (RSI level, Bollinger Band
      touch, standard deviations from a moving average, ATR-multiple move, something else)? Or a
      visual/price-action pattern? This is the first, most important thing to pin down — it's the
      actual trigger condition.
- [ ] What timeframe(s) does this run on?
- [ ] What confirms the reversion is actually starting (vs. price staying overextended longer)?
- [ ] Entry rule — exact trigger once overextension + reversion confirmation line up.
- [ ] Stop-loss rule.
- [ ] Take-profit / exit rule (reversion back to what — the mean itself? A fixed target? Prior
      structure?).
- [ ] Instrument/session — same NQ/MNQ as the trend strategy? Same trading hours?
- [ ] Position sizing.

## Notes

_(nothing captured yet — this fills in as we talk through it)_
