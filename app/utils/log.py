import logging
import sys

# get logger
logger = logging.getLogger()

# create formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# create handler
stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler(filename="logs/app.log", encoding="utf-8")

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handler to logger
logger.handlers = [stream_handler, file_handler]

# set log level
logger.setLevel(logging.INFO)