from typing import Union, List, Optional
from pydantic import BaseModel

from mlbstatsapi.models.game.livedata.plays.play import Play
from mlbstatsapi.models.game.livedata.plays.playbyinning import PlayByInning


class Plays(BaseModel):
    """Represents the plays in a game.

    Attributes:
        allplays (Union[List[Play]]): All the plays in this game.
        currentplay (Optional[Play]): The current play in this game. Defaults to None.
        scoringplays (List[int]): Indices of scoring plays in `allPlays`.
        playsbyinning (List[PlayByInning]): Plays organized by inning.
    """
    allPlays: List[Play]
    scoringPlays: List[int]
    playsByInning: List[PlayByInning]
    currentPlay: Optional[Play] = None