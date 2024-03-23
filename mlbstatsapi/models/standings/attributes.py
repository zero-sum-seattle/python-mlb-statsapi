from typing import Optional, List
from pydantic import BaseModel, Field
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division

class Streak(BaseModel):
    """Represents a winning streak
    

    Attributes:
        streaktype(str): Steak type     
        streaknumber(int): Streak number
        streakcode(str): Steak code

    """
    streakType: str
    streakNumber: int
    streakCode: str

class DivisionRecord(BaseModel):
    """Represents a league record.

    Attributes:
        wins (int): Number of wins in the league record.
        losses (int): Number of losses in the league record.
        pct (str): Winning percentage of the league record.
        division (Division): 
    """
    wins: int
    losses: int
    pct: str
    division: Division
    

class LeagueRecord(BaseModel):
    """Represents a league record.

    Attributes:
        wins (int): Number of wins in the league record.
        losses (int): Number of losses in the league record.
        pct (str): Winning percentage of the league record.
        league (League): Number of ties in the league record. Optional.
    """
    wins: int = None
    losses: int = None
    pct: str = None
    league: League = None
    
class Record(BaseModel):
    """Represents a league record.

    Attributes:
        wins (int): Number of wins in the league record.
        losses (int): Number of losses in the league record.
        ties (int, optional): Number of ties in the league record. Optional.
        pct (str): Winning percentage of the league record.
    """
    wins: int
    losses: int
    pct: str
    ties: Optional[int] = None

class Records(BaseModel):
    """Represents a league record.

    Attributes:
        splitRecords (list): 
        divisionRecords (list): List[DivisionRecord]
        overallRecords: List[Record]
        leagueRecords: 
    """
    splitRecords: List[Record] = Field(default_factory=list)
    divisionRecords: List[DivisionRecord] = Field(default_factory=list)
    overallRecords: List[Record] = Field(default_factory=list)
    leagueRecords: List[LeagueRecord] = Field(default_factory=list)
    expectedRecords: Optional[List[Record]] = Field(default=list)


class TeamRecord(BaseModel):
    """
    Extends TeamRecord to include detailed statistics and standings for a team.

    Attributes:
        team (`Team`): The team for which the record is maintained. This can be either an instance
            of the Team class or a dictionary containing team information.
        season (int): The year of the season for which the record is relevant.
        streak (`Streak`): Information about the team's current streak. This can be either an instance
            of the Streak class or a dictionary containing streak information.
        divisionRank (str): The team's rank within their division.
        leagueRank (str): The team's rank within their league.
        sportRank (str): The team's rank within their sport.
        gamesPlayed (`int`, optional): The total number of games played by the team.
        gamesBack (str): The number of games the team is behind the division leader.
        wildCardGamesBack (`str`, optional): The number of games the team is behind the wild card leader.
        leagueGamesBack (`str`, optional): The number of games the team is behind the league leader.
        springLeagueGamesBack (`str`, optional): The number of games the team is behind the spring league leader.
        sportGamesBack (`str`, optional): The number of games the team is behind the sport leader.
        divisionGamesBack (`str`, optional): The number of games the team is behind the division leader.
        conferenceGamesBack (`str`, optional): The number of games the team is behind the conference leader.
        leagueRecord (OverallLeagueRecord, optional): The team's overall league record, which can be either an instance
            of the OverallLeagueRecord class or a dictionary containing league record information.
        lastUpdated (str): The timestamp when the record was last updated.
        records (Records, optional): Detailed records of the team, which can be either an instance of the Records class
            or a dictionary containing records information.
        runsAllowed (int): The total number of runs allowed by the team.
        runsScored (int): The total number of runs scored by the team.
        divisionChamp (bool): Indicates whether the team is the division champion.
        divisionLeader (`bool`, optional): Indicates whether the team is leading their division.
        hasWildcard (bool): Indicates whether the team has a wildcard spot.
        clinched (bool): Indicates whether the team has clinched a spot in the playoffs.
        eliminationNumber (str): The "magic number" of games the team needs to either win or have their
            competitors lose to be eliminated from playoff contention.
        eliminationNumberSport (`str`, optional): Sport-specific elimination number.
        eliminationNumberLeague (`str`, optional): League-specific elimination number.
        eliminationNumberDivision (`str`, optional): Division-specific elimination number.
        eliminationNumberConference (`str`, optional): Conference-specific elimination number.
        wildCardEliminationNumber (`str`, optional): The number of games needed to be eliminated from wild card contention.
        wins (`int`, optional): The total number of wins.
        losses (`int`, optional): The total number of losses.
        runDifferential (int): The difference between runs scored and runs allowed.
        winningPercentage (`str`, optional): The percentage of games won.
        wildCardRank (`str`, optional): The rank of the team in the wild card standings.
        wildCardLeader (`bool`, optional): Indicates whether the team is leading the wild card standings.
        magicNumber (`str`, optional): The number of games the team needs to either win or have their competitors lose
            to clinch a playoff spot.
        clinchIndicator (`str`, optional): A symbol indicating the team's clinch status for playoffs.
    """
    team: Team
    season: int
    streak: Streak
    divisionRank: str
    leagueRank: str
    sportRank: str
    gamesPlayed: Optional[int] = None
    gamesBack: str
    wildCardGamesBack: Optional[str] = None
    leagueGamesBack: Optional[str] = None
    springLeagueGamesBack: Optional[str] = None
    sportGamesBack: Optional[str] = None
    divisionGamesBack: Optional[str] = None
    conferenceGamesBack: Optional[str] = None
    leagueRecord: Optional[LeagueRecord] = None
    lastUpdated: str
    records: Records
    runsAllowed: int
    runsScored: int
    divisionChamp: bool
    divisionLeader: Optional[bool] = None
    hasWildcard: bool
    clinched: bool
    eliminationNumber: str
    eliminationNumberSport: str
    eliminationNumberLeague: str
    eliminationNumberDivision: str
    eliminationNumberConference: str
    wildCardEliminationNumber: str
    wins: Optional[int] = None
    losses: Optional[int] = None
    runDifferential: int
    winningPercentage: Optional[str] = None
    wildCardRank: Optional[str] = None
    wildCardLeader: Optional[bool] = None
    magicNumber: Optional[str] = None
    clinchIndicator: Optional[str] = None
