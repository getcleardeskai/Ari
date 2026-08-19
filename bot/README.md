# Ari Trading Bot

Receives TradingView webhook alerts from `../pinescript/trend-bias-qqe-strategy.pine` and
`../pinescript/auto-reversion-strategy.pine`, and places matching orders on Tradovate. Runs on
your own PC, exposed to the internet via a Cloudflare Tunnel (no router/port-forwarding needed).

Architecture, end to end:

```
Pine strategy (bias/signal already validated) --alert()--> TradingView Alert
    --webhook POST--> Cloudflare Tunnel --> this server (webhook_server.py)
    --if valid & DRY_RUN=false--> tradovate_client.py --> Tradovate API --> real order
```

Matches the design in `../knowledge/automation-architecture.md`: the bot does not decide
anything — the Pine strategy already validated the rules before it ever alerted. The bot's job is
narrow — confirm the payload is genuine (shared secret) and not a duplicate, then place the order.

## ⚠️ Before you do anything live

- Start with `DRY_RUN=true` and `TRADOVATE_ENV=demo` — **both are the defaults**. Do not change
  either until you've watched the logs confirm real signals arrive correctly.
- This places real orders once `DRY_RUN=false`. On `TRADOVATE_ENV=live`, those orders use real
  money. Treat flipping either switch as a deliberate, separate decision — not something to do
  while still debugging.
- The `.env` file holds real credentials. It's covered by the repo's `.gitignore` — keep it that
  way, never commit it, never paste its contents into chat.

## Setup

### 1. Install dependencies

```
cd bot
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```
cp .env.example .env
```

Edit `.env`:
- `WEBHOOK_SECRET` — make up a long random string. You'll paste this exact value into the Pine
  script's "Webhook secret" input too (Settings on the indicator/strategy on your chart).
- Tradovate credentials — `TRADOVATE_USERNAME`/`PASSWORD` are your normal login. `APP_ID`, `CID`,
  `SEC` come from registering an API application at Tradovate (Settings → API Access on
  trader.tradovate.com). `DEVICE_ID` can be any stable string you pick.
- Leave `DRY_RUN=true` and `TRADOVATE_ENV=demo` for now.

### 3. Run the server

```
uvicorn webhook_server:app --host 0.0.0.0 --port 8000
```

Leave this running. Visit `http://localhost:8000/` in a browser — you should see
`{"status":"ok","dry_run":true,"env":"demo"}`.

### 4. Expose it to the internet with a Cloudflare Tunnel

TradingView's alert servers need a public HTTPS URL to send webhooks to — your PC's local address
won't work. Cloudflare Tunnel does this without opening any ports on your router.

1. Install `cloudflared`: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. Run (in a separate terminal, leave it running alongside the server):
   ```
   cloudflared tunnel --url http://localhost:8000
   ```
3. It prints a URL like `https://random-two-words.trycloudflare.com` — that's your public webhook
   base. Your webhook endpoint is `https://random-two-words.trycloudflare.com/webhook`.

**Note:** this "quick tunnel" mode gives you a new random URL every time you restart
`cloudflared`. That's fine for testing. Once you're happy with everything and want a stable URL
that doesn't change, that needs a (free) Cloudflare account + a domain and a named tunnel instead
— ask if/when you want that set up.

### 5. Set the webhook secret in the Pine script

On your TradingView chart, open the strategy's settings (gear icon) → find "Webhook secret" under
the "Bot Webhook" group → paste the same value you put in `.env`'s `WEBHOOK_SECRET`.

### 6. Create the TradingView alert

1. With the strategy on your chart, click **Alert** (clock icon) → **Create Alert**.
2. **Condition:** choose the strategy, then "Any alert() function call" (not a specific
   alertcondition — the script's `alert()` calls carry the actual JSON payload).
3. **Webhook URL:** paste `https://<your-tunnel-url>/webhook`.
4. The **Message** field is ignored when using `alert()` in the script (the script's own JSON is
   what actually gets sent) — leave it as the default or anything, it doesn't matter.
5. Save. Repeat for the other strategy if you're running both.

### 7. Test in DRY_RUN

Wait for a signal (or force one by loosening the strategy's conditions temporarily, or just wait
for a real setup). Watch the `uvicorn` terminal — you should see a log line like:

```
Signal received: strategy=trend_qqe symbol=MNQ1! action=long price=21050.25
DRY_RUN — not placing a real order. Would do: long MNQ1! x1
```

If you see this, the whole pipeline works end to end. If not, see Troubleshooting below.

### 8. Go live, carefully, in stages

1. Keep `TRADOVATE_ENV=demo`, flip `DRY_RUN=false`. Confirm real (paper) orders land correctly in
   your Tradovate demo account.
2. Only after that's been solid for a while, and only when you've deliberately decided to, switch
   `TRADOVATE_ENV=live`. This is real money — treat it as a distinct decision, not a checkbox.

## Troubleshooting

- **No log line ever appears when a signal should have fired:** check the TradingView alert is
  still active (alerts can expire/need re-creating), and that the Cloudflare Tunnel is still
  running (its URL changes on restart in quick-tunnel mode — the TradingView alert needs updating
  if that happens).
- **401 "Invalid secret" in the logs:** the `webhookSecret` input on the Pine script doesn't match
  `.env`'s `WEBHOOK_SECRET`. They must be character-for-character identical.
- **400 "Malformed payload":** open the alert's delivery log in TradingView (or check the raw
  webhook body) — the JSON the script sent doesn't match what the server expects. Send me the
  exact payload and I'll fix it.
- **Tradovate auth errors:** double check `TRADOVATE_APP_ID`/`CID`/`SEC` are from an app actually
  registered against the account you're logging in with, and that `TRADOVATE_ENV` matches where
  that app is registered (demo vs. live are separate).

## What's NOT built yet

- Position-size verification against Tradovate before ordering (currently trusts the Pine
  strategy's own no-reentry logic + the dedupe window — see the docstring on
  `tradovate_client.execute_signal`).
- Contract symbol mapping/rollover handling (right now it just forwards `syminfo.ticker` from the
  Pine script as the order symbol — worth checking this matches Tradovate's expected symbol format
  for MNQ/NQ, e.g. whether it needs the specific contract month rather than the continuous `MNQ1!`
  ticker).
- Daily loss limits / max-trades-per-day / a kill switch — flagged as open in
  `../knowledge/open-questions.md` and `../knowledge/automation-architecture.md`, worth adding
  before running unattended for real.
- Running both strategies (Trend + Auto Reversion) together and reconciling conflicting signals —
  right now each just fires independently; the "confirm or deny each other" combination logic from
  `../knowledge/automation-architecture.md` isn't implemented.
