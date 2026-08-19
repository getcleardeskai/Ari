# Trend Following Strategy

Status: **v1 built.** Trader's one-line description (2026-08-19): "looks for a big move, a big
push." Implemented as `../../pinescript/trend-bias-qqe-strategy.pine` — built before the
two-strategy framing was made explicit, but it's exactly this strategy: Daily/Weekly/Hourly
market-structure bias gates direction, QQE crossovers trigger entries, ATR trailing stop manages
risk. See `../automation-architecture.md` for how this fits the bigger plan.

## Current rules (as implemented)

- **Bias:** market structure (BOS = continuation, CHoCH = reversal) computed independently on
  Daily, Weekly, Hourly. One is "primary" (default Daily) and gates direction; optional
  require-all-three-agree toggle.
- **Entry:** QQE (smoothed RSI + ATR-trailing-band) crossover, only taken in the bias direction.
- **Exit:** ATR trailing stop always active; optional early exit on opposing QQE cross or bias
  flip against the position.
- **No painting:** signals only act/plot once `barstate.isconfirmed`.
- **No re-entries:** `pyramiding = 0` + explicit position-size check.

## Next steps for this strategy specifically

- [ ] Actually run the backtest in TradingView's Strategy Tester and look at the stats (win rate,
      profit factor, drawdown, etc.) — nothing has been validated against real data yet.
- [ ] Tune parameters based on what the stats show (QQE length/smoothing, pivot length for
      structure, ATR stop multiple, primary bias timeframe choice).
- [ ] Decide whether "big push/move" needs anything beyond QQE + structure bias, or if that
      combination already captures the trader's actual discretionary read of "a big move." Worth
      revisiting once backtest results are in — if the strategy's entries don't match what the
      trader would call a real trend move by eye, that's a sign something needs to change (e.g. a
      minimum displacement/momentum filter beyond just the QQE cross).

## Notes

_(add backtest results / observations here as they come in)_
