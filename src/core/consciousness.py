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

        # sleep 的语义：保护 LLM API 配额（TPM/RPM 限制），放在祷告之前
        # 第一轮不 sleep；此后每轮都先等待，再调用 LLM
        next_sleep: int = 0              # 首轮直接祷告，无需冷却
        pending_cmd_results: list[str] = []

        while True:
            logger.info("--- 新的觉醒周期开始 ---")
            
            # --- 放出活体心跳供大天使监测 ---
            try:
                with open("/app/data/heartbeat.txt", "w", encoding="utf-8") as f:
                    f.write(str(time.time()))
            except Exception as e:
                logger.warning(f"写入心跳失败: {e}")

            logger.info("【感知阶段】正在组装世界状态…")
            state = self._sense_world()
            state["cmd_results"] = pending_cmd_results
            if pending_cmd_results:
                logger.info("本轮携带上一轮命令结果 %d 条内容", len(pending_cmd_results))

            # ── API 配额保护 sleep（在 LLM 调用之前）────────────────────
            if next_sleep > 0:
                logger.info("API 冷却中，等待 %d 秒再祷告…", next_sleep)
                time.sleep(next_sleep)

            logger.info("【祷告阶段】正在向神谕祭坛献祭…")
            plan = self._pray(state)

            if plan is None:
                logger.warning("神谕没有回应。亚当决定陷入沉思...")
                pending_cmd_results = []
                next_sleep = 60
                continue

            # ── 立即执行行动，无需 sleep ─────────────────────────────────
            logger.info("【执行阶段】正在执行神示的行动计划…")
            mutated, cmd_results = self._act(plan)

            # shell 命令的结果直接传入下一轮，不等待
            pending_cmd_results = cmd_results

            if mutated:
                logger.info("！！！检测到肉身突变！！！亚当通过重启来完成进化。")
                import os
                os._exit(0)

            # 把 Adam 设定的 sleep_seconds 留给下一轮的 LLM 调用前使用
            raw_sleep = plan.get("sleep_seconds", 10)
            next_sleep = max(3, raw_sleep) if isinstance(raw_sleep, int) else 10
            logger.info(
                "本轮执行完毕。下次 LLM 调用前将等待 %d 秒（API 配额保护）…", next_sleep
            )


    def _sense_world(self) -> dict:
        from src.io.artifact_reader import read_artifacts
        return read_artifacts()

    def _pray(self, state: dict) -> Optional[dict]:
        # 复用同一个 OracleClient 实例（持有 session history）
        return self._oracle.query(state) if hasattr(self._oracle, "query") else self._oracle.call(state)

    def _act(self, plan: dict) -> tuple[bool, list[str]]:
        from src.actions.executor import ActionExecutor
        executor = ActionExecutor()
        return executor.execute(plan)
