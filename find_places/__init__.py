import logging

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logging.info("starting application")
