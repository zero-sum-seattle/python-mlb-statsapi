from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League

@dataclass(kw_only=True)
class Stats:
    team : Optional[Union[Team, dict]] = field(default_factory=dict)
    player : Optional[Union[Person, dict]] = field(default_factory=dict)
    league : Optional[Union[League, dict]] = field(default_factory=dict)
    sport : Optional[Union[Sport, dict]] = field(default_factory=dict)
    position : Optional[Union[Position, dict]] = field(default_factory=dict)
    gametype : Optional[str] = None
    numteams : Optional[str] = None
    season : Optional[str] = None
    
