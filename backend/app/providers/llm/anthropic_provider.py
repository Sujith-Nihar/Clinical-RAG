from anthropic import Anthropic
from app.providers.llm.base import LLMProvider
from app.config import settings

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str | None = None):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = model or settings.LLM_MODEL

    def generate(self, prompt: str, system: str | None = None) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=900,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text