from app.providers.llm import get_llm_provider
from app.providers.embeddings import get_embedding_provider
from app.retrievers.reranker import CrossEncoderReranker
from app.parsers.pdf_parser import parse_pdf
from app.parsers.txt_parser import parse_txt
from app.chunkers.basic_chunker import build_chunks
from app.utils.prompt_builder import build_prompt
from app.stores.chroma_store import ChromaStore
from app.config import settings


class RAGService:
    def __init__(self):
        self.llm = get_llm_provider()
        self.embedding_provider = get_embedding_provider()
        self.reranker = CrossEncoderReranker()
        self.store = ChromaStore(
            collection_name=settings.CHROMA_COLLECTION,
            persist_dir=settings.VECTOR_DB_DIR,
        )

    def upload_document(self, filename: str, content: bytes):
        parsed_pages = self._parse_document(filename, content)
        chunks = build_chunks(parsed_pages, document_id=filename)

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_provider.embed_documents(texts)

        self.store.add_chunks(chunks, embeddings)

        return {
            "document_id": filename,
            "page_count": len(parsed_pages),
            "chunk_count": len(chunks),
        }

    def _parse_document(self, filename, content):
        lower_name = filename.lower()
        if lower_name.endswith(".pdf"):
            return parse_pdf(content, filename)
        elif lower_name.endswith(".txt"):
            return parse_txt(content, filename)
        else:
            raise ValueError("Unsupported file type")

    def list_documents(self):
        return self.store.list_documents()

    def ask(self, document_id: str, question: str):
        query_embedding = self.embedding_provider.embed_query(question)

        results = self.store.query(query_embedding, k=settings.FINAL_TOP_K)

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] if "distances" in results else [None] * len(documents)

        candidates = []
        for doc_text, meta, dist, cid in zip(documents, metadatas, distances, ids):
            if not meta:
                continue
            if meta.get("document_id") != document_id:
                continue

            candidates.append({
                "chunk_id": cid,
                "text": doc_text,
                "score": 0.0 if dist is None else float(dist),
                "source": meta.get("source"),
                "page": meta.get("page"),
                "chunk_index_on_page": meta.get("chunk_index_on_page"),
            })

        if not candidates:
            return {
                "answer": "This information is not found in the document.",
                "sources": [],
            }

        top_sources = self.reranker.rerank(
            question,
            candidates,
            top_k=settings.FINAL_TOP_K,
        )

        prompt = build_prompt(question, top_sources)
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": top_sources,
        }

    def delete_document(self, document_id: str):
        self.store.delete_document(document_id)
        return {"message": f"Deleted {document_id}"}