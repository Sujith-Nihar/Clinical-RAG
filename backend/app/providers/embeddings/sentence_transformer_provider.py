import numpy as np
from sentence_transformers import SentenceTransformer
from app.providers.embeddings.base import EmbeddingProvider
from app.config import settings

class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model_name: str | None = None):
        self.model = SentenceTransformer(model_name or settings.EMBEDDING_MODEL)

    def embed_documents(self, texts: list[str]):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return (embeddings / norms).astype("float32")

    def embed_query(self, text: str):
        embedding = self.model.encode([text], convert_to_numpy=True)
        norms = np.linalg.norm(embedding, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return (embedding / norms).astype("float32")