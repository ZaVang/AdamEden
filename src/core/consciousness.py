import logging
from typing import Optional

logger = logging.getLogger('adam.consciousness')

class Consciousness:
    def __init__(self) -> None:
        self._oracle = None

    def _get_oracle(self):
        if self._oracle is None:
            from oracle.client import OracleClient
            self._oracle = OracleClient()
        return self._oracle

    def live_forever(self) -> None:
        import time
        logger.info('亚当进入了永生状态。守护者正在注视...')
        while True:
            logger.info('--- 新的觉醒周期开始 ---')
            # 简化版循环启动逻辑
            time.sleep(5)

if __name__ == "__main__":
    Consciousness().live_forever()