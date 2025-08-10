import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model='text-embedding-3-small'
    )
    return response.data[0].embedding


def get_summary_from_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful tech market analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
