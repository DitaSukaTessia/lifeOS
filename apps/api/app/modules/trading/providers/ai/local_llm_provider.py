"""
Local LLM provider skeleton (Ollama).

To activate:
  1. Install Ollama: https://ollama.ai
  2. Run: ollama pull llama3
  3. pip install httpx (already in dev deps)
  4. Call set_ai_provider(LocalLLMProvider()) in main.py startup
"""
from app.modules.trading.providers.ai.base_ai_provider import (
    BaseAIProvider,
    ArticleSummaryData,
    MarketImpactData,
    MarketInsightData,
    MarketContext,
)


class LocalLLMProvider(BaseAIProvider):
    """
    Ollama-based local LLM provider.
    Zero API cost, runs fully offline.
    Quality depends on the model pulled locally.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self._base_url = base_url
        self._model = model

    @property
    def provider_name(self) -> str:
        return f"local/{self._model}"

    @property
    def is_available(self) -> bool:
        # Requires a live health check against the Ollama HTTP API
        # import httpx
        # try:
        #     r = httpx.get(f"{self._base_url}/api/tags", timeout=2)
        #     return r.status_code == 200
        # except Exception:
        #     return False
        return False

    async def summarize_article(self, article_id: str, headline: str, content: str) -> ArticleSummaryData:
        # import httpx, json
        # async with httpx.AsyncClient() as client:
        #     r = await client.post(
        #         f"{self._base_url}/api/generate",
        #         json={
        #             "model": self._model,
        #             "prompt": f"Summarize this financial article as JSON...\n{headline}\n{content}",
        #             "format": "json",
        #             "stream": False,
        #         },
        #         timeout=60,
        #     )
        #     data = json.loads(r.json()["response"])
        #     return ArticleSummaryData(**data)
        raise NotImplementedError("Start Ollama and uncomment the implementation above")

    async def analyze_impact(
        self, article_id: str, headline: str, content: str, context: MarketContext
    ) -> MarketImpactData:
        raise NotImplementedError("Start Ollama and uncomment the implementation above")

    async def generate_insights(self, context: MarketContext, headlines: list[str]) -> MarketInsightData:
        raise NotImplementedError("Start Ollama and uncomment the implementation above")
