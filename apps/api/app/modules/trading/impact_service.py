import asyncio

from app.modules.trading.ai_service import get_ai_provider
from app.modules.trading.news_service import get_news_article
from app.modules.trading.market_service import get_market_overview
from app.modules.trading.providers.ai.base_ai_provider import MarketContext
from app.modules.trading.schemas import MarketImpact


async def analyze_impact(article_id: str) -> MarketImpact:
    article, overview = await asyncio.gather(
        get_news_article(article_id),
        get_market_overview(),
    )

    context = MarketContext(
        btc_price=overview.btc.price_usd,
        btc_change=overview.btc.change_24h,
        fear_greed_value=overview.fear_greed.value,
        fear_greed_label=overview.fear_greed.label,
    )

    provider = get_ai_provider()
    result = await provider.analyze_impact(
        article_id=article_id,
        headline=article.headline,
        content=article.content or article.summary,
        context=context,
    )

    return MarketImpact(
        article_id=article_id,
        bias=result.bias,  # type: ignore[arg-type]
        confidence=result.confidence,
        reasoning=result.reasoning,
        provider=provider.provider_name,
    )
