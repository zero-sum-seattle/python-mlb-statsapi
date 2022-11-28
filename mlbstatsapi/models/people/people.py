from dataclasses import dataclass, field, InitVar
from typing import List, Union, Dict, Any, Optional

from .attributes import BatSide, Position, PitchHand, Status
from mlbstatsapi.models.teams import Team


@dataclass
class Person:
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        id number of the person
    full_name : str
        full_name of the person
    primaryposition : str
        PrimaryPosition of the Person
    pitchhand : str
        PitchHand of the Person
    batside : str
        BatSide of the Person
    fullname : str
        full name of the Person
    firstname : str
        First name of the Person
    lastname : str
        Last name of the Person
    primarynumber : str
        Primary number of the Person
    birthdate : str
        Birth date of the Person
    currentteam : str
        The current Team of the Person
    currentage : str
        The current age of the Person
    birthcity : str
        The birthcity of the Person
    birthstateprovince : str
        The province of the birth state
    height : str
        The height of the Person
    weight : str
        The weight of the Person
    active : str
        The active status of the Person
    usename : str
        The use name of the Person
    middlename : str
        The middle name of the Person
    boxscorename : str
        The box score name of the Person
    nickname : str
        The nickname of the Person
    draftyear : int
        The draft year of the Person
    mlbdebutdate : str
        The MLB debut date of the Person
    namefirstlast : str
        The first and last name of the Person
    nameslug : str
        The name slug of the Person
    firstlastname : str
        The first and last name of the Person
    lastfirstname : str
        The last and first name of the Person
    lastinitname : str
        The last init name of the Person
    initlastname : str
        The init last name of the Person
    fullfmlname : str
        The full fml name of the Person
    fulllfmname : str
        The full lfm name of the Person
    uselastname : str
        The last name of the
    birthcountry : str
        The birth country of the Person
    pronunciation : str
        The pronuciation of the Person's name
    strikezonetop : float
        The strike zone top of the Person
    strikezonebottom : float
        The strike zone bottom of the Person
    nametitle : str
        The name title of the Person
    gender : str
        The gender of the Person
    isplayer : bool
        The player status of the Person
    isverified : bool
        The verification of the Person
    namematrilineal : str
        The name matrilineal of the Person
    deathdate : str
        The death date of the Person
    deathcity : str
        The death city of the Person
    deathcountry : str
        The death country of the Person
    lastplayeddate : str
        The last played date of the Person
    namesuffix : str
        The namesuffix of the Person
    """

    id: int
    link: str
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
    lastplayeddate: Optional[str] = None
    uselastname: Optional[str] = None
    namesuffix: Optional[str] = None

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
    jerseynumber : str
        id number of the person
    status : 
        Status of the player
    parentteamid : int
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
    jerseynumber : str
        id number of the person
    job : str
        job of the coach
    jobid : str
        job id of the coach
    title : str
        title of the coach
    parentteamid : int
    """
    jerseynumber: str
    job: str
    jobid: str
    title: str


@dataclass(kw_only=True)
class Batter(Person):
    """
    A class to represent a Batter.
    """
    pass


@dataclass(kw_only=True)
class Pitcher(Person):
    """
    A class to represent a Pitcher
    """
    pass


@dataclass(kw_only=True)
class DraftPick(Person):
    """
    bisplayerid : int
    pickround :  str
    picknumber :  int
    roundpicknumber :  int
    rank :  int
    pickvalue : str
    signingbonus :  str
    home : dict
    scoutingreport : str
    school : dict 
    blurb : str
    headshotlink : str
    person : Person
    team : Team
    drafttype : dict
    isdrafted : bool
    ispass : bool
    year : str
    """

    bisplayerid: Optional[int] = None
    pickround:  str
    picknumber:  int
    roundpicknumber:  int
    rank: Optional[int] = None
    pickvalue: Optional[str] = None
    signingbonus:  str
    home: dict
    scoutingreport: Optional[str] = None
    school: dict 
    blurb: Optional[str] = None
    headshotlink: str
    team: Union[Team, dict]
    drafttype: dict
    isdrafted: bool
    ispass: bool
    year: str
