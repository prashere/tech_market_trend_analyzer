import numpy as np
import faiss
import os
import pickle
from vector_store.create_embeddings import get_embedding


INDEX_PATH = "faiss/articles_faiss.index"
METADATA_PATH = "faiss/articles_metadata.pkl"

index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, 'rb') as f:
    metadata = pickle.load(f)


def query_faiss(query, top_k: int = 7):
    query_vector = np.array(get_embedding(query)).astype('float32')

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results
