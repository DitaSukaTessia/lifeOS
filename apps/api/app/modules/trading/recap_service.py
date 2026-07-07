import asyncio
from datetime import datetime, timezone
from typing import Literal

from app.modules.trading.ai_service import get_ai_provider
from app.modules.trading.calendar_service import get_economic_calendar
from app.modules.trading.history_service import add_history_entry
from app.modules.trading.insight_service import generate_insights
from app.modules.trading.market_service import get_market_overview
from app.modules.trading.news_service import get_news_feed
from app.modules.trading.providers.ai.base_ai_provider import MarketContext
from app.modules.trading.schemas import MarketRecap, VoiceAudioMetadata
from app.modules.trading.voice_service import get_voice_provider

RecapType = Literal["morning", "midday", "evening"]

_RECAP_TITLES = {
    "morning": "Morning Recap",
    "midday": "Midday Recap",
    "evening": "Evening Recap",
}


async def generate_recap(recap_type: RecapType = "morning") -> MarketRecap:
    overview, feed, calendar, insight = await asyncio.gather(
        get_market_overview(),
        get_news_feed(page=1, limit=3),
        get_economic_calendar(),
        generate_insights(),
    )

    context = MarketContext(
        btc_price=overview.btc.price_usd,
        btc_change=overview.btc.change_24h,
        fear_greed_value=overview.fear_greed.value,
        fear_greed_label=overview.fear_greed.label,
    )
    headlines = [a.headline for a in feed.articles]
    calendar_events = [
        f"{e.title} ({e.country}, {e.impact} impact)"
        for e in calendar.events[:3]
    ]

    ai = get_ai_provider()
    script_data = await ai.generate_briefing_script(
        context=context,
        headlines=headlines,
        calendar_events=calendar_events,
        daily_summary=insight.daily_summary,
        risk_warnings=insight.risk_warnings,
        briefing_type=recap_type,
    )

    voice = get_voice_provider()
    audio = await voice.speak(script_data.full_script)

    generated_at = datetime.now(timezone.utc).isoformat()
    title = _RECAP_TITLES[recap_type]

    add_history_entry(
        entry_type="recap",
        title=title,
        generated_at=generated_at,
        full_script=script_data.full_script,
        ai_provider=ai.provider_name,
        voice_provider=voice.provider_name,
    )

    return MarketRecap(
        recap_type=recap_type,
        generated_at=generated_at,
        script=script_data.full_script,
        voice=VoiceAudioMetadata(
            provider=audio.provider,
            text=audio.text,
            audio_url=audio.audio_url,
            duration_estimate_seconds=audio.duration_estimate_seconds,
        ),
        ai_provider=ai.provider_name,
        voice_provider=voice.provider_name,
    )
