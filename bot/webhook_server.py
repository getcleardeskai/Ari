"""
Webhook server — receives TradingView alert payloads (from the alert()
calls in ../pinescript/trend-bias-qqe-strategy.pine and
../pinescript/auto-reversion-strategy.pine) and forwards validated signals
to the Tradovate execution client.

Run with:
    uvicorn webhook_server:app --host 0.0.0.0 --port 8000

See ../bot/README.md for full setup — Cloudflare Tunnel to expose this
locally-run server to TradingView, and how to configure the TradingView
alert itself.
"""
import logging
import os
import time
from typing import Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

import tradovate_client as tv

load_dotenv()

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"
DEFAULT_QTY = int(os.environ.get("DEFAULT_QTY", "1"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("webhook_server")

if not WEBHOOK_SECRET or WEBHOOK_SECRET == "changeme":
    log.warning(
        "WEBHOOK_SECRET is unset or still the default 'changeme' — every request will be "
        "rejected until this matches the secret configured in the Pine script's input."
    )
if DRY_RUN:
    log.info("DRY_RUN is ON — signals will be logged but no real orders will be placed.")
else:
    log.warning("DRY_RUN is OFF — this WILL place real orders on Tradovate (%s environment).", os.environ.get("TRADOVATE_ENV", "demo"))

app = FastAPI(title="Ari Trading Bot Webhook Receiver")

# In-memory de-dupe: ignore an identical (strategy, symbol, action) signal
# seen again within this many seconds, in case TradingView redelivers the
# same alert (it does retry on failed deliveries).
DEDUPE_WINDOW_SECONDS = 5
_recent_signals: Dict[str, float] = {}


class AlertPayload(BaseModel):
    secret: str
    strategy: str
    symbol: str
    action: str  # "long" | "short" | "close_long" | "close_short"
    price: Optional[float] = None
    qty: Optional[int] = None


@app.get("/")
def health():
    return {"status": "ok", "dry_run": DRY_RUN, "env": os.environ.get("TRADOVATE_ENV", "demo")}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    try:
        payload = AlertPayload(**body)
    except Exception as e:
        log.warning("Rejected malformed payload: %s (%s)", body, e)
        raise HTTPException(status_code=400, detail="Malformed payload") from e

    if not WEBHOOK_SECRET or payload.secret != WEBHOOK_SECRET:
        log.warning("Rejected payload with bad/missing secret (strategy=%s)", payload.strategy)
        raise HTTPException(status_code=401, detail="Invalid secret")

    dedupe_key = f"{payload.strategy}:{payload.symbol}:{payload.action}"
    now = time.time()
    last_seen = _recent_signals.get(dedupe_key)
    if last_seen is not None and (now - last_seen) < DEDUPE_WINDOW_SECONDS:
        log.info("Ignoring duplicate signal within dedupe window: %s", dedupe_key)
        return {"status": "duplicate_ignored"}
    _recent_signals[dedupe_key] = now

    log.info(
        "Signal received: strategy=%s symbol=%s action=%s price=%s",
        payload.strategy, payload.symbol, payload.action, payload.price,
    )

    qty = payload.qty or DEFAULT_QTY

    if DRY_RUN:
        log.info("DRY_RUN — not placing a real order. Would do: %s %s x%s", payload.action, payload.symbol, qty)
        return {"status": "dry_run", "would_execute": payload.action}

    try:
        result = tv.execute_signal(symbol=payload.symbol, action=payload.action, qty=qty)
        log.info("Order result: %s", result)
        return {"status": "executed", "result": result}
    except Exception as e:
        log.exception("Order execution failed")
        raise HTTPException(status_code=500, detail=f"Execution failed: {e}") from e
