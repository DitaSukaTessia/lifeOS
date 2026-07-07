from app.modules.trading.providers.ai.base_ai_provider import (
    BaseAIProvider,
    ArticleSummaryData,
    BriefingScriptData,
    MarketContext,
    MarketImpactData,
    MarketInsightData,
    NewsNarrationData,
)

_SUMMARIES: dict[str, ArticleSummaryData] = {
    "1": ArticleSummaryData(
        tldr="Bitcoin broke $67K on $412M daily ETF inflows — strongest institutional buying in over a month.",
        key_points=[
            "ETF net inflows reached $412M in a single trading day",
            "BlackRock IBIT led all products with $213M in new capital",
            "BTC hit a 3-week high as long-term holders reduced selling pressure",
            "A weakening dollar provided secondary macro support",
        ],
        important_numbers=["$412M single-day ETF inflows", "$213M from BlackRock IBIT", "$67,420 BTC price"],
        risk_factors=[
            "ETF-driven rallies can reverse rapidly on outflow days",
            "Elevated leverage in perpetual futures markets increases drawdown risk",
            "Macro conditions remain data-dependent — one bad CPI print can shift sentiment",
        ],
    ),
    "2": ArticleSummaryData(
        tldr="Ethereum Pectra upgrade confirmed for mainnet within 6 weeks — smart EOAs and higher blob throughput incoming.",
        key_points=[
            "Mainnet deployment window confirmed at AllCoreDevs call — no known blockers",
            "EIP-7702 lets EOA wallets temporarily act as smart contracts",
            "Blob throughput increase directly reduces fees for Arbitrum, Base, and other L2s",
            "Upgrade bundles multiple EIPs with incremental but compounding effect",
        ],
        important_numbers=["6-week mainnet window", "EIP-7702", "Multiple blob count increases"],
        risk_factors=[
            "Ethereum upgrades have historically slipped timelines",
            "EIP-7702 introduces new wallet attack surface that needs security auditing",
            "Market may already be pricing in the upgrade ahead of deployment",
        ],
    ),
    "3": ArticleSummaryData(
        tldr="May CPI printed 3.1% vs 2.9% consensus — Fed pushes rate cut expectations to Q4, sustaining macro pressure on risk assets.",
        key_points=[
            "CPI YoY at 3.1%, above the 2.9% consensus estimate",
            "Fed Governor Bowman signals patience — further data needed before any cuts",
            "Rate cut expectations now pushed to Q4 2026 at earliest",
            "Risk assets sold off on the print but recovered intraday — resilience noted",
        ],
        important_numbers=["3.1% CPI YoY (vs 2.9% forecast)", "Q4 2026 earliest rate cut window"],
        risk_factors=[
            "Higher-for-longer rates reduce the relative appeal of non-yielding assets like BTC",
            "Dollar strength from rate differential suppresses USD-denominated crypto prices",
            "Each above-consensus CPI print extends the restrictive period further",
        ],
    ),
    "4": ArticleSummaryData(
        tldr="Solana's DEX ecosystem hit $8B weekly volume — Jupiter at 55% share, validator rewards at multi-month highs.",
        key_points=[
            "$8B weekly DEX volume milestone — top-tier globally across all chains",
            "Jupiter aggregator routes 55% of all Solana swap volume",
            "Raydium captures the majority of remaining liquidity pool activity",
            "Network fees and validator rewards at multi-month highs signal sustained demand",
        ],
        important_numbers=["$8B weekly DEX volume", "55% Jupiter market share", "Multi-month high validator rewards"],
        risk_factors=[
            "DEX volumes are highly correlated with market sentiment and can drop sharply",
            "Base and Arbitrum growing rapidly as direct competitors for DeFi activity",
            "SOL price sustainability depends on continued ecosystem growth",
        ],
    ),
    "5": ArticleSummaryData(
        tldr="BlackRock's $500M+ BUIDL fund expanding to Avalanche and Aptos — signals accelerating TradFi-DeFi convergence.",
        key_points=[
            "BUIDL holds $500M+ in tokenized U.S. Treasury exposure",
            "Expansion targets Avalanche and Aptos as next deployment networks",
            "Filing targets institutional asset managers and family offices exclusively",
            "Regulatory documentation signals a formal, long-term RWA commitment from BlackRock",
        ],
        important_numbers=["$500M+ BUIDL AUM", "Avalanche and Aptos as target networks"],
        risk_factors=[
            "Regulatory landscape for tokenized securities remains uncertain across jurisdictions",
            "Direct price impact on AVAX and APT tokens is indirect and speculative",
            "Competition from Franklin Templeton, WisdomTree, and others in the RWA space",
        ],
    ),
}

_IMPACTS: dict[str, MarketImpactData] = {
    "1": MarketImpactData(
        bias="bullish",
        confidence=0.82,
        reasoning=(
            "Strong, consistent ETF inflows signal institutional conviction rather than retail speculation. "
            "$412M single-day inflow is historically significant — similar flow events in 2024 preceded "
            "sustained moves higher. BlackRock's IBIT dominance indicates this is programmatic accumulation."
        ),
    ),
    "2": MarketImpactData(
        bias="bullish",
        confidence=0.70,
        reasoning=(
            "Confirmed protocol upgrade timelines with clear technical improvements are historically bullish "
            "for ETH. The L2 blob throughput benefit expands the addressable ecosystem and reduces user costs, "
            "improving network stickiness."
        ),
    ),
    "3": MarketImpactData(
        bias="bearish",
        confidence=0.76,
        reasoning=(
            "Delayed rate cuts remove a key risk-asset catalyst. Higher rates for longer increase the "
            "opportunity cost of holding non-yielding assets like BTC. Historically, crypto bull runs are "
            "amplified in rate-cutting cycles — their absence is a structural headwind."
        ),
    ),
    "4": MarketImpactData(
        bias="bullish",
        confidence=0.68,
        reasoning=(
            "Record DEX volume during a volatile macro period demonstrates genuine ecosystem demand, not "
            "just speculation. Network fundamentals strengthening alongside usage is a healthy sign for "
            "SOL's long-term value accrual. Validator economics improving is a positive supply dynamic."
        ),
    ),
    "5": MarketImpactData(
        bias="bullish",
        confidence=0.60,
        reasoning=(
            "BlackRock expanding tokenized RWA products to additional L1 chains validates on-chain finance "
            "broadly. While the direct price impact is limited short-term, the institutional signal effect "
            "on crypto adoption supports a multi-year thesis."
        ),
    ),
}

_DEFAULT_SUMMARY = ArticleSummaryData(
    tldr="Insufficient article content to generate a detailed summary.",
    key_points=["Review the full article for key developments", "Monitor related market data for context"],
    important_numbers=[],
    risk_factors=["Market uncertainty remains elevated", "Verify information from primary sources"],
)

_DEFAULT_IMPACT = MarketImpactData(
    bias="neutral",
    confidence=0.40,
    reasoning="Insufficient context to determine a directional bias with meaningful confidence.",
)


class MockAIProvider(BaseAIProvider):
    provider_name = "mock"

    @property
    def is_available(self) -> bool:
        return True

    async def summarize_article(self, article_id: str, headline: str, content: str) -> ArticleSummaryData:
        return _SUMMARIES.get(article_id, _DEFAULT_SUMMARY)

    async def analyze_impact(
        self, article_id: str, headline: str, content: str, context: MarketContext
    ) -> MarketImpactData:
        return _IMPACTS.get(article_id, _DEFAULT_IMPACT)

    async def generate_briefing_script(
        self,
        context: MarketContext,
        headlines: list[str],
        calendar_events: list[str],
        daily_summary: str,
        risk_warnings: list[str],
        briefing_type: str = "morning",
    ) -> BriefingScriptData:
        direction = "up" if context.btc_change >= 0 else "down"
        return BriefingScriptData(
            full_script=(
                f"Good {'morning' if briefing_type == 'morning' else 'afternoon'}. This is your Jarvis {briefing_type} briefing. "
                f"Bitcoin is currently trading at ${context.btc_price:,.0f}, {direction} {abs(context.btc_change):.2f}% over the last 24 hours. "
                f"The Fear and Greed index sits at {context.fear_greed_value}, signaling {context.fear_greed_label} sentiment across the market. "
                f"{daily_summary} "
                f"On the news front: {headlines[0] if headlines else 'No major headlines at this time.'}. "
                f"{'Key risk to watch: ' + risk_warnings[0] if risk_warnings else ''} "
                f"Stay disciplined, manage your risk, and have a productive trading session."
            )
        )

    async def generate_news_narration(
        self,
        headline: str,
        content: str,
        summary: str,
    ) -> NewsNarrationData:
        return NewsNarrationData(
            full_script=(
                f"Here is today's story. {headline}. "
                f"{summary} "
                "For the full details, check the source link in your news feed."
            )
        )

    async def generate_insights(self, context: MarketContext, headlines: list[str]) -> MarketInsightData:
        fg_warning = (
            f"Fear & Greed at {context.fear_greed_value} ({context.fear_greed_label}) — "
            + ("historically precedes short-term corrections." if context.fear_greed_value > 70
               else "sentiment remains cautious, watch for capitulation signals.")
        )
        btc_signal = (
            f"BTC {'up' if context.btc_change >= 0 else 'down'} "
            f"{abs(context.btc_change):.2f}% — "
            + ("institutional accumulation pattern via ETF flows." if context.btc_change >= 1.5
               else "consolidating near key levels, directional break pending.")
        )
        return MarketInsightData(
            daily_summary=(
                f"Crypto markets show mixed signals — Bitcoin {'strength' if context.btc_change >= 0 else 'weakness'} "
                f"driven by {'institutional ETF flows contrasts with' if context.btc_change >= 0 else 'macro headwinds align with'} "
                f"macro pressure from sticky inflation. "
                f"Fear & Greed at {context.fear_greed_value} ({context.fear_greed_label}). "
                "Key risk event: ECB decision and upcoming PCE data."
            ),
            risk_warnings=[
                "Fed rate cut timeline pushed to Q4 — macro headwind remains active",
                "CPI at 3.1% above consensus signals inflation may be stickier than expected",
                "ECB rate decision upcoming — potential volatility catalyst",
                fg_warning,
            ],
            opportunity_signals=[
                btc_signal,
                "ETH Pectra upgrade catalyst within 6-week window — protocol event approaching",
                "SOL DEX ecosystem hitting volume milestones — fundamental strength confirmed",
                "BlackRock BUIDL expansion signals accelerating TradFi-DeFi convergence",
            ],
        )
