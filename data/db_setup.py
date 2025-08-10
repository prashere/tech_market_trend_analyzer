import sqlite3

from pathlib import Path

DB_FILE = Path('db/articles.db')
DB_FILE.parent.mkdir(parents=True, exist_ok=True)


CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT UNIQUE,
    published_date TEXT,
    summary TEXT,
    full_text TEXT
);
"""


def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()
    print(f"Database setup complete. Articles will be stored in {DB_FILE}")
