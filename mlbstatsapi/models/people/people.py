from typing import List, Dict, Union, Any, Optional
from dataclasses import dataclass, field, InitVar

from .attributes import PitchHand, Position, BatSide, Status

@dataclass
class Person:
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
    mlb_class: str = "people"
    primaryposition: Union[Position, Dict[str, Any]] = field(default_factory=dict)
    pitchhand: Union[PitchHand, Dict[str, Any]] = field(default_factory=dict)
    batside: Union[BatSide, Dict[str, Any]] = field(default_factory=dict)
    fullname: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    primarynumber: Optional[str] = None
    birthdate: Optional[str] = None
    currentteam: Optional[str] = None
    currentage: Optional[str] = None
    birthcity: Optional[str] = None
    birthstateprovince: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    usename: Optional[str] = None
    middlename: Optional[str] = None
    boxscorename: Optional[str] = None
    nickname: Optional[str] = None
    draftyear: Optional[int] = None
    mlbdebutdate: Optional[str] = None
    namefirstlast: Optional[str] = None
    nameslug: Optional[str] = None
    firstlastname: Optional[str] = None
    lastfirstname: Optional[str] = None
    lastinitname: Optional[str] = None
    initlastname: Optional[str] = None
    fullfmlname: Optional[str] = None
    fulllfmname: Optional[str] = None
    birthcountry: Optional[str] = None
    pronunciation: Optional[str] = None
    strikezonetop: Optional[float] = None
    strikezonebottom: Optional[float] = None
    nametitle: Optional[str] = None
    gender: Optional[str] = None
    isplayer: Optional[bool] = None
    isverified: Optional[bool] = None
    namematrilineal: Optional[str] = None
    deathdate: Optional[str] = None
    deathcity: Optional[str] = None
    deathcountry: Optional[str] = None

    def __post_init__(self):
        self.primaryposition = Position(**self.primaryposition) if self.primaryposition else self.primaryposition
        self.pitchhand = PitchHand(**self.pitchhand) if self.pitchhand else self.pitchhand
        self.batside = BatSide(**self.batside) if self.batside else self.batside

@dataclass(kw_only=True)
class Player(Person):
    """
    A class to represent a Player.

    Attributes
    ----------
    jerseyNumber : str
        id number of the person
    status : 
        Status of the player
    parentTeamId : int
        parent team id
    """
    jerseynumber: str
    parentteamid: int
    position: InitVar[dict]
    status: Union[Status, dict]

    def __post_init__(self, position: dict):
        self.primaryposition = Position(**position)

@dataclass(kw_only=True)
class Coach(Person):
    """
    A class to represent a Player.

    Attributes
    ----------
    jerseyNumber : str
        id number of the person
    job : str
        job of the coach
    jobId : str
        job id of the coach
    title : str
        title of the coach
    parentTeamId : int
    """
    jerseynumber: str
    job: str
    jobid: str
    title: str



