import time
from threading import Thread

from api.app import app
from bot_status import thread_bot_status
from config import API_LISTEN_IP, API_LISTEN_PORT
from db import thread_db
from tele_receiver import thread_tele_receiver

if __name__ == '__main__':
    tele_receiver_thread = Thread(target=thread_tele_receiver, daemon=True)
    db_thread = Thread(target=thread_db, daemon=True)
    bot_status_thread = Thread(target=thread_bot_status, daemon=True)

    tele_receiver_thread.start()
    db_thread.start()
    bot_status_thread.start()

    app.run(host=API_LISTEN_IP, port=API_LISTEN_PORT)

