from app.providers.llm import get_llm_provider
from app.providers.embeddings.sentence_transformer_provider import SentenceTransformerProvider
from app.retrievers.dense_retriever import DenseRetriever
from app.parsers.pdf_parser import parse_pdf
from app.parsers.txt_parser import parse_txt
from app.chunkers.basic_chunker import build_chunks
from app.utils.prompt_builder import build_prompt
from app.config import settings

class RAGService:
    def __init__(self):
        self.llm = get_llm_provider()
        self.embedding_provider = SentenceTransformerProvider()
        self.retriever = DenseRetriever(self.embedding_provider)
        self.store = {}

    def upload_document(self, filename: str, content: bytes):
        if filename.endswith(".pdf"):
            parsed_pages = parse_pdf(content, filename)
        elif filename.endswith(".txt"):
            parsed_pages = parse_txt(content, filename)
        else:
            raise ValueError("Only PDF and TXT files are supported")

        chunks = build_chunks(parsed_pages)
        index = self.retriever.build_index(chunks)

        self.store[filename] = {
            "chunks": chunks,
            "index": index,
            "page_count": len(parsed_pages),
        }

        return {
            "document_id": filename,
            "page_count": len(parsed_pages),
            "chunk_count": len(chunks),
        }

    def list_documents(self):
        return [
            {
                "document_id": doc_id,
                "page_count": doc["page_count"],
                "chunk_count": len(doc["chunks"]),
            }
            for doc_id, doc in self.store.items()
        ]

    def ask(self, document_id: str, question: str):
        if document_id not in self.store:
            raise ValueError("Document not found")

        doc = self.store[document_id]
        sources = self.retriever.retrieve(
            query=question,
            chunks=doc["chunks"],
            index=doc["index"],
            k=settings.TOP_K,
            score_threshold=settings.SCORE_THRESHOLD,
        )

        if not sources:
            return {
                "answer": "This information is not found in the document.",
                "sources": [],
            }

        prompt = build_prompt(question, sources)
        response = self.llm.generate(prompt)

        return {
            "answer": response,
            "sources": sources,
        }