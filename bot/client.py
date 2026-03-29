"""Binance Futures Testnet API client."""
import hashlib
import hmac
import time
import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

logger = logging.getLogger("trading_bot")

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClientError(Exception):
    """Raised on API-level errors."""
    def __init__(self, status_code: int, code: int, message: str):
        self.status_code = status_code
        self.code = code
        super().__init__(f"Binance API error {code}: {message}")


class BinanceClient:
    """Thin wrapper around the Binance Futures Testnet REST API."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    # ---- internal helpers ----

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params: Dict[str, Any],
                 signed: bool = True) -> Dict[str, Any]:
        if signed:
            params = self._sign(params)
        url = f"{self.base_url}{path}"
        logger.debug("REQUEST  %s %s params=%s", method, url,
                      {k: v for k, v in params.items() if k != "signature"})
        try:
            resp = self.session.request(method, url, params=params, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            logger.error("Network error: %s", exc)
            raise ConnectionError(f"Could not reach {url}") from exc
        except requests.exceptions.Timeout as exc:
            logger.error("Request timed out: %s", exc)
            raise TimeoutError("Request timed out") from exc

        logger.debug("RESPONSE %s %s", resp.status_code, resp.text[:500])

        if resp.status_code >= 400:
            body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            raise BinanceClientError(
                resp.status_code,
                body.get("code", resp.status_code),
                body.get("msg", resp.text),
            )
        return resp.json()

    # ---- public API ----

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        """Place an order on Binance Futures Testnet."""
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force
        elif order_type == "STOP":
            params["price"] = price
            params["stopPrice"] = stop_price
            params["timeInForce"] = time_in_force

        return self._request("POST", "/fapi/v1/order", params)

    def get_account(self) -> Dict[str, Any]:
        """Fetch account information (useful for connectivity check)."""
        return self._request("GET", "/fapi/v2/account", {})
