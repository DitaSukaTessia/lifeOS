from dataclasses import dataclass
from typing import Optional


@dataclass
class CoinData:
    symbol: str
    price_usd: float
    change_24h: float
    market_cap_usd: float


@dataclass
class GlobalMarketData:
    total_market_cap_usd: float
    btc_dominance: float


class CoinGeckoProvider:
    provider_name = "coingecko"

    @property
    def is_available(self) -> bool:
        return True

    async def get_coin(self, symbol: str) -> Optional[CoinData]:
        # Mock data — replace with real CoinGecko API call when key is available
        _mock: dict[str, CoinData] = {
            "BTC": CoinData("BTC", 67_420.00, 2.45, 1_328_000_000_000),
            "ETH": CoinData("ETH", 3_512.80, 1.82, 422_000_000_000),
            "SOL": CoinData("SOL", 176.40, -0.53, 81_000_000_000),
        }
        return _mock.get(symbol)

    async def get_global_market(self) -> Optional[GlobalMarketData]:
        return GlobalMarketData(
            total_market_cap_usd=2_450_000_000_000,
            btc_dominance=54.2,
        )
