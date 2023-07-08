import logging
import os

LOG_FILE = 'logfile.log'
LOGS_PATH = os.path.join(os.getcwd(), 'logs', LOG_FILE)

os.makedirs(LOGS_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
