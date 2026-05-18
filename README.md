## Setup
1. Clone the repo
2. pip install -r requirements.txt
3. Create .env with your Binance Testnet API keys
4. python app.py

## Endpoints
POST /order — place a market or limit order
GET /health — check server status

## Assumptions
- Uses Binance USDT-M Futures Testnet
- LIMIT orders require timeInForce=GTC