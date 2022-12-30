from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.leagues import League

@dataclass
class Record:
    """
    Record

    Attributes:
    ___________
    wins : int
        Number of wins
    losses : int
        Number of losses
    pct : str
        Percentage
    """
    wins: int
    losses: int
    pct: str

@dataclass
class OverallleagueRecord(Record):
    """
    Overall League Record
    

    Attributes:
    ___________
    wins : int
        Overall number of wins in league
    losses : int
        Overall number of losses in league
    pct : str
        Overall percentage in league
    """
    ties: int

@dataclass
class Typerecords(Record):
    """
    Type records

    Attributes:
    ___________
    wins : int
        Number of wins in type
    losses : int
        Number of losses in type
    pct : str
        Percentage in type
    type : str
        Type of record
    """
    type: str

@dataclass
class Divisionrecords(Record):
    """
    Division records

    Attributes:
    ___________
    wins : int
        Number of wins in division
    losses : int
        Number of losses in division
    pct : str
        Percentage in division
    division : Divison
        Division
    """
    division: Union[Division, dict]

@dataclass
class Leaguerecords(Record):
    """
    League records

    Attributes:
    ___________
    wins : int
        Number of wins in league
    losses : int
        Number of losses in league
    pct : str
        Percentage in league
    league : League
        League
    """
    league: Union[League, dict]

@dataclass
class Records:
    """"
    A class representing the records of a team.

    Attributes:
    ___________
    splitrecords : Typerecords
        A list of split records
    divisionrecords : Divisionrecords
        A list of division records
    overallrecords : Typerecords
        A list of overall records
    leaguerecords : Leaguerecords
        A list of league records
    expectedrecords : Typerecords
        A list of expected records
    """
    splitrecords: Optional[List[Union[Typerecords, dict]]] = None
    divisionrecords: Optional[List[Union[Divisionrecords, dict]]] = None
    overallrecords: Optional[List[Union[Typerecords, dict]]] = None
    leaguerecords: Optional[List[Union[Leaguerecords, dict]]] = None
    expectedrecords: Optional[List[Union[Typerecords, dict]]] = None

    def __post_init__(self):
        self.splitrecords = [Typerecords(**splitrecord) for splitrecord in self.splitrecords] if self.splitrecords else None
        self.divisionrecords = [Divisionrecords(**divisionrecord) for divisionrecord in self.divisionrecords] if self.divisionrecords else None
        self.overallrecords = [Typerecords(**overallrecord) for overallrecord in self.overallrecords] if self.overallrecords else None
        self.leaguerecords = [Leaguerecords(**leaguerecord) for leaguerecord in self.leaguerecords] if self.leaguerecords else None
        self.expectedrecords = [Typerecords(**expectedrecord) for expectedrecord in self.expectedrecords] if self.expectedrecords else None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class TeamRecord:
    """
    A class to represent a teams current record.

    Attributes 
    ----------
    gamesplayed: int
        The number of games played by the team.
    wildcardgamesback: str
        The number of games behind the leader in the wild card race.
    leaguegamesback: str
        The number of games behind the leader in the league.
    springleaguegamesback: str
        The number of games behind the leader in the spring league.
    sportgamesback: str
        The number of games behind the leader in the sport.
    divisiongamesback: str
        The number of games behind the leader in the division.
    conferencegamesback: str
        The number of games behind the leader in the conference.
    leaguerecord: OverallleagueRecord
        The overall league record of the team. Can be an instance of the OverallleagueRecord class or a dictionary with relevant information about the record.
    records: Records
        The records of the team. Can be an instance of the Records class or a dictionary with relevant information about the records.
    divisionleader: bool
        A flag indicating whether the team is the leader in their division.
    wins: int
        The number of wins of the team.
    losses: int
        The number of losses of the team.
    winningpercentage: str
        The winning percentage of the team.
    """
    gamesplayed: int
    wildcardgamesback: str
    leaguegamesback: str
    springleaguegamesback: str
    sportgamesback: str
    divisiongamesback: str
    conferencegamesback: str
    leaguerecord: Union[OverallleagueRecord, dict]
    records: Union[Records, dict]
    divisionleader: bool
    wins: int
    losses: int
    winningpercentage: str

    def __post_init__(self):
        self.leaguerecord = OverallleagueRecord(**self.leaguerecord)
        self.records = Records(**self.records)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))