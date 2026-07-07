"""
Google Gemini provider for Trading Terminal AI features.

Activation:
  1. pip install -e . (installs google-genai from pyproject.toml)
  2. Add GEMINI_API_KEY=<your-key> to apps/api/.env
  3. Provider auto-activates at API startup (wired in main.py lifespan)

Default model: gemini-2.0-flash — fast and cost-efficient.
Swap to gemini-2.0-flash-thinking-exp for higher reasoning quality.
"""
import json
import logging

from google import genai
from google.genai import types

from app.modules.trading.providers.ai.base_ai_provider import (
    ArticleSummaryData,
    BaseAIProvider,
    MarketContext,
    MarketImpactData,
    MarketInsightData,
)

log = logging.getLogger(__name__)

_JSON_CONFIG = types.GenerateContentConfig(response_mime_type="application/json")

_SUMMARIZE_PROMPT = """\
You are a financial analyst. Given the article headline and content below, return a JSON object with exactly these fields:
- tldr: one sentence summary
- key_points: list of 3-5 bullet points (strings)
- important_numbers: list of key figures/percentages mentioned (strings)
- risk_factors: list of 2-4 risks (strings)
Return only valid JSON, no markdown, no code blocks.\
"""

_IMPACT_PROMPT = """\
You are a crypto market analyst. Given the article and current market context, return a JSON object with exactly these fields:
- bias: one of "bullish", "bearish", or "neutral"
- confidence: float between 0.0 and 1.0
- reasoning: one paragraph explanation
Return only valid JSON, no markdown, no code blocks.\
"""

_INSIGHTS_PROMPT = """\
You are a senior crypto market analyst. Given the current market context and recent headlines, return a JSON object with exactly these fields:
- daily_summary: 2-3 sentence summary of today's market conditions
- risk_warnings: list of 3-5 current risk factors (strings)
- opportunity_signals: list of 2-4 trading opportunities or bullish signals (strings)
Return only valid JSON, no markdown, no code blocks.\
"""


class GeminiProvider(BaseAIProvider):
    """
    Production Gemini provider using google-genai SDK.
    Default model: gemini-2.0-flash — fast, cheap, good quality.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self._client = genai.Client(api_key=api_key)
        self._api_key = api_key
        self._model = model

    @property
    def provider_name(self) -> str:
        return f"gemini/{self._model}"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    async def summarize_article(self, article_id: str, headline: str, content: str) -> ArticleSummaryData:
        prompt = f"{_SUMMARIZE_PROMPT}\n\nHeadline: {headline}\n\nContent: {content}"
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=_JSON_CONFIG,
        )
        data = json.loads(response.text)
        return ArticleSummaryData(
            tldr=data["tldr"],
            key_points=data["key_points"],
            important_numbers=data["important_numbers"],
            risk_factors=data["risk_factors"],
        )

    async def analyze_impact(
        self, article_id: str, headline: str, content: str, context: MarketContext
    ) -> MarketImpactData:
        market_ctx = (
            f"BTC Price: ${context.btc_price:,.0f} ({context.btc_change:+.2f}%)\n"
            f"Fear & Greed: {context.fear_greed_value} ({context.fear_greed_label})"
        )
        prompt = f"{_IMPACT_PROMPT}\n\nHeadline: {headline}\n\nContent: {content}\n\nMarket Context:\n{market_ctx}"
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=_JSON_CONFIG,
        )
        data = json.loads(response.text)
        return MarketImpactData(
            bias=data["bias"],
            confidence=float(data["confidence"]),
            reasoning=data["reasoning"],
        )

    async def generate_insights(self, context: MarketContext, headlines: list[str]) -> MarketInsightData:
        headlines_text = "\n".join(f"- {h}" for h in headlines)
        market_ctx = (
            f"BTC Price: ${context.btc_price:,.0f} ({context.btc_change:+.2f}%)\n"
            f"Fear & Greed: {context.fear_greed_value} ({context.fear_greed_label})"
        )
        prompt = (
            f"{_INSIGHTS_PROMPT}\n\n"
            f"Market Context:\n{market_ctx}\n\n"
            f"Recent Headlines:\n{headlines_text}"
        )
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=_JSON_CONFIG,
        )
        data = json.loads(response.text)
        return MarketInsightData(
            daily_summary=data["daily_summary"],
            risk_warnings=data["risk_warnings"],
            opportunity_signals=data["opportunity_signals"],
        )
