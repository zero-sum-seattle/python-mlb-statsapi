from typing import Union, Optional, List
from pydantic import BaseModel

from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.leagues import League

class Record(BaseModel):
    """Represents a basic record, providing a general structure for wins, losses, and winning percentage.

    Attributes:
        wins (int): The number of wins.
        losses (int): The number of losses.
        pct (str): The winning percentage.
    """
    wins: int
    losses: int
    pct: str

class OverallLeagueRecord(Record):
    """Represents the overall league record for a team, including wins, losses, and overall win percentage.

    Attributes:
        wins (int): The overall number of wins in the league.
        losses (int): The overall number of losses in the league.
        pct (str): The overall win percentage in the league.
    """
    ties: int


class TypeRecords(Record):
    """Represents specific types of records for a team, such as home vs. away or pre/post All-Star break.

    Attributes:
        wins (int): The number of wins for the specified type.
        losses (int): The number of losses for the specified type.
        pct (str): The win percentage for the specified type.
        type (str): The type of record (e.g., "Home", "Away", "Post-All-Star").
    """
    type: str

class DivisionRecords(Record):
    """Represents the team's record within their division, including wins, losses, and win percentage.

    Attributes:
        wins (int): The number of wins within the division.
        losses (int): The number of losses within the division.
        pct (str): The win percentage within the division.
        division (Union[Division, dict]): The division for which the record is applicable.
    """
    division: Division

class LeagueRecords(Record):
    """Represents the team's record within their league, detailing wins, losses, and win percentage.

    Attributes:
        wins (int): The number of wins within the league.
        losses (int): The number of losses within the league.
        pct (str): The win percentage within the league.
        league (Union[League, dict]): The league for which the record is applicable.
    """
    league: League

class Records(BaseModel):
    """Represents the various types of records held by a team, categorized into splits, divisions, overall, league, and expected records.

    Attributes:
        splitRecords (List[Typerecords]): A list of the team's records split by various criteria. If not applicable, the list may be empty.
        divisionRecords (List[Divisionrecords]): A list detailing the team's records within their division. If not applicable, the list may be empty.
        overallRecords (List[Typerecords]): A list of the team's overall records across all games played. If not applicable, the list may be empty.
        leagueRecords (List[Leaguerecords]): A list of the team's records within their league. If not applicable, the list may be empty.
        expectedRecords (List[Typerecords]): A list of the team's expected records based on performance metrics. If not applicable, the list may be empty.
    """
    splitRecords: Optional[List[TypeRecords]] = None
    divisionRecords: Optional[List[DivisionRecords]] = None
    overallRecords: Optional[List[TypeRecords]] = None
    leagueRecords: Optional[List[LeagueRecords]] = None
    expectedRecords: Optional[List[TypeRecords]] = None


class TeamRecord(BaseModel):
    """Represents a team's current record, including their standing in various leagues and their overall performance.

    Attributes:
        gamesPlayed (int): The number of games played by the team.
        wildCardGamesBack (str): The number of games behind the leader in the wild card race.
        leagueGamesBack (str): The number of games behind the leader in the league.
        springLeagueGamesBack (str): The number of games behind the leader in the spring league.
        sportGamesBack (str): The number of games behind the leader in the sport.
        divisionGamesBack (str): The number of games behind the leader in the division.
        conferenceGamesBack (str): The number of games behind the leader in the conference.
        leagueRecord (OverallleagueRecord): The overall league record of the team.
        records (Records): The records of the team.
        divisionLeader (bool): Indicates whether the team is the leader in their division.
        wins (int): The number of wins by the team.
        losses (int): The number of losses by the team.
        winningPercentage (str): The winning percentage of the team.
    """
    gamesPlayed: int
    wildCardGamesBack: str
    leagueGamesBack: str
    springLeagueGamesBack: str
    sportGamesBack: str
    divisionGamesBack: str
    conferenceGamesBack: str
    leagueRecord: OverallLeagueRecord
    records: Records
    divisionLeader: bool
    wins: int
    losses: int
    winningPercentage: str
