import logging
from os.path import dirname
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Logging
LOG_LEVEL = logging.INFO

# Directories
PROJECT_ROOT = Path(dirname(__file__)).parent
DATA_DIR = PROJECT_ROOT / "data"

# Change this to your device IP in Zerotier network. Use 127.0.0.1 when running on RPI
MAVLINK_IP = "172.25.0.101"

# Database
USE_SQLITE = True
SQLITE_PATH = DATA_DIR / "sqlite.db"
