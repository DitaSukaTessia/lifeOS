import httpx

from app.modules.genshin.providers import enka
from app.modules.genshin.schemas import CharacterDetail, PlayerStats


class GenshinServiceError(Exception):
    pass


async def _call(coro):
    try:
        return await coro
    except httpx.HTTPStatusError as e:
        status = e.response.status_code if e.response is not None else 0
        if status == 404:
            raise GenshinServiceError("UID not found on Enka") from e
        raise GenshinServiceError(f"Enka provider error (HTTP {status})") from e
    except httpx.RequestError as e:
        raise GenshinServiceError("Failed to reach Enka Network") from e


async def get_player_stats(uid: str) -> PlayerStats:
    return await _call(enka.fetch_player(uid))


async def get_character_detail(uid: str, character_id: int) -> CharacterDetail:
    return await _call(enka.fetch_character_detail(uid, character_id))
