from dataclasses import InitVar, dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.game import Game

from .stats import Stats, CodeDesc, Count

@dataclass
class SimplePitching:
    """
    A class to represent a advanced pitching statistics
    """
    gamesplayed: Optional[int] = None
    gamesstarted: Optional[int] = None
    groundouts: Optional[int] = None
    airouts: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeruns: Optional[int] = None
    strikeouts: Optional[int] = None
    baseonballs: Optional[int] = None
    intentionalwalks: Optional[int] = None
    hits: Optional[int] = None
    hitbypitch: Optional[int] = None
    avg: Optional[str] = None
    atbats: Optional[int] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[str] = None
    groundintodoubleplay: Optional[int] = None
    numberofpitches: Optional[int] = None
    era: Optional[str] = None
    inningspitched: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    saves: Optional[int] = None
    saveopportunities: Optional[int] = None
    holds: Optional[int] = None
    blownsaves: Optional[int] = None
    earnedruns: Optional[int] = None
    whip: Optional[str] = None
    outs: Optional[int] = None
    gamespitched: Optional[int] = None
    completegames: Optional[int] = None
    shutouts: Optional[int] = None
    strikes: Optional[int] = None
    strikepercentage: Optional[str] = None
    hitbatsmen: Optional[int] = None
    balks: Optional[int] = None
    wildpitches: Optional[int] = None
    pickoffs: Optional[int] = None
    totalbases: Optional[int] = None
    groundoutstoairouts: Optional[str] = None
    winpercentage: Optional[str] = None
    pitchesperinning: Optional[str] = None
    gamesfinished: Optional[int] = None
    strikeoutwalkratio: Optional[str] = None
    strikeoutsper9inn: Optional[str] = None
    walksper9inn: Optional[str] = None
    hitsper9inn: Optional[str] = None
    runsscoredper9: Optional[str] = None
    homerunsper9: Optional[str] = None
    catchersinterference: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    battersfaced: Optional[int] = None
    inheritedrunners: Optional[int] = None
    inheritedrunnersscored: Optional[int] = None

@dataclass
class AdvancedPitching:
    """
    A class to represent a advanced pitching statistics
    """
    winningpercentage: Optional[str] = None
    runsscoredper9: Optional[str] = None
    battersfaced: Optional[int] = None
    babip: Optional[str] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    strikeoutsper9: Optional[str] = None
    baseonballsper9: Optional[str] = None
    homerunsper9: Optional[str] = None
    hitsper9: Optional[str] = None
    strikesoutstowalks: Optional[str] = None
    stolenbases: Optional[int] = None
    caughtstealing: Optional[int] = None
    qualitystarts: Optional[int] = None
    gamesfinished: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    gidp: Optional[int] = None
    gidpopp: Optional[int] = None
    wildpitches: Optional[int] = None
    balks: Optional[int] = None
    pickoffs: Optional[int] = None
    totalswings: Optional[int] = None
    swingandmisses: Optional[int] = None
    ballsinplay: Optional[int] = None
    runsupport: Optional[int] = None
    strikepercentage: Optional[str] = None
    pitchesperinning: Optional[str] = None
    pitchesperplateappearance: Optional[str] = None
    walksperplateappearance: Optional[str] = None
    strikeoutsperplateappearance: Optional[str] = None
    homerunsperplateappearance: Optional[str] = None
    walksperstrikeout: Optional[str] = None
    iso: Optional[str] = None
    flyouts: Optional[int] = None
    popouts: Optional[int] = None
    lineouts: Optional[int] = None
    groundouts: Optional[int] = None
    flyhits: Optional[int] = None
    pophits: Optional[int] = None
    linehits: Optional[int] = None
    groundhits: Optional[int] = None
    inheritedrunners: Optional[int] = None
    inheritedrunnersscored: Optional[int] = None
    bequeathedrunners: Optional[int] = None
    bequeathedrunnersscored: Optional[int] = None

@dataclass(kw_only=True)
class PitchingSabermetrics(Stats):
    """
    A class to represent a pitching sabermetric statistics

    Attributes
    ----------
    fip : float
        Fielding Independent Pitching
    fipminus : float
        Fielding Independent Pitching Minus
    ra9war : float
        Runs Allowed 9 innings Wins Above Replacement
    rar : float 
        Runs Above Replacement
    war : float
        Wins Above Replacement
    gametype : str
        the gametype code of the pitching season 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = ['sabermetrics']
    gametype: str
    fip: float
    fipminus: float
    ra9war: float
    rar: float
    war: float
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingSeason(Stats, SimplePitching):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    gametype : str
        the gametype code of the pitching season 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'season', 'statsSingleSeason' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingCareer(Stats, SimplePitching):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'career']
    gametype: Optional[str] = None
    numteams: Optional[int] = None

@dataclass(kw_only=True)
class PitchingCareerAdvanced(Stats, AdvancedPitching):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'careerAdvanced' ]
    gametype: Optional[str] = None
    numteams: Optional[int] = None

@dataclass(kw_only=True)
class PitchingYBY(Stats, SimplePitching):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'yearByYear' ]
    numteams: Optional[str] = None
    gametype: Optional[str] = None

@dataclass(kw_only=True)
class PitchingYBYPlayoffs(Stats, SimplePitching):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'yearByYearPlayoffs' ]
    numteams: Optional[str] = None
    gametype: Optional[str] = None

@dataclass(kw_only=True)
class PitchingYBYAdvanced(Stats, AdvancedPitching):
    """
    A class to represent a pitching yearByYear statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'yearByYearAdvanced' ]
    numteams: Optional[str] = None
    gametype: Optional[str] = None

@dataclass(kw_only=True)
class PitchingSeasonAdvanced(Stats, AdvancedPitching):
    """
    A class to represent a pitching seasonAdvanced statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching season 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ "seasonAdvanced", 'statsSingleSeasonAdvanced' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingGameLog(Stats, SimplePitching):
    """
    A class to represent a gamelog stat for a pitcher

    Attributes
    ----------
    ishome : bool
        bool to hold ishome
    iswin : bool
        bool to hold iswin
    game : Game
        Game of the log
    date : str
        date of the log
    gametype : str
        type of game
    opponent : Team
        Team of the opponent
    """
    ishome: bool
    iswin: bool
    game: Union[Game, dict]
    date: str
    gametype: str
    opponent: Union[Team, dict]
    type_ = [ 'gameLog' ]

@dataclass
class PlayDetails:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    call : dict
        play call code and description
    description : str
        description of the play
    event : str
        type of event
    eventtype : str
        type of event
    isinplay : bool
        is the ball in play true or false
    isstrike : bool
        is the ball a strike true or false
    isball : bool
        is it a ball true or false
    isbasehit : bool
        is the event a base hit true or false
    isatbat : bool
        is the event at bat true or false
    isplateappearance : bool
        is the event a at play appears true or false
    type : dict
        type of pitch code and description
    batside : dict
        bat side code and description
    pitchhand : dict
        pitch hand code and description
    """
    call: Union[CodeDesc, dict]
    event: str
    eventtype: str
    isinplay: bool
    isstrike: bool
    isball: bool
    isbasehit: bool
    isatbat: bool
    isplateappearance: bool
    type: Union[CodeDesc, dict]
    batside: Union[CodeDesc, dict]
    pitchhand: Union[CodeDesc, dict]
    description: Optional[str] = None

@dataclass(kw_only=True)
class PitchingLog(Stats):
    """
    A class to represent a gamelog stat for a pitcher

    Attributes
    ----------
    season : str
        season for the stat
    stat : PlayLog
        information regarding the play for the stat
    team : Team
        team of the stat
    player : Person
        player of the stat
    opponent : Team
        opponent
    date : str
        date of log
    gametype : str
        game type code
    ishome : bool
        is the game at home bool
    pitcher : Person
        pitcher of the log
    batter : Person
        batter of the log
    game : Game
        the game of the log

    """
    type_ = [ 'pitchLog' ]
    season: str
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    playid: str
    pitchnumber: int
    atbatnumber: int
    ispitch: bool

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

@dataclass(kw_only=True)
class PitchingPlayLog(Stats):
    """
    A class to represent a gamelog stat for a pitcher

    Attributes
    ----------
    season : str
        season for the stat
    stat : PlayLog
        information regarding the play for the stat
    team : Team
        team of the stat
    player : Person
        player of the stat
    opponent : Team
        opponent
    date : str
        date of log
    gametype : str
        game type code
    ishome : bool
        is the game at home bool
    pitcher : Person
        pitcher of the log
    batter : Person
        batter of the log
    game : Game
        the game of the log

    """
    type_ = [ 'playLog' ]
    season: str
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    playid: str
    pitchnumber: int
    atbatnumber: int
    ispitch: bool

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)


@dataclass(kw_only=True)
class PitchingByDateRange(Stats, SimplePitching):
    """
    A class to represent a byDateRange stat for a pitcher

    Attributes
    ----------
    daysofweek : int
    numteams : int
    daysofweek : int

    """
    type_ = [ 'byDateRange' ]
    daysofweek: int
    numteams: int
    daysofweek: Optional[int] = None

@dataclass(kw_only=True)
class PitchingByDateRangeAdvanced(Stats, AdvancedPitching):
    """
    A class to represent a byDateRangeAdvanced stat for a pitcher

    Attributes
    ----------
    numteams : int
    daysofweek : int
    """
    type_ = [ 'byDateRangeAdvanced' ]
    numteams: int
    daysofweek: Optional[int] = None

@dataclass(kw_only=True)
class PitchingByMonth(Stats, SimplePitching):
    """
    A class to represent a byMonthPlayoffs stat for a pitcher

    Attributes
    ----------
    month : int
    numteams : int

    """
    type_ = [ 'byMonth', 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class PitchingByMonthPlayoffs(Stats, SimplePitching):
    """
    A class to represent a byMonthPlayoffs stat for a pitcher

    Attributes
    ----------
    month : int
    numteams : int
    """
    type_ = [ 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class PitchingByDayOfWeek(Stats, SimplePitching):
    """
    A class to represent a byDayOfWeek stat for a pitcher

    Attributes
    ----------
    dayofweek : int
    daysofweek : int
    numteams: int

    """
    type_ = [ 'byDayOfWeek' ]
    dayofweek: int
    daysofweek: Optional[int] = None
    numteams: int

@dataclass(kw_only=True)
class PitchingByDayOfWeekPlayOffs(Stats, SimplePitching):
    """
    A class to represent a byDayOfWeekPlayoffs stat for a pitcher

    Attributes
    ----------
    daysofweek : int
    daysofweek : int
    numteams : int

    """
    type_ = [ 'byDayOfWeekPlayoffs' ]
    dayofweek: int
    daysofweek: Optional[int] = None
    numteams: int

@dataclass(kw_only=True)
class PitchingHAA(Stats, SimplePitching):
    """
    A class to represent a homeAndAway stat for a pitcher

    Attributes
    ----------
    ishome : bool

    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class PitchingHAAPlayoffs(Stats, SimplePitching):
    """
    A class to represent a homeAndAwayPlayoffs stat for a pitcher

    Attributes
    ----------
    ishome : bool
    """
    type_ = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class PitchingWL(Stats, SimplePitching):
    """
    A class to represent a winLoss stat for a pitcher

    Attributes
    ----------
    iswin : bool
    """
    type_ = [ 'winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class PitchingWLPlayoffs(Stats, SimplePitching):
    """
    A class to represent a winLossPlayoffs stat for a pitcher

    Attributes
    ----------
    iswin : bool
    """
    type_ = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class PitchingRankings(Stats, SimplePitching):
    """
    A class to represent a rankings stat for a pitcher

    Attributes
    ----------
    gametype : str
    """
    type_ = [ 'rankings', 'rankingsByYear' ]
    gametype: str

@dataclass(kw_only=True)
class PitchingOpponentsFaced(Stats):
    """
    A class to represent a opponentsFaced stat for a pitcher

    Attributes
    ----------
    gametype : str
    group : str
    pitch : Person
    batter : Person
    battingteam : Team
    """
    type_ = [ 'opponentsFaced' ]
    gametype: str
    group: str
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    battingteam: Union[Team, dict]


