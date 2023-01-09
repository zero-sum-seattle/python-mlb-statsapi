from typing import Union, List
from dataclasses import dataclass, field

from mlbstatsapi.models.game.livedata.plays.play import Play
from mlbstatsapi.models.game.livedata.plays.playbyinning import PlayByInning


@dataclass(repr=False)
class Plays:
    """
    A class to represent the plays in this game.

    Attributes
    ----------
    allplays : List[Play]
        All the plays in this game
    currentplay : Play
        The current play in this game
    scoringplays : List[int]
        Which plays are scoring plays, indexed with allPlays
    playsbyinning : List[PlayByInning]
        Plays by inning
    """
    allplays: Union[List[Play], List[dict]]
    scoringplays: List[int]
    playsbyinning: Union[List[PlayByInning], List[dict]]
    currentplay: Union[Play, dict] = field(default_factory=dict)


    def __post_init__(self):
        self.allplays = [Play(**play) for play in self.allplays if play]
        self.currentplay = Play(**self.currentplay) if self.currentplay else self.currentplay
        self.playsbyinning = [PlayByInning(**inning) for inning in self.playsbyinning if inning]

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))