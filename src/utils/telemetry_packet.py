import datetime
from typing import Optional, List

from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import MAVLink, MAVLink_message

from utils.compression import compress, decompress
from utils.fifo import FIFOQueue
from utils.mavlink_packet import merge_packages, split_packages


# Custom datagram (Telemetry Packet) format:
# 1 byte: start byte (0xFE)
# 2 bytes: length of payload (in bytes) = n
# 8 bytes: timestamp (in milliseconds)
# the following data is gzipped (n bytes after compression)
# 1 byte: identifier length (in bytes) = m
# m bytes: identifier
# x bytes: payload (up to 100 mavlink messages concatenated)
class TelemetryPacket:
    def __init__(self, robot_id: str, message_bytes: List[bytes],
                 timestamp: datetime.datetime = None):
        self.robot_id = robot_id
        self.message_bytes = message_bytes
        self.timestamp = timestamp
        if timestamp is None:
            self.timestamp = datetime.datetime.now()

    @classmethod
    def _add_robot_id(cls, robot_id: str, payload: bytes) -> bytes:
        robot_id = robot_id.encode("utf-8")
        identifier_length = len(robot_id).to_bytes(1, byteorder="big")

        return identifier_length + robot_id + payload

    @classmethod
    def _add_packet_header(cls, payload: bytes, timestamp: datetime.datetime) -> bytes:
        compressed_payload = compress(payload)
        payload_length = len(compressed_payload).to_bytes(2, byteorder="big")
        timestamp = int(timestamp.timestamp() * 1000).to_bytes(8, byteorder="big")
        start_byte = b"\xFE"

        return start_byte + payload_length + timestamp + compressed_payload

    @classmethod
    def from_queue(cls, robot_id: str, queue: FIFOQueue, limit: int = 100) -> 'TelemetryPacket':
        messages = []  # type:[mavutil.mavlink.MAVLink_message]
        for i in range(limit):
            if queue.is_empty():
                break
            messages.append(queue.dequeue())
        messages_binary = [m._msgbuf for m in messages]
        return cls(robot_id=robot_id, message_bytes=messages_binary)

    def get_messages(self) -> [MAVLink_message]:
        parser = MAVLink(None)
        return parser.parse_buffer(merge_packages(self.message_bytes))

    def to_bytes(self) -> bytes:
        payload = self._add_robot_id(self.robot_id, merge_packages(self.message_bytes))
        return self._add_packet_header(payload, self.timestamp)

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional['TelemetryPacket']:
        try:
            start_index = data.index(b"\xfe")

            payload_length = int.from_bytes(data[start_index + 1:start_index + 3], byteorder="big")
            timestamp = int.from_bytes(data[start_index + 3:start_index + 11], byteorder="big")
            compressed_payload = data[start_index + 11:start_index + 11 + payload_length]

            payload = decompress(compressed_payload)
            identifier_length = int.from_bytes(payload[0:1], byteorder="big")
            robot_id = payload[1:1 + identifier_length].decode("utf-8")
            message_bytes = payload[1 + identifier_length:]

            return cls(robot_id=robot_id, message_bytes=split_packages(message_bytes),
                       timestamp=datetime.datetime.fromtimestamp(timestamp / 1000.0))
        except ValueError:
            return None


if __name__ == '__main__':
    mavlink_packets = [
        b"\xfd\x32\x00\x00\xdd\x01\x01\x7c\x00\x00\x30\x33\xb6\x32\x27\x00"
        b"\x00\x00\x1d\x55\x31\x1a\xbd\xbd\xa4\xd0\x72\x84\x04\x00\x00\x00"
        b"\x00\x00\x37\x00\x46\x00\x00\x00\xbc\x02\x06\x1a\x00\x60\x86\x71"
        b"\xf7\x03\x00\x14\x00\x00\x00\x1c\x00\x00\x00\xe6\x12\xab",
        b"\xfd\x05\x00\x00\x64\x01\x01\x7d\x00\x00\xd7\x12\x59\x13\x05\xd4\xfb",
        b"\xfd\x10\x00\x00\x26\x03\x01\x74\x00\x00\x49\xc0\x61\x01\x0b\x00"
        b"\xb5\x00\x95\xfc\x30\x00\x36\x00\xb1\xff\xc2\x55"
    ]

    packet = TelemetryPacket(robot_id="ROBOT_ID", message_bytes=mavlink_packets)
    packet_bytes = packet.to_bytes()
    packet2 = TelemetryPacket.from_bytes(packet_bytes)

    print(packet2.robot_id)
    print(packet2.timestamp)
    print(packet2.message_bytes)
