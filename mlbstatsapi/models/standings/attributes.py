from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.leagues import League

@dataclass
class Streak:
    """
    

    Attributes:
    ___________
    
    """
    streaktype: str
    streaknumber: int
    streakcode: str

@dataclass
class Record:
    """
    

    Attributes:
    ___________
    
    """
    wins: int
    losses: int
    pct: str

@dataclass
class OverallleagueRecord(Record):
    """
    

    Attributes:
    ___________
    
    """
    ties: int

@dataclass
class Typerecords(Record):
    """
    

    Attributes:
    ___________
    
    """
    type: str

@dataclass
class Divisionrecords(Record):
    """
    

    Attributes:
    ___________
    
    """
    division: Union[Division, dict]

@dataclass
class Leaguerecords(Record):
    """
    

    Attributes:
    ___________
    
    """
    league: Union[League, dict]

@dataclass
class Records:
    """
    

    Attributes:
    ___________
    
    """
    splitrecords: List[Union[Typerecords, dict]]
    divisionrecords: List[Union[Divisionrecords, dict]]
    overallrecords: List[Union[Typerecords, dict]]
    leaguerecords: List[Union[Leaguerecords, dict]]
    expectedrecords: List[Union[Typerecords, dict]]

    def __post_init__(self):
        self.splitrecords = [Typerecords(**splitrecord) for splitrecord in self.splitrecords]
        self.divisionrecords = [Divisionrecords(**divisionrecord) for divisionrecord in self.divisionrecords]
        self.overallrecords = [Typerecords(**overallrecord) for overallrecord in self.overallrecords]
        self.leaguerecords = [Leaguerecords(**leaguerecord) for leaguerecord in self.leaguerecords]
        self.expectedrecords = [Typerecords(**expectedrecord) for expectedrecord in self.expectedrecords]

@dataclass
class Teamrecords:
    """
    

    Attributes:
    ___________
    team : Team

    season : int

    streak : Streak

    divisionrank : str

    leaguerank : str

    sportrank : str

    gamesplayed : int

    gamesback : str

    wildcardgamesback : str

    leaguegamesback : str

    springleaguegamesback : str

    sportgamesback : str

    divisiongamesback : str

    conferencegamesback : str

    leaguerecord : OverallleagueRecord

    lastupdated : str

    records : Records

    runsallowed : int

    runsscored : int

    divisionchamp : bool

    divisionleader : bool

    haswildcard : bool

    clinched : bool

    eliminationnumber : str

    wildcardeliminationnumber : str    

    wins : int

    losses : int

    rundifferential : int

    winningpercentage : str

    wildcardrank : str

    wildcardleader : bool

    magicnumber : str

    clinchindicator : str

    
    """
    team: Union[Team, dict]
    season: int
    streak: Union[Streak, dict]    
    divisionrank: str
    leaguerank: str
    sportrank: str
    gamesplayed: int
    gamesback: str
    wildcardgamesback: str
    leaguegamesback: str
    springleaguegamesback: str
    sportgamesback: str
    divisiongamesback: str
    conferencegamesback: str
    leaguerecord: Union[OverallleagueRecord, dict]
    lastupdated: str
    records: Union[Records, dict]
    runsallowed: int
    runsscored: int
    divisionchamp: bool
    divisionleader: bool
    haswildcard: bool
    clinched: bool
    eliminationnumber: str
    wildcardeliminationnumber: str    
    wins: int
    losses: int
    rundifferential: int
    winningpercentage: str
    wildcardrank: Optional[str] = None
    wildcardleader: Optional[bool] = None
    magicnumber: Optional[str] = None
    clinchindicator: Optional[str] = None

    def __post_init__(self):
        self.team = Team(**self.team)
        self.streak = Streak(**self.streak)
        self.leaguerecord = OverallleagueRecord(**self.leaguerecord)
        self.records = Records(**self.records)