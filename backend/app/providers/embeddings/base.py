from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]):
        pass

    @abstractmethod
    def embed_query(self, text: str):
        pass