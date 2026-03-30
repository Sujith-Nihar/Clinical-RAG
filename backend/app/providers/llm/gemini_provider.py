from google import genai
from app.providers.llm.base import LLMProvider
from app.config import settings

class GeminiProvider(LLMProvider):
    def __init__(self, model: str | None = None):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = model or settings.LLM_MODEL

    def generate(self, prompt: str, system: str | None = None) -> str:
        full_prompt = prompt if not system else f"{system}\n\n{prompt}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )
        return response.text