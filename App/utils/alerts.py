import os
from datetime import datetime
from App.config import ALERT_LOG_FILE
from App.core.logger import logger

os.makedirs(os.path.dirname(ALERT_LOG_FILE), exist_ok=True)

def log_alert(user_id, alert_type, message=None):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"[{timestamp}] User: {user_id} | Type: {alert_type}"
        if message:
            alert_message += f" | Message: {message}"
        
        with open(ALERT_LOG_FILE, 'a') as f:
            f.write(alert_message + "\\n")
        
        logger.info(f"Alert logged: {alert_message}")
    except Exception as e:
        logger.error(f"Failed to log alert: {e}")
        raise