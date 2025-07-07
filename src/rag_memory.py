import faiss
import numpy as np

class RagMemory:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.store = []
        self.dim = dim

    def embed(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dim, dtype='float32')
        for i, c in enumerate(text.encode("utf-8")[:self.dim]):
            vec[i] = float(c)
        return vec

    def add(self, text: str):
        self.store.append(text)
        embedding = self.embed(text)
        self.index.add(np.array([embedding]))

    def search(self, query: str, k: int = 3):
        if not self.store:
            return []
        query_vec = self.embed(query)
        _, I = self.index.search(np.array([query_vec]), k)
        return [self.store[i] for i in I[0] if i < len(self.store)]
