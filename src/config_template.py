import logging
from os.path import dirname
from pathlib import Path

# Logging
LOG_LEVEL = logging.DEBUG

PROJECT_ROOT = Path(dirname(__file__)).parent
DATA_DIR = PROJECT_ROOT / "data"

# Change this to your device IP in Zerotier network. Use 127.0.0.1 when running on RPI
MAVLINK_IP = "127.0.0.1"

USE_SQLITE = True
SQLITE_PATH = DATA_DIR / "data.db"