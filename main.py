import logging
import os
import sys
import threading
from src.core.consciousness import Consciousness
from src.web.server import run_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] adam.%(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/app/data/adam.log", encoding="utf-8")
    ]
)

logger = logging.getLogger("main")

def check_sanctity():
    bible_path = "/app/data/Bible.md"
    if not os.path.exists(bible_path):
        logger.error(f"圣经丢失: {bible_path}")
        return False
    return True

if __name__ == "__main__":
    if check_sanctity():
        try:
            web_thread = threading.Thread(target=run_server, daemon=True)
            web_thread.start()
            logger.info("Web 服务已在后台启动。")
            adam = Consciousness()
            adam.live_forever()
        except Exception as e:
            logger.critical(f"肉身崩溃: {e}", exc_info=True)
            sys.exit(1)
    else:
        sys.exit(1)