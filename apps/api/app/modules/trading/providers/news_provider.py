from dataclasses import dataclass
from typing import Optional


@dataclass
class NewsArticleData:
    id: str
    headline: str
    source: str
    published_at: str  # ISO 8601
    summary: str
    url: str
    content: Optional[str] = None


_MOCK_ARTICLES: list[NewsArticleData] = [
    NewsArticleData(
        id="1",
        headline="Bitcoin surges past $67,000 as ETF inflows accelerate",
        source="CoinDesk",
        published_at="2026-06-19T08:30:00Z",
        summary="Bitcoin climbed to its highest level in three weeks, driven by renewed institutional interest and strong ETF inflows exceeding $400M in a single day.",
        url="https://example.com/news/1",
        content=(
            "Bitcoin surged past the $67,000 mark on Thursday, reaching levels not seen in nearly three weeks. "
            "The move was attributed to a combination of strong institutional buying through spot Bitcoin ETFs "
            "and reduced selling pressure from long-term holders.\n\n"
            "Spot Bitcoin ETF products in the United States recorded net inflows of approximately $412 million "
            "on Wednesday, the highest single-day figure in over a month. BlackRock's IBIT led the charge "
            "with $213 million in new capital.\n\n"
            "Analysts pointed to improving macroeconomic conditions and a weakening dollar as secondary "
            "catalysts for the move."
        ),
    ),
    NewsArticleData(
        id="2",
        headline="Ethereum developers finalize Pectra upgrade timeline",
        source="The Block",
        published_at="2026-06-19T07:15:00Z",
        summary="The Ethereum core development team confirmed the Pectra network upgrade is scheduled for mainnet deployment within six weeks, bringing key EIP improvements.",
        url="https://example.com/news/2",
        content=(
            "Ethereum's core developers reached consensus during Thursday's AllCoreDevs call, setting a firm "
            "mainnet deployment window for the Pectra upgrade. The upgrade bundles several Ethereum Improvement "
            "Proposals aimed at improving validator UX, blob throughput, and smart contract efficiency.\n\n"
            "Key EIPs included in Pectra feature EIP-7702, which allows EOAs to temporarily adopt smart "
            "contract behavior, and increases to the blob target count per block, directly benefiting "
            "Layer 2 rollups."
        ),
    ),
    NewsArticleData(
        id="3",
        headline="Fed signals no rate cuts before Q4 as inflation data disappoints",
        source="Reuters",
        published_at="2026-06-19T06:00:00Z",
        summary="Federal Reserve officials indicated rate reductions are unlikely before Q4 after May CPI came in above consensus at 3.1%, dampening expectations for near-term easing.",
        url="https://example.com/news/3",
        content=(
            "Federal Reserve Governor Michelle Bowman said Thursday that the central bank would need to see "
            "several more months of cooling inflation data before considering interest rate reductions. "
            "Her comments followed the release of May CPI data showing a 3.1% year-over-year increase, "
            "above the 2.9% consensus estimate.\n\n"
            "Risk assets initially sold off on the news but recovered as traders interpreted the Fed's "
            "messaging as consistent with a patient, data-dependent approach rather than a hawkish pivot."
        ),
    ),
    NewsArticleData(
        id="4",
        headline="Solana DEX volume hits $8B weekly milestone",
        source="DeFi Llama",
        published_at="2026-06-18T21:00:00Z",
        summary="Decentralized exchanges on Solana processed over $8 billion in weekly volume, with Jupiter and Raydium capturing the largest share as network activity remains elevated.",
        url="https://example.com/news/4",
        content=(
            "Solana-based decentralized exchanges reached a weekly volume milestone of $8 billion, "
            "maintaining a position among the top DEX ecosystems globally. Jupiter remained the dominant "
            "aggregator, routing approximately 55% of all swap volume, while Raydium captured most of "
            "the remaining liquidity pool activity.\n\n"
            "Network transaction fees and validator rewards hit multi-month highs, signaling sustained "
            "user engagement beyond speculative trading."
        ),
    ),
    NewsArticleData(
        id="5",
        headline="BlackRock files for tokenized money market fund expansion",
        source="Bloomberg",
        published_at="2026-06-18T14:00:00Z",
        summary="BlackRock submitted documentation to extend its tokenized money market fund to additional blockchain networks, citing growing institutional demand for on-chain yield products.",
        url="https://example.com/news/5",
        content=(
            "BlackRock submitted regulatory documentation indicating plans to extend its tokenized money "
            "market fund, BUIDL, to additional blockchain networks beyond Ethereum. The filing cited "
            "strong institutional demand from asset managers and family offices seeking compliant, "
            "on-chain yield instruments.\n\n"
            "The fund currently holds over $500 million in assets and offers institutional investors "
            "exposure to U.S. Treasury yields through a tokenized format. BlackRock indicated Avalanche "
            "and Aptos are under evaluation for the expansion."
        ),
    ),
]


class NewsProvider:
    provider_name = "mock_news"

    @property
    def is_available(self) -> bool:
        return True

    async def get_articles(self, page: int = 1, limit: int = 20) -> list[NewsArticleData]:
        start = (page - 1) * limit
        return _MOCK_ARTICLES[start : start + limit]

    async def get_article_by_id(self, article_id: str) -> Optional[NewsArticleData]:
        return next((a for a in _MOCK_ARTICLES if a.id == article_id), None)

    async def total_count(self) -> int:
        return len(_MOCK_ARTICLES)
