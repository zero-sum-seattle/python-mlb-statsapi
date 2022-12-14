from dataclasses import dataclass


@dataclass
class BatSide:
    """
    A class to represent a BatSide.

    Attributes
    ----------
    code : str
        code number of the BatSide
    descritpion: str
        description of the BatSide
    """
    code: str
    description: str


@dataclass
class PitchHand:
    """
    A class to represent a PitchHand.

    Attributes
    ----------
    code : str
        code number of the PitchHand
    descritpion: str
        description of the PitchHand
    """
    code: str
    description: str


@dataclass
class Position:
    """
    A class to represent a batside.

    Attributes
    ----------
    code: str
        code number of the Position
    name: str
        the name of the Position
    type: str
        the type of the Position
    abbreviation: str
        the abbreviation of the Position
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
    code: str
        code of the player
    description: str
        description of the status
    """
    code: str
    description: str

@dataclass
class Home:
    """
    A home is a where a draft player is from

    Attributes
    ----------
    city : str
        The city where the player is from.
    state : str
        The state where the player is from.
    country : str
        The country where the player is from.
    """
    city: str
    state: str
    country: str

@dataclass
class School:
    """
    Represents the school the draft player is from.

    Attributes
    ----------
    name : str
        The name of the school.
    schoolclass : str
        The class the student is in.
    city : str
        The city where the school is located.
    country : str
        The country where the school is located.
    state : str
        The state where the school is located.
    """
    name: str
    schoolclass: str
    city: str
    country: str
    state: str