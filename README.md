# Ari — NQ/MNQ Confluence Model & Pine Script Bot

Personal research project for building, testing, and refining a discretionary-turned-systematic
trading model on NQ / MNQ futures, plus the Pine Script implementation of that model.

**Note on execution context:** the strategy work in this repo is developed independently of any
specific broker/prop-firm platform. Any live or simulated execution happens elsewhere; this repo
only contains the model logic, confluence definitions, and backtesting notes.

## How this repo is used

You (the trader) describe confluences, rules, and examples in conversation. Claude maintains this
repo as the persistent record — writing, updating, and versioning everything below — so nothing
needs to be re-explained between sessions, and no manual GitHub work is required.

## Structure

- `knowledge/model-overview.md` — the core framework: how the midnight level/deviation and
  multi-timeframe confluence scaling fit together.
- `knowledge/confluences.yaml` — the living, weighted list of individual confluences (what they
  are, what timeframe they're drawn from, current weight/importance, status). This is the file
  that changes most often as we test and re-rank confluences.
- `knowledge/examples.md` — real or annotated trade examples used as reference cases when
  validating logic changes.
- `pinescript/` — Pine Script indicators/strategies as we build and iterate on them.
- `backtests/` — notes and results from testing specific rule/weight configurations.

## Core model, in short

1. Establish the **midnight level** (midnight open) and the **midnight deviation** off that level
   as the anchor for the day's setup.
2. Go to a **much larger timeframe** first and map areas of significant confluence (buying/selling
   pressure, liquidity, structure) around price.
3. **Scale down** through timeframes, refining those same areas into tighter and tighter zones.
4. Look for the point where the **midnight deviation aligns with a refined, multi-timeframe
   confluence zone** — that alignment is the entry trigger, with the goal of a tight/precise stop
   and a large target (historically 1:6–1:10 R).
5. Confluences are individually weighted and the weights are expected to change as we backtest —
   `knowledge/confluences.yaml` is built specifically to make that fast to edit.
