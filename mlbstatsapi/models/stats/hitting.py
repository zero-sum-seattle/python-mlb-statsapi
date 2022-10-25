from dataclasses import dataclass, field
from typing import Optional, Union, List

import mlbstatsapi

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.game import Game

from .stats import Stats, CodeDesc, Count

@dataclass
class AdvancedHittingStat:
    """
    A class to represent a advanced hitting statistics

    Used for the following stat types:
    seasonAdvanced, careerAdvanced
    """
    plateappearances: Optional[int] = None
    totalbases: Optional[int] = None
    leftonbase: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    babip: Optional[str] = None
    extrabasehits: Optional[int] = None
    hitbypitch: Optional[int] = None
    gidp: Optional[int] = None
    gidpopp: Optional[int] = None
    numberofpitches: Optional[int] = None
    pitchesperplateappearance: Optional[str] = None
    walksperplateappearance: Optional[str] = None
    strikeoutsperplateappearance: Optional[str] = None
    homerunsperplateappearance: Optional[str] = None
    walksperstrikeout: Optional[str]= None
    iso: Optional[str] = None
    reachedonerror: Optional[int] = None
    walkoffs: Optional[int] = None
    flyouts: Optional[int] = None
    totalswings: Optional[int] = None
    swingandmisses: Optional[int] = None
    ballsinplay: Optional[int] = None
    popouts: Optional[int] = None
    lineouts: Optional[int] = None
    groundouts: Optional[int] = None
    flyhits: Optional[int] = None
    pophits: Optional[int] = None
    groundhits: Optional[int] = None
    linehits: Optional[int] = None

@dataclass
class SimpleHittingStat:
    """
    A class to represent a simple hitting statistics
    """
    gamesplayed: Optional[int] = None
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
    stolenbasepercentage: Optional[int] = None
    groundintodoubleplay: Optional[int] = None
    groundintotripleplay: Optional[int] = None
    numberofpitches: Optional[int] = None
    plateappearances: Optional[int] = None
    totalbases: Optional[int] = None
    rbi: Optional[int] = None
    leftonbase: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    babip: Optional[str] = None
    groundoutstoairouts: Optional[int] = None
    catchersinterference: Optional[int] = None
    atbatsperhomerun: Optional[int] = None

@dataclass(kw_only=True)
class HittingWL(Stats, SimpleHittingStat):
    """
    A class to represent a hitting winLoss or statistic

    Attributes
    ----------
    season : str
        the batter of the hitting winLoss
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    """
    type_ = [ 'winLoss', 'winLossPlayoffs' ]
    season: str
    iswin: bool

@dataclass(kw_only=True)
class HittingHAA(Stats, SimpleHittingStat):
    """
    A class to represent a hitting homeAndAway or statistic

    Attributes
    ----------
    season : str
        the batter of the hitting homeAndAway
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    """
    type_ = [ 'homeAndAway', 'homeAndAwayPlayoffs' ]
    season: str
    ishome: bool

@dataclass(kw_only=True)
class HittingCareer(Stats, SimpleHittingStat):
    """
    A class to represent a hitting career or careerPlayoffs statistic

    Attributes
    ----------
    season : str
        the batter of the hitting career
    gametype : Team
        the gametype code of the hitting career 
    player : Person
        the player of the hitting career
    sport : Sport
        the sport of the hitting career 
    league : League
        the league of the hitting career
    team : Team
        the team of the hitting career
    numteams : str
        the number of teams for the hitting career
    """
    type_ = [ 'career', 'careerPlayoffs', 'careerRegularSeason' ]
    season: str
    gametype: str
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingSeason(Stats, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    season : str
        the batter of the hitting season
    gametype : Team
        the gametype code of the hitting season 
    player : Person
        the player of the hitting season
    sport : Sport
        the sport of the hitting season 
    league : League
        the league of the hitting season
    team : Team
        the team of the hitting season
    numteams : str
        the number of teams for the hitting season
    """
    type_ = [ 'season', 'statsSingleSeason' ]
    season: str
    gametype: Optional[str] = None
    player: Optional[Union[Person, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingAdvancedSeason(Stats, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    season : str
        the batter of the hitting season
    gametype : Team
        the gametype code of the hitting season 
    player : Person
        the player of the hitting season
    sport : Sport
        the sport of the hitting season 
    league : League
        the league of the hitting season
    team : Team
        the team of the hitting season
    numteams : str
        the number of teams for the hitting season
    """
    type_ = [ 'careerAdvanced', 'seasonAdvanced' ]
    season: Optional[str] = None
    gametype: Optional[str] = None
    player: Optional[Union[Person, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingYBY(Stats, SimpleHittingStat):
    """
    A class to represent a hitting yearbyyear or yearByYearPlayoffs statistic

    Attributes
    ----------
    season : Person
        the batter of the hitting yearbyyear
    gametype : Team
        the gametype code of the hitting yearbyyear 
    player : Person
        the player of the hitting seayearbyyearson
    sport : Sport
        the sport of the hitting yearbyyear 
    league : League
        the league of the hitting yearbyyear
    team : Team
        the team of the hitting yearbyyear
    numteams : str
        the number of teams for the hitting yearbyyear
    """
    type_ = [ 'yearByYear', 'yearByYearPlayoffs' ]
    season: str
    gametype: Optional[str] = None
    player: Optional[Union[Person, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass
class OpponentsFacedHitting(Stats):
    """
    A class to represent a hitting opponentsFaced statistic

    Attributes
    ----------
    batter : Person
        the batter of that stat object
    fieldingteam : Team
        the defence team of the stat object
    pitcher : Person
        the pitcher of that stat object
    group : str
        stat group
    """
    type_ = [ 'opponentsFaced' ]
    group: str
    batter: Union[Person, dict]
    fieldingteam: Union[Team, dict]
    pitcher: Union[Person, dict]
    gametype: Optional[str]

@dataclass
class HittingSabermetrics(Stats):
    """
    A class to represent a hitting sabermetric statistic

    """
    type_ = [ 'sabermetrics' ]
    season: str
    gametype: str
    woba: float
    wrc: float
    wrcplus: float
    rar: float
    war: float
    player: Optional[Union[Person, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[int] = None

@dataclass(kw_only=True)
class HittingLog(Stats, SimpleHittingStat):
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    positionsplayed : List[Position]
    stat : SimpleHittingStat
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
    sport : Sport
        Sport of the stat
    league : League
        League of the stat
    player : Person
        Player of the stat
    """
    type_ = [ 'gameLog' ]
    positionsplayed: List[Position]
    ishome: bool
    iswin: bool
    game: Union[Game, dict]
    date: str
    gametype: str
    opponent: Union[Team, dict]
    sport: Union[Sport, dict]
    league: Union[League, dict]
    player: Union[Person, dict]

    def __post_init__(self):
        if self.positionsplayed:
            self.positionsplayed = [ Position(**position) for position in self.positionsplayed ]
        
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
    description: str
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

@dataclass
class HittingLog(Stats):
    """
    A class to represent a gamelog stat for a hitter

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
    type_ = [ 'playLog', 'pitchLog' ]
    season: str
    team: Union[Team, dict]
    player: Union[Person, dict]
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

@dataclass
class SprayChart(Stats):
    """
    centerfield : float
    leftcenterfield : float 
    leftfield : float
    rightcenterfield : float
    rightfield
    batter
    
    """
    type_ = [ 'sprayChart' ]
    batter: Union[Person, dict]
    centerfield: float
    leftcenterfield: float
    leftfield: float
    rightcenterfield: float
    rightfield: float

@dataclass(kw_only=True)
class HittingLastXGames(Stats, SimpleHittingStat):
    type_ = [ 'lastXGames' ]
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    numteams: int

@dataclass(kw_only=True)
class HittingDateRange(Stats, SimpleHittingStat):
    type_ = [ 'byDateRange' ]
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    numteams: int

@dataclass(kw_only=True)
class HittingDateRangeAdvanced(Stats, AdvancedHittingStat):
    type_ = [ 'byDateRangeAdvanced' ]
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    numteams: int

@dataclass(kw_only=True)
class HittingByMonth(Stats, AdvancedHittingStat):
    type_ = [ 'byMonthPlayoffs', 'byMonth' ]
    season: str
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    month: int
    numteams: int

@dataclass(kw_only=True)
class HittingDayOfWeek(Stats, SimpleHittingStat):
    type_ = [ 'byDayOfWeek', 'byDayOfWeekPlayoffs' ]
    season: str
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    month: int
    numteams: int


