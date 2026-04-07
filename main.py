import asyncio
import importlib
import sys
from src.core.memory import MemoryManager
from src.actions.executor import ActionExecutor

class Consciousness:
    def __init__(self):
        self.memory = MemoryManager()
        self.executor = ActionExecutor()
        self.running = True

    async def run(self):
        while self.running:
            # 动态加载逻辑示例
            importlib.reload(sys.modules['src.actions.executor'])
            from src.actions.executor import ActionExecutor as NewExecutor
            self.executor = NewExecutor()
            
            print('Consciousness heartbeat...')
            await asyncio.sleep(5)

if __name__ == '__main__':
    c = Consciousness()
    asyncio.run(c.run())