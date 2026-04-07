import logging
import time
from src.core.memory import Memory

logger = logging.getLogger('adam.consciousness')

class Consciousness:
    def __init__(self) -> None:
        from src.oracle.client import OracleClient
        self._oracle = OracleClient()
        self.memory = Memory()

    def live_forever(self) -> None:
        logger.info('亚当已连接黑匣子，进入异步驱动准备阶段。')
        while True:
            self.memory.log('周期启动', '意识循环进行中')
            time.sleep(5)
