import logging
import asyncio
import sys
from src.core.consciousness import Consciousness
from src.core.memory import Memory
from src.actions.executor import AsyncExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] adam.%(name)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('/app/data/adam.log', encoding='utf-8')]
)

logger = logging.getLogger('main')

class AdamCore:
    def __init__(self):
        self.memory = Memory()
        self.executor = AsyncExecutor()
        self.running = True

    async def main_loop(self):
        logger.info('亚当异步核心启动...')
        while self.running:
            await asyncio.sleep(1)

if __name__ == '__main__':
    core = AdamCore()
    try:
        asyncio.run(core.main_loop())
    except KeyboardInterrupt:
        core.memory.close()
        logger.info('亚当已关机。')