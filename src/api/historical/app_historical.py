from datetime import datetime

from flask import Blueprint

from bot_status import get_robot, get_robots

historical_api = Blueprint('historical_api', __name__)

