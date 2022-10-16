from dataclasses import dataclass

@dataclass
class PlayMatchupSide:
    """
    A class to represent a play Matchup Side.

    Attributes
    ----------
    code : str

    description : str

    """
    code: str
    description: str

@dataclass
class PlayMatchupSplits:
    """
    A class to represent a playMatchup Split.

    Attributes
    ----------
    batter : str

    pitcher : str

    menonbase : str

    """
    batter: str
    pitcher: str
    menonbase: str