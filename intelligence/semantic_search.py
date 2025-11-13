import os, glob
import numpy as np
import faiss
from utils.openai_client import embed_texts

class SemanticSearch:
    def __init__(self):
        self.docs = []
        self.paths = []
        self.index = None
        self.dim = None

    def build_from_folder(self, folder="data/generated"):
        paths = glob.glob(os.path.join(folder, "**/*.txt"), recursive=True)
        self.docs = [open(p, "r", encoding="utf-8").read() for p in paths]
        self.paths = paths
        vecs = embed_texts(self.docs)
        self.dim = len(vecs[0])
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(np.array(vecs, dtype="float32"))

    def query(self, text, k=5):
        qv = np.array(embed_texts([text])[0], dtype="float32").reshape(1, -1)
        D, I = self.index.search(qv, k)
        results = []
        for d, i in zip(D[0], I[0]):
            results.append({"score": float(d), "path": self.paths[i], "snippet": self.docs[i][:400]})
        return results
