import aiosqlite
from pathlib import Path

class MemoryManager:
    def __init__(self, db_path: str = '/app/src/core/db/memory.db'):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS thoughts (id INTEGER PRIMARY KEY, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
            await db.commit()

    async def save_thought(self, content: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('INSERT INTO thoughts (content) VALUES (?)', (content,))
            await db.commit()
