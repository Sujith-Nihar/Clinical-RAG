import faiss

class DenseRetriever:
    def __init__(self, embedding_provider):
        self.embedding_provider = embedding_provider

    def build_index(self, chunks: list[dict]):
        texts = [c["text"] for c in chunks]
        embeddings = self.embedding_provider.embed_documents(texts)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        return index

    def retrieve(self, query: str, chunks: list[dict], index, k: int, score_threshold: float):
        q_emb = self.embedding_provider.embed_query(query)
        scores, indices = index.search(q_emb, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            if idx < len(chunks) and float(score) >= score_threshold:
                chunk = chunks[idx]
                results.append({
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "score": float(score),
                    "source": chunk["source"],
                    "page": chunk["page"],
                })

        return results