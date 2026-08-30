from typing import Optional, List, Any, ClassVar
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel, OptionalFloat
from mlbstatsapi.models.people import Person, Position, Batter, Pitcher
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.data import PitchData, HitData, Count, PlayDetails
from .stats import Sabermetrics, ExpectedStatistics, Split


class AdvancedHittingSplit(MLBBaseModel):
    """
    A class to represent advanced hitting statistics.

    Attributes
    ----------
    age : int
        Player age at the beginning of the season.
    plate_appearances : int
        The number of plate appearances.
    total_bases : int
        The total number of bases.
    left_on_base : int
        The amount of runners left on base.
    sac_bunts : int
        The amount of sac bunts.
    sac_flies : int
        The amount of sac flies.
    babip : float
        Batting Average on Balls in Play.
    extra_base_hits : int
        The amount of extra base hits.
    hit_by_pitch : int
        The amount of times the batter has been hit by a pitch.
    gidp : int
        The amount of hits that lead to a double play.
    gidp_opp : int
        The amount of GIDP opportunities.
    number_of_pitches : int
        The number of pitches the batter has faced.
    pitches_per_plate_appearance : float
        The avg amount of pitches per plate appearance.
    walks_per_plate_appearance : float
        The avg walks per plate appearance.
    strikeouts_per_plate_appearance : float
        The amount of strike outs per plate appearance.
    home_runs_per_plate_appearance : float
        The amount of home runs per plate appearance.
    walks_per_strikeout : float
        The amount of walks per strike out.
    iso : float
        Isolated power.
    reached_on_error : int
        The amount of times the batter has reached base on an error.
    walkoffs : int
        The amount of times the batter has walked off a game.
    flyouts : int
        The amount of flyouts for the batter.
    total_swings : int
        The amount of swings the batter has taken.
    swing_and_misses : int
        The amount of swing and misses.
    balls_in_play : int
        The amount of balls the batter has put in play.
    popouts : int
        The amount of popouts.
    lineouts : int
        The amount of lineouts.
    groundouts : int
        The amount of groundouts.
    fly_hits : int
        The amount of fly hits.
    pop_hits : int
        The amount of pop hits.
    ground_hits : int
        The amount of ground hits.
    line_hits : int
        The amount of line hits.
    """
    age: Optional[int] = None
    plate_appearances: Optional[int] = Field(default=None, alias="plateAppearances")
    total_bases: Optional[int] = Field(default=None, alias="totalBases")
    left_on_base: Optional[int] = Field(default=None, alias="leftOnBase")
    sac_bunts: Optional[int] = Field(default=None, alias="sacBunts")
    sac_flies: Optional[int] = Field(default=None, alias="sacFlies")
    babip: OptionalFloat = None
    extra_base_hits: Optional[int] = Field(default=None, alias="extraBaseHits")
    hit_by_pitch: Optional[int] = Field(default=None, alias="hitByPitch")
    gidp: Optional[int] = None
    gidp_opp: Optional[int] = Field(default=None, alias="gidpOpp")
    number_of_pitches: Optional[int] = Field(default=None, alias="numberOfPitches")
    pitches_per_plate_appearance: OptionalFloat = Field(default=None, alias="pitchesPerPlateAppearance")
    walks_per_plate_appearance: OptionalFloat = Field(default=None, alias="walksPerPlateAppearance")
    strikeouts_per_plate_appearance: OptionalFloat = Field(default=None, alias="strikeoutsPerPlateAppearance")
    home_runs_per_plate_appearance: OptionalFloat = Field(default=None, alias="homeRunsPerPlateAppearance")
    walks_per_strikeout: OptionalFloat = Field(default=None, alias="walksPerStrikeout")
    iso: OptionalFloat = None
    reached_on_error: Optional[int] = Field(default=None, alias="reachedOnError")
    walkoffs: Optional[int] = Field(default=None, alias="walkOffs")
    flyouts: Optional[int] = Field(default=None, alias="flyOuts")
    total_swings: Optional[int] = Field(default=None, alias="totalSwings")
    swing_and_misses: Optional[int] = Field(default=None, alias="swingAndMisses")
    balls_in_play: Optional[int] = Field(default=None, alias="ballsInPlay")
    popouts: Optional[int] = Field(default=None, alias="popOuts")
    lineouts: Optional[int] = Field(default=None, alias="lineOuts")
    groundouts: Optional[int] = Field(default=None, alias="groundOuts")
    fly_hits: Optional[int] = Field(default=None, alias="flyHits")
    pop_hits: Optional[int] = Field(default=None, alias="popHits")
    ground_hits: Optional[int] = Field(default=None, alias="groundHits")
    line_hits: Optional[int] = Field(default=None, alias="lineHits")


class SimpleHittingSplit(MLBBaseModel):
    """
    A class to represent simple hitting statistics.

    Attributes
    ----------
    age : int
        Player's age at the beginning of the season.
    games_played : int
        The number of games played by the batter.
    flyouts : int
        The number of flyouts hit by the batter.
    groundouts : int
        The amount of groundouts hit by the batter.
    airouts : int
        The amount of air outs by the batter.
    runs : int
        The amount of runs plated by the batter.
    doubles : int
        The amount of doubles hit by the batter.
    triples : int
        The amount of triples hit by the batter.
    home_runs : int
        The amount of home runs hit by the batter.
    strikeouts : int
        The amount of strikeouts for the batter.
    base_on_balls : int
        The amount of base on balls (walks) for the batter.
    intentional_walks : int
        The number of intentional walks for the batter.
    hits : int
        The number of hits for the batter.
    hit_by_pitch : int
        The number of pitches the batter has been hit by.
    avg : float
        The batting avg of the batter.
    at_bats : int
        The number of at bats of the batter.
    obp : float
        The on base percentage of the batter.
    slg : float
        The slugging percentage of the batter.
    ops : float
        The on-base plus slugging of the batter.
    caught_stealing : int
        The amount of times the batter has been caught stealing.
    caught_stealing_percentage : float
        The caught stealing percentage.
    stolen_bases : int
        The amount of stolen bases achieved by the batter.
    stolen_base_percentage : int
        The stolen base percentage of the batter.
    ground_into_double_play : int
        The number of times the batter has hit into a double play.
    ground_into_triple_play : int
        The number of times the batter has hit into a triple play.
    number_of_pitches : int
        The number of pitches the batter has faced.
    plate_appearances : int
        The number of plate appearances of the batter.
    total_bases : int
        The number of bases achieved by batter.
    rbi : int
        The number of Runs Batted In by the batter.
    left_on_base : int
        The number of runners left on base by the batter.
    sac_bunts : int
        The number of sac bunts performed by the batter.
    sac_flies : int
        The number of sac flies performed by the batter.
    babip : float
        The batting average of balls in play of the batter.
    groundouts_to_airouts : int
        The groundout-to-airout ratio of the batter.
    catchers_interference : int
        The number of times the batter has reached base due to catchers interference.
    at_bats_per_home_run : int
        The number of at bats per home run of the batter.
    """
    age: Optional[int] = None
    games_played: Optional[int] = Field(default=None, alias="gamesPlayed")
    flyouts: Optional[int] = Field(default=None, alias="flyOuts")
    groundouts: Optional[int] = Field(default=None, alias="groundOuts")
    airouts: Optional[int] = Field(default=None, alias="airOuts")
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
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
    ground_into_double_play: Optional[int] = Field(default=None, alias="groundIntoDoublePlay")
    ground_into_triple_play: Optional[int] = Field(default=None, alias="groundIntoTriplePlay")
    number_of_pitches: Optional[int] = Field(default=None, alias="numberOfPitches")
    plate_appearances: Optional[int] = Field(default=None, alias="plateAppearances")
    total_bases: Optional[int] = Field(default=None, alias="totalBases")
    rbi: Optional[int] = None
    left_on_base: Optional[int] = Field(default=None, alias="leftOnBase")
    sac_bunts: Optional[int] = Field(default=None, alias="sacBunts")
    sac_flies: Optional[int] = Field(default=None, alias="sacFlies")
    babip: OptionalFloat = None
    groundouts_to_airouts: OptionalFloat = Field(default=None, alias="groundoutsToAirouts")
    catchers_interference: Optional[int] = Field(default=None, alias="catchersInterference")
    at_bats_per_home_run: OptionalFloat = Field(default=None, alias="atBatsPerHomeRun")


class HittingWinLoss(Split):
    """
    A class to represent a hitting winLoss statistic.

    Attributes
    ----------
    is_win : bool
        The bool to hold if a win or not.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['winLoss']
    is_win: bool = Field(alias="isWin")
    stat: SimpleHittingSplit


class HittingWinLossPlayoffs(Split):
    """
    A class to represent a hitting winLossPlayoffs statistic.

    Attributes
    ----------
    is_win : bool
        The bool to hold if a win or not.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['winLossPlayoffs']
    is_win: bool = Field(alias="isWin")
    stat: SimpleHittingSplit


class HittingHomeAndAway(Split):
    """
    A class to represent a hitting homeAndAway statistic.

    Attributes
    ----------
    is_home : bool
        The bool to hold if it is home.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAway']
    is_home: bool = Field(alias="isHome")
    stat: SimpleHittingSplit


class HittingHomeAndAwayPlayoffs(Split):
    """
    A class to represent a hitting homeAndAway Playoff statistic.

    Attributes
    ----------
    is_home : bool
        The bool to hold if it is home.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAwayPlayoffs']
    is_home: bool = Field(alias="isHome")
    stat: SimpleHittingSplit


class HittingCareer(Split):
    """
    A class to represent a hitting career, careerRegularSeason or careerPlayoffs statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['career', 'careerRegularSeason', 'careerPlayoffs']
    stat: SimpleHittingSplit


class HittingSeason(Split):
    """
    A class to represent a hitting season statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['season']
    stat: SimpleHittingSplit


class HittingSingleSeason(Split):
    """
    A class to represent a hitting statsSingleSeason statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeason']
    stat: SimpleHittingSplit


class HittingSeasonAdvanced(Split):
    """
    A class to represent a hitting seasonAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['seasonAdvanced']
    stat: AdvancedHittingSplit


class HittingCareerAdvanced(Split):
    """
    A class to represent a hitting careerAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['careerAdvanced']
    stat: AdvancedHittingSplit


class HittingYearByYear(Split):
    """
    A class to represent a hitting yearByYear statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYear']
    stat: SimpleHittingSplit


class HittingYearByYearPlayoffs(Split):
    """
    A class to represent a hitting yearByYearPlayoffs statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearPlayoffs']
    stat: SimpleHittingSplit


class OpponentsFacedHitting(Split):
    """
    A class to represent a hitting opponentsFaced statistic.

    Attributes
    ----------
    batter : Batter
        The batter of that stat object.
    fielding_team : Team
        The defence team of the stat object.
    pitcher : Pitcher
        The pitcher of that stat object.
    group : str
        Stat group.
    """
    _stat: ClassVar[List[str]] = ['opponentsFaced']
    group: str
    batter: Batter
    fielding_team: Team = Field(alias="fieldingTeam")
    pitcher: Pitcher


class HittingSabermetrics(Split):
    """
    A class to represent a hitting sabermetric statistic.

    Attributes
    ----------
    stat : Sabermetrics
        The sabermetric statistics.
    """
    _stat: ClassVar[List[str]] = ['sabermetrics']
    stat: Sabermetrics


class HittingGameLog(Split):
    """
    A class to represent a gamelog stat for a hitter.

    Attributes
    ----------
    positions_played : List[Position]
        List of positions played.
    stat : SimpleHittingSplit
        The hitting split stat.
    is_home : bool
        Bool to hold is home.
    is_win : bool
        Bool to hold is win.
    game : Game
        Game of the log.
    date : str
        Date of the log.
    opponent : Team
        Team of the opponent.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    is_home: bool = Field(alias="isHome")
    is_win: bool = Field(alias="isWin")
    game: Game
    date: str
    opponent: Team
    positions_played: Optional[List[Position]] = Field(default=[], alias="positionsPlayed")
    stat: Optional[SimpleHittingSplit] = None

    @field_validator('stat', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingPlay(MLBBaseModel):
    """
    A class to represent a play stat for a hitter.

    Attributes
    ----------
    details : PlayDetails
        Play details.
    count : Count
        The count.
    is_pitch : bool
        Is pitch bool.
    pitch_number : int
        Pitch number.
    at_bat_number : int
        At bat number.
    index : str
        Index.
    play_id : str
        Play ID.
    pitch_data : PitchData
        Pitch data.
    hit_data : HitData
        Hit data.
    start_time : str
        Start time.
    end_time : str
        End time.
    type : str
        Type.
    """
    details: PlayDetails
    count: Count
    is_pitch: bool = Field(alias="isPitch")
    pitch_number: Optional[int] = Field(default=None, alias="pitchNumber")
    at_bat_number: Optional[int] = Field(default=None, alias="atBatNumber")
    index: Optional[int] = None
    play_id: Optional[str] = Field(default=None, alias="playId")
    pitch_data: Optional[PitchData] = Field(default=None, alias="pitchData")
    hit_data: Optional[HitData] = Field(default=None, alias="hitData")
    start_time: Optional[str] = Field(default=None, alias="startTime")
    end_time: Optional[str] = Field(default=None, alias="endTime")
    type: Optional[str] = None

    @field_validator('pitch_data', 'hit_data', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingPlayLog(Split):
    """
    A class to represent a play log stat for a hitter.

    Attributes
    ----------
    stat : HittingPlay
        Information regarding the play for the stat.
    opponent : Team
        Opponent.
    date : str
        Date of log.
    is_home : bool
        Is the game at home bool.
    pitcher : Pitcher
        Pitcher of the log.
    batter : Batter
        Batter of the log.
    game : Game
        The game of the log.
    """
    _stat: ClassVar[List[str]] = ['playLog']
    stat: HittingPlay
    opponent: Optional[Team] = None
    date: Optional[str] = None
    is_home: Optional[bool] = Field(default=None, alias="isHome")
    pitcher: Optional[Pitcher] = None
    batter: Optional[Batter] = None
    game: Optional[Game] = None

    @field_validator('stat', mode='before')
    @classmethod
    def extract_play(cls, v: Any) -> Any:
        """Extract play from stat dict."""
        if isinstance(v, dict) and 'play' in v:
            return v['play']
        return v

    @field_validator('opponent', 'pitcher', 'batter', 'game', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingPitchLog(Split):
    """
    A class to represent a pitch log stat for a hitter.

    Attributes
    ----------
    stat : HittingPlay
        Information regarding the play for the stat.
    opponent : Team
        Opponent.
    date : str
        Date of log.
    is_home : bool
        Is the game at home bool.
    pitcher : Pitcher
        Pitcher of the log.
    batter : Batter
        Batter of the log.
    game : Game
        The game of the log.
    play_id : str
        Play ID.
    """
    _stat: ClassVar[List[str]] = ['pitchLog']
    stat: HittingPlay
    opponent: Team
    date: str
    is_home: bool = Field(alias="isHome")
    pitcher: Pitcher
    batter: Batter
    game: Game
    play_id: Optional[str] = Field(default=None, alias="playId")

    @field_validator('stat', mode='before')
    @classmethod
    def extract_play(cls, v: Any) -> Any:
        """Extract play from stat dict."""
        if isinstance(v, dict) and 'play' in v:
            return v['play']
        return v


class HittingLastXGames(Split):
    """
    A class to represent a lastXGames statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['lastXGames']
    stat: SimpleHittingSplit


class HittingDateRange(Split):
    """
    A class to represent a byDateRange statistic.

    Attributes
    ----------
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRange']
    stat: SimpleHittingSplit


class HittingDateRangeAdvanced(Split):
    """
    A class to represent a byDateRangeAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRangeAdvanced']
    stat: AdvancedHittingSplit


class HittingDateRangeAdvancedByMonth(Split):
    """
    A class to represent a byDateRangeAdvanced by month statistic.

    Attributes
    ----------
    stat : AdvancedHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRangeAdvancedbyMonth']
    stat: AdvancedHittingSplit


class HittingByMonth(Split):
    """
    A class to represent a byMonth hitting statistic.

    Attributes
    ----------
    month : int
        The month.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonth']
    month: int
    stat: SimpleHittingSplit


class HittingByMonthPlayoffs(Split):
    """
    A class to represent a byMonthPlayoffs hitting statistic.

    Attributes
    ----------
    month : int
        The month of the stat.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonthPlayoffs']
    month: int
    stat: SimpleHittingSplit


class HittingDayOfWeek(Split):
    """
    A class to represent a byDayOfWeek hitting statistic.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeek']
    day_of_week: int = Field(alias="dayOfWeek")
    stat: SimpleHittingSplit


class HittingDayOfWeekPlayoffs(Split):
    """
    A class to represent a byDayOfWeekPlayoffs hitting statistic.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeekPlayoffs']
    day_of_week: int = Field(alias="dayOfWeek")
    stat: SimpleHittingSplit


class HittingExpectedStatistics(Split):
    """
    A class to represent expected statistics statType: expectedStatistics.

    Attributes
    ----------
    stat : ExpectedStatistics
        The expected statistics.
    """
    _stat: ClassVar[List[str]] = ['expectedStatistics']
    stat: ExpectedStatistics


class HittingVsTeam(Split):
    """
    A class to represent a vsTeam hitting statistic.

    Requires the use of the opposingTeamId parameter.

    Attributes
    ----------
    opponent : Team
        The opponent team.
    batter : Batter
        The batter.
    pitcher : Pitcher
        The pitcher.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsTeam']
    opponent: Team
    stat: SimpleHittingSplit
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingVsTeamTotal(Split):
    """
    A class to represent a vsTeamTotal hitting statistic.

    Requires the use of the opposingTeamId parameter.

    Attributes
    ----------
    opponent : Team
        Opponent team.
    batter : Batter
        Batting person.
    pitcher : Pitcher
        Pitching person.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsTeamTotal']
    opponent: Team
    stat: SimpleHittingSplit
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingVsTeam5Y(Split):
    """
    A class to represent a vsTeam5Y hitting statistic.

    Requires the use of the opposingTeamId parameter.

    Attributes
    ----------
    opponent : Team
        Opponent team.
    batter : Batter
        The batter.
    pitcher : Pitcher
        The pitcher.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsTeam5Y']
    opponent: Team
    stat: SimpleHittingSplit
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingVsPlayer(Split):
    """
    A class to represent a vsPlayer hitting statistic.

    Requires the param opposingPlayerId set.

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat.
    batter : Batter
        The batter of the hitting vsplayer stat.
    opponent : Team
        The team of the hitting vsplayer stat.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayer']
    pitcher: Pitcher
    batter: Batter
    stat: SimpleHittingSplit
    opponent: Optional[Team] = None

    @field_validator('opponent', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingVsPlayerTotal(Split):
    """
    A class to represent a vsPlayerTotal hitting statistic.

    Requires the param opposingPlayerId set.

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat.
    batter : Batter
        The batter of the hitting vsplayer stat.
    opponent : Team
        The team of the hitting vsplayer stat.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayerTotal']
    pitcher: Pitcher
    batter: Batter
    stat: SimpleHittingSplit
    opponent: Optional[Team] = None

    @field_validator('opponent', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class HittingVsPlayer5Y(Split):
    """
    A class to represent a vsPlayer5Y hitting statistic.

    Requires the param opposingPlayerId set.

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat.
    batter : Person
        The batter of the hitting vsplayer stat.
    opponent : Team
        The team of the hitting vsplayer stat.
    stat : SimpleHittingSplit
        The hitting split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayer5Y']
    stat: SimpleHittingSplit
    pitcher: Optional[Pitcher] = None
    batter: Optional[Person] = None
    opponent: Optional[Team] = None

    @field_validator('opponent', 'pitcher', 'batter', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
