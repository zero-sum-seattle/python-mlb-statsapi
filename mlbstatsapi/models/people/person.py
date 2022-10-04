from typing import List, Dict, Union, Any
from mlbstatsapi import MlbObject
from mlbstatsapi.models.stats import Stats
from dataclasses import dataclass, field

@dataclass
class BatSide:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    descritpion: str
        description of the batside
    """
    code: str
    description: str

@dataclass
class PitchHand:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    descritpion: str
        description of the batside
    """
    code: str
    description: str


@dataclass
class PrimaryPosition:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    """
    code: str
    name: str
    type: str
    abbreviation: str

@dataclass
class Person(MlbObject):
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        id number of the person
    full_name: str
        full_name of the person
    """

    id: int
    link: str
    fullName: str
    stats: List[Stats]
    primaryPosition: Union[PrimaryPosition, dict] = field(default_factory=dict)
    pitchHand: Union[PitchHand,dict] = field(default_factory=dict)
    batSide: Union[BatSide,dict] = field(default_factory=dict)
    stats: Union[Stats, dict] = field(default_factory=dict)
    firstName: str = None
    lastName: str = None
    primaryNumber: str = None
    birthDate: str = None
    currentTeam: str = None
    currentAge: int = None
    birthCity: str = None
    birthStateProvince: str = None
    height: str = None
    weight: int = None
    active: bool = None
    useName: str = None
    middleName: str = None
    boxscoreName: str = None
    nickName: str = None
    draftYear: int = None
    mlbDebutDate: str = None
    nameFirstLast: str = None
    nameSlug: str = None
    firstLastName: str = None
    lastFirstName: str = None
    lastInitName: str = None
    initLastName: str = None
    fullFMLName: str = None
    fullLFMName: str = None
    birthCountry: str = None
    pronunciation: str = None
    strikeZoneTop: float = None
    strikeZoneBottom: float = None
    nameTitle: str = None
    gender: str = None
    isPlayer: bool = None
    isVerified: bool = None
    nameMatrilineal: str = None
    deathDate: str = None
    deathCity: str = None
    deathCountry: str = None
    mlb_class: str = "people"

    def __post_init__(self):
        self.primaryPosition = PrimaryPosition(**self.primaryPosition)


     