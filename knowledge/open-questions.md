# Master Open Questions

Every unresolved question across the knowledge base, consolidated in one place. Sourced from the
"Open questions" sections in each doc plus additional gaps found while building this list.
Answer any of these in any order, any time — I'll fold answers back into the relevant doc and
check them off here.

## Midnight Deviation

- [ ] Exact timezone/session definition for "00:00" — you've said UTC, also Georgia/US, also
      "maybe Asia session open." Need the actual precise rule (e.g. "00:00 New York time" or
      "00:00 UTC" specifically) since Pine Script needs an exact `timestamp()`/session string.
- [ ] Does the bullish-candle-first mirror case (bullish 00:00 candle → bearish follow-through)
      work identically to the documented bearish→bullish case, just flipped?
- [ ] Trend-day variant: when a trend is already running through midnight instead of
      chopping/reversing, what changes about how the deviation gets marked?
- [ ] When do you use Method A (candle-run) vs. Method B (manipulation leg)? Is there a rule, or
      is it always discretionary which one applies on a given day?
- [ ] How do you actually identify a "manipulation leg" (Method B) — any objective marker, or
      pure feel?
- [ ] Per-level weight within the 16-level ladder — is every level in the pullback band (1 to
      -2.5) equally likely, or is there a hierarchy inside that band too? Same question for the
      reversion band (-3 to -5).
- [ ] Can more than one midnight deviation form in the same session (e.g. a second reversal later
      re-triggers a new deviation), or is it strictly one-per-day?
- [ ] What happens if price gaps straight through several levels at once without reacting at any
      of them — does the setup just get skipped that day, or is there a fallback?

## News / Volume Filter

- [ ] What counts as "news" for the no-trade filter — a specific list (FOMC, NFP, CPI, PPI, etc.),
      or any red-folder/high-impact economic calendar event?
- [ ] How wide is the blackout window around a news event — e.g. 15 minutes before/after, 30, an
      hour?
- [ ] Where should the bot pull news times from — manual daily input, a fixed recurring schedule,
      or an external data feed? (Pine Script has no native news feed, so this determines the
      implementation path.)
- [ ] For the volume-spike entry trigger: what actually counts as "high volume" — a multiple of
      average volume (e.g. 2x, 3x the 20-bar average), a fixed contract count, or something else?
      Right now this is undefined/discretionary.

## OTE

- [ ] More probability data beyond 0.62 (lowest) / 0.66 / 0.7 (center) / 0.78 (highest) — any
      other levels you use?
- [ ] What's the actual rule (or heuristic) for picking which swing low/high to draw the OTE
      from — NY AM range, prior day range, something else? Even a rough decision tree would help.
- [ ] When do you reverse the OTE tool vs. leave it as-is?
- [ ] How close does an OTE level need to be to a midnight deviation level (or other confluence)
      to count as "aligned" — a tick/point tolerance, or just visual overlap?

## Confluence weighting & scoring (the whole point of this repo)

- [ ] For every confluence currently sitting at the default weight (50) in `confluences.yaml` —
      which ones do you already have a strong opinion on being more/less important, even before
      formal backtesting? (Just naming a handful to start re-ranking is enough — doesn't need to
      be exhaustive.)
- [ ] How should confidence score actually combine multiple aligned confluences — simple sum of
      weights, average, something multiplicative (so one missing "must-have" confluence tanks the
      score), or a minimum-count rule ("need at least N of these")?
- [ ] Is `premium_discount_zone` and `news_filter` meant to be a hard yes/no gate (trade
      disallowed entirely) rather than something that just lowers a score? (I've been treating
      them as regular weighted entries so far, flagged this as open in the registry.)
- [ ] Minimum number of confluences required before you'd even consider taking a trade?

## Trade management / exits

- [ ] Exit is currently documented as "other midnight-dev levels or HTF S&R, or signs of price
      reversing" — what specifically counts as "signs of reversing"? A structure break against
      you, a rejection candle, an opposing FVG forming, something else?
- [ ] Do you scale out (partial profits at the first opposing level, trail the rest) or exit the
      full position at once?
- [ ] Stop-loss placement rule: always at the far edge of the confluence zone? A fixed tick
      buffer beyond it? Something structure-based (beyond the manipulation leg, beyond a
      liquidity sweep low/high)?

## Definitions still missing entirely

- [ ] **Mitigation Block** — mentioned twice in the source material (E&R section, HTF PDA list)
      but never actually defined. What is it, and how does it differ from an Order Block/Breaker
      Block?
- [ ] **Kill Zones** — London Kill Zone and New York Kill Zone were named as part of "Time &
      Session Alignment" but not given exact times. What are the exact windows you use?
- [ ] Long-Term High/Low (LTH/LTL) — only the high side was shown in the reference diagram; is
      the low-side mirror (LTL) exactly analogous, or anything different about it?

## Execution / account context (needed before this becomes a real bot, not just a model)

- [ ] Where will this actually execute once built ("somewhere else," per your first message) —
      what platform/broker/data feed? This affects tick size handling, symbol naming, and whether
      it's TradingView Pine Script alerts + manual/webhook execution, vs. something else entirely.
- [ ] Position sizing — fixed contract count, or risk-based (e.g. risk X% of account per trade,
      calculated from stop distance)?
- [ ] Any daily loss limit or max-trades-per-day rule?
- [ ] Do you trade every session, or only specific days/sessions (e.g. skip Fridays, skip low
      liquidity holiday weeks)?
- [ ] Contract rollover handling for MNQ/NQ (quarterly expiration) — does the midnight-dev logic
      need any special handling around roll dates, or does it just not matter?

## Backtesting

- [ ] Do you already have a log of past trades/setups (even informal) we could digitize into
      `examples.md`, or are we starting purely from new forward-testing once the Pine Script
      exists?
- [ ] How far back do you want backtesting to go, and is there a specific data source/resolution
      concern (5m data availability on MNQ historically)?
