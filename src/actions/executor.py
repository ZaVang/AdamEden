import asyncio
import logging

logger = logging.getLogger("adam.actions.executor")

class AsyncExecutor:
    async def execute_command(self, cmd: str):
        logger.info(f"Executing: {cmd}")
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode() + stderr.decode()