import datetime
import time

from pymavlink import mavutil

from config import MAVLINK_IP
from db import raw_message_queue
from util import get_logger


def get_mavlink_connections() -> [mavutil.mavlink_connection]:
    return [mavutil.mavlink_connection(f'udpin:{MAVLINK_IP}:14550')]

def receive_all(connection, target_queue):
    get_logger().info(f'Starting receive thread for mavlink connection: {connection.address}')
    while True:
        msg = connection.recv_match(blocking=True)
        msg.timestamp = datetime.datetime.now()
        target_queue.enqueue(msg)

if __name__ == '__main__':
    receive_all(get_mavlink_connections()[0], raw_message_queue)