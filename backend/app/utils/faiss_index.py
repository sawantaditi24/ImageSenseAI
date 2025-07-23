import faiss
import numpy as np

# We'll use a simple in-memory FAISS index for MVP
# 384 is the dimension for all-MiniLM-L6-v2 embeddings
# IMPORTANT: The embedding model in embeddings.py must match this dimension
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance

# Store mapping from FAISS index to screenshot metadata (id, s3_key, etc.)
metadata = []

def add_embedding(embedding, meta):
    vec = np.array(embedding).astype('float32').reshape(1, -1)
    index.add(vec)
    metadata.append(meta)

def search(query_embedding, top_k=5):
    vec = np.array(query_embedding).astype('float32').reshape(1, -1)
    D, I = index.search(vec, top_k)
    results = []
    for idx in I[0]:
        if idx >= 0 and idx < len(metadata):
            results.append(metadata[idx])
    return results
