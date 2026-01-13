from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class PlayMatchupSplits(MLBBaseModel):
    """
    A class to represent a play matchup split.

    Attributes
    ----------
    batter : str
        Batter matchup split.
    pitcher : str
        Pitcher matchup split.
    men_on_base : str
        Men on base matchup split.
    """
    batter: str
    pitcher: str
    men_on_base: str = Field(alias="menOnBase")
