from app.config import settings
from app.providers.llm.anthropic_provider import AnthropicProvider
from app.providers.llm.gemini_provider import GeminiProvider

def get_llm_provider():
    if settings.LLM_PROVIDER.lower() == "gemini":
        return GeminiProvider(settings.LLM_MODEL)
    return AnthropicProvider(settings.LLM_MODEL)