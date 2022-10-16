from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

@dataclass
class SeasonHitting(Stats):
    type_ = "season"
    gamesplayed : int
    groundouts : int 
    airouts : int
    runs : int
    doubles : int 
    triples : int 
    homeruns : int 
    strikeouts : int 
    baseonballs : int 
    intentionalwalks : int 
    hits : int 
    hitbypitch : int
    avg : str
    atbats : int 
    obp : str
    slg : str
    ops : str
    caughtstealing : int 
    stolenbases : int
    stolenbasepercentage : int 
    groundintodoubleplay : int 
    numberofpitches : int 
    plateappearances : int 
    totalbases : int
    rbi : int 
    leftonbase : int 
    sacbunts : int 
    sacflies : int 
    babip : str 
    groundoutstoairouts : int
    catchersinterference : int 
    atbatsperhomerun : int
    gametype : Optional[str] = None
    numteams : Optional[str] = None
    season : Optional[str] = None


@dataclass
class SeasonAdvancedHitting(Stats):
    type_ = "seasonadvanced"
    plateappearances : int
    totalbases : int
    leftonbase : int
    sacbunts : int
    sacflies : int
    babip : str
    extrabasehits : int
    hitbypitch : int
    gidp : int
    gidpopp : int
    numberofpitches : int
    pitchesperplateappearance : str
    walksperplateappearance : str
    strikeoutsperplateappearance : str
    homerunsperplateappearance : str
    walksperstrikeout : str
    iso : str
    reachedonerror : int
    walkoffs : int
    flyouts : int
    totalswings : int
    swingandmisses : int
    ballsinplay : int
    popouts : int
    lineouts : int
    groundouts : int
    flyhits : int
    pophits : int
    groundhits : int
    linehits : int
    gametype : Optional[str] = None
    numteams : Optional[str] = None
    season : Optional[str] = None
