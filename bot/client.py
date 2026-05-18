from binance.client import Client
from bot.logging_config import setup_logger

logger = setup_logger()

def get_client(api_key: str, api_secret: str) -> Client:
    if not api_key or not api_secret:
        raise ValueError("API key and secret must be set in .env")

    client = Client(api_key, api_secret, testnet=True)
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    logger.info("Binance Futures Testnet client initialized.")
    return client