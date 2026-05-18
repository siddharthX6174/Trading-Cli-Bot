import argparse
import os
from dotenv import load_dotenv
from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--symbol",     required=True,  help="Trading pair       e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--order_type", required=True,  help="MARKET, LIMIT, or STOP_LIMIT")
    parser.add_argument("--quantity",   required=True,  type=float, help="Order quantity     e.g. 0.01")
    parser.add_argument("--price",      required=False, type=float, help="Limit price        (LIMIT / STOP_LIMIT)")
    parser.add_argument("--stop_price", required=False, type=float, help="Trigger price      (STOP_LIMIT only)")

    args = parser.parse_args()

    data = {
        "symbol":     args.symbol,
        "side":       args.side,
        "order_type": args.order_type,
        "quantity":   args.quantity,
        "price":      args.price,
        "stop_price": args.stop_price,
    }

    # Validate
    is_valid, error_msg = validate_order(data)
    if not is_valid:
        print(f"\n❌ Validation Error: {error_msg}\n")
        return

    # Print request summary
    print("\n========== Order Request ==========")
    print(f"  Symbol      : {data['symbol'].upper()}")
    print(f"  Side        : {data['side'].upper()}")
    print(f"  Order Type  : {data['order_type'].upper()}")
    print(f"  Quantity    : {data['quantity']}")
    if data.get("price"):
        print(f"  Limit Price : {data['price']}")
    if data.get("stop_price"):
        print(f"  Stop Price  : {data['stop_price']}")
    print("====================================\n")

    try:
        client = get_client(
            os.getenv("BINANCE_API_KEY"),
            os.getenv("BINANCE_API_SECRET")
        )
        response = place_order(
            client=client,
            symbol=data["symbol"],
            side=data["side"],
            order_type=data["order_type"],
            quantity=data["quantity"],
            price=data.get("price"),
            stop_price=data.get("stop_price")
        )

        print("========== Order Response ==========")
        print(f"  Order ID     : {response.get('orderId')}")
        print(f"  Status       : {response.get('status')}")
        print(f"  Type         : {response.get('type')}")
        print(f"  Executed Qty : {response.get('executedQty')}")
        print(f"  Avg Price    : {response.get('avgPrice')}")
        if response.get("stopPrice"):
            print(f"  Stop Price   : {response.get('stopPrice')}")
        print("=====================================")
        print("\n Order placed successfully!\n")

    except Exception as e:
        print(f"\n Failed to place order: {e}\n")

if __name__ == "__main__":
    main()