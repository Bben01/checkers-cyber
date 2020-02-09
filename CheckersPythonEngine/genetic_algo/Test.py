import logging
import time


logging.basicConfig(filename=r"../Log/Test", level=logging.INFO)
time = time.strftime('%Y-%m-%d %H:%M:%S')
logging.info(f"{time}    Test")
