from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.seasons import Season


class LeagueRecord(MLBBaseModel):
    """
    A class to represent a league record.

    Attributes
    ----------
    wins : int
        Number of wins in league record.
    losses : int
        Number of losses in league record.
    pct : str
        Winning percentage of league record.
    ties : int
        Number of ties in league record.
    """
    wins: int
    losses: int
    pct: str
    ties: Optional[int] = None


class League(MLBBaseModel):
    """
    A class to represent a league.

    Attributes
    ----------
    id : int
        ID number of the league.
    link : str
        API link for the league.
    name : str
        Name of the league.
    abbreviation : str
        Abbreviation of the league.
    name_short : str
        Short name for the league.
    season_state : str
        State of the league's season.
    has_wildcard : bool
        Status of the league's wildcard.
    has_split_season : bool
        Status of the league's split season.
    num_games : int
        Total number of league games.
    has_playoff_points : bool
        Status of the league's playoff points.
    num_teams : int
        Total number of teams in league.
    num_wildcard_teams : int
        Total number of wildcard teams in league.
    season_date_info : Season
        Season object.
    season : str
        League season.
    org_code : str
        League's organization code.
    conferences_in_use : bool
        Status of in-use conferences of the league.
    divisions_in_use : bool
        Status of league's divisions in use.
    sport : Sport
        What sport this league is a part of.
    sort_order : int
        League sort order.
    active : bool
        Status on the activity of the league.
    """
    id: int
    link: str
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    name_short: Optional[str] = Field(default=None, alias="nameshort")
    season_state: Optional[str] = Field(default=None, alias="seasonstate")
    has_wildcard: Optional[bool] = Field(default=None, alias="haswildcard")
    has_split_season: Optional[bool] = Field(default=None, alias="hassplitseason")
    num_games: Optional[int] = Field(default=None, alias="numgames")
    has_playoff_points: Optional[bool] = Field(default=None, alias="hasplayoffpoints")
    num_teams: Optional[int] = Field(default=None, alias="numteams")
    num_wildcard_teams: Optional[int] = Field(default=None, alias="numwildcardteams")
    season_date_info: Optional[Season] = Field(default=None, alias="seasondateinfo")
    season: Optional[str] = None
    org_code: Optional[str] = Field(default=None, alias="orgcode")
    conferences_in_use: Optional[bool] = Field(default=None, alias="conferencesinuse")
    divisions_in_use: Optional[bool] = Field(default=None, alias="divisionsinuse")
    sport: Optional[Sport] = None
    sort_order: Optional[int] = Field(default=None, alias="sortorder")
    active: Optional[bool] = None
