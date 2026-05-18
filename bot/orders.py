from binance.enums import TIME_IN_FORCE_GTC
from binance.exceptions import BinanceAPIException, BinanceRequestException
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
        logger.info("Order success | response: %s", response)
        return response
    except BinanceAPIException as exc:
        logger.error(
            "Binance API error | code=%s | message=%s | params=%s",
            getattr(exc, "code", None),
            getattr(exc, "message", str(exc)),
            params,
        )
        if getattr(exc, "code", None) == -2015:
            raise PermissionError(
                "Binance rejected the API key for this testnet endpoint. "
                "Use Binance Futures Testnet credentials and confirm any IP whitelist settings."
            ) from exc
        raise
    except BinanceRequestException as exc:
        logger.error("Binance network/request error | params=%s | error=%s", params, exc)
        raise ConnectionError("Network failure while calling Binance Futures.") from exc
    except Exception as exc:
        logger.error("Unexpected order failure | params=%s | error=%s", params, exc)
        raise