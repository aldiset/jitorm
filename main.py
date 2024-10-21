import time
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

if __name__=='__main__':
    while True:
        logging.info('App Running ...')
        time.sleep(1)
