from dataclasses import dataclass
from typing import Optional


@dataclass
class FearGreedData:
    value: int   # 0–100
    label: str   # "Extreme Fear" | "Fear" | "Neutral" | "Greed" | "Extreme Greed"


class FearGreedProvider:
    provider_name = "alternative_me"

    @property
    def is_available(self) -> bool:
        return True

    async def get_index(self) -> Optional[FearGreedData]:
        # Mock data — replace with https://api.alternative.me/fng/ when ready
        return FearGreedData(value=72, label="Greed")
