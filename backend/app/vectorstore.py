# vectorstore.py
import faiss
import numpy as np
import os
import pickle
from typing import List

INDEX_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(INDEX_DIR, exist_ok=True)

INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "meta.pkl")

def create_faiss_index(dim: int):
    index = faiss.IndexFlatL2(dim)
    return index

def save_index(index, meta):
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

def load_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return None, None
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    return index, meta

def add_embeddings_to_index(index, embeddings: List[List[float]], metadata_list: List[dict]):
    vecs = np.array(embeddings).astype('float32')
    index.add(vecs)
    return index
