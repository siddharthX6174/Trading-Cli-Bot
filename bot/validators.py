VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_LIMIT"]

def validate_order(data: dict) -> tuple[bool, str]:
    symbol     = data.get("symbol", "")
    side       = data.get("side", "").upper()
    order_type = data.get("order_type", "").upper()
    quantity   = data.get("quantity")
    price      = data.get("price")
    stop_price = data.get("stop_price")

    if not symbol:
        return False, "Symbol is required (e.g. BTCUSDT)."

    if side not in VALID_SIDES:
        return False, "Side must be BUY or SELL."

    if order_type not in VALID_ORDER_TYPES:
        return False, "Order type must be MARKET, LIMIT, or STOP_LIMIT."

    try:
        if float(quantity) <= 0:
            return False, "Quantity must be a positive number."
    except (TypeError, ValueError):
        return False, "Quantity must be a valid number."

    if order_type == "LIMIT":
        try:
            if float(price) <= 0:
                return False, "Price must be positive for LIMIT orders."
        except (TypeError, ValueError):
            return False, "Price is required for LIMIT orders."

    if order_type == "STOP_LIMIT":
        try:
            if float(price) <= 0:
                return False, "Price (limit price) must be positive for STOP_LIMIT orders."
        except (TypeError, ValueError):
            return False, "Price (limit price) is required for STOP_LIMIT orders."
        try:
            if float(stop_price) <= 0:
                return False, "Stop price must be positive for STOP_LIMIT orders."
        except (TypeError, ValueError):
            return False, "Stop price is required for STOP_LIMIT orders."

    return True, ""