# Ari — NQ/MNQ Trend Bias + QQE Trading Model

Personal research project for building, testing, and refining a systematic trend-following
trading model on NQ / MNQ futures, plus the Pine Script implementation of that model.

**Note on execution context:** the strategy work in this repo is developed independently of any
specific broker/prop-firm platform. Any live or simulated execution happens elsewhere; this repo
only contains the model logic and backtesting notes.

## How this repo is used

You (the trader) describe the model, rules, and examples in conversation. Claude maintains this
repo as the persistent record — writing, updating, and versioning everything below — so nothing
needs to be re-explained between sessions, and no manual GitHub work is required.

## Current direction (2026-08-19)

**Trend Bias + QQE.** Market structure (BOS/CHoCH) computed on Daily, Weekly, and Hourly sets a
directional bias, shown in a dashboard on the chart. QQE (smoothed-RSI + ATR-trailing-band)
crossovers trigger entries, only in the direction the bias allows. An ATR trailing stop manages
risk. See `pinescript/trend-bias-qqe-strategy.pine` — the working implementation — and
`knowledge/model-overview.md` "Current direction" for the full pivot history (this is the third
approach tried in one day; the first two — midnight-deviation/OTE, then ICT confluence-clustering
— are archived, not deleted, in case anything from them becomes useful again).

## Structure

- `knowledge/model-overview.md` — the core framework, current direction, and full pivot history.
  Start here.
- `pinescript/trend-bias-qqe-strategy.pine` — the current strategy. See `pinescript/README.md` for
  all scripts and how to use them.
- `knowledge/confluences.yaml`, `knowledge/ict-glossary.md`, `knowledge/trade-strength-framework.md`
  — mostly reference material from the archived ICT-confluence phase now; `market_structure` and
  `change_of_structure` in `confluences.yaml` remain active since they're the basis for the
  current bias model.
- `knowledge/examples.md` — real or reference/illustrative trade examples.
- `knowledge/open-questions.md` — running checklist, mostly from the archived phase; due for a
  fresh pass specific to the Trend Bias + QQE model once there's backtest data to react to.
- `knowledge/midnight-deviation-method.md`, `knowledge/ote-method.md`,
  `knowledge/automation-requirements.md` — archived, kept for reference.
- `backtests/` — notes and results from testing specific configurations.
