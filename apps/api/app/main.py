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
    yield
    await close_redis()
    log.info("LifeOS API shutdown")


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
