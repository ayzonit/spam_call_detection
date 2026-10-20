import os
from dotenv import load_dotenv
load_dotenv()

# App Config
APP_NAME = os.getenv("APP_NAME", "VoiceAuthAPI")
APP_ENV = os.getenv("APP_ENV", "dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Model paths
MODEL_DIR = os.getenv("MODEL_DIR", "models")
SPEAKER_MODEL_PATH = os.path.join(MODEL_DIR, "speaker_model.pt")
SPOOF_MODEL_PATH = os.path.join(MODEL_DIR, "spoof_model.pt")

# Embeddings storage
EMBEDDINGS_DIR = os.getenv("EMBEDDINGS_DIR", "models/embeddings")

# Verification thresholds
THRESHOLD_SPEAKER = float(os.getenv("THRESHOLD_SPEAKER", 0.75))
THRESHOLD_SPOOF = float(os.getenv("THRESHOLD_SPOOF", 0.15))

# Alerts / Notifications
ALERT_LOG_FILE = os.getenv("ALERT_LOG_FILE", "logs/alerts.log")
ALERT_WEBHOOK = os.getenv("ALERT_WEBHOOK", None)

# Audio processing
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 16000))
N_MFCC = int(os.getenv("N_MFCC", 20))
TOP_DB_TRIM = int(os.getenv("TOP_DB_TRIM", 25))

# Misc
DEBUG_MODE = APP_ENV == "dev"