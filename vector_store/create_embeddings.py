import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

_api_key = os.getenv("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=_api_key or None)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")


def get_embedding(text):
    if not _api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to .env — see setup.md.")
    response = client.embeddings.create(
        input=text[:8000],
        model=EMBEDDING_MODEL,
    )
    return response.data[0].embedding


def get_summary_from_openai(prompt):
    if not _api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to .env — see setup.md.")
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful tech market analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
