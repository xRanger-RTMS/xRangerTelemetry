from typing import List

from peewee import *
from pymavlink import mavutil

from config import DB_SQLITE_PATH
import datetime

from utils.fifo import FIFOQueue
from utils.interval_thread import IntervalThread
from utils.util import get_logger

_db = SqliteDatabase(DB_SQLITE_PATH)
messages_to_save_queue = None


def get_connection():
    if _db.is_closed():
        _db.connect()
    return _db


def get_messages_to_save_queue():
    global messages_to_save_queue
    if messages_to_save_queue is None:
        messages_to_save_queue = FIFOQueue()
    return messages_to_save_queue


class BaseModel(Model):
    class Meta:
        database = get_connection()


class Device(BaseModel):
    id = CharField(primary_key=True)
    connectionAddress = CharField(unique=True)
    connectionPort = IntegerField()


class RawMessage(BaseModel):
    id = PrimaryKeyField()
    robot_id = ForeignKeyField(Device, backref='raw_messages')
    system_id = IntegerField()
    component_id = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    message_type = CharField()
    message = TextField()

    class Meta:
        db_table = 'raw_messages'

    @classmethod
    def from_mavlink_message(cls, robot_id: str, timestamp:datetime.datetime,
                             message: mavutil.mavlink.MAVLink_message) -> 'RawMessage':
        msg_dict = message.to_dict()
        system_id, component_id = message._msgbuf[5:7]
        return RawMessage(robot_id=robot_id, system_id=system_id, component_id=component_id,
                          timestamp=timestamp,
                          message_type=message.get_type(), message=str(msg_dict))

    @classmethod
    def from_queue(cls, queue: FIFOQueue, limit: int = 1000) -> List['RawMessage']:
        messages = []
        for i in range(limit):
            if queue.is_empty():
                break
            (robot_id, timestamp, message) = queue.dequeue()
            if message:
                messages.append(cls.from_mavlink_message(robot_id, timestamp, message))
        return messages

def thread_db():
    get_logger().info('Starting database thread')
    IntervalThread(1, save_messages_from_queue)

def save_messages_from_queue():
    queue = get_messages_to_save_queue()
    messages = RawMessage.from_queue(queue, limit=len(queue))
    RawMessage.bulk_create(messages)
    get_logger().info(f'Saved {len(messages)} messages to database')

if __name__ == '__main__':
    get_connection().create_tables([Device, RawMessage])
    get_connection().close()
