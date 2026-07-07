from abc import ABC, abstractmethod
from dataclasses import dataclass


# --- Input context ---

@dataclass
class MarketContext:
    btc_price: float
    btc_change: float
    fear_greed_value: int
    fear_greed_label: str


# --- Output data structures ---

@dataclass
class ArticleSummaryData:
    tldr: str
    key_points: list[str]
    important_numbers: list[str]
    risk_factors: list[str]


@dataclass
class MarketImpactData:
    bias: str  # "bullish" | "bearish" | "neutral"
    confidence: float  # 0.0–1.0
    reasoning: str


@dataclass
class MarketInsightData:
    daily_summary: str
    risk_warnings: list[str]
    opportunity_signals: list[str]


@dataclass
class BriefingScriptData:
    full_script: str  # natural speech, no markdown


@dataclass
class NewsNarrationData:
    full_script: str  # voice-friendly article reading


# --- Provider contract ---

class BaseAIProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    async def summarize_article(
        self,
        article_id: str,
        headline: str,
        content: str,
    ) -> ArticleSummaryData: ...

    @abstractmethod
    async def analyze_impact(
        self,
        article_id: str,
        headline: str,
        content: str,
        context: MarketContext,
    ) -> MarketImpactData: ...

    @abstractmethod
    async def generate_insights(
        self,
        context: MarketContext,
        headlines: list[str],
    ) -> MarketInsightData: ...

    @abstractmethod
    async def generate_briefing_script(
        self,
        context: MarketContext,
        headlines: list[str],
        calendar_events: list[str],
        daily_summary: str,
        risk_warnings: list[str],
        briefing_type: str = "morning",
    ) -> BriefingScriptData: ...

    @abstractmethod
    async def generate_news_narration(
        self,
        headline: str,
        content: str,
        summary: str,
    ) -> NewsNarrationData: ...
