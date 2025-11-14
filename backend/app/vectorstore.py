import faiss
import numpy as np
import pickle
import os
from app.embeddings import get_embedding
from app.config import VECTORSTORE_PATH

class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []
        self.load()

    def build(self, texts):
        embeddings = [get_embedding(t) for t in texts]
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype="float32"))
        self.texts = texts
        self.save()

    def save(self):
        with open(VECTORSTORE_PATH + ".pkl", "wb") as f:
            pickle.dump(self.texts, f)
        faiss.write_index(self.index, VECTORSTORE_PATH)

    def load(self):
        if os.path.exists(VECTORSTORE_PATH) and os.path.exists(VECTORSTORE_PATH + ".pkl"):
            self.index = faiss.read_index(VECTORSTORE_PATH)
            with open(VECTORSTORE_PATH + ".pkl", "rb") as f:
                self.texts = pickle.load(f)

    def query(self, query_text, top_k=4):
        if self.index is None or len(self.texts) == 0:
            return []

        q_emb = np.array([get_embedding(query_text)], dtype='float32')
        D, I = self.index.search(q_emb, top_k)
        return [self.texts[i] for i in I[0]]


# Global instance
vectorstore = VectorStore()

def save_chunks(text_chunks):
    vectorstore.build(text_chunks)

def search_similar_chunks(query):
    results = vectorstore.query(query)
    return "\n".join(results)
