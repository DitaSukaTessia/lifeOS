from fastapi import APIRouter

from app.modules.trading.schemas import ArticleSummary, MarketImpact, MarketInsight, SummarizeRequest, ImpactRequest
from app.modules.trading.summary_service import summarize_article
from app.modules.trading.impact_service import analyze_impact
from app.modules.trading.insight_service import generate_insights

ai_router = APIRouter(prefix="/ai", tags=["trading-ai"])


@ai_router.post("/summarize", response_model=ArticleSummary)
async def summarize(body: SummarizeRequest) -> ArticleSummary:
    return await summarize_article(body.article_id)


@ai_router.post("/impact", response_model=MarketImpact)
async def impact(body: ImpactRequest) -> MarketImpact:
    return await analyze_impact(body.article_id)


@ai_router.get("/insights", response_model=MarketInsight)
async def insights() -> MarketInsight:
    return await generate_insights()
