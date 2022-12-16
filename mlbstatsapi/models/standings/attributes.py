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
    streaktype : str
        Steak type
    streaknumber : int
        Streak number
    streakcode : str
        Steak code
    """
    streaktype: str
    streaknumber: int
    streakcode: str

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
    Team Records

    Attributes:
    ___________
    team: Team
        The team for which the data belongs to. Can be an instance of the Team class or a dictionary with relevant information about the team.
    season: int
        The season for which the data belongs to.
    streak: Streak
        The streak of the team. Can be an instance of the Streak class or a dictionary with relevant information about the streak.
    divisionrank: str
        The rank of the team in their division.
    leaguerank: str
        The rank of the team in their league.
    sportrank: str
        The rank of the team in their sport.
    gamesplayed: int
        The number of games played by the team.
    gamesback: str
        The number of games behind the leader in the division.
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
    lastupdated: str
        The date when the data was last updated.
    records: Records
        The records of the team. Can be an instance of the Records class or a dictionary with relevant information about the records.
    runsallowed: int
        The number of runs allowed by the team.
    runsscored: int
        The number of runs scored by the team.
    divisionchamp: bool
        A flag indicating whether the team is the division champion.
    divisionleader: bool
        A flag indicating whether the team is the leader in their division.
    haswildcard: bool
        A flag indicating whether the team has a wild card spot.
    clinched: bool
        A flag indicating whether the team has clinched a spot in the playoffs.
    eliminationnumber: str
        The number of games the team needs to win or the number of games their opponents need to lose in order to be eliminated from playoff contention.
    wildcardeliminationnumber: str
        The number of games the team needs to win or the number of games their opponents need to lose in order to be eliminated from wild card contention.
    wins: int
        The number of wins of the team.
    losses: int
        The number of losses of the team.
    rundifferential: int
        The run differential of the team (runs scored minus runs allowed).
    winningpercentage: str
        The winning percentage of the team.
    wildcardrank: str
        The rank of the team in the wild card race.
    wildcardleader: bool
        A flag indicating whether the team is the leader in the wild card race.
    magicnumber: str
        The number of games the team needs to win or the number of games their opponents need to lose in order to clinch a spot in the playoffs.
    clinchindicator: Optional
    
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