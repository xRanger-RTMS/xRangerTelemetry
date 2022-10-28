import logging
import socket

from config import LOG_LEVEL, LOG_TO_FILE, LOG_FILE

_logger = None
def get_ip_address(hostname: str) -> str:
    return socket.gethostbyname(hostname)

def get_logger():
    global _logger
    if _logger is None:
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s](%(module)s): %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        _logger = logging.getLogger('root')
        _logger.setLevel(LOG_LEVEL)
        _logger.addHandler(handler)

        if LOG_TO_FILE:
            handler = logging.FileHandler(LOG_FILE)
            handler.setFormatter(formatter)

        _logger.debug('Logger initialized')
    return _logger