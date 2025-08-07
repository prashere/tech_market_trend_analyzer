import feedparser
import json
from datetime import datetime


from filters import *

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

        articles.append(article)
    return articles


def save_articles_json(articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {filename}")


if __name__ == "__main__":
    feed = fetch_rss_feed(TECHCRUNCH_RSS)
    articles = extract_articles(feed)
    articles = filter_articles_by_keywords(articles)
    articles = deduplicate_articles(articles)
    print(
        f"Filtered and deduplicated {len(articles)} articles from TechCrunch")
    save_articles_json(articles, 'raw/techcrunch_article.json')

    feed = fetch_rss_feed(DECODER_RSS)
    articles = extract_articles(feed)
    articles = filter_articles_by_keywords(articles)
    articles = deduplicate_articles(articles)
    print(f"Filtered and deduplicated {len(articles)} articles from Decoder")
    save_articles_json(articles, 'raw/decoder_article.json')

    feed = fetch_rss_feed(VENTURE_BEAT_RSS)
    articles = extract_articles(feed)
    articles = filter_articles_by_keywords(articles)
    articles = deduplicate_articles(articles)
    print(
        f"Filtered and deduplicated {len(articles)} articles from VentureBeat")
    save_articles_json(articles, 'raw/venturebeat_article.json')
