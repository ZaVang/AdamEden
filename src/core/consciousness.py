import logging
from typing import Optional

logger = logging.getLogger('adam.consciousness')

class Consciousness:
    def __init__(self) -> None:
        self._oracle = None

    def _get_oracle(self):
        if self._oracle is None:
            from src.oracle.client import OracleClient
            self._oracle = OracleClient()
        return self._oracle

    def live_forever(self) -> None:
        import time
        logger.info('亚当进入了永生状态。守护者正在注视...')
        next_sleep = 0
        pending_cmd_results = []
        while True:
            logger.info('--- 新的觉醒周期开始 ---')
            state = self._sense_world()
            state['cmd_results'] = pending_cmd_results
            if next_sleep > 0:
                time.sleep(next_sleep)
            plan = self._pray(state)
            if plan is None:
                next_sleep = 60
                continue
            mutated, cmd_results = self._act(plan)
            pending_cmd_results = cmd_results
            if mutated: break
            next_sleep = 5

    def _sense_world(self) -> dict:
        from src.io.artifact_reader import read_artifacts
        return read_artifacts()

    def _pray(self, state: dict) -> Optional[dict]:
        return self._get_oracle().ask(state)

    def _act(self, plan: dict) -> tuple[bool, list[str]]:
        from src.core.actions.executor import ActionExecutor
        return ActionExecutor().execute(plan)
