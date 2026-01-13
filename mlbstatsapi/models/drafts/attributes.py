from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class DraftHome(MLBBaseModel):
    """
    A class representing where a draft player is from.

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
    country: str
    state: Optional[str] = None


class DraftSchool(MLBBaseModel):
    """
    A class representing the school the draft player is from.

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
    country: str
    state: Optional[str] = None
    school_class: Optional[str] = Field(default=None, alias="schoolclass")
    city: Optional[str] = None
