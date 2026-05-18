import os

from binance.client import Client
from bot.logging_config import setup_logger

logger = setup_logger()

DEFAULT_FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"

def get_client(api_key: str, api_secret: str) -> Client:
    if not api_key or not api_secret:
        raise ValueError("API key and secret must be set in .env")

    futures_url = os.getenv("BINANCE_FUTURES_BASE_URL", DEFAULT_FUTURES_TESTNET_URL).rstrip("/")

    client = Client(api_key, api_secret, ping=False)
    client.FUTURES_URL = futures_url
    logger.info("Binance Futures client initialized | futures_url=%s", futures_url)
    return client