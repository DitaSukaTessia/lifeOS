from dataclasses import dataclass
from typing import Optional


@dataclass
class EconomicEventData:
    id: str
    title: str
    country: str
    impact: str  # "low" | "medium" | "high"
    scheduled_at: str  # ISO 8601
    actual: Optional[str] = None
    forecast: Optional[str] = None
    previous: Optional[str] = None


_MOCK_EVENTS: list[EconomicEventData] = [
    EconomicEventData(
        id="1",
        title="Initial Jobless Claims",
        country="US",
        impact="medium",
        scheduled_at="2026-06-19T12:30:00Z",
        forecast="215K",
        previous="222K",
    ),
    EconomicEventData(
        id="2",
        title="Philadelphia Fed Manufacturing Index",
        country="US",
        impact="medium",
        scheduled_at="2026-06-19T12:30:00Z",
        forecast="5.2",
        previous="4.5",
    ),
    EconomicEventData(
        id="3",
        title="ECB Interest Rate Decision",
        country="EU",
        impact="high",
        scheduled_at="2026-06-20T11:15:00Z",
        forecast="3.75%",
        previous="3.75%",
    ),
    EconomicEventData(
        id="4",
        title="UK Retail Sales (MoM)",
        country="GB",
        impact="medium",
        scheduled_at="2026-06-20T06:00:00Z",
        forecast="0.3%",
        previous="-0.1%",
    ),
    EconomicEventData(
        id="5",
        title="Bank of Japan Policy Rate",
        country="JP",
        impact="high",
        scheduled_at="2026-06-20T03:00:00Z",
        forecast="0.25%",
        previous="0.25%",
    ),
    EconomicEventData(
        id="6",
        title="US Core PCE Price Index (YoY)",
        country="US",
        impact="high",
        scheduled_at="2026-06-27T12:30:00Z",
        forecast="2.6%",
        previous="2.8%",
    ),
]


class EconomicCalendarProvider:
    provider_name = "mock_calendar"

    @property
    def is_available(self) -> bool:
        return True

    async def get_events(self) -> list[EconomicEventData]:
        return _MOCK_EVENTS
