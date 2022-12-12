from dataclasses import dataclass

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