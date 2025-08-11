import os
import pickle
import numpy as np
import faiss
import schedule
import time
import threading
from datetime import datetime, timedelta
from data.db_setup import setup_database
from data.rss_ingest import load_data
from db.loader_to_df_from_db import load_articles
from data.data_cleaner import clean_text, clean_missing_and_duplicates, clean_article_text
from vector_store.create_embeddings import get_embedding


def dash():
    """Print dashboard separator for console output"""
    print('----------------------------------------------')
    print()


def process_article_data():
    print("Loading articles from database...")
    articles_df = load_articles()

    if articles_df.empty:
        print("No articles found in database.")
        return articles_df

    print(f"Processing {len(articles_df)} articles...")

    articles_df['title'] = articles_df['title'].apply(clean_text)
    articles_df['summary'] = articles_df['summary'].apply(clean_text)
    articles_df['full_text'] = articles_df['full_text'].apply(
        clean_article_text)
    articles_df['full_text'] = articles_df['full_text'].apply(clean_text)

    articles_df = clean_missing_and_duplicates(articles_df)

    print(
        f"Data cleaning completed. {len(articles_df)} articles ready for processing.")
    return articles_df


def create_embeddings_and_store(articles_df, update_mode=False):
    if articles_df.empty:
        print("No articles to process for embeddings.")
        return 0, False

    print("Generating embeddings...")

    embeddings = []
    metadata = []

    for _, row in articles_df.iterrows():
        if row['full_text']:
            try:
                embedding = get_embedding(row['full_text'])
                embeddings.append(embedding)
                metadata.append({
                    'title': row['title'],
                    'url': row['url'],
                    'published_date': row['published_date'],
                    'summary': row['summary']
                })
            except Exception as e:
                print(
                    f"ERROR: Error generating embedding for article: {row['title'][:50]}... - {e}")
                continue

    if not embeddings:
        print("WARNING: No embeddings generated.")
        return 0, False

    os.makedirs("faiss", exist_ok=True)
    INDEX_PATH = "faiss/articles_faiss.index"
    METADATA_PATH = "faiss/articles_metadata.pkl"

    if update_mode and os.path.exists(INDEX_PATH):
        # Load existing index and append new embeddings
        print("Updating existing FAISS index...")
        existing_index = faiss.read_index(INDEX_PATH)

        # Load existing metadata
        with open(METADATA_PATH, 'rb') as f:
            existing_metadata = pickle.load(f)

        # Add new embeddings to existing index
        existing_index.add(np.array(embeddings).astype('float32'))

        # Combine metadata
        combined_metadata = existing_metadata + metadata

        # Save updated index and metadata
        faiss.write_index(existing_index, INDEX_PATH)
        with open(METADATA_PATH, 'wb') as f:
            pickle.dump(combined_metadata, f)

        print(
            f"Updated FAISS index with {len(embeddings)} new embeddings. Total: {existing_index.ntotal}")
    else:
        # Create new index
        print("Creating new FAISS index...")
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))

        # Save new index and metadata
        faiss.write_index(index, INDEX_PATH)
        with open(METADATA_PATH, 'wb') as f:
            pickle.dump(metadata, f)

        print(f"Created new FAISS index with {len(embeddings)} embeddings.")

    return len(embeddings), True


def full_data_pipeline(update_mode=False):
    try:
        start_time = datetime.now()
        print(
            f"Starting {'update' if update_mode else 'initial'} data pipeline at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        dash()

        print("Setting up database...")
        setup_database()

        print("Fetching latest data from RSS sources...")
        load_data()

        articles_df = process_article_data()

        if articles_df.empty:
            print("No new articles to process.")
            return True

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'articles_cleaned_{timestamp}.csv'
        articles_df.to_csv(csv_filename, index=False)
        print(f"Data exported to {csv_filename}")

        num_embeddings, success = create_embeddings_and_store(
            articles_df, update_mode)

        end_time = datetime.now()
        duration = end_time - start_time

        if success:
            print(f"Pipeline completed successfully in {duration}")
            print(f"Processed {num_embeddings} articles")
            dash()
            return True
        else:
            print(f"Pipeline completed with errors in {duration}")
            dash()
            return False

    except Exception as e:
        print(f"ERROR: Pipeline failed with error: {e}")
        dash()
        return False


def update_data_pipeline():
    print("Scheduled update starting...")
    success = full_data_pipeline(update_mode=True)
    if success:
        print("Scheduled update completed successfully")
    else:
        print("Scheduled update failed")

    next_run = datetime.now() + timedelta(hours=24)
    print(
        f"Next update scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")


def start_scheduler():
    print("Setting up automatic updates every 24 hours...")

    schedule.every(24).hours.do(update_data_pipeline)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    next_run = datetime.now() + timedelta(hours=24)
    print(
        f"Automatic updates started. Next update: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main function to run the complete pipeline"""
    print("Tech Market Trend Analyzer - Data Pipeline")
    print("=" * 50)

    # Run initial pipeline
    success = full_data_pipeline(update_mode=False)

    if success:
        # Start automatic updates
        start_scheduler()
        print("System is now running with automatic updates every 24 hours.")
        print("You can keep this script running to maintain automatic updates.")
        print("Press Ctrl+C to stop the scheduler.")

        try:
            # Keep the main thread alive
            while True:
                time.sleep(3600)  # Sleep for 1 hour, then check again
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")
            print("Goodbye!")
    else:
        print("Initial pipeline failed. Please check the logs and try again.")


if __name__ == "__main__":
    main()
