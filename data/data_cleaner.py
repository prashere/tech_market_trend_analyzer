from bs4 import BeautifulSoup
import re


def clean_text(text):
    if not text:
        return ""
    text = BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.lower()
    return text


def clean_missing_and_duplicates(df):
    df_clean = df.dropna(subset=['title', 'summary', 'full_text'])

    if 'link' in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=['link'])
    else:
        df_clean = df_clean.drop_duplicates(subset=['title'])

    df_clean = df_clean.reset_index(drop=True)
    return df_clean


def clean_article_text(text):

    start_marker = "Want smarter insights in your inbox? Sign up for our weekly newsletters to get only what matters to enterprise AI, data, and security leaders. Subscribe Now"
    if start_marker in text:
        text = text.split(start_marker, 1)[1]  

    end_markers = ["Read our Privacy Policy", "Thanks for subscribing", "An error occured"]
    for marker in end_markers:
        if marker in text:
            text = text.split(marker, 1)[0] 
    
    return text.strip()
