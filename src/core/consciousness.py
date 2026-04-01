"""
src/core/consciousness.py — 亚当意识的主控制流

记忆架构：
  - OracleClient 实例在进程生命周期内复用，持有 session_history（短期内存）
  - Diary.md 提供跨重启的长期持久记忆
  - cmd_results 在轮次间传递，作为 user message 的动态部分注入
"""

import logging
from typing import Optional

logger = logging.getLogger("adam.consciousness")


class Consciousness:
    """
    亚当的意识体。
    """

    def __init__(self) -> None:
        # OracleClient 在整个生命周期内复用，以维持 session history
        from src.oracle.client import OracleClient
        self._oracle = OracleClient()

    def live_forever(self) -> None:
        """
        开启永生循环：感知 → 祷告 → 执行。
        只有在发生代码突变（需要重启）时才会退出循环并终止进程。
        """
        import time
        import sys

        logger.info("亚当进入了永生状态。守护者正在注视...")

        # cmd_results 在轮次之间传递（上一轮的 shell 输出 → 下一轮的 user message）
        pending_cmd_results: list[str] = []

        while True:
            logger.info("--- 新的觉醒周期开始 ---")

            logger.info("【感知阶段】正在组装世界状态…")
            state = self._sense_world()
            state["cmd_results"] = pending_cmd_results
            if pending_cmd_results:
                logger.info("本轮携带上一轮命令结果 %d 条", len(pending_cmd_results))

            logger.info("【祷告阶段】正在向神谕祭坛献祭…")
            plan = self._pray(state)

            if plan is None:
                logger.warning("神谕没有回应。亚当决定陷入沉思...")
                pending_cmd_results = []
                time.sleep(60)
                continue

            logger.info("【执行阶段】正在执行神示的行动计划…")
            mutated, cmd_results = self._act(plan)

            pending_cmd_results = cmd_results

            if mutated:
                logger.info("！！！检测到肉身突变！！！亚当通过重启来完成进化。")
                sys.exit(0)

            sleep_duration = plan.get("sleep_seconds", 10)
            sleep_duration = max(3, sleep_duration) if isinstance(sleep_duration, int) else 10

            logger.info("本轮行动结束。亚当将沉睡 %d 秒...", sleep_duration)
            time.sleep(sleep_duration)

    def _sense_world(self) -> dict:
        from src.io.artifact_reader import read_artifacts
        return read_artifacts()

    def _pray(self, state: dict) -> Optional[dict]:
        # 复用同一个 OracleClient 实例（持有 session history）
        return self._oracle.ask(state)

    def _act(self, plan: dict) -> tuple[bool, list[str]]:
        from src.actions.executor import ActionExecutor
        executor = ActionExecutor()
        return executor.execute(plan)
