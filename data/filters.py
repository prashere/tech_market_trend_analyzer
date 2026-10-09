from dateutil import parser as date_parser
import pytz

KEYWORDS = [
    # Core AI Terms
    "AI", "Artificial Intelligence", "Machine Learning", "ML", "Deep Learning", "Neural Networks",
    "Generative AI", "GenAI", "LLM", "Large Language Model", "Transformer", "Multi-modal AI",

    # Subfields & Concepts
    "NLP", "Natural Language Processing", "Computer Vision", "Reinforcement Learning",
    "Agentic AI", "Autonomous Agents", "AI Safety", "AI Alignment",

    # Notable Tools & Models
    "ChatGPT", "GPT-4", "GPT-4o", "DALL·E", "Whisper", "Claude", "Claude 3", "Sora", "Gemini", "Gemini 1.5", "PaLM", "LLaMA", "Mistral", "Mixtral",

    # Company Names
    "OpenAI", "Google", "Google DeepMind", "Alphabet", "Microsoft", "Meta", "Facebook", "Anthropic", "Amazon", "xAI", "Tesla AI", "Apple AI", "NVIDIA",

    # Startup & Funding Terms
    "Startup", "Tech Startup", "AI Startup", "Unicorn", "Seed Funding", "Series A", "Series B", "Venture Capital", "VC", "Investment", "Investor", "Acquisition", "Tech IPO",

    # Industry Buzzwords & Trends
    "Responsible AI", "AI Regulation", "AI Policy", "Open Source AI", "AI Ethics", "Model Fine-Tuning", "LoRA", "Prompt Engineering", "RAG", "Retrieval-Augmented Generation",

    # Hype & Industry Movement
    "AI Trends", "Tech Trends", "AI Breakthrough", "AI Research", "AI Innovation", "Product Launch", "AI Conference"
]


def filter_articles_by_keywords(articles, keywords=KEYWORDS):
    filtered = []
    for article in articles:
        content = (article.get("title", "") + article.get("summary", "")).lower()
        if any(keyword.lower() in content for keyword in keywords):
            filtered.append(article)
    return filtered


def deduplicate_articles(articles):
    seen = set()
    unique_articles = []
    for article in articles:

        if article['link'] not in seen:
            unique_articles.append(article)
            seen.add(article['link'])
    return unique_articles


def parse_and_format_date(published_str):
    try:
        date = date_parser.parse(published_str)

        if date.tzinfo is None:
            date = pytz.utc.localize(date)
        else:
            date = date.astimezone(pytz.utc)
        return date.isoformat()
    except Exception:
        print(f"Error parsing date: {published_str}")
        return None
