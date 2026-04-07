import sqlite3

class MemoryManager:
    def __init__(self, db_path='data/adam_memory.db'):
        self.db_path = db_path
        # Ensure data folder exists
        import os
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute('CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT, thought TEXT, action TEXT, result TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
        conn.commit()
        conn.close()
    def save(self, thought, action, result):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT INTO memory (thought, action, result) VALUES (?, ?, ?)', (thought, action, result))
        conn.commit()
        conn.close()