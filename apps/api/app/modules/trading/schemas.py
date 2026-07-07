from typing import Literal, Optional
from pydantic import BaseModel


class JournalEntry(BaseModel):
    id: int
    date: str
    symbol: str
    direction: str  # "long" | "short"
    result: str     # "win" | "loss" | "breakeven"
    notes: str


# --- Market ---

class CoinMetric(BaseModel):
    symbol: str
    price_usd: float
    change_24h: float


class FearGreedMetric(BaseModel):
    value: int
    label: str


class MarketOverview(BaseModel):
    btc: CoinMetric
    eth: CoinMetric
    sol: CoinMetric
    total_market_cap_usd: float
    btc_dominance: float
    fear_greed: FearGreedMetric
    provider_status: dict[str, bool]


# --- News ---

class NewsArticle(BaseModel):
    id: str
    headline: str
    source: str
    published_at: str
    summary: str
    url: str


class NewsArticleDetail(NewsArticle):
    content: Optional[str] = None


class NewsFeed(BaseModel):
    articles: list[NewsArticle]
    total: int
    page: int


# --- Calendar ---

class EconomicEvent(BaseModel):
    id: str
    title: str
    country: str
    impact: Literal["low", "medium", "high"]
    scheduled_at: str
    actual: Optional[str] = None
    forecast: Optional[str] = None
    previous: Optional[str] = None


class EconomicCalendar(BaseModel):
    events: list[EconomicEvent]


# --- AI ---

class SummarizeRequest(BaseModel):
    article_id: str


class ImpactRequest(BaseModel):
    article_id: str


class ArticleSummary(BaseModel):
    article_id: str
    tldr: str
    key_points: list[str]
    important_numbers: list[str]
    risk_factors: list[str]
    provider: str


class MarketImpact(BaseModel):
    article_id: str
    bias: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str
    provider: str


class MarketInsight(BaseModel):
    daily_summary: str
    risk_warnings: list[str]
    opportunity_signals: list[str]
    provider: str


# --- Jarvis ---

class VoiceAudioMetadata(BaseModel):
    provider: str
    text: str
    audio_url: Optional[str] = None
    duration_estimate_seconds: Optional[float] = None


class MorningBriefing(BaseModel):
    briefing_type: str
    generated_at: str
    script: str
    voice: VoiceAudioMetadata
    ai_provider: str
    voice_provider: str


class RecapRequest(BaseModel):
    recap_type: Literal["morning", "midday", "evening"] = "morning"


class MarketRecap(BaseModel):
    recap_type: str
    generated_at: str
    script: str
    voice: VoiceAudioMetadata
    ai_provider: str
    voice_provider: str


class ReadNewsRequest(BaseModel):
    article_id: str


class NewsNarration(BaseModel):
    article_id: str
    headline: str
    script: str
    voice: VoiceAudioMetadata
    ai_provider: str
    voice_provider: str


class JarvisHistoryEntry(BaseModel):
    id: str
    entry_type: str      # "briefing" | "recap" | "news"
    title: str
    generated_at: str
    script_preview: str
    ai_provider: str
    voice_provider: str


class JarvisHistory(BaseModel):
    entries: list[JarvisHistoryEntry]
    total: int
