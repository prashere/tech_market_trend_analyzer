from data.db_setup import setup_database
from data.rss_ingest import *
from db.loader_to_df_from_db import load_articles
from data.data_cleaner import clean_text, clean_missing_and_duplicates,clean_article_text

setup_database()
load_data()

articles_df = load_articles()

articles_df['title'] = articles_df['title'].apply(clean_text)
articles_df['summary'] = articles_df['summary'].apply(clean_text)
articles_df['full_text'] = articles_df['full_text'].apply(clean_article_text)
articles_df['full_text'] = articles_df['full_text'].apply(clean_text)


articles_df = clean_missing_and_duplicates(articles_df)

articles_df.to_csv('articles_cleaned.csv', index=False)
print(articles_df['full_text'].tail())
