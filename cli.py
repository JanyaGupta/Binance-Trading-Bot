#!/usr/bin/env python3
"""CLI entry point for the Binance Futures Testnet trading bot."""
import argparse
import os
import sys

from bot.client import BinanceClient, BinanceClientError
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import ValidationError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Market buy
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit sell
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000

  # Stop-limit order (bonus)
  python cli.py --symbol ETHUSDT --side SELL --type STOP --quantity 0.01 --price 2400 --stop-price 2450
""",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
                        help="Order side")
    parser.add_argument("--type", required=True, dest="order_type",
                        choices=["MARKET", "LIMIT", "STOP", "market", "limit", "stop"],
                        help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, default=None,
                        help="Limit price (required for LIMIT and STOP)")
    parser.add_argument("--stop-price", type=float, default=None,
                        help="Stop trigger price (required for STOP)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = setup_logging()

    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("❌ Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.")
        logger.error("Missing API credentials in environment.")
        sys.exit(1)

    client = BinanceClient(api_key, api_secret)

    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as exc:
        print(f"❌ Validation error: {exc}")
        logger.error("Validation error: %s", exc)
        sys.exit(1)
    except BinanceClientError as exc:
        print(f"❌ API error: {exc}")
        logger.error("API error: %s", exc)
        sys.exit(1)
    except (ConnectionError, TimeoutError) as exc:
        print(f"❌ Network error: {exc}")
        logger.error("Network error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
