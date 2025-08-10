import sqlite3
from pathlib import Path

DB_FILE = Path('db/articles.db')
DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_FILE)
