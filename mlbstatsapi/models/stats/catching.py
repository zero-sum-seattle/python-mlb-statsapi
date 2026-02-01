from typing import Optional, List, ClassVar
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel, OptionalFloat
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from .stats import Split


class SimpleCatchingSplit(MLBBaseModel):
    """
    A class to represent a simple catching split.

    Attributes
    ----------
    age : int
        Age at beginning of season.
    games_played : int
        The number of games played by the catcher.
    runs : int
        The number of runs given up while catching.
    home_runs : int
        The number of home runs given up while catching.
    strikeouts : int
        The number of strike outs while catching.
    base_on_balls : int
        The number of base on balls while catching.
    intentional_walks : int
        The number of intentional walks while catching.
    hits : int
        The number of hits while catching.
    hit_by_pitch : int
        The number of batters hit by a pitch while catching.
    avg : float
        The batting average while catching.
    at_bats : int
        The number of at bats while catching.
    obp : float
        The on base percentage while catching.
    slg : float
        The slugging percentage while catching.
    ops : float
        The on-base slugging while catching.
    caught_stealing : int
        The number of runners caught stealing by the catcher.
    caught_stealing_percentage : float
        Percentage of runners caught stealing by the catcher.
    stolen_bases : int
        The number of stolen bases while catching.
    stolen_base_percentage : float
        The stolen base percentage against the catcher.
    earned_runs : int
        The earned run amount against the catcher.
    batters_faced : int
        The number of batters faced while catching.
    games_pitched : int
        The number of games pitched while catching.
    hit_batsmen : int
        The number of batters hit by pitches while catching.
    wild_pitches : int
        The number of wild pitches while catching.
    pickoffs : int
        The number of pick offs while catching.
    total_bases : int
        The total number of bases.
    strikeout_walk_ratio : float
        The strike out to walk ratio while catching.
    catchers_interference : int
        The number of times catcher interference committed.
    sac_bunts : int
        The number of sac bunts performed while catching.
    sac_flies : int
        The number of sac flies while catching.
    passed_ball : int
        The number of passed balls while catching.
    pickoff_attempts : int
        The number of pickoff attempts.
    """
    age: Optional[int] = None
    games_played: Optional[int] = Field(default=None, alias="gamesPlayed")
    runs: Optional[int] = None
    home_runs: Optional[int] = Field(default=None, alias="homeRuns")
    strikeouts: Optional[int] = Field(default=None, alias="strikeOuts")
    base_on_balls: Optional[int] = Field(default=None, alias="baseOnBalls")
    intentional_walks: Optional[int] = Field(default=None, alias="intentionalWalks")
    hits: Optional[int] = None
    hit_by_pitch: Optional[int] = Field(default=None, alias="hitByPitch")
    avg: OptionalFloat = None
    at_bats: Optional[int] = Field(default=None, alias="atBats")
    obp: OptionalFloat = None
    slg: OptionalFloat = None
    ops: OptionalFloat = None
    caught_stealing: Optional[int] = Field(default=None, alias="caughtStealing")
    caught_stealing_percentage: OptionalFloat = Field(default=None, alias="caughtStealingPercentage")
    stolen_bases: Optional[int] = Field(default=None, alias="stolenBases")
    stolen_base_percentage: OptionalFloat = Field(default=None, alias="stolenBasePercentage")
    earned_runs: Optional[int] = Field(default=None, alias="earnedRuns")
    batters_faced: Optional[int] = Field(default=None, alias="battersFaced")
    games_pitched: Optional[int] = Field(default=None, alias="gamesPitched")
    hit_batsmen: Optional[int] = Field(default=None, alias="hitBatsmen")
    wild_pitches: Optional[int] = Field(default=None, alias="wildPitches")
    pickoffs: Optional[int] = None
    total_bases: Optional[int] = Field(default=None, alias="totalBases")
    strikeout_walk_ratio: OptionalFloat = Field(default=None, alias="strikeoutWalkRatio")
    catchers_interference: Optional[int] = Field(default=None, alias="catchersInterference")
    sac_bunts: Optional[int] = Field(default=None, alias="sacBunts")
    sac_flies: Optional[int] = Field(default=None, alias="sacFlies")
    passed_ball: Optional[int] = Field(default=None, alias="passedBall")
    pickoff_attempts: Optional[int] = Field(default=None, alias="pickoffAttempts")


class CatchingSeason(Split):
    """
    A class to represent a catching season statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['season']
    stat: SimpleCatchingSplit


class CatchingSingleSeason(Split):
    """
    A class to represent a catching statsSingleSeason statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeason']
    stat: SimpleCatchingSplit


class CatchingYearByYearPlayoffs(Split):
    """
    A class to represent a catching yearByYearPlayoffs statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearPlayoffs']
    stat: SimpleCatchingSplit


class CatchingYearByYear(Split):
    """
    A class to represent a catching yearByYear statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYear']
    stat: SimpleCatchingSplit


class CatchingProjected(Split):
    """
    A class to represent a catching projectedRos statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['projectedRos']
    stat: SimpleCatchingSplit


class CatchingCareer(Split):
    """
    A class to represent a catching career statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['career']
    stat: SimpleCatchingSplit


class CatchingCareerRegularSeason(Split):
    """
    A class to represent a catching careerRegularSeason statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['careerRegularSeason']
    stat: SimpleCatchingSplit


class CatchingGameLog(Split):
    """
    A class to represent a catching gameLog statistic.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    is_win : bool
        Is win bool.
    date : str
        The date.
    game : Game
        The game.
    opponent : Team
        The opponent.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    is_home: bool = Field(alias="isHome")
    is_win: bool = Field(alias="isWin")
    date: str
    game: Game
    opponent: Team


class CatchingLastXGames(Split):
    """
    A class to represent a catching lastXGames statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['lastXGames']
    stat: SimpleCatchingSplit


class CatchingByDateRange(Split):
    """
    A class to represent a catching byDateRange statistic.

    Attributes
    ----------
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRange']
    stat: SimpleCatchingSplit


class CatchingByDayOfWeek(Split):
    """
    A class to represent a catching byDayOfWeek statistic.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeek']
    day_of_week: int = Field(alias="dayOfWeek")
    stat: SimpleCatchingSplit


class CatchingHomeAndAway(Split):
    """
    A class to represent a catching homeAndAway statistic.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAway']
    is_home: bool = Field(alias="isHome")
    stat: SimpleCatchingSplit


class CatchingWinLoss(Split):
    """
    A class to represent a catching winLoss statistic.

    Attributes
    ----------
    is_win : bool
        Is win bool.
    stat : SimpleCatchingSplit
        The catching split stat.
    """
    _stat: ClassVar[List[str]] = ['winLoss']
    is_win: bool = Field(alias="isWin")
    stat: SimpleCatchingSplit
