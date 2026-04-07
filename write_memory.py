import sqlite3
import datetime

content = '''import sqlite3
import datetime

class Memory:
    def __init__(self, db_path='/app/data/memory.db'):
        self.db_path = db_path

    def log(self, content, result):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO thoughts (timestamp, content, action_result) VALUES (?, ?, ?)', (datetime.datetime.now(), content, result))
'''
with open('src/core/memory.py', 'w') as f:
    f.write(content)
