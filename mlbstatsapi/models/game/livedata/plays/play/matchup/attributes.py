from pydantic import BaseModel

class PlayMatchupSplits(BaseModel):
    """
    A class to represent a playMatchup Split.

    Attributes
    ----------
    batter : str
        Batter matchup split
    pitcher : str
        Pitcher matchup split
    menonbase : str
        Menonbase matchup split
    """
    batter: str
    pitcher: str
    menOnBase: str