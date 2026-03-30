CLINICAL_PROMPT = """
You are a clinical AI assistant analyzing medical documents.

Instructions:
- Answer ONLY from the provided context.
- Do NOT use outside knowledge.
- If the answer is not clearly supported by the context, say:
  "This information is not found in the document."
- Be precise and clinically grounded.
- Do not invent diagnoses, treatments, contraindications, or dosages.
- Cite the evidence using source/page/chunk references.

Context:
{context}

Question:
{question}

Return in this format:

Answer:
<answer>

Evidence:
- <source citation>
- <source citation>
"""

def build_context(sources: list[dict]) -> str:
    parts = []
    for s in sources:
        parts.append(
            f"[Source: {s['source']}, Page: {s['page']}, Chunk: {s['chunk_id']}]\n{s['text']}"
        )
    return "\n\n".join(parts)

def build_prompt(question: str, sources: list[dict]) -> str:
    context = build_context(sources)
    return CLINICAL_PROMPT.format(context=context, question=question)