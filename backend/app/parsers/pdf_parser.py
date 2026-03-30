import fitz
import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def parse_pdf(file_bytes: bytes, filename: str) -> list[dict]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []

    for page_num, page in enumerate(doc, start=1):
        text = clean_text(page.get_text())
        if text:
            pages.append({
                "source": filename,
                "page": page_num,
                "text": text,
            })

    return pages