from agent.clusters import get_article_clusters
from agent.build_prompt import *
from vector_store.create_embeddings import get_summary_from_openai
import pandas as pd
import glob
import os
import json
import re
import numpy as np


def numpy_json_encoder(obj):
    """Custom JSON encoder for handling numpy data types"""
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def get_latest_csv_file():
    csv_files = glob.glob('articles_cleaned_*.csv')

    if not csv_files:
        # Fallback to old filename if no timestamped files exist
        if os.path.exists('articles_cleaned.csv'):
            return 'articles_cleaned.csv'
        else:
            print("ERROR: No articles CSV file found!")
            return None

    csv_files.sort(key=os.path.getmtime, reverse=True)

    latest_file = csv_files[0]
    print(f"Using latest CSV file: {latest_file}")
    return latest_file


def generate_cluster_analysis(prompt):
    """Generate cluster analysis using OpenAI"""
    response = get_summary_from_openai(prompt)
    return response


def parse_analysis_json(analysis_text):
    try:
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            print("No JSON found in analysis response")
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse analysis JSON: {e}")
        print(f"Raw response: {analysis_text[:200]}...")
        return None


def get_article_info_for_cluster(articles):
    article_info = []
    for article in articles:
        article_info.append({
            'title': article.get('title', 'Unknown Title'),
            'url': article.get('url', '#'),
            'published_date': article.get('published_date', 'Unknown Date'),
            'summary': article.get('summary', '')[:200] + '...' if len(article.get('summary', '')) > 200 else article.get('summary', '')
        })
    return article_info


def process_all_clusters():
    latest_csv = get_latest_csv_file()
    if not latest_csv:
        print("ERROR: Cannot proceed without articles data file.")
        return []

    articles_df = pd.read_csv(latest_csv)
    clusters = get_article_clusters()

    processed_clusters = []

    for cluster_id, articles in clusters.items():
        print(
            f"\nGenerating analysis for Cluster {cluster_id} with {len(articles)} articles...")

        # Generate analysis
        prompt = build_cluster_prompt(articles, articles_df)
        analysis_text = generate_cluster_analysis(prompt)

        # Parse the JSON analysis
        parsed_analysis = parse_analysis_json(analysis_text)

        # Get article information
        article_info = get_article_info_for_cluster(articles)

        # Organize cluster data
        cluster_data = {
            'cluster_id': int(cluster_id),  # Ensure cluster_id is a Python int
            'article_count': len(articles),
            'articles': article_info,
            'analysis': parsed_analysis if parsed_analysis else {
                'title': f'Cluster {cluster_id} Analysis',
                'key_developments': ['Analysis parsing failed'],
                'emerging_trends': ['Analysis parsing failed'],
                'differences_in_viewpoints': ['Analysis parsing failed'],
                'strategic_moves': ['Analysis parsing failed']
            },
            'raw_analysis': analysis_text
        }

        processed_clusters.append(cluster_data)

    return processed_clusters


def save_cluster_data_to_json(cluster_data, filename='cluster_analysis.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cluster_data, f, indent=2, ensure_ascii=False,
                      default=numpy_json_encoder)
        print(f"\nCluster analysis saved to {filename}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to save cluster data: {e}")
        return False


def get_cluster_analysis_for_frontend():
    cluster_data = process_all_clusters()

    if not cluster_data:
        return {
            'success': False,
            'message': 'No cluster data available',
            'clusters': []
        }

    save_cluster_data_to_json(cluster_data)

    return {
        'success': True,
        'message': f'Successfully processed {len(cluster_data)} clusters',
        'total_clusters': len(cluster_data),
        'clusters': cluster_data,
        'generated_at': pd.Timestamp.now().isoformat()
    }
