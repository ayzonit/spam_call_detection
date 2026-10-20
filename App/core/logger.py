import logging
import os
from logging.handlers import RotatingFileHandler
from App.config import LOG_LEVEL

# Create logs folder
os.makedirs("logs", exist_ok=True)
LOG_FILE = os.path.join("logs", "app.log")

def setup_logger():
    logger = logging.getLogger("voice_auth")
    logger.setLevel(LOG_LEVEL.upper() if LOG_LEVEL else "INFO")
    logger.handlers = []

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL.upper() if LOG_LEVEL else "INFO")
    ch_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(ch_formatter)

    # File handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    fh.setLevel(LOG_LEVEL.upper() if LOG_LEVEL else "INFO")
    fh_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(fh_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info("Logger initialized successfully")

    return logger

logger = setup_logger()