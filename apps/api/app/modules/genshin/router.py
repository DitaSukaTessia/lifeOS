from fastapi import APIRouter, HTTPException

from app.modules.genshin.schemas import CharacterDetail, PlayerStats
from app.modules.genshin.service import GenshinServiceError, get_character_detail, get_player_stats

router = APIRouter(prefix="/genshin", tags=["genshin"])


@router.get("/player/{uid}", response_model=PlayerStats)
async def player(uid: str) -> PlayerStats:
    try:
        return await get_player_stats(uid)
    except GenshinServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/player/{uid}/character/{character_id}", response_model=CharacterDetail)
async def character_detail(uid: str, character_id: int) -> CharacterDetail:
    try:
        return await get_character_detail(uid, character_id)
    except GenshinServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))
