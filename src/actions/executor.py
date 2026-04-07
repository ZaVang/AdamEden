import asyncio

class ActionExecutor:
    async def execute(self, task):
        await asyncio.sleep(0.1)
        return f"Executed {task}"
