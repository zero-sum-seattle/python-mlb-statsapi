from typing import Optional, List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.leagues import League


class Record(MLBBaseModel):
    """
    A class to represent a basic record.

    Attributes
    ----------
    wins : int
        Number of wins.
    losses : int
        Number of losses.
    pct : str
        Winning percentage.
    """
    wins: int
    losses: int
    pct: str


class OverallLeagueRecord(Record):
    """
    A class to represent overall league record.

    Attributes
    ----------
    wins : int
        Overall number of wins in league.
    losses : int
        Overall number of losses in league.
    pct : str
        Overall percentage in league.
    ties : int
        Number of ties.
    """
    ties: int


class TypeRecords(Record):
    """
    A class to represent type records.

    Attributes
    ----------
    wins : int
        Number of wins in type.
    losses : int
        Number of losses in type.
    pct : str
        Percentage in type.
    type : str
        Type of record.
    """
    type: str


class DivisionRecords(Record):
    """
    A class to represent division records.

    Attributes
    ----------
    wins : int
        Number of wins in division.
    losses : int
        Number of losses in division.
    pct : str
        Percentage in division.
    division : Division
        Division.
    """
    division: Division


class LeagueRecords(Record):
    """
    A class to represent league records.

    Attributes
    ----------
    wins : int
        Number of wins in league.
    losses : int
        Number of losses in league.
    pct : str
        Percentage in league.
    league : League
        League.
    """
    league: League


class Records(MLBBaseModel):
    """
    A class representing the records of a team.

    Attributes
    ----------
    split_records : List[TypeRecords]
        A list of split records.
    division_records : List[DivisionRecords]
        A list of division records.
    overall_records : List[TypeRecords]
        A list of overall records.
    league_records : List[LeagueRecords]
        A list of league records.
    expected_records : List[TypeRecords]
        A list of expected records.
    """
    split_records: Optional[List[TypeRecords]] = Field(default=None, alias="splitrecords")
    division_records: Optional[List[DivisionRecords]] = Field(default=None, alias="divisionrecords")
    overall_records: Optional[List[TypeRecords]] = Field(default=None, alias="overallrecords")
    league_records: Optional[List[LeagueRecords]] = Field(default=None, alias="leaguerecords")
    expected_records: Optional[List[TypeRecords]] = Field(default=None, alias="expectedrecords")


class TeamRecord(MLBBaseModel):
    """
    A class to represent a team's current record.

    Attributes
    ----------
    games_played : int
        The number of games played by the team.
    wildcard_games_back : str
        The number of games behind the leader in the wild card race.
    league_games_back : str
        The number of games behind the leader in the league.
    spring_league_games_back : str
        The number of games behind the leader in the spring league.
    sport_games_back : str
        The number of games behind the leader in the sport.
    division_games_back : str
        The number of games behind the leader in the division.
    conference_games_back : str
        The number of games behind the leader in the conference.
    league_record : OverallLeagueRecord
        The overall league record of the team.
    records : Records
        The records of the team.
    division_leader : bool
        Whether the team is the leader in their division.
    wins : int
        The number of wins of the team.
    losses : int
        The number of losses of the team.
    winning_percentage : str
        The winning percentage of the team.
    """
    games_played: int = Field(alias="gamesplayed")
    wildcard_games_back: str = Field(alias="wildcardgamesback")
    league_games_back: str = Field(alias="leaguegamesback")
    spring_league_games_back: str = Field(alias="springleaguegamesback")
    sport_games_back: str = Field(alias="sportgamesback")
    division_games_back: str = Field(alias="divisiongamesback")
    conference_games_back: str = Field(alias="conferencegamesback")
    league_record: OverallLeagueRecord = Field(alias="leaguerecord")
    records: Records
    division_leader: bool = Field(alias="divisionleader")
    wins: int
    losses: int
    winning_percentage: str = Field(alias="winningpercentage")
