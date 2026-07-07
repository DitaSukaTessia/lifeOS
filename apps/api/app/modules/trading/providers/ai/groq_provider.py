"""
Groq provider for Trading Terminal AI features.

Activation:
  1. pip install -e . (installs groq from pyproject.toml)
  2. Add GROQ_API_KEY=<your-key> to apps/api/.env
  3. Provider auto-activates at API startup (wired in main.py lifespan)

Default model: llama-3.3-70b-versatile — fast, capable, free tier available.
"""
import json
import logging

from groq import AsyncGroq

from app.modules.trading.providers.ai.base_ai_provider import (
    ArticleSummaryData,
    BaseAIProvider,
    BriefingScriptData,
    MarketContext,
    MarketImpactData,
    MarketInsightData,
    NewsNarrationData,
)

log = logging.getLogger(__name__)

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

_BRIEFING_PROMPT = """\
You are Jarvis, a professional AI trading assistant. Generate a {briefing_type} market briefing script to be read aloud by a narrator.

Return a JSON object with exactly one field:
- full_script: complete narration (350-600 words, natural spoken language, no markdown, no bullet points, no headers)

The script must flow naturally through these sections in order:
1. Opening greeting appropriate for {briefing_type}
2. Current market conditions (BTC price, trend, Fear & Greed)
3. Key news highlights (weave in 2-3 headlines conversationally)
4. Upcoming economic events (mention 1-2 if relevant)
5. Risk alerts
6. Closing note

Write as if speaking to a trader starting their day. Use contractions, natural transitions, vary sentence length.\
"""

_NEWS_NARRATION_PROMPT = """\
You are a financial news narrator. Convert this article into a natural voice reading script.

Return a JSON object with exactly one field:
- full_script: natural narration (100-200 words, spoken language, no markdown, no bullet points)

Start by reading the headline naturally, then expand with key details from the summary and content.
Write as if reading live on a financial radio broadcast.\
"""


class GroqProvider(BaseAIProvider):
    """
    Groq-hosted LLM provider. Extremely fast inference via Groq's LPU hardware.
    Default model: llama-3.3-70b-versatile.
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self._client = AsyncGroq(api_key=api_key)
        self._api_key = api_key
        self._model = model

    @property
    def provider_name(self) -> str:
        return f"groq/{self._model}"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    async def _complete(self, system: str, user: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    async def summarize_article(self, article_id: str, headline: str, content: str) -> ArticleSummaryData:
        user = f"Headline: {headline}\n\nContent: {content}"
        data = json.loads(await self._complete(_SUMMARIZE_PROMPT, user))
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
        user = f"Headline: {headline}\n\nContent: {content}\n\nMarket Context:\n{market_ctx}"
        data = json.loads(await self._complete(_IMPACT_PROMPT, user))
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
        user = f"Market Context:\n{market_ctx}\n\nRecent Headlines:\n{headlines_text}"
        data = json.loads(await self._complete(_INSIGHTS_PROMPT, user))
        return MarketInsightData(
            daily_summary=data["daily_summary"],
            risk_warnings=data["risk_warnings"],
            opportunity_signals=data["opportunity_signals"],
        )

    async def generate_briefing_script(
        self,
        context: MarketContext,
        headlines: list[str],
        calendar_events: list[str],
        daily_summary: str,
        risk_warnings: list[str],
        briefing_type: str = "morning",
    ) -> BriefingScriptData:
        system = _BRIEFING_PROMPT.format(briefing_type=briefing_type)
        market_ctx = (
            f"BTC Price: ${context.btc_price:,.0f} ({context.btc_change:+.2f}%)\n"
            f"Fear & Greed: {context.fear_greed_value} ({context.fear_greed_label})"
        )
        headlines_text = "\n".join(f"- {h}" for h in headlines)
        calendar_text = "\n".join(f"- {e}" for e in calendar_events) or "No major events today."
        risks_text = "\n".join(f"- {r}" for r in risk_warnings)
        user = (
            f"Market Context:\n{market_ctx}\n\n"
            f"Market Summary: {daily_summary}\n\n"
            f"Key Headlines:\n{headlines_text}\n\n"
            f"Economic Calendar:\n{calendar_text}\n\n"
            f"Risk Alerts:\n{risks_text}"
        )
        data = json.loads(await self._complete(system, user))
        return BriefingScriptData(full_script=data["full_script"])

    async def generate_news_narration(
        self,
        headline: str,
        content: str,
        summary: str,
    ) -> NewsNarrationData:
        user = f"Headline: {headline}\n\nSummary: {summary}\n\nContent: {content}"
        data = json.loads(await self._complete(_NEWS_NARRATION_PROMPT, user))
        return NewsNarrationData(full_script=data["full_script"])
