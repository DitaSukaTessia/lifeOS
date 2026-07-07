from app.modules.trading.ai_service import get_ai_provider
from app.modules.trading.news_service import get_news_article
from app.modules.trading.schemas import ArticleSummary


async def summarize_article(article_id: str) -> ArticleSummary:
    article = await get_news_article(article_id)
    provider = get_ai_provider()

    result = await provider.summarize_article(
        article_id=article_id,
        headline=article.headline,
        content=article.content or article.summary,
    )

    return ArticleSummary(
        article_id=article_id,
        tldr=result.tldr,
        key_points=result.key_points,
        important_numbers=result.important_numbers,
        risk_factors=result.risk_factors,
        provider=provider.provider_name,
    )
