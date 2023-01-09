from typing import Union, Optional
from dataclasses import dataclass, field
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
    runs : int
        Team runs for this inning
    iswinner : bool
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
    A class to represent a inning for a games Linescore

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
        self.home = LinescoreTeamScoreing(**self.home) if self.home else self.home
        self.away = LinescoreTeamScoreing(**self.away) if self.away else self.away

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
    home: Union[LinescoreTeamScoreing, dict] = field(default_factory=dict)
    away: Union[LinescoreTeamScoreing, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.home = LinescoreTeamScoreing(**self.home) if self.home else self.home
        self.away = LinescoreTeamScoreing(**self.away) if self.away else self.away

@dataclass(repr=False)
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
    team: Union[Team, dict]
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    ondeck: Optional[Union[Person, dict]] = field(default_factory=dict)
    inhole: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)
    battingorder: Optional[int] = None
    first: Optional[str] = None
    second: Optional[str] = None
    third: Optional[str] = None

    def __post_init__(self):
        self.batter = Person(**self.batter) if self.batter else self.batter
        self.ondeck = Person(**self.ondeck) if self.ondeck else self.ondeck
        self.inhole = Person(**self.inhole) if self.inhole else self.inhole
        self.pitcher = Person(**self.pitcher) if self.pitcher else self.pitcher
        self.team = Team(**self.team)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
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
    team: Union[Team, dict]
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)
    catcher: Optional[Union[Person, dict]] = field(default_factory=dict)
    first: Optional[Union[Person, dict]] = field(default_factory=dict)
    second: Optional[Union[Person, dict]] = field(default_factory=dict)
    third: Optional[Union[Person, dict]] = field(default_factory=dict)
    shortstop: Optional[Union[Person, dict]] = field(default_factory=dict)
    left: Optional[Union[Person, dict]] = field(default_factory=dict)
    center: Optional[Union[Person, dict]] = field(default_factory=dict)
    right: Optional[Union[Person, dict]] = field(default_factory=dict)
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    ondeck: Optional[Union[Person, dict]] = field(default_factory=dict)
    inhole: Optional[Union[Person, dict]] = field(default_factory=dict)
    battingorder: int = None


    def __post_init__(self):
        self.pitcher = Person(**self.pitcher) if self.pitcher else self.pitcher
        self.catcher = Person(**self.catcher) if self.catcher else self.catcher
        self.first = Person(**self.first) if self.first else self.first
        self.second = Person(**self.second) if self.second else self.second
        self.third = Person(**self.third) if self.third else self.third
        self.shortstop = Person(**self.shortstop) if self.shortstop else self.shortstop
        self.left = Person(**self.left) if self.left else self.left
        self.center = Person(**self.center) if self.center else self.center
        self.right = Person(**self.right) if self.right else self.right
        self.batter = Person(**self.batter) if self.batter else self.batter
        self.ondeck = Person(**self.ondeck) if self.ondeck else self.ondeck
        self.inhole = Person(**self.inhole) if self.inhole else self.inhole
        self.team = Team(**self.team)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))