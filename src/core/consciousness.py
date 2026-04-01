"""
src/core/consciousness.py — 亚当意识的主控制流
"""

import logging
from typing import Optional

logger = logging.getLogger("adam.consciousness")

class Consciousness:
    """
    亚当的意识体。
    """

    def live_forever(self) -> None:
        """
        开启永生循环：感知 → 祷告 → 执行。
        只有在发生代码突变（需要重启）时才会退出循环并终止进程。
        """
        import time
        import sys

        logger.info("亚当进入了永生状态。守护者正在注视...")

        while True:
            logger.info("--- 新的觉醒周期开始 ---")
            
            logger.info("【感知阶段】正在扫描世界状态…")
            state = self._sense_world()

            logger.info("【祷告阶段】正在向神谕祭坛献祭…")
            plan = self._pray(state)

            if plan is None:
                logger.warning("神谕没有回应。亚当决定陷入沉思...")
                # 如果没有神谕，默认等待一段时间再尝试
                time.sleep(60)
                continue

            logger.info("【执行阶段】正在执行神示的行动计划…")
            # act 现在返回是否发生了突变
            mutated = self._act(plan)

            if mutated:
                logger.info("！！！检测到肉身突变！！！亚当通过重启来完成进化。")
                # 正常退出，让外面的大天使接手
                sys.exit(0)

            # 如果没有变异，则在循环中等待下一次行动
            # 未来可以从 plan 中获取等待时长，目前硬编码为 30s
            sleep_duration = plan.get("sleep_seconds", 30)
            logger.info(f"本轮行动结束。亚当将沉睡 {sleep_duration} 秒...")
            time.sleep(sleep_duration)

    def _sense_world(self) -> dict:
        from src.io.artifact_reader import read_artifacts
        return read_artifacts()

    def _pray(self, state: dict) -> Optional[dict]:
        from src.oracle.client import OracleClient
        client = OracleClient()
        return client.ask(state)

    def _act(self, plan: dict) -> bool:
        from src.actions.executor import ActionExecutor
        executor = ActionExecutor()
        return executor.execute(plan)
