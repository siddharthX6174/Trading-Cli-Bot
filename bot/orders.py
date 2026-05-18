from binance.enums import TIME_IN_FORCE_GTC
from bot.logging_config import setup_logger

logger = setup_logger()

def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Places MARKET, LIMIT, or STOP_LIMIT orders on Binance Futures Testnet.

    STOP_LIMIT on Binance Futures uses type=STOP with:
      - price      → the limit price (order executes at this price or better)
      - stopPrice  → the trigger price (order is activated when market hits this)
    """

    params = {
        "symbol":   symbol.upper(),
        "side":     side.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "MARKET":
        params["type"] = "MARKET"

    elif order_type.upper() == "LIMIT":
        params["type"]        = "LIMIT"
        params["price"]       = price
        params["timeInForce"] = TIME_IN_FORCE_GTC

    elif order_type.upper() == "STOP_LIMIT":
        params["type"]        = "STOP"          # Binance Futures uses STOP for stop-limit
        params["price"]       = price           # limit price
        params["stopPrice"]   = stop_price      # trigger price
        params["timeInForce"] = TIME_IN_FORCE_GTC

    logger.info(f"Placing {order_type.upper()} order | params: {params}")

    try:
        response = client.futures_create_order(**params)
        logger.info(f"Order success | response: {response}")
        return response
    except Exception as e:
        logger.error(f"Order failed | error: {e}")
        raise