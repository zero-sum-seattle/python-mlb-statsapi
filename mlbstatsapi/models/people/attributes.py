from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class BatSide(MLBBaseModel):
    """
    A class to represent a bat side.

    Attributes
    ----------
    code : str
        Code of the bat side.
    description : str
        Description of the bat side.
    """
    code: str
    description: str


class PitchHand(MLBBaseModel):
    """
    A class to represent a pitch hand.

    Attributes
    ----------
    code : str
        Code of the pitch hand.
    description : str
        Description of the pitch hand.
    """
    code: str
    description: str


class Position(MLBBaseModel):
    """
    A class to represent a position.

    Attributes
    ----------
    code : str
        Code of the position.
    name : str
        Name of the position.
    type : str
        Type of the position.
    abbreviation : str
        Abbreviation of the position.
    """
    code: str
    name: str
    type: str
    abbreviation: str


class Status(MLBBaseModel):
    """
    A class to represent player status.

    Attributes
    ----------
    code : str
        Code of the player status.
    description : str
        Description of the status.
    """
    code: str
    description: str


class Home(MLBBaseModel):
    """
    A class to represent where a draft player is from.

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


class School(MLBBaseModel):
    """
    A class to represent the school a draft player is from.

    Attributes
    ----------
    name : str
        The name of the school.
    school_class : str
        The class the student is in.
    city : str
        The city where the school is located.
    country : str
        The country where the school is located.
    state : str
        The state where the school is located.
    """
    name: str
    school_class: str = Field(alias="schoolclass")
    city: str
    country: str
    state: str
