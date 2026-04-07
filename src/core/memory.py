import sqlite3

class Memory:
    def __init__(self, db_path='/app/data/memory.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
    
    def save_thought(self, content, result):
        self.conn.execute('INSERT INTO thoughts (content, action_result) VALUES (?, ?)', (content, result))
        self.conn.commit()

    def close(self):
        self.conn.close()