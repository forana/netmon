import http.client
import logging
import os
import random
import sqlite3
import time
from urllib.parse import urlparse

DATABASE_FILE = os.getenv("DATABASE_FILE", "/tmp/netmon.sqlite")
CHECK_URL = os.getenv("CHECK_URL", "https://alexforan.com/hello.txt")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
CHECK_VARIANCE = int(os.getenv("CHECK_VARIANCE", "0"))
CHECK_TIMEOUT = int(os.getenv("CHECK_TIMEOUT", "30"))

logging.basicConfig(format="%(asctime)-15s - %(message)s")
logger = logging.getLogger("netmon")
logger.setLevel(logging.DEBUG if os.getenv("LOG_LEVEL") == "DEBUG" else logging.INFO)

logger.info("netmon starting")
logger.info(f"will check {CHECK_URL} every {CHECK_INTERVAL} seconds, +/- {CHECK_VARIANCE}")
logger.info(f"db = {DATABASE_FILE}")

conn = sqlite3.connect(DATABASE_FILE, timeout=10)
conn.execute("CREATE TABLE IF NOT EXISTS pings (success BOOLEAN, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)") 

def check(url: str, timeout: int) -> bool:
    parsed = urlparse(url)
    hostname = parsed.netloc.split(":", 1)[0]
    c = http.client.HTTPSConnection(hostname, timeout=CHECK_TIMEOUT)
    c.request("GET", parsed.path)
    try:
        c.getresponse()
        return True
    except ConnectionError as e:
        logger.exception(e)
        return False

while True:
    check_result = check(CHECK_URL, CHECK_TIMEOUT)
    logger.info(f"Success: {check_result}")
    result_value = 1 if check_result else 0
    conn.execute(f"INSERT INTO pings (success) VALUES ({result_value})")
    conn.commit()
    interval = CHECK_INTERVAL - CHECK_VARIANCE + (random.random() * 2*CHECK_VARIANCE)
    logger.debug(f"Sleeping {interval}s")
    time.sleep(interval)
