from typing import Optional, List, Any, ClassVar
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person, Pitcher, Batter
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.data import Count, PlayDetails
from .stats import Sabermetrics, ExpectedStatistics, Split
from .hitting import SimpleHittingSplit


class SimplePitchingSplit(MLBBaseModel):
    """
    A class to represent simple pitching statistics.

    Attributes
    ----------
    summary : str
        Summary of stats for the pitcher.
    games_played : int
        The games played by the pitcher.
    games_started : int
        The games started by the pitcher.
    flyouts : int
        The number of flyouts for the pitcher.
    groundouts : int
        The number of groundouts for the pitcher.
    airouts : int
        The number of airouts for the pitcher.
    runs : int
        The number of runs given up by the pitcher.
    doubles : int
        The number of doubles given up by the pitcher.
    triples : int
        The number of triples given up by the pitcher.
    home_runs : int
        The number of home runs given up by the pitcher.
    strikeouts : int
        The number of strike outs performed by the pitcher.
    base_on_balls : int
        The number of base on balls (walks) performed by the pitcher.
    intentional_walks : int
        The number of intentional walks performed by the pitcher.
    hits : int
        The number of hits given up by the pitcher.
    hit_by_pitch : int
        The number of batters hit by the pitcher.
    avg : str
        The batting avg against the pitcher.
    at_bats : int
        The at bats pitched by the pitcher.
    obp : str
        The on base percentage against the pitcher.
    slg : str
        The slugging percentage against the pitcher.
    ops : str
        The on base slugging against the pitcher.
    caught_stealing : int
        The number of runners caught stealing against the pitcher.
    stolen_bases : int
        The number of stolen bases while pitching.
    stolen_base_percentage : str
        The stolen base percentage while pitching.
    ground_into_double_play : int
        The number of double plays hit into.
    number_of_pitches : int
        The number of pitches thrown.
    era : str
        The earned run average of the pitcher.
    innings_pitched : str
        The number of innings pitched by the pitcher.
    wins : int
        The number of wins by the pitcher.
    losses : int
        The number of losses by the pitcher.
    saves : int
        The number of saves by the pitcher.
    save_opportunities : int
        The number of save opportunities by the pitcher.
    holds : int
        The number of holds by the pitcher.
    blown_saves : int
        The number of blown saves performed by the pitcher.
    earned_runs : int
        The number of earned runs given up by the pitcher.
    whip : str
        The number of walks and hits per inning pitched.
    outs : int
        The number of outs.
    games_pitched : int
        The number of games pitched.
    complete_games : int
        The number of complete games pitched.
    shutouts : int
        The number of shut outs pitched.
    strikes : int
        The number of strikes thrown by the pitcher.
    hit_batsmen : int
        The number of batters hit by a pitch.
    strike_percentage : str
        The strike percentage thrown by the pitcher.
    wild_pitches : int
        The number of wild pitches thrown by the pitcher.
    balks : int
        The number of balks committed by the pitcher.
    total_bases : int
        The total bases given up by the pitcher.
    pickoffs : int
        The number of pick offs performed by the pitcher.
    win_percentage : str
        The win percentage of the pitcher.
    groundouts_to_airouts : str
        The groundout-to-airout ratio of the pitcher.
    games_finished : int
        The number of games finished by the pitcher.
    pitches_per_inning : str
        The number of pitches thrown per inning by the pitcher.
    strikeouts_per_9_inn : str
        The number of strike outs per 9 innings by the pitcher.
    strikeout_walk_ratio : str
        The strike out to walk ratio of the pitcher.
    hits_per_9_inn : str
        The number of hits per 9 innings pitched.
    walks_per_9_inn : str
        The number of walks per 9 innings pitched.
    home_runs_per_9 : str
        The number of home runs per 9 innings pitched.
    runs_scored_per_9 : str
        The number of runs scored per 9 innings pitched.
    sac_bunts : int
        The number of sac bunts given up when pitched.
    catchers_interference : int
        The number of times a runner has reached from catchers interference.
    batters_faced : int
        The number of batters faced by the pitcher.
    sac_flies : int
        The number of sac flies given up by the pitcher.
    inherited_runners_scored : int
        The number of inherited runners scored by the pitcher.
    inherited_runners : int
        The number of inherited runners for the pitcher.
    age : int
        The age of the pitcher.
    caught_stealing_percentage : str
        The caught stealing percentage for the pitcher.
    """
    summary: Optional[str] = None
    age: Optional[int] = None
    games_played: Optional[int] = Field(default=None, alias="gamesplayed")
    games_started: Optional[int] = Field(default=None, alias="gamesstarted")
    flyouts: Optional[int] = None
    groundouts: Optional[int] = None
    airouts: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    home_runs: Optional[int] = Field(default=None, alias="homeruns")
    strikeouts: Optional[int] = None
    base_on_balls: Optional[int] = Field(default=None, alias="baseonballs")
    intentional_walks: Optional[int] = Field(default=None, alias="intentionalwalks")
    hits: Optional[int] = None
    hit_by_pitch: Optional[int] = Field(default=None, alias="hitbypitch")
    avg: Optional[str] = None
    at_bats: Optional[int] = Field(default=None, alias="atbats")
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caught_stealing: Optional[int] = Field(default=None, alias="caughtstealing")
    caught_stealing_percentage: Optional[str] = Field(default=None, alias="caughtstealingpercentage")
    stolen_bases: Optional[int] = Field(default=None, alias="stolenbases")
    stolen_base_percentage: Optional[str] = Field(default=None, alias="stolenbasepercentage")
    ground_into_double_play: Optional[int] = Field(default=None, alias="groundintodoubleplay")
    number_of_pitches: Optional[int] = Field(default=None, alias="numberofpitches")
    era: Optional[str] = None
    innings_pitched: Optional[str] = Field(default=None, alias="inningspitched")
    wins: Optional[int] = None
    losses: Optional[int] = None
    saves: Optional[int] = None
    save_opportunities: Optional[int] = Field(default=None, alias="saveopportunities")
    holds: Optional[int] = None
    blown_saves: Optional[int] = Field(default=None, alias="blownsaves")
    earned_runs: Optional[int] = Field(default=None, alias="earnedruns")
    whip: Optional[str] = None
    outs: Optional[int] = None
    games_pitched: Optional[int] = Field(default=None, alias="gamespitched")
    complete_games: Optional[int] = Field(default=None, alias="completegames")
    shutouts: Optional[int] = None
    strikes: Optional[int] = None
    strike_percentage: Optional[str] = Field(default=None, alias="strikepercentage")
    hit_batsmen: Optional[int] = Field(default=None, alias="hitbatsmen")
    balks: Optional[int] = None
    wild_pitches: Optional[int] = Field(default=None, alias="wildpitches")
    pickoffs: Optional[int] = None
    total_bases: Optional[int] = Field(default=None, alias="totalbases")
    groundouts_to_airouts: Optional[str] = Field(default=None, alias="groundoutstoairouts")
    win_percentage: Optional[str] = Field(default=None, alias="winpercentage")
    pitches_per_inning: Optional[str] = Field(default=None, alias="pitchesperinning")
    games_finished: Optional[int] = Field(default=None, alias="gamesfinished")
    strikeout_walk_ratio: Optional[str] = Field(default=None, alias="strikeoutwalkratio")
    strikeouts_per_9_inn: Optional[str] = Field(default=None, alias="strikeoutsper9inn")
    walks_per_9_inn: Optional[str] = Field(default=None, alias="walksper9inn")
    hits_per_9_inn: Optional[str] = Field(default=None, alias="hitsper9inn")
    runs_scored_per_9: Optional[str] = Field(default=None, alias="runsscoredper9")
    home_runs_per_9: Optional[str] = Field(default=None, alias="homerunsper9")
    catchers_interference: Optional[int] = Field(default=None, alias="catchersinterference")
    sac_bunts: Optional[int] = Field(default=None, alias="sacbunts")
    sac_flies: Optional[int] = Field(default=None, alias="sacflies")
    batters_faced: Optional[int] = Field(default=None, alias="battersfaced")
    inherited_runners: Optional[int] = Field(default=None, alias="inheritedrunners")
    inherited_runners_scored: Optional[int] = Field(default=None, alias="inheritedrunnersscored")
    balls: Optional[int] = None
    outs_pitched: Optional[int] = Field(default=None, alias="outspitched")
    rbi: Optional[int] = None


class AdvancedPitchingSplit(MLBBaseModel):
    """
    A class to represent advanced pitching statistics.

    Attributes
    ----------
    age : int
        The age of the pitcher.
    winning_percentage : str
        The winning percentage of the pitcher.
    runs_scored_per_9 : str
        The number of runs scored per 9 innings.
    batters_faced : int
        The number of batters faced.
    babip : str
        The BABIP of the pitcher.
    obp : str
        The on base percentage against the pitcher.
    slg : str
        The slugging percentage against the pitcher.
    ops : str
        The on base slugging against the pitcher.
    strikeouts_per_9 : str
        The number of strike outs per 9 innings.
    base_on_balls_per_9 : str
        The number of base on balls per 9 innings.
    home_runs_per_9 : str
        The number of home runs per 9 innings.
    hits_per_9 : str
        The number of hits per 9 innings.
    strikeouts_to_walks : str
        The strike out to walk ratio.
    stolen_bases : int
        The number of stolen bases while pitching.
    caught_stealing : int
        The number of runners caught stealing.
    quality_starts : int
        The number of quality starts.
    games_finished : int
        The number of games finished.
    doubles : int
        The number of doubles given up.
    triples : int
        The number of triples given up.
    gidp : int
        The amount of hits that lead to a double play.
    gidp_opp : int
        The amount of GIDP opportunities.
    wild_pitches : int
        The number of wild pitches thrown.
    balks : int
        The number of balks committed.
    pickoffs : int
        The number of pick offs attempted.
    total_swings : int
        The number of swings against the pitcher.
    swing_and_misses : int
        The number of swing and misses.
    balls_in_play : int
        The number of balls put into play.
    run_support : int
        The number of run support.
    strike_percentage : str
        The strike percentage thrown.
    pitches_per_inning : str
        The number of pitches per inning.
    pitches_per_plate_appearance : str
        The avg number of pitches per plate appearance.
    walks_per_plate_appearance : str
        The number of walks per plate appearance.
    strikeouts_per_plate_appearance : str
        The strike outs per plate appearance.
    home_runs_per_plate_appearance : str
        The home runs per plate appearance.
    walks_per_strikeout : str
        The walk per strike out ratio.
    iso : str
        Isolated power.
    flyouts : int
        The number of fly outs given up.
    popouts : int
        The number of pop outs given up.
    lineouts : int
        The number of line outs given up.
    groundouts : int
        The number of ground outs given up.
    fly_hits : int
        The number of fly hits given up.
    pop_hits : int
        The number of pop hits given up.
    line_hits : int
        The number of line hits given up.
    ground_hits : int
        The number of ground hits given up.
    inherited_runners : int
        The number of inherited runners.
    inherited_runners_scored : int
        The number of inherited runners scored.
    bequeathed_runners : int
        The number of bequeathed runners.
    bequeathed_runners_scored : int
        The number of bequeathed runners scored.
    """
    age: Optional[int] = None
    winning_percentage: Optional[str] = Field(default=None, alias="winningpercentage")
    runs_scored_per_9: Optional[str] = Field(default=None, alias="runsscoredper9")
    batters_faced: Optional[int] = Field(default=None, alias="battersfaced")
    babip: Optional[str] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    strikeouts_per_9: Optional[str] = Field(default=None, alias="strikeoutsper9")
    base_on_balls_per_9: Optional[str] = Field(default=None, alias="baseonballsper9")
    home_runs_per_9: Optional[str] = Field(default=None, alias="homerunsper9")
    hits_per_9: Optional[str] = Field(default=None, alias="hitsper9")
    strikeouts_to_walks: Optional[str] = Field(default=None, alias="strikesoutstowalks")
    stolen_bases: Optional[int] = Field(default=None, alias="stolenbases")
    caught_stealing: Optional[int] = Field(default=None, alias="caughtstealing")
    quality_starts: Optional[int] = Field(default=None, alias="qualitystarts")
    games_finished: Optional[int] = Field(default=None, alias="gamesfinished")
    doubles: Optional[int] = None
    triples: Optional[int] = None
    gidp: Optional[int] = None
    gidp_opp: Optional[int] = Field(default=None, alias="gidpopp")
    wild_pitches: Optional[int] = Field(default=None, alias="wildpitches")
    balks: Optional[int] = None
    pickoffs: Optional[int] = None
    total_swings: Optional[int] = Field(default=None, alias="totalswings")
    swing_and_misses: Optional[int] = Field(default=None, alias="swingandmisses")
    strikeouts_minus_walks_percentage: Optional[str] = Field(default=None, alias="strikeoutsminuswalkspercentage")
    gidp_percentage: Optional[str] = Field(default=None, alias="gidppercentage")
    batters_faced_per_game: Optional[str] = Field(default=None, alias="battersfacedpergame")
    bunts_failed: Optional[int] = Field(default=None, alias="buntsfailed")
    bunts_missed_tipped: Optional[int] = Field(default=None, alias="buntsmissedtipped")
    whiff_percentage: Optional[str] = Field(default=None, alias="whiffpercentage")
    balls_in_play: Optional[int] = Field(default=None, alias="ballsinplay")
    run_support: Optional[int] = Field(default=None, alias="runsupport")
    strike_percentage: Optional[str] = Field(default=None, alias="strikepercentage")
    pitches_per_inning: Optional[str] = Field(default=None, alias="pitchesperinning")
    pitches_per_plate_appearance: Optional[str] = Field(default=None, alias="pitchesperplateappearance")
    walks_per_plate_appearance: Optional[str] = Field(default=None, alias="walksperplateappearance")
    strikeouts_per_plate_appearance: Optional[str] = Field(default=None, alias="strikeoutsperplateappearance")
    home_runs_per_plate_appearance: Optional[str] = Field(default=None, alias="homerunsperplateappearance")
    walks_per_strikeout: Optional[str] = Field(default=None, alias="walksperstrikeout")
    iso: Optional[str] = None
    flyouts: Optional[int] = None
    popouts: Optional[int] = None
    lineouts: Optional[int] = None
    groundouts: Optional[int] = None
    fly_hits: Optional[int] = Field(default=None, alias="flyhits")
    pop_hits: Optional[int] = Field(default=None, alias="pophits")
    line_hits: Optional[int] = Field(default=None, alias="linehits")
    ground_hits: Optional[int] = Field(default=None, alias="groundhits")
    inherited_runners: Optional[int] = Field(default=None, alias="inheritedrunners")
    inherited_runners_scored: Optional[int] = Field(default=None, alias="inheritedrunnersscored")
    bequeathed_runners: Optional[int] = Field(default=None, alias="bequeathedrunners")
    bequeathed_runners_scored: Optional[int] = Field(default=None, alias="bequeathedrunnersscored")
    innings_pitched_per_game: Optional[str] = Field(default=None, alias="inningspitchedpergame")
    flyball_percentage: Optional[str] = Field(default=None, alias="flyballpercentage")


class PitchingSabermetrics(Split):
    """
    A class to represent pitching sabermetric statistics.

    Attributes
    ----------
    stat : Sabermetrics
        The sabermetric statistics.
    """
    _stat: ClassVar[List[str]] = ['sabermetrics']
    stat: Sabermetrics


class PitchingSeason(Split):
    """
    A class to represent a pitching season statistic.

    Attributes
    ----------
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['season', 'statsSingleSeason']
    stat: SimplePitchingSplit


class PitchingCareer(Split):
    """
    A class to represent a pitching career statistic.

    Attributes
    ----------
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['career']
    stat: SimplePitchingSplit


class PitchingCareerAdvanced(Split):
    """
    A class to represent a pitching careerAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedPitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['careerAdvanced']
    stat: AdvancedPitchingSplit


class PitchingYearByYear(Split):
    """
    A class to represent a pitching yearByYear statistic.

    Attributes
    ----------
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYear']
    stat: SimplePitchingSplit


class PitchingYearByYearPlayoffs(Split):
    """
    A class to represent a pitching yearByYearPlayoffs statistic.

    Attributes
    ----------
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearPlayoffs']
    stat: SimplePitchingSplit


class PitchingYearByYearAdvanced(Split):
    """
    A class to represent a pitching yearByYearAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedPitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['yearByYearAdvanced']
    stat: AdvancedPitchingSplit


class PitchingSeasonAdvanced(Split):
    """
    A class to represent a pitching seasonAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedPitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['seasonAdvanced']
    stat: AdvancedPitchingSplit


class PitchingSingleSeasonAdvanced(Split):
    """
    A class to represent a pitching statsSingleSeasonAdvanced statistic.

    Attributes
    ----------
    stat : AdvancedPitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['statsSingleSeasonAdvanced']
    stat: AdvancedPitchingSplit


class PitchingGameLog(Split):
    """
    A class to represent a gamelog stat for a pitcher.

    Attributes
    ----------
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
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['gameLog']
    is_home: bool = Field(alias="ishome")
    is_win: bool = Field(alias="iswin")
    game: Game
    date: str
    opponent: Team
    stat: SimplePitchingSplit


class PitchingPlay(MLBBaseModel):
    """
    A class to represent a play stat for a pitcher.

    Attributes
    ----------
    details : PlayDetails
        Play details.
    count : Count
        The count.
    pitch_number : int
        Pitch number.
    at_bat_number : int
        At bat number.
    is_pitch : bool
        Is pitch bool.
    play_id : str
        Play ID.
    """
    details: PlayDetails
    count: Count
    pitch_number: int = Field(alias="pitchnumber")
    at_bat_number: int = Field(alias="atbatnumber")
    is_pitch: bool = Field(alias="ispitch")
    play_id: str = Field(alias="playid")


class PitchingLog(Split):
    """
    A class to represent a pitchLog stat for a pitcher.

    Attributes
    ----------
    stat : PitchingPlay
        Information regarding the play for the stat.
    season : str
        Season for the stat.
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
    _stat: ClassVar[List[str]] = ['pitchLog']
    stat: PitchingPlay
    season: str
    opponent: Team
    date: str
    is_home: bool = Field(alias="ishome")
    pitcher: Pitcher
    batter: Batter
    game: Game

    @field_validator('stat', mode='before')
    @classmethod
    def extract_play(cls, v: Any) -> Any:
        """Extract play from stat dict."""
        if isinstance(v, dict) and 'play' in v:
            return v['play']
        return v


class PitchingPlayLog(Split):
    """
    A class to represent a playLog stat for a pitcher.

    Attributes
    ----------
    stat : PitchingPlay
        Information regarding the play for the stat.
    season : str
        Season for the stat.
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
    stat: PitchingPlay
    season: str
    opponent: Team
    date: str
    is_home: bool = Field(alias="ishome")
    pitcher: Pitcher
    batter: Batter
    game: Game

    @field_validator('stat', mode='before')
    @classmethod
    def extract_play(cls, v: Any) -> Any:
        """Extract play from stat dict."""
        if isinstance(v, dict) and 'play' in v:
            return v['play']
        return v


class PitchingByDateRange(Split):
    """
    A class to represent a byDateRange stat for a pitcher.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRange']
    stat: SimplePitchingSplit
    day_of_week: Optional[int] = Field(default=None, alias="dayofweek")


class PitchingByDateRangeAdvanced(Split):
    """
    A class to represent a byDateRangeAdvanced stat for a pitcher.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : AdvancedPitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDateRangeAdvanced']
    stat: AdvancedPitchingSplit
    day_of_week: Optional[int] = Field(default=None, alias="dayofweek")


class PitchingByMonth(Split):
    """
    A class to represent a byMonth stat for a pitcher.

    Attributes
    ----------
    month : int
        The month.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonth']
    month: int
    stat: SimplePitchingSplit


class PitchingByMonthPlayoffs(Split):
    """
    A class to represent a byMonthPlayoffs stat for a pitcher.

    Attributes
    ----------
    month : int
        The month.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byMonthPlayoffs']
    month: int
    stat: SimplePitchingSplit


class PitchingByDayOfWeek(Split):
    """
    A class to represent a byDayOfWeek stat for a pitcher.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeek']
    stat: SimplePitchingSplit
    day_of_week: Optional[int] = Field(default=None, alias="dayofweek")


class PitchingByDayOfWeekPlayOffs(Split):
    """
    A class to represent a byDayOfWeekPlayoffs stat for a pitcher.

    Attributes
    ----------
    day_of_week : int
        The day of the week.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['byDayOfWeekPlayoffs']
    stat: SimplePitchingSplit
    day_of_week: Optional[int] = Field(default=None, alias="dayofweek")


class PitchingHomeAndAway(Split):
    """
    A class to represent a homeAndAway stat for a pitcher.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAway']
    is_home: bool = Field(alias="ishome")
    stat: SimplePitchingSplit


class PitchingHomeAndAwayPlayoffs(Split):
    """
    A class to represent a homeAndAwayPlayoffs stat for a pitcher.

    Attributes
    ----------
    is_home : bool
        Is home bool.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['homeAndAwayPlayoffs']
    is_home: bool = Field(alias="ishome")
    stat: SimplePitchingSplit


class PitchingWinLoss(Split):
    """
    A class to represent a winLoss stat for a pitcher.

    Attributes
    ----------
    is_win : bool
        Is win bool.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['winLoss']
    is_win: bool = Field(alias="iswin")
    stat: SimplePitchingSplit


class PitchingWinLossPlayoffs(Split):
    """
    A class to represent a winLossPlayoffs stat for a pitcher.

    Attributes
    ----------
    is_win : bool
        Is win bool.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['winLossPlayoffs']
    is_win: bool = Field(alias="iswin")
    stat: SimplePitchingSplit


class PitchingRankings(Split):
    """
    A class to represent a rankingsByYear stat for a pitcher.

    Attributes
    ----------
    outs_pitched : int
        Outs pitched.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['rankingsByYear']
    stat: SimplePitchingSplit
    outs_pitched: Optional[int] = Field(default=None, alias="outspitched")


class PitchingOpponentsFaced(Split):
    """
    A class to represent an opponentsFaced stat for a pitcher.

    Attributes
    ----------
    group : str
        The stat group.
    pitcher : Pitcher
        The pitcher.
    batter : Batter
        The batter.
    batting_team : Team
        The batting team.
    """
    _stat: ClassVar[List[str]] = ['opponentsFaced']
    group: str
    pitcher: Pitcher
    batter: Batter
    batting_team: Team = Field(alias="battingteam")


class PitchingExpectedStatistics(Split):
    """
    A class to represent an expectedStatistics stat for a pitcher.

    Attributes
    ----------
    stat : ExpectedStatistics
        The expected statistics.
    """
    _stat: ClassVar[List[str]] = ['expectedStatistics']
    stat: ExpectedStatistics


class PitchingVsPlayer5Y(Split):
    """
    A class to represent a vsPlayer5Y pitching statistic.

    Requires the use of opposingPlayerId params.

    Attributes
    ----------
    opponent : Team
        The opponent team.
    batter : Batter
        The batter.
    pitcher : Pitcher
        The pitcher.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayer5Y']
    opponent: Team
    stat: SimplePitchingSplit
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class PitchingVsPlayer(Split):
    """
    A class to represent a vsPlayer pitching statistic.

    Requires the use of opposingPlayerId params.

    Attributes
    ----------
    opponent : Team
        The opponent team.
    batter : Batter
        The batter.
    pitcher : Pitcher
        The pitcher.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayer']
    opponent: Team
    stat: SimplePitchingSplit
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class PitchingVsPlayerTotal(Split):
    """
    A class to represent a vsPlayerTotal pitching statistic.

    Requires the use of opposingPlayerId params.

    Attributes
    ----------
    opponent : Team
        The opponent team.
    batter : Batter
        The batter.
    pitcher : Pitcher
        The pitcher.
    stat : SimplePitchingSplit
        The pitching split stat.
    """
    _stat: ClassVar[List[str]] = ['vsPlayerTotal']
    stat: SimplePitchingSplit
    opponent: Optional[Team] = None
    batter: Optional[Batter] = None
    pitcher: Optional[Pitcher] = None

    @field_validator('opponent', 'batter', 'pitcher', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


# These stat_types return a hitting stat for a pitching stat group
class PitchingVsTeam(Split):
    """
    A class to represent a vsTeam pitching statistic.

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


class PitchingVsTeamTotal(Split):
    """
    A class to represent a vsTeamTotal pitching statistic.

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


class PitchingVsTeam5Y(Split):
    """
    A class to represent a vsTeam5Y pitching statistic.

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
