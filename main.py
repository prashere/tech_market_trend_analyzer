import os
import pickle
import numpy as np
import faiss
from data.db_setup import setup_database
from data.rss_ingest import *
from db.loader_to_df_from_db import load_articles
from data.data_cleaner import clean_text, clean_missing_and_duplicates, clean_article_text
from vector_store.create_embeddings import get_embedding


def dash():
    print('----------------------------------------------')
    print()


setup_database()
load_data()

articles_df = load_articles()

articles_df['title'] = articles_df['title'].apply(clean_text)
articles_df['summary'] = articles_df['summary'].apply(clean_text)
articles_df['full_text'] = articles_df['full_text'].apply(clean_article_text)
articles_df['full_text'] = articles_df['full_text'].apply(clean_text)


articles_df = clean_missing_and_duplicates(articles_df)

articles_df.to_csv('articles_cleaned.csv', index=False)

print('Data stored and exported to csv')
dash()

embeddings = []
metadata = []

for _, row in articles_df.iterrows():
    if row['full_text']:
        embedding = get_embedding(row['full_text'])
        embeddings.append(embedding)
        metadata.append({
            'title': row['title'],
            'url': row['url'],
            'published_date': row['published_date'],
            'summary': row['summary']
        })

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

os.makedirs("faiss", exist_ok=True)
INDEX_PATH = "faiss/articles_faiss.index"
METADATA_PATH = "faiss/articles_metadata.pkl"

faiss.write_index(index, INDEX_PATH)
with open(METADATA_PATH, 'wb') as f:
    pickle.dump(metadata, f)

print(f"Stored {len(embeddings)} article embeddings in FAISS.")
dash()
