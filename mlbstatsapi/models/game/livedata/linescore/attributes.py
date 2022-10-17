from typing import Union, Optional
from dataclasses import dataclass
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

@dataclass
class LinescoreTeamScoreing:
    """
    A class to represent a games Linescore

    Attributes
    ----------
    hits : int
        Team hits for this inning
    errors : int
        Team errors for this inning
    leftonbase : int
        Player left on base for this inning
    runs : int = None
        Team runs for this inning
    iswinner : bool = None
        If team is winner
    """
    hits: int
    errors: int
    leftonbase: int
    runs: Optional[int] = None
    iswinner: Optional[bool] = None

@dataclass
class LinescoreInning:
    """
    A class to represent a inning for a ames Linescore

    Attributes
    ----------
    num : int
        Inning number
    ordinalnum : str
        Inning ordinal
    home : LinescoreTeamScoreing
        Home team inning info
    away : LinescoreTeamScoreing
        Away team inning info
    """
    num: int
    ordinalnum: str
    home: Union[LinescoreTeamScoreing, dict]
    away: Union[LinescoreTeamScoreing, dict]

    def __post_init__(self):
        self.home = LinescoreTeamScoreing(**self.home)
        self.away = LinescoreTeamScoreing(**self.away)

@dataclass
class LinescoreTeams:
    """
    A class to represent home and away teams in the linescore

    Attributes
    ----------
    home : LinescoreTeamScoreing
        Home team current inning info
    away : LinescoreTeamScoreing
        Away team current inning info
    """
    home: Union[LinescoreTeamScoreing, dict]
    away: Union[LinescoreTeamScoreing, dict]

    def __post_init__(self):
        self.home = LinescoreTeamScoreing(**self.home)
        self.away = LinescoreTeamScoreing(**self.away)

@dataclass
class LinescoreOffense:
    """
    A class to represent a games current offense

    Attributes
    ----------
    batter : Person
        Current batter
    ondeck : Person
        Current on deck batter
    inhole : Person
        Current in the hole batter
    pitcher : Person
        Who is this teams pitcher
    battingorder : int
        Number in the batting order
    team : Team
        The team currently on offense
    """
    batter: Union[Person, dict]
    ondeck: Union[Person, dict]
    inhole: Union[Person, dict]
    pitcher: Union[Person, dict]
    battingorder: int
    team: Union[Team, dict]

    def __post_init__(self):
        self.batter = Person(**self.batter)
        self.ondeck = Person(**self.ondeck)
        self.inhole = Person(**self.inhole)
        self.pitcher = Person(**self.pitcher)
        self.team = Team(**self.team)

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
    ondeck : Person
        The next ondeck batter when this team switches to offense
    inhole : Person
        The next inHole batter when this team switches to offense
    battingorder : int
        Number this team is in the batting order
    team : Team
        The team that is playing defense currently
    """
    pitcher: Union[Person, dict]
    catcher: Union[Person, dict]
    first: Union[Person, dict]
    second: Union[Person, dict]
    third: Union[Person, dict]
    shortstop: Union[Person, dict]
    left: Union[Person, dict]
    center: Union[Person, dict]
    right: Union[Person, dict]
    batter: Union[Person, dict]
    ondeck: Union[Person, dict]
    inhole: Union[Person, dict]
    battingorder: int
    team: Union[Team, dict]

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
        self.ondeck = Person(**self.ondeck)
        self.inhole = Person(**self.inhole)
        self.team = Team(**self.team)