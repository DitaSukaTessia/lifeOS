import asyncio

from app.modules.trading.providers.coingecko import CoinGeckoProvider, CoinData
from app.modules.trading.providers.fear_greed import FearGreedProvider
from app.modules.trading.schemas import CoinMetric, FearGreedMetric, MarketOverview


async def get_market_overview() -> MarketOverview:
    coingecko = CoinGeckoProvider()
    fg_provider = FearGreedProvider()

    btc_r, eth_r, sol_r, global_r, fg_r = await asyncio.gather(
        coingecko.get_coin("BTC"),
        coingecko.get_coin("ETH"),
        coingecko.get_coin("SOL"),
        coingecko.get_global_market(),
        fg_provider.get_index(),
        return_exceptions=True,
    )

    def _coin(result: object, fallback: str) -> CoinMetric:
        if isinstance(result, Exception) or result is None:
            return CoinMetric(symbol=fallback, price_usd=0.0, change_24h=0.0)
        data: CoinData = result  # type: ignore[assignment]
        return CoinMetric(symbol=data.symbol, price_usd=data.price_usd, change_24h=data.change_24h)

    fear_greed = (
        FearGreedMetric(value=fg_r.value, label=fg_r.label)  # type: ignore[union-attr]
        if fg_r and not isinstance(fg_r, Exception)
        else FearGreedMetric(value=0, label="Unknown")
    )

    total_mcap = global_r.total_market_cap_usd if global_r and not isinstance(global_r, Exception) else 0.0  # type: ignore[union-attr]
    btc_dom = global_r.btc_dominance if global_r and not isinstance(global_r, Exception) else 0.0  # type: ignore[union-attr]

    return MarketOverview(
        btc=_coin(btc_r, "BTC"),
        eth=_coin(eth_r, "ETH"),
        sol=_coin(sol_r, "SOL"),
        total_market_cap_usd=total_mcap,
        btc_dominance=btc_dom,
        fear_greed=fear_greed,
        provider_status={
            coingecko.provider_name: coingecko.is_available,
            fg_provider.provider_name: fg_provider.is_available,
        },
    )
