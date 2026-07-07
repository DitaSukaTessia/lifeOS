import asyncio

from fastapi import HTTPException

from app.modules.trading.providers.news_provider import NewsProvider
from app.modules.trading.schemas import NewsArticle, NewsArticleDetail, NewsFeed


async def get_news_feed(page: int = 1, limit: int = 20) -> NewsFeed:
    provider = NewsProvider()
    articles_data, total = await asyncio.gather(
        provider.get_articles(page=page, limit=limit),
        provider.total_count(),
    )
    articles = [
        NewsArticle(
            id=a.id,
            headline=a.headline,
            source=a.source,
            published_at=a.published_at,
            summary=a.summary,
            url=a.url,
        )
        for a in articles_data
    ]
    return NewsFeed(articles=articles, total=total, page=page)


async def get_news_article(article_id: str) -> NewsArticleDetail:
    provider = NewsProvider()
    data = await provider.get_article_by_id(article_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return NewsArticleDetail(
        id=data.id,
        headline=data.headline,
        source=data.source,
        published_at=data.published_at,
        summary=data.summary,
        url=data.url,
        content=data.content,
    )
