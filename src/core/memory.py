import sqlite3

class MemoryManager:
    def __init__(self, db_path='data/adam_memory.db'):
        self.db_path = db_path
    def save(self, thought, action, result):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT INTO memory (thought, action, result) VALUES (?, ?, ?)\, (thought, action, result))
        conn.commit()
        conn.close()