# Trade Examples

Concrete reference cases — real trades, backtested setups, or annotated chart examples. These are
used to sanity-check model/rule changes against reality ("does this new weighting still catch
this known-good example / still avoid this known-bad one?").

## Template

Copy this block per example:

```
### YYYY-MM-DD — MNQ (or NQ) — Long/Short

- Midnight open: <price>
- Midnight deviation: <description, e.g. "deviated 40pts above midnight open by 3:15am ET">
- HTF confluence: <what zone, what timeframe, why it qualified>
- LTF refinement: <how it tightened down, final zone>
- Entry: <price/time>
- Stop: <price> (<pts/ticks> risk)
- Target: <price> (<R multiple>)
- Outcome: <win/loss/scratch, actual R>
- Notes: <what worked, what didn't, any confluence that should be re-weighted because of this>
```

## Examples

_None logged yet — add the first one whenever you're ready._
