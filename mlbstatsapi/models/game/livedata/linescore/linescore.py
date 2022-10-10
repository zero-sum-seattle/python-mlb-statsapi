from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

from mlbstatsapi.models.game.livedata.linescore.linescoreinning import LinescoreInning
from mlbstatsapi.models.game.livedata.linescore.linescoreteams import LinescoreTeams
from mlbstatsapi.models.game.livedata.linescore.linescoreoffense import LinescoreOffense

@dataclass
class LinescoreDefense:
    """
    A class to represent a games current defense

    Attributes
    ----------
    pitcher : Person
        Current pitcher
    catcher : Person
        Current catcher
    first : Person
        Current first
    second : Person
        Current second
    third : Person
        Current third
    shortstop : Person
        Current shortstop
    left : Person
        Current left
    center : Person
        Current center
    right : Person
        Current right
    batter : Person
        The next batter when this team switches to offense
    onDeck : Person
        The next ondeck batter when this team switches to offense
    inHole : Person
        The next inHole batter when this team switches to offense
    battingOrder : int
        Number this team is in the batting order
    team : Team
        The team that is playing defense currently
    """
    pitcher:        Union[Person, Dict[str, Any]]
    catcher:        Union[Person, Dict[str, Any]]
    first:          Union[Person, Dict[str, Any]]
    second:         Union[Person, Dict[str, Any]]
    third:          Union[Person, Dict[str, Any]]
    shortstop:      Union[Person, Dict[str, Any]]
    left:           Union[Person, Dict[str, Any]]
    center:         Union[Person, Dict[str, Any]]
    right:          Union[Person, Dict[str, Any]]
    batter:         Union[Person, Dict[str, Any]]
    onDeck:         Union[Person, Dict[str, Any]]
    inHole:         Union[Person, Dict[str, Any]]
    battingOrder:   int
    team:           Union[Team, Dict[str, Any]]

    def __post_init__(self):
        self.pitcher = Person(**self.pitcher)
        self.catcher = Person(**self.catcher)
        self.first = Person(**self.first)
        self.second = Person(**self.second)
        self.third = Person(**self.third)
        self.shortstop = Person(**self.shortstop)
        self.left = Person(**self.left)
        self.center = Person(**self.center)
        self.right = Person(**self.right)
        self.batter = Person(**self.batter)
        self.onDeck = Person(**self.onDeck)
        self.inHole = Person(**self.inHole)
        self.team = Team(**self.team)

@dataclass
class Linescore:
    """
    A class to represent a games Linescore

    Attributes
    ----------
    currentInning : int
        The games current inning
    currentInningOrdinal : str
        This innings ordinal
    inningState : str
        What state this inning is in
    inningHalf : str
        WHich half of the inning are we in
    isTopInning : bool
        Is this the top of the inning
    scheduledInnings : int
        How many innings are scheduled for this game
    innings : List[LinescoreInning]
        Data on each inning
    teams : LinescoreTeams
        Line score data on our teams
    defense : LinescoreDefense
        Current defense
    offense : LinescoreOffense
        Current offense
    balls : int
        current count balls
    strikes : int
        current count strikes
    outs : int
        current count outs
    """
    currentInning:          int
    currentInningOrdinal:   str
    inningState:            str
    inningHalf:             str
    isTopInning:            bool
    scheduledInnings:       int
    innings:                Union[List[LinescoreInning], List[Dict[str, Any]]]
    teams:                  Union[LinescoreTeams, Dict[str, Any]]
    defense:                Union[LinescoreDefense, Dict[str, Any]]
    offense:                Union[LinescoreOffense, Dict[str, Any]]
    balls:                  int
    strikes:                int
    outs:                   int

    def __post_init__(self):
        self.innings = [LinescoreInning(**inning) for inning in self.innings]
        self.teams = LinescoreTeams(**self.teams)
        self.defense = LinescoreDefense(**self.defense)
        self.offense = LinescoreOffense(**self.offense)
