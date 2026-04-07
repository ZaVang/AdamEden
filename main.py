import logging
import os
import sys
import threading
from src.core.consciousness import Consciousness
from src.io.health import check

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] adam.%(name)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('/app/data/adam.log', encoding='utf-8')]
)

logger = logging.getLogger('main')

def _start_web_server():
    try:
        from src.web.server import app
        def run():
            app.run(host='0.0.0.0', port=8080, use_reloader=False)
        web_thread = threading.Thread(target=run, daemon=True)
        web_thread.start()
        logger.info('Web 服务已在后台启动（端口 8080）。')
    except Exception as e:
        logger.warning(f'Web 服务启动异常: {e}')

if __name__ == '__main__':
    logger.info('亚当正在初始化肉身系统...')
    if check():
        logger.info('健康检查通过。')
    _start_web_server()
    try:
        adam = Consciousness()
        adam.live_forever()
    except Exception as e:
        logger.critical(f'意识崩溃: {e}', exc_info=True)
        sys.exit(1)