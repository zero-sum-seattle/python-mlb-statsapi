from typing import List, Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import BoxScoreTeams, BoxScoreOfficial, BoxScoreVL, PlayersDictPerson


class TopPerformer(MLBBaseModel):
    """
    A class to represent this game's top performer.

    Attributes
    ----------
    player : PlayersDictPerson
        Player.
    type : str
        The type of top performer.
    game_score : int
        Game score.
    hitting_game_score : int
        Hitting game score.
    pitching_game_score : int
        Pitching game score.
    """
    player: PlayersDictPerson
    type: str
    game_score: int = Field(alias="gameScore")
    hitting_game_score: Optional[int] = Field(default=None, alias="hittingGameScore")
    pitching_game_score: Optional[int] = Field(default=None, alias="pitchingGameScore")


class BoxScore(MLBBaseModel):
    """
    A class to represent this game's boxscore.

    Attributes
    ----------
    teams : BoxScoreTeams
        Box score data for each team.
    officials : List[BoxScoreOfficial]
        The officials for this game.
    info : List[BoxScoreVL]
        Box score information.
    pitching_notes : List[str]
        Pitching notes for this game.
    top_performers : List[TopPerformer]
        Top performers for this game.
    """
    teams: BoxScoreTeams
    officials: List[BoxScoreOfficial] = []
    info: List[BoxScoreVL] = []
    pitching_notes: List[str] = Field(default=[], alias="pitchingNotes")
    top_performers: List[TopPerformer] = Field(default=[], alias="topPerformers")
