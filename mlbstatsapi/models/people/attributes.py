from dataclasses import dataclass

@dataclass
class BatSide:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    descritpion: str
        description of the batside
    """
    code: str
    description: str

@dataclass
class PitchHand:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    descritpion: str
        description of the batside
    """
    code: str
    description: str


@dataclass
class Position:
    """
    A class to represent a batside.

    Attributes
    ----------
    code : str
        code number of the batside
    """
    code: str
    name: str
    type: str
    abbreviation: str

@dataclass
class Status:
    """
    A dataclass to hold player status

    Attributes
    ----------
    code : str
        code of the player
    description : str
        description of the status
    """
    code: str
    description: str