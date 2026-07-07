import asyncio

from app.modules.trading.ai_service import get_ai_provider
from app.modules.trading.market_service import get_market_overview
from app.modules.trading.news_service import get_news_feed
from app.modules.trading.providers.ai.base_ai_provider import MarketContext
from app.modules.trading.schemas import MarketInsight


async def generate_insights() -> MarketInsight:
    overview, feed = await asyncio.gather(
        get_market_overview(),
        get_news_feed(page=1, limit=5),
    )

    context = MarketContext(
        btc_price=overview.btc.price_usd,
        btc_change=overview.btc.change_24h,
        fear_greed_value=overview.fear_greed.value,
        fear_greed_label=overview.fear_greed.label,
    )

    provider = get_ai_provider()
    result = await provider.generate_insights(
        context=context,
        headlines=[a.headline for a in feed.articles],
    )

    return MarketInsight(
        daily_summary=result.daily_summary,
        risk_warnings=result.risk_warnings,
        opportunity_signals=result.opportunity_signals,
        provider=provider.provider_name,
    )
