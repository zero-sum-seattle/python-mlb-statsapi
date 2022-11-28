from dataclasses import InitVar, dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Pitcher, Batter
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from mlbstatsapi.mlb_module import merge_keys
from mlbstatsapi.models.data import (
    Count,
    PlayDetails,
)

from .stats import Stat, Sabermetrics, ExpectedStatistics
from .hitting import SimpleHittingSplit


@dataclass
class SimplePitchingSplit:
    """
    A class to represent a advanced pitching statistics

    attributes are all optional as there is no documentation for the stats endpoint

    Attributes
    ----------
    gamesplayed : int
        The games played by the pitcher.
    gamesstarted : int
        The games started by the pitcher.
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
    homeruns : int
        The number of home runs given up by the pitcher.
    strikeouts : int
        The number of strike outs performed by the pitcher.
    baseonballs : int
        The number of base on balls (walks) performed by the pitcher.
    intentionalwalks : int
        The number of intentional walks performed by the pitcher.
    hits : int
        The number of hits given up by the pitcher.
    hitbypitch : int
        The number of batters hit by the pitcher.
    avg : int
        The batting avg against the pitcher.
    atbats : int
        The at bats pitched by the pitcher.
    obp : str
        The on base percentage again the pitcher.
    slg : str
        The slugging percentage against the pitcher.
    ops : str
        The on base slugging against the pitcher.
        see also: https://www.mlb.com/glossary/standard-stats/on-base-plus-slugging
    caughtstealing : int
        The number of runners caught stealing against the pitcher.
    stolenbases : int
        The number of stolen bases while pitching.
    stolenbasepercentage : int
        The stolen base percentage while pitching.
    groundintodoubleplay : int
        The number of hits against 
    numberofpitches : int
        The number of pitches thrown.
    era : str
        The earned run average of the pitcher.
    inningspitched : int
        The number of innings pitched by the pitcher.
    wins : int
        The number of wins by the pitcher.
    losses : int
        The number of losses by the pitcher.
    saves : int
        The number of saves by the pitcher.
    saveopportunities : int
        The number of save opportunities by the pitcher.
    holds : int
        The number of holds by the pitcher.
    blownsaves : int
        The number of blown saves performed by the pitcher.
    earnedruns : int
        The number of earned runs given up by the pitcher.
    whip : str
        The number of walks and hits per inning pitched.
        see also: https://www.mlb.com/glossary/standard-stats/walks-and-hits-per-inning-pitched
    outs : int
        The number of outs 
    gamespitched : int
        The number of games pitched.
    completegames : int
        The number of complete games pitched.
    shutouts : int
        The number of shut outs pitched.
    strikes : int
        The number of strikes thown by the pitcher.
    hitbatsmen : int
        The number of batters hit by a pitch.
    strikepercentage : str
        The strike percentage thrown by the pitcher.
    wildpitches : int
        The number of wild pitches thown by the pitcher.
    balks : int
        The number of balks commited by the pitcher.
    totalbases : int
        The total bases given up by the pitcher.
    pickoffs : int
        The number of pick offs performed by the pitcher.
    winpercentage : str
        The winpercentage of the pitcher.
    groundoutstoairouts : str
        The groundout-to-airout ratio of the pitcher.
    gamesfinished : int
        The number of games finished by the pitcher.
    pitchesperinning : str
        The number of pitches thown per inning by the pitcher.
    strikeoutsper9inn : str
        The number of strike outs per 9 innings by the pitcher
    strikeoutwalkratio : str
        The strike out to walk ratio of the pitcher.
    hitsper9inn : str
        The number of hits per 9 innings pitched.
    walksper9inn : str
        The number of walks per 9 innings pitched.
    homerunsper9 : str
        The number of home runs per 9 innings pitched.
    runsscoredper9 : str
        The number of runs scored per 9 innings pitched.
    sacbunts : int
        The number of sac bunts given up when pitched.
    catchersinterference : int
        The number of times a runner has reached from catchers interference while pitching.
    battersfaced : int
        The number of batters faced by the pitcher.
    sacflies : int
        The number of sac flies given up by the pitcher.
    inheritedrunnersscored : int
        The number of inherited runners scored by the pitcher.
    inheritedrunners : int
        The number of inherited runners for the pitcher.
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
    balls: Optional[int] = None
    outspitched: Optional[int] = None
    rbi: Optional[int] = None

@dataclass
class AdvancedPitchingSplit:
    """
    A class to represent a advanced pitching statistics 
    
    winningpercentage : str
        The winning percentage of the pitcher.
    runsscoredper9 : str
        The number of runs scored per 9 innings
    battersfaced : int
        The number of batters faced
    babip : str
        The BABIP of the pitcher.
    obp : str
        The on base percentage again the pitcher.
    slg : str
        The slugging percentage against the pitcher.
    ops : str
        The on base slugging against the pitcher.
        see also: https://www.mlb.com/glossary/standard-stats/on-base-plus-slugging
    strikeoutsper9 : str
        The number of strike outs per 9 innings by the pitcher
    baseonballsper9 : str
        The number of base on balls per 9 innings by the pitcher.
    homerunsper9 : str
        The number of home runs per 9 innings by the pitcher.
    hitsper9 : str
        The number of hits per 9 innings by the pitcher.
    strikesoutstowalks : str
        The strike out to walk ratio of the pitcher.
    stolenbases : int
         The number of stolen bases while pitching.  
    caughtstealing : int
        The number of runners caught stealing by the pitcher.
    qualitystarts : int
        The number of quality starts performed by the pitcher.
    gamesfinished : int
        The number of games finished performed by the pitcher.
    doubles : int
        The number of doubles given up by the pitcher.
    triples : int
        The number of triples given up by the pitcher.
    gidp : int
        The amount of hits that lead to a double play.
        see here: https://www.mlb.com/glossary/standard-stats/ground-into-double-play
    gidpopp : int
        The amount of GIDP opportunities. 
    wildpitches : int
        The number of wild pitches thown by the pitcher.
    balks : int
        The number of balks commited by the pitcher.
    pickoffs : int
        The number of pick offs attempted by the pitcher.
    totalswings : int
        The number of swings against the pitcher.
    swingandmisses : int
        The number of swing and misses against the pitcher. 
    ballsinplay : int
        The number of balls put into play against the pitcher.
    runsupport : int
        The number of run support
    strikepercentage : str
        The strike percentage thown by the pitcher.
    pitchesperinning : str
        The number of pitches per inning
    pitchesperplateappearance : str
        The avg number of pitches per plate appearance of the pitcher.
    walksperplateappearance : str
        The number of walks per plate appearance for the pitcher.
    strikeoutsperplateappearance : str
        The strike outs per plate appearance for the pitcher.
    homerunsperplateappearance : str
        The home runs per plate appearance for the pitcher.
    walksperstrikeout : str
        The walk per strike out ratio of the pitcher
    iso : str
        Isolasted power.
        see also: https://www.mlb.com/glossary/advanced-stats/isolated-power
    flyouts : int
        The number of ly outs given up by the pitcher.
    popouts : int
        The number of pop outs given up by the pitcher.
    lineouts : int
        The number of line outs given up by the pitcher.
    groundouts : int
        The number of ground outs given up by the pitcher.
    flyhits : int
        The number of fly hits given up by the pitcher.
    pophits : int
        The number of pop hits given up by the pitcher.
    linehits : int
        The number of line hits given up by the pitcher.
    groundhits : int
        The number of ground hits given up by the pitcher.
    inheritedrunners : int
        The number of inherited runners for the pitcher.
    inheritedrunnersscored : int
        The number of inherited runners scored for the pitcher.
    bequeathedrunners : int
        The number of bequeathed runners.
        see also: https://www.mlb.com/glossary/advanced-stats/bequeathed-runners
    bequeathedrunnersscored : int
        The number of bequeathed runners scored.
        see also: https://www.mlb.com/glossary/advanced-stats/bequeathed-runners
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
class PitchingSabermetrics(Stat):
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
    _stat = ['sabermetrics']
    stat: Union[Sabermetrics, dict]

    def __post_init__(self):
        self.stat = Sabermetrics(**self.stat)


@dataclass(kw_only=True)
class PitchingSeason(Stat):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    """
    _stat = ['season', 'statsSingleSeason']
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingCareer(Stat):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    """
    _stat = ['career']
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingCareerAdvanced(Stat):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    """
    _stat = ['careerAdvanced']
    stat: Union[AdvancedPitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedPitchingSplit(**self.stat)


@dataclass(kw_only=True)
class PitchingYearByYear(Stat):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingYearByYearPlayoffs(Stat):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingYearByYearAdvanced(Stat):
    """
    A class to represent a pitching yearByYear statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearAdvanced']
    stat: Union[AdvancedPitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedPitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingSeasonAdvanced(Stat):
    """
    A class to represent a pitching seasonAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['seasonAdvanced']
    stat: Union[AdvancedPitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedPitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingSingleSeasonAdvanced(Stat):
    """
    A class to represent a pitching seasonAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['statsSingleSeasonAdvanced']
    stat: Union[AdvancedPitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedPitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingGameLog(Stat):
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
    opponent: Union[Team, dict]
    _stat = ['gameLog']
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass
class PitchingPlay:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    """
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    pitchnumber: int
    atbatnumber: int
    ispitch: bool
    playid: str

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

@dataclass(kw_only=True)
class PitchingLog(Stat):
    """
    A class to represent a pitchLog stat for a pitcher

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
    _stat = ['pitchLog']
    stat: Union[PitchingPlay, dict]
    season: str
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    game: Union[Game, dict]

    def __post_init__(self):
        self.stat = PitchingPlay(**merge_keys(self.stat, 'play'))

@dataclass(kw_only=True)
class PitchingPlayLog(Stat):
    """
    A class to represent a playLog stat for a pitcher

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
    _stat = ['playLog']
    stat: Union[PitchingPlay, dict]
    season: str
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    game: Union[Game, dict]

    def __post_init__(self):
        self.stat = PitchingPlay(**merge_keys(self.stat, 'play'))

@dataclass(kw_only=True)
class PitchingByDateRange(Stat):
    """
    A class to represent a byDateRange stat for a pitcher

    Attributes
    ----------
    dayofweek : int
    """
    _stat = ['byDateRange']
    dayofweek: Optional[int] = None
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingByDateRangeAdvanced(Stat):
    """
    A class to represent a byDateRangeAdvanced stat for a pitcher

    Attributes
    ----------
    dayofweek : int
    """
    _stat = ['byDateRangeAdvanced']
    dayofweek: Optional[int] = None
    stat: Union[AdvancedPitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedPitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingByMonth(Stat):
    """
    A class to represent a byMonthPlayoffs stat for a pitcher

    Attributes
    ----------
    month : int
    """
    _stat = ['byMonth']
    month: int
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingByMonthPlayoffs(Stat):
    """
    A class to represent a byMonthPlayoffs stat for a pitcher

    Attributes
    ----------
    month : int
    """
    _stat = ['byMonthPlayoffs']
    month: int
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingByDayOfWeek(Stat):
    """
    A class to represent a byDayOfWeek stat for a pitcher

    Attributes
    ----------
    dayofweek : int
    """
    _stat = ['byDayOfWeek']
    dayofweek: Optional[int] = None
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingByDayOfWeekPlayOffs(Stat):
    """
    A class to represent a byDayOfWeekPlayoffs stat for a pitcher

    Attributes
    ----------
    dayofweek : int
    """
    _stat = ['byDayOfWeekPlayoffs']
    dayofweek: Optional[int] = None
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingHomeAndAway(Stat):
    """
    A class to represent a homeAndAway stat for a pitcher

    Attributes
    ----------
    ishome : bool
    """
    _stat = ['homeAndAway']
    ishome: bool
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingHomeAndAwayPlayoffs(Stat):
    """
    A class to represent a homeAndAwayPlayoffs stat for a pitcher

    Attributes
    ----------
    ishome : bool
    """
    _stat = ['homeAndAwayPlayoffs']
    ishome: bool
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingWinLoss(Stat):
    """
    A class to represent a winLoss stat for a pitcher

    Attributes
    ----------
    iswin : bool
    """
    _stat = ['winLoss']
    iswin: bool
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingWinLossPlayoffs(Stat):
    """
    A class to represent a winLossPlayoffs stat for a pitcher

    Attributes
    ----------
    iswin : bool
    """
    _stat = ['winLossPlayoffs']
    iswin: bool
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingRankings(Stat):
    """
    A class to represent a rankings stat for a pitcher

    Attributes
    ----------
    """
    _stat = ['rankingsByYear']
    outspitched: Optional[int] = None
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingOpponentsFaced(Stat):
    """
    A class to represent a opponentsFaced stat for a pitcher

    Attributes
    ----------
    group : str
    pitch : Person
    batter : Person
    battingteam : Team
    """
    _stat = ['opponentsFaced']
    group: str
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    battingteam: Union[Team, dict]


@dataclass(kw_only=True)
class PitchingExpectedStatistics(Stat):
    """
    A class to represent a excepted statistics statType: expectedStatistics.

    Attributes
    ----------
    avg : str
    slg : str
    woba : str
    wobaCon : str
    rank : int
    """
    _stat = ['expectedStatistics']
    stat: Union[ExpectedStatistics, dict]



@dataclass(kw_only=True)
class PitchingVsPlayer5Y(Stat):
    """
    A class to represent a vsTeam pitching statistic

    Attributes
    ----------
    """
    _stat = ['vsPlayer5Y']
    opponent: Union[Team, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)    
    stat: Union[SimplePitchingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimplePitchingSplit(**self.stat)


# These stat_types return a hitting stat for a pitching stat group
# odd, but need to deal with it.
@dataclass(kw_only=True)
class PitchingVsTeam(Stat):
    """
    A class to represent a vsTeam pitching statistic

    Attributes
    ----------
    """
    _stat = ['vsTeam']
    opponent: Union[Team, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)    
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingVsTeamTotal(Stat):
    """
    A class to represent a vsTeamTotal pitching statistic

    Attributes
    ----------
    """
    _stat = ['vsTeamTotal']
    opponent: Union[Team, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)

@dataclass(kw_only=True)
class PitchingVsTeam5Y(Stat):
    """
    A class to represent a vsTeam5Y pitching statistic

    Attributes
    ----------
    """
    _stat = ['vsTeam5Y']
    opponent: Union[Team, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)

#
# These dataclasses are for the game stats end point only
# url: https://statsapi.mlb.com/api/v1/people/663728/stats/game/715757
# The gamelog stats in this JSON have different keys set for their stat
# and group. This breaks my logic of handling stat classes
#



@dataclass
class PitchingSplit:
    gamesplayed: int
    gamesstarted: int
    flyouts: int
    groundouts : int
    airouts: int
    runs: int
    doubles: int
    triples : int
    homeruns: int
    strikeouts: int
    baseonballs: int
    intentionalwalks: int
    hits: int
    hitbypitch: int
    atbats: int
    caughtstealing : int
    stolenbases : int
    stolenbasepercentage: str
    numberofpitches: int
    inningspitched: str
    wins: int
    losses: int
    saves: int
    saveopportunities: int
    holds: int
    blownsaves : int
    earnedruns: int
    battersfaced: int
    outs: int
    gamespitched: int
    completegames: int
    shutouts: int
    pitchesthrown: int
    balls: int
    strikes: int
    strikepercentage: str
    hitbatsmen: int
    balks: int
    wildpitches: int
    pickoffs: int
    rbi: int
    gamesfinished: int
    runsscoredper9: str 
    homerunsper9: str
    inheritedrunners: int
    inheritedrunnersscored: int
    catchersinterference: int
    sacbunts: int
    sacflies: int
    passedball: int


@dataclass
class PitchingGameLogStat:
    type: str
    group: str
    stat: Union[PitchingSplit, dict]
    _stat = ['pitching']

    def __post_init__(self):
        self.stat = PitchingSplit(**self.stat)


