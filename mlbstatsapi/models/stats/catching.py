from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

@dataclass
class SimpleCatching(Stats):
    type_ = [ 'season' ]
    gamesplayed : Optional[int] = None
    runs : Optional[int] = None
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
    stolenbasepercentage : Optional[str] = None
    earnedruns : Optional[int] = None
    battersfaced : Optional[int] = None
    gamespitched : Optional[int] = None
    hitbatsmen : Optional[int] = None
    wildpitches : Optional[int] = None
    pickoffs : Optional[int] = None
    totalbases : Optional[int] = None
    strikeoutwalkratio : Optional[str] = None
    catchersinterference : Optional[int] = None
    sacbunts : Optional[int] = None
    sacflies : Optional[int] = None
    passedball : Optional[int] = None