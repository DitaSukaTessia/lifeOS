import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.redis import close_redis
from app.routers import health
from app.modules.trading import router as trading_router
from app.modules.genshin import router as genshin_router
from app.modules.cyber_lab import router as cyber_lab_router
from app.modules.exploit_lab import router as exploit_lab_router

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(debug=settings.debug)
    log.info("LifeOS API starting")
    _setup_ai_provider()
    _setup_voice_provider()
    yield
    await close_redis()
    log.info("LifeOS API shutdown")


def _setup_voice_provider() -> None:
    from app.modules.trading.voice_service import set_voice_provider
    if settings.elevenlabs_api_key:
        from app.modules.trading.providers.voice.elevenlabs_provider import ElevenLabsProvider
        set_voice_provider(ElevenLabsProvider(api_key=settings.elevenlabs_api_key))
        log.info("Voice provider: ElevenLabs activated")
    elif settings.openai_api_key:
        from app.modules.trading.providers.voice.openai_tts_provider import OpenAITTSProvider
        set_voice_provider(OpenAITTSProvider(api_key=settings.openai_api_key))
        log.info("Voice provider: OpenAI TTS activated")
    else:
        log.info("Voice provider: Browser TTS (set ELEVENLABS_API_KEY to upgrade)")


def _setup_ai_provider() -> None:
    from app.modules.trading.ai_service import set_ai_provider
    if settings.groq_api_key:
        from app.modules.trading.providers.ai.groq_provider import GroqProvider
        set_ai_provider(GroqProvider(api_key=settings.groq_api_key))
        log.info("AI provider: Groq activated")
    elif settings.gemini_api_key:
        from app.modules.trading.providers.ai.gemini_provider import GeminiProvider
        set_ai_provider(GeminiProvider(api_key=settings.gemini_api_key))
        log.info("AI provider: Gemini activated")
    else:
        log.info("AI provider: Mock (set GROQ_API_KEY in .env to activate)")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(trading_router, prefix="/api/v1")
app.include_router(genshin_router, prefix="/api/v1")
app.include_router(cyber_lab_router, prefix="/api/v1")
app.include_router(exploit_lab_router, prefix="/api/v1")
