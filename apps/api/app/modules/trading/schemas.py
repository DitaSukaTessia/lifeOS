from pydantic import BaseModel


class JournalEntry(BaseModel):
    id: int
    date: str
    symbol: str
    direction: str  # "long" | "short"
    result: str     # "win" | "loss" | "breakeven"
    notes: str
