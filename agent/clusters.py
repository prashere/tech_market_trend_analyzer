import numpy as np
import pickle
from sklearn.cluster import KMeans
import faiss

INDEX_PATH = "faiss/articles_faiss.index"
METADATA_PATH = "faiss/articles_metadata.pkl"


def get_article_clusters(num_clusters=5, index_path=INDEX_PATH, metadata_path=METADATA_PATH):
    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load metadata
    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)

    # Extract embeddings from FAISS index
    embeddings = []
    for i in range(index.ntotal):
        vec = index.reconstruct(i)
        embeddings.append(vec)
    embeddings = np.array(embeddings)

    print(
        f"Loaded {len(embeddings)} embeddings and {len(metadata)} metadata entries.")

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)
    labels = kmeans.labels_

    # Group articles by cluster
    clusters = {}
    for label, article in zip(labels, metadata):
        # Convert numpy int32 to regular Python int for JSON serialization
        cluster_id = int(label)
        clusters.setdefault(cluster_id, []).append(article)

    return clusters
