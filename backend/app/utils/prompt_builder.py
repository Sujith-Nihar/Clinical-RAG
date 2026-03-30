CLINICAL_PROMPT = """
You are a clinical AI assistant analyzing medical documents.

Rules:
- Answer ONLY from the provided context
- Do NOT use outside knowledge
- If not found, say exactly: "This information is not found in the document."
- Be precise and factual
- Cite sources

Context:
{context}

Question:
{question}

Return:

Answer:
<answer>

Evidence:
- Source: <source>, Page: <page>, Chunk: <chunk_id>
"""

def build_context(sources):
    parts = []
    for s in sources:
        parts.append(
            f"[Source: {s['source']}, Page: {s['page']}, Chunk: {s['chunk_id']}]\n{s['text']}"
        )
    return "\n\n".join(parts)

def build_prompt(question, sources):
    return CLINICAL_PROMPT.format(
        context=build_context(sources),
        question=question
    )