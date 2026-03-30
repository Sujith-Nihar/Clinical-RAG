import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Clinical RAG API"

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")   # anthropic / gemini
    LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    TOP_K = int(os.getenv("TOP_K", 6))
    SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", 0.30))

settings = Settings()