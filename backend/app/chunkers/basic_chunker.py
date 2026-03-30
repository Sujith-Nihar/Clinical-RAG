import re
from typing import List, Dict

def split_into_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

def chunk_paragraphs(paragraphs: List[str], chunk_size: int = 900, overlap: int = 150):
    chunks = []
    current = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)

        if current and current_len + para_len > chunk_size:
            chunk = "\n\n".join(current)
            chunks.append(chunk)

            overlap_text = chunk[-overlap:]
            current = [overlap_text, para]
            current_len = len(overlap_text) + para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks

def build_chunks(parsed_pages: List[Dict], document_id: str = None) -> List[Dict]:
    all_chunks = []
    chunk_id = 0

    for page_obj in parsed_pages:
        paragraphs = split_into_paragraphs(page_obj["text"])
        page_chunks = chunk_paragraphs(paragraphs)

        for idx, chunk in enumerate(page_chunks):
            all_chunks.append({
                "chunk_id": chunk_id,
                "document_id": document_id or page_obj["source"],
                "source": page_obj["source"],
                "page": page_obj["page"],
                "chunk_index_on_page": idx,
                "text": chunk,
            })
            chunk_id += 1

    return all_chunks