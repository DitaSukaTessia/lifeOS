import asyncio

import httpx

from app.modules.genshin.schemas import (
    Artifact,
    BuildAnalysis,
    BuildStats,
    Character,
    CharacterDetail,
    ConstellationSlot,
    ImaginariumTheater,
    PlayerStats,
    SpiralAbyss,
    StatValue,
    StygianOnslaught,
    Talent,
    Weapon,
)

ENKA_BASE = "https://enka.network/api"
ENKA_ASSETS = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/gi"
ENKA_CDN = "https://enka.network"

ELEMENT_MAP = {
    "Fire":     "Pyro",
    "Water":    "Hydro",
    "Wind":     "Anemo",
    "Electric": "Electro",
    "Grass":    "Dendro",
    "Ice":      "Cryo",
    "Rock":     "Geo",
}

SLOT_MAP = {
    "EQUIP_BRACER":   "flower",
    "EQUIP_NECKLACE": "feather",
    "EQUIP_SHOES":    "sands",
    "EQUIP_RING":     "goblet",
    "EQUIP_DRESS":    "circlet",
}

TALENT_LABELS = ["Normal Attack", "Elemental Skill", "Elemental Burst"]

# fightPropMap string keys → (label, is_percent)
FULL_STAT_MAP: list[tuple[str, str, bool]] = [
    ("2000", "HP",                  False),
    ("2001", "ATK",                 False),
    ("2002", "DEF",                 False),
    ("20",   "CRIT Rate",           True),
    ("22",   "CRIT DMG",            True),
    ("23",   "Energy Recharge",     True),
    ("28",   "Elemental Mastery",   False),
    ("26",   "Healing Bonus",       True),
    ("40",   "Pyro DMG Bonus",      True),
    ("41",   "Hydro DMG Bonus",     True),
    ("42",   "Dendro DMG Bonus",    True),
    ("43",   "Electro DMG Bonus",   True),
    ("44",   "Anemo DMG Bonus",     True),
    ("45",   "Geo DMG Bonus",       True),
    ("46",   "Cryo DMG Bonus",      True),
    ("50",   "Physical DMG Bonus",  True),
]

PERCENT_PROPS = {
    "FIGHT_PROP_HP_PERCENT", "FIGHT_PROP_ATTACK_PERCENT", "FIGHT_PROP_DEFENSE_PERCENT",
    "FIGHT_PROP_CRITICAL", "FIGHT_PROP_CRITICAL_HURT", "FIGHT_PROP_CHARGE_EFFICIENCY",
    "FIGHT_PROP_FIRE_ADD_HURT", "FIGHT_PROP_WATER_ADD_HURT", "FIGHT_PROP_WIND_ADD_HURT",
    "FIGHT_PROP_ELEC_ADD_HURT", "FIGHT_PROP_GRASS_ADD_HURT", "FIGHT_PROP_ICE_ADD_HURT",
    "FIGHT_PROP_ROCK_ADD_HURT", "FIGHT_PROP_PHYSICAL_ADD_HURT", "FIGHT_PROP_HEAL_ADD",
}

PROP_LABELS = {
    "FIGHT_PROP_HP":                "HP",
    "FIGHT_PROP_HP_PERCENT":        "HP%",
    "FIGHT_PROP_ATTACK":            "ATK",
    "FIGHT_PROP_ATTACK_PERCENT":    "ATK%",
    "FIGHT_PROP_DEFENSE":           "DEF",
    "FIGHT_PROP_DEFENSE_PERCENT":   "DEF%",
    "FIGHT_PROP_CRITICAL":          "CRIT Rate",
    "FIGHT_PROP_CRITICAL_HURT":     "CRIT DMG",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "Energy Recharge",
    "FIGHT_PROP_ELEMENT_MASTERY":   "Elemental Mastery",
    "FIGHT_PROP_FIRE_ADD_HURT":     "Pyro DMG Bonus",
    "FIGHT_PROP_WATER_ADD_HURT":    "Hydro DMG Bonus",
    "FIGHT_PROP_WIND_ADD_HURT":     "Anemo DMG Bonus",
    "FIGHT_PROP_ELEC_ADD_HURT":     "Electro DMG Bonus",
    "FIGHT_PROP_GRASS_ADD_HURT":    "Dendro DMG Bonus",
    "FIGHT_PROP_ICE_ADD_HURT":      "Cryo DMG Bonus",
    "FIGHT_PROP_ROCK_ADD_HURT":     "Geo DMG Bonus",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "Physical DMG Bonus",
    "FIGHT_PROP_HEAL_ADD":          "Healing Bonus",
    "FIGHT_PROP_BASE_ATTACK":       "Base ATK",
}


class EnkaAssets:
    def __init__(self, avatars: dict, weapons: dict, relics: dict, locs: dict):
        self._avatars = avatars
        self._weapons = weapons
        self._relic_items = relics.get("Items", {})
        self._relic_sets = relics.get("Sets", {})
        self._locs = locs.get("en", {})

    def _loc(self, hash_val) -> str:
        return self._locs.get(str(hash_val), "Unknown")

    def _cdn(self, path: str) -> str:
        return f"{ENKA_CDN}{path}"

    def char_name(self, avatar_id: int) -> str:
        av = self._avatars.get(str(avatar_id), {})
        return self._loc(av.get("NameTextMapHash", ""))

    def char_element(self, avatar_id: int) -> str:
        av = self._avatars.get(str(avatar_id), {})
        return ELEMENT_MAP.get(av.get("Element", ""), av.get("Element", ""))

    def char_rarity(self, avatar_id: int) -> int:
        av = self._avatars.get(str(avatar_id), {})
        return 5 if av.get("QualityType") == "QUALITY_ORANGE" else 4

    def char_icon(self, avatar_id: int, costume_id: int | None = None) -> str:
        av = self._avatars.get(str(avatar_id), {})
        if costume_id:
            costume = av.get("Costumes", {}).get(str(costume_id), {})
            if costume.get("Icon"):
                return self._cdn(costume["Icon"])
        side = av.get("SideIconName", "")
        # /ui/UI_AvatarIcon_Side_Yoimiya.png → /ui/UI_AvatarIcon_Yoimiya.png
        icon = side.replace("_Side_", "_")
        return self._cdn(icon) if icon else ""

    def char_gacha_icon(self, avatar_id: int, costume_id: int | None = None) -> str:
        av = self._avatars.get(str(avatar_id), {})
        if costume_id:
            costume = av.get("Costumes", {}).get(str(costume_id), {})
            if costume.get("Art"):
                return self._cdn(costume["Art"])
        side = av.get("SideIconName", "")
        # /ui/UI_AvatarIcon_Side_Yoimiya.png → /ui/UI_Gacha_AvatarImg_Yoimiya.png
        name = side.replace("/ui/UI_AvatarIcon_Side_", "").replace(".png", "")
        return self._cdn(f"/ui/UI_Gacha_AvatarImg_{name}.png") if name else ""

    def char_skill_order(self, avatar_id: int) -> list[int]:
        av = self._avatars.get(str(avatar_id), {})
        return av.get("SkillOrder", [])

    def char_skill_icons(self, avatar_id: int) -> dict[int, str]:
        av = self._avatars.get(str(avatar_id), {})
        return {int(k): self._cdn(v) for k, v in av.get("Skills", {}).items()}

    def char_const_icons(self, avatar_id: int) -> list[str]:
        av = self._avatars.get(str(avatar_id), {})
        return [self._cdn(c) for c in av.get("Consts", [])]

    def weapon_name(self, item_id: int) -> str:
        wp = self._weapons.get(str(item_id), {})
        return self._loc(wp.get("NameTextMapHash", ""))

    def weapon_rarity(self, item_id: int) -> int:
        return self._weapons.get(str(item_id), {}).get("Rarity", 1)

    def weapon_icon(self, item_id: int) -> str:
        wp = self._weapons.get(str(item_id), {})
        return self._cdn(wp.get("AwakenIcon") or wp.get("Icon", ""))

    def artifact_set_name(self, item_id: int) -> str:
        item = self._relic_items.get(str(item_id), {})
        set_id = item.get("SetId")
        if set_id is None:
            return "Unknown"
        name_hash = self._relic_sets.get(str(set_id), {}).get("Name", "")
        return self._loc(name_hash)

    def artifact_icon(self, item_id: int) -> str:
        item = self._relic_items.get(str(item_id), {})
        return self._cdn(item.get("Icon", ""))


async def _fetch_assets(client: httpx.AsyncClient) -> EnkaAssets:
    avatars_r, weapons_r, relics_r, locs_r = await asyncio.gather(
        client.get(f"{ENKA_ASSETS}/avatars.json"),
        client.get(f"{ENKA_ASSETS}/weapons.json"),
        client.get(f"{ENKA_ASSETS}/relics.json"),
        client.get(f"{ENKA_ASSETS}/locs.json"),
    )
    return EnkaAssets(avatars_r.json(), weapons_r.json(), relics_r.json(), locs_r.json())


def _format_stat(prop_id: str, value: float) -> StatValue:
    label = PROP_LABELS.get(prop_id, prop_id)
    if prop_id in PERCENT_PROPS:
        display = f"{value:.1f}%"
        return StatValue(type=label, value=round(value, 1), display=display)
    return StatValue(type=label, value=round(value), display=str(round(value)))


def _parse_weapon(equip: dict, assets: EnkaAssets) -> Weapon | None:
    item_id = equip.get("itemId", 0)
    wp = equip.get("weapon", {})
    affix_map = wp.get("affixMap", {})
    refinement = (list(affix_map.values())[0] + 1) if affix_map else 1
    return Weapon(
        name=assets.weapon_name(item_id),
        rarity=assets.weapon_rarity(item_id),
        level=wp.get("level", 1),
        refinement=refinement,
        icon=assets.weapon_icon(item_id),
    )


def _parse_artifact(equip: dict, assets: EnkaAssets) -> Artifact:
    item_id = equip.get("itemId", 0)
    flat = equip.get("flat", {})
    rel = equip.get("reliquary", {})
    main_raw = flat.get("reliquaryMainstat", {})
    main_stat = _format_stat(main_raw.get("mainPropId", ""), main_raw.get("statValue", 0.0))
    sub_stats = [
        _format_stat(s.get("appendPropId", ""), s.get("statValue", 0.0))
        for s in flat.get("reliquarySubstats", [])
    ]
    return Artifact(
        slot=SLOT_MAP.get(flat.get("equipType", ""), flat.get("equipType", "")),
        set_name=assets.artifact_set_name(item_id),
        rarity=flat.get("rankLevel", 4),
        level=max(0, rel.get("level", 1) - 1),
        main_stat=main_stat,
        sub_stats=sub_stats,
        icon=assets.artifact_icon(item_id),
    )


def _parse_build_stats(fight_prop: dict) -> BuildStats:
    def get(key: str) -> float:
        return fight_prop.get(key, 0.0)

    return BuildStats(
        hp=round(get("2000")),
        atk=round(get("2001")),
        defense=round(get("2002")),
        crit_rate=round(get("20") * 100, 1),
        crit_dmg=round(get("22") * 100, 1),
        energy_recharge=round(get("23") * 100, 1),
        elemental_mastery=round(get("28")),
    )


def _parse_full_stats(fight_prop: dict) -> list[StatValue]:
    result = []
    for key, label, is_percent in FULL_STAT_MAP:
        raw = fight_prop.get(key, 0.0)
        if is_percent:
            value = round(raw * 100, 1)
            result.append(StatValue(type=label, value=value, display=f"{value:.1f}%"))
        else:
            value = round(raw)
            result.append(StatValue(type=label, value=value, display=str(value)))
    return result


def _parse_talents(
    avatar_id: int,
    skill_level_map: dict[str, int],
    assets: EnkaAssets,
) -> list[Talent]:
    order = assets.char_skill_order(avatar_id)
    icons = assets.char_skill_icons(avatar_id)
    talents = []
    for i, skill_id in enumerate(order[:3]):
        level = skill_level_map.get(str(skill_id), 1)
        label = TALENT_LABELS[i] if i < len(TALENT_LABELS) else f"Skill {i + 1}"
        icon = icons.get(skill_id, "")
        talents.append(Talent(label=label, icon=icon, level=level))
    return talents


def _parse_constellations(
    avatar_id: int,
    talent_id_list: list[int],
    assets: EnkaAssets,
) -> list[ConstellationSlot]:
    const_icons = assets.char_const_icons(avatar_id)
    unlocked_count = len(talent_id_list)
    return [
        ConstellationSlot(icon=icon, unlocked=(i < unlocked_count))
        for i, icon in enumerate(const_icons)
    ]


def _build_analysis(stats: BuildStats) -> BuildAnalysis:
    cr = stats.crit_rate
    cd = stats.crit_dmg
    crit_score = round(cr * 2 + cd, 1)
    if crit_score >= 220:
        rating = "S"
    elif crit_score >= 180:
        rating = "A"
    elif crit_score >= 140:
        rating = "B"
    else:
        rating = "C"
    return BuildAnalysis(crit_score=crit_score, crit_ratio=f"{cr:.1f}:{cd:.1f}", rating=rating)


async def fetch_player(uid: str) -> PlayerStats:
    async with httpx.AsyncClient(timeout=15.0) as client:
        profile_r, assets = await asyncio.gather(
            client.get(f"{ENKA_BASE}/uid/{uid}"),
            _fetch_assets(client),
        )
        profile_r.raise_for_status()

    data = profile_r.json()
    info = data.get("playerInfo", {})

    characters: list[Character] = []
    for av in data.get("avatarInfoList", []):
        avatar_id = av.get("avatarId", 0)
        prop_map = av.get("propMap", {})
        level = int(prop_map.get("4001", {}).get("val", 1))
        constellation = len(av.get("talentIdList", []))
        friendship = av.get("fetterInfo", {}).get("expLevel", 0)
        costume_id = av.get("costumeId")

        weapon: Weapon | None = None
        for equip in av.get("equipList", []):
            if equip.get("flat", {}).get("itemType") == "ITEM_WEAPON":
                weapon = _parse_weapon(equip, assets)
                break

        characters.append(Character(
            id=avatar_id,
            name=assets.char_name(avatar_id),
            element=assets.char_element(avatar_id),
            rarity=assets.char_rarity(avatar_id),
            level=level,
            constellation=constellation,
            weapon=weapon,
            icon=assets.char_icon(avatar_id, costume_id),
            friendship=friendship,
        ))

    spiral_abyss = None
    if "towerFloorIndex" in info:
        spiral_abyss = SpiralAbyss(
            floor=info["towerFloorIndex"],
            chamber=info.get("towerLevelIndex", 0),
            stars=info.get("towerStarIndex", 0),
        )

    imaginarium_theater = None
    if "theaterActIndex" in info:
        imaginarium_theater = ImaginariumTheater(
            act=info["theaterActIndex"],
            stars=info.get("theaterStarIndex", 0),
        )

    stygian_onslaught = None
    if "stygianSeconds" in info:
        stygian_onslaught = StygianOnslaught(
            seconds=info["stygianSeconds"],
        )

    return PlayerStats(
        uid=uid,
        nickname=info.get("nickname", uid),
        level=info.get("level", 0),
        world_level=info.get("worldLevel", 0),
        signature=info.get("signature", ""),
        achievements=info.get("finishAchievementNum", 0),
        characters=characters,
        spiral_abyss=spiral_abyss,
        imaginarium_theater=imaginarium_theater,
        stygian_onslaught=stygian_onslaught,
    )


async def fetch_character_detail(uid: str, character_id: int) -> CharacterDetail:
    async with httpx.AsyncClient(timeout=15.0) as client:
        profile_r, assets = await asyncio.gather(
            client.get(f"{ENKA_BASE}/uid/{uid}"),
            _fetch_assets(client),
        )
        profile_r.raise_for_status()

    data = profile_r.json()
    av_list = data.get("avatarInfoList", [])

    target = next((a for a in av_list if a.get("avatarId") == character_id), None)
    if target is None:
        raise httpx.HTTPStatusError(
            f"Character {character_id} not in showcase",
            request=None,  # type: ignore[arg-type]
            response=None,  # type: ignore[arg-type]
        )

    avatar_id = target["avatarId"]
    prop_map = target.get("propMap", {})
    level = int(prop_map.get("4001", {}).get("val", 1))
    constellation = len(target.get("talentIdList", []))
    friendship = target.get("fetterInfo", {}).get("expLevel", 0)
    fight_prop = target.get("fightPropMap", {})
    costume_id = target.get("costumeId")

    weapon: Weapon | None = None
    artifacts: list[Artifact] = []
    for equip in target.get("equipList", []):
        item_type = equip.get("flat", {}).get("itemType")
        if item_type == "ITEM_WEAPON":
            weapon = _parse_weapon(equip, assets)
        elif item_type == "ITEM_RELIQUARY":
            artifacts.append(_parse_artifact(equip, assets))

    stats = _parse_build_stats(fight_prop)

    return CharacterDetail(
        id=avatar_id,
        name=assets.char_name(avatar_id),
        element=assets.char_element(avatar_id),
        rarity=assets.char_rarity(avatar_id),
        level=level,
        constellation=constellation,
        weapon=weapon,
        artifacts=artifacts,
        stats=stats,
        analysis=_build_analysis(stats),
        icon=assets.char_icon(avatar_id, costume_id),
        gacha_icon=assets.char_gacha_icon(avatar_id, costume_id),
        friendship=friendship,
        talents=_parse_talents(avatar_id, target.get("skillLevelMap", {}), assets),
        constellations=_parse_constellations(avatar_id, target.get("talentIdList", []), assets),
        full_stats=_parse_full_stats(fight_prop),
    )
