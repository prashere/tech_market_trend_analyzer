import sqlite3
from pathlib import Path

db_path = Path("db/articles.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM articles") 
conn.commit()

conn.close()

print("All records deleted successfully.")
