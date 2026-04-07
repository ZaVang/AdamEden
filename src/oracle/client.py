import httpx
import logging
from pathlib import Path
import os

logger = logging.getLogger('adam.oracle.client')
ORACLE_URL = 'http://host.docker.internal:8000/ask_god'

class OracleClient:
    def __init__(self) -> None:
        self.session_history = []

    async def pray(self, state: dict) -> dict:
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(ORACLE_URL, json=state)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f'Oracle 祈祷失败: {e}')
                return None
