import faiss
import numpy as np
import os
import pickle

class MemoryStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []  # To store original prompts/responses

    def embed(self, text):
         
        vec = np.zeros(self.dim, dtype='float32')
        for i, c in enumerate(text.encode('utf-8')[:self.dim]):
            vec[i] = float(c)
        return vec

    def add(self, text):
        vec = self.embed(text)
        self.index.add(np.array([vec]))
        self.texts.append(text)

    def search(self, query, top_k=3):
        vec = self.embed(query)
        D, I = self.index.search(np.array([vec]), top_k)
        results = [self.texts[i] for i in I[0] if i < len(self.texts)]
        return results
