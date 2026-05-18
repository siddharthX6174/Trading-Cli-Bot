import logging
import os

def setup_logger(name="trading_bot"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("logs/trading_bot.log")
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger