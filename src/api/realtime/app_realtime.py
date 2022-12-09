from flask import Blueprint

from bot_status import get_robot, get_robots

realtime_api = Blueprint('realtime_api', __name__, url_prefix='/api/realtime')


@realtime_api.route('/status')
def status():
    return {
        "message": "OK"
    }


@realtime_api.route('/list/')
def online_list():
    return {
        "robots": [
            {
                "robot_id": robot_id,
                "online": robot.is_online(),
                "last_update_time": robot.last_update_time.timestamp() * 1000 if robot.last_update_time else None
            }
            for robot_id, robot in get_robots().items()
        ]
    }

@realtime_api.route('/robot/<robot_id>/')
def status_info(robot_id: str):
    robot = get_robot(robot_id)
    if robot is None:
        return {
                   "code": 404,
                   "message": f"Robot with robot_id={robot_id} not found"
               }, 404
    return {
        "robot_id": robot_id,
        "is_online": robot.is_online(),
        "last_update_time": robot.last_update_time.timestamp() * 1000 if robot.last_update_time is not None else None
    }


@realtime_api.route('/robot/<robot_id>/<message_type>')
def detailed_info(robot_id: str, message_type: str):
    robot = get_robot(robot_id)
    if robot is None:
        return {
                   "code": 404,
                   "message": f"Robot with robot_id={robot_id} not found"
               }, 404
    return robot.get_status_json(message_type)
