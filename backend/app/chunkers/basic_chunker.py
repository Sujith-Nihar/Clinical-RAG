def chunk_text(text: str, chunk_size: int = 180, overlap: int = 40) -> list[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        start += max(chunk_size - overlap, 1)

    return chunks


def build_chunks(parsed_pages: list[dict]) -> list[dict]:
    all_chunks = []
    chunk_id = 0

    for page_obj in parsed_pages:
        page_chunks = chunk_text(page_obj["text"])

        for local_idx, chunk in enumerate(page_chunks):
            all_chunks.append({
                "chunk_id": chunk_id,
                "source": page_obj["source"],
                "page": page_obj["page"],
                "chunk_index_on_page": local_idx,
                "text": chunk,
            })
            chunk_id += 1

    return all_chunks