"""Order placement logic — bridges validation, client, and presentation."""
import logging
from typing import Any, Dict, Optional

from bot.client import BinanceClient, BinanceClientError
from bot.validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

logger = logging.getLogger("trading_bot")


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
) -> Dict[str, Any]:
    """Validate inputs, place order, and return result dict."""
    # Validate
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    stop_price = validate_stop_price(stop_price, order_type)

    # Summarize
    summary = (
        f"Order Request: {side} {quantity} {symbol} "
        f"({order_type})"
    )
    if price:
        summary += f" @ {price}"
    if stop_price:
        summary += f" stop={stop_price}"
    logger.info(summary)
    print(f"\n{'='*50}")
    print(f"  {summary}")
    print(f"{'='*50}")

    # Execute
    result = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price,
    )

    # Present
    print(f"\n  ✅ Order placed successfully!")
    print(f"  Order ID   : {result.get('orderId')}")
    print(f"  Status     : {result.get('status')}")
    print(f"  Executed   : {result.get('executedQty')}")
    print(f"  Avg Price  : {result.get('avgPrice', 'N/A')}")
    print(f"{'='*50}\n")

    logger.info(
        "Order success: orderId=%s status=%s executedQty=%s avgPrice=%s",
        result.get("orderId"),
        result.get("status"),
        result.get("executedQty"),
        result.get("avgPrice"),
    )
    return result
