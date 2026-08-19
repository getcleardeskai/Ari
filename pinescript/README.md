# Pine Script

Strategies/indicators implementing the model from `../knowledge/model-overview.md`.

## `basic-trend-strategy.pine`

Starting scaffold (2026-08-19) — a simple EMA-crossover trend-following strategy with an
ATR-based stop/target, meant to backtest cleanly in the TradingView Strategy Tester today. This
is **not** the full midnight-deviation/ICT model from `../knowledge/` — it's a working baseline
to iterate from now that the full discretionary model was judged too complex to encode in one
shot. Next steps will likely layer in a trend/structure filter and, eventually, the midnight
deviation confluences on top of this.

**How to use it:** open TradingView → open an MNQ1! or NQ1! chart → Pine Editor → paste this
file's contents → Add to Chart → Strategy Tester tab to see backtest results. Every parameter
(EMA lengths, ATR stop/target multiples, long/short toggle, date range) is exposed as an input so
it can be tuned without editing code.
