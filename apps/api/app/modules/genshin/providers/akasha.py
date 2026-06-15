import httpx

from app.modules.genshin.schemas import (
    Artifact,
    BuildAnalysis,
    BuildStats,
    Character,
    CharacterDetail,
    PlayerStats,
    StatValue,
    Weapon,
)

AKASHA_BASE = "https://akasha.cv/api"

# Akasha stat key → human-readable label
STAT_LABELS: dict[str, str] = {
    "FIGHT_PROP_HP":                    "HP",
    "FIGHT_PROP_HP_PERCENT":            "HP%",
    "FIGHT_PROP_ATTACK":                "ATK",
    "FIGHT_PROP_ATTACK_PERCENT":        "ATK%",
    "FIGHT_PROP_DEFENSE":               "DEF",
    "FIGHT_PROP_DEFENSE_PERCENT":       "DEF%",
    "FIGHT_PROP_CRITICAL":              "CRIT Rate",
    "FIGHT_PROP_CRITICAL_HURT":         "CRIT DMG",
    "FIGHT_PROP_CHARGE_EFFICIENCY":     "Energy Recharge",
    "FIGHT_PROP_ELEMENT_MASTERY":       "Elemental Mastery",
    "FIGHT_PROP_FIRE_ADD_HURT":         "Pyro DMG Bonus",
    "FIGHT_PROP_WATER_ADD_HURT":        "Hydro DMG Bonus",
    "FIGHT_PROP_WIND_ADD_HURT":         "Anemo DMG Bonus",
    "FIGHT_PROP_ELEC_ADD_HURT":         "Electro DMG Bonus",
    "FIGHT_PROP_GRASS_ADD_HURT":        "Dendro DMG Bonus",
    "FIGHT_PROP_ICE_ADD_HURT":          "Cryo DMG Bonus",
    "FIGHT_PROP_ROCK_ADD_HURT":         "Geo DMG Bonus",
    "FIGHT_PROP_PHYSICAL_ADD_HURT":     "Physical DMG Bonus",
    "FIGHT_PROP_HEAL_ADD":              "Healing Bonus",
}

PERCENT_STATS = {
    "FIGHT_PROP_HP_PERCENT",
    "FIGHT_PROP_ATTACK_PERCENT",
    "FIGHT_PROP_DEFENSE_PERCENT",
    "FIGHT_PROP_CRITICAL",
    "FIGHT_PROP_CRITICAL_HURT",
    "FIGHT_PROP_CHARGE_EFFICIENCY",
    "FIGHT_PROP_FIRE_ADD_HURT",
    "FIGHT_PROP_WATER_ADD_HURT",
    "FIGHT_PROP_WIND_ADD_HURT",
    "FIGHT_PROP_ELEC_ADD_HURT",
    "FIGHT_PROP_GRASS_ADD_HURT",
    "FIGHT_PROP_ICE_ADD_HURT",
    "FIGHT_PROP_ROCK_ADD_HURT",
    "FIGHT_PROP_PHYSICAL_ADD_HURT",
    "FIGHT_PROP_HEAL_ADD",
}

SLOT_MAP = {
    "EQUIP_BRACER":   "flower",
    "EQUIP_NECKLACE": "feather",
    "EQUIP_SHOES":    "sands",
    "EQUIP_RING":     "goblet",
    "EQUIP_DRESS":    "circlet",
}


def _format_stat(key: str, value: float) -> StatValue:
    label = STAT_LABELS.get(key, key)
    if key in PERCENT_STATS:
        display = f"{value * 100:.1f}%"
        return StatValue(type=label, value=round(value * 100, 1), display=display)
    return StatValue(type=label, value=round(value), display=str(round(value)))


def _parse_artifact(raw: dict) -> Artifact:
    main_raw = raw.get("mainStat", {})
    main_stat = _format_stat(
        main_raw.get("type", ""),
        main_raw.get("value", 0.0),
    )
    sub_stats = [
        _format_stat(s.get("type", ""), s.get("value", 0.0))
        for s in raw.get("subStats", [])
    ]
    return Artifact(
        slot=SLOT_MAP.get(raw.get("slotKey", ""), raw.get("slotKey", "")),
        set_name=raw.get("setName", "Unknown"),
        rarity=raw.get("rarity", 4),
        level=raw.get("level", 0),
        main_stat=main_stat,
        sub_stats=sub_stats,
    )


def _parse_weapon(raw: dict | None) -> Weapon | None:
    if not raw:
        return None
    return Weapon(
        name=raw.get("name", "Unknown"),
        rarity=raw.get("rarity", 1),
        level=raw.get("level", 1),
        refinement=raw.get("refinement", 1),
    )


def _build_analysis(stats: BuildStats) -> BuildAnalysis:
    cr = stats.crit_rate
    cd = stats.crit_dmg
    crit_score = round(cr * 2 + cd, 1)
    ratio = f"{cr:.1f}:{cd:.1f}"

    if crit_score >= 220:
        rating = "S"
    elif crit_score >= 180:
        rating = "A"
    elif crit_score >= 140:
        rating = "B"
    else:
        rating = "C"

    return BuildAnalysis(crit_score=crit_score, crit_ratio=ratio, rating=rating)


async def fetch_player(uid: str) -> PlayerStats:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{AKASHA_BASE}/user/{uid}")
        response.raise_for_status()
        data = response.json()

    owner = data.get("owner", {})
    builds = data.get("builds", [])

    characters: list[Character] = []
    for build in builds:
        char_data = build.get("character", {})
        characters.append(
            Character(
                id=char_data.get("id", 0),
                name=char_data.get("name", "Unknown"),
                element=char_data.get("element", ""),
                rarity=char_data.get("rarity", 4),
                level=build.get("level", 1),
                constellation=build.get("constellation", 0),
                weapon=_parse_weapon(build.get("weapon")),
            )
        )

    return PlayerStats(
        uid=uid,
        nickname=owner.get("nickname", uid),
        level=owner.get("adventureRank", 0),
        world_level=owner.get("worldLevel", 0),
        signature=owner.get("signature", ""),
        achievements=owner.get("achievements", 0),
        characters=characters,
    )


async def fetch_character_detail(uid: str, character_id: int) -> CharacterDetail:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{AKASHA_BASE}/user/{uid}/builds/{character_id}")
        response.raise_for_status()
        data = response.json()

    build = data.get("build", data)  # some endpoints wrap in "build"
    char_data = build.get("character", {})

    # Parse calculated stats block Akasha provides
    calc = build.get("calculatedStats", {})
    stats = BuildStats(
        crit_rate=round(calc.get("critRate", {}).get("value", 0.0) * 100, 1),
        crit_dmg=round(calc.get("critDmg", {}).get("value", 0.0) * 100, 1),
        atk=round(calc.get("atk", {}).get("value", 0.0)),
        hp=round(calc.get("hp", {}).get("value", 0.0)),
        defense=round(calc.get("def", {}).get("value", 0.0)),
        energy_recharge=round(calc.get("energyRecharge", {}).get("value", 0.0) * 100, 1),
        elemental_mastery=round(calc.get("elementalMastery", {}).get("value", 0.0)),
    )

    artifacts = [_parse_artifact(a) for a in build.get("artifacts", [])]

    return CharacterDetail(
        id=char_data.get("id", character_id),
        name=char_data.get("name", "Unknown"),
        element=char_data.get("element", ""),
        rarity=char_data.get("rarity", 4),
        level=build.get("level", 1),
        constellation=build.get("constellation", 0),
        weapon=_parse_weapon(build.get("weapon")),
        artifacts=artifacts,
        stats=stats,
        analysis=_build_analysis(stats),
    )
