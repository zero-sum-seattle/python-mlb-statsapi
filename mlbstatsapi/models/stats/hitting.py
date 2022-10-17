from dataclasses import dataclass, field
from optparse import Option
from typing import Optional, Union

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

from .stats import Stats
 

@dataclass
class AdvancedHitting(Stats):
    """
    A class to represent a advanced hitting statistics

    Used for the following stat types:
    seasonAdvanced, careerAdvanced
    """
    type_ = [ 'seasonAdvanced', 'careerAdvanced', 'yearByYearAdvanced' ]
    plateappearances : Optional[int] = None
    totalbases : Optional[int] = None
    leftonbase : Optional[int] = None
    sacbunts : Optional[int] = None
    sacflies : Optional[int] = None
    babip : Optional[str] = None
    extrabasehits : Optional[int] = None
    hitbypitch : Optional[int] = None
    gidp : Optional[int] = None
    gidpopp : Optional[int] = None
    numberofpitches : Optional[int] = None
    pitchesperplateappearance : Optional[str] = None
    walksperplateappearance : Optional[str] = None
    strikeoutsperplateappearance : Optional[str] = None
    homerunsperplateappearance : Optional[str] = None
    walksperstrikeout : Optional[str]= None
    iso : Optional[str] = None
    reachedonerror : Optional[int] = None
    walkoffs : Optional[int] = None
    flyouts : Optional[int] = None
    totalswings : Optional[int] = None
    swingandmisses : Optional[int] = None
    ballsinplay : Optional[int] = None
    popouts : Optional[int] = None
    lineouts : Optional[int] = None
    groundouts : Optional[int] = None
    flyhits : Optional[int] = None
    pophits : Optional[int] = None
    groundhits : Optional[int] = None
    linehits : Optional[int] = None

@dataclass
class SimpleHitting(Stats):
    """
    A class to represent a simple hitting statistics

    Used for the following stat types:
    yearByYear, projectedros, season, projectedros, projected, career, careerPlayoffs, yearByYearPlayoffs
    """
    type_ = [ 'yearByYear', 'projectedros', 'season', 'projectedros', 'projected', 'career', 
    'careerPlayoffs', 'yearByYearPlayoffs' ]
    gamesplayed : Optional[int] = None
    groundouts : Optional[int] = None
    airouts : Optional[int] = None
    runs : Optional[int] = None
    doubles : Optional[int] = None
    triples : Optional[int] = None
    homeruns : Optional[int] = None
    strikeouts : Optional[int] = None
    baseonballs : Optional[int] = None
    intentionalwalks : Optional[int] = None
    hits : Optional[int] = None
    hitbypitch : Optional[int] = None
    avg : Optional[str] = None
    atbats : Optional[int] = None
    obp : Optional[str] = None
    slg : Optional[str] = None
    ops : Optional[str] = None
    caughtstealing : Optional[int] = None
    stolenbases : Optional[int] = None
    stolenbasepercentage : Optional[int] = None
    groundintodoubleplay : Optional[int] = None
    numberofpitches : Optional[int] = None
    plateappearances : Optional[int] = None
    totalbases : Optional[int] = None
    rbi : Optional[int] = None
    leftonbase : Optional[int] = None
    sacbunts : Optional[int] = None
    sacflies : Optional[int] = None
    babip : Optional[str] = None
    groundoutstoairouts : Optional[int] = None
    catchersinterference : Optional[int] = None
    atbatsperhomerun : Optional[int] = None

class HittingSabermetrics(Stats):
    """
    A class to represent a hitting sabermetric statistic

    Used for the following stat types:
    seasonAdvanced, careerAdvanced
    """
    type_ = [ 'sabermetrics' ]
    woba : float
    wrc : float
    wrcplus : float
    rar : float
    war : float

class OpponentsFacedHitting(Stats):
    """
    A class to represent a hitting sabermetric statistic

    Used for the following stat types:
    opponentsFaced

    Attributes
    ----------
    batter : Person
        the batter of that stat object
    fieldingteam : Team
        the defence team of the stat object
    group : str
        the stat group of the stat
    pitcher : Person
        the pitcher of that stat object
    """
    type_ = [ 'opponentsFaced' ]
    batter : Union[Person, dict]
    fieldingteam : Union[Team, dict]
    group : str
    pitcher : Union[Person, dict]

    def __post_init__(self):
        self.fieldingteam = Team(**self.fieldingteam) if self.fieldingteam else self.fieldingteam
        self.batter = Person(**self.batter) if self.batter else self.batter
        self.pitcher = Person(**self.pitcher) if self.pitcher else self.pitcher

