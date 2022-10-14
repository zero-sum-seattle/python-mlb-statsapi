from typing import List, Dict, Union, Any, Optional
from .attributes import PitchHand, PrimaryPosition, BatSide, Status
from mlbstatsapi.models.stats import Stats
from dataclasses import dataclass, field, InitVar


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
    primaryposition: Union[PrimaryPosition, Dict[str, Any]] = field(default_factory=dict)
    pitchhand: Union[PitchHand, Dict[str, Any]] = field(default_factory=dict)
    batside: Union[BatSide, Dict[str, Any]] = field(default_factory=dict)
    stats: Union[Stats, list] = field(default_factory=list)
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
        self.primaryposition = PrimaryPosition(**self.primaryposition) if self.primaryposition else self.primaryposition
        self.pitchhand = PitchHand(**self.pitchhand) if self.pitchhand else self.pitchhand
        self.batside = BatSide(**self.batside) if self.batside else self.batside
        self.stats = [ Stats(**stat) for stat in self.stats ] if self.stats else self.stats

    @staticmethod
    def from_mlb_response(mlbdata: dict) -> "Person":        
        # maybe create a function that does this in mlbdata?
        mlbdata = {k.lower(): v for k, v in mlbdata.items()}
        return Person(**mlbdata)

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
        self.primaryposition = PrimaryPosition(**position)

    @staticmethod
    def from_mlb_response(mlbdata: dict) -> "Player":
        
        # maybe create a function that does this in mlbdata?
        person = mlbdata.pop('person')
        mlbdata = {**mlbdata, **person}
        mlbdata = {k.lower(): v for k, v in mlbdata.items()}

        return Player(**mlbdata)


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

    @staticmethod
    def from_mlb_response(mlbdata: dict) -> "Coach":
    # maybe create a function that does this in mlbdata?
        person = mlbdata.pop('person')
        mlbdata = {**mlbdata, **person}
        mlbdata = {k.lower(): v for k, v in mlbdata.items()}

        return Coach(**mlbdata)

