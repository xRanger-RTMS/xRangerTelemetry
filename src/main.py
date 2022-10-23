import time
from threading import Thread

from db import raw_message_queue, RawMessage
from receiver import get_mavlink_connections, receive_all
from util import IntervalThread, get_logger

if __name__ == '__main__':
    mavlink_connections = get_mavlink_connections()
    get_logger().info(f'Found {len(mavlink_connections)} mavlink connections')
    receive_threads = []

    for connection in mavlink_connections:
        thread = Thread(target=receive_all, args=(connection, raw_message_queue), daemon=True)
        receive_threads.append(thread)
        thread.start()

    save_thread = IntervalThread(1, lambda: RawMessage.from_queue(raw_message_queue))

    while True:
        time.sleep(1)