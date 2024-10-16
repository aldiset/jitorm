import time
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main execution
if __name__ == '__main__':
    while True:
        logging.info("running...")
        time.sleep(10)  # Sleep for 10 seconds to reduce CPU usage
