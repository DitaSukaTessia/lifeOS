from fastapi import APIRouter, Query

from app.modules.trading.ai_router import ai_router
from app.modules.trading.jarvis_router import jarvis_router
from app.modules.trading.schemas import (
    JournalEntry,
    MarketOverview,
    NewsFeed,
    NewsArticleDetail,
    EconomicCalendar,
)
from app.modules.trading.service import get_journal_entries
from app.modules.trading.market_service import get_market_overview
from app.modules.trading.news_service import get_news_feed, get_news_article
from app.modules.trading.calendar_service import get_economic_calendar

router = APIRouter(prefix="/trading", tags=["trading"])
router.include_router(ai_router)
router.include_router(jarvis_router)


@router.get("/journal", response_model=list[JournalEntry])
async def journal() -> list[JournalEntry]:
    return await get_journal_entries()


@router.get("/market", response_model=MarketOverview)
async def market() -> MarketOverview:
    return await get_market_overview()


@router.get("/news", response_model=NewsFeed)
async def news(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
) -> NewsFeed:
    return await get_news_feed(page=page, limit=limit)


@router.get("/news/{article_id}", response_model=NewsArticleDetail)
async def news_article(article_id: str) -> NewsArticleDetail:
    return await get_news_article(article_id)


@router.get("/calendar", response_model=EconomicCalendar)
async def calendar() -> EconomicCalendar:
    return await get_economic_calendar()
