from fastapi import APIRouter

from app.modules.trading.schemas import JournalEntry
from app.modules.trading.service import get_journal_entries

router = APIRouter(prefix="/trading", tags=["trading"])


@router.get("/journal", response_model=list[JournalEntry])
async def journal() -> list[JournalEntry]:
    return await get_journal_entries()
