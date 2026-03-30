import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def parse_txt(file_bytes: bytes, filename: str) -> list[dict]:
    text = clean_text(file_bytes.decode("utf-8", errors="ignore"))
    return [{
        "source": filename,
        "page": 1,
        "text": text,
    }]