# Binance Futures Testnet Trading Bot

A clean, structured Python CLI tool for placing orders on Binance Futures Testnet (USDT-M).

## Features

- **Market & Limit orders** on Binance Futures Testnet
- **Stop-Limit orders** (bonus feature)
- **BUY and SELL** sides
- Input validation with clear error messages
- Structured logging to file + console
- Clean separation: client layer, order logic, validators, CLI

## Setup

### 1. Prerequisites

- Python 3.8+
- Binance Futures Testnet account → [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

### 2. Install dependencies

```bash
pip install -r requirements.txt


Note:
Binance Futures Testnet may not immediately execute orders due to limited liquidity.
Orders may remain in "NEW" status even though they are successfully placed.