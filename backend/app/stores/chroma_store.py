import chromadb
from chromadb.config import Settings as ChromaSettings


class ChromaStore:
    def __init__(self, collection_name: str = "rag_docs", persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: list[dict], embeddings):
        ids = [str(chunk["chunk_id"]) for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "document_id": chunk["document_id"],
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_index_on_page": chunk["chunk_index_on_page"],
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings.tolist(),
        )

    def query(self, query_embedding, k: int = 10):
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=k,
        )
        return results

    def list_documents(self):
        data = self.collection.get(include=["metadatas"])
        metadatas = data.get("metadatas", [])

        seen = {}
        for meta in metadatas:
            if not meta:
                continue
            doc_id = meta.get("document_id")
            if doc_id:
                seen[doc_id] = seen.get(doc_id, 0) + 1

        return [
            {
                "document_id": doc_id,
                "chunk_count": count,
            }
            for doc_id, count in seen.items()
        ]

    def delete_document(self, document_id: str):
        data = self.collection.get(include=["metadatas"])
        ids_to_delete = []

        for idx, meta in zip(data["ids"], data["metadatas"]):
            if meta and meta.get("document_id") == document_id:
                ids_to_delete.append(idx)

        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)