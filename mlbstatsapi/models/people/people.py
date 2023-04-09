from dataclasses import dataclass, field, InitVar
from typing import Union, Dict, Any, Optional

from .attributes import BatSide, Position, PitchHand, Status, Home, School
from mlbstatsapi.models.data import CodeDesc

@dataclass(repr=False)
class Person:
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        id number of the person
    full_name : str
        full_name of the person
    link : str
        Api link to person
    primaryposition : Position
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
    fullName: Optional[str] = None
    link: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    primaryNumber: Optional[str] = None
    birthDate: Optional[str] = None
    currentAge: Optional[str] = None
    birthCity: Optional[str] = None
    birthStateProvince: Optional[str] = None
    birthCountry: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    primaryPosition: Union[Position, Dict[str, Any]] = field(default_factory=dict)
    useName: Optional[str] = None
    useLastName: Optional[str] = None
    middleName: Optional[str] = None
    boxscoreName: Optional[str] = None
    nickName: Optional[str] = None
    gender: Optional[str] = None
    isPlayer: Optional[bool] = None
    isVerified: Optional[bool] = None
    draftYear: Optional[int] = None
    pronunciation: Optional[str] = None
    mlbDebutDate: Optional[str] = None
    batSide: Union[BatSide, Dict[str, Any]] = field(default_factory=dict)
    pitchHand: Union[PitchHand, Dict[str, Any]] = field(default_factory=dict)
    nameFirstLast: Optional[str] = None
    nameSlug: Optional[str] = None
    firstLastName: Optional[str] = None
    lastFirstName: Optional[str] = None
    lastInitName: Optional[str] = None
    initLastName: Optional[str] = None
    fullFMLName: Optional[str] = None
    fullLFMName: Optional[str] = None
    strikeZoneTop: Optional[float] = None
    strikeZoneBottom: Optional[float] = None
    currentTeam: Optional[str] = None
    nameMatrilineal: Optional[str] = None
    lastPlayedDate: Optional[str] = None
    nameTitle: Optional[str] = None
    nameSuffix: Optional[str] = None

    def __post_init__(self):
        self.primaryPosition = Position(**self.primaryPosition) if self.primaryPosition else self.primaryPosition
        self.pitchhand = PitchHand(**self.pitchHand) if self.pitchHand else self.pitchHand
        self.batSide = BatSide(**self.batSide) if self.batSide else self.batSide

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(kw_only=True, repr=False)
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
    jerseyNumber: str
    parentTeamId: int
    position: InitVar[dict]
    status: Union[Status, dict]

    def __post_init__(self, position: dict):
        self.primaryPosition = Position(**position)


@dataclass(kw_only=True, repr=False)
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
    jerseyNumber: str
    job: str
    jobId: str
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
