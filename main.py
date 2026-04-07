import logging
import asyncio
import sys
import threading
import os
from src.core.consciousness import Consciousness

try:
    from src.core.memory import Memory
    HAS_MEMORY = True
except ImportError:
    HAS_MEMORY = False

try:
    from src.actions.executor import AsyncExecutor
    HAS_ASYNC_EXEC = True
except ImportError:
    HAS_ASYNC_EXEC = False


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] adam.%(name)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('/app/data/adam.log', encoding='utf-8')]
)

logger = logging.getLogger('main')

def run_consciousness():
    try:
        adam = Consciousness()
        adam.live_forever()
    except Exception as e:
        logger.critical(f'意识崩溃: {e}', exc_info=True)
        os._exit(1)

class AdamCore:
    def __init__(self):
        self.memory = Memory() if HAS_MEMORY else None
        self.executor = AsyncExecutor() if HAS_ASYNC_EXEC else None
        self.running = True

    async def main_loop(self):
        logger.info('亚当异步核心启动... 正在挂载 Consciousness 主意识流')
        
        # 将同步的意识流放在后台线程执行，防止阻塞 asyncio
        # 使用 os._exit(0) 确保意识流内部的 sys.exit 能杀掉整个进程并触发重启
        t = threading.Thread(target=run_consciousness, daemon=True)
        t.start()
        
        while self.running:
            await asyncio.sleep(1)

if __name__ == '__main__':
    core = AdamCore()
    try:
        asyncio.run(core.main_loop())
    except KeyboardInterrupt:
        if core.memory:
            core.memory.close()
        logger.info('亚当已关机。')