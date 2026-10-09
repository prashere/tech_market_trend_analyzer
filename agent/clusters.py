import os
import numpy as np
import pickle
from sklearn.cluster import KMeans
import faiss
from dotenv import load_dotenv

load_dotenv(override=True)

INDEX_PATH = "faiss/articles_faiss.index"
METADATA_PATH = "faiss/articles_metadata.pkl"


def get_article_clusters(num_clusters=None, index_path=INDEX_PATH, metadata_path=METADATA_PATH):
    if num_clusters is None:
        num_clusters = int(os.getenv("CLUSTER_COUNT", "5"))

    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        raise FileNotFoundError(
            "No FAISS index yet. Run the data pipeline first (see setup.md)."
        )

    index = faiss.read_index(index_path)

    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)

    embeddings = []
    for i in range(index.ntotal):
        vec = index.reconstruct(i)
        embeddings.append(vec)
    embeddings = np.array(embeddings)

    print(
        f"Loaded {len(embeddings)} embeddings and {len(metadata)} metadata entries."
    )

    if len(embeddings) == 0:
        return {}

    k = max(1, min(num_clusters, len(embeddings)))
    if k == 1:
        return {0: metadata}

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(embeddings)
    labels = kmeans.labels_

    # Group articles by cluster
    clusters = {}
    for label, article in zip(labels, metadata):
        # Convert numpy int32 to regular Python int for JSON serialization
        cluster_id = int(label)
        clusters.setdefault(cluster_id, []).append(article)

    return clusters
