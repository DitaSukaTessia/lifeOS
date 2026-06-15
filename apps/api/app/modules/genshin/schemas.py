from pydantic import BaseModel


class Weapon(BaseModel):
    name: str
    rarity: int
    level: int
    refinement: int
    icon: str = ""


class Character(BaseModel):
    id: int
    name: str
    element: str
    rarity: int
    level: int
    constellation: int
    weapon: Weapon | None = None
    icon: str = ""
    friendship: int = 0


class SpiralAbyss(BaseModel):
    floor: int
    chamber: int
    stars: int


class ImaginariumTheater(BaseModel):
    act: int
    stars: int


class StygianOnslaught(BaseModel):
    seconds: int


class PlayerStats(BaseModel):
    uid: str
    nickname: str
    level: int
    world_level: int
    signature: str
    achievements: int
    characters: list[Character]
    spiral_abyss: SpiralAbyss | None = None
    imaginarium_theater: ImaginariumTheater | None = None
    stygian_onslaught: StygianOnslaught | None = None


# --- Character Detail ---

class StatValue(BaseModel):
    type: str
    value: float
    display: str


class Artifact(BaseModel):
    slot: str
    set_name: str
    rarity: int
    level: int
    main_stat: StatValue
    sub_stats: list[StatValue]
    icon: str = ""


class BuildStats(BaseModel):
    crit_rate: float
    crit_dmg: float
    atk: float
    hp: float
    defense: float
    energy_recharge: float
    elemental_mastery: float


class BuildAnalysis(BaseModel):
    crit_score: float
    crit_ratio: str
    rating: str


class Talent(BaseModel):
    label: str   # "Normal Attack" | "Elemental Skill" | "Elemental Burst"
    icon: str
    level: int


class ConstellationSlot(BaseModel):
    icon: str
    unlocked: bool


class CharacterDetail(BaseModel):
    id: int
    name: str
    element: str
    rarity: int
    level: int
    constellation: int
    weapon: Weapon | None
    artifacts: list[Artifact]
    stats: BuildStats
    analysis: BuildAnalysis
    icon: str = ""
    gacha_icon: str = ""
    friendship: int = 0
    talents: list[Talent] = []
    constellations: list[ConstellationSlot] = []
    full_stats: list[StatValue] = []
