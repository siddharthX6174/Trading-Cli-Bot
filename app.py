from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger

load_dotenv()
app = Flask(__name__)
logger = setup_logger()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/order", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    is_valid, error_msg = validate_order(data)
    if not is_valid:
        logger.warning(f"Validation failed: {error_msg}")
        return jsonify({"error": error_msg}), 400

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

        result = {
            "message":     "Order placed successfully.",
            "orderId":     response.get("orderId"),
            "status":      response.get("status"),
            "type":        response.get("type"),
            "executedQty": response.get("executedQty"),
            "avgPrice":    response.get("avgPrice"),
        }
        if response.get("stopPrice"):
            result["stopPrice"] = response.get("stopPrice")

        return jsonify(result), 200

    except (PermissionError, ConnectionError, ValueError) as e:
        logger.error("Flask order error: %s", e)
        return jsonify({"error": str(e)}), 400
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error("Flask Binance error: %s", e)
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        logger.exception("Unhandled Flask order error")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)