from app.modules.trading.providers.economic_calendar import EconomicCalendarProvider
from app.modules.trading.schemas import EconomicCalendar, EconomicEvent


async def get_economic_calendar() -> EconomicCalendar:
    provider = EconomicCalendarProvider()
    events_data = await provider.get_events()
    events = [
        EconomicEvent(
            id=e.id,
            title=e.title,
            country=e.country,
            impact=e.impact,  # type: ignore[arg-type]
            scheduled_at=e.scheduled_at,
            actual=e.actual,
            forecast=e.forecast,
            previous=e.previous,
        )
        for e in events_data
    ]
    return EconomicCalendar(events=events)
