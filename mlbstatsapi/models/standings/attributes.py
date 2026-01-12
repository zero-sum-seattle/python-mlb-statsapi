from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.teams.attributes import TeamRecord


class Streak(MLBBaseModel):
    """
    A class to represent a streak.

    Attributes
    ----------
    streak_type : str
        Streak type.
    streak_number : int
        Streak number.
    streak_code : str
        Streak code.
    """
    streak_type: str = Field(alias="streaktype")
    streak_number: int = Field(alias="streaknumber")
    streak_code: str = Field(alias="streakcode")


class TeamRecords(TeamRecord):
    """
    A class to represent team standings records.

    Attributes
    ----------
    team : Team
        The team for which the data belongs to.
    season : int
        The season for which the data belongs to.
    streak : Streak
        The streak of the team.
    division_rank : str
        The rank of the team in their division.
    league_rank : str
        The rank of the team in their league.
    sport_rank : str
        The rank of the team in their sport.
    games_back : str
        The number of games behind the leader in the division.
    last_updated : str
        The date when the data was last updated.
    runs_allowed : int
        The number of runs allowed by the team.
    runs_scored : int
        The number of runs scored by the team.
    division_champ : bool
        Whether the team is the division champion.
    has_wildcard : bool
        Whether the team has a wild card spot.
    clinched : bool
        Whether the team has clinched a spot in the playoffs.
    elimination_number : str
        The elimination number for playoffs.
    elimination_number_sport : str
        The elimination number for sport.
    elimination_number_league : str
        The elimination number for league.
    elimination_number_division : str
        The elimination number for division.
    elimination_number_conference : str
        The elimination number for conference.
    wildcard_elimination_number : str
        The wildcard elimination number.
    run_differential : int
        The run differential of the team.
    wildcard_rank : str
        The rank of the team in the wild card race.
    wildcard_leader : bool
        Whether the team is the leader in the wild card race.
    magic_number : str
        The magic number for clinching.
    clinch_indicator : str
        Clinch indicator.
    """
    team: Team
    season: int
    streak: Streak
    division_rank: str = Field(alias="divisionrank")
    league_rank: str = Field(alias="leaguerank")
    sport_rank: str = Field(alias="sportrank")
    games_back: str = Field(alias="gamesback")
    last_updated: str = Field(alias="lastupdated")
    runs_allowed: int = Field(alias="runsallowed")
    runs_scored: int = Field(alias="runsscored")
    division_champ: bool = Field(alias="divisionchamp")
    has_wildcard: bool = Field(alias="haswildcard")
    clinched: bool
    elimination_number: str = Field(alias="eliminationnumber")
    elimination_number_sport: str = Field(alias="eliminationnumbersport")
    elimination_number_league: str = Field(alias="eliminationnumberleague")
    elimination_number_division: str = Field(alias="eliminationnumberdivision")
    elimination_number_conference: str = Field(alias="eliminationnumberconference")
    wildcard_elimination_number: str = Field(alias="wildcardeliminationnumber")
    run_differential: int = Field(alias="rundifferential")
    wildcard_rank: Optional[str] = Field(default=None, alias="wildcardrank")
    wildcard_leader: Optional[bool] = Field(default=None, alias="wildcardleader")
    magic_number: Optional[str] = Field(default=None, alias="magicnumber")
    clinch_indicator: Optional[str] = Field(default=None, alias="clinchindicator")
