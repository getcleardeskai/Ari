# Ari — NQ/MNQ Trend & Confluence Model / Pine Script Bot

Personal research project for building, testing, and refining a systematic trend-following
trading model on NQ / MNQ futures, using ICT-style structural confluences, plus the Pine Script
implementation of that model.

**Note on execution context:** the strategy work in this repo is developed independently of any
specific broker/prop-firm platform. Any live or simulated execution happens elsewhere; this repo
only contains the model logic, confluence definitions, and backtesting notes.

## How this repo is used

You (the trader) describe confluences, rules, and examples in conversation. Claude maintains this
repo as the persistent record — writing, updating, and versioning everything below — so nothing
needs to be re-explained between sessions, and no manual GitHub work is required.

## Current direction (2026-08-19)

Trend-following, built on ICT structural confluences (market structure/bias, FVG, iFVG, BPR,
Order Block, Breaker Block, Rejection Block, Inverse Rejection Block, liquidity concepts). The
original midnight-deviation + OTE approach was tried first, then dropped as too discretionary to
encode reliably — see `knowledge/model-overview.md` "Current direction" for the full history.
Those two method docs are kept archived, not deleted, in case anything from them is useful later.

## Structure

- `knowledge/model-overview.md` — the core framework, current direction, and pivot history. Start
  here.
- `knowledge/confluences.yaml` — the living, weighted list of individual confluences (what they
  are, what timeframe they're drawn from, current weight/importance, status — includes which ones
  are deprecated).
- `knowledge/ict-glossary.md` — reference definitions for every ICT concept in the model (FVG,
  IFVG, BPR, PLC/PL, RB/IRB, OB/BB, BOS/MSS, liquidity concepts, premium/discount, etc).
- `knowledge/trade-strength-framework.md` — the general checklist of what stacks confluence into a
  stronger setup.
- `knowledge/examples.md` — real or reference/illustrative trade examples.
- `knowledge/open-questions.md` — master checklist of everything still unresolved.
- `knowledge/midnight-deviation-method.md`, `knowledge/ote-method.md`,
  `knowledge/automation-requirements.md` — archived/pre-pivot docs, kept for reference.
- `pinescript/` — Pine Script indicators/strategies as we build and iterate on them. See
  `pinescript/README.md` for what's there and how to use it.
- `backtests/` — notes and results from testing specific rule/weight configurations.
