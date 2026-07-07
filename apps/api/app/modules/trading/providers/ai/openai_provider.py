"""
OpenAI provider skeleton.

To activate:
  1. pip install openai
  2. Set OPENAI_API_KEY in your environment
  3. Call set_ai_provider(OpenAIProvider(api_key=...)) in main.py startup
"""
from app.modules.trading.providers.ai.base_ai_provider import (
    BaseAIProvider,
    ArticleSummaryData,
    MarketImpactData,
    MarketInsightData,
    MarketContext,
)

_SUMMARIZE_PROMPT = """
You are a financial analyst. Given the article headline and content below, return a JSON object with:
- tldr: one sentence summary
- key_points: list of 3-5 bullet points
- important_numbers: list of key figures/percentages mentioned
- risk_factors: list of 2-4 risks
Return only valid JSON, no markdown.
"""

_IMPACT_PROMPT = """
You are a crypto market analyst. Given the article and current market context, return a JSON object with:
- bias: "bullish", "bearish", or "neutral"
- confidence: float between 0.0 and 1.0
- reasoning: one paragraph explanation
Return only valid JSON, no markdown.
"""


class OpenAIProvider(BaseAIProvider):
    """
    Production OpenAI provider.
    Uses GPT-4o-mini by default for cost efficiency.
    Swap to gpt-4o for higher quality at higher cost.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self._api_key = api_key
        self._model = model

    @property
    def provider_name(self) -> str:
        return f"openai/{self._model}"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    async def summarize_article(self, article_id: str, headline: str, content: str) -> ArticleSummaryData:
        # import openai
        # client = openai.AsyncOpenAI(api_key=self._api_key)
        # response = await client.chat.completions.create(
        #     model=self._model,
        #     messages=[
        #         {"role": "system", "content": _SUMMARIZE_PROMPT},
        #         {"role": "user", "content": f"Headline: {headline}\n\nContent: {content}"},
        #     ],
        #     response_format={"type": "json_object"},
        # )
        # data = json.loads(response.choices[0].message.content)
        # return ArticleSummaryData(**data)
        raise NotImplementedError("Set OPENAI_API_KEY and uncomment the implementation above")

    async def analyze_impact(
        self, article_id: str, headline: str, content: str, context: MarketContext
    ) -> MarketImpactData:
        raise NotImplementedError("Set OPENAI_API_KEY and uncomment the implementation above")

    async def generate_insights(self, context: MarketContext, headlines: list[str]) -> MarketInsightData:
        raise NotImplementedError("Set OPENAI_API_KEY and uncomment the implementation above")
