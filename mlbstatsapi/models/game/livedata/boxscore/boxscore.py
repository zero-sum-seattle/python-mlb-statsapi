from typing import Union, List
from pydantic import BaseModel
from .attributes import BoxScoreTeams, BoxScoreOffical, BoxScoreVL

class BoxScore(BaseModel):
    """Represents the box score of this game.

    Attributes:
        teams (BoxScoreTeams): Box score data for each team, detailing their performance in the game.
        officials (List[BoxScoreOfficial]): A list of officials overseeing this game.
        info (List[BoxScoreVL]): General box score information, potentially including various statistics and notable events.
        pitchingNotes (List[str]): Notes regarding pitching during the game, such as remarkable achievements or critical plays.
    """
    teams: BoxScoreTeams
    officials: List[BoxScoreOffical]
    info: List[BoxScoreVL]
    pitchingNotes: List[str]

