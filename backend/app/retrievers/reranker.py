from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, candidates: list[dict], top_k: int = 5):
        pairs = [[query, c["text"]] for c in candidates]
        scores = self.model.predict(pairs)

        for i, score in enumerate(scores):
            candidates[i]["rerank_score"] = float(score)

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_k]