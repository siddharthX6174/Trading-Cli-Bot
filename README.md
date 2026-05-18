# Trading Bot

Small Binance Futures (USDT-M) testnet trading bot exposing a simple HTTP API and a CLI for placing orders.

**Key features**
- HTTP endpoints: `/health`, `/order`
- CLI tool to place orders from the command line
- Supports `MARKET`, `LIMIT`, and `STOP_LIMIT` orders (STOP_LIMIT implemented using Binance Futures `STOP` type)
- Logging to `logs/trading_bot.log`

**Python compatibility**
- Developed for Python 3.9+ (typing `tuple[...]` used). If you need wider compatibility, update `bot/validators.py` typings.

## Setup

1. Clone the repo
2. Create and activate a virtual environment (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
# Note: keep `python-binance` and `python-dotenv`; remove any duplicate/conflicting `binance` package if present.
```

4. Create a `.env` file in the project root containing your testnet keys:

```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

5. Run the web API

```bash
python app.py
```

The server runs on port 5000 by default (Flask debug mode configured in `app.py`).

## HTTP Endpoints

- `GET /health`
	- Returns 200 with `{ "status": "ok" }` when the service is up.

- `POST /order`
	- Place an order. Expect `application/json` body with fields:
		- `symbol` (string) — e.g. `BTCUSDT`
		- `side` (string) — `BUY` or `SELL`
		- `order_type` (string) — `MARKET`, `LIMIT`, or `STOP_LIMIT`
		- `quantity` (number)
		- `price` (number) — required for `LIMIT` and `STOP_LIMIT`
		- `stop_price` (number) — required for `STOP_LIMIT` (trigger price)

	- Example request body:

```json
{
	"symbol": "BTCUSDT",
	"side": "BUY",
	"order_type": "LIMIT",
	"quantity": 0.001,
	"price": 30000
}
```

	- Response: JSON with a success message and selected order fields (orderId, status, type, executedQty, avgPrice). The exact response keys come from the `python-binance` client.

## CLI Usage

Use the `cli.py` script to place orders from the command line. Example:

```powershell
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.001

# LIMIT example
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.001 --price 35000

# STOP_LIMIT example
python cli.py --symbol BTCUSDT --side SELL --order_type STOP_LIMIT --quantity 0.001 --price 34900 --stop_price 35100
```

## Behaviour notes

- `LIMIT` and `STOP_LIMIT` orders set `timeInForce=GTC` by default (see `bot/orders.py`).
- `STOP_LIMIT` is implemented using Binance Futures `STOP` order type: `price` is the limit price, `stopPrice` is the trigger price.
- `bot/validators.py` enforces basic input validation for required fields and numeric values.
- `bot/client.py` creates a testnet client (`testnet=True`) and overrides `FUTURES_URL`; verify this is appropriate for your `python-binance` version.

## Logging

Logs are written to `logs/trading_bot.log` and warnings/errors also print to the console. The logger is configured in `bot/logging_config.py`.


## Contributing / Safety

- Do not commit real API keys. Use `.env` and add it to `.gitignore`.
- If you want, I can add a `.env.example` and basic unit tests next.

---