from .db_connector import get_connection
import pandas as pd


def load_articles():
    with get_connection() as conn:
        query = """
SELECT title,url,published_date,summary,full_text FROM articles"""
        df = pd.read_sql_query(query, conn)
        return df
