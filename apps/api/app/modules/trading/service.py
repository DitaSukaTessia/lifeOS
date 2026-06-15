from app.modules.trading.schemas import JournalEntry


async def get_journal_entries() -> list[JournalEntry]:
    # No persistence yet — returns empty list
    # Future: query database for entries by user/date range
    return []
