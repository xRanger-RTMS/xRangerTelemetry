import logging
import os
from os.path import dirname
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# [Directories]
PROJECT_ROOT = Path(dirname(__file__)).parent
DATA_DIR = PROJECT_ROOT / "data"

# [Database]
DB_USE_SQLITE = True
DB_SQLITE_PATH = DATA_DIR / "sqlite.db"

# [Logging]
LOG_LEVEL = logging.INFO
LOG_TO_FILE = os.environ.get("LOG_TO_FILE", "False") == "True"
LOG_FILE = DATA_DIR / "log.txt"

# [Telemetry Connection]
TELE_UDP_BUFFER_SIZE = 25536
TELE_LISTEN_IP = os.environ.get("UDP_LISTEN_IP", "127.0.0.1")
TELE_LISTEN_PORTS = [20000]

# [API Server]
API_LISTEN_IP = os.environ.get("API_LISTEN_IP", "127.0.0.1")
API_LISTEN_PORT = os.environ.get("API_LISTEN_PORT", 15000)