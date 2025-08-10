from agent.clusters import get_article_clusters
from agent.build_prompt import *
from vector_store.create_embeddings import get_summary_from_openai
import pandas as pd


def generate_cluster_analysis(prompt):
    response = get_summary_from_openai(prompt)
    return response


articles_df = pd.read_csv('articles_cleaned.csv')
clusters = get_article_clusters()


for cluster_id, articles in clusters.items():
    print(
        f"\nGenerating analysis for Cluster {cluster_id} with {len(articles)} articles...")
    prompt = build_cluster_prompt(articles, articles_df)
    analysis = generate_cluster_analysis(prompt)
    print(f"\nCluster {cluster_id} Analysis:\n{analysis}\n")
    # break

# print('DONE')