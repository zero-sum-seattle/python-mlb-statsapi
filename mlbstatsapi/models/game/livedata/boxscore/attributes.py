from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc


class BoxScoreVL(MLBBaseModel):
    """
    A class to represent a boxscore team's info label and value.

    Attributes
    ----------
    label : str
        The label for this piece of info.
    value : str
        The info associated with this label.
    """
    label: str
    value: Optional[str] = None


class BoxScoreTeamInfo(MLBBaseModel):
    """
    A class to represent a boxscore team's info.

    Attributes
    ----------
    title : str
        Type of information.
    field_list : List[BoxScoreVL]
        List holding the info for this info type.
    """
    title: str
    field_list: List[BoxScoreVL] = Field(alias="fieldlist")


class BoxScoreGameStatus(MLBBaseModel):
    """
    A class representing the game status of a player.

    Attributes
    ----------
    is_current_batter : bool
        Whether the player is the current batter.
    is_current_pitcher : bool
        Whether the player is the current pitcher.
    is_on_bench : bool
        Whether the player is on the bench.
    is_substitute : bool
        Whether the player is a substitute.
    """
    is_current_batter: bool = Field(alias="iscurrentbatter")
    is_current_pitcher: bool = Field(alias="iscurrentpitcher")
    is_on_bench: bool = Field(alias="isonbench")
    is_substitute: bool = Field(alias="issubstitute")


class PlayersDictPerson(MLBBaseModel):
    """
    A class representing a person in a dictionary of players.

    Attributes
    ----------
    person : Person
        The person object.
    jersey_number : str
        The person's jersey number.
    position : Position
        The person's position.
    status : CodeDesc
        The person's status.
    parent_team_id : int
        The ID of the person's parent team.
    stats : dict
        A dictionary of the person's stats.
    season_stats : dict
        A dictionary of the person's season stats.
    game_status : BoxScoreGameStatus
        The person's game status.
    batting_order : int
        The person's place in the batting order if available.
    all_positions : List[Position]
        All of the person's positions if available.
    """
    person: Person
    status: CodeDesc
    stats: dict
    season_stats: dict = Field(alias="seasonstats")
    game_status: BoxScoreGameStatus = Field(alias="gamestatus")
    position: Optional[Position] = None
    batting_order: Optional[int] = Field(default=None, alias="battingorder")
    jersey_number: Optional[str] = Field(default=None, alias="jerseynumber")
    parent_team_id: Optional[int] = Field(default=None, alias="parentteamid")
    all_positions: Optional[List[Position]] = Field(default=None, alias="allpositions")


class BoxScoreTeam(MLBBaseModel):
    """
    A class to represent the boxscore team.

    Attributes
    ----------
    team : Team
        This team.
    team_stats : dict
        Team stats.
    players : dict
        Players on team.
    batters : List[int]
        List of batter player IDs for this team.
    pitchers : List[int]
        List of pitcher player IDs for this team.
    bench : List[int]
        List of bench player IDs for this team.
    bullpen : List[int]
        Bullpen list of player IDs.
    batting_order : List[int]
        Batting order for this team as a list of player IDs.
    info : List[BoxScoreTeamInfo]
        Batting and fielding info for team.
    note : List[BoxScoreVL]
        Team notes.
    """
    team: Team
    team_stats: dict = Field(alias="teamstats")
    players: Dict[str, PlayersDictPerson]
    batters: List[int]
    pitchers: List[int]
    bench: List[int]
    bullpen: List[int]
    batting_order: List[int] = Field(alias="battingorder")
    info: List[BoxScoreTeamInfo]
    note: List[BoxScoreVL] = []


class BoxScoreTeams(MLBBaseModel):
    """
    A class to represent the boxscore home and away teams.

    Attributes
    ----------
    home : BoxScoreTeam
        Home team boxscore information.
    away : BoxScoreTeam
        Away team boxscore information.
    """
    home: BoxScoreTeam
    away: BoxScoreTeam


class BoxScoreOfficial(MLBBaseModel):
    """
    A class to represent an official for this game.

    Attributes
    ----------
    official : Person
        The official person.
    official_type : str
        What type of official this person is.
    """
    official: Person
    official_type: str = Field(alias="officialtype")
