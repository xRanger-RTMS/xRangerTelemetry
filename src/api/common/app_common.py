from datetime import datetime

from flask import Blueprint

from bot_status import get_robot, get_robots

common_api = Blueprint('common_api', __name__)

@common_api.route('/status')
def status():
    return {
        "status": "online"
    }

@common_api.route('/time')
def time():
    # return the current timestamp in milliseconds
    timestamp = int(datetime.now().timestamp() * 1000)
    return {
        "time": timestamp
    }