import sqlite3
from pathlib import Path
from db.db_connector import get_connection



def store_articles_to_db(articles):
    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0
    skipped_count = 0

    for article in articles:
        try:
            cursor.execute("""
                            INSERT OR IGNORE INTO articles(title,url,published_date,summary,full_text)
                            VALUES(?,?,?,?,?)
                            """, (
                article.get('title'),
                article.get('link'),
                article.get('published'),
                article.get('summary'),
                article.get('full_text', '')
            ))

            if cursor.rowcount == 1:
                inserted_count += 1
            else:

                skipped_count += 1
        except sqlite3.Error as e:
            print(f"Error inserting article {article.get('title')}: {e}")
            continue

    conn.commit()
    conn.close()

    print(f"Inserted {inserted_count} articles into the database.")
    print(f"Skipped {skipped_count} articles (already exists or error).")
