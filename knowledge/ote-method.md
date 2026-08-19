> **ARCHIVED 2026-08-19.** Dropped from the active model — swing-point selection discretion was
> judged too inconsistent to build a reliable system around, same reasoning as the midnight
> deviation drop. Kept here for reference only.

# OTE (Optimal Trade Entry) — Method

A second fib-based tool, separate from (but used *alongside*) the midnight deviation. Referenced
by the `ote` confluence in `confluences.yaml`. Captured 2026-08-19 — **trader stresses this is
highly discretionary** and will keep feeding new stats/levels/examples over time; treat this doc
as a living spec, not a closed one.

## What it is

- Standard ICT-style **Optimal Trade Entry**: a fib retracement drawn across a swing leg, used to
  find a high-probability, tight entry zone within that leg.
- Drawn from the **most obvious swing low to swing high** (or high-to-low, depending on
  direction — see "Reversal" below) on whatever range the trader judges relevant.
- The goal is to get the **OTE zone to line up ("connect") with a midnight deviation level** —
  the OTE is a refinement/precision tool on top of the midnight dev, not a replacement for it.
  This is a direct instance of the model's core "alignment = tight entry" principle from
  `model-overview.md`.

## Levels & probability (trader's field data, 2026-08-19)

From the observed settings (screenshot, TradingView Fib Retracement tool), the enabled levels on
the OTE tool are: **0, 0.62, 0.66, 0.7, 0.78, 1** (plus the 0/1 anchors). The **0.7** level is
explicitly labeled "OTE" on the chart — the center/anchor of the zone.

- **0.78 = highest probability**
- **0.62 = lowest probability**
- (0.66, 0.7 fall between, 0.7 being the named "OTE" center point)
- Trader is explicit that they don't know the underlying "why" for this ranking — "I don't know
  the map behind it or the logic, but we accept that as fact." Treat this as an empirical,
  trader-supplied ranking to encode as-is, not something to second-guess against textbook ICT OTE
  convention (which usually treats 0.62 as the standard sweet spot) — **this model's own
  documented probability ordering is 0.78 > 0.66/0.7 > 0.62**, and that's what should drive the
  weighting here.
- More levels/stats for OTE are expected to be added over time — this section should be extended,
  not replaced, as new data comes in.

## How the swing points are chosen (highly discretionary)

- There is a **large range of valid highs/lows** that can be used as the swing low/swing high
  anchors — e.g. NY AM session high/low, or other session-based extremes — and which one is
  "correct" is a matter of trader judgment, not a fixed rule.
- The tool can be **reversed** in settings to try to align the OTE zone with wherever the trader
  wants it to end up.
- Trader's own framing: this is "incredibly good for refining your trade to an exact point entry,"
  but it also "requires you to be incredibly biased for where you want it to end up" — i.e. it's
  acknowledged as somewhat confirmation-bias-prone by design. If you can find a rationale for the
  OTE to land on a particular swing high/low, it "just increases your odds" (in the trader's
  framing) — but this is explicitly a soft, judgment-based process, not a hard rule that should be
  automated as-is without a lot of examples to learn the pattern from.
- **Implication for automation:** OTE placement is the single hardest thing in this model to turn
  into a deterministic Pine Script rule, because the swing-point selection itself is discretionary.
  Likely needs either (a) a large labeled example set to learn the trader's actual selection
  pattern from, or (b) a scored/candidate-ranking approach (compute OTE off several plausible
  swing points, e.g. NY AM high/low, prior day high/low, etc., and score each by which one aligns
  with a midnight deviation level) rather than one canonical calculation.

## Combining OTE with other confluences

- OTE aligning with a midnight deviation level is the primary combination.
- OTE can also align with **other confluences**, e.g. the trader gave the example of OTE lining up
  with the **0.5 level of a rejection block**.
- Trader's stated observation: tighter/more-stacked confluence tends to correspond to bigger
  resulting moves. Two data points given:
  - Midnight dev alone, high-volume level: ~15 tick drawdown → ~500 tick expansion.
  - OTE + rejection block 0.5 confluence: ~5 tick drawdown → ~700 tick expansion (tighter
    drawdown, bigger expansion).
  - Treat these as anecdotal/example data points for now, not statistically validated — log them
    in `examples.md` as trade examples once we have specific dated instances, and use them to
    sanity-check any weighting scheme instead of the other way round.

## What's still open

- [ ] Systematic rule (or scoring method) for swing-point selection — currently pure discretion.
- [ ] Full probability table beyond 0.62/0.66/0.7/0.78 — trader says more levels/stats coming.
- [ ] Exact rule for when to reverse the tool.
- [ ] Threshold for what counts as "aligned" with a midnight deviation level or other confluence
      (how close is close enough).

## Automation note

Per the overall automation goal in `README.md`, the eventual target is still full automation, but
OTE is flagged as the piece most likely to need a different approach than straightforward formula
replication (see "Implication for automation" above) — expect this to take more iteration/examples
than the midnight deviation math did.
