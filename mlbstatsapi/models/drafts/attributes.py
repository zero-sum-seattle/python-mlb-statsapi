from dataclasses import dataclass, field
from typing import Optional
from pydantic import BaseModel

class Home(BaseModel):
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
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class School(BaseModel):
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
    schoolClass: Optional[str] = None
    city: Optional[str] = None
    country: str
    state: Optional[str] = None