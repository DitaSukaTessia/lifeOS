"""
In-memory briefing/recap/news history store.

Intentionally ephemeral — survives only while the server is running.
Database persistence is a later milestone.
"""
import uuid
from collections import deque
from dataclasses import dataclass
from typing import Deque

_MAX_ENTRIES = 50


@dataclass
class HistoryEntry:
    id: str
    entry_type: str       # "briefing" | "recap" | "news"
    title: str
    generated_at: str     # ISO 8601 UTC
    script_preview: str   # first 150 characters
    full_script: str
    ai_provider: str
    voice_provider: str


_history: Deque[HistoryEntry] = deque(maxlen=_MAX_ENTRIES)


def add_history_entry(
    entry_type: str,
    title: str,
    generated_at: str,
    full_script: str,
    ai_provider: str,
    voice_provider: str,
) -> HistoryEntry:
    entry = HistoryEntry(
        id=str(uuid.uuid4()),
        entry_type=entry_type,
        title=title,
        generated_at=generated_at,
        script_preview=full_script[:150].rstrip() + ("…" if len(full_script) > 150 else ""),
        full_script=full_script,
        ai_provider=ai_provider,
        voice_provider=voice_provider,
    )
    _history.appendleft(entry)
    return entry


def get_history(entry_type: str | None = None) -> list[HistoryEntry]:
    if entry_type is None:
        return list(_history)
    return [e for e in _history if e.entry_type == entry_type]
