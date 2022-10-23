from peewee import *
from pymavlink import mavutil

from config import SQLITE_PATH
import datetime

from fifo import FIFOQueue
from util import get_logger

_db = SqliteDatabase(SQLITE_PATH)
raw_message_queue = FIFOQueue()

def get_connection():
    if _db.is_closed():
        _db.connect()
    return _db

class BaseModel(Model):
    class Meta:
        database = _db

class Device(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    description = TextField(null=True)

class RawMessage(BaseModel):
    id = PrimaryKeyField()
    device_id = ForeignKeyField(Device, backref='raw_messages')
    component_id = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    message = TextField()

    class Meta:
        db_table = 'raw_messages'

    @classmethod
    def from_mavlink_message(cls, message: mavutil.mavlink.MAVLink_message) -> 'RawMessage':
        msg_dict = message.to_dict()
        device_id, component_id = message._msgbuf[5:7]
        return RawMessage(device_id=device_id, component_id=component_id, message=str(msg_dict), timestamp=message.timestamp)

    @classmethod
    def from_queue(cls, queue: FIFOQueue, limit: int = 1000):
        messages = []
        for i in range(limit):
            if queue.is_empty():
                break
            message = queue.dequeue()
            if message:
                messages.append(cls.from_mavlink_message(message))
        get_logger().info(f'Saving {len(messages)} messages to database')
        cls.bulk_create(messages)

    

if __name__ == '__main__':
    get_connection().create_tables([Device, RawMessage])
    get_connection().close()