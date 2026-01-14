from typing import Optional, List, Any, ClassVar
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Batter, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.data import CodeDesc


class PitchArsenalSplit(MLBBaseModel):
    """
    A class to represent a pitching pitch arsenal split.

    Attributes
    ----------
    percentage : float
        Percentage of this pitch type.
    count : int
        Count of this pitch type.
    total_pitches : int
        Total pitches thrown.
    average_speed : float
        Average speed of this pitch type.
    type : CodeDesc
        The pitch type code and description.
    """
    percentage: float
    count: int
    total_pitches: int = Field(alias="totalPitches")
    average_speed: float = Field(alias="averageSpeed")
    type: CodeDesc


class ExpectedStatistics(MLBBaseModel):
    """
    A class to hold expected statistics.

    Attributes
    ----------
    avg : str
        Expected batting average.
    slg : str
        Expected slugging.
    woba : str
        Expected wOBA.
    wobacon : str
        Expected wOBA on contact.
    """
    avg: str
    slg: str
    woba: str
    wobacon: str = Field(alias="wobaCon")


class Sabermetrics(MLBBaseModel):
    """
    A class to hold sabermetric statistics.

    Attributes
    ----------
    woba : float
        Weighted on-base average.
    wraa : float
        Weighted runs above average.
    wrc : float
        Weighted runs created.
    wrc_plus : float
        Weighted runs created plus.
    rar : float
        Runs above replacement.
    war : float
        Wins above replacement.
    batting : float
        Batting runs.
    fielding : float
        Fielding runs.
    base_running : float
        Base running runs.
    positional : float
        Positional adjustment.
    w_league : float
        League adjustment.
    replacement : float
        Replacement level runs.
    spd : float
        Speed score.
    ubr : float
        Ultimate base running.
    w_gdp : float
        Weighted grounded into double play runs.
    w_sb : float
        Weighted stolen base runs.
    """
    woba: Optional[float] = None
    wraa: Optional[float] = None
    wrc: Optional[float] = None
    wrc_plus: Optional[float] = Field(default=None, alias="wrcPlus")
    rar: Optional[float] = None
    war: Optional[float] = None
    batting: Optional[float] = None
    fielding: Optional[float] = None
    base_running: Optional[float] = Field(default=None, alias="baseRunning")
    positional: Optional[float] = None
    w_league: Optional[float] = Field(default=None, alias="wLeague")
    replacement: Optional[float] = None
    spd: Optional[float] = None
    ubr: Optional[float] = None
    w_gdp: Optional[float] = Field(default=None, alias="wGdp")
    w_sb: Optional[float] = Field(default=None, alias="wSb")


class Split(MLBBaseModel):
    """
    Base class for splits.

    Attributes
    ----------
    season : str
        The season.
    num_teams : int
        Number of teams.
    num_leagues : int
        Number of leagues.
    game_type : str
        The game type.
    rank : int
        The rank.
    position : Position
        The position.
    team : Team
        The team.
    player : Person
        The player.
    sport : Sport
        The sport.
    league : League
        The league.
    """
    season: Optional[str] = None
    num_teams: Optional[int] = Field(default=None, alias="numTeams")
    num_leagues: Optional[int] = Field(default=None, alias="numLeagues")
    game_type: Optional[str] = Field(default=None, alias="gameType")
    rank: Optional[int] = None
    position: Optional[Position] = None
    team: Optional[Team] = None
    player: Optional[Person] = None
    sport: Optional[Sport] = None
    league: Optional[League] = None

    @field_validator('position', 'team', 'player', 'sport', 'league', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class Stat(MLBBaseModel):
    """
    Base class for stats.

    Attributes
    ----------
    group : str
        Type of the stat group.
    type : str
        Type of the stat.
    total_splits : int
        The number of split objects.
    exemptions : list
        Exemptions list.
    splits : list
        A list of split objects.
    """
    group: str
    type: str
    total_splits: int = Field(alias="totalSplits")
    exemptions: Optional[List] = []
    splits: Optional[List] = []


class PitchArsenal(Split):
    """
    A class to represent a pitcharsenal stat for a hitter and pitcher.

    Attributes
    ----------
    stat : PitchArsenalSplit
        The pitch arsenal statistics.
    """
    _stat: ClassVar[List[str]] = ['pitchArsenal']
    stat: PitchArsenalSplit


class ZoneCodes(MLBBaseModel):
    """
    A class to represent a zone code statistic used in hot cold zones.

    Attributes
    ----------
    zone : str
        Zone code location.
    color : str
        RGBA code for the color of zone.
    temp : str
        Temperature description of the zone.
    value : str
        Batting percentage of the zone.
    """
    zone: str
    value: str
    color: Optional[str] = None
    temp: Optional[str] = None


class Zones(MLBBaseModel):
    """
    A class to represent a hot cold zone statistic.

    Attributes
    ----------
    name : str
        Name of the hot cold zone.
    zones : List[ZoneCodes]
        A list of zone codes to describe the zone.
    """
    name: str
    zones: List[ZoneCodes] = []


class HotColdZones(Split):
    """
    A class to represent a hotcoldzone statistic.

    Attributes
    ----------
    stat : Zones
        The hot cold zones for the stat.
    """
    _stat: ClassVar[List[str]] = ['hotColdZones']
    stat: Zones


class Chart(MLBBaseModel):
    """
    A class to represent a chart for SprayCharts.

    Attributes
    ----------
    left_field : int
        Left field percentage.
    left_center_field : int
        Left center field percentage.
    center_field : int
        Center field percentage.
    right_center_field : int
        Right center field percentage.
    right_field : int
        Right field percentage.
    """
    left_field: int = Field(alias="leftField")
    left_center_field: int = Field(alias="leftCenterField")
    center_field: int = Field(alias="centerField")
    right_center_field: int = Field(alias="rightCenterField")
    right_field: int = Field(alias="rightField")


class SprayCharts(Split):
    """
    A class to represent spray chart statistics.

    Attributes
    ----------
    stat : Chart
        The spray chart data.
    batter : Batter
        The batter.
    """
    _stat: ClassVar[List[str]] = ['sprayChart']
    stat: Chart
    batter: Optional[Batter] = None

    @field_validator('batter', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class OutsAboveAverage(Split):
    """
    A class to represent an outs above average statistic.

    NOTE: This stat type returns an empty list, or keys with the value 0.
    """
    _stat: ClassVar[List[str]] = ['outsAboveAverage']
    attempts: int
    total_outs_above_average_back: int = Field(alias="totalOutsAboveAverageBack")
    total_outs_above_average_back_unrounded: int = Field(alias="totalOutsAboveAverageBackUnrounded")
    outs_above_average_back_straight: int = Field(alias="outsAboveAverageBackStraight")
    outs_above_average_back_straight_unrounded: int = Field(alias="outsAboveAverageBackStraightUnrounded")
    outs_above_average_back_left: int = Field(alias="outsAboveAverageBackLeft")
    outs_above_average_back_left_unrounded: int = Field(alias="outsAboveAverageBackLeftUnrounded")
    outs_above_average_back_right: int = Field(alias="outsAboveAverageBackRight")
    outs_above_average_back_right_unrounded: int = Field(alias="outsAboveAverageBackRightUnrounded")
    total_outs_above_average_in: int = Field(alias="totalOutsAboveAverageIn")
    total_outs_above_average_in_unrounded: int = Field(alias="totalOutsAboveAverageInUnrounded")
    outs_above_average_in_straight: int = Field(alias="outsAboveAverageInStraight")
    outs_above_average_in_straight_unrounded: int = Field(alias="outsAboveAverageInStraightUnrounded")
    outs_above_average_in_left: int = Field(alias="outsAboveAverageInLeft")
    outs_above_average_in_left_unrounded: int = Field(alias="outsAboveAverageInLeftUnrounded")
    outs_above_average_in_right: int = Field(alias="outsAboveAverageInRight")
    outs_above_average_in_right_unrounded: int = Field(alias="outsAboveAverageInRightUnrounded")
    player: Person
    game_type: str = Field(alias="gameType")


class PlayerGameLogStat(Split):
    """
    A class to represent a player game log stat.

    Attributes
    ----------
    type : str
        The stat type.
    group : str
        The stat group.
    stat : dict
        The stat data.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    type: str
    group: str
    stat: dict
