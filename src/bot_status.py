import datetime
from queue import Queue
from typing import Dict, Tuple, Optional

from pymavlink.dialects.v20.ardupilotmega import MAVLink_message

from db import Robot, RawMessage
from utils.fifo import FIFOQueue
from utils.util import get_logger

_robots = {}  # type: Dict[str, RobotStatus]
messages_to_update_queue = Queue()  # type:Queue[Tuple[str, datetime.datetime, MAVLink_message]]


def get_messages_to_update_queue():
    return messages_to_update_queue


def get_robot(robot_id: str) -> 'RobotStatus':
    return _robots.get(robot_id, None)


def get_robots() -> dict:
    return _robots


class RobotStatus:
    def __init__(self, robot_id: str):
        self.robot_id = robot_id
        self.status_messages: Dict[str, MAVLink_message] = {}
        self.status_message_update_times: Dict[str, datetime.datetime] = {}
        self.last_update_time = None

    def update_status_message(self, message: MAVLink_message, timestamp: datetime.datetime):
        self.status_messages[message.get_type().upper()] = message
        self.status_message_update_times[message.get_type().upper()] = timestamp
        self.last_update_time = timestamp
        get_logger().debug(f"Robot {self.robot_id} status updated: {message.get_type()}")

    def _get_status(self, message_type: str) -> Tuple[
        Optional[MAVLink_message], Optional[datetime.datetime]]:
        message_type = message_type.upper()
        return self.status_messages.get(message_type, None), self.status_message_update_times.get(
            message_type, None)

    def get_status_json(self, message_type: str) -> Dict:
        message, timestamp = self._get_status(message_type)
        if message is None:
            return {}
        return {
            "timestamp": int(timestamp.timestamp() * 1000),
            "message": message.to_dict()
        }

    def is_online(self) -> bool:
        return self.last_update_time is not None and (
                datetime.datetime.now() - self.last_update_time).total_seconds() < 5


class SimulatedRobotStatus(RobotStatus):
    def __init__(self, robot_id: str, reference_robot_id: str):
        super().__init__(robot_id)
        self.reference_robot_id = reference_robot_id

    def get_status_json(self, message_type: str) -> Dict:
        # Get raw message from table "raw_messages" with message_type and reference_robot_id
        message_row = RawMessage.get(RawMessage.message_type == message_type,
                                     RawMessage.robot_id == self.reference_robot_id)
        if message_row is None:
            return {}
        return {
            "timestamp": int(datetime.datetime.now().timestamp() * 1000),
            "message": message_row.message
        }

    def is_online(self) -> bool:
        return True


def thread_bot_status():
    # Load device info from database and initialize the status
    robot_ids = [robot.id for robot in Robot.select()]
    for robot_id in robot_ids:
        get_robots()[robot_id] = RobotStatus(robot_id)
    get_logger().info(f"Loaded {len(robot_ids)} robot(s) from database")

    # Create a simulated robot
    get_robots()["RPI_SIM"] = SimulatedRobotStatus("RPI_SIM", "RPI2")
    get_logger().info(f"Simulated robot {'simulated'} created")

    queue = get_messages_to_update_queue()
    while True:
        (robot_id, timestamp, message) = queue.get(block=True)
        if message:
            robot_status = get_robot(robot_id)
            robot_status.update_status_message(message, timestamp)


if __name__ == '__main__':
    simulated = SimulatedRobotStatus("simulated", "RPI2")
    print(simulated.get_status_json("HEARTBEAT"))
