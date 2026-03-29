"""Input validation for trading bot parameters."""
import re
from typing import Optional


class ValidationError(Exception):
    """Raised when user input fails validation."""


def validate_symbol(symbol: str) -> str:
    """Validate and normalize a trading symbol."""
    symbol = symbol.upper().strip()
    if not re.match(r"^[A-Z]{2,10}USDT$", symbol):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Expected format like BTCUSDT, ETHUSDT."
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    side = side.upper().strip()
    if side not in ("BUY", "SELL"):
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    order_type = order_type.upper().strip()
    allowed = ("MARKET", "LIMIT", "STOP")
    if order_type not in allowed:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(allowed)}."
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    """Validate order quantity."""
    if quantity <= 0:
        raise ValidationError(f"Quantity must be positive, got {quantity}.")
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Validate price based on order type."""
    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValidationError("Price is required and must be positive for LIMIT orders.")
    if order_type == "STOP" and (price is None or price <= 0):
        raise ValidationError("Price is required and must be positive for STOP orders.")
    if price is not None and price < 0:
        raise ValidationError(f"Price cannot be negative, got {price}.")
    return price


def validate_stop_price(stop_price: Optional[float], order_type: str) -> Optional[float]:
    """Validate stop price for STOP orders."""
    if order_type == "STOP" and (stop_price is None or stop_price <= 0):
        raise ValidationError("Stop price is required and must be positive for STOP orders.")
    return stop_price
