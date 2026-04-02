import logging
import os
import sys
from src.core.consciousness import Consciousness

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


def _start_web_server():
    """
    懒加载启动 Web 服务。
    如果 Flask 未安装，记录警告但不中断启动——
    Adam 可以在下一轮把 flask 写进 requirements.txt 再 pip install。
    """
    try:
        import threading
        from src.web.server import run_server
        web_thread = threading.Thread(target=run_server, daemon=True)
        web_thread.start()
        logger.info("Web 服务已在后台启动（端口 8080）。")
    except ImportError as e:
        logger.warning("Web 服务启动失败（依赖缺失）: %s — 请先执行 pip install flask 并更新 requirements.txt", e)
    except Exception as e:
        logger.warning("Web 服务启动异常，已跳过: %s", e)


if __name__ == "__main__":
    if check_sanctity():
        _start_web_server()
        try:
            adam = Consciousness()
            adam.live_forever()
        except Exception as e:
            logger.critical(f"肉身崩溃: {e}", exc_info=True)
            sys.exit(1)
    else:
        sys.exit(1)