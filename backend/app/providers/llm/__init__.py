from app.config import settings
from app.providers.llm.gemini_provider import GeminiProvider
from app.providers.llm.anthropic_provider import AnthropicProvider

def get_llm_provider():
    if settings.LLM_PROVIDER == "gemini":
        return GeminiProvider()
    elif settings.LLM_PROVIDER == "anthropic":
        return AnthropicProvider()

    raise ValueError("Unsupported LLM provider")