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

**Two independent strategies, built/validated separately, that will eventually confirm or deny
each other:**

1. **Mean reversion** — waits for price to overextend, trades the reversion back. Not yet
   formalized — `knowledge/strategies/mean-reversion.md`.
2. **Trend following** — looks for a big directional push and trades with it. First version
   already built: market structure (BOS/CHoCH) on Daily/Weekly/Hourly sets bias, QQE crossovers
   trigger entries in that direction, ATR trailing stop manages risk —
   `pinescript/trend-bias-qqe-strategy.pine`, described in
   `knowledge/strategies/trend-following.md`.

**The live execution bot is now built** (`bot/`) — TradingView alert → webhook → Tradovate order,
running on a Cloudflare Tunnel from your own PC, defaulting to dry-run/demo mode. See
`bot/README.md` for setup. Full architecture: `knowledge/automation-architecture.md`. Full pivot
history (this trend approach is the third tried in one day; midnight-deviation/OTE and ICT
confluence-clustering are archived, not deleted): `knowledge/model-overview.md`.

## Structure

- `knowledge/automation-architecture.md` — the end-goal system: two independent strategies, how
  they're meant to combine, and what the live execution bot actually does. Start here for the big
  picture.
- `knowledge/strategies/mean-reversion.md`, `knowledge/strategies/trend-following.md` — one doc
  per strategy, built/refined independently.
- `knowledge/model-overview.md` — full pivot history for how we got to the current approach.
- `pinescript/trend-bias-qqe-strategy.pine` — the trend strategy's current implementation. See
  `pinescript/README.md` for all scripts and how to use them.
- `bot/` — the live execution bot (webhook receiver + Tradovate order execution). See
  `bot/README.md` for setup, `knowledge/automation-architecture.md` for the design.
- `knowledge/confluences.yaml`, `knowledge/ict-glossary.md`, `knowledge/trade-strength-framework.md`
  — reference material from the archived ICT-confluence phase; `market_structure` and
  `change_of_structure` in `confluences.yaml` remain active since they're the basis for the trend
  strategy's bias model.
- `knowledge/examples.md` — real or reference/illustrative trade examples.
- `knowledge/open-questions.md` — running checklist, mostly from the archived phase.
- `knowledge/midnight-deviation-method.md`, `knowledge/ote-method.md`,
  `knowledge/automation-requirements.md` — archived, kept for reference.
- `backtests/` — notes and results from testing specific configurations.
