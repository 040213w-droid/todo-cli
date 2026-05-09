import sqlite3
import os #获取当前目录

# db.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "text.db")

#当你只需要执行一条简单的SQL不关心返回结果集（或者一次性拿完所有行）时，直接用 conn.execute() 就行
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #查询结果会变成类似字典的东西
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos(
                id INTEGER PRIMARY KEY,
                title TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

