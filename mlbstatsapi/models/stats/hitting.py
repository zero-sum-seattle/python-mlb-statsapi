from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats
 
@dataclass
class AdvancedHitting(Stats):
    type_ = [ "seasonAdvanced" ]
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
    type_ = [ 'yearByYear', 'projectedros', 'season', 'projectedros', 'projected' ]
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