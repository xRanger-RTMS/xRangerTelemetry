import datetime
import time

from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import MAVLink

from bot_status import get_messages_to_update_queue
from config import TELE_LISTEN_IP, TELE_LISTEN_PORTS
from db import messages_to_save_queue, get_messages_to_save_queue
from utils.fifo import FIFOQueue
from utils.telemetry_packet import TelemetryPacket
from utils.udp import UdpPort
from utils.util import get_logger

_tele_packet_connections = {}


def get_tele_packet_connection(port: int = None) -> UdpPort:
    global _tele_packet_connections
    if port is None:
        port = TELE_LISTEN_PORTS[0]
    if port not in _tele_packet_connections:
        _tele_packet_connections[port] = UdpPort(TELE_LISTEN_IP, port)
    return _tele_packet_connections[port]


def get_tele_packet_connections() -> [UdpPort]:
    return list(_tele_packet_connections.values())


def thread_tele_receiver():
    connection = get_tele_packet_connection()
    get_logger().info(
        f'Starting receive thread for tele packet connection: {connection.listen_ip}:{connection.listen_port}')
    while True:
        data, addr = connection.receive()
        tele_packet = TelemetryPacket.from_bytes(data)
        if tele_packet is not None:
            messages = tele_packet.get_messages()
            if messages is not None:
                for msg in messages:
                    get_logger().debug(f'Received message: {msg.to_dict()}')
                    message_info = (tele_packet.robot_id, tele_packet.timestamp, msg)

                    get_messages_to_save_queue().enqueue(message_info)
                    get_messages_to_update_queue().put(message_info)
            else:
                get_logger().debug(
                    f'Failed to get mavlink messages from tele packet: {tele_packet.to_bytes()}')
        else:
            get_logger().debug(f'Failed to parse tele packet: {data}')

if __name__ == '__main__':
    # receive_all(get_mavlink_connections()[0], raw_message_queue)

    parser = MAVLink(None)
    mavlink_packets = [
        b"\xfd\x32\x00\x00\xdd\x01\x01\x7c\x00\x00\x30\x33\xb6\x32\x27\x00"
        b"\x00\x00\x1d\x55\x31\x1a\xbd\xbd\xa4\xd0\x72\x84\x04\x00\x00\x00"
        b"\x00\x00\x37\x00\x46\x00\x00\x00\xbc\x02\x06\x1a\x00\x60\x86\x71"
        b"\xf7\x03\x00\x14\x00\x00\x00\x1c\x00\x00\x00\xe6\x12\xab",
        b"\xfd\x05\x00\x00\x64\x01\x01\x7d\x00\x00\xd7\x12\x59\x13\x05\xd4\xfb",
        b"\xfd\x10\x00\x00\x26\x03\x01\x74\x00\x00\x49\xc0\x61\x01\x0b\x00"
        b"\xb5\x00\x95\xfc\x30\x00\x36\x00\xb1\xff\xc2\x55"
    ]
    msg = parser.parse_buffer(b"".join(mavlink_packets))

    print(msg)
