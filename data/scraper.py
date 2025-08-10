from bs4 import BeautifulSoup
import requests
from newspaper import Article
from datetime import datetime


def extract_full_text(url: str):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            'full_text': article.text.strip()
        }
    except Exception as e:
        print(f"Error extracting article text: {e}")
        return None



# Scraping using BeautifulSoup
def extract_full_text_custom(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        article_body = soup.find('div', class_='article-content')

        if not article_body:
            print(f'No article body found for {url}')
            return None

        paragraphs = article_body.find_all('p')
        full_text = '\n'.join([p.get_text()
                              for p in paragraphs if p.get_text().strip()])

        return {
            'full_text': full_text.strip()
        }
    except requests.RequestException as e:
        print(f"Error fetching article {url}: {e}")
        return None
