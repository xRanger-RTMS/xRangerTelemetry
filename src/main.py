import time
from threading import Thread

from db import thread_db
from tele_receiver import thread_tele_receiver

if __name__ == '__main__':
    tele_receiver_thread = Thread(target=thread_tele_receiver, daemon=True)
    db_thread = Thread(target=thread_db, daemon=True)

    tele_receiver_thread.start()
    db_thread.start()

    while True:
        pass
