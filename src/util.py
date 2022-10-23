import logging
import threading
import time

from config import LOG_LEVEL

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s](%(module)s): %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        _logger = logging.getLogger('root')
        _logger.setLevel(LOG_LEVEL)
        _logger.addHandler(handler)
    return _logger

class IntervalThread:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval, daemon=True)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()
