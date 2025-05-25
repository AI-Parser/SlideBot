import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

class SlideVectorIndex:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.slides = []
        self.embeddings = []

    def add_slides(self, slides):
        contents = [slide["content"] for slide in slides]
        self.embeddings = model.encode(contents)
        self.index.add(np.array(self.embeddings).astype("float32"))
        self.slides = slides

    def query(self, question, top_k=3):
        q_embedding = model.encode([question]).astype("float32")
        _, indices = self.index.search(q_embedding, top_k)
        return [self.slides[i] for i in indices[0]]
