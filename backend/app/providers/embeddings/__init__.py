from app.config import settings
from app.providers.embeddings.sentence_transformer_provider import SentenceTransformerProvider

def get_embedding_provider():
    if settings.EMBEDDING_MODEL == "all-MiniLM-L6-v2":
        return SentenceTransformerProvider()

    raise ValueError(f"Unsupported embedding provider: {settings.EMBEDDING_MODEL}")