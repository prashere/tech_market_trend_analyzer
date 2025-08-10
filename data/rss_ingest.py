import feedparser
import json
from datetime import datetime


from .filters import *
from .store_articles_to_db import store_articles_to_db
from .scraper import extract_full_text, extract_full_text_custom

TECHCRUNCH_RSS = "https://techcrunch.com/feed/"
DECODER_RSS = 'https://the-decoder.com/feed/'
VENTURE_BEAT_RSS = 'https://venturebeat.com/category/ai/feed/'


def fetch_rss_feed(url):
    try:
        feed = feedparser.parse(url)
        return feed
    except Exception as e:
        print(f"Error fetching RSS feed from {url}: {e}")
        return None


def extract_articles(feed):
    articles = []
    for entry in feed.entries:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": parse_and_format_date(entry.published),
            "summary": entry.summary
        }
        # print('Date:', article["published"])
        articles.append(article)
    return articles


def save_articles_json(articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filename}")


def load_data():
    for source_name, rss_url in [
        ("TechCrunch", TECHCRUNCH_RSS),
        ("Decoder", DECODER_RSS),
        ("VentureBeat", VENTURE_BEAT_RSS)
    ]:
        print(f"Fetching from {source_name}....")
        feed = fetch_rss_feed(rss_url)
        articles = extract_articles(feed)
        articles = filter_articles_by_keywords(articles)
        articles = deduplicate_articles(articles)
        enriched_articles = []
        for article in articles:
            if source_name == 'VentureBeat':
                result = extract_full_text_custom(article["link"])
            else:
                result = extract_full_text(article["link"])
            if result and result.get("full_text"):
                article["full_text"] = result["full_text"]
                enriched_articles.append(article)
            else:
                print(
                    f"Skipping article due to missing full text: {article['link']}")
        store_articles_to_db(enriched_articles)
