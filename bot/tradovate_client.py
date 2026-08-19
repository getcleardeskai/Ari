"""
Minimal Tradovate REST API client — authentication + market order placement.

Defaults to Tradovate's DEMO environment (TRADOVATE_ENV=demo in .env) — do
not point this at "live" until the strategy has been validated on demo and
you've deliberately decided to risk real money. See ../bot/README.md.

This is intentionally minimal: authenticate, find an account, place a
market order. It does NOT currently check existing position size against
Tradovate before sending an order (see the docstring on execute_signal for
why that's an acceptable v1 tradeoff, and what to add before trusting this
unattended for a long stretch).
"""
import logging
import os
import time
from typing import Optional, Tuple

import requests

log = logging.getLogger("tradovate_client")

ENV = os.environ.get("TRADOVATE_ENV", "demo")
BASE_URL = "https://live.tradovateapi.com/v1" if ENV == "live" else "https://demo.tradovateapi.com/v1"

_access_token: Optional[str] = None
_token_expires_at: float = 0.0
_account_id: Optional[int] = None
_account_spec: Optional[str] = None


def _authenticate() -> str:
    global _access_token, _token_expires_at
    resp = requests.post(
        f"{BASE_URL}/auth/accesstokenrequest",
        json={
            "name": os.environ["TRADOVATE_USERNAME"],
            "password": os.environ["TRADOVATE_PASSWORD"],
            "appId": os.environ["TRADOVATE_APP_ID"],
            "appVersion": os.environ.get("TRADOVATE_APP_VERSION", "1.0"),
            "deviceId": os.environ["TRADOVATE_DEVICE_ID"],
            "cid": os.environ["TRADOVATE_CID"],
            "sec": os.environ["TRADOVATE_SEC"],
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if "accessToken" not in data:
        raise RuntimeError(f"Tradovate authentication failed: {data}")
    _access_token = data["accessToken"]
    # expirationTime comes back as an ISO timestamp; rather than parse it,
    # just re-authenticate somewhat conservatively (Tradovate tokens are
    # typically valid several hours).
    _token_expires_at = time.time() + 60 * 60 * 4
    log.info("Authenticated with Tradovate (%s environment)", ENV)
    return _access_token


def _get_token() -> str:
    if _access_token is None or time.time() >= _token_expires_at:
        return _authenticate()
    return _access_token


def _headers() -> dict:
    return {"Authorization": f"Bearer {_get_token()}", "Content-Type": "application/json"}


def _get_account() -> Tuple[int, str]:
    global _account_id, _account_spec
    if _account_id is not None and _account_spec is not None:
        return _account_id, _account_spec

    resp = requests.get(f"{BASE_URL}/account/list", headers=_headers(), timeout=15)
    resp.raise_for_status()
    accounts = resp.json()
    if not accounts:
        raise RuntimeError("No Tradovate accounts found for this login")

    account = accounts[0]
    override_id = os.environ.get("TRADOVATE_ACCOUNT_ID")
    if override_id:
        match = next((a for a in accounts if str(a["id"]) == override_id), None)
        if match is None:
            raise RuntimeError(f"TRADOVATE_ACCOUNT_ID={override_id} not found among this login's accounts")
        account = match

    _account_id = account["id"]
    _account_spec = account["name"]
    log.info("Using Tradovate account: %s (id=%s)", _account_spec, _account_id)
    return _account_id, _account_spec


def place_market_order(symbol: str, side: str, qty: int) -> dict:
    """side must be 'Buy' or 'Sell'."""
    account_id, account_spec = _get_account()
    body = {
        "accountSpec": account_spec,
        "accountId": account_id,
        "action": side,
        "symbol": symbol,
        "orderQty": qty,
        "orderType": "Market",
        "isAutomated": True,
    }
    resp = requests.post(f"{BASE_URL}/order/placeorder", headers=_headers(), json=body, timeout=15)
    resp.raise_for_status()
    return resp.json()


def execute_signal(symbol: str, action: str, qty: int) -> dict:
    """
    action: 'long' -> Buy, 'short' -> Sell, 'close_long' -> Sell (flatten),
    'close_short' -> Buy (flatten).

    Deliberately simple for v1: this places a market order in the requested
    direction and relies on Tradovate's own position netting to open/flip/
    close as appropriate — it does NOT check Tradovate's actual current
    position via /position/list before ordering. The Pine strategy's own
    no-reentry logic (pyramiding=0 + position-size checks) should already
    prevent duplicate same-direction signals from firing in the first
    place, and the webhook server's short dedupe window guards against
    TradingView redelivering the same alert — but if this is going to run
    unattended for real money over a long stretch, add an explicit
    position-check-before-order step here as a second line of defense.
    """
    side_map = {"long": "Buy", "short": "Sell", "close_long": "Sell", "close_short": "Buy"}
    if action not in side_map:
        raise ValueError(f"Unknown action: {action}")
    return place_market_order(symbol=symbol, side=side_map[action], qty=qty)
