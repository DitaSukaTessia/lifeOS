import logging

from fastapi import APIRouter, HTTPException

from app.modules.trading.ai_service import get_ai_provider
from app.modules.trading.briefing_service import generate_morning_briefing
from app.modules.trading.history_service import add_history_entry, get_history
from app.modules.trading.news_service import get_news_article
from app.modules.trading.recap_service import generate_recap
from app.modules.trading.schemas import (
    JarvisHistory,
    JarvisHistoryEntry,
    MorningBriefing,
    MarketRecap,
    NewsNarration,
    ReadNewsRequest,
    RecapRequest,
    VoiceAudioMetadata,
)
from app.modules.trading.voice_service import get_voice_provider

from datetime import datetime, timezone

log = logging.getLogger(__name__)

jarvis_router = APIRouter(prefix="/jarvis", tags=["jarvis"])


@jarvis_router.post("/morning-briefing", response_model=MorningBriefing)
async def morning_briefing() -> MorningBriefing:
    return await generate_morning_briefing()


@jarvis_router.post("/recap", response_model=MarketRecap)
async def recap(request: RecapRequest) -> MarketRecap:
    return await generate_recap(recap_type=request.recap_type)


@jarvis_router.post("/read-news", response_model=NewsNarration)
async def read_news(request: ReadNewsRequest) -> NewsNarration:
    article = await get_news_article(request.article_id)

    ai = get_ai_provider()
    narration = await ai.generate_news_narration(
        headline=article.headline,
        content=article.content or "",
        summary=article.summary,
    )

    voice = get_voice_provider()
    audio = await voice.speak(narration.full_script)

    generated_at = datetime.now(timezone.utc).isoformat()

    add_history_entry(
        entry_type="news",
        title=article.headline,
        generated_at=generated_at,
        full_script=narration.full_script,
        ai_provider=ai.provider_name,
        voice_provider=voice.provider_name,
    )

    return NewsNarration(
        article_id=request.article_id,
        headline=article.headline,
        script=narration.full_script,
        voice=VoiceAudioMetadata(
            provider=audio.provider,
            text=audio.text,
            audio_url=audio.audio_url,
            duration_estimate_seconds=audio.duration_estimate_seconds,
        ),
        ai_provider=ai.provider_name,
        voice_provider=voice.provider_name,
    )


@jarvis_router.get("/history", response_model=JarvisHistory)
async def history(entry_type: str | None = None) -> JarvisHistory:
    entries = get_history(entry_type=entry_type)
    return JarvisHistory(
        entries=[
            JarvisHistoryEntry(
                id=e.id,
                entry_type=e.entry_type,
                title=e.title,
                generated_at=e.generated_at,
                script_preview=e.script_preview,
                ai_provider=e.ai_provider,
                voice_provider=e.voice_provider,
            )
            for e in entries
        ],
        total=len(entries),
    )
